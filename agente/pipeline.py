"""Pipeline do Guarda do Lote.

carregar_lote -> triagem (regras) -> montar_dossie -> analisar (modelo) -> travar (regras) -> executar -> fila_humana
`processar_titulo` e `processar_lote` são usados pela tela e pelo eval.
"""
from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor

from pydantic import ValidationError

from agente import fonte, regras, ferramentas, prompts, llm
from agente.esquemas import Decisao

MODOS = ("llm", "regras", "demo")  # demo = só cache do modelo, sem rede


def _extrair_json(texto: str) -> dict:
    texto = texto.strip()
    if texto.startswith("```"):
        texto = texto.strip("`").split("\n", 1)[1] if "\n" in texto else texto
    ini, fim = texto.find("{"), texto.rfind("}")
    return json.loads(texto[ini:fim + 1])


def analisar(dossie: dict, titulo_id: str, modo: str = "llm") -> tuple[dict | None, dict]:
    """Chama o modelo; valida o JSON; 1 nova tentativa; senão None (vai para revisão humana)."""
    info = {"cache": False, "tentativas": 0, "erro": None}
    pedido = prompts.usuario(dossie)
    for tentativa in range(2):
        info["tentativas"] = tentativa + 1
        try:
            texto, cache = llm.chamar(prompts.SISTEMA, pedido, somente_cache=(modo == "demo"))
            info["cache"] = cache
            d = Decisao.model_validate({**_extrair_json(texto), "titulo_id": titulo_id})
            return d.model_dump(), info
        except (ValidationError, ValueError, json.JSONDecodeError) as e:
            info["erro"] = f"saída inválida: {str(e)[:200]}"
            pedido = prompts.usuario(dossie) + prompts.correcao(str(e))
        except llm.ErroModelo as e:
            info["erro"] = f"modelo indisponível: {e}"
            break
    return None, info


def processar_titulo(titulo_id: str, lote_df=None, lote_id: str | None = None, modo: str = "llm") -> dict:
    t = fonte.titulos().loc[titulo_id]
    if lote_df is None:
        ag = fonte.agenda()
        lote_id = ag[ag.titulo_id == titulo_id].lote_remessa.iloc[0]
        lote_df = fonte.lote(lote_id)
    lote_id = lote_id or lote_df.lote_remessa.iloc[0]
    f = fonte.fornecedores().loc[t.fornecedor_id]
    etapas = {}

    alertas = regras.triagem(titulo_id, lote_df)
    graves = [a for a in alertas if a.gravidade != "atencao"]
    etapas["triagem"] = {"alertas": [a.dict() for a in alertas], "precisa_analise": bool(graves)}
    base = regras.decisao_por_regras(titulo_id, alertas)

    if not graves:
        decisao = {"diagnostico": "ok", **base, "confianca": 1.0, "alertas_descartados": [], "evidencias": [],
                   "motivo": "Conferido pelas regras: NF, duplicata, cadastro e boleto sem divergência.",
                   "instrucao_suspeita_no_texto": False}
        origem = "regras"
    elif modo == "regras":
        decisao = {"diagnostico": "outro", **base, "confianca": 1.0, "alertas_descartados": [], "evidencias": [],
                   "motivo": "; ".join(a.evidencia for a in graves), "instrucao_suspeita_no_texto": False}
        origem = "regras"
    else:
        dossie = ferramentas.montar_dossie(titulo_id, alertas, lote_id)
        etapas["dossie"] = {"fontes": [k for k, v in dossie.items() if v]}
        proposta, info = analisar(dossie, titulo_id, modo)
        etapas["analise"] = {**info, "proposta": proposta}
        if proposta is None:
            decisao = {"diagnostico": "outro", "acao": "revisao_humana", "acionar": ["PS01"], "valor_corrigido": None,
                       "confianca": 0.0, "alertas_descartados": [], "evidencias": [a.evidencia for a in graves],
                       "motivo": f"O agente não conseguiu analisar ({info['erro']}); o título fica retido para revisão.",
                       "instrucao_suspeita_no_texto": False}
            origem = "revisao_humana"
        else:
            decisao = proposta
            origem = "modelo"

    final, motivo_trava = regras.travar(decisao, alertas, titulo_id)
    if motivo_trava:
        final = {**decisao, **final, "motivo": decisao.get("motivo", "")}
        origem = "trava"
    etapas["trava"] = {"acionada": bool(motivo_trava), "motivo": motivo_trava}
    if final["acao"] == "revisao_humana" and not final.get("acionar"):
        final["acionar"] = ["PS01"]

    paga = final["acao"] in regras.ACOES_QUE_PAGAM
    valor_pago = (final.get("valor_corrigido") or t.valor) if paga else 0.0
    etapas["execucao"] = {"acao": final["acao"], "simulada": True, "sai_no_lote": paga, "valor_que_sai": round(valor_pago, 2)}
    return {
        "titulo_id": titulo_id, "lote": lote_id, "fornecedor_id": t.fornecedor_id, "fornecedor": f.razao_social,
        "categoria": f.categoria, "valor": round(t.valor, 2), "vencimento": t.vencimento, "forma": t.forma_pagamento,
        "lancado_por": t.lancado_por, "decisao": final, "origem_decisao": origem,
        "fila_humana": bool(final.get("acionar")) or final["acao"] in ("solicitar_aprovacao", "revisao_humana"),
        "pessoas": [{"id": p, "nome": regras.PESSOAS.get(p, p)} for p in final.get("acionar", [])],
        "etapas": etapas,
    }


def resumo(itens: list[dict]) -> dict:
    tot = sum(i["valor"] for i in itens)
    sai = [i for i in itens if i["etapas"]["execucao"]["sai_no_lote"]]
    sozinho = [i for i in itens if not i["fila_humana"]]
    por_acao, por_pessoa = {}, {}
    for i in itens:
        a = i["decisao"]["acao"]
        por_acao.setdefault(a, {"n": 0, "valor": 0.0})
        por_acao[a]["n"] += 1
        por_acao[a]["valor"] += i["valor"]
        for p in i["pessoas"]:
            por_pessoa[p["nome"]] = por_pessoa.get(p["nome"], 0) + 1
    return {
        "titulos": len(itens), "valor_total": round(tot, 2),
        "resolvidos_sozinho": len(sozinho), "na_fila_humana": len(itens) - len(sozinho),
        "liberados": len(sai), "valor_liberado": round(sum(i["etapas"]["execucao"]["valor_que_sai"] for i in sai), 2),
        "retidos": len(itens) - len(sai), "valor_retido": round(sum(i["valor"] for i in itens if i not in sai), 2),
        "analisados_pelo_modelo": sum(1 for i in itens if "analise" in i["etapas"]),
        "travas_acionadas": sum(1 for i in itens if i["etapas"]["trava"]["acionada"]),
        "por_acao": {k: {"n": v["n"], "valor": round(v["valor"], 2)} for k, v in por_acao.items()},
        "por_pessoa": por_pessoa,
    }


def processar_lote(lote_id: str, modo: str = "llm", paralelo: int = 6) -> dict:
    lote_df = fonte.lote(lote_id)
    with ThreadPoolExecutor(paralelo) as ex:
        itens = list(ex.map(lambda tid: processar_titulo(tid, lote_df, lote_id, modo), lote_df.titulo_id))
    cab = lote_df.iloc[0]
    return {"lote": lote_id, "banco": cab.banco_pagador, "data": cab.data_prevista, "fechamento": cab.horario_fechamento,
            "modo": modo, "resumo": resumo(itens), "itens": itens}

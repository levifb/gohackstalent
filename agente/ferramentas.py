"""Ferramentas de leitura dos sistemas (nomes do ferramentas.csv) usadas para montar o dossiê."""
from __future__ import annotations

import pandas as pd

from agente import fonte, regras


def _limpo(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None and not (isinstance(v, float) and pd.isna(v)) and v != ""}


def consultar_titulo(titulo_id: str) -> dict:
    t = fonte.titulos().loc[titulo_id]
    campos = ["titulo_id", "fornecedor_id", "numero_nf_digitado", "oc_id", "parcela", "valor", "vencimento",
              "forma_pagamento", "cnpj_beneficiario_boleto", "origem_lancamento", "lancado_por", "data_lancamento", "historico"]
    return _limpo({c: t[c] for c in campos})


def consultar_fornecedor(fornecedor_id: str) -> dict:
    f = fonte.fornecedores().loc[fornecedor_id]
    campos = ["razao_social", "cnpj", "categoria", "banco", "agencia", "conta", "chave_pix", "forma_pagamento_padrao",
              "email_cadastrado", "telefone_cadastrado", "data_cadastro", "data_ultima_alteracao", "ultima_alteracao_por"]
    return _limpo({c: f[c] for c in campos})


def consultar_historico_cadastro(fornecedor_id: str, dias: int = 60) -> list[dict]:
    a = fonte.alteracoes()
    a = a[(a.fornecedor_id == fornecedor_id) & (a.data_hora >= fonte.AGORA - pd.Timedelta(days=dias))]
    return [_limpo(r) for r in a[["data_hora", "campo", "valor_anterior", "valor_novo", "alterado_por", "origem",
                                  "confirmacao_registrada", "confirmacao_como"]].astype(str).to_dict("records")]


def consultar_nf(titulo_id: str) -> dict | None:
    loc = regras.localizar_nf(fonte.titulos().loc[titulo_id])
    if not loc:
        return None
    nf = loc["nf"]
    return _limpo({"numero_nf": nf["numero_nf"], "serie": nf["serie"], "cnpj_emitente": nf["cnpj_emitente"],
                   "razao_social_emitente": nf["razao_social_emitente"], "data_emissao": nf["data_emissao"],
                   "valor_total": nf["valor_total"], "oc_informada": nf["oc_informada"],
                   "duplicata": loc["duplicata"] and {k: loc["duplicata"][k] for k in ("n_dup", "vencimento", "valor")},
                   "n_duplicatas": loc["n_duplicatas"]})


def consultar_pedido_compra(oc_id) -> dict | None:
    pcs = fonte.pedidos_compra()
    if not isinstance(oc_id, str) or oc_id not in pcs.index:
        return None
    o = pcs.loc[oc_id]
    return _limpo({c: o[c] for c in ["oc_id", "descricao", "tipo", "valor_total", "valor_mensal", "condicao_pagamento",
                                      "status", "aprovado_por"]})


def consultar_boleto_dda(titulo_id: str) -> dict | None:
    t = fonte.titulos().loc[titulo_id]
    if t.forma_pagamento != "boleto":
        return None
    reg = regras._idx_dda_linha().get(t.linha_digitavel)
    if not reg:
        return {"registrado_no_dda": False, "banco_da_linha": fonte.banco_da_linha(t.linha_digitavel)}
    return _limpo({"registrado_no_dda": True, **{k: reg[k] for k in ("banco_cobrador", "beneficiario", "cnpj_beneficiario",
                                                                    "numero_documento", "valor", "vencimento", "situacao")}})


SENSIVEL = r"banc|conta|pix|cobran[cç]a|duplicidade|parcial|n[aã]o identificad|reajuste|protesto|urgente|assistente|rob[oô]"


def listar_comunicacoes(fornecedor_id: str, limite: int = 6) -> list[dict]:
    """E-mails do fornecedor: primeiro os sensíveis (banco, conta, pagamento, reajuste, instrução), depois os mais recentes."""
    c = regras.comunicacoes_do_fornecedor(fornecedor_id)
    sens = c[c.assunto.str.contains(SENSIVEL, case=False, na=False) | c.texto.str.contains(SENSIVEL, case=False, na=False) | c.dominio_parecido]
    rotina = c.drop(sens.index)
    c = pd.concat([sens.sort_values("data_hora", ascending=False).head(limite),
                   rotina.sort_values("data_hora", ascending=False)]).head(max(limite, min(len(sens), 10)))
    return [{"data_hora": r.data_hora, "remetente": r.remetente, "dominio_parecido_com_cadastro": bool(r.dominio_parecido),
             "assunto": r.assunto, "texto": str(r.texto)[:700]} for r in c.itertuples()]


def titulos_relacionados(titulo_id: str, alertas: list) -> list[dict]:
    """Outros títulos citados nos alertas (ex.: suspeita de duplicidade), com NF e OC, para comparar lado a lado."""
    import re
    ids = sorted({x for a in alertas for x in re.findall(r"T[PS]\d{6}", a.evidencia)} - {titulo_id})
    out = []
    for x in ids[:3]:
        if x not in fonte.titulos().index:
            continue
        t = fonte.titulos().loc[x]
        out.append({"titulo": consultar_titulo(x), "status": t.status, "nota_fiscal": consultar_nf(x),
                    "pedido_compra": consultar_pedido_compra(t.oc_id)})
    return out


def montar_dossie(titulo_id: str, alertas: list, lote_id: str) -> dict:
    t = fonte.titulos().loc[titulo_id]
    return {
        "titulos_relacionados": titulos_relacionados(titulo_id, alertas),
        "lote": lote_id,
        "titulo": consultar_titulo(titulo_id),
        "alertas_da_triagem": [{k: v for k, v in a.dict().items() if k != "valor_corrigido" or v is not None} for a in alertas],
        "fornecedor": consultar_fornecedor(t.fornecedor_id),
        "alteracoes_cadastro_60d": consultar_historico_cadastro(t.fornecedor_id),
        "nota_fiscal": consultar_nf(titulo_id),
        "pedido_compra": consultar_pedido_compra(t.oc_id),
        "boleto_dda": consultar_boleto_dda(titulo_id),
        "comunicacoes_do_fornecedor": listar_comunicacoes(t.fornecedor_id),
        "lancador": regras.lancador(t),
    }


def _brl(v) -> str:
    return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def visao_sistemas(titulo_id: str, destino: str = "") -> list[dict]:
    """O mesmo título visto em cada sistema, lado a lado, com a divergência marcada pelo código.
    É o que o analista hoje confere à mão abrindo várias telas. status: ok | divergente | ausente | n/a."""
    t = fonte.titulos().loc[titulo_id]
    fs = fonte.fornecedores()
    f = fs.loc[t.fornecedor_id]
    linhas = [{"sistema": "ERP · título", "status": "ok",
               "diz": f"{f.razao_social} · CNPJ {f.cnpj} · NF {t.numero_nf_digitado or '-'} parc {t.parcela} · {_brl(t.valor)} · vence {t.vencimento} · {t.forma_pagamento}",
               "nota": f"lançado por {t.lancado_por} ({t.origem_lancamento})"}]
    # Compras
    pcs = fonte.pedidos_compra()
    if isinstance(t.oc_id, str) and t.oc_id in pcs.index:
        o = pcs.loc[t.oc_id]
        ref = o.valor_mensal if o.tipo == "contrato" and isinstance(o.valor_mensal, str) else o.valor_total
        st, nota = "ok", ""
        if str(o.cnpj_fornecedor)[:8] != f.raiz:
            st, nota = "divergente", "OC de outra empresa (CNPJ diferente do fornecedor do título)"
        elif o.status != "aprovada":
            st, nota = "divergente", f"OC {o.status}"
        linhas.append({"sistema": "Compras · OC", "status": st, "nota": nota,
                       "diz": f"{t.oc_id} · {o.nome_fornecedor} · CNPJ {o.cnpj_fornecedor} · {_brl(ref)}{' por mês' if o.tipo == 'contrato' else ''} · {o.status}"})
    else:
        linhas.append({"sistema": "Compras · OC", "status": "n/a" if f.categoria == "utilidades" else "ausente", "diz": "sem OC no título",
                       "nota": "utilidades não têm OC" if f.categoria == "utilidades" else "pagamento sem OC aprovada exige aprovação dupla"})
    # Portal NF-e
    loc = regras.localizar_nf(t)
    if loc:
        nf, dup = loc["nf"], loc["duplicata"]
        st, nota = "ok", ""
        if dup is not None and abs(float(dup["valor"]) - t.valor) > regras.TOLERANCIA_DUPLICATA:
            st, nota = "divergente", f"duplicata de {_brl(dup['valor'])}, título de {_brl(t.valor)}"
        linhas.append({"sistema": "Portal NF-e", "status": st, "nota": nota,
                       "diz": f"NF {nf['numero_nf']}/{nf['serie']} · {nf['razao_social_emitente']} · CNPJ {nf['cnpj_emitente']} · total {_brl(nf['valor_total'])}"
                              + (f" · duplicata {dup['n_dup']} {_brl(dup['valor'])} vence {dup['vencimento']}" if dup is not None else "")})
    elif t.nf_norm:
        n = fonte.notas()
        outra = n[(n.nf_norm == t.nf_norm) & (n.raiz != f.raiz)]
        if len(outra):
            o = outra.iloc[0]
            linhas.append({"sistema": "Portal NF-e", "status": "divergente", "nota": "a NF é de outra empresa: título lançado no fornecedor errado",
                           "diz": f"NF {o.numero_nf} · {o.razao_social_emitente} · CNPJ {o.cnpj_emitente} · total {_brl(o.valor_total)}"})
        else:
            linhas.append({"sistema": "Portal NF-e", "status": "ausente", "diz": f"NF {t.numero_nf_digitado} não encontrada", "nota": "pagamento sem NF exige aprovação dupla"})
    else:
        linhas.append({"sistema": "Portal NF-e", "status": "n/a" if f.categoria == "aluguel" else "ausente", "diz": "sem NF",
                       "nota": "aluguel é pago pelo boleto do contrato" if f.categoria == "aluguel" else "pagamento sem NF exige aprovação dupla"})
    # DDA
    if t.forma_pagamento == "boleto":
        reg = regras._idx_dda_linha().get(t.linha_digitavel)
        if reg is None:
            linhas.append({"sistema": "DDA (banco)", "status": "divergente", "diz": f"linha digitável do banco {fonte.banco_da_linha(t.linha_digitavel)} não registrada",
                           "nota": "boleto não registrado contra o CNPJ do Gogroup"})
        else:
            st, nota = "ok", ""
            if reg["situacao"] != "em aberto":
                st, nota = "divergente", f"boleto {reg['situacao']} em {reg['data_situacao']}"
            elif fonte.raiz_cnpj(reg["cnpj_beneficiario"]) != f.raiz:
                st, nota = "divergente", "beneficiário de outro CNPJ"
            linhas.append({"sistema": "DDA (banco)", "status": st, "nota": nota,
                           "diz": f"banco {reg['banco_cobrador']} · {reg['beneficiario']} · CNPJ {reg['cnpj_beneficiario']} · {_brl(reg['valor'])} · {reg['situacao']}"})
    else:
        linhas.append({"sistema": "DDA (banco)", "status": "n/a", "diz": f"{t.forma_pagamento.upper()}: sem boleto", "nota": ""})
    # Cadastro bancário
    alts = [a for a in consultar_historico_cadastro(t.fornecedor_id, 60) if a.get("campo") in regras.CAMPOS_BANCARIOS]
    st, nota = "ok", "sem troca de conta nos últimos 60 dias"
    if alts:
        ult = alts[-1]
        conf = ult.get("confirmacao_registrada") == "sim"
        st = "ok" if conf else "divergente"
        nota = f"conta trocada em {ult['data_hora'][:10]} via {ult.get('origem')}, " + ("confirmada" if conf else "SEM confirmação registrada")
    linhas.append({"sistema": "Cadastro bancário (ERP)", "status": st, "nota": nota,
                   "diz": f"banco {f.banco} · ag {f.agencia} · conta {f.conta}" + (f" · destino no lote: {destino}" if destino else "")})
    # Extratos
    p = regras._avulsos_por_titulo().get(titulo_id)
    linhas.append({"sistema": "Extratos (Meridiano e Litoral)", "status": "divergente" if p else "ok",
                   "diz": f"pagamento avulso de {_brl(p['valor'])} em {p['data']} ({p['descricao']})" if p else "nenhum pagamento deste título fora do lote",
                   "nota": "já pago: seguir no lote pagaria duas vezes" if p else ""})
    # Caixa de e-mail
    c = regras.comunicacoes_do_fornecedor(t.fornecedor_id)
    parecido = c[c.dominio_parecido] if len(c) else c
    linhas.append({"sistema": "Caixa de e-mail", "status": "divergente" if len(parecido) else "ok",
                   "diz": f"{len(c)} e-mails ligados ao fornecedor" + (f"; {len(parecido)} de domínio parecido ({parecido.iloc[0].remetente})" if len(parecido) else ""),
                   "nota": "domínio imitando o do cadastro" if len(parecido) else ""})
    return linhas

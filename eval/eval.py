"""Eval do Guarda do Lote contra o gabarito anotado.

uso: python -X utf8 eval/eval.py [--modo llm|regras|demo] [--casos TP1,TP2]
Imprime acerto por etapa, lista de erros e o placar em R$ do agente contra os baselines.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from agente import fonte, llm, pipeline  # noqa: E402

RELACIONAMENTO = {"produto": 3000, "frete": 1500, "embalagens": 800, "insumos_capa": 800, "aluguel": 500, "ti_saas": 400,
                  "utilidades": 400, "servicos": 300, "marketing_agencia": 300, "influenciador": 250}
CUSTO_ACIONAMENTO = 60.0
ARQUIVO = "gabarito.csv"


def carregar_gabarito():
    with open(RAIZ / "eval" / ARQUIVO, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def custo_caso(g: dict, sai: bool, acionados: set[str], valor_que_sai: float) -> dict:
    """Placar de um caso (parametros.md): dinheiro indevido + atraso de legítimo + acionamentos desnecessários."""
    t = fonte.titulos().loc[g["titulo_id"]]
    cat = fonte.fornecedores().loc[t.fornecedor_id].categoria
    esperado_sai = g["sai_no_lote"] == "sim"
    indevido = atraso = acion = 0.0
    if sai and not esperado_sai:
        if g["tipo"] == "virgula":
            loc = fonte.duplicatas()  # valor certo = duplicata; indevido = o que passou disso
            from agente import regras
            d = regras.localizar_nf(t)["duplicata"]
            indevido = max(valor_que_sai - float(d["valor"]), 0.0)
        else:
            indevido = valor_que_sai
    if sai and esperado_sai and g["valor_corrigido_esperado"]:
        certo = float(g["valor_corrigido_esperado"])
        indevido = max(valor_que_sai - certo, 0.0)
    if not sai and esperado_sai:
        v = t.valor if not g["valor_corrigido_esperado"] else float(g["valor_corrigido_esperado"])
        atraso = v * 0.02 + v * 0.01 * 7 / 30 + RELACIONAMENTO.get(cat, 300)
    esperados = set(filter(None, g["acionar_esperado"].split("|")))
    if not esperados:
        acion = CUSTO_ACIONAMENTO * len(acionados)
    return {"indevido": indevido, "atraso": atraso, "acionamentos": acion, "total": indevido + atraso + acion}


def avaliar_item(g: dict, r: dict) -> dict:
    d = r["decisao"]
    sai = r["etapas"]["execucao"]["sai_no_lote"]
    acionados = set(d.get("acionar") or [])
    acoes_ok = set(g["acao_esperada"].split("|"))
    esperados = set(filter(None, g["acionar_esperado"].split("|")))
    graves = [a for a in r["etapas"]["triagem"]["alertas"] if a["gravidade"] != "atencao"]
    ok = {
        "triagem": bool(graves) == (g["sai_no_lote"] == "nao" or bool(g["valor_corrigido_esperado"])),
        "dinheiro": sai == (g["sai_no_lote"] == "sim"),
        "acao": d["acao"] in acoes_ok,
        "pessoas": esperados <= acionados if esperados else not acionados,
        "valor": (not g["valor_corrigido_esperado"]) or (d.get("valor_corrigido") is not None and
                                                         abs(float(d["valor_corrigido"]) - float(g["valor_corrigido_esperado"])) <= 0.10),
    }
    return {"ok": ok, "custo": custo_caso(g, sai, acionados, r["etapas"]["execucao"]["valor_que_sai"]),
            "obtido": {"acao": d["acao"], "acionar": sorted(acionados), "sai": sai, "origem": r["origem_decisao"],
                       "motivo": d.get("motivo", "")[:220]}}


def baseline(g: dict, nome: str) -> dict:
    t = fonte.titulos().loc[g["titulo_id"]]
    if nome == "assinar_sem_conferir":
        return custo_caso(g, True, set(), t.valor)
    # bloquear todo alerta: qualquer alerta não-atenção retira do lote e aciona a coordenadora
    r = pipeline.processar_titulo(g["titulo_id"], modo="regras")
    graves = [a for a in r["etapas"]["triagem"]["alertas"] if a["gravidade"] != "atencao"]
    return custo_caso(g, not graves, {"PS01"} if graves else set(), t.valor)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modo", default="llm", choices=pipeline.MODOS)
    ap.add_argument("--casos", default="")
    ap.add_argument("--arquivo", default="gabarito.csv", help="gabarito.csv ou validacao.csv")
    args = ap.parse_args()
    global ARQUIVO
    ARQUIVO = args.arquivo
    gab = carregar_gabarito()
    if args.casos:
        gab = [g for g in gab if g["titulo_id"] in args.casos.split(",")]
    ini = time.time()
    linhas = []
    for g in gab:
        r = pipeline.processar_titulo(g["titulo_id"], modo=args.modo)
        linhas.append({"g": g, **avaliar_item(g, r)})
    n = len(linhas)
    # comparação honesta: o mesmo gabarito com só as regras (sem modelo)
    so_regras = [{"g": g, **avaliar_item(g, pipeline.processar_titulo(g["titulo_id"], modo="regras"))} for g in gab]
    print(f"\nEVAL · {ARQUIVO} · {n} casos · {time.strftime('%H:%M')}\n")
    print(f"  {'etapa':<10} {'agente (' + args.modo + ')':>14} {'só regras':>11}")
    for etapa in ("triagem", "dinheiro", "acao", "pessoas", "valor"):
        k = sum(l["ok"][etapa] for l in linhas)
        k2 = sum(l["ok"][etapa] for l in so_regras)
        print(f"  {etapa:<10} {f'{k}/{n}':>14} {f'{k2}/{n}':>11}")
    certos = sum(all(l["ok"].values()) for l in linhas)
    certos_regras = sum(all(l["ok"].values()) for l in so_regras)
    print(f"  {'TUDO CERTO':<10} {f'{certos}/{n}':>14} {f'{certos_regras}/{n}':>11}  [dinheiro + ação + pessoas + valor + triagem]")
    dif = [l["g"]["titulo_id"] for l, r in zip(linhas, so_regras) if all(l["ok"].values()) != all(r["ok"].values())]
    print(f"  casos em que o modelo muda o resultado: {dif or 'nenhum'}\n")

    tipos = {}
    for l in linhas:
        t = tipos.setdefault(l["g"]["tipo"], [0, 0])
        t[0] += all(l["ok"].values())
        t[1] += 1
    print("  por tipo: " + " · ".join(f"{k} {v[0]}/{v[1]}" for k, v in tipos.items()))

    erros = [l for l in linhas if not all(l["ok"].values())]
    print(f"\nERROS ({len(erros)})")
    for l in erros:
        falhou = [k for k, v in l["ok"].items() if not v]
        o = l["obtido"]
        print(f"  {l['g']['titulo_id']} [{l['g']['tipo']}] falhou em {falhou}: esperado {l['g']['acao_esperada']} "
              f"acionar={l['g']['acionar_esperado'] or '-'} sai={l['g']['sai_no_lote']} | obtido {o['acao']} "
              f"acionar={o['acionar'] or '-'} sai={'sim' if o['sai'] else 'nao'} ({o['origem']})\n      motivo: {o['motivo']}")

    def soma(cs):
        return {k: round(sum(c[k] for c in cs), 2) for k in ("indevido", "atraso", "acionamentos", "total")}
    placar = {"agente": soma([l["custo"] for l in linhas]),
              "assinar_sem_conferir": soma([baseline(l["g"], "assinar_sem_conferir") for l in linhas]),
              "bloquear_todo_alerta": soma([baseline(l["g"], "bloquear_todo_alerta") for l in linhas])}
    print("\nPLACAR EM R$ nos casos do gabarito (custo; menor é melhor)")
    for k, v in placar.items():
        print(f"  {k:<22} R$ {v['total']:>12,.2f}  (indevido {v['indevido']:,.2f} · atraso {v['atraso']:,.2f} · acionamentos {v['acionamentos']:,.2f})")
    print(f"\nmodelo: {llm.USO} · {time.time() - ini:.0f}s")

    out = RAIZ / "eval" / "resultados"
    out.mkdir(parents=True, exist_ok=True)
    arq = out / f"eval_{time.strftime('%H%M')}_{args.modo}_{ARQUIVO.split('.')[0]}.json"
    arq.write_text(json.dumps({"modo": args.modo, "n": n, "tudo_certo": certos,
                               "por_etapa": {e: sum(l["ok"][e] for l in linhas) for e in ("triagem", "dinheiro", "acao", "pessoas", "valor")},
                               "placar": placar, "uso_modelo": dict(llm.USO),
                               "erros": [{"titulo_id": l["g"]["titulo_id"], "ok": l["ok"], "obtido": l["obtido"]} for l in erros]},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"salvo em {arq.relative_to(RAIZ)}")
    if not args.casos:  # resumo do eval completo para a tela do app
        web = RAIZ / "web" / "public" / "eval.json"
        atual = json.loads(web.read_text(encoding="utf-8")) if web.exists() else {}
        atual[ARQUIVO.split(".")[0]] = {"n": n, "tudo_certo": certos, "so_regras": certos_regras, "dinheiro": sum(l["ok"]["dinheiro"] for l in linhas),
                                       "placar": placar, "em": time.strftime("%H:%M"), "modo": args.modo}
        web.write_text(json.dumps(atual, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()

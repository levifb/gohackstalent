"""Roda o agente sobre os lotes e grava o resultado para o app.

uso: python -m agente.rodar [--modo llm|regras|demo] [--lotes RM20261103-MER,...]
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from agente import fonte, llm, pipeline

RAIZ = Path(__file__).resolve().parent.parent


def exportar_casos_ao_vivo(resultado: dict):
    """Gera web/api/_casos.ts para a rota /api/reprocessar: prompt do sistema e, por título analisado pelo modelo,
    a mensagem com o dossiê, os alertas, a decisão por regras (fallback da trava) e a decisão em cache (modo demo)."""
    from agente import ferramentas, prompts, regras
    casos = {}
    for L in resultado["lotes"]:
        lote_df = fonte.lote(L["lote"])
        for i in L["itens"]:
            if "analise" not in i["etapas"]:
                continue
            alertas = regras.triagem(i["titulo_id"], lote_df)
            casos[i["titulo_id"]] = {
                "usuario": prompts.usuario(ferramentas.montar_dossie(i["titulo_id"], alertas, L["lote"])),
                "alertas": [{"codigo": a.codigo, "gravidade": a.gravidade, "contestavel": a.contestavel,
                             "valor_corrigido": a.valor_corrigido} for a in alertas],
                "valor": i["valor"],
                "base": regras.decisao_por_regras(i["titulo_id"], alertas),
                "cache": i["etapas"]["analise"]["proposta"],
                "final_cache": i["decisao"],
            }
    api = RAIZ / "web" / "api"
    api.mkdir(parents=True, exist_ok=True)
    corpo = json.dumps({"sistema": prompts.SISTEMA, "casos": casos}, ensure_ascii=False, default=str)
    (api / "_casos.ts").write_text("// gerado por agente/rodar.py; não editar à mão\nconst dados = " + corpo + " as const;\nexport default dados;\n",
                                   encoding="utf-8")
    print(f"casos ao vivo: {len(casos)} títulos em web/api/_casos.ts")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modo", default="llm", choices=pipeline.MODOS)
    ap.add_argument("--lotes", default="")
    args = ap.parse_args()
    lotes = args.lotes.split(",") if args.lotes else sorted(fonte.agenda().lote_remessa.unique())
    ini = time.time()
    resultado = {"gerado_em": time.strftime("%Y-%m-%d %H:%M"), "agora_ficticio": str(fonte.AGORA), "modo": args.modo,
                 "lotes": []}
    for L in lotes:
        r = pipeline.processar_lote(L, args.modo)
        s = r["resumo"]
        print(f"{L}: {s['titulos']} títulos | sozinho {s['resolvidos_sozinho']} | fila {s['na_fila_humana']} | "
              f"modelo {s['analisados_pelo_modelo']} | travas {s['travas_acionadas']} | retido R$ {s['valor_retido']:,.2f}")
        resultado["lotes"].append(r)
    todos = [i for r in resultado["lotes"] for i in r["itens"]]
    resultado["semana"] = pipeline.resumo(todos)
    from agente import sentinela
    emails = sentinela.rodar(args.modo)
    resultado["sentinela"] = {"resumo": sentinela.resumo(emails),
                              "itens": [e for e in emails if e["acao"] not in ("nada",)]}
    print("sentinela:", resultado["sentinela"]["resumo"])
    resultado["uso_modelo"] = dict(llm.USO)
    resultado["segundos"] = round(time.time() - ini, 1)
    (RAIZ / "saida").mkdir(exist_ok=True)
    (RAIZ / "saida" / "resultado.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    web = RAIZ / "web" / "public"
    web.mkdir(parents=True, exist_ok=True)
    (web / "resultado.json").write_text(json.dumps(resultado, ensure_ascii=False, default=str), encoding="utf-8")
    exportar_casos_ao_vivo(resultado)
    print("semana:", json.dumps(resultado["semana"], ensure_ascii=False))
    print("uso do modelo:", resultado["uso_modelo"], "| segundos:", resultado["segundos"])


if __name__ == "__main__":
    main()

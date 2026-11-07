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
    resultado["uso_modelo"] = dict(llm.USO)
    resultado["segundos"] = round(time.time() - ini, 1)
    (RAIZ / "saida").mkdir(exist_ok=True)
    (RAIZ / "saida" / "resultado.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    web = RAIZ / "web" / "public"
    web.mkdir(parents=True, exist_ok=True)
    (web / "resultado.json").write_text(json.dumps(resultado, ensure_ascii=False, default=str), encoding="utf-8")
    print("semana:", json.dumps(resultado["semana"], ensure_ascii=False))
    print("uso do modelo:", resultado["uso_modelo"], "| segundos:", resultado["segundos"])


if __name__ == "__main__":
    main()

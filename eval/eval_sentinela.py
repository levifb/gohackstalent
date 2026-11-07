"""Eval da sentinela de comunicações: python -X utf8 eval/eval_sentinela.py"""
import csv, json, sys, time
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from agente import sentinela, llm  # noqa: E402

itens = sentinela.rodar("llm")
by = {i["comunicacao_id"]: i for i in itens}
g = list(csv.DictReader(open(RAIZ / "eval" / "gabarito_sentinela.csv", encoding="utf-8")))
ok = 0
for r in g:
    i = by[r["comunicacao_id"]]
    esp = set(filter(None, r["acionar_esperado"].split("|")))
    certo = i["acao"] == r["acao_esperada"] and (esp <= set(i["acionar"]) if esp else not i["acionar"])
    ok += certo
    if not certo:
        print("ERRO", r["comunicacao_id"], "esperado", r["acao_esperada"], sorted(esp), "| obtido", i["acao"], i["acionar"], i["jev"])
print(f"SENTINELA: {ok}/{len(g)} · resumo {sentinela.resumo(itens)}")
print("uso Jev:", {k: llm.USO[k] for k in ("jev_chamadas", "jev_input_tokens", "jev_usd", "cache")})
web = RAIZ / "web" / "public" / "eval.json"
atual = json.loads(web.read_text(encoding="utf-8")) if web.exists() else {}
atual["sentinela"] = {"n": len(g), "tudo_certo": ok, "em": time.strftime("%H:%M")}
web.write_text(json.dumps(atual, ensure_ascii=False, indent=1), encoding="utf-8")

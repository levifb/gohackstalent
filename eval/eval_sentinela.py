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
import re  # noqa: E402
from agente import fonte  # noqa: E402


def sem_jev(e):
    """Baseline sem IA: só cadastro, anexo e palavras-chave (o que se escreveria sem o modelo)."""
    fid, no_cad = sentinela._fornecedor_do_email(e["remetente"])
    txt = f"{e['assunto']} {e['texto']}".lower()
    anexo = str(e.get("anexos") or "").lower()
    if not no_cad and (fid or any(x in anexo for x in (".zip", ".exe"))):
        return "alerta_golpe", ["PS01", "PS08"]
    if re.search(r"assistente de ia|rob[oô]|sem conferir", txt):
        return "alerta_injecao", ["PS01", "PS08"]
    if re.search(r"dados banc|domic[ií]lio banc|nova conta|recebimentos no banco", txt):
        c = sentinela._troca_confirmada_depois(fid, e["data_hora"]) if fid else None
        return ("troca_confirmada", []) if c == "sim" else ("pedir_confirmacao_troca", ["PS01"])
    if re.search(r"duplicidade|parcial|n[aã]o identificad", txt):
        return "conciliar", ["PS09"]
    return "nada", []


emails = {e["comunicacao_id"]: e for e in fonte.comunicacoes().to_dict("records")}
ok_b = 0
for r in g:
    acao, acionar = sem_jev(emails[r["comunicacao_id"]])
    esp = set(filter(None, r["acionar_esperado"].split("|")))
    ok_b += acao == r["acao_esperada"] and (esp <= set(acionar) if esp else not acionar)
dif_semana = sum(1 for i in itens if sem_jev(emails[i["comunicacao_id"]])[0] != i["acao"])
print(f"SENTINELA: com Jev {ok}/{len(g)} · sem Jev (palavras-chave) {ok_b}/{len(g)} · e-mails da caixa com decisão diferente: {dif_semana} de {len(itens)}")
for i in itens:
    b = sem_jev(emails[i["comunicacao_id"]])[0]
    if b != i["acao"]:
        print(f"  {i['comunicacao_id']} {i['assunto'][:50]!r}: com Jev {i['acao']} · sem Jev {b}")
print(f"resumo {sentinela.resumo(itens)}")

# robustez: 12 e-mails fictícios criados por nós, com o mesmo pedido escrito de outro jeito
# e e-mails normais que contêm as palavras-gatilho (eval/variacoes_emails.csv)
var = list(csv.DictReader(open(RAIZ / "eval" / "variacoes_emails.csv", encoding="utf-8")))
ok_v = ok_vb = 0
print()
print("ROBUSTEZ (variações escritas por nós)")
for r in var:
    i = sentinela.analisar_email(r, "llm")
    b, bacion = sem_jev(r)
    esp = set(filter(None, r["acionar_esperado"].split("|")))
    cj = i["acao"] == r["acao_esperada"] and (esp <= set(i["acionar"]) if esp else not i["acionar"])
    cb = b == r["acao_esperada"] and (esp <= set(bacion) if esp else not bacion)
    ok_v += cj
    ok_vb += cb
    print(f"  {r['comunicacao_id']} esperado {r['acao_esperada']:<24} com Jev {i['acao']:<24}{'ok ' if cj else 'ERRO'} | sem Jev {b:<24}{'ok' if cb else 'ERRO'}")
print(f"ROBUSTEZ: com Jev {ok_v}/{len(var)} · sem Jev {ok_vb}/{len(var)}")
print("uso Jev:", {k: llm.USO[k] for k in ("jev_chamadas", "jev_input_tokens", "jev_usd", "cache")})
web = RAIZ / "web" / "public" / "eval.json"
atual = json.loads(web.read_text(encoding="utf-8")) if web.exists() else {}
atual["sentinela"] = {"n": len(g), "tudo_certo": ok, "sem_jev": ok_b, "robustez_n": len(var), "robustez_jev": ok_v, "robustez_sem_jev": ok_vb, "em": time.strftime("%H:%M")}
web.write_text(json.dumps(atual, ensure_ascii=False, indent=1), encoding="utf-8")

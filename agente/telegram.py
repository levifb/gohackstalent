"""Canal do time: o agente publica no Telegram o resumo do lote e a fila de aprovação, com botões.

uso: python -X utf8 -m agente.telegram [--lote RM20261103-MER] [--webhook]
Os cliques nos botões chegam em web/api/telegram.ts (Vercel), que responde no próprio chat.
Ações simuladas: nenhum sistema real é alterado.
"""
from __future__ import annotations

import argparse
import html
import json
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")
APP = "https://guarda-do-lote.vercel.app"

ROTULO = {"bloquear_titulo": "🔴 BLOQUEADO", "retirar_do_lote": "🔴 RETIRADO DO LOTE", "cancelar_titulo": "🟠 CANCELADO (duplicidade)",
          "revisao_humana": "🟠 REVISÃO HUMANA", "solicitar_aprovacao": "🔵 AGUARDA APROVAÇÃO"}
ORDEM = {"bloquear_titulo": 0, "retirar_do_lote": 1, "cancelar_titulo": 2, "revisao_humana": 3, "solicitar_aprovacao": 4}


def _api(metodo: str, **dados):
    tok = os.environ["TELEGRAM_BOT_TOKEN"]
    r = httpx.post(f"https://api.telegram.org/bot{tok}/{metodo}", json=dados, timeout=30)
    d = r.json()
    if not d.get("ok"):
        raise RuntimeError(f"Telegram {metodo}: {d.get('description')}")
    return d["result"]


def brl(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def publicar(lote_id: str):
    chat = os.environ["TELEGRAM_CHAT_ID"]
    res = json.loads((RAIZ / "saida" / "resultado.json").read_text(encoding="utf-8"))
    L = next(l for l in res["lotes"] if l["lote"] == lote_id)
    r = L["resumo"]
    fila = sorted([i for i in L["itens"] if i["fila_humana"]], key=lambda i: (ORDEM.get(i["decisao"]["acao"], 9), -i["valor"]))
    data = "/".join(reversed(L["data"].split("-")[1:]))
    _api("sendMessage", chat_id=chat, parse_mode="HTML", disable_web_page_preview=True, text=(
        f"<b>Guarda do Lote · {html.escape(L['banco'])} · {data} {L['fechamento']}</b>\n"
        f"Conferi os {r['titulos']} títulos ({brl(r['valor_total'])}).\n"
        f"✅ {r['resolvidos_sozinho']} resolvidos sozinho ({r['liberados']} saem no lote, {brl(r['valor_liberado'])})\n"
        f"✋ {r['na_fila_humana']} precisam de uma pessoa, abaixo.\n"
        f"<i>Dados fictícios do GoHacks; ações simuladas.</i> <a href=\"{APP}\">Abrir o painel</a>"))
    for i in fila:
        d = i["decisao"]
        pessoas = ", ".join(p["nome"].split(",")[0] for p in i["pessoas"]) or "Renata Paiva"
        botoes = ([{"text": "Aprovar", "callback_data": f"ap:{i['titulo_id']}"}, {"text": "Recusar", "callback_data": f"rc:{i['titulo_id']}"}]
                  if d["acao"] == "solicitar_aprovacao" else
                  [{"text": "Manter retido", "callback_data": f"mr:{i['titulo_id']}"}, {"text": "Liberar mesmo assim", "callback_data": f"lb:{i['titulo_id']}:{d['acao']}"}])
        _api("sendMessage", chat_id=chat, parse_mode="HTML", reply_markup={"inline_keyboard": [botoes]}, text=(
            f"{ROTULO.get(d['acao'], d['acao'])} · <b>{brl(i['valor'])}</b>\n"
            f"<b>{html.escape(i['fornecedor'])}</b> · {i['titulo_id']}\n\n"
            f"{html.escape(d['motivo'])}\n\n"
            f"👤 Para: {html.escape(pessoas)}"))
    print(f"publicado: 1 resumo + {len(fila)} casos no chat {chat}")


def configurar_webhook():
    url = f"{APP}/api/telegram"
    _api("setWebhook", url=url, secret_token=os.environ["TELEGRAM_WEBHOOK_SECRET"], allowed_updates=["callback_query", "message"])
    print("webhook:", _api("getWebhookInfo")["url"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lote", default="RM20261103-MER")
    ap.add_argument("--webhook", action="store_true")
    a = ap.parse_args()
    if a.webhook:
        configurar_webhook()
    else:
        publicar(a.lote)

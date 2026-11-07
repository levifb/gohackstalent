"""Cliente do modelo: AI Proxy do evento (formato OpenAI), seguindo a skill ai-proxy.

- chat: POST {AI_PROXY_URL}/chat/completions
- jev:  POST {AI_PROXY_URL}/systemone (decisão tipada, barata; usado como roteador)
Cada chamada imprime uma linha de custo e soma no total da sessão (USO).
Cache em disco por hash do pedido: reexecutar o eval ou a demo não gasta token.
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")
CACHE = Path(os.environ.get("CACHE_LLM_DIR", RAIZ / "saida" / "cache_llm"))
USO = {"chamadas": 0, "cache": 0, "prompt_tokens": 0, "completion_tokens": 0, "reasoning_tokens": 0,
       "jev_chamadas": 0, "jev_input_tokens": 0, "jev_usd": 0.0}
_trava = threading.Lock()
SILENCIOSO = os.environ.get("LLM_SILENCIOSO") == "1"


class ErroModelo(RuntimeError):
    pass


def _config():
    url = os.environ.get("AI_PROXY_URL", "https://ai-proxy.gogroupbr.com/v1").rstrip("/")
    tok = os.environ.get("AI_PROXY_API_KEY", "")
    modelo = os.environ.get("AI_MODEL", "gpt-6-astra")
    if not tok:
        raise ErroModelo("AI_PROXY_API_KEY ausente (.env ou vercel env)")
    if "deepseek" in modelo.lower():
        raise ErroModelo("modelos deepseek-* estão bloqueados no evento")
    return url, tok, modelo


def _linha_custo(txt: str):
    if not SILENCIOSO:
        try:
            print(txt, flush=True)
        except UnicodeEncodeError:  # console do Windows em cp1252
            print(txt.replace("💲", "$").encode("ascii", "replace").decode(), flush=True)


def _post(caminho: str, corpo: dict, timeout: float) -> httpx.Response:
    url, tok, _ = _config()
    ultimo = None
    for tentativa in range(4):
        try:
            r = httpx.post(f"{url}{caminho}", json=corpo, timeout=timeout,
                           headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
            if r.status_code == 200:
                return r
            ultimo = f"HTTP {r.status_code}: {r.text[:200]}"
            if r.status_code == 429:
                espera = float(r.headers.get("x-ratelimit-reset", 5) or 5)
                time.sleep(min(max(espera, 1), 60))
                continue
            if r.status_code in (400, 401, 403, 404, 413):
                break
        except httpx.HTTPError as e:
            ultimo = repr(e)
        time.sleep(2 * (tentativa + 1))
    raise ErroModelo(ultimo or "falha desconhecida")


def chamar(sistema: str, usuario: str, *, usar_cache: bool = True, somente_cache: bool = False,
           temperatura: float = 0.0, timeout: float = 90.0) -> tuple[str, bool]:
    """Chat. Devolve (texto da resposta, veio_do_cache)."""
    modelo = os.environ.get("AI_MODEL", "gpt-6-astra")
    chave = hashlib.sha256(json.dumps([modelo, sistema, usuario, temperatura]).encode()).hexdigest()[:24]
    arq = CACHE / f"{chave}.json"
    if usar_cache and arq.exists():
        with _trava:
            USO["cache"] += 1
        return json.loads(arq.read_text(encoding="utf-8"))["texto"], True
    if somente_cache:
        raise ErroModelo("resposta não está no cache (modo demo)")
    corpo = {"model": modelo, "temperature": temperatura,
             "messages": [{"role": "system", "content": sistema}, {"role": "user", "content": usuario}]}
    r = _post("/chat/completions", corpo, timeout)
    d = r.json()
    texto = d["choices"][0]["message"]["content"]
    u = d.get("usage") or {}
    rac = (u.get("completion_tokens_details") or {}).get("reasoning_tokens", 0) or 0
    servido = r.headers.get("x-model-served", d.get("model", modelo))
    with _trava:
        USO["chamadas"] += 1
        USO["prompt_tokens"] += u.get("prompt_tokens", 0)
        USO["completion_tokens"] += u.get("completion_tokens", 0)
        USO["reasoning_tokens"] += rac
        sess = USO["prompt_tokens"] + USO["completion_tokens"]
        n = USO["chamadas"]
    _linha_custo(f"💲 {servido} · entrada {u.get('prompt_tokens', 0)} tok · saída {u.get('completion_tokens', 0)} tok"
                 f" (raciocínio {rac}) · sem preço por chamada | sessão: {n} chamadas, {sess:,} tok")
    CACHE.mkdir(parents=True, exist_ok=True)
    arq.write_text(json.dumps({"modelo": servido, "texto": texto, "uso": u, "em": time.strftime("%Y-%m-%d %H:%M:%S")},
                              ensure_ascii=False), encoding="utf-8")
    return texto, False


def jev(state, questions: dict, *, usar_cache: bool = True, somente_cache: bool = False, timeout: float = 30.0) -> tuple[dict, bool]:
    """Jev (/systemone): decisão tipada (choice, score, noul). Devolve (answers, veio_do_cache)."""
    chave = hashlib.sha256(json.dumps(["jev", state, questions], sort_keys=True, default=str).encode()).hexdigest()[:24]
    arq = CACHE / f"jev_{chave}.json"
    if usar_cache and arq.exists():
        with _trava:
            USO["cache"] += 1
        return json.loads(arq.read_text(encoding="utf-8"))["answers"], True
    if somente_cache:
        raise ErroModelo("resposta do Jev não está no cache (modo demo)")
    r = _post("/systemone", {"state": state, "questions": questions}, timeout)
    d = r.json()
    u = d.get("usage") or {}
    usd = float(u.get("estimated_cost_usd") or r.headers.get("x-estimated-cost-usd") or 0)
    with _trava:
        USO["jev_chamadas"] += 1
        USO["jev_input_tokens"] += u.get("input_tokens", 0)
        USO["jev_usd"] += usd
        tot = USO["jev_usd"]
    _linha_custo(f"💲 {d.get('model', 'jev')} · entrada {u.get('input_tokens', 0)} tok · US$ {usd:.7f} | sessão Jev: US$ {tot:.7f}")
    CACHE.mkdir(parents=True, exist_ok=True)
    arq.write_text(json.dumps({"answers": d["answers"], "uso": u}, ensure_ascii=False), encoding="utf-8")
    return d["answers"], False

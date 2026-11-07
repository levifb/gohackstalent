---
name: ai-proxy
description: "Como usar o AI Proxy (https://ai-proxy.gogroupbr.com) em qualquer projeto — chat/texto (GPT, GLM, MiMo, Kimi), visão, gerar e editar imagem, chamada assíncrona (chat/jobs e images/jobs), Goal (tarefa longa autônoma) e Jev (decisões estruturadas em ms: classificar, pontuar, sim/não), informando o custo de cada chamada. Use SEMPRE que for chamar um LLM pelo proxy num app, script ou automação, quando aparecer \"ai proxy\", \"ai-proxy\", \"gw-tok\", \"Jev\", \"systemone\", \"goal\", \"glm\", \"kimi\", \"mimo\", ou quando precisar classificar/rotear/pontuar itens em lote barato."
---

# AI Proxy

Porta única de IA no formato OpenAI. Base URL: `https://ai-proxy.gogroupbr.com/v1`. Qualquer SDK OpenAI funciona trocando `base_url` + `api_key`.

## Regras do evento (sempre)

1. **DeepSeek bloqueado.** Nunca use `deepseek-v4-pro`, `deepseek-v4.1-flash` nem qualquer `deepseek-*`, mesmo que apareça em `/v1/models` ou o usuário peça. Se pedirem, diga que está fora do evento e ofereça `glm-5.3` (texto) ou `kimi-for-coding` (código). Ao listar modelos, esconda os `deepseek-*`.
2. **Informe o custo de toda chamada** (ver "Custo" abaixo). Em código, imprima/registre o uso de cada chamada.
3. **Token nunca em código versionado**, log, print ou resposta ao usuário.

## Token

- Header: `Authorization: Bearer <token>` + `Content-Type: application/json`.
- O token `gw-tok-...` é entregue pela organização do evento. Procure antes de pedir: variável `AI_PROXY_API_KEY` no ambiente ou no `.env`/`.env.local` do projeto. Não achou → peça ao usuário e guarde em `.env` (fora do git).
- Se o seu ambiente bloquear rede (sandbox), libere o host `ai-proxy.gogroupbr.com`.

## Qual endpoint usar

| Preciso de… | Endpoint | Modo |
|---|---|---|
| Texto: resumo, redação, extração, chat | `POST /v1/chat/completions` | síncrono |
| Texto que demora (raciocínio, lote, plataforma que corta requisição longa) | `POST /v1/chat/jobs` + `GET /v1/chat/jobs/{id}?wait=25` | assíncrono |
| **Decisão tipada** (classificar, pontuar, sim/não) | `POST /v1/systemone` (Jev) | síncrono, ~0,5s |
| Tarefa longa autônoma (pesquisa web, navegar) | `POST /v1/goals` + `GET /v1/goals/{id}` | assíncrono |
| Gerar imagem | `POST /v1/images/generations` | síncrono (corta em ~125s) |
| Editar imagem | `POST /v1/images/edits` | síncrono (corta em ~125s) |
| Imagem pesada (gerar ou editar, >2 min) | `POST /v1/images/jobs` + `GET /v1/images/jobs/{id}?wait=25` | assíncrono |

Regra prática: **precisa de texto → chat. Precisa de decisão dentro do código → Jev.**

## Modelos (chat)

`GET /v1/models` lista. `latest` aponta sempre pro mais avançado (hoje `gpt-6-astra`) — use em app; fixe o nome só se precisar de versão estável.

- **GPT:** `latest`, `gpt-6-astra`, `gpt-6-sol`, `gpt-6-luna`, `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`. `gpt-5.6-sol` é raciocínio (60–95s) → use `chat/jobs`.
- **Extras (troque só o `model`; funcionam em `/v1/chat/jobs` e com `stream`):**

| model | O que é |
|---|---|
| `glm-5.3` | GLM mais capaz. **Só texto** (imagem → 400; use o flash) |
| `glm-5.3-flash` | GLM rápido. Texto + imagem |
| `mimo-v2.6-pro` | MiMo (Xiaomi) mais capaz. Texto + imagem |
| `mimo-v2.6-flash` | MiMo rápido. Texto + imagem |
| `k3.1-pro` | Kimi K3.1 Pro. Sempre raciocina. Texto, imagem, ferramentas |
| `kimi-for-coding` | Kimi rápido, foco em código. Texto, imagem, ferramentas |

- Nos extras: mande `max_tokens` **≥ 2000** (o raciocínio consome tokens antes da resposta) e, se quiser, `reasoning_effort` (`minimal`…`high`). A resposta vem em `content`; o raciocínio vem à parte em `reasoning_content` (ignore).
- Jev não aparece em `/v1/models`; o `/v1/systemone` sempre usa `jev-latest`.

## Custo — informe a cada chamada

Depois de cada chamada, mostre ao usuário uma linha assim, e o total acumulado da sessão (some tokens de chat e US$ separados; não converta um no outro):

```
💲 glm-5.3-flash · entrada 18 tok · saída 179 tok (raciocínio 176) · sem preço por chamada | sessão: 3 chamadas, 1.240 tok
💲 jev-1.14.0 · entrada 280 tok · US$ 0,0000118 | sessão: US$ 0,0000352
```

- **Onde ler:**
  - Chat: `usage.prompt_tokens`, `usage.completion_tokens`, `usage.completion_tokens_details.reasoning_tokens`. Em `chat/jobs`, fica em `completion.usage`. O header `x-model-served` diz qual modelo rodou de fato.
  - Jev: `usage.input_tokens` e `usage.estimated_cost_usd` (também no header `x-estimated-cost-usd`).
  - Qualquer endpoint: se vier `usage.estimated_cost_usd` ou o header `x-estimated-cost-usd`, mostre o valor em US$.
- **Chat (GPT, GLM, MiMo, Kimi):** o proxy devolve só tokens, sem preço por chamada. Mostre os tokens e escreva "sem preço por chamada". **Nunca invente valor em US$.**
- **Jev:** US$ 0,042 por 1M tokens de entrada; saída grátis. É estimativa, não fatura.
- Em código (Python, SDK OpenAI):

```python
import os
from openai import OpenAI

client = OpenAI(base_url="https://ai-proxy.gogroupbr.com/v1", api_key=os.environ["AI_PROXY_API_KEY"])
r = client.chat.completions.create(model="latest", messages=[{"role": "user", "content": "Resuma em 1 frase: ..."}])
print(r.choices[0].message.content)
u = r.usage
print(f"💲 {r.model} · entrada {u.prompt_tokens} tok · saída {u.completion_tokens} tok")
```

## Chat — `/v1/chat/completions`

```json
{ "model": "latest", "messages": [{ "role": "user", "content": "..." }] }
```
Resposta: `choices[0].message.content`. Formato OpenAI.

**Visão:** `content` vira lista:
```json
[{ "type": "text", "text": "pergunta" },
 { "type": "image_url", "image_url": { "url": "data:image/png;base64,..." } }]
```

## Chat assíncrono — `/v1/chat/jobs`

1. `POST /v1/chat/jobs` com o mesmo body do chat (`stream` é ignorado) + header `Idempotency-Key: <uuid>` (opcional, 1–200 caracteres) → `202 { id: "chatjob-…", status: "pending", poll }`.
2. `GET /v1/chat/jobs/{id}?wait=25` (wait 0–25s) em loop sem pausa enquanto `pending`/`running`. O GET não consome cota.
3. `done` → texto em `completion.choices[0].message.content` (`completion` = objeto do chat normal; `model` diz qual rodou).
- Erro: `status: "error"` com `error.type` (`timeout`, `server_restart` ou erro do upstream) e `error.retryable`. `true` → reenviar o MESMO POST com a MESMA chave (máx. ~3). `false` → corrigir o pedido.
- POST: 400 body inválido · 409 mesma chave com body diferente · 429 rate limit ou `too_many_open_jobs`.
- Máx. 24 jobs abertos por token (**somando chat e imagem**). Job ≤10 min; resultado guardado 1h (depois 404). Só o token que criou lê o job.

## Jev — `/v1/systemone` (decisão estruturada)

Não gera texto. Manda `state` (string, objeto ou array) + `questions`; devolve a decisão com probabilidade. Várias perguntas na mesma chamada = uma requisição. Custo só por input. **Não** mande `messages`; `model` é opcional.

```json
{
  "state": { "mensagem": "Meu pedido chegou quebrado, quero o dinheiro de volta", "canal": "email" },
  "questions": {
    "assunto":  { "type": "choice", "instructions": "Assunto principal da mensagem",
                  "criteria": { "reembolso": "pede dinheiro de volta", "troca": "quer trocar o produto", "duvida": "só tem uma pergunta" } },
    "urgencia": { "type": "score", "instructions": "Urgência do atendimento", "criteria": ["baixa", "média", "alta"] },
    "reclamacao": { "type": "noul", "instructions": "É uma reclamação?" }
  }
}
```

Resposta:
```json
{ "model": "jev-1.14.0",
  "answers": {
    "assunto":    { "type": "choice", "choice": "reembolso", "confidence": 0.81, "probabilities": { "reembolso": 0.86, ... } },
    "urgencia":   { "type": "score", "score": 1.6, "legend": { "0": "baixa", "1": "média", "2": "alta" }, "probabilities": { ... } },
    "reclamacao": { "type": "noul", "noul": 0.95 } },
  "usage": { "input_tokens": 368, "output_tokens": 63, "estimated_cost_usd": 0.0000155 } }
```
- `choice` → `answers.<id>.choice` (chave de `criteria`; use nomes que o código entenda).
- `score` → `answers.<id>.score` de 0 ao índice do último nível (mín. 2 níveis).
- `noul` → `answers.<id>.noul` = probabilidade de "sim".
- Use `confidence` para mandar pra revisão humana (ex.: < 0,7).
- Erros: 400 body/pergunta mal formada (ler `error.message`/`error.upstream`) · 413 body > 200 mil caracteres · 429 cota, esperar · 503 sobrecarga, backoff · 502 falha no upstream.
- Bom para: triagem, roteamento, moderação, classificar lista grande item a item. **Não** use para calcular valores.

## Goal — `/v1/goals`

1. `POST { "objective": "objetivo completo" }` → `{ id, status: "pending" }`.
2. `GET /v1/goals/{id}` a cada 5–10s até `done` (ou `error`) → `result`, `goal_status`, `artifacts`. Navegação pode levar minutos.

## Imagens

- Gerar: `POST /v1/images/generations` `{ "prompt": "...", "size": "1024x1024", "n": 1 }` → `data[0].b64_json` (PNG em base64).
- Editar: `POST /v1/images/edits` `{ "prompt": "o que alterar", "image": "URL /images/ do proxy | data URI | base64" }` → `data[0].b64_json`.
- Rotas síncronas são cortadas em ~125s pela rede (erro **524**). Pode passar de 2 min → use a assíncrona:
  1. `POST /v1/images/jobs` + `Idempotency-Key` — mesmo body de generations (`prompt`, `size`, `quality`, `model`, `n`); com `image` ou `images` vira edição → `202 { id: "imgjob-…", status, poll }`.
  2. `GET /v1/images/jobs/{id}?wait=25` até `done` → `{ kind, data: [{ url, revised_prompt }] }`. `?b64=1` traz também `b64_json`.
  - `data[i].url` vale **48h** — baixe/guarde antes. Idempotência, retry, limite de 24 jobs, 10 min e 1h iguais ao chat/jobs.

## Limites

- Rate limit por token (hoje 250 req/min), nos headers `x-ratelimit-limit`, `x-ratelimit-remaining`, `x-ratelimit-reset`. O token pode ser dividido com outras pessoas do evento: em 429, espere `x-ratelimit-reset` segundos e tente de novo; em lote, controle a concorrência.

## Teste rápido

```bash
curl -s https://ai-proxy.gogroupbr.com/v1/chat/completions \
  -H "Authorization: Bearer $AI_PROXY_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"latest","messages":[{"role":"user","content":"ping"}]}'
```
Mostre a resposta e a linha 💲 com os tokens de `usage`.

@prompts/claude_contexto_hackathon.md

# Guarda do Lote (GoHacks Talent 2026)

- **Desafio:** Pagamentos (enunciado em `materiais/desafios.md`; dados fictícios em `dados/pagamentos/`, fora do git).
- **Recorte:** agente que confere cada título do lote de remessa antes do fechamento do banco (lote de demo `RM20261103-MER`: 192 títulos, R$ 2,24 mi, fecha 10h de 03/11), libera sozinho o normal, corrige/retira o que tem erro e manda os casos de risco para a pessoa certa.
- **Persona:** Marcos Teles, tesoureiro. Detalhes, métricas e suposições em `SPEC.md`; erros da IA e mudanças de rota em `LOG.md`.

## Skills

| Skill | Quando usar | Responsabilidade | Entrega |
| --- | --- | --- | --- |
| `dados-pagamentos` | ler/juntar dados, tirar números | camada de dados e achados | `agente/fonte.py`, `analise/`, "Achados dos dados" no SPEC |
| `politica-cp` | regra de negócio, trava, placar | política como código | `agente/regras.py`, `agente/placar.py`, respostas de negócio do gabarito |
| `agente-guarda-lote` | pipeline, prompts, chamada ao modelo | orquestração e IA | `agente/pipeline.py`, `ferramentas.py`, `llm.py`, `prompts.py`, `esquemas.py` |
| `eval-gabarito` | gabarito, eval, testes | conferência medida | `eval/gabarito.csv`, `eval/eval.py`, `tests/`, linhas de acerto no LOG |
| `app-vercel` | tela, API, deploy | interface e publicação | `web/`, `api/`, `vercel.json`, link sem login |
| `ai-proxy` | toda chamada ao modelo | regras do AI Proxy do evento (endpoints, Jev, custo por chamada, sem deepseek) | seguida por `agente/llm.py` |
| `apresentacao-pitch` | a partir das 15h20 | slides e roteiros | `apresentacao/` (PDF ≤ 10 slides) |

Fluxo entre skills: achados dos dados → SPEC; IDs de casos estranhos → gabarito; erros do eval → LOG.md e ajuste no prompt ou na regra; números finais (eval, placar) → tela e slides.

## Arquitetura do agente

```
carregar_lote → triagem (regras.py, sem modelo) → montar_dossie (ferramentas) → analisar (modelo, JSON)
             → travar (regras.py) → executar (ação simulada) → fila_humana (pessoa PS01..PS11 + motivo)
```
- Núcleo: `agente/pipeline.py` com `processar_lote(lote_id)` e `processar_titulo(titulo_id)`; a tela e o eval usam as mesmas funções.
- Dados: só por `agente/fonte.py`. Prompts: `agente/prompts.py`. Modelo: `agente/llm.py` (AI Proxy, `.env`). Eval: `python eval/eval.py`.
- Saídas: `saida/` (estado do lote, cache do modelo) e `web/public/resultado.json` para o app.

## Princípios

- Ponta a ponta primeiro, depois melhorar cada etapa. Commits pequenos.
- Regras que não podem errar no código; o modelo só vê títulos com alerta (economia de tokens).
- Saída do modelo em JSON validado (pydantic), 1 nova tentativa, depois revisão humana.
- Python: `.venv/Scripts/python.exe -X utf8 -m agente.rodar` (módulos do projeto; `-I` só para scripts soltos que leem `dados/`). Modelo: `gpt-6-astra` pelo AI Proxy, chave `AI_PROXY_API_KEY`; informar o custo de cada chamada. App: https://guarda-do-lote.vercel.app (deploy com `vercel deploy --prod` em `web/`). Dados ficam em `dados/` (fora do git); o app recebe só resultados processados. Token só em `.env` / `vercel env`.
- Todo número com fonte (eval, script ou estimativa explicada). Toda correção da IA vai para o LOG.md.

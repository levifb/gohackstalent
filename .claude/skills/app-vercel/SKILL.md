---
name: app-vercel
description: Interface e publicação do Guarda do Lote na Vercel: React + TypeScript (Vite) lendo o resultado do lote processado, função de servidor Python para reprocessar um título ao vivo, modo demo com cache, segredos fora do front e checagem do link sem login. Use ao criar ou mudar web/, api/, vercel.json, ao fazer deploy, ou ao ajustar a tela para a demo de 90 segundos. Não use para lógica do agente (agente-guarda-lote) nem para regras (politica-cp).
---

# App na Vercel

Dono de: `web/` (Vite + React + TS), `api/` (funções Python da Vercel), `vercel.json`, deploy e o teste dos 10 segundos.

## Arquitetura

- O lote é processado pelo pipeline Python no notebook (`python -m agente.rodar RM20261103-MER`) e grava `web/public/resultado.json` (só resultado e evidências necessárias, nunca os CSVs). A tela diz: "Lote processado pelo agente às hh:mm".
- `api/reprocessar.py` (função Python da Vercel): recebe `titulo_id`, carrega o dossiê já montado em `web/public/dossies.json` e chama o modelo via `agente/llm.py` com `AI_PROXY_*` configurados em `vercel env`. Com `?demo=1` ou se o proxy falhar, devolve a decisão em cache e a tela mostra "resposta em cache".
- Segredos: só `vercel env add AI_PROXY_TOKEN` (e URL, modelo). Nada de `VITE_` com segredo; o front nunca chama o proxy.
- Deploy com a Vercel CLI (`"$APPDATA/npm/vercel.cmd"` até reiniciar o terminal): `vercel --prod`. Conferir o link com `curl -s -o /dev/null -w "%{http_code}"` e numa janela anônima, sem login (desligar Deployment Protection se pedir login).

## Tela (a história em 10 segundos)

Topo: "Marcos Teles, tesoureiro · Lote Banco Meridiano 03/11 · fecha às 10:00 · 192 títulos · R$ 2,24 mi".
1. Faixa de resultado: liberados sozinhos (n, R$) | corrigidos | retidos | na fila humana; R$ protegido; placar vs. "assinar sem conferir".
2. Fila humana: cartão por caso com pessoa acionada (nome e cargo), motivo em 1 frase, evidências, botões aprovar/recusar (simulados).
3. Trilha do agente por título: etapas nomeadas (triagem → dossiê → análise → trava → ação) com o que cada uma concluiu.
4. Rodapé: "Eval: x/N casos (hh:mm)" com link para o detalhe.

Estilo: limpo, sem template genérico, sem gradiente roxo, sem emoji, sem card dentro de card. Paleta do evento (ver skill apresentacao-pitch) para tela e slides conversarem. Funciona em 1366×768 (notebook do evento e projetor).

## Critérios de qualidade

- `npm run build` sem erro; deploy abre sem login; a demo funciona com a rede desligada (cache).
- Todo número na tela vem de `resultado.json` ou do último eval; nada fixo no código.
- Nenhum segredo no repositório: `git grep -n "gw-tok"` vazio antes de cada push.

## Erros a evitar

- Painel bonito que não age: a tela precisa mostrar as ações executadas e a fila de aprovação, não só alertas.
- Dependência pesada nova sem perguntar ao Levi.
- Polir visual antes do ponta a ponta existir (meta: primeiro deploy até 12h00).

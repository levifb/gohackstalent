# Passagem de sessão (07/11/2026, ~13h50)

Leia primeiro: `CLAUDE.md` (importa `prompts/claude_contexto_hackathon.md`), `SPEC.md`, `README.md`, `LOG.md` e este arquivo. Prazos do dia: congelamento 15h20 (só correção de bug, textos, slides, pitch), **submissão 16h30**, pré-júri 16h35 a 18h10 (horário no app do evento).

## Links

| O quê | Link / id |
| --- | --- |
| Site publicado (aba "A história" + "Painel do agente") | https://guarda-do-lote.vercel.app |
| Repositório público | https://github.com/levifb/gohackstalent |
| Deck do pitch (Google Slides, 10 slides v2) | https://docs.google.com/presentation/d/1mVAGrmmNUs4j35EpH_0qqqpnHoZxF41FEcJKkLCvm7A/edit (id `1mVAGrmmNUs4j35EpH_0qqqpnHoZxF41FEcJKkLCvm7A`) |
| Brandbook do Gogroup (Google Slides da organização) | https://docs.google.com/presentation/d/1Lu9G9LwXW3lOzIkgNcaS425GpOOuDG5a4VJpT97A1_c/edit · PDF/PPTX em `C:\Users\Notebook\Downloads\[Gohacks Talent] Brandbook Gogroup.*` |
| Material do workshop de pitch | `C:\Users\Notebook\Downloads\[GoHacks Talent 2026] Pitch.pptx` |
| Bot do Telegram | @guardadolote_bot (https://t.me/guardadolote_bot), webhook em `/api/telegram` |
| AI Proxy do evento | https://ai-proxy.gogroupbr.com/v1 (skill `.claude/skills/ai-proxy`) · modelo `gpt-6-astra` · Jev em `/v1/systemone` |
| Site do evento | https://gohacks-talent-evento.devgogroup.com (dados públicos em `/api/publico`) |

Segredos ficam só em `.env` (fora do git) e no `vercel env`: `AI_PROXY_API_KEY`, `AI_PROXY_URL`, `AI_MODEL`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `TELEGRAM_WEBHOOK_SECRET`. Nunca imprimir nem versionar.

## O que pedir ao Levi logo no início (autenticação)

1. **Google Slides e Google Drive**: os conectores claude.ai precisam estar ligados na conta nova (para editar o deck acima). Testar com `read_presentation` no id do deck; se falhar, pedir para o Levi ligar os conectores e abrir o deck com a conta que tem acesso (o deck está no Drive da conta usada antes; se a conta nova não enxergar, ele precisa compartilhar o deck com ela).
2. **Vercel CLI**: `vercel whoami`; se não estiver logado, o Levi roda `! vercel login`. Deploy sempre de `web/`: `cd web && vercel deploy --prod --yes`.
3. **GitHub CLI**: `gh auth status`; se não, `! gh auth login -h github.com --git-protocol https --web`.
4. **Skills do projeto** em `.claude/skills/` (dados-pagamentos, politica-cp, agente-guarda-lote, eval-gabarito, app-vercel, apresentacao-pitch, ai-proxy). Se a conta nova tiver a skill `anthropic-skills:google-workspace`, carregar antes de editar o deck.

## Estado (tudo commitado e publicado)

- Agente: 876 títulos da semana, 815 sem humano (93%); lote das 10h de 03/11: 192 títulos, 181 sozinho, 13 no modelo, 11 na fila. Sentinela de e-mails (Jev). Telegram com botões. Reanálise ao vivo (`web/api/reprocessar.ts`).
- Eval: gabarito 30/30 (só regras 29/30); validação cega 12/12; julgamento sintético 6/6 (só regras 3/6); sentinela 17/17; robustez 12/12 (palavras-chave 1/12). Placar 30 casos: assinar sem conferir R$ 529.805; bloquear todo alerta R$ 1.493; agente R$ 0.
- Entregáveis em `entregaveis/`: `submissao.md` (contagem de caracteres), `pitch_5min.md` (v2, roteiro do workshop), `preparacao_banca.md`, `sabatina.md`, `video_2min.md`, `relatorio_individual.md`. Faltam: feedback de mentor (marcadores), PDF do deck (o Levi exporta no fim da tarde), vídeo de 2 min (opcional).

## Como o deck v2 foi feito (para editar)

- Fundos do brandbook: `web/public/marca/marca_conteudo.png` e `marca_impacto.png` (publicados em `https://guarda-do-lote.vercel.app/marca/`). Logo no canto inferior direito; os três pontinhos no canto superior esquerdo fazem parte do fundo.
- Imagens: capturas das seções do site com o modo `?so=<seção>` (`hero, dor, simulacao, casos, telegram, impacto, prova, criterios, fim`), que mostra uma seção só, já no estado final. Captura em 2x com o Edge sem janela:
  `"/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --window-size=1300,1500 --virtual-time-budget=9000 --screenshot="C:\...\arquivo.png" "http://localhost:4173/?so=telegram"` (servidor local: `cd web && npm run build && npx vite preview --port 4173`).
- O Google Slides só insere imagem por URL pública: copiar o PNG para `web/public/capturas/`, publicar (`vercel deploy --prod --yes` em `web/`) e usar `https://guarda-do-lote.vercel.app/capturas/<arquivo>.png`. Use um nome novo a cada versão (cache).
- Gerador das requisições: `apresentacao/gerar/deck_v2.py` (geometria em polegadas; página 10 × 5,625 in).
- Ids dos slides: `v2s01` … `v2s10`. Imagens: `v2s02_img` (dor), `v2s03_img2` (achados), `v2s05_img` (192 quadradinhos), `v2s07_img` (casos), `v2s08_img` (celular), `v2s09_img` (eval). Notas do apresentador já preenchidas com tempos e fontes.
- Atenção no Slides: mudar a escala de uma imagem com `updatePageElementTransform` aplica sobre o tamanho nativo (a imagem pode virar um ponto); para redimensionar, apagar e recriar com `createImage` e `size` em EMU. "R$ 661 mil" e similares usam espaço não separável (`\u00a0`) no texto; `replaceAllText` precisa do mesmo caractere. Conferir sempre pela miniatura (`read_slide_page_thumbnail`).

## Tarefas pedidas pelo Levi para a próxima sessão

1. **Slide 8 (Telegram, `v2s08_img`)**: o celular está pequeno, com cara de recorte, com fundo verde-limão em volta e os três pontinhos do carrossel embaixo. Fazer um PNG do celular **sem fundo** (transparente) e **sem os pontinhos**, e colocá-lo **maior** no slide. Caminho sugerido: no site, um modo de captura que esconda `.celular-pontos` e deixe o fundo transparente (ex.: `?so=telegram&limpo=1`, com `body`, `.h-pagina` e `.h-secao.limao` transparentes), e capturar com o Edge usando `--default-background-color=00000000`; depois recortar só o celular (bounding box dos pixels não transparentes). Alternativa: montar no PIL uma moldura de celular arredondada com o print real `apresentacao/capturas/tg_politica.png` dentro, com alpha. Altura sugerida no slide: cerca de 4,2 in, à direita, sem invadir o logo do canto inferior direito (x de 7,66 a 8,6 in, y de 4,75 a 4,97 in).
2. **Slide 5 (192 quadradinhos, `v2s05_img`)**: a imagem está pequena e com cara de recorte (borda e fundo azul do cartão do site). Deixar maior e integrada ao slide: por exemplo, recapturar só a grade (`.sim-grade`) e os números com fundo transparente, ou montar a grade direto no slide; o texto das 3 etapas pode ir para baixo ou ficar mais estreito. Manter as cores (verde = liberado, rosa = barrado, azul = aguarda a diretora).
3. Depois de cada mudança: conferir as miniaturas dos 10 slides, registrar no `LOG.md` e fazer commit + push (com a linha `Co-Authored-By` que o sistema indicar).

## Comandos úteis

- Python: `.venv/Scripts/python.exe -X utf8 -m agente.rodar --modo llm` (tudo em cache; não gasta token se nada mudou) · `-m pytest -q tests` · `eval/eval.py`, `eval/eval.py --arquivo validacao.csv`, `eval/eval.py --arquivo sinteticos.csv`, `eval/eval_sentinela.py`.
- Telegram, publicar o lote de novo: `.venv/Scripts/python.exe -X utf8 -m agente.telegram --lote RM20261103-MER`.
- Conferir segredos antes de push: `git grep -nE "gw-tok-[A-Za-z0-9]{8}|[0-9]{9,10}:AA[A-Za-z0-9_-]{20,}"` deve dar vazio (chave do proxy e token do bot).

---
name: apresentacao-pitch
description: Slides do pitch do Guarda do Lote (máx. 10 slides, PDF até 20 MB, legível no telão) no estilo direto de lançamento, com a persona Marcos Teles como herói, números do eval e dos dados com fonte nas notas, e visual inspirado no site do evento. Use a partir das 15h20 ao pedir slides, roteiro de pitch, PDF da apresentação, .pptx ou roteiro do vídeo de 2 min. Não use antes do congelamento, exceto para capturar telas do app.
---

# Apresentação do pitch

Dona de: `apresentacao/` (roteiro, HTML dos slides, PDF final, capturas). Usa fatos do `SPEC.md`, do último `eval/resultados/eval_*.json` e do `LOG.md`. Não inventa número.

## Estilo

- Uma ideia por slide. Título = frase afirmativa de até 8 palavras ("O lote das 10h sai sem conferência"), nunca rótulo ("Problema").
- Sem listas de tópicos. Use: um número grande com legenda curta, uma frase, uma captura real do app, ou "antes → depois" lado a lado.
- Herói: Marcos Teles, tesoureiro. História: a dor dele hoje → o custo → a virada ("Guarda do Lote é um agente de IA que confere cada título do lote antes do fechamento, para que o Marcos assine sem duplicidade, valor errado ou conta suspeita") → demo → número que prova → impacto → o que eu faria na segunda-feira.
- Slide da demo quase vazio ("Vamos ver funcionando"); plano B = captura ou vídeo.
- Cada número tem a fonte nas notas do apresentador (eval, comando da sonda ou LOG). Estimativa aparece como estimativa.
- Texto no estilo do contexto: sem adjetivo de vendedor, sem "não é só X, é Y", sem emoji.

## Roteiro base (ajustar com os números finais)

1. Abertura: "Às 10h, R$ 2,24 milhões saem sem conferência" (192 títulos, lote Meridiano 03/11).
2. Dor e persona: Marcos assina sem abrir os títulos (citação da política).
3. Custo: no lote agendado, 26 duplicidades (R$ 210 mil) e uma troca de conta sem confirmação (R$ 194 mil).
4. Fluxo atual em 4 passos (lançamento manual → entra no lote → assina → erro aparece no extrato).
5. Solução em uma frase + diagrama das etapas (triagem → dossiê → análise → trava → ação → fila humana).
6. Demo ("Vamos ver funcionando"): um caso comum liberado sozinho e um de risco indo para a Renata com motivo.
7. Número que prova: eval x/N e % liberado sozinho.
8. Impacto: placar em R$ do agente vs. assinar sem conferir vs. bloquear tudo.
9. Onde a IA errou e como corrigi (do LOG.md, com antes → depois).
10. Segunda-feira: plugar no ERP/DDA/CNAB, rodar às 9h antes de cada lote, aprovação no canal do time; próximas frentes (sentinela de cadastro, conciliação).

## Limites do evento

Máximo 10 slides, até 3 elementos por slide, PDF ≤ 20 MB. Estrutura do evento: problema, solução, demonstração, impacto, próximos passos; tempos do pitch de 5 min no arquivo de contexto. Legível do fundo da sala: corpo ≥ 24 pt, números de destaque ≥ 96 pt.

## Visual: brandbook do Gogroup (enviado pela organização às 12h)

O deck usa os fundos do brandbook (`apresentacao/marca/`, publicados em `guarda-do-lote.vercel.app/marca/`): `marca_conteudo.png` (moldura azul #2659a5, cartão creme, três pontinhos verde-limão, logo gogroup no canto inferior direito) nos slides de conteúdo e `marca_impacto.png` (moldura verde-limão, cartão azul, logo branco) nos slides de impacto. Regras do brandbook: escrever "Gogroup" (G maiúsculo, resto minúsculo); nunca mudar a cor, distorcer ou aplicar efeito no logo; só cores da paleta (#d7d900, #2659a5, #e5381a, #e61782, #e5273c, #f8ae13, #3dbfef, branco); cuidado com contraste (branco sobre amarelo não). Títulos em azul #2659a5 no cartão creme. Rótulos começam depois dos três pontinhos (x ≥ 1,4 in) e textos do rodapé terminam antes do logo (largura ≤ 7 in).

### Visual anterior (referência)

- Cores: azul-marinho `#1b2540` (texto e fundo dos slides de impacto), fundo claro `#f4f6fa`, cartões `#ffffff` com borda `#e5e8ef`, azul `#2659a5`, verde-limão `#d7d900` (destaque), rosa `#e61782` (alerta, pouco), ciano `#3dbfef` e âmbar `#f8ae13` (etiquetas), cinza `#6b7280` (secundário).
- Fontes: Poppins 800 nos títulos e Poppins no corpo; JetBrains Mono em caixa alta, pequena, com espaçamento, para rótulos ("ANTES", "DEPOIS", "EVAL · 25 CASOS"). Carregar do Google Fonts no HTML.
- Muito espaço em branco, cantos arredondados discretos, etiquetas pequenas coloridas, 1 ou 2 slides azul-marinho com o número principal em verde-limão. Sem gradiente, sem sombra pesada, sem ícone decorativo.

## Produção e conferência

1. Roteiro primeiro (`apresentacao/roteiro.md`) com fala e fonte de cada número; validar com o Levi.
2. Slides em HTML 16:9 (`apresentacao/slides.html`, um `<section>` por slide, 1920×1080) → PDF com Chrome/Edge headless: `msedge --headless --print-to-pdf=apresentacao/pitch.pdf --no-pdf-header-footer apresentacao/slides.html` (ou `chrome`). .pptx só se sobrar tempo (skill pptx), com notas.
3. Capturas reais do app publicado (não telas desenhadas).
4. Conferir: converter cada página em imagem e olhar uma por uma (texto cortado, sobreposição, contraste, fonte trocada); contar as páginas do PDF; tamanho < 20 MB.
5. Cronometrar as notas a ~140 palavras/min: tem que caber em 5 min com a demo.
6. Roteiro do vídeo de 2 min (plano B) no mesmo arquivo de roteiro.

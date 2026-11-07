# Prompt: o Claude cria as skills do projeto

Use depois de escolher o desafio e o recorte (`prompt_escolher_desafio.md`) e antes de escrever o SPEC. O Claude decide quais skills criar, até 5, de acordo com o desafio do dia, e cria sempre uma sexta, `apresentacao-pitch`, para os slides.

Tempo previsto: 15 a 20 minutos. Se passar de 20, peça para ele fechar com o que tiver.

---

```
Hora agora: [hh:mm]. Desafio escolhido: [nome]. Recorte: [recorte combinado].

Antes de começar o produto, crie até 5 skills do Claude Code que você julgue as melhores para
este projeto. Você escolhe quantas e quais, pensando no desafio, nos dados desta pasta e nos
critérios da banca do claude_contexto_hackathon.md. Menos skills bem feitas valem mais que cinco
genéricas: crie só as que mudam a qualidade do trabalho de hoje.

Ideias de partida (pode renomear, juntar, descartar ou criar outras):
- data-analyst: análise exploratória, pandas, NumPy, estatística, padrões, tratamento e validação
  de dados. Prioriza análises reproduzíveis e fundamentadas nos dados reais.
- business-analyst: indicadores financeiros, métricas operacionais, gargalos, priorização e impacto
  econômico. Traduz descobertas técnicas em recomendações práticas para o negócio.
- ai-agent-engineer: arquitetura e implementação de agentes que executam ações úteis, usam
  ferramentas, decidem dentro de limites definidos e produzem resultados verificáveis. Nada de
  chatbot genérico.
- fullstack-engineer: arquitetura, APIs, frontend, backend, banco de dados, UX e deploy. Prioriza
  código organizado, segurança, manutenibilidade e boa experiência de uso.
- qa-evaluation: testes automatizados, validação de cálculos, testes de integração, avaliação de
  agentes de IA e casos extremos. Confere se os resultados da aplicação são corretos e reproduzíveis.

Além dessas até 5, crie obrigatoriamente uma skill a mais: `apresentacao-pitch`, para os slides do
pitch. Ela entra em ação a partir das 15h20 e precisa estar pronta desde já, ajustada ao desafio.
O que ela deve conter:

a) Estilo: apresentação direta, no estilo dos lançamentos do Steve Jobs, que mostra o impacto real.
   - Uma ideia por slide. O título é uma frase afirmativa de no máximo 8 palavras
     ("A Ana perde 3 horas por dia com isso"), não um rótulo ("Problema").
   - Sem listas de tópicos. No lugar delas: um número grande com uma legenda curta, uma frase,
     uma imagem ou captura da tela do app, ou um "antes → depois" lado a lado.
   - O herói é a persona com nome. A história segue: a dor dela hoje, o custo, a virada (a solução
     em uma frase: "[Nome] é um agente de IA que [ação], para que [persona] [resultado]"), a demo,
     o número que prova, o impacto no negócio e o que eu faria na segunda-feira.
   - A demo é o centro. O slide dela é quase vazio ("Vamos ver funcionando"), porque a demo é ao
     vivo; o plano B é a captura ou o vídeo.
   - Cada número vem do eval, dos dados ou do LOG.md, com a fonte nas notas do apresentador.
     Estimativa aparece como estimativa. Nada de número inventado para causar efeito.
   - Texto no estilo do arquivo de contexto: sem adjetivo de vendedor, sem "não é só X, é Y",
     sem emoji.

b) Limites do evento: no máximo 10 slides, até 3 elementos por slide, PDF de até 20 MB. A estrutura
   sugerida pelo evento é problema, solução, demonstração, impacto e próximos passos, e o roteiro do
   pitch de 5 min do arquivo de contexto define o tempo de cada parte. Se eu for finalista, o PDF vai
   para o telão: tudo precisa ser legível do fundo da sala (corpo de texto com pelo menos 24 pt,
   números de destaque com 96 pt ou mais).

c) Visual com o site do evento (gohacks-talent-evento.devgogroup.com) como referência. Use a paleta e
   a tipografia como inspiração, sem copiar logotipos nem marcas do Gogroup, da Gocase ou da Gobeaut:
   - cores: azul-marinho #1b2540 (texto e fundo dos slides de impacto), fundo claro #f4f6fa,
     cartões brancos #ffffff com borda #e5e8ef, azul #2659a5, verde-limão #d7d900 (destaque, como o
     marca-texto em "em ação" no site), rosa #e61782 (alerta, usar pouco), ciano #3dbfef e
     âmbar #f8ae13 (etiquetas), cinza #6b7280 (texto secundário);
   - fontes: Poppins para títulos (peso 800) e corpo; JetBrains Mono em caixa alta, pequena e com
     espaçamento entre letras para rótulos e etiquetas (ex.: "ANTES", "DEPOIS", "EVAL · 25 CASOS");
     se as fontes não estiverem instaladas, baixe do Google Fonts ou use a alternativa sans mais próxima;
   - linguagem visual: muito espaço em branco, cantos arredondados discretos, etiquetas pequenas
     com fundo colorido, e um ou dois slides de fundo azul-marinho com o número principal em
     verde-limão para os momentos de impacto. Sem gradiente, sem sombra pesada, sem ícone decorativo.

d) Produção e conferência:
   - o entregável obrigatório é o PDF. Gere o .pptx também se der (skill pptx, se disponível, ou
     python-pptx) e com notas do apresentador contendo a fala de cada slide e a fonte de cada número.
     Se não houver como converter o .pptx em PDF no notebook, monte os slides em HTML 16:9 e gere o
     PDF com o Chrome headless (`--print-to-pdf --no-pdf-header-footer`);
   - depois de gerar, converta cada página em imagem e olhe uma por uma: texto cortado, sobreposição,
     contraste, fonte trocada. Conte as páginas do PDF gerado (não confie na prévia);
   - use capturas reais do app publicado, não telas desenhadas;
   - cronometre: leia as notas em voz alta no ritmo de fala (cerca de 140 palavras por minuto) e
     confira se cabe em 5 minutos com a demo.

Requisitos:
1. Siga o padrão oficial de skills do Claude Code: cada skill em .claude/skills/<nome>/SKILL.md,
   com frontmatter YAML contendo `name` (minúsculas e hífens, igual ao nome da pasta) e
   `description` (o que a skill faz e quando ativar, com os gatilhos concretos). Material de apoio
   longo vai em arquivos ao lado do SKILL.md, citados no corpo. Se a skill skill-creator estiver
   disponível, siga o padrão dela.
2. Instruções detalhadas, práticas e específicas deste desafio, não descrições superficiais.
   Cite os arquivos de dados reais pelo caminho, as colunas que importam, os termos do enunciado
   e as métricas do recorte.
3. Cada SKILL.md define com clareza: quando ativar (e quando não ativar), metodologia passo a
   passo, ferramentas e bibliotecas recomendadas (dentro da stack combinada), critérios de
   qualidade verificáveis e erros a evitar.
4. As skills se complementam. Defina o dono de cada responsabilidade (quem mantém o gabarito e o
   eval, quem escreve os prompts do produto, quem cuida dos números do pitch etc.) e como uma
   passa descobertas para a outra: achados dos dados vão para a seção "Achados dos dados" do
   SPEC.md, com o número e o comando que o gerou; erros da IA e mudanças de rota vão para o LOG.md.
   Sem duas skills cobrindo a mesma coisa.
5. Não invente informações sobre o negócio. Toda afirmação sobre a empresa sai do enunciado ou
   dos dados; o resto é suposição marcada como tal.
6. Não altere arquivos existentes do projeto sem necessidade. Não escreva código do produto agora.
7. As skills obedecem ao claude_contexto_hackathon.md. Em caso de conflito, o arquivo de contexto
   vence (stack, prazos, JSON validado, chaves só no servidor, sem números inventados, estilo dos
   textos).
8. Crie ou atualize o CLAUDE.md na raiz do projeto com: uma linha `@claude_contexto_hackathon.md`
   para importar o contexto; o desafio e o recorte em 3 linhas; a tabela das skills (nome, quando
   usar, responsabilidade, o que entrega); a arquitetura prevista do agente (etapas nomeadas,
   onde ficam prompts, fonte de dados, eval); e os princípios de desenvolvimento. Curto: o
   detalhe fica nas skills.

No fim:
- confira se todo SKILL.md tem frontmatter válido e se `name` bate com o nome da pasta;
- me mostre a árvore de .claude/skills/, a description de cada skill e por que escolheu essas e
  não outras (uma linha cada);
- me diga se preciso reiniciar a sessão para as skills aparecerem; se precisar, o CLAUDE.md
  garante que o contexto volta sozinho;
- faça um commit ("skills e CLAUDE.md do projeto").
```

---

Depois disso, siga para o SPEC (segunda mensagem da seção 1 do `prompts_do_dia.md`).

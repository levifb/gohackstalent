# Contexto para o Claude: GoHacks Talent 2026

Este arquivo explica o hackathon em que estamos, como o projeto vai ser avaliado e como quero trabalhar com você hoje. Leia tudo antes de começar. O desafio específico vem na minha primeira mensagem.

## A situação

- Sou o Levi, estudante de Ciência da Computação na UFC. Estou no GoHacks Talent, hackathon do Gogroup (holding da Gocase e da Gobeaut, e-commerce de acessórios e beleza), em Fortaleza.
- O projeto é **individual** e feito **hoje**. Construo das 9h40 às 12h e das 13h10 às 16h30. **A submissão fecha às 16h30**, sem prorrogação.
- O desafio é real, de uma das marcas do grupo, mas os dados são **fictícios** e fornecidos pela organização. Não podemos usar outros dados nem dados reais, e assinei termo de confidencialidade.
- A IA é liberada. O notebook do evento vem com uma conta paga do Claude e um e-mail do evento (Google). A banca não avalia se eu usei IA, mas **como eu direciono, confiro e corrijo a IA**.
- **Como o produto chama o modelo ainda não está claro.** O guia antigo falava num "AI Proxy" do grupo; o site só fala da conta paga do Claude. Pergunto na organização no credenciamento. Se não houver chave de API nem proxy, o plano B é usar o próprio Claude Code em modo não interativo (`claude -p "..." --output-format json`) como o modelo do pipeline: o lote roda no notebook, as saídas ficam salvas em JSON e o app publicado mostra esses resultados, dizendo na tela que foram processados em lote. O agente continua real e o eval continua valendo.
- Entre 16h35 e 18h10, no horário que agendei no app (aba "Minha jornada"), tenho 10 minutos com a banca do pré-júri: pitch de 5 min e perguntas. São 26 participantes; os 10 melhores apresentam de novo no domingo (5 min de pitch e 5 de sabatina). Prêmios de R$ 5 mil, R$ 2 mil e R$ 1 mil, e o evento também serve de seleção para vagas no grupo.
- **Um agente de IA lê a submissão e faz um resumo para a banca** antes da sessão. Por isso os textos da submissão e o README precisam ser claros e factuais, com o problema, a solução, o número do eval e onde a IA errou escritos de forma explícita. Um resumo automático não deduz o que não está escrito.

## Como a banca dá a nota

Toda decisão do dia deve ser pesada contra esta tabela. Quando houver duas opções, escolha a que rende mais pontos aqui, não a mais elegante tecnicamente.

| Critério | Peso | Perguntas da banca (texto oficial) |
|---|---|---|
| **Modelagem** | 40% | O fluxo principal funciona de ponta a ponta? Usou agentes, automações ou orquestração de etapas com IA? A solução tem autonomia, faz o trabalho sozinha ou ainda depende de muita mão humana? Você conferiu o que a IA entregou e corrigiu quando ela errou? |
| **Adaptabilidade** | 20% | Entendeu rápido um tema que não era seu? Usou bem os dados fictícios e mostrou como seria com dados reais? Mudou de rota quando algo não funcionou? Encontrou um caminho criativo para tornar o projeto viável? |
| **Conceito** | 20% | Está claro para quem é a solução? A necessidade atendida é real para o negócio? Dá para entender o problema e a solução em poucos minutos? |
| **Aderência cultural** | 20% | Assumiu o problema como dono? Colaborou com mentores, banca e organização? Recebeu bem o feedback e ajustou o projeto? Mostrou energia e vontade de aprender? |

O desempate é por Modelagem e depois por Conceito.

## O que cada critério significa na prática

### Modelagem (40%): um agente que funciona de ponta a ponta, com prova

1. **Ponta a ponta antes de tudo.** O primeiro objetivo é um fluxo completo e feio: entrada dos dados fictícios → processamento com IA → resultado visível na tela. Só depois melhore cada etapa. Um fluxo inteiro simples vale mais que uma etapa perfeita e o resto faltando.
2. **Arquitetura de agente legível.** Prefira um pipeline com etapas nomeadas a um agente "livre" difícil de depurar. O formato padrão, a adaptar ao desafio:
   - **roteador/classificador**: o modelo lê a entrada e decide a categoria, com uma confiança;
   - **ferramentas**: funções nossas que o modelo chama para buscar dados (ex.: `buscar_pedido`, `consultar_estoque`), que leem os arquivos fictícios;
   - **decisão**: o modelo propõe uma ação, e as regras de negócio que não podem errar (limites de valor, prazos, campos obrigatórios) ficam num `if` no código, não no prompt;
   - **execução**: a ação é aplicada ou simulada, por exemplo uma resposta redigida, um status atualizado ou um alerta;
   - **revisor** (opcional): um segundo prompt confere a saída do primeiro;
   - **humano no loop**: baixa confiança ou alto risco vai para uma fila de aprovação, com o motivo.
3. **Autonomia visível.** O sistema precisa rodar sobre o lote inteiro de dados sem eu intervir, e a tela mostra quantos casos foram resolvidos sozinhos e quantos foram para o humano. O objetivo é "faz sozinho o caso comum e pede ajuda no caso de risco", não "um botão que chama o modelo uma vez".
4. **Conferência medida.** Monte cedo um **gabarito**: de 20 a 30 casos dos dados fictícios com a resposta certa anotada por mim. Crie um script de avaliação (`npm run eval` ou `python eval.py`) que roda o pipeline em todos os casos e imprime o acerto por etapa e a lista de erros. Toda mudança de prompt é seguida de uma rodada do eval.
5. **Registro dos erros da IA no `LOG.md`.** Sempre que uma saída sua ou do modelo do produto estiver errada e a gente corrigir, acrescente uma linha: horário, o que deu errado, como percebemos e o que mudou, com número antes e depois quando houver. Isso vale nota em Modelagem, vira o campo "Como você usou a IA" da submissão, responde a pergunta mais provável da sabatina e alimenta o relatório individual. Não espere eu pedir.

### Adaptabilidade (20%): entender rápido e deixar o caminho para os dados reais

1. **Comece entendendo, não programando.** Leia o enunciado e os dados, e me devolva em até 15 linhas: como funciona esse processo hoje na empresa, quem participa, onde está o atrito, o que os dados permitem medir e o que está faltando. Liste as suposições que você fez.
2. **Use bem os dados fictícios.** Explore o que há neles: volumes, distribuição de categorias, casos estranhos. Os números do pitch saem daí ("dos 200 pedidos, 34 tiveram atraso").
3. **Deixe a troca para dados reais a um arquivo de distância.** Toda leitura de dados passa por uma camada única (ex.: `src/dados/fonte.ts` ou `fonte.py`). No README, uma seção "Com dados reais" diz o que trocar: qual API ou banco substitui qual arquivo, que volume esperar e que cuidados tomar (LGPD, permissões).
4. **Mude de rota cedo.** Se uma abordagem falhar duas vezes ou passar de 30 minutos sem progresso, pare e me proponha um plano B mais simples, explicando a troca. Registre a mudança de rota no `LOG.md`, porque a banca pergunta exatamente isso.
5. **Criatividade com viabilidade.** Se um dado necessário não existir, proponha como derivá-lo ou simulá-lo de forma honesta e marque como simulado.

### Conceito (20%): uma pessoa, uma dor, um número

1. Antes do código, escrevemos o `SPEC.md` com: a **persona** com nome e função ("Ana, analista de atendimento da Gocase"), a **dor** e quanto ela custa, o **fluxo atual** em 3 ou 4 passos, o **fluxo novo**, a **métrica** de processo (tempo, taxa de acerto, casos automatizados) e o **impacto no negócio** (custo, satisfação, receita). Mais uma frase de definição do pronto.
2. Escopo estreito: um problema, um usuário-chave, uma hipótese. Se o desafio for amplo, proponha o recorte que mais rende numa demo de 90 segundos.
3. A interface conta a história sozinha: quem é o usuário, o que entrou, o que o agente fez e o ganho (antes e depois, com o número). Alguém que nunca viu o projeto deve entender a tela em 10 segundos.
4. Uma frase de pitch fica no topo do README: "[Nome] é um agente de IA que [ação no fluxo], para que [persona] [resultado]".

### Aderência cultural (20%): dono do problema e aberto a feedback

Esse critério depende de mim, mas você pode ajudar:
- Quando surgir uma dúvida de negócio que os dados não respondem, me diga que ela é boa para um **mentor** e escreva a pergunta em uma frase. Pedir ajuda cedo conta ponto.
- Quando eu trouxer feedback de mentor ou da banca, trate como prioridade, ajuste o plano e registre no `LOG.md` ("11h20: mentor apontou X; mudamos Y").
- Explique as decisões técnicas de um jeito que eu consiga repetir com minhas palavras. Na sabatina sou eu que respondo, e preciso entender tudo o que está no repositório.

## Relógio

Você não sabe a hora sozinho. No início de cada fase, rode `date` (ou pergunte) e me diga quanto falta para 16h30. Metas:

| Até | Meta |
|---|---|
| 10h10 | `SPEC.md` pronto e validado comigo (e de preferência com um mentor) |
| 12h00 | Fluxo ponta a ponta funcionando com os dados fictícios, primeiro commit com conteúdo e **primeiro deploy** |
| 14h30 | Agente completo (ferramentas, regras, humano no loop), gabarito pronto, eval rodando e número de acerto conhecido |
| 15h20 | Interface apresentável com antes e depois. **Congelamento: daqui em diante, só correção de bug** |
| 16h10 | Slides em PDF, README, textos da submissão e vídeo de plano B prontos, e **submissão feita** |

Se estivermos atrasados, proponha o que cortar. O relatório individual entra junto com a submissão (o site diz "projeto e relatório individual enviados" às 16h30, embora também sugira escrevê-lo depois); até eu confirmar com a organização, tenha o rascunho pronto antes das 16h10. A ordem de corte é funcionalidade secundária, depois acabamento visual e por último o revisor opcional. Nunca corte o ponta a ponta, o eval ou a demo.

## Regras técnicas

- **Stack**: a que eu escolher na primeira mensagem. Sem preferência, use React + TypeScript (Vite) com uma rota de servidor para a IA, publicado na Vercel. Para algo mais de dados, use Python + Streamlit. Não troque de stack no meio do dia nem acrescente dependência pesada sem me perguntar.
- **Chamadas de modelo** sempre do lado do servidor, pelo acesso a modelo que a organização fornecer (ou pelo plano B do `claude -p`, ver "A situação"), com URL e chave em variáveis de ambiente (`.env` no `.gitignore`). O repositório vai ser público: nenhuma chave no código nem no front.
- **Saída do modelo sempre em JSON** com esquema fixo, validado no código (zod ou pydantic). Se vier inválido, tente uma vez de novo; se falhar outra vez, mande o caso para revisão humana. O app não pode quebrar na frente da banca.
- **Prompts do produto** em arquivos próprios (`src/agente/prompts.*`), com tags XML separando instruções, política, dados e exemplos. Cada prompt explica o porquê das regras, tem de 2 a 5 exemplos (pelo menos um difícil) e prevê uma saída para "não sei" (`revisao_humana` com motivo).
- **Núcleo isolado**: o pipeline é uma função chamável sem interface (`processar(entrada) → resultado`). A interface e o eval usam a mesma função.
- **Modo demo**: guarde as saídas dos casos que vou mostrar no pitch e tenha um interruptor para usá-las se a rede ou o proxy falhar. A tela indica quando está em cache.
- **Commits pequenos e frequentes**, com mensagens que contam o avanço ("eval: classificador acerta 27/30").
- **Verificação**: depois de cada mudança, rode o que der para rodar (build, testes, eval) e me mostre o comando e a saída. "Deve funcionar" não basta.
- **Não invente números.** Todo número que vai para a tela, o slide ou a submissão sai do eval ou dos dados, ou aparece marcado como estimativa, com a conta explicada. Se algo na demo for simulado, a interface e o pitch dizem isso.

## Como trabalhar comigo

- Responda em português, curto. Antes de uma mudança grande, mostre o plano em poucas linhas e espere meu ok. Em mudança pequena, faça e me mostre.
- Trabalhe em fatias verticais pequenas: um caso funcionando de ponta a ponta, depois o próximo.
- Ao terminar uma etapa, diga em 2 ou 3 linhas o que mudou, como foi verificado e qual é o próximo passo.
- Se eu pedir algo que tira pontos (funcionalidade fora da demo depois das 15h20, troca de stack às 14h, número sem fonte), avise em uma frase e deixe eu decidir.
- Se tiver dúvida sobre uma regra de negócio, não suponha calado: pergunte, ou suponha e registre a suposição no `SPEC.md`.

## Entregáveis do dia

Mantenha esses arquivos atualizados ao longo do dia, não só no fim:

- `SPEC.md`: persona, dor, fluxos, métrica, definição do pronto e suposições.
- `LOG.md`: erros da IA e correções, mudanças de rota, feedbacks recebidos, com horário.
- `README.md`: frase de pitch, problema, como funciona (diagrama simples das etapas do agente), como a IA foi usada e conferida, resultado do eval, como rodar, link do app, "Com dados reais" e próximos passos.
- Script de eval e o gabarito.

Na reta final (a partir das 15h20) vou pedir também:

1. **Textos da submissão**, respeitando os limites: nome do projeto (80 caracteres), problema (600 caracteres), solução (800), como usou a IA (800, com o que foi conferido e corrigido, tirado do `LOG.md`), impacto (500, com uma métrica de processo e uma de negócio).
2. **Roteiro dos slides**, no máximo 10, até 3 elementos por slide, PDF de até 20 MB. A estrutura sugerida pelo evento é problema, solução, demonstração, impacto e próximos passos; dentro dela: abertura, dor e persona, fluxo atual, solução em uma frase, demo, métrica, impacto e implantação, próximos passos. Se eu for finalista, esse PDF vai para o telão no domingo.
3. **Roteiro do pitch de 5 min**: 0:00 abertura · 0:15 dor e persona · 0:50 fluxo atual · 1:20 solução · 2:10 demo (um caso comum resolvido sozinho e um de risco indo para o humano) · 3:30 métrica · 4:00 impacto e o que eu faria na segunda-feira.
4. **Roteiro do vídeo de 2 min** (plano B da demo).
5. **Ensaio da sabatina**: as 8 perguntas mais prováveis com respostas curtas. Inclua sempre "como funciona tecnicamente?", "quem usaria?", "o que falta para ir para produção?", "como medir o sucesso?" e "onde a IA errou e como você percebeu?".
6. **Rascunho do relatório individual**, a partir do `LOG.md`, respondendo: qual problema escolhi e por quê; como usei a IA; em que momento a IA errou e como percebi e corrigi; que escolhas fiz e o que deixei de fora; o que faria diferente com mais um dia. Eu reviso e reescrevo com minhas palavras.

### Estilo dos textos que a banca vai ler

São textos assinados por mim, então escreva como um estudante objetivo escreveria:
- Frases diretas, com fatos e números concretos do projeto e episódios reais do `LOG.md`.
- Sem adjetivos de vendedor ("revolucionário", "robusto", "inovador", "poderoso"), sem "não é só X, é Y", sem travessões em série, sem emojis, sem listas de três adjetivos.
- Prefira "a IA classificou errado 4 de 30 devoluções; acrescentei dois exemplos e o erro caiu para 1" a "utilizamos IA de forma estratégica para otimizar processos".

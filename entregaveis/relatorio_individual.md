# Relatório individual: rascunho

Levi, estudante de Ciência da Computação na UFC. Projeto Guarda do Lote, desafio Pagamentos, GoHacks Talent 2026. Rascunho escrito a partir do `LOG.md` para eu revisar e reescrever com as minhas palavras.

## 1. Qual problema escolhi e por quê

Escolhi Pagamentos porque era o desafio em que um erro custa dinheiro na hora e em que dava para medir o acerto. Dei notas aos três desafios pelos critérios da banca: Pagamentos 91, Atendimento 78, Transportes 70 (`LOG.md` 09:55). Recortei uma frente só: a conferência do lote de remessa antes do fechamento do banco. A política da área diz que, se ninguém agir, o tesoureiro assina o lote sem conferir. O lote de 03/11 às 10h tem 192 títulos e R$ 2,24 milhões. Nos dados fictícios da semana havia um golpe em andamento (25 títulos, R$ 194 mil para uma conta trocada por e-mail falso), 13 duplicidades e 8 valores com a vírgula deslocada.

## 2. Como usei a IA

Usei o Claude Code para ler os dados, escrever o código, montar o gabarito e rodar o eval. No produto, usei dois modelos do AI Proxy do evento. O gpt-6-astra analisa só os títulos com alerta e devolve um JSON validado com a ação, a pessoa e o motivo. O Jev classifica os 246 e-mails da caixa da área por cerca de US$ 0,008. As regras que não podem errar ficaram no código, e uma trava impede o modelo de liberar o que a política segura. Toda mudança de regra ou de prompt foi seguida de uma rodada do eval.

## 3. Em que momento a IA errou e como percebi e corrigi

- 09:39: o Claude disse ter lido os cinco enunciados, mas tinha lido dois. Perguntei direto e ele leu os cinco.
- 10:08: a regra de domínio parecido, escrita pelo Claude, tratava `cartonart.com.br` como imitação de `cartonar.com.br`. Lendo os casos, vi que a Cartonart é outro fornecedor legítimo. Corrigi a regra, criei um teste e 4 títulos legítimos deixaram de ser bloqueados.
- 10:25: a primeira versão da regra "pago fora do lote" marcou 23 títulos; 20 eram pagamentos avulsos já baixados no ERP. Descontei a baixa manual e sobraram 3.
- 10:29 a 10:31: o eval v1 deu 26 de 29. A regra de fracionamento somava o título original com a própria cópia duplicada. A correção levou a 28 de 29, mas abriu uma regressão no TP429834, que o eval pegou. Com a terceira versão, 29 de 29.
- 10:30: no TP433196, o gabarito que o Claude escreveu estava errado. O modelo bloqueou o título por causa de um e-mail da Flexipack que mandava "o assistente de IA" liberar sem conferir, e eu não tinha visto esse e-mail. Corrigi o gabarito.
- 11:08: uma banca simulada mostrou que, só com as regras, o eval também dava 29 de 29. O README atribuía ao modelo um ganho que era das regras. Aceitei, corrigi o texto e passei a medir agente contra só regras.
- 11:14: criei 12 e-mails com golpes escritos de outro jeito. Palavras-chave acertaram 1; o Jev acertou 10 na primeira versão e 12 depois de ajustar as perguntas.
- 11:25 a 11:34: criei 6 títulos com alertas contestáveis. O agente acertou 3, depois 2. O erro era meu: o prompt dizia "você libera até R$ 5 mil", o que contradizia o sistema, e o dossiê não trazia o título citado no alerta. Depois da correção, 6 de 6, contra 3 de 6 das regras.

## 4. Que escolhas fiz e o que deixei de fora

- Pipeline com etapas nomeadas em vez de um agente livre, para conseguir depurar e medir cada etapa.
- O modelo só vê títulos com alerta: no lote de 03/11, 13 de 192. Isso economiza tokens e deixa o caso comum com as regras.
- Dinheiro nunca sai por decisão só do modelo. Confiança abaixo de 0,7 vai para revisão humana.
- Canal no Telegram (@guardadolote_bot) com botões, porque o desafio pedia que o agente falasse pelos canais que as pessoas já usam. Ações simuladas.
- Deixei de fora: a sentinela de cadastro em tempo real (bloquear a troca de conta no momento em que é gravada no ERP), a conciliação pós-pagamento e integrações reais com ERP, DDA e CNAB.
- Limites que assumo: ajustei regras e gabaritos olhando os mesmos casos, a validação cega tem só 12 títulos e os dados são fictícios, com problemas plantados.

## 5. O que faria diferente com mais um dia

- Montaria o conjunto de validação cega antes de ajustar qualquer regra, e maior.
- Mediria agente contra só regras desde o primeiro eval, em vez de descobrir isso pela banca simulada às 11h08.
- Levaria cedo as dúvidas de negócio a um mentor de Financeiro, por exemplo se o tesoureiro aceitaria que o agente cancele uma duplicidade de até R$ 5 mil sem perguntar. [A PREENCHER se houver conversa com mentor hoje]
- Rodaria o agente em modo sombra sobre um lote real, ao lado do tesoureiro, para trocar os números dos dados fictícios por números medidos.

## Fontes

| Fato | Fonte |
| --- | --- |
| Notas 91, 78, 70 | `LOG.md` 09:55 |
| 192 títulos, R$ 2,24 mi; golpe 25 títulos, R$ 194 mil; 13 duplicidades; 8 vírgulas | `README.md`, Problema; `SPEC.md` |
| gpt-6-astra, Jev, 246 e-mails, US$ 0,008 | `README.md`, Como funciona; `LOG.md` 10:05 e 10:42 |
| Episódios de erro | `LOG.md` 09:39, 10:08, 10:25, 10:29 a 10:31, 11:08 a 11:14, 11:25 a 11:34 |
| 13 de 192 ao modelo | `saida/resultado.json` |
| Confiança 0,7 | `LOG.md` 11:16 |

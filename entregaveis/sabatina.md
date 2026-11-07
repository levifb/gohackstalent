# Ensaio da sabatina: 8 perguntas prováveis

Primeira versão. Respostas curtas (2 a 3 frases), na primeira pessoa, para eu dizer com as minhas palavras. As perguntas 2, 7 e 8 vêm da banca simulada (`avaliacoes/avaliacao_1108.md`).

## 1. Como funciona tecnicamente?

É um pipeline em Python com etapas nomeadas: carregar o lote, triagem por regras da política, dossiê montado por ferramentas que leem os sistemas, análise do modelo (gpt-6-astra pelo AI Proxy) com saída em JSON validada por pydantic, trava no código, execução simulada e fila humana. O modelo só vê os títulos com alerta: no lote de 03/11, 13 de 192. A fila vai para a tela e para o Telegram (@guardadolote_bot), e um segundo agente, a sentinela, classifica os 246 e-mails da caixa com o Jev.

## 2. Se as regras sozinhas fazem 28 de 29, para que serve o modelo?

Nos dados da organização quase todo alerta é duro (golpe, duplicidade, alçada), então as regras decidem o dinheiro e eu escolhi que fosse assim: dinheiro nunca sai por decisão só do modelo. O modelo muda 1 caso no gabarito, acionando o jurídico na injeção da Flexipack (TP433196), escolhe a pessoa e escreve o motivo. Onde há julgamento, testei com 6 títulos que criei com alertas contestáveis: o agente acertou 6 e as regras 3, porque as regras seguram também os legítimos. E na caixa de e-mail, com golpes reescritos, o Jev acertou 12 de 12 e as palavras-chave 1.

## 3. Onde a IA errou e como você percebeu?

Percebi pelo eval e lendo os casos. A regra de domínio parecido que o Claude escreveu bloqueava 4 títulos legítimos da Cartonart; a regra de "pago fora do lote" marcou 23 títulos e 20 estavam errados; o eval v1 deu 26 de 29, e a correção do fracionamento abriu uma regressão que o próprio eval pegou. Num caso o erro era do gabarito que o Claude escreveu: o modelo bloqueou o TP433196 por causa de um e-mail que mandava "o assistente de IA" liberar sem conferir, e o modelo estava certo. Também errei eu: o prompt dizia "você libera até R$ 5 mil" e o julgamento caiu para 2 de 6 até eu corrigir (`LOG.md` 11:31).

## 4. Quem usaria?

O Marcos Teles, tesoureiro, que hoje assina o lote no fechamento sem abrir os títulos. Quem recebe a fila são as pessoas que a política já manda acionar: Renata (coordenadora de contas a pagar), Helena (diretora, acima de R$ 50 mil), Lívia (jurídico, golpe) e compras. Elas decidem pelo Telegram, sem abrir outro sistema (na prova de conceito, o bot fala com um chat de teste e as ações são simuladas).

## 5. O que falta para ir para produção?

Trocar os CSVs pela fonte real em `agente/fonte.py`: ERP, portal de NF-e, DDA e a caixa de e-mail, com o papel de menor permissão e cuidado com LGPD e sigilo bancário. Depois, duas semanas em modo sombra, às 9h e às 13h, só publicando no canal o que o agente faria, enquanto o Marcos continua assinando. Só então autonomia por degraus: primeiro retirar e acionar a pessoa, depois corrigir até R$ 5 mil, a alçada do analista.

## 6. Como medir o sucesso?

Processo: porcentagem do lote resolvida sem humano (hoje 93% da semana nos dados fictícios) e acerto no gabarito por etapa. Negócio: o placar da área, que soma dinheiro que saiu indevido, atraso de pagamento legítimo e R$ 60 por acionamento desnecessário; no gabarito, assinar sem conferir custa R$ 517 mil e o agente R$ 0. No modo sombra eu mediria os erros reais retidos, os legítimos segurados sem motivo e o tempo da equipe por lote.

## 7. O gabarito foi escrito por você e pelo Claude nos mesmos casos em que ajustou as regras. O 29 de 29 não é sobreajuste?

Provavelmente é otimista, e o README diz isso. Por isso anotei 12 títulos sorteados antes de ver a decisão (12 de 12), mas a amostra é pequena e fácil; os 6 de julgamento e os 12 e-mails reescritos também foram escritos por mim. O número que vale de verdade é o do modo sombra com dados reais.

## 8. Esses problemas foram plantados pela organização. O que acontece com um golpe que as suas regras não conhecem?

Um título sem nenhum alerta é liberado sem passar pelo modelo, então um golpe sem sinal nos dados passaria. A defesa é a regra de troca de conta sem confirmação, que pega o caminho mais comum do golpe seja qual for o texto, e a sentinela, que lê a caixa inteira; nos e-mails reescritos com outras palavras ela acertou 12 de 12. Se o modelo responder com confiança abaixo de 0,7, o dinheiro não sai e o caso vai para revisão humana.

## Reserva (se sobrar tempo)

- **"Os dados e o cache do modelo estão no repositório público?"** Os CSVs originais ficam fora do git; os resultados processados e o cache, derivados dos dados fictícios, estão no repositório por decisão minha, e isso está registrado como pergunta pendente para a organização no `SPEC.md`. [CONFIRMAR com a organização antes da sessão]
- **"Falou com algum mentor?"** [A PREENCHER: o `LOG.md` ainda não tem feedback de mentor. A banca simulada sugeriu levar a um mentor de Financeiro: "o tesoureiro aceitaria que o agente cancele uma duplicidade de até R$ 5 mil sem perguntar?" e "quem pode apertar 'liberar mesmo assim' num título com troca bancária sem confirmação?"]

## Fontes

| Número | Fonte |
| --- | --- |
| 13 de 192 ao modelo; 246 e-mails | `saida/resultado.json`; `README.md`, Resultado atual |
| 29/29, 28/29; 6/6, 3/6; 12/12, 1/12; 12/12 validação cega | `web/public/eval.json`; `README.md`, Eval |
| Cartonart (4 títulos); pago fora do lote 23/20; v1 26/29; regressão TP429834; TP433196; prompt R$ 5 mil e 2/6 | `LOG.md` 10:08, 10:25, 10:29 a 10:31, 11:31 |
| 93%; R$ 517 mil × R$ 0; R$ 60 por acionamento | `README.md`, Resultado atual e Eval; `SPEC.md`, Dor e custo |
| Confiança abaixo de 0,7 | `LOG.md` 11:16; `README.md`, O que a IA faz de fato |
| Pessoas acionadas | `SPEC.md`, Persona |
| Modo sombra e degraus | `README.md`, Implantação |

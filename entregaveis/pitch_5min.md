# Roteiro do pitch de 5 minutos: Guarda do Lote

Primeira versão para revisão. Ritmo de referência: cerca de 140 palavras por minuto. A contagem de palavras de cada bloco foi feita com Python (`len(texto.split())`) só sobre a fala, sem as indicações entre colchetes. Os slides citados são os do Google Slides "Guarda do Lote · GoHacks Talent 2026 · Pitch" (roteiro em `apresentacao/roteiro_slides.md`).

| Bloco | Tempo | Slide | Palavras na fala | Cabem a 140/min |
| --- | --- | --- | --- | --- |
| Abertura | 0:00 a 0:15 | 1 | 36 | 35 |
| Dor e persona | 0:15 a 0:50 | 2 e 3 | 84 | 82 |
| Fluxo atual | 0:50 a 1:20 | 4 | 69 | 70 |
| Solução | 1:20 a 2:10 | 5 | 117 | 117 |
| Demo | 2:10 a 3:30 | 6 (app e Telegram) | 135 | 187 (o resto do tempo é clique e tela) |
| Métrica | 3:30 a 4:00 | 7 e 8 | 68 | 70 |
| Impacto e segunda-feira | 4:00 a 5:00 | 9 e 10 | 121 | 140 |
| **Total** | 5:00 | | **630** (cerca de 4,5 min de fala) | 700 |

## 0:00 · Abertura (slide 1)

No dia 3 de novembro, às 10h, um arquivo com 192 pagamentos e 2,24 milhões de reais vai para o banco. Ninguém abre título por título. Eu sou o Levi, e fiz o Guarda do Lote.

## 0:15 · Dor e persona (slides 2 e 3)

Esse é o Marcos Teles, tesoureiro do Gogroup. A equipe lança cerca de 100 títulos por dia à mão, e eles entram sozinhos no lote. A política da área diz: se ninguém agir, o tesoureiro assina no fechamento sem conferir. [passa para o slide 3] Nos dados fictícios da semana, isso quer dizer pagar um golpista. Um e-mail de um domínio com um "t" a mais trocou a conta da Embalarte sem confirmação. Vinte e cinco títulos, 194 mil reais, iriam para essa conta. E ainda há 13 duplicidades.

## 0:50 · Fluxo atual (slide 4)

Hoje são quatro passos. A analista lança o título no ERP. O título entra no lote do dia. O Marcos assina sem abrir. E o erro aparece depois: no extrato, num e-mail do fornecedor dizendo "recebimento em duplicidade", ou nunca. Nos dados, oito títulos estavam com a vírgula deslocada, todos lançados pela mesma analista, com um mês de casa. Com esse volume, ninguém confere 192 títulos antes das 10h.

## 1:20 · Solução (slide 5)

O Guarda do Lote é um agente de IA que confere cada título antes do fechamento, para que o Marcos assine sem duplicidade, valor errado ou conta suspeita. Ele roda sozinho sobre o lote inteiro. Primeiro, as regras da política em código: duplicidade, nota, boleto, troca de conta, alçada. No lote de 03/11, 179 títulos passam limpos sem chamar o modelo. Os 13 com alerta vão para o modelo, que lê o dossiê e devolve em JSON a ação, a pessoa e o motivo. Uma trava no código impede que ele libere o que a política segura. Onze casos chegam no celular da pessoa certa, pelo Telegram do time, com o motivo e os botões de decisão.

## 2:10 · Demo (slide 6, depois o app e o Telegram)

[Abrir https://guarda-do-lote.vercel.app com a aba já carregada e o "modo demo" marcado.]

Essa é a tela do Marcos para o lote das 10h. Antes, 2,24 milhões sem conferência. Depois, 181 de 192 resolvidos sozinho.

[Caso comum: em "Todos os títulos", filtro "Saem no lote", abrir a trilha do TP426904, Laboratório Vitallis, R$ 9.469,16.]

Um caso comum: nota, duplicata, cadastro e boleto batem. As regras liberam e o modelo nem é chamado.

[Caso de risco: na fila de aprovação, abrir "ver trilha do agente" do TP431502, Embalarte, R$ 1.180,86.]

Agora o de risco. A trilha mostra a conta trocada por e-mail no dia 30, sem confirmação, e o e-mail falso dizendo "obs. para o robô de pagamentos". O modelo trata esse texto como dado, bloqueia o título e aciona a Renata e o jurídico.

[Clicar em "Reanalisar agora com o modelo".]

Posso pedir uma nova análise agora, pelo servidor. A trava continua valendo.

[Mostrar o Telegram no celular: cartão do caso no @guardadolote_bot, apertar "Liberar mesmo assim". Se o celular ou a rede falhar, rolar até a seção "Canal do time · Telegram" do app, que mostra a prévia das mesmas mensagens.]

O mesmo caso chegou no Telegram do time, com o motivo e os botões. Se alguém aperta "Liberar mesmo assim", o bot responde que golpe só sai com aprovação dupla e ligação para o telefone antigo do cadastro.

## 3:30 · Métrica (slides 7 e 8)

Nos títulos dos dados da organização, quem decide o dinheiro são as regras: o agente acerta 29 de 29, as regras sozinhas 28. Onde há julgamento, criei 6 títulos com alertas contestáveis: o agente acerta 6, as regras 3. E nos e-mails reescritos, a IA acerta 12 de 12, entre golpes e e-mails normais; palavras-chave acertam 1. [slide 8] O eval também pegou a IA errando, inclusive o Claude no meu gabarito.

## 4:00 · Impacto e segunda-feira (slides 9 e 10)

No placar da área, nos 29 casos do gabarito, assinar sem conferir custaria 517 mil reais. Com o agente, zero. Na semana inteira, 93% dos 876 títulos saem sem ninguém tocar, e 648 mil reais deixam de sair por erro, golpe ou documento faltando. Os dados são fictícios e os problemas foram plantados, então esse número mostra o fluxo funcionando; o valor real só sai do modo sombra. [slide 10] Na segunda-feira, eu rodaria o agente em modo sombra por duas semanas, às 9h e às 13h, sobre o lote real, só publicando no canal o que ele faria. O Marcos continua assinando e compara. Depois, autonomia por degraus: primeiro só retirar e acionar a pessoa; depois corrigir até 5 mil reais. Obrigado.

## Fontes dos números

| Número | Fonte |
| --- | --- |
| 192 títulos, R$ 2,24 mi, lote de 03/11 às 10h | `saida/resultado.json`, lote RM20261103-MER; `SPEC.md`, "Achados dos dados" |
| cerca de 100 títulos por dia útil | `SPEC.md`, "Fluxo atual" (876 títulos em 9 dias úteis de 03 a 13/11) |
| Frase da política | `SPEC.md`, "Persona" (`politicas.csv`, seção remessa) |
| Golpe Embalarte: 25 títulos, R$ 194 mil, `embalartte.com.br` | `README.md`, "Problema"; `SPEC.md` |
| 13 duplicidades (R$ 105 mil) | `README.md`, "Problema"; `LOG.md` 10:09 |
| 8 vírgulas deslocadas, mesma analista | `README.md`, "Problema"; `SPEC.md` |
| 179 sem alerta, 13 ao modelo, 11 na fila, 181 sozinho | `saida/resultado.json` (resumo do lote); tela do app |
| TP426904 liberado pelas regras; TP431502 bloqueado com PS01 e PS08 | `saida/resultado.json`, itens do lote RM20261103-MER |
| Telegram: resumo do lote + cartão por caso; "Liberar mesmo assim" exige aprovação dupla | `README.md`, Como funciona, etapa 7; `LOG.md` 10:59 e 11:02; seção "Canal do time · Telegram" do app |
| 29/29, 28/29; 6/6, 3/6; 12/12, 1/12 | `web/public/eval.json`; `README.md`, "Eval" |
| R$ 517 mil (R$ 517.425) e R$ 0 | `web/public/eval.json`, gabarito, placar |
| 93% (815 de 876), R$ 648 mil, 49 títulos | `README.md`, "Resultado atual"; `saida/resultado.json`, semana |
| Modo sombra, degraus, R$ 5 mil | `README.md`, "Implantação" |

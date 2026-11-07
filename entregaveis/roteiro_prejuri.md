# Roteiro do pré-júri: pitch de 5 min (Guarda do Lote)

Fala completa, slide a slide, na ordem atual do deck (10 slides). Cerca de 560 palavras faladas (contadas): com os cliques e os 10 s do modelo ao vivo, dá uns 4 min e meio, com folga para os 5. Entre colchetes, o que fazer. Os números saem de `saida/resultado.json` e `web/public/eval.json` (fontes nas notas de cada slide).

Antes de começar: site aberto em `https://guarda-do-lote.vercel.app/#simulacao` (zoom 110%), deck em tela cheia, Telegram no celular parado no cartão "BLOQUEADO · R$ 1.935,75 · Embalarte · TP432024". Plano B no fim deste arquivo; respostas curtas para a sabatina em `preparacao_banca.md`.

---

## 0:00 · Slide 1: abertura (15 s)

Às 10h de 3 de novembro, um arquivo com 192 pagamentos e 2,24 milhões de reais vai para o banco, e ninguém abre um por um. Para o tesoureiro do Gogroup, que assina esse lote sem conferir, eu construí o Guarda do Lote: um agente que confere cada título, libera o certo e chama a pessoa certa quando há risco. Com ele, o Marcos olha 11 de 192.

## 0:15 · Slide 2: a dor (20 s)

Esse é o Marcos Teles, tesoureiro. A própria política diz: se ninguém agir, ele assina o lote sem conferir. São uns 100 títulos por dia, lançados à mão, cada um em sete sistemas.

## 0:35 · Slide 3: o custo (20 s)

E o que estava escondido na semana? Um golpe: um e-mail de um domínio com um "t" a mais trocou a conta da Embalarte. 194 mil reais iriam para o golpista. Mais 16 pagamentos em dobro, 8 vírgulas no lugar errado e 2 títulos no fornecedor errado.

## 0:55 · Slide 4: o que já funciona (15 s)

O agente faz três coisas: confere cada título antes de o arquivo ir ao banco, lê a caixa de e-mail marcando golpes, e leva cada caso à pessoa certa no Telegram.

## 1:10 · Slide 5: o agente (25 s)

Ele roda sozinho no lote inteiro. As regras da política, em código, olham cada título. Só os 13 com alerta vão para o modelo, que lê o dossiê e propõe ação, pessoa e motivo. Uma trava no código impede que ele libere o que a política segura. Resultado: 181 de 192 resolvidos sozinho.

## 1:35 · Slide 6: o que o agente pegou (15 s)

Casos que passariam pela assinatura: nomes quase iguais com o dinheiro indo para a empresa errada, um título 10 vezes maior que a nota, um boleto já pago, e um e-mail mandando a IA liberar sem conferir.

## 1:50 · Slide 7: Telegram (15 s)

E tudo chega no celular de quem decide, com motivo, pessoa e botões.

## 2:05 · Slide 8 + demo ao vivo (1 min 25 s)

Vamos ver funcionando.

[Troca para o site, no lote. Clica em "↻ Rodar de novo".]

Esse é o lote das 10h. Os laranjas piscando são os 13 com alerta, indo para o modelo. Verde sai sozinho, rosa foi barrado, azul espera a diretora.

[Clica no primeiro quadradinho, canto superior esquerdo: Laboratório Vitallis.]

Caso comum: nota, duplicata, cadastro e boleto batem em todos os sistemas. Saiu sozinho, sem gastar modelo.

[Fecha. Clica no rosa da linha 4, coluna 22: Embalarte, TP431502.]

Agora o golpe: cadastro bancário e e-mail em vermelho. A conta foi trocada por e-mail, sem confirmação, de um domínio que imita o do fornecedor.

[Rola até "3. Análise do modelo" e clica em "Reanalisar agora com o modelo".]

Vou pedir ao modelo para analisar ao vivo. Se ele propuser liberar, a trava no código não deixa o dinheiro sair.

[Resposta aparece, em uns 10 s.]

Bloquear, confiança de 99%, e ele marcou que o texto tentou dar ordem ao robô. Aciona a Renata e o jurídico.

[Pega o celular.]

E no Telegram de quem decide, vou tentar liberar mesmo assim.

[Aperta "Liberar mesmo assim" e mostra a tela para a banca.]

Não deixa: título com suspeita de golpe só sai com aprovação dupla e ligação para o telefone antigo do cadastro. A política vale até contra mim.

[Volta para o deck.]

## 3:30 · Slide 9: como medi (30 s)

Medi contra um gabarito de 30 casos que eu revisei: o agente acerta 30; as regras sozinhas, 29. Onde o alerta pode ser falso, 6 de 6 contra 3. Golpes reescritos com outras palavras: 12 de 12 contra 1 da busca por palavra-chave. Quando a IA errou, o eval mostrou: um prompt meu derrubou o julgamento para 2 de 6, e eu corrigi. Tudo está no LOG.md.

## 4:00 · Slide 10: impacto e segunda-feira (50 s)

Nos 30 casos do gabarito, assinar sem conferir custaria 530 mil reais. Com o agente, zero. Na semana, 93% dos títulos saem sem ninguém tocar.

Os dados são fictícios; o valor real sai do modo sombra.

Na segunda-feira: duas semanas em modo sombra no lote real, publicando no canal o que faria, enquanto o Marcos continua assinando. Depois, autonomia por degraus.

Obrigado.

---

## Se o tempo apertar

- Corte primeiro o slide 6 (casos): a demo mostra a Embalarte de qualquer jeito.
- Depois, o caso comum da demo (Vitallis).
- Nunca corte o golpe com o modelo ao vivo nem o "Liberar mesmo assim" no celular.

## Se algo falhar na demo

| Problema | O que fazer |
| --- | --- |
| Reanálise demora mais de 15 s ou dá erro | Marca "modo demo (usar cache)" ao lado do botão e clica de novo: "sem rede, ele usa a resposta salva, e a tela avisa". |
| Site não abre | Fica nos slides 6 e 7 e, se der tempo, toca o vídeo de 2 min. |
| Telegram não responde | Mostra o print do slide 7: "essa é a resposta que o bot deu hoje de manhã". |

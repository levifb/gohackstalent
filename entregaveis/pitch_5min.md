# Pitch de 5 minutos (v2, roteiro do workshop de pitch)

Estrutura do workshop: 0:00 abertura (elevator pitch) · 0:15 dor · 0:50 o que já funciona · 1:20 o agente · 2:10 demo · 3:30 como fez · 4:00 impacto. Regra de ouro: se precisar cortar, corte texto, não a demo. A fala completa de cada slide está nas notas do apresentador do [deck](https://docs.google.com/presentation/d/1mVAGrmmNUs4j35EpH_0qqqpnHoZxF41FEcJKkLCvm7A/edit).

## Elevator pitch (abertura, submissão e "o que você fez?")

> Para o tesoureiro do Gogroup, que assina às 10h um lote de R$ 2,24 milhões sem abrir os títulos, construí o Guarda do Lote: um agente que confere cada título, libera o certo e chama a pessoa certa no risco. Com ele, o Marcos olha 11 de 192.

## SOAR (esqueleto)

- **Situação:** o lote de remessa sai às 10h e às 14h sem conferência; a política diz que o tesoureiro assina sem conferir.
- **Obstáculos:** a informação está em sete sistemas com formatos diferentes; os golpes vêm escritos de jeitos diferentes; bloquear tudo atrasa pagamento legítimo e também custa.
- **Ações:** regras da política em código nos 192 títulos, modelo só nos 13 com alerta, trava no código, sentinela na caixa de e-mail, fila no Telegram e eval comparando agente × regras.
- **Resultados:** 181 de 192 resolvidos sozinho; R$ 194 mil do golpe barrados; placar da área R$ 0 contra R$ 530 mil de assinar sem conferir (30 casos, dados fictícios).

## Blocos

| Tempo | Slide | O que dizer (resumo; fala completa nas notas) |
| --- | --- | --- |
| 0:00 | 1 | Elevator pitch acima |
| 0:15 | 2 e 3 | Marcos assina sem conferir; na semana, golpe de R$ 194 mil, 16 pagamentos em dobro, 8 vírgulas, 2 fornecedores trocados |
| 0:50 | 4 | O que o agente já faz hoje: confere o lote, lê a caixa de e-mail e leva cada caso à pessoa certa no Telegram |
| 1:20 | 5 | Regras nos 192, modelo nos 13 com alerta, trava; 181 sozinho, 11 para uma pessoa |
| 2:10 | 6 a 8 | Demo: Antes 192, depois 11. Rodar o agente no site, um caso verde (sozinho) e a Embalarte (escala); Telegram "Liberar mesmo assim" |
| 3:30 | 9 | 30/30 × 29/30; 6/6 × 3/6; 12/12 × 1/12; onde a IA errou e o eval pegou |
| 4:00 | 10 | R$ 530 mil × R$ 0 com a premissa; segunda-feira: modo sombra e autonomia por degraus |

## Demo (cliques)

1. Site aberto na aba "A história", já no ponto da simulação (não abrir no login nem no topo).
2. "Rodar o agente": os 192 quadradinhos ficam verdes, rosa e azuis.
3. Clicar num verde (liberado sozinho) e depois no rosa da Embalarte (TP431502): trilha com conta trocada e e-mail falso.
4. "Reanalisar agora com o modelo" (modo demo ligado se a rede estiver ruim).
5. Telegram no celular: "Liberar mesmo assim" e a resposta da política.

Plano B: slides 7 e 8 e o vídeo de 2 minutos.

## Evitar (dica do workshop)

Detalhe de implementação, nome de biblioteca, "como a IA foi treinada", buzzword sem contexto. Falar do que a IA faz no fluxo, qual passo acelera e o ganho frente ao manual.

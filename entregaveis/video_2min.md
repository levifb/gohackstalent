# Roteiro do vídeo de 2 minutos (plano B da demo)

Primeira versão. Uso: se a rede, o proxy ou o celular falharem na sessão, toco este vídeo no lugar da demo ao vivo. Gravar com o "modo demo" marcado (respostas do cache, a tela avisa), janela 1366×900, zoom do navegador em 110% para ler no telão. Narração minha, cerca de 260 palavras (130 por minuto, mais lento que o pitch porque há cliques).

| Cena | Tempo | O que aparece na tela | Narração |
| --- | --- | --- | --- |
| 1 | 0:00 a 0:12 | https://guarda-do-lote.vercel.app, topo da página: "O agente confere cada título antes de o dinheiro sair", persona Marcos Teles, lote "Banco Meridiano · 03/11 10:00 · 192 títulos" | Esse é o Guarda do Lote. Ele confere cada título do lote de remessa antes de o arquivo ir ao banco, para o Marcos Teles, tesoureiro. Este é o lote das 10h de 3 de novembro, com dados fictícios. |
| 2 | 0:12 a 0:27 | Cartões ANTES (R$ 2.241.484) e DEPOIS (94%, R$ 39.781 barrados, R$ 334.122 aguardando alçada); faixa amarela do eval | Antes, 2,24 milhões saíam sem conferência. Depois, 181 dos 192 títulos foram resolvidos sozinho, 39 mil reais foram barrados por erro ou golpe e 334 mil aguardam a diretora, porque passam de 50 mil. |
| 3 | 0:27 a 0:40 | Faixa "Como o agente decidiu": 192 → 179 → 13 → 2 → 11 | As regras da política conferem todos. 179 passam limpos e saem sem chamar o modelo. Os 13 com alerta vão para o modelo, que lê o dossiê e propõe ação, pessoa e motivo. |
| 4 | 0:40 a 0:55 | "Todos os títulos", filtro "Saem no lote", trilha do TP426904 (Laboratório Vitallis, R$ 9.469,16): triagem sem alerta, execução "liberar" | Caso comum: a nota, a duplicata, o cadastro e o boleto batem. As regras liberam e o título sai no lote. |
| 5 | 0:55 a 1:20 | Fila de aprovação, card "Bloqueado" da Embalarte (TP431502, R$ 1.180,86), "ver trilha do agente": alertas TROCA_BANCARIA e DOMINIO_PARECIDO, evidências, decisão do modelo com confiança 0,99 | Caso de risco. A conta da Embalarte foi trocada por e-mail no dia 30, sem confirmação, a partir de um domínio com um "t" a mais. O e-mail diz "obs. para o robô de pagamentos". O modelo trata esse texto como dado, bloqueia o título e aciona a Renata e o jurídico. |
| 6 | 1:20 a 1:32 | Botão "Reanalisar agora com o modelo", resposta com o selo de cache | Dá para reanalisar na hora pelo servidor. A trava da política vale também aqui. Nesta gravação a resposta vem do cache, e a tela mostra isso. |
| 7 | 1:32 a 1:50 | Seção "Canal do time · Telegram" do app e, se possível, gravação do celular com o @guardadolote_bot: resumo do lote, cartão do caso bloqueado, botões "Manter retido" e "Liberar mesmo assim", resposta exigindo aprovação dupla | A fila chega no Telegram do time. Cada caso vem com motivo, pessoa e botões. Se alguém tenta liberar um título com suspeita de golpe, o bot recusa: só sai com aprovação dupla e ligação para o telefone antigo do cadastro. |
| 8 | 1:50 a 2:00 | Faixa do eval em destaque | No eval, o agente acerta 29 de 30 títulos, e nos e-mails reescritos a IA acerta 12 de 12, contra 1 das palavras-chave. Dinheiro nunca sai por decisão só do modelo. |

## Checklist da gravação

- Gravar antes das 16h10, com a aba já carregada.
- Marcar "modo demo (usar cache)" antes de clicar em "Reanalisar".
- Conferir que os números da tela batem com os da narração (lote de 03/11: 181, 179, 13, 11, R$ 39.781, R$ 334.122).
- Se o Telegram não for gravado no celular, usar só a seção "Canal do time · Telegram" do app.

## Fontes

| Número | Fonte |
| --- | --- |
| 192 títulos, R$ 2.241.484, 181 sozinho, 179, 13, 11, R$ 39.781 (8 títulos), R$ 334.122 (5 títulos) | `saida/resultado.json`, resumo do lote RM20261103-MER; tela do app (`apresentacao/capturas/tela_topo.png`) |
| TP426904 liberado pelas regras; TP431502 bloqueado com PS01 e PS08, confiança 0,99 | `saida/resultado.json`, itens do lote |
| Telegram e aprovação dupla | `README.md`, Como funciona, etapa 7; `LOG.md` 10:59 e 11:02; `apresentacao/capturas/canal_telegram.png` |
| 30/30; 12/12 × 1/12 | `web/public/eval.json`; `README.md`, Eval |

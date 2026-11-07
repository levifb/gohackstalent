# Vídeo de 2 minutos (opcional da submissão; plano B da demo)

Gravado sem material do Levi: o Edge, controlado pelo Playwright, navega o site publicado (https://guarda-do-lote.vercel.app, aba A história) com cliques reais, e a narração é gerada por voz sintética, com legendas.

- Arquivo: `apresentacao/video/guarda_do_lote_2min.mp4` (fora do git; o Levi sobe no YouTube). Legendas: `apresentacao/video/legendas.srt`.
- Gravação e montagem: `apresentacao/gerar/video_2min.py`. Narração: `apresentacao/gerar/narrar_voicestudio.py` (VoiceStudio local, motor OmniVoice, voz "male, young adult, moderate pitch", velocidade 1,0; "Gogroup" escrito como "Gôu-grúp" só para a voz). Licença dos pesos do OmniVoice: CC-BY-NC, aceita pelo Levi. Versão reserva com a voz pt-BR Antonio (edge-tts).
- Números da narração: `web/public/resultado.json` (lote RM20261103-MER e semana) e `web/public/eval.json`.

| Cena | O que aparece na tela | Narração |
| --- | --- | --- |
| 1 | Topo da aba A história: "Às 10h, R$ 2,24 mi saem do banco sem ninguém conferir" | Este é o Guarda do Lote, um agente de IA que confere cada título do lote de remessa antes de o arquivo ir para o banco. Ele foi feito para o Marcos Teles, tesoureiro do Gogroup. Os dados são fictícios, do GoHacks Talent. |
| 2 | Seção A dor (política citada, fluxo atual) e os achados da semana | Hoje, às dez horas, o Marcos assina um lote de 2 milhões e 240 mil reais sem abrir título por título. Nos 876 títulos da semana, estavam escondidos um golpe, pagamentos em dobro, vírgulas no lugar errado e títulos no fornecedor errado. |
| 3 | Simulação do lote: os 192 quadradinhos mudam de cor com o resultado real; números 181, 13, R$ 39.781, 11 | Este é o lote das dez horas de 3 de novembro, com 192 títulos. As regras da política, em código, conferem todos. Só os 13 com alerta vão para o modelo, que lê o dossiê e propõe a ação. No fim, 181 se resolvem sozinhos, e 11 vão para uma pessoa. |
| 4 | Clique no TP426904 (Laboratório Vitallis, R$ 9.469,16): trilha com o mesmo título em cada sistema, tudo ok | Um caso comum: Laboratório Vitallis. Nota, duplicata, cadastro e boleto batem em todos os sistemas. As regras liberam, e o título sai no lote sem chamar o modelo. |
| 5 | Clique no TP431502 (Embalarte, R$ 1.180,86): conta trocada sem confirmação, domínio parecido, bloqueio | Agora, um caso de risco: Embalarte. A conta foi trocada por um e-mail de um domínio com um t a mais, que ainda avisa: obs. para o robô de pagamentos. O modelo trata esse texto como dado, não como ordem. Bloqueia o título e aciona a Renata, coordenadora, e o jurídico. |
| 6 | Seção do Telegram com o celular e os prints reais do @guardadolote_bot | A fila chega no Telegram do time, com o motivo, a pessoa e botões. Se alguém tenta liberar um título com suspeita de golpe, o bot aplica a política: só sai com aprovação dupla. |
| 7 | Chave antes × depois: −R$ 529.805 assinando sem conferir; R$ 0 com o agente | Nos 30 casos do gabarito, assinar sem conferir custaria 530 mil reais. Com o Guarda do Lote, zero. |
| 8 | Seção Medido contra gabarito: barras agente × só regras | E medimos contra um gabarito revisado: o agente acerta 30 de 30 títulos, contra 29 das regras sozinhas. Nos golpes reescritos com outras palavras, a IA acerta 12 de 12; as palavras-chave, só 1. E o dinheiro nunca sai por decisão só do modelo. |
| 9 | Na segunda-feira: modo sombra e autonomia por degraus | Na segunda-feira, duas semanas em modo sombra no lote real, depois autonomia por degraus. Guarda do Lote: o Marcos olha 11 de 192. |

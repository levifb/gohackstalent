# Desafios GoHacks Talent 2026: Agentes de IA

Copiado do site do evento (`/api/publico`, campo `desafios`) em 07/11/2026 09:20.

## O que a organização espera

Cada desafio parte de uma dor real que uma empresa vive hoje, em uma área inteira, e não em uma tarefa isolada. Seu papel é imaginar e construir um agente de IA que trabalhe nessa área como um colega: que entenda o dia a dia, faça sozinho o que pode fazer e saiba pedir ajuda quando não pode. Descrevemos aqui os problemas, não as soluções. O como é seu.

**É:**
- Entende quais são os afazeres da área e acompanha o que acontece no dia a dia.
- Faz com autonomia o que está ao alcance dele, agindo nos sistemas, e não só sugerindo.
- Sabe levantar a mão: reconhece quando não consegue ou não deve decidir sozinho e chama a pessoa certa.
- Trabalha em equipe: pode chamar outros agentes quando precisa.

**Não é:**
- Um chatbot que responde perguntas.
- Uma IA consultando uma base de textos ou documentos.
- Uma automação que resolve um único passo e para ali.
- Um painel bonito que mostra o problema, mas não age sobre ele.

**Visão:** Cada problema tem várias frentes. Esperamos que o seu plano enxergue a área inteira: tudo o que esse colega deveria assumir, como as frentes se conectam e onde as pessoas continuam no controle. A prova de conceito do dia pode atacar uma frente só, desde que mostre como ela se encaixa nessa visão maior.

**Canais:** Um colega de trabalho não fica escondido em uma tela à parte. Se o seu agente conversar com as pessoas pelos canais que elas já usam, avisando, pedindo aprovação e recebendo pedidos, melhor: Slack, Google Chat, WhatsApp, Telegram ou outro.

**Dados:** As bases não são obrigatórias: elas servem para guiar. Se sentir necessidade, edite os dados ou crie os seus próprios dados fictícios. O grande ponto é o que o seu agente vai fazer.

---

## d1 · Atendimento ao Cliente (área: Atendimento)

**Dor:** Milhares de contatos por mês, por WhatsApp, e-mail e Reclame Aqui, e a maior parte ainda tratada à mão.

**Contexto:** Uma empresa de e-commerce recebe milhares de contatos de clientes todo mês, por WhatsApp, e-mail e Reclame Aqui. O volume é alto, e a maior parte ainda é tratada à mão.

**Por que é oneroso:** Resolver um contato quase nunca é só responder uma mensagem. Um único pedido de cliente pode exigir passar por vários sistemas: consultar o pedido, entrar no portal da transportadora, abrir um chamado, gerar uma troca ou um reenvio. E nem toda reclamação procede: há casos de avaria que não é real.

**Alguns dos desafios:**
- O volume e o tempo que cada contato consome.
- O trabalho espalhado entre sistemas e portais diferentes.
- Saber se a reclamação é verdadeira antes de agir.
- Decidir o que se resolve sozinho e o que precisa de uma pessoa.
- Contatos que se repetem e poderiam ter sido evitados.

## d2 · Pagamentos (área: Financeiro)

**Dor:** Muitos pagamentos, cadastro manual em vários sistemas e nenhuma forma de conferir cada um no detalhe.

**Contexto:** Uma empresa processa uma quantidade alta de pagamentos e, hoje, não consegue olhar cada um no detalhe.

**Por que é arriscado:** Vários processos dependem de cadastro manual em sistemas, o que abre espaço para erro: pagamento em duplicidade, um zero a mais, dado cadastrado errado. E a informação necessária para conferir está descentralizada, espalhada entre sistemas diferentes e bancos.

**Alguns dos desafios:**
- Um volume que não permite revisar pagamento por pagamento.
- Processos de cadastro extremamente manuais, repetidos em mais de um sistema.
- Erros que nascem no cadastro manual: duplicidade, valores errados.
- Informação fragmentada entre sistemas internos e bancos.
- Pegar o erro antes de o dinheiro sair, e não depois.
- Saber o que pode seguir sozinho e o que precisa de aprovação.

## d3 · Transportes (área: Transportes)

**Dor:** Várias transportadoras, cada uma num portal diferente, e um prazo no site que precisa vender sem quebrar o SLA.

**Contexto:** Uma empresa trabalha com várias transportadoras, e cada envio pode ir por uma delas. As informações de cada uma ficam em portais diferentes.

**Por que é difícil:** O prazo mostrado no site precisa vender, mas não pode ser irreal a ponto de quebrar o SLA com o cliente. Para acertar isso, é preciso saber quem entrega bem em cada região, a que preço e como a empresa está em relação aos concorrentes, e hoje essa visão é montada à mão, quando é montada.

**Alguns dos desafios:**
- Escolher a melhor transportadora para cada envio.
- Definir o prazo do site: competitivo para converter, realista para cumprir.
- Medir a performance de cada transportadora por cabeça de CEP.
- Entender o posicionamento: o prazo está melhor, igual ou muito pior que o dos concorrentes?
- Definir o melhor preço de frete para cada região.
- Reunir informação que hoje está espalhada em vários portais.

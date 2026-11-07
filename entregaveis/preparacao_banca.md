# Preparação para a banca: como funciona e respostas curtas

## 1. Como funciona, para eu explicar com as minhas palavras (1 minuto)

1. **Entrada.** O agente lê o lote de remessa (agenda_remessa: 192 títulos no lote das 10h de 03/11) e, para cada título, puxa o que os sistemas dizem: ERP (título e cadastro do fornecedor), Compras (OC), portal NF-e (nota e duplicatas), DDA (boleto registrado), os extratos dos dois bancos e a caixa de e-mail. Tudo passa por um arquivo só, `agente/fonte.py`.
2. **Triagem por regras, em código (`agente/regras.py`).** São as regras da política escritas como `if`: duplicidade, valor do título contra a duplicata (tolerância de R$ 0,10), NF contra OC (2% ou R$ 50), CNPJ da nota contra o do fornecedor (pega o fornecedor trocado), boleto no DDA (já pago? beneficiário de outro CNPJ?), troca de conta sem ligação de confirmação, domínio de e-mail parecido, pagamento já feito fora do lote, alçada e fracionamento. Cada regra gera um alerta com gravidade: bloqueio, aprovação, correção ou atenção. Alguns alertas são "contestáveis" (ex.: banco de cobrança novo): o modelo pode julgá-los. Os duros (golpe, alçada, troca de conta) só uma pessoa resolve.
3. **Quem não tem alerta sai liberado sem chamar o modelo.** No lote das 10h: 179 de 192. Isso é rápido, barato e previsível.
4. **Dossiê + modelo.** Para os 13 com alerta, o código monta um dossiê (o título, a nota, a OC, o boleto, o cadastro, as trocas de conta, os e-mails do fornecedor, o lançador) e manda ao modelo (`gpt-6-astra`, pelo AI Proxy do evento). O prompt (`agente/prompts.py`) explica a política, o custo de errar para os dois lados, traz 4 exemplos e manda tratar texto de e-mail como dado, nunca como ordem. A resposta volta em JSON e é validada (pydantic): ação, pessoa a acionar, confiança e motivo. Se o JSON vier inválido, tenta de novo uma vez; se falhar, vai para revisão humana.
5. **Trava (`regras.travar`).** O código confere a proposta do modelo: ele não pode liberar com alerta duro ativo, não pode descartar alerta duro, não pode corrigir ou cancelar acima de R$ 5 mil (alçada do analista) e, se a confiança for menor que 0,7, não deixa dinheiro sair. Se violar, vale a decisão das regras.
6. **Ação e fila.** As ações são simuladas: liberar, corrigir, cancelar, retirar do lote, bloquear, pedir aprovação. Quem precisa de uma pessoa vai para a fila com o nome certo da política (Renata, coordenadora; Helena, diretora acima de R$ 50 mil; Lívia, jurídico; compradores; controller) e é publicado no Telegram com botões. O webhook na Vercel aplica a política no clique (liberar golpe exige aprovação dupla).
7. **Segundo agente: sentinela de e-mails (`agente/sentinela.py`).** Lê os 246 e-mails da caixa da área. O Jev (classificador do AI Proxy, barato e rápido) responde perguntas fechadas: assunto, se o texto dá ordem a um sistema, se há pressão ou pedido de senha, se pede pagamento por fora, se diz que a conta continua a mesma. O código cruza com o cadastro e decide: golpe, tentativa de instruir o agente, pedir confirmação de troca, conciliar ou nada. As marcas viram contexto para o agente do lote.
8. **Medição (`eval/`).** Gabarito de 30 títulos revisado por mim, validação cega de 12, julgamento com 6 casos criados por mim, sentinela com 17 e-mails reais e 12 reescritos. O eval imprime acerto por etapa e compara com "só regras" e "palavras-chave".

Stack: Python (pandas, pydantic, httpx) no agente; React + TypeScript (Vite) no site, publicado na Vercel com duas funções de servidor (reanálise ao vivo e webhook do Telegram). O token do modelo fica só no servidor.

## 2. Perguntas prováveis e respostas curtas

**Como funciona tecnicamente?**
Regras da política em código olham cada título em sete sistemas; o que está limpo sai sem modelo. O que tem alerta vai com um dossiê para o modelo, que propõe ação, pessoa e motivo em JSON validado, e uma trava no código impede que ele libere o que a política segura. Os casos de risco chegam no Telegram da pessoa certa.

**Se as regras sozinhas acertam 29 de 30, para que serve o modelo?**
Nos dados da organização quase todo alerta é duro, e aí quem decide o dinheiro são as regras; foi uma escolha. O modelo entra onde a regra não decide sozinha: nos alertas contestáveis ele acertou 6 de 6 contra 3 de 6 das regras, liberando pagamentos legítimos que as regras atrasariam. Ele também escolhe a pessoa, explica o motivo, e na caixa de e-mail acerta golpes escritos de outro jeito (12 de 12 contra 1 de 12 das palavras-chave).

**Onde a IA errou e como você percebeu?**
Três exemplos: a regra de domínio parecido, escrita pelo Claude, bloqueava um fornecedor legítimo (Cartonart × Cartonar), vi lendo os casos; o eval v1 deu 26 de 29 e a correção abriu uma regressão, que o próprio eval pegou; e um prompt meu dizia "você libera até R$ 5 mil", o que derrubou o julgamento para 2 de 6. Tudo está no LOG.md com horário e antes/depois.

**Quem usaria?**
O tesoureiro, que assina o lote, e a coordenadora de contas a pagar, que recebe os casos de risco. Os aprovadores (diretora, compradores, jurídico) recebem só o que é deles, no Telegram.

**O que falta para ir para produção?**
Trocar os CSVs pelas fontes reais (ERP, portal NF-e, DDA, extratos, caixa de e-mail) no `fonte.py`; as ações saírem do simulado para as ferramentas do ERP com o papel de analista; e duas semanas em modo sombra para medir. Também cuidar de LGPD e sigilo bancário: dados bancários e CNPJs, com o menor acesso possível.

**Como medir o sucesso?**
Processo: % de títulos resolvidos sem humano e quantos casos chegam a uma pessoa. Negócio: o placar da própria área em R$ (dinheiro que sai indevido + atraso de pagamento legítimo + R$ 60 por acionamento desnecessário). No modo sombra: erros reais retidos e pagamentos legítimos segurados sem motivo.

**O 30 de 30 não é sobreajuste?**
Em parte, sim, e eu digo isso: ajustei regras e gabarito nos mesmos casos. Por isso fiz uma validação cega com 12 títulos sorteados e anotados antes de ver a decisão (12 de 12) e casos novos de julgamento. A prova de verdade é o modo sombra com dados reais.

**E se o modelo cair ou alucinar?**
Se cair, os títulos com alerta vão para revisão humana e nada sai; o site tem modo demo com cache. Se alucinar, a trava barra: ele não consegue liberar com alerta duro, nem acima da alçada, nem com confiança baixa. O dinheiro nunca sai só pela palavra do modelo.

**E injeção de prompt (um e-mail mandando o robô liberar)?**
Aconteceu nos dados: a Embalarte falsa e a Flexipack. O prompt manda tratar texto como dado, o modelo marca "instrução suspeita", a sentinela aciona o jurídico e, mesmo que o modelo acreditasse, a trava não deixa liberar um golpe.

**Quanto custa rodar?**
A semana inteira (876 títulos) usou cerca de 70 chamadas ao modelo (uns 250 mil tokens de entrada) porque só os títulos com alerta vão para ele, e a caixa inteira de e-mails no Jev custou cerca de US$ 0,01. Tudo fica em cache.

**Por que não bloquear tudo que tem alerta?**
Porque atrasar pagamento legítimo também custa: multa, juros e relacionamento (R$ 3.000 por título de fornecedor de produto, pela política). Nos 30 casos, bloquear todo alerta custa R$ 1.493; o agente, R$ 0.

**Por que Telegram?**
O desafio pede que o agente converse com as pessoas pelos canais que elas usam. O Telegram foi o mais rápido de integrar no dia; com o canal oficial do time (Slack, Google Chat) muda só a camada de envio.

**O que é real e o que é simulado?**
Real: o agente rodando sobre os dados fictícios da organização, o modelo, o eval, o site, o bot e os cliques. Simulado: as ações nos sistemas (nada é alterado de verdade) e o chat do Telegram, que é de teste.

**O que você faria com mais um dia?**
Mais casos ambíguos no gabarito, o pré-lançamento do título a partir do XML (atacar o cadastro manual na origem) e a conciliação pós-pagamento para os 12 e-mails de divergência que a sentinela já separa.

## 3. Números para ter na ponta da língua

- Lote das 10h de 03/11: 192 títulos, R$ 2,24 mi; 181 resolvidos sozinho, 13 analisados pelo modelo, 11 para uma pessoa.
- Semana: 876 títulos, R$ 10,2 mi; 93% sem humano; R$ 648 mil retidos por erro, golpe ou documento faltando.
- Golpe da Embalarte: 25 títulos, R$ 194 mil.
- Eval: 30/30 (só regras 29/30); julgamento 6/6 (só regras 3/6); e-mails reescritos 12/12 (palavras-chave 1/12); validação cega 12/12; v1 do eval 26/29.
- Placar nos 30 casos: assinar sem conferir R$ 530 mil; bloquear todo alerta R$ 1.493; agente R$ 0.

# Prompts do dia: GoHacks Talent

Junto com estes prompts vai o `claude_contexto_hackathon.md`, que explica as regras e os critérios. Aqui ficam só as mensagens de cada fase, para copiar, completar os `[colchetes]` e enviar.

---

## 0. Credenciamento (8h30 a 9h00)

No app do evento, aba "Minha jornada": agende o horário do pré-júri (16h35 a 18h10). Prefira um horário a partir de umas 17h: dá tempo de ensaiar o pitch e fechar o relatório sem pressa, e a banca já viu alguns projetos para comparar. Pergunte à organização como o app publicado deve chamar o modelo (chave de API, proxy do grupo ou só a conta do Claude) e se o relatório individual é entregue até 16h30.

Teste se tudo funciona antes de saber o desafio:

```
Leia claude_contexto_hackathon.md. Ainda não sei o desafio. Por enquanto:
1. confira se git, node/python e o acesso a modelo para o produto funcionam neste notebook
   (chave de API ou proxy, se a organização tiver dado; senão teste `claude -p "responda só {\"ok\": true}" --output-format json`)
   e faça uma chamada de teste mínima, mostrando a resposta;
2. me diga o que falta configurar para eu publicar um app na Vercel daqui.
Não crie projeto ainda.
```

---

## 1. Abertura: quando eu souber o desafio (09h40)

Os desafios aparecem no site às 9h e a escolha abre às 9h40, depois do mini workshop. Leia o catálogo assim que abrir.

Ordem da abertura:
1. `prompt_escolher_desafio.md` (às 9h, com o catálogo): o Claude lê todos os desafios e os dados que houver, recomenda um e já devolve o entendimento do processo, 3 recortes e as perguntas. Eu confirmo.
2. `prompt_criar_skills.md`: o Claude cria até 5 skills para o desafio e o CLAUDE.md do projeto.
3. A mensagem "Fechado: ..." abaixo, para escrever o SPEC.

Se eu mesmo escolher o desafio, pulo o passo 1 e uso a mensagem a seguir no lugar dele:

```
O desafio que escolhi é este:
<desafio>
[cole o texto do desafio do catálogo]
</desafio>

Os dados fictícios estão em: [caminho da pasta/arquivos]
Stack: [React+TS na Vercel | Python+Streamlit | deixe você sugerir]
Hora agora: [hh:mm]

Siga o claude_contexto_hackathon.md. Nesta primeira etapa não escreva código do produto:
1. leia o desafio e explore os dados (volumes, colunas, categorias, casos estranhos);
2. me devolva em até 15 linhas como esse processo funciona hoje, quem sofre, onde está o atrito
   e o que os dados permitem medir;
3. proponha 3 recortes de problema, cada um com persona, dor, ideia de agente e métrica,
   e ranqueie pelos critérios da banca (principalmente Modelagem e Conceito);
4. me faça no máximo 5 perguntas de múltipla escolha para fechar o recorte.
```

Depois de responder às perguntas:

```
Fechado: [recorte escolhido]. Escreva o SPEC.md (persona, dor, fluxo atual, fluxo novo,
métrica, impacto, definição do pronto, suposições) e crie LOG.md, README.md com a frase de pitch
e a estrutura do projeto. Inicie o git e faça o primeiro commit. Me mostre o SPEC em 10 linhas
para eu validar com um mentor.
```

---

## 2. Ponta a ponta (até 12h)

```
SPEC validado [incluir o feedback do mentor, se houver]. Agora construa a fatia mais fina
de ponta a ponta: carregar os dados fictícios pela camada de fonte de dados → uma etapa com IA
via o acesso a modelo combinado (saída JSON validada) → resultado na tela. Pode ser feio. Depois:
publique na Vercel [ou Streamlit Cloud], abra o link e me confirme que funciona sem login. Commit.
```

---

## 3. Gabarito e eval (logo depois do almoço)

```
Vamos medir. Selecione 25 casos variados dos dados (inclua difíceis e ambíguos) e monte
gabarito com a resposta que você acha certa para cada um. Eu vou revisar e corrigir o gabarito
antes de usar. Depois crie o script de eval, que roda o pipeline em todos e imprime acerto por etapa
e a lista de erros. Rode e me mostre o resultado.
```

Depois de revisar o gabarito:

```
Corrigi o gabarito nos casos [ids]. Rode o eval de novo, analise os erros, agrupe por causa
e proponha a menor mudança no prompt ou no código para cada grupo. Aplique uma por vez,
rode o eval depois de cada uma e registre no LOG.md o antes e depois.
```

---

## 4. Agente completo (até 14h30)

```
Complete o agente conforme o SPEC: [ferramentas que faltam], regras duras no código
([ex.: valor > R$ 300 vai para humano]), saída "revisao_humana" com motivo para baixa confiança,
e processamento do lote inteiro sem intervenção. A tela deve mostrar: quantos casos foram
resolvidos sozinhos, quantos foram para humano e por quê. Rode o eval no final.
```

Se algo travar:

```
Isso falhou duas vezes. Pare, me explique em 3 linhas a causa provável e proponha um plano B
mais simples que preserve o ponta a ponta. Registre a mudança de rota no LOG.md.
```

---

## 5. Polimento da demo (14h30 a 15h20)

Antes de polir, rode o `agente_avaliador.md` num terminal novo para saber onde está a nota mais fraca. Repita às 15h10 e às 16h00.

```
Hora: [hh:mm]. Foco na demo para a banca. Ajuste a interface para contar a história em 10 segundos:
persona e problema no topo, o que entrou, o que o agente fez em cada etapa, casos para o humano
com motivo, e o antes e depois com o número do eval. Sem cara de template: nada de gradiente roxo,
emoji ou card dentro de card. Ative o modo demo com cache dos casos [ids] que vou mostrar.
Rode o build, publique e me mande o link.
```

Para pedir uma revisão independente:

```
Use um subagente que não viu esta conversa para revisar o código contra o SPEC.md: o fluxo do pitch
funciona, alguma chave ficou exposta, algum número na tela não vem do eval? Reporte só problemas
que afetam a demo ou a correção. Ignore estilo.
```

---

## 6. Congelamento e entregáveis (15h20)

```
Congelamento. A partir de agora, só correção de bug. Gere, nesta ordem:
1. os textos da submissão (problema 600, solução 800, uso de IA 800, impacto 500 caracteres),
   com a contagem de caracteres de cada um;
2. os slides com a skill apresentacao-pitch: roteiro primeiro, depois o PDF (e o .pptx, se der),
   com as capturas reais do app;
3. o roteiro do pitch de 5 min com tempos;
4. o roteiro do vídeo de 2 min.
Use fatos do SPEC, do eval e do LOG.md. Siga o estilo de texto do arquivo de contexto.
Atualize o README (resultado do eval, "Com dados reais", próximos passos) e faça o commit final.
Confirme que o repositório está pronto para ficar público: nenhum segredo, .env fora do git.
```

---

## 7. Enquanto espero o pré-júri (16h30 até o meu horário)

```
Me sabatine como a banca faria: 8 perguntas, uma de cada vez. Espere minha resposta e me dê
um retorno curto (o que faltou, como responder em 2 frases). Inclua: como funciona tecnicamente,
quem usaria, o que falta para produção, como medir o sucesso, onde a IA errou e como percebi,
e o que eu faria com mais um dia.
```

```
Rascunhe o relatório individual a partir do LOG.md, respondendo às 5 perguntas do evento.
Frases curtas, em primeira pessoa, com episódios concretos. Eu vou reescrever com minhas palavras.
```

---

## Atalhos durante o dia

- Desvio: `Esc` e redirecione.
- Duas correções falharam: `/clear`, cole o contexto de novo (ou confie no CLAUDE.md) e escreva um prompt melhor com o que aprendeu.
- Problema difícil de raciocínio: comece o prompt com `ultrathink`.
- Antes de cada commit importante: "rode o build e o eval e me mostre a saída".
- Feedback de mentor: "Mentor disse: [x]. Registre no LOG.md e me diga em 3 linhas o que muda no plano."

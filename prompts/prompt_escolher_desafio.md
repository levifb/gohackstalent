# Prompt: o Claude escolhe o desafio

Os desafios aparecem no site do evento às 9h e a escolha abre às 9h40. Use este prompt assim que o catálogo abrir: copie os enunciados para a pasta do projeto (e os dados, se já estiverem disponíveis). Se os dados só vierem depois da escolha, o Claude avalia pelos enunciados e diz isso. A ideia é que o Claude leia todos os desafios e escolha aquele em que dá para tirar a maior nota, pesando a tabela de critérios do `claude_contexto_hackathon.md`. A decisão final é minha: ele recomenda e eu confirmo.

Tempo previsto: até 15 minutos, para eu chegar às 9h40 com o desafio e um plano B decididos. Depois deste prompt vem o `prompt_criar_skills.md`.

---

```
Hora agora: [hh:mm]. A submissão fecha às 16h30.

Leia o claude_contexto_hackathon.md inteiro antes de tudo. Ele traz a tabela de critérios da banca,
que é a régua desta escolha.

Nesta pasta estão os enunciados de todos os desafios e os dados fictícios de cada um
[se souber, diga onde: pasta/arquivo]. Quero que você escolha o desafio em que temos a maior chance
de tirar a nota mais alta e de nos destacar entre os outros participantes. Não escreva código do produto
ainda.

1. Leia cada enunciado completo e, se os dados já estiverem aqui, abra os de cada um (tamanho, colunas,
   exemplos de linhas, qualidade): dados pobres ou confusos mudam a nota possível. Se ainda não houver
   dados, avalie pelo enunciado e diga o que precisaria ser verdade nos dados para a nota se confirmar.

2. Para cada desafio, dê uma nota de 0 a 10 em cada critério, pensando no melhor projeto que dá para
   entregar até as 16h30 com uma pessoa e com você:
   - Modelagem (40%): cabe um agente de ponta a ponta com etapas nomeadas, ferramentas que leem os
     dados, regras duras no código e humano no loop? O lote roda sozinho? Dá para montar um gabarito
     de 20 a 30 casos a partir dos dados e medir acerto com um eval? Desafio em que a "IA" vira
     um chatbot ou um dashboard sem decisão rende pouco aqui.
   - Conceito (20%): existe uma persona clara com uma dor que custa dinheiro ou tempo? Dá para
     explicar problema e solução em 90 segundos de demo?
   - Adaptabilidade (20%): os dados permitem números concretos para o pitch? O caminho para dados
     reais é fácil de explicar?
   - Aderência cultural (20%): o problema é central para o negócio do grupo (e-commerce de
     acessórios e beleza), a ponto de eu poder falar como dono dele?
   Calcule a nota ponderada de 0 a 100.

3. Depois ajuste por risco e por diferenciação, explicando cada ajuste:
   - risco de execução: integrações que não temos, dados que faltam, escopo que não cabe no dia,
     dependência de algo que a organização não forneceu;
   - diferenciação: somos 26 participantes e só 10 vão para a final; qual desafio a maioria tende a escolher, e se dá para fazer nele algo que
     destoe; um desafio menos óbvio, bem executado, pode render mais;
   - meu perfil: Python, pandas e ML (previsão de demanda, detecção de anomalias, XGBoost),
     React + TypeScript, e experiência com pipelines de agentes (subagentes do Claude Code).
     Programação competitiva me deixa rápido com lógica e algoritmos.

4. Entregue, curto:
   - tabela com os desafios nas linhas, as quatro notas, a ponderada, o ajuste e a nota final;
   - o desafio recomendado em uma frase, e o segundo colocado como plano B, com o motivo da troca
     caso o primeiro trave;
   - para o recomendado: em até 15 linhas, como esse processo funciona hoje na empresa, quem participa,
     onde está o atrito, o que os dados permitem medir e o que falta (com as suposições listadas);
   - 3 recortes do problema, cada um com persona, dor, ideia de agente e métrica, ranqueados pelos
     critérios (principalmente Modelagem e Conceito);
   - no máximo 5 perguntas de múltipla escolha para fecharmos o recorte, e uma pergunta boa para
     levar a um mentor.

Não invente fatos sobre o negócio: o que não está no enunciado nem nos dados entra como suposição.
```

---

Depois que eu confirmar o desafio e o recorte, sigo para o `prompt_criar_skills.md` e então para o SPEC (seção 1 do `prompts_do_dia.md`).

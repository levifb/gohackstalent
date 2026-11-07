---
name: eval-gabarito
description: Gabarito de 20 a 30 títulos anotados e o script de avaliação do agente Guarda do Lote (acerto por etapa, lista de erros, placar em R$ contra os baselines), além de testes das regras determinísticas. Use ao montar ou revisar o gabarito, ao rodar o eval depois de qualquer mudança de prompt ou regra, ao analisar erros do agente e ao registrar antes/depois no LOG.md. Não use para escrever as regras (politica-cp) nem o prompt (agente-guarda-lote).
---

# Gabarito e eval

Dono de: `eval/gabarito.csv`, `eval/eval.py`, `tests/` e das linhas de LOG.md sobre acerto do agente. O número do eval é o principal argumento de Modelagem: tem que ser reproduzível com um comando.

## Gabarito (`eval/gabarito.csv`)

Colunas: `titulo_id, lote, diagnostico_esperado, acao_esperada, acionar_esperado, valor_corrigido_esperado, dificuldade (facil|media|dificil), justificativa, revisado_por_levi (sim|nao)`.

Composição (25 a 30 casos, quase todos do lote `RM20261103-MER`; complete com outros lotes se faltar um tipo):
- 8 a 10 limpos que devem ser liberados (incluir 2 a 3 com alerta falso: banco de cobrança diferente porém histórico, filial com outra razão social, multa/juros legítimos);
- 4 a 5 duplicidades (incluir NF digitada com zeros ou série diferente);
- 3 a 4 valores errados (vírgula deslocada para mais e para menos, e um erro pequeno);
- 2 a 3 da troca bancária sem confirmação (FP4615) e o caso do domínio `embalartte.com.br` se houver título ligado;
- 2 a 3 de alçada/aprovação dupla (acima de R$ 50 mil, fracionamento, sem NF/OC);
- 1 a 2 ambíguos em que a resposta certa é `revisao_humana`.

A anotação inicial é proposta pelo Claude com a justificativa citando a regra (skill politica-cp); o Levi revisa e marca `revisado_por_levi=sim`. Não rode o eval como número oficial antes da revisão.

## Script (`python eval/eval.py [--sem-llm] [--casos id1,id2]`)

Usa `pipeline.processar_titulo` (a mesma função da interface). Imprime:
1. acerto por etapa: triagem (alerta certo?), diagnóstico, ação, pessoa acionada, valor corrigido;
2. acerto final (ação certa) em `n/N`;
3. matriz simples esperado × obtido para a ação;
4. lista de erros: id, esperado, obtido, motivo do modelo;
5. placar em R$ do agente vs. "assinar sem conferir" vs. "bloquear todo alerta" (via `placar.py`);
6. tokens gastos (se o proxy informar) e quantos vieram do cache.
Salva `eval/resultados/eval_<hhmm>.json` para comparar rodadas.

`--sem-llm` mede só as regras determinísticas (roda sem proxy, útil antes da URL do proxy existir).

## Ciclo de melhoria

1. Rodar eval → agrupar erros por causa (regra, dossiê incompleto, prompt, gabarito errado).
2. Propor a menor mudança para cada grupo; aplicar uma por vez; rodar de novo.
3. Registrar no LOG.md: `hh:mm | o que errou | como percebemos (eval x/N) | o que mudou | antes → depois`.
4. Se o gabarito estiver errado, corrigir com justificativa e registrar também (isso é conferir a IA, conta ponto).

## Testes (`pytest`)

Testes curtos das regras com casos reais: normalização de NF, raiz de CNPJ, valor da linha digitável, tolerância de R$ 0,10, alçada com fracionamento, troca bancária < 30 dias. Rodar `pytest -q` antes de cada commit importante.

## Erros a evitar

- Gabarito só com casos fáceis (o número fica bonito e a banca desconfia).
- Medir só o acerto final: a banca pergunta "onde errou"; mostre por etapa.
- Número de eval na tela ou no slide que não corresponde ao último `eval_<hhmm>.json`.

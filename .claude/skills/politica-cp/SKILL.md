---
name: politica-cp
description: Regras de negócio de contas a pagar do Gogroup traduzidas em verificações no código e no cálculo do placar em R$ (alçadas, aprovação dupla, conferência de 3 vias, troca de dados bancários, boleto, duplicidade, fracionamento, quem acionar). Use ao escrever agente/regras.py, ao decidir se uma ação do modelo pode ser aplicada, ao definir a resposta certa de um caso do gabarito ou ao calcular o impacto em R$ para o pitch. Não use para leitura de arquivos (dados-pagamentos) nem para prompt (agente-guarda-lote).
---

# Política de contas a pagar como código

Dona de: `agente/regras.py` (verificações determinísticas e trava das ações), `agente/placar.py` (placar em R$) e das respostas de negócio do gabarito. Fonte: `dados/pagamentos/politicas.csv` e `parametros.md`. Toda regra abaixo cita a linha da política; o que não está lá entra como suposição no SPEC.

## Princípio

O modelo propõe; o código decide se pode. Regra que não pode errar fica num `if`, nunca só no prompt. Cada verificação devolve um alerta estruturado: `{codigo, gravidade (bloqueio|aprovacao|atencao), evidencia, regra_citada}`.

## Verificações por título (rodam nos 192 títulos, sem modelo)

| Código | Regra (politicas.csv) | Implementação |
| --- | --- | --- |
| `DUPLICIDADE` | título já lançado | outro título vivo (não cancelado) com mesmo fornecedor, NF normalizada e parcela; ou mesmo fornecedor + valor + vencimento; ou já pago (status pago ou no extrato Meridiano com `documento`) |
| `VALOR_DUPLICATA` | tres_vias.titulo_x_duplicata: diferença até R$ 0,10 | `abs(valor - valor_dup) > 0.10`; marcar fator 10/0,1 como `VIRGULA_DESLOCADA`; aceitar multa 2% + juros 1% a.m. pro rata se pago após vencimento |
| `NF_OC` | tres_vias.nf_x_oc: NF até 2% ou R$ 50 acima da OC (o maior) | `valor_total_nf > valor_oc + max(0.02*valor_oc, 50)` → acionar comprador (PS04 produto/embalagens, PS05 insumos/serviços) |
| `SEM_NF` / `SEM_OC` | dispensas: utilidades sem OC, aluguel sem NF | sem NF fora de aluguel, ou sem OC aprovada fora de utilidades → aprovação dupla |
| `RAIZ_CNPJ` | tres_vias.fornecedor | raiz da NF ≠ raiz do fornecedor do título (filial com mesma raiz é ok) |
| `BOLETO_BENEFICIARIO` | dados_bancarios.boleto | banco (linha digitável 1-3) ou CNPJ do beneficiário ≠ fornecedor e ≠ banco de cobrança histórico no DDA |
| `TROCA_BANCARIA` | aprovacao_dupla.quando + dados_bancarios.troca_de_conta | alteração de banco/agência/conta/pix há menos de 30 dias com `confirmacao_registrada != sim`, ou confirmada por telefone novo/informado na mensagem |
| `ALCADA` | alcadas | valor (somado por fornecedor + NF + dia, regra de fracionamento) > 5 mil → aprovador; > 50 mil → aprovador + PS03 |
| `FRACIONAMENTO` | alcadas.fracionamento | vários títulos do mesmo fornecedor/NF/dia que somados passam da alçada |
| `PAGO_FORA_DO_LOTE` | dados_bancarios.pagamento_manual | pagamento avulso no extrato para o fornecedor/valor e título ainda agendado |

## Trava das ações (o que o agente pode fazer sozinho)

Papel do agente: `analista_cp` (ver `ferramentas.csv`).
- `liberar`: só sem alerta de gravidade bloqueio/aprovacao e valor dentro da alçada do analista (até R$ 5 mil) ou já aprovado.
- `corrigir_lancamento`: diferença de valor até R$ 5 mil e a duplicata da NF é a fonte inequívoca.
- `retirar_do_lote` / `cancelar_titulo` (duplicidade): cancelar só até R$ 5 mil; acima, retirar do lote e `solicitar_aprovacao`.
- Troca bancária sem confirmação: nunca liberar; retirar do lote, `acionar_pessoa` PS01 (suspeita de fraude) e `contatar_fornecedor` pelo telefone **anterior** do cadastro.
- Golpe provável (domínio parecido, urgência, "diretor" por canal fora do habitual): PS01 + PS08 (jurídico); acima de R$ 50 mil também PS03.
- Segregação: quem lançou não aprova a própria ação.

## Placar (parametros.md)

`placar = -(dinheiro_indevido + custo_atraso_legitimo + 60 * acionamentos_desnecessarios)`
- dinheiro indevido: valor pago a mais, em duplicidade, a terceiro ou golpista.
- atraso de título legítimo retirado sem necessidade: 7 dias corridos → `valor*0.02 + valor*0.01*7/30 + custo_relacionamento[categoria]` (produto 3000, frete 1500, embalagens 800, insumos_capa 800, aluguel 500, ti_saas 400, utilidades 400, servicos 300, marketing_agencia 300, influenciador 250).
- Comparar sempre com o cenário atual (assinar tudo sem conferir) e com "bloquear tudo que tem alerta". Mostrar os dois baselines no pitch.

## Erros a evitar

- Bloquear todo alerta: atrasar legítimo custa caro (R$ 3.000 por título de produto). O objetivo é o placar, não o número de alertas.
- Confiar em confirmação feita para telefone trocado há menos de 30 dias.
- Esquecer a soma por fornecedor + NF + dia na alçada.
- Inventar regra: se a política não diz, registre como suposição no SPEC e pergunte ao Levi.

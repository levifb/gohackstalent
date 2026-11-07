# LOG

Erros da IA e correções, mudanças de rota e feedbacks, com horário.

| Hora | O que aconteceu | Como percebemos | O que mudou |
| --- | --- | --- | --- |
| 09:20 | O site do evento é renderizado por JavaScript; a primeira leitura (fetch) não trouxe os desafios | A página voltou só com o título | Lemos os enunciados direto da API pública do site (`/api/publico`) e salvamos em `materiais/desafios.md` |
| 09:25 | O notebook não tinha Python nem Node instalados | `python` abria a Microsoft Store | Instalamos Python 3.12, Node 26, gh e Vercel CLI via winget/npm |
| 09:39 | Na escolha do desafio, o Claude disse ter lido todos os prompts, mas só tinha lido 2 de 5 | Pergunta direta do Levi | Leu os 5; a escolha (Pagamentos) se manteve, agora com sonda nos dados |
| 09:40 | Primeira busca por e-mails de troca de conta voltou 0 | O assunto "Alteração de dados bancários" aparecia 3 vezes na contagem por assunto | A regex procurava termos que não estavam no texto; refeita pelo assunto, achou o e-mail do domínio `embalartte.com.br` |
| 09:55 | Desafio escolhido: Pagamentos, recorte "guarda do lote" | Notas pelos critérios: Pagamentos 91, Atendimento 78, Transportes 70 | SPEC.md escrito |
| 10:05 | O AI Proxy é no formato OpenAI e serve GPT, GLM, MiMo, Kimi e Jev, não Claude | `GET /v1/models` | Cliente `agente/llm.py` em `/v1/chat/completions` com `gpt-6-astra`; depois ajustado à skill ai-proxy (variável `AI_PROXY_API_KEY`, linha de custo por chamada, espera no 429, função Jev) |
| 10:08 | Regra de "domínio parecido" (escrita pelo Claude) marcou `cartonart.com.br` como imitação de `cartonar.com.br` | Lendo os casos: Cartonart é outro fornecedor legítimo cadastrado (FP5079), com troca de conta confirmada por ligação | Domínio que pertence a qualquer fornecedor cadastrado deixa de ser "parecido"; 4 títulos legítimos deixaram de ser bloqueados (6 → 2 alertas no lote 03/11); teste `test_dominio_de_outro_fornecedor_nao_e_parecido` |
| 10:09 | O SPEC dizia "26 títulos em duplicidade" | A triagem do agente achou 13 | A sonda contava o original e a cópia; as cópias de fato são 13 (R$ 105 mil). SPEC corrigido |
| 10:14 | Trava da política acionada em 4 títulos com vírgula deslocada em que o modelo propôs a correção certa | Inspeção dos casos com trava em `saida/resultado.json` | A trava contava o próprio alerta que a correção resolve; agora a correção para o valor da duplicata (dentro da alçada) resolve o alerta. Travas falsas: 4 → 0; teste `test_correcao_resolve_virgula_dentro_da_alcada` |
| 10:15 | Primeiro ponta a ponta: 876 títulos, 812 resolvidos sozinhos (92,7%), 64 na fila humana, 73 analisados pelo modelo (253 mil tokens), 192 s | `python -X utf8 -m agente.rodar` | Golpe da Embalarte bloqueado pelo modelo, que marcou a instrução no e-mail como suspeita |

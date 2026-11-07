# LOG

Erros da IA e correções, mudanças de rota e feedbacks, com horário.

| Hora | O que aconteceu | Como percebemos | O que mudou |
| --- | --- | --- | --- |
| 09:20 | O site do evento é renderizado por JavaScript; a primeira leitura (fetch) não trouxe os desafios | A página voltou só com o título | Lemos os enunciados direto da API pública do site (`/api/publico`) e salvamos em `materiais/desafios.md` |
| 09:25 | O notebook não tinha Python nem Node instalados | `python` abria a Microsoft Store | Instalamos Python 3.12, Node 26, gh e Vercel CLI via winget/npm |
| 09:39 | Na escolha do desafio, o Claude disse ter lido todos os prompts, mas só tinha lido 2 de 5 | Pergunta direta do Levi | Leu os 5; a escolha (Pagamentos) se manteve, agora com sonda nos dados |
| 09:40 | Primeira busca por e-mails de troca de conta voltou 0 | O assunto "Alteração de dados bancários" aparecia 3 vezes na contagem por assunto | A regex procurava termos que não estavam no texto; refeita pelo assunto, achou o e-mail do domínio `embalartte.com.br` |
| 09:55 | Desafio escolhido: Pagamentos, recorte "guarda do lote" | Notas pelos critérios: Pagamentos 91, Atendimento 78, Transportes 70 | SPEC.md escrito |

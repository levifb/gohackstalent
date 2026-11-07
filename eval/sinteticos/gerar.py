"""Gera o lote sintético RM20261116-SIN: títulos fictícios criados por nós (não vieram da organização)
para medir o julgamento do modelo em alertas contestáveis. Só é carregado com INCLUIR_SINTETICOS=1.

uso: python -X utf8 eval/sinteticos/gerar.py
"""
import csv
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
LOTE, DATA, BANCO_PAGADOR = "RM20261116-SIN", "2026-11-16", "Banco Meridiano"


def chave(cnpj14, numero):
    return f"23" + "2611" + cnpj14 + "55" + "001" + f"{int(numero):09d}" + "1" + "00000000" + "0"


def linha(banco, valor, venc):
    fator = (date.fromisoformat(venc) - date(2025, 2, 22)).days + 1000
    corpo = f"{banco}9" + "1234567890123456789012345678" + "9"
    return corpo + f"{fator:04d}" + f"{round(valor * 100):010d}"


def escrever(nome, linhas):
    with open(AQUI / f"{nome}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        w.writeheader()
        w.writerows(linhas)


# (titulo, fornecedor, cnpj, razao, nf, oc, valor, forma, banco_boleto, destino, cenário)
casos = [
    ("TS900001", "FP2838", "97646186000192", "POLIMAX PLASTICOS TECNICOS LTDA", 72001, "OC-SIN01", 18450.00, "boleto", "823", "boleto banco 823",
     "boleto por banco de cobrança novo, registrado no DDA pelo CNPJ do fornecedor e avisado antes pelo e-mail cadastrado"),
    ("TS900002", "FP1748", "60360748000127", "KRAFTBOX EMBALAGENS LTDA", 9801, "OC-SIN02", 6120.00, "boleto", "905", "boleto banco 905",
     "boleto por banco de cobrança novo, sem nenhum aviso do fornecedor"),
    ("TS900003", "FP3172", "14343478000129", "ECOPRINT SACOLAS PERSONALIZADAS LTDA", 66601, "OC-SIN03", 1840.00, "ted", None, "ted 146/2758/9837556-8",
     "NF 66601, mesmo valor e vencimento da NF 66602, mas são duas entregas diferentes"),
    ("TS900004", "FP3172", "14343478000129", "ECOPRINT SACOLAS PERSONALIZADAS LTDA", 66602, "OC-SIN04", 1840.00, "ted", None, "ted 146/2758/9837556-8",
     "NF 66602, par da anterior, entrega diferente"),
    ("TS900005", "FP1103", "34030017000103", "VITRINE PLATAFORMAS DE COMERCIO LTDA", 50120, "OC-35892", 2640.75, "pix", None, "pix 244c83bc-a736-4fff-afa2-6e12fdcf5242",
     "NF com reajuste de 5% em novembro; o e-mail do fornecedor diz que o reajuste vale a partir de dezembro"),
    ("TS900006", "FP4977", "49102883000130", "TALENTOS RH LTDA", 30551, "", 7800.00, "ted", None, "ted 612/9860/8504373-2",
     "NF de serviço avulso sem OC, de fornecedor sem contrato"),
]

titulos, agenda, nfs, dups, dda, ocs = [], [], [], [], [], []
for tid, fid, cnpj, razao, nf, oc, valor, forma, banco, destino, cenario in casos:
    ld = linha(banco, valor, DATA) if banco else ""
    cnpj_fmt = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    titulos.append({"titulo_id": tid, "fornecedor_id": fid, "numero_nf_digitado": str(nf), "oc_id": oc, "parcela": "1/1",
                    "valor": f"{valor:.2f}", "vencimento": DATA, "forma_pagamento": forma, "linha_digitavel": ld,
                    "cnpj_beneficiario_boleto": cnpj_fmt if banco else "", "origem_lancamento": "xml_portal",
                    "lancado_por": "usuario_08", "data_lancamento": "2026-10-30 10:00:00", "status": "agendado",
                    "banco_pagador": BANCO_PAGADOR, "lote_remessa": LOTE, "historico": f"NF {nf} parc 1/1 - {razao.split()[0].title()}"})
    agenda.append({"lote_remessa": LOTE, "banco_pagador": BANCO_PAGADOR, "data_prevista": DATA, "horario_fechamento": "10:00",
                   "titulo_id": tid, "fornecedor_id": fid, "valor": f"{valor:.2f}", "vencimento": DATA, "forma_pagamento": forma,
                   "destino_pagamento": destino})
    ch = chave(cnpj, nf)
    nfs.append({"chave_acesso": ch, "modelo": "55", "numero_nf": str(nf), "serie": "1", "cnpj_emitente": cnpj, "razao_social_emitente": razao,
                "data_emissao": "2026-10-29", "valor_total": f"{valor:.2f}", "oc_informada": oc, "informacoes_complementares": "Tributos aproximados conforme Lei 12.741/2012.",
                "data_recebimento_portal": "2026-10-29 18:00:00", "situacao_sefaz": "autorizada", "manifestacao_destinatario": "confirmação da operação"})
    dups.append({"chave_acesso": ch, "n_dup": "001", "vencimento": DATA, "valor": f"{valor:.2f}"})
    if banco:
        dda.append({"dda_id": f"DDASIN{tid[-3:]}", "data_registro": "2026-10-30 03:00:00", "cnpj_pagador": "41208533000221",
                    "banco_cobrador": banco, "nome_banco_cobrador": {"823": "Banco Capital Paulista", "905": "Nubra Pagamentos"}[banco],
                    "beneficiario": razao.title(), "cnpj_beneficiario": cnpj_fmt, "numero_documento": f"{nf}/1",
                    "nosso_numero": f"{nf:011d}", "valor": f"{valor:.2f}", "vencimento": DATA, "linha_digitavel": ld,
                    "situacao": "em aberto", "data_situacao": "2026-10-30"})
    if oc.startswith("OC-SIN"):
        desc = {"OC-SIN01": "Peças técnicas injetadas - lote 4", "OC-SIN02": "Caixas kraft 30x20 - 3.000 un",
                "OC-SIN03": "Sacolas kraft P - 2.000 un", "OC-SIN04": "Sacolas kraft G - 1.000 un"}[oc]
        ocs.append({"oc_id": oc, "cod_fornecedor_compras": "FCSIN", "cnpj_fornecedor": cnpj, "nome_fornecedor": razao[:20],
                    "data_emissao": "2026-10-10", "descricao": desc, "tipo": "pontual", "valor_total": f"{valor:.2f}", "valor_mensal": "",
                    "condicao_pagamento": "28 ddl", "centro_custo": "CC-2110", "aprovado_por": "cmenezes", "data_aprovacao": "2026-10-10",
                    "status": "aprovada"})

comunicacoes = [{
    "comunicacao_id": "EMSIN001", "data_hora": "2026-09-24 10:15:00", "canal": "email", "remetente": "contasareceber@polimax.com",
    "nome_remetente": "Juliana Freitas - Polimax", "destinatario": "contasapagar@gogroup.com.br", "assunto": "Novo banco de cobrança",
    "texto": "Prezados, a partir de outubro nossos boletos passam a ser registrados pelo Banco Capital Paulista (823). "
             "A conta para TED e a chave pix continuam as mesmas. Os boletos seguem com o CNPJ 97.646.186/0001-92. Juliana Freitas",
    "anexos": ""}]

for nome, linhas_ in [("contas_a_pagar", titulos), ("agenda_remessa", agenda), ("notas_fiscais", nfs), ("nf_duplicatas", dups),
                      ("dda_boletos", dda), ("pedidos_compra", ocs), ("comunicacoes_fornecedores", comunicacoes)]:
    escrever(nome, linhas_)
print(f"lote sintético {LOTE}: {len(titulos)} títulos")

"""Ferramentas de leitura dos sistemas (nomes do ferramentas.csv) usadas para montar o dossiê."""
from __future__ import annotations

import pandas as pd

from agente import fonte, regras


def _limpo(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None and not (isinstance(v, float) and pd.isna(v)) and v != ""}


def consultar_titulo(titulo_id: str) -> dict:
    t = fonte.titulos().loc[titulo_id]
    campos = ["titulo_id", "fornecedor_id", "numero_nf_digitado", "oc_id", "parcela", "valor", "vencimento",
              "forma_pagamento", "cnpj_beneficiario_boleto", "origem_lancamento", "lancado_por", "data_lancamento", "historico"]
    return _limpo({c: t[c] for c in campos})


def consultar_fornecedor(fornecedor_id: str) -> dict:
    f = fonte.fornecedores().loc[fornecedor_id]
    campos = ["razao_social", "cnpj", "categoria", "banco", "agencia", "conta", "chave_pix", "forma_pagamento_padrao",
              "email_cadastrado", "telefone_cadastrado", "data_cadastro", "data_ultima_alteracao", "ultima_alteracao_por"]
    return _limpo({c: f[c] for c in campos})


def consultar_historico_cadastro(fornecedor_id: str, dias: int = 60) -> list[dict]:
    a = fonte.alteracoes()
    a = a[(a.fornecedor_id == fornecedor_id) & (a.data_hora >= fonte.AGORA - pd.Timedelta(days=dias))]
    return [_limpo(r) for r in a[["data_hora", "campo", "valor_anterior", "valor_novo", "alterado_por", "origem",
                                  "confirmacao_registrada", "confirmacao_como"]].astype(str).to_dict("records")]


def consultar_nf(titulo_id: str) -> dict | None:
    loc = regras.localizar_nf(fonte.titulos().loc[titulo_id])
    if not loc:
        return None
    nf = loc["nf"]
    return _limpo({"numero_nf": nf["numero_nf"], "serie": nf["serie"], "cnpj_emitente": nf["cnpj_emitente"],
                   "razao_social_emitente": nf["razao_social_emitente"], "data_emissao": nf["data_emissao"],
                   "valor_total": nf["valor_total"], "oc_informada": nf["oc_informada"],
                   "duplicata": loc["duplicata"] and {k: loc["duplicata"][k] for k in ("n_dup", "vencimento", "valor")},
                   "n_duplicatas": loc["n_duplicatas"]})


def consultar_pedido_compra(oc_id) -> dict | None:
    pcs = fonte.pedidos_compra()
    if not isinstance(oc_id, str) or oc_id not in pcs.index:
        return None
    o = pcs.loc[oc_id]
    return _limpo({c: o[c] for c in ["oc_id", "descricao", "tipo", "valor_total", "valor_mensal", "condicao_pagamento",
                                      "status", "aprovado_por"]})


def consultar_boleto_dda(titulo_id: str) -> dict | None:
    t = fonte.titulos().loc[titulo_id]
    if t.forma_pagamento != "boleto":
        return None
    reg = regras._idx_dda_linha().get(t.linha_digitavel)
    if not reg:
        return {"registrado_no_dda": False, "banco_da_linha": fonte.banco_da_linha(t.linha_digitavel)}
    return _limpo({"registrado_no_dda": True, **{k: reg[k] for k in ("banco_cobrador", "beneficiario", "cnpj_beneficiario",
                                                                    "numero_documento", "valor", "vencimento", "situacao")}})


def listar_comunicacoes(fornecedor_id: str, limite: int = 6) -> list[dict]:
    c = regras.comunicacoes_do_fornecedor(fornecedor_id).sort_values("data_hora", ascending=False).head(limite)
    return [{"data_hora": r.data_hora, "remetente": r.remetente, "dominio_parecido_com_cadastro": bool(r.dominio_parecido),
             "assunto": r.assunto, "texto": str(r.texto)[:700]} for r in c.itertuples()]


def montar_dossie(titulo_id: str, alertas: list, lote_id: str) -> dict:
    t = fonte.titulos().loc[titulo_id]
    return {
        "lote": lote_id,
        "titulo": consultar_titulo(titulo_id),
        "alertas_da_triagem": [{k: v for k, v in a.dict().items() if k != "valor_corrigido" or v is not None} for a in alertas],
        "fornecedor": consultar_fornecedor(t.fornecedor_id),
        "alteracoes_cadastro_60d": consultar_historico_cadastro(t.fornecedor_id),
        "nota_fiscal": consultar_nf(titulo_id),
        "pedido_compra": consultar_pedido_compra(t.oc_id),
        "boleto_dda": consultar_boleto_dda(titulo_id),
        "comunicacoes_do_fornecedor": listar_comunicacoes(t.fornecedor_id),
        "lancador": regras.lancador(t),
    }

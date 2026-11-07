"""Camada única de leitura dos dados.

Hoje lê os CSVs fictícios de dados/pagamentos/. Com dados reais, cada função
troca por uma consulta ao sistema de origem (ver README, "Com dados reais").
"""
from __future__ import annotations

import os
import re
from functools import lru_cache
from pathlib import Path

import pandas as pd

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
DADOS = Path(os.environ.get("DADOS_DIR", RAIZ_PROJETO / "dados" / "pagamentos"))
AGORA = pd.Timestamp("2026-11-02 08:00:00")  # "agora" do ambiente fictício


SINTETICOS = RAIZ_PROJETO / "eval" / "sinteticos"


def _csv(nome: str) -> pd.DataFrame:
    df = pd.read_csv(DADOS / f"{nome}.csv", dtype=str, encoding="utf-8")
    extra = SINTETICOS / f"{nome}.csv"
    if os.environ.get("INCLUIR_SINTETICOS") == "1" and extra.exists():
        # casos fictícios criados por nós para o eval de julgamento (eval/sinteticos/gerar.py); nunca entram no lote real
        df = pd.concat([df, pd.read_csv(extra, dtype=str, encoding="utf-8")], ignore_index=True)
    return df


# ---------- normalizações (uma vez, aqui) ----------

def norm_nf(x) -> str:
    """'000967-1' -> '967'; '9671/1' -> '9671'. Vazio se não houver NF."""
    if not isinstance(x, str) or not x.strip():
        return ""
    return re.split(r"[-/]", x.strip())[0].lstrip("0")


def so_digitos(x) -> str:
    return re.sub(r"\D", "", x) if isinstance(x, str) else ""


def raiz_cnpj(x) -> str:
    return so_digitos(x)[:8]


def banco_da_linha(linha) -> str:
    return linha[:3] if isinstance(linha, str) and len(linha) >= 3 else ""


def dominio(email) -> str:
    return email.split("@")[-1].lower().strip() if isinstance(email, str) and "@" in email else ""


# ---------- tabelas ----------

@lru_cache(maxsize=None)
def fornecedores() -> pd.DataFrame:
    df = _csv("fornecedores")
    df["raiz"] = df.cnpj.map(raiz_cnpj)
    df["dominio"] = df.email_cadastrado.map(dominio)
    return df.set_index("fornecedor_id", drop=False)


@lru_cache(maxsize=None)
def titulos() -> pd.DataFrame:
    df = _csv("contas_a_pagar")
    df["valor"] = df.valor.astype(float)
    df["nf_norm"] = df.numero_nf_digitado.map(norm_nf)
    df["data_lancamento"] = pd.to_datetime(df.data_lancamento)
    return df.set_index("titulo_id", drop=False)


@lru_cache(maxsize=None)
def agenda() -> pd.DataFrame:
    df = _csv("agenda_remessa")
    df["valor"] = df.valor.astype(float)
    return df


def lote(lote_id: str) -> pd.DataFrame:
    return agenda()[agenda().lote_remessa == lote_id]


def lotes() -> pd.DataFrame:
    return (agenda().groupby(["lote_remessa", "banco_pagador", "data_prevista", "horario_fechamento"])
            .valor.agg(["count", "sum"]).reset_index())


@lru_cache(maxsize=None)
def notas() -> pd.DataFrame:
    df = _csv("notas_fiscais")
    df["valor_total"] = df.valor_total.astype(float)
    df["raiz"] = df.cnpj_emitente.str[:8]
    df["nf_norm"] = df.numero_nf.map(norm_nf)
    return df


@lru_cache(maxsize=None)
def duplicatas() -> pd.DataFrame:
    df = _csv("nf_duplicatas")
    df["valor"] = df.valor.astype(float)
    return df


@lru_cache(maxsize=None)
def alteracoes() -> pd.DataFrame:
    df = _csv("alteracoes_cadastro")
    df["data_hora"] = pd.to_datetime(df.data_hora)
    return df


@lru_cache(maxsize=None)
def dda() -> pd.DataFrame:
    df = _csv("dda_boletos")
    df["valor"] = df.valor.astype(float)
    df["raiz"] = df.cnpj_beneficiario.map(raiz_cnpj)
    return df


@lru_cache(maxsize=None)
def pedidos_compra() -> pd.DataFrame:
    df = _csv("pedidos_compra")
    df["valor_total"] = df.valor_total.astype(float)
    return df.set_index("oc_id", drop=False)


@lru_cache(maxsize=None)
def comunicacoes() -> pd.DataFrame:
    df = _csv("comunicacoes_fornecedores")
    df["dominio"] = df.remetente.map(dominio)
    return df


@lru_cache(maxsize=None)
def pagamentos_avulsos() -> pd.DataFrame:
    """Débitos feitos fora do lote nos dois bancos, num formato só: data, banco, descricao, valor (positivo)."""
    m = _csv("extrato_banco_meridiano")
    m = m[m.tipo == "PAGTO AVULSO"].assign(valor=lambda d: -d.valor.astype(float), data=lambda d: pd.to_datetime(d.data),
                                            banco="Banco Meridiano")[["data", "banco", "descricao", "valor"]]
    lit = pd.read_csv(DADOS / "extrato_banco_litoral.csv", dtype=str, sep=";", encoding="utf-8")
    lit = lit[lit["Histórico"].str.match(r"(PIX ENV|TED ENV|PAG BOL)", na=False)]
    lit = pd.DataFrame({"data": pd.to_datetime(lit.Data, format="%d/%m/%Y"), "banco": "Banco Litoral",
                        "descricao": lit["Histórico"],
                        "valor": -lit["Valor (R$)"].str.replace(".", "", regex=False).str.replace(",", ".").astype(float)})
    # o Litoral não marca o avulso: é avulso o débito que não corresponde a título pago por lote no mesmo dia e valor
    t = titulos()
    pagos = t[(t.status == "pago") & (t.banco_pagador == "Banco Litoral") & t.lote_remessa.notna()]
    chaves = set(zip(pd.to_datetime(pagos.data_pagamento), pagos.valor.round(2)))
    lit = lit[[(d, round(v, 2)) not in chaves for d, v in zip(lit.data, lit.valor)]]
    return pd.concat([m, lit], ignore_index=True)


def sem_acento(s: str) -> str:
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn").upper()


@lru_cache(maxsize=None)
def usuarios() -> pd.DataFrame:
    return _csv("usuarios_sistema").set_index("login", drop=False)

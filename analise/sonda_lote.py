"""Sonda rápida: os problemas de Pagamentos são detectáveis no lote agendado?"""
import sys, re
import pandas as pd

base = sys.argv[1]
r = lambda f, **k: pd.read_csv(f"{base}/{f}.csv", dtype=str, **k)
ag = r("agenda_remessa"); cp = r("contas_a_pagar"); fo = r("fornecedores")
alt = r("alteracoes_cadastro"); nf = r("notas_fiscais"); dup = r("nf_duplicatas")
us = r("usuarios_sistema"); com = r("comunicacoes_fornecedores")
for d in (ag, cp, dup, nf):
    for c in ("valor", "valor_total"):
        if c in d: d[c] = d[c].astype(float)

print("agenda:", len(ag), "titulos | R$ %.0f" % ag.valor.sum(), "| lotes:", ag.lote_remessa.nunique())
print(ag.groupby("lote_remessa").valor.agg(["count", "sum"]).head(12).round(0))

a = ag.merge(cp, on="titulo_id", suffixes=("", "_cp"))
print("\nstatus dos titulos agendados:", a.status.value_counts().to_dict())
print("origem:", a.origem_lancamento.value_counts().to_dict())

# 1) duplicidade: mesmo fornecedor + NF normalizada + valor
def norm_nf(x):
    if not isinstance(x, str): return ""
    x = re.split(r"[-/]", x.strip())[0]
    return x.lstrip("0")
cp["nf_norm"] = cp.numero_nf_digitado.map(norm_nf)
viva = cp[~cp.status.isin(["cancelado"])]
k = viva.groupby(["fornecedor_id", "nf_norm", "parcela"]).titulo_id.transform("count")
dups = viva[(k > 1) & (viva.nf_norm != "")]
dag = dups[dups.titulo_id.isin(ag.titulo_id)]
print("\n[duplicidade] grupos fornecedor+NF+parcela com >1 titulo vivo:", dups.groupby(["fornecedor_id","nf_norm","parcela"]).ngroups,
      "| desses, titulos no lote agendado:", len(dag), "R$ %.0f" % dag.valor.sum())

# 2) destino do pagamento diferente do cadastro
fo["conta_cad"] = fo.banco + "/" + fo.agencia + "/" + fo.conta
a2 = a.merge(fo[["fornecedor_id", "conta_cad", "chave_pix", "data_ultima_alteracao"]], on="fornecedor_id", how="left")
ted = a2[a2.forma_pagamento.str.contains("ted", na=False)]
ted_dif = ted[ted.destino_pagamento.str.replace("ted ", "", regex=False) != ted.conta_cad]
print("[destino] TED no lote com conta != cadastro atual:", len(ted_dif), "R$ %.0f" % ted_dif.valor.sum())

# 3) troca bancaria recente sem confirmacao
banc = alt[alt.campo.isin(["banco", "agencia", "conta", "chave_pix", "dados_bancarios"]) | alt.campo.str.contains("banc|conta|pix", na=False)]
print("[cadastro] alteracoes:", alt.campo.value_counts().to_dict())
semconf = banc[banc.confirmacao_registrada != "sim"]
print("  alteracoes bancarias sem confirmacao:", len(semconf), "| fornecedores no lote:",
      ag.fornecedor_id.isin(semconf.fornecedor_id).sum(), "titulos, R$ %.0f" % ag[ag.fornecedor_id.isin(semconf.fornecedor_id)].valor.sum())
print(semconf[["data_hora","fornecedor_id","campo","origem","alterado_por","confirmacao_como"]].tail(8).to_string())

# 4) valor x duplicata da NF (zero a mais / errado)
nf["nnum"] = nf.numero_nf.str.lstrip("0")
nf["raiz"] = nf.cnpj_emitente.str[:8]
fo["raiz"] = fo.cnpj.str.replace(r"\D", "", regex=True).str[:8]
x = a.merge(fo[["fornecedor_id","raiz"]], on="fornecedor_id").assign(nf_norm=lambda d: d.numero_nf_digitado.map(norm_nf))
x = x.merge(nf[["chave_acesso","nnum","raiz","valor_total"]], left_on=["raiz","nf_norm"], right_on=["raiz","nnum"], how="left")
print("\n[NF] titulos do lote sem NF encontrada no portal:", x.chave_acesso.isna().sum(), "de", len(x))
x["par"] = x.parcela.str.split("/").str[0].str.zfill(3)
x = x.merge(dup, left_on=["chave_acesso","par"], right_on=["chave_acesso","n_dup"], how="left", suffixes=("","_dup"))
xm = x[x.valor_dup.notna()]
diff = xm[(xm.valor - xm.valor_dup).abs() > 0.10]
print("[valor] titulos com valor != duplicata (>R$0,10):", len(diff), "de", len(xm))
diff = diff.assign(razao=(diff.valor / diff.valor_dup).round(2))
print(diff[["titulo_id","fornecedor_id","valor","valor_dup","razao","lancado_por"]].sort_values("razao").to_string(max_rows=20))

# 5) lancador novato
us["adm"] = pd.to_datetime(us.data_admissao)
print("\n[usuarios] lancadores dos titulos agendados:", a.lancado_por.value_counts().head(8).to_dict())
print(us[["login","cargo","perfil","alcada_rs","data_admissao","status"]].to_string())

# 6) comunicacoes pedindo troca de conta
troca = com[com.texto.str.contains("nova conta|alteração bancária|troca de conta|novos dados bancários|mudamos de banco|conta atualizada", case=False, na=False)]
print("\n[comunicacoes] canais:", com.canal.value_counts().to_dict(), "| pedindo troca de conta:", len(troca))
print(troca[["data_hora","canal","remetente","assunto"]].tail(10).to_string())

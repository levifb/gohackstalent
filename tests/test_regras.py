import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agente import fonte, regras  # noqa: E402
from agente.regras import Alerta  # noqa: E402


def test_norm_nf():
    assert fonte.norm_nf("000967-1") == "967"
    assert fonte.norm_nf("9671/1") == "9671"
    assert fonte.norm_nf("") == "" and fonte.norm_nf(None) == ""


def test_raiz_cnpj():
    assert fonte.raiz_cnpj("85.779.751/0001-00") == "85779751"


def _decisao(acao, vc=None, desc=()):
    return {"acao": acao, "valor_corrigido": vc, "acionar": [], "alertas_descartados": list(desc)}


def test_trava_impede_liberar_com_bloqueio():
    al = [Alerta("TROCA_BANCARIA", "bloqueio", "x", "y", ["PS01"])]
    final, motivo = regras.travar(_decisao("liberar"), al, "TP431502")
    assert motivo and final["acao"] != "liberar"


def test_trava_nao_deixa_descartar_alerta_duro():
    al = [Alerta("TROCA_BANCARIA", "bloqueio", "x", "y", ["PS01"])]
    final, motivo = regras.travar(_decisao("liberar", desc=["TROCA_BANCARIA"]), al, "TP431502")
    assert motivo and final["acao"] != "liberar"


def test_correcao_resolve_virgula_dentro_da_alcada():
    al = [Alerta("VIRGULA_DESLOCADA", "bloqueio", "x", "y", [], valor_corrigido=2406.36)]
    final, motivo = regras.travar(_decisao("corrigir_lancamento", 2406.36), al, "TP431634")
    assert motivo is None and final["acao"] == "corrigir_lancamento"


def test_correcao_acima_da_alcada_e_travada():
    al = [Alerta("VIRGULA_DESLOCADA", "bloqueio", "x", "y", ["PS01"], valor_corrigido=9087.38)]
    final, motivo = regras.travar(_decisao("corrigir_lancamento", 9087.38), al, "TP431775")
    assert motivo and final["acao"] != "corrigir_lancamento"


def test_dominio_de_outro_fornecedor_nao_e_parecido():
    c = regras.comunicacoes_do_fornecedor("FP6799")  # Cartonar x Cartonart (outro fornecedor legítimo)
    assert not c.dominio_parecido.any()


def test_golpe_embalarte_detectado():
    lt = fonte.lote("RM20261103-MER")
    codigos = {a.codigo for a in regras.triagem("TP431502", lt)}
    assert {"TROCA_BANCARIA", "DOMINIO_PARECIDO"} <= codigos

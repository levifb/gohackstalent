"""Imagens com fundo transparente para os slides 5 e 8 (deck v2).

- grade_192: os 192 títulos do lote RM20261103-MER na mesma ordem e cores da aba "A história"
  (verde liberado, rosa barrado, azul aguarda a diretora), sem o cartão azul do site.
- celular_tg: moldura de celular com o print real tg_politica.png, sem fundo e sem os pontinhos.
uso: .venv/Scripts/python.exe -X utf8 apresentacao/gerar/imagens_v3.py
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw

RAIZ = Path(__file__).resolve().parents[2]
SAI = RAIZ / "web" / "public" / "capturas"
PAGAM = {"liberar", "corrigir_lancamento"}
VERDE, ROSA, CIANO = (63, 208, 138, 255), (230, 23, 130, 255), (61, 191, 239, 255)


def grade():
    d = json.loads((RAIZ / "web/public/resultado.json").read_text(encoding="utf8"))
    itens = next(l for l in d["lotes"] if l["lote"] == "RM20261103-MER")["itens"]
    cont = {}
    def cor(i):
        if not i["etapas"].get("analise"):
            return VERDE
        a = i["decisao"]["acao"]
        return VERDE if a in PAGAM else CIANO if a == "solicitar_aprovacao" else ROSA
    cols, lado, gap, s = 24, 60, 12, 4  # desenha em 4x e reduz (borda lisa)
    rows = (len(itens) + cols - 1) // cols
    W, H = cols * lado + (cols - 1) * gap, rows * lado + (rows - 1) * gap
    im = Image.new("RGBA", (W * s, H * s), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    for k, i in enumerate(itens):
        c = cor(i); cont[c] = cont.get(c, 0) + 1
        x, y = (k % cols) * (lado + gap), (k // cols) * (lado + gap)
        dr.rounded_rectangle([x * s, y * s, (x + lado) * s, (y + lado) * s], radius=12 * s, fill=c)
    im = im.resize((W, H), Image.LANCZOS)
    im.save(SAI / "slide5_grade_v3.png")
    print("grade", im.size, {"verde": cont.get(VERDE), "rosa": cont.get(ROSA), "azul": cont.get(CIANO)})


def celular():
    shot = Image.open(RAIZ / "apresentacao/capturas/tg_politica.png").convert("RGBA")
    s = 2
    tela_w = 760
    shot = shot.resize((tela_w, round(shot.height * tela_w / shot.width)), Image.LANCZOS)
    tela_h = shot.height + 150
    borda, raio = 26, 92
    W, H = tela_w + 2 * borda, tela_h + 2 * borda
    sombra = 26
    im = Image.new("RGBA", ((W + sombra) * s, (H + sombra) * s), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    dr.rounded_rectangle([sombra * s, sombra * s, (W + sombra) * s, (H + sombra) * s], radius=raio * s, fill=(20, 40, 75, 60))
    dr.rounded_rectangle([0, 0, W * s, H * s], radius=raio * s, fill=(17, 17, 17, 255))
    dr.rounded_rectangle([borda * s, borda * s, (W - borda) * s, (H - borda) * s], radius=(raio - borda) * s, fill=(15, 27, 45, 255))
    dr.rounded_rectangle([(W / 2 - 70) * s, (borda + 22) * s, (W / 2 + 70) * s, (borda + 48) * s], radius=13 * s, fill=(17, 17, 17, 255))
    im = im.resize((W + sombra, H + sombra), Image.LANCZOS)
    im.alpha_composite(shot, (borda, borda + 90))
    im = im.rotate(-3, resample=Image.BICUBIC, expand=True)
    im = im.crop(im.getbbox())
    im.save(SAI / "slide8_celular_v3.png")
    print("celular", im.size, round(im.width / im.height, 3))


grade()
celular()

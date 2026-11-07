"""Narração do vídeo de 2 min pelo VoiceStudio local (motor OmniVoice), no lugar do edge-tts.

Gera a{k}_{cena}.wav na pasta de trabalho com o mesmo texto de video_2min.CENAS; depois
video_2min.py reaproveita esses arquivos (não chama o edge-tts quando a fala já existe).
uso: python apresentacao/gerar/narrar_voicestudio.py <pasta_de_trabalho> [--so 0] [--instruct "male, middle-aged, low pitch"]
"""
import argparse
import sys
import time
import urllib.request
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from video_2min import CENAS  # noqa: E402

API = "http://localhost:3900/generate"
# grafia fonética só para a voz (a legenda continua com o texto original)
PRONUNCIA = {"Gogroup": "Gôu-grúp", "GoHacks Talent": "Gôu-Réks Télent", "IA": "I-A"}


def foneticas(texto):
    for a, b in PRONUNCIA.items():
        texto = texto.replace(a, b)
    return texto


def multipart(campos):
    b = uuid.uuid4().hex
    corpo = b"".join(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in campos.items())
    return corpo + f"--{b}--\r\n".encode(), f"multipart/form-data; boundary={b}"


def gerar(texto, destino, instruct, seed, speed):
    corpo, ct = multipart({"text": foneticas(texto), "language": "pt", "instruct": instruct, "seed": seed, "speed": speed})
    req = urllib.request.Request(API, data=corpo, headers={"Content-Type": ct}, method="POST")
    with urllib.request.urlopen(req, timeout=900) as r:
        dados, tipo = r.read(), r.headers.get("Content-Type", "")
    if not dados.startswith(b"RIFF"):
        raise RuntimeError(f"resposta não é WAV ({tipo}): {dados[:300]!r}")
    destino.write_bytes(dados)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pasta")
    ap.add_argument("--so", type=int, default=None, help="gera só a cena de índice N (amostra)")
    ap.add_argument("--instruct", default="male, middle-aged, low pitch")
    ap.add_argument("--seed", default="7")
    ap.add_argument("--speed", default="1.1")
    ap.add_argument("--sufixo", default="")
    a = ap.parse_args()
    pasta = Path(a.pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    for k, (nome, txt) in enumerate(CENAS):
        if a.so is not None and k != a.so:
            continue
        t0 = time.time()
        gerar(txt, pasta / f"a{k:02d}_{nome}{a.sufixo}.wav", a.instruct, a.seed, a.speed)
        print(f"cena {k} {nome}: {time.time() - t0:.0f} s de processamento", flush=True)


if __name__ == "__main__":
    main()

"""Grava o vídeo de 2 min (plano B da demo) sozinho: site publicado + narração neural.

1. Narração de cada cena com a voz pt-BR-AntonioNeural (edge-tts).
2. Gravação da aba "A história" de https://guarda-do-lote.vercel.app com o Edge controlado
   pelo Playwright (cliques reais: simulação do lote, trilha de um caso comum e do golpe da Embalarte).
3. Montagem com ffmpeg: vídeo + narração + legendas.

Números da narração: web/public/resultado.json (lote RM20261103-MER) e web/public/eval.json.
uso (ambiente separado com edge-tts, imageio-ffmpeg e playwright):
  python apresentacao/gerar/video_2min.py <pasta_de_trabalho> <saida.mp4>
"""
import asyncio
import re
import subprocess
import sys
import time
from pathlib import Path

import edge_tts
import imageio_ffmpeg
from playwright.sync_api import sync_playwright

URL = "https://guarda-do-lote.vercel.app/"
VOZ = "pt-BR-AntonioNeural"
FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H = 1280, 720

CENAS = [
    ("hero", "Este é o Guarda do Lote, um agente de IA que confere cada título do lote de remessa antes de o arquivo ir para o banco. "
             "Ele foi feito para o Marcos Teles, tesoureiro do Gogroup. Os dados são fictícios, do GoHacks Talent."),
    ("dor", "Hoje, às dez horas, o Marcos assina um lote de 2 milhões e 240 mil reais sem abrir título por título. "
            "Nos 876 títulos da semana, estavam escondidos um golpe, pagamentos em dobro, vírgulas no lugar errado e títulos no fornecedor errado."),
    ("simulacao", "Este é o lote das dez horas de 3 de novembro, com 192 títulos. As regras da política, em código, conferem todos. "
                  "Só os 13 com alerta vão para o modelo, que lê o dossiê e propõe a ação. No fim, 181 se resolvem sozinhos, e 11 vão para uma pessoa."),
    ("comum", "Um caso comum: Laboratório Vitallis. Nota, duplicata, cadastro e boleto batem em todos os sistemas. "
              "As regras liberam, e o título sai no lote sem chamar o modelo."),
    ("risco", "Agora, um caso de risco: Embalarte. A conta foi trocada por um e-mail de um domínio com um t a mais, que ainda avisa: obs. para o robô de pagamentos. "
              "O modelo trata esse texto como dado, não como ordem. Bloqueia o título e aciona a Renata, coordenadora, e o jurídico."),
    ("telegram", "A fila chega no Telegram do time, com o motivo, a pessoa e botões. "
                 "Se alguém tenta liberar um título com suspeita de golpe, o bot aplica a política: só sai com aprovação dupla."),
    ("impacto", "Nos 30 casos do gabarito, assinar sem conferir custaria 530 mil reais. Com o Guarda do Lote, zero."),
    ("prova", "E medimos contra um gabarito revisado: o agente acerta 30 de 30 títulos, contra 29 das regras sozinhas. "
              "Nos golpes reescritos com outras palavras, a IA acerta 12 de 12; as palavras-chave, só 1. E o dinheiro nunca sai por decisão só do modelo."),
    ("fim", "Na segunda-feira, duas semanas em modo sombra no lote real, depois autonomia por degraus. Guarda do Lote: o Marcos olha 11 de 192."),
]
FOLGA = 0.45  # segundos de respiro depois de cada fala


def duracao(arq):
    err = subprocess.run([FF, "-i", str(arq)], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


async def narrar(pasta):
    for k, (nome, txt) in enumerate(CENAS):
        if list(pasta.glob(f"a{k:02d}_{nome}.*")):  # narração já gerada (ex.: VoiceStudio): reaproveita
            continue
        await edge_tts.Communicate(txt, VOZ, rate="+13%").save(str(pasta / f"a{k:02d}_{nome}.mp3"))


def rolar(page, css, texto=None, ms=1400, centro=True, margem=16):
    """Rola até o elemento (css, opcionalmente com o texto) sem cortar o topo dele.

    Cabe na janela abaixo da barra do site: fica centralizado. Não cabe: o topo fica logo
    abaixo da barra, com uma margem. Assim a etiqueta e o título da seção nunca somem.
    """
    page.evaluate(
        """([css, t, ms, centro, margem]) => {
            const el = [...document.querySelectorAll(css)].find(e => !t || e.textContent.includes(t));
            if (!el) return;
            const nav = document.querySelector('.nav')?.offsetHeight ?? 0;
            const livre = window.innerHeight - nav;
            const r = el.getBoundingClientRect();
            const folga = centro && r.height + 2 * margem <= livre ? (livre - r.height) / 2 : margem;
            const alvo = Math.max(0, r.top + window.scrollY - nav - folga);
            const ini = window.scrollY, t0 = performance.now();
            const passo = (agora) => {
                const p = Math.min(1, (agora - t0) / ms), e = p < .5 ? 2*p*p : 1 - Math.pow(-2*p + 2, 2) / 2;
                window.scrollTo(0, ini + (alvo - ini) * e);
                if (p < 1) requestAnimationFrame(passo);
            };
            requestAnimationFrame(passo);
        }""",
        [css, texto, ms, centro, margem],
    )


def rolar_modal(page, ms=2500):
    page.evaluate(
        """(ms) => {
            const m = document.querySelector('.modal'); if (!m) return;
            const fim = m.scrollHeight - m.clientHeight, t0 = performance.now();
            const passo = (agora) => { const p = Math.min(1, (agora - t0) / ms); m.scrollTop = fim * p * 0.6; if (p < 1) requestAnimationFrame(passo); };
            requestAnimationFrame(passo);
        }""",
        ms,
    )


def gravar(pasta, durs):
    with sync_playwright() as p:
        nav = p.chromium.launch(channel="msedge", headless=True)
        ctx = nav.new_context(viewport={"width": W, "height": H}, record_video_dir=str(pasta), record_video_size={"width": W, "height": H})
        t_criado = time.monotonic()
        page = ctx.new_page()
        page.goto(URL, wait_until="networkidle")
        page.wait_for_selector(".hero h1")
        page.wait_for_timeout(1200)
        t_pronto = time.monotonic()
        marcas = []

        def cena(k):
            marcas.append(time.monotonic() - t_pronto)
            return time.monotonic() + durs[k]

        def ate(fim):
            resta = fim - time.monotonic()
            if resta > 0:
                page.wait_for_timeout(int(resta * 1000))

        fim = cena(0); ate(fim)
        S = ".h-secao"
        fim = cena(1); rolar(page, S, "O lote é assinado"); page.wait_for_timeout(int(durs[1] * 450))
        rolar(page, ".sub-h", "O que estava escondido", 1200, centro=False, margem=24); ate(fim)
        fim = cena(2); rolar(page, S, "O agente confere os"); page.wait_for_timeout(2600)
        rolar(page, ".sim", ms=1200); ate(fim)
        fim = cena(3); page.click('button[aria-label^="TP426904"]'); page.wait_for_timeout(1800); rolar_modal(page, 3000); ate(fim - 0.3)
        page.click(".modal .fechar")
        fim = cena(4); page.click('button[aria-label^="TP431502"]'); page.wait_for_timeout(2500); rolar_modal(page, 5000); ate(fim - 0.3)
        page.click(".modal .fechar")
        fim = cena(5); rolar(page, S, "A fila chega no celular"); ate(fim)
        fim = cena(6); rolar(page, S, "Do mesmo lote, dois resultados"); page.wait_for_timeout(1700)
        page.click("button:has-text(\"Assinar sem conferir\")"); page.wait_for_timeout(int(durs[6] * 550)); page.click("button:has-text(\"Com o Guarda do Lote\")"); ate(fim)
        fim = cena(7); rolar(page, S, "Medido contra gabarito"); ate(fim)
        fim = cena(8); rolar(page, S, "Duas semanas em modo sombra"); ate(fim + 0.8)
        corte = t_pronto - t_criado
        video = page.video.path()
        ctx.close()
        nav.close()
    return Path(video), corte, marcas


def srt_tempo(s):
    ms = int(round(s * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def legendas(pasta, marcas, falas):
    linhas, n = [], 1
    for (nome, txt), ini, dur in zip(CENAS, marcas, falas):
        frases = [f for f in re.split(r"(?<!obs\.)(?<=[.:;])\s+", txt) if f]
        tot = sum(len(f) for f in frases)
        t = ini
        for f in frases:
            d = dur * len(f) / tot
            linhas.append(f"{n}\n{srt_tempo(t)} --> {srt_tempo(t + d)}\n{f}\n")
            n += 1
            t += d
    (pasta / "legendas.srt").write_text("\n".join(linhas), encoding="utf8")


def main():
    pasta, saida = Path(sys.argv[1]), Path(sys.argv[2])
    pasta.mkdir(parents=True, exist_ok=True)
    asyncio.run(narrar(pasta))
    audios = sorted(a for a in pasta.glob("a*_*.*") if a.suffix in (".mp3", ".wav"))
    falas = [duracao(a) for a in audios]
    durs = [f + FOLGA for f in falas]
    print("cenas (s):", [round(d, 1) for d in durs], "total", round(sum(durs), 1))
    video, corte, marcas = gravar(pasta, durs)
    print("vídeo bruto", video, "corte inicial", round(corte, 2), "marcas", [round(m, 1) for m in marcas])
    # trilha de áudio: cada fala começa na marca real da cena
    entradas, filtros = [], []
    for k, (a, m) in enumerate(zip(audios, marcas)):
        entradas += ["-i", str(a)]
        filtros.append(f"[{k}]adelay={int(m * 1000)}|{int(m * 1000)}[a{k}]")
    mix = "".join(f"[a{k}]" for k in range(len(audios)))
    filtros.append(f"{mix}amix=inputs={len(audios)}:normalize=0[sai]")
    subprocess.run([FF, "-y", *entradas, "-filter_complex", ";".join(filtros), "-map", "[sai]", str(pasta / "narracao.wav")], check=True, capture_output=True)
    legendas(pasta, marcas, falas)
    srt = str(pasta / "legendas.srt").replace("\\", "/").replace(":", "\\:")
    estilo = "FontName=Segoe UI,FontSize=17,PrimaryColour=&H00FFFFFF,BackColour=&H99000000,BorderStyle=3,Outline=6,Shadow=0,MarginV=26"
    base = [FF, "-y", "-ss", f"{corte:.2f}", "-i", str(video), "-i", str(pasta / "narracao.wav")]
    fim_ = ["-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", str(saida)]
    r = subprocess.run(base + ["-vf", f"subtitles='{srt}':force_style='{estilo}'"] + fim_, capture_output=True, text=True)
    if r.returncode != 0:
        print("legenda queimada falhou; gerando sem legenda:", r.stderr[-400:])
        subprocess.run(base + fim_, check=True, capture_output=True)
    print("pronto:", saida, round(duracao(saida), 1), "s")


if __name__ == "__main__":
    main()

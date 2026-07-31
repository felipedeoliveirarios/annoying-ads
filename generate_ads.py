#!/usr/bin/env python3
"""Gera anúncios falsos estilo "pop-up de vírus" como imagens PNG em ads/.

Uso:  uv run python generate_ads.py
Edite ADS/PALETTES abaixo e rode de novo para trocar o conjunto.
"""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# (título, corpo, texto do botão)
ADS = [
    ("PARABÉNS!", "Você é o VISITANTE de número 1.000.000!", "RESGATAR PRÊMIO"),
    ("!!! ALERTA DE VÍRUS !!!", "Seu computador está INFECTADO com 99 ameaças.", "LIMPAR AGORA"),
    ("GANHE DINHEIRO EM CASA", "R$ 5.000 por dia trabalhando 2h pelo celular!", "QUERO GANHAR"),
    ("VOCÊ GANHOU UM iPhone 15", "Confirme seus dados para receber a entrega.", "RECEBER AGORA"),
    ("SISTEMA CORROMPIDO", "Ligue para o suporte oficial: 0800-GOLPE-JA", "LIGAR JÁ"),
    ("OFERTA RELÂMPAGO", "90% DE DESCONTO só nos próximos 2 minutos!", "COMPRAR"),
    ("PRÊMIO EXCLUSIVO", "Gire a roleta da sorte e ganhe na hora.", "GIRAR AGORA"),
    ("ATENÇÃO NECESSÁRIA", "Detectamos 47 problemas graves no seu PC.", "CORRIGIR TUDO"),
    ("CARTÃO PRÉ-APROVADO", "Limite de R$ 50.000 liberado no seu nome!", "ATIVAR CARTÃO"),
    ("TRAVE SEU COMPUTADOR", "Dica de segurança: bloqueie a estação ao sair.", "OK, ENTENDI"),
]

# (fundo, título, corpo, botão-fundo, botão-texto)
PALETTES = [
    ("#ff0055", "#ffee00", "#ffffff", "#ffee00", "#ff0055"),
    ("#0a0a2a", "#ff3b3b", "#e0e0ff", "#ff3b3b", "#ffffff"),
    ("#12b886", "#052e1a", "#eafff5", "#ffd43b", "#052e1a"),
    ("#1971c2", "#ffe066", "#e7f5ff", "#ffe066", "#1971c2"),
    ("#111111", "#39ff14", "#c8ffc8", "#39ff14", "#111111"),
    ("#f76707", "#ffffff", "#fff4e6", "#ffffff", "#f76707"),
    ("#ae3ec9", "#ffe8ff", "#f3d9fa", "#ffd43b", "#5f1466"),
    ("#e03131", "#fff5f5", "#ffe3e3", "#ffe066", "#c92a2a"),
    ("#2b8a3e", "#fffbe6", "#ebfbee", "#ffd43b", "#1b4332"),
    ("#f783ac", "#3d0022", "#fff0f6", "#3d0022", "#ffd6e7"),
]


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def centered(draw, lines, font, cx, top, fill, gap=6, stroke=0, stroke_fill=None):
    y = top
    for ln in lines:
        bbox = draw.textbbox((0, 0), ln, font=font, stroke_width=stroke)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((cx - w / 2, y), ln, font=font, fill=fill,
                  stroke_width=stroke, stroke_fill=stroke_fill)
        y += h + gap
    return y


def make_ad(path, title, body, button, pal):
    bg, c_title, c_body, c_btn, c_btn_txt = pal
    W = random.randint(460, 520)
    H = random.randint(300, 350)
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)

    f_tag = ImageFont.truetype(FONT_BOLD, 15)
    f_title = ImageFont.truetype(FONT_BOLD, 34)
    f_body = ImageFont.truetype(FONT_REG, 20)
    f_btn = ImageFont.truetype(FONT_BOLD, 22)

    # bordas berrantes
    d.rectangle([0, 0, W - 1, H - 1], outline=c_btn, width=6)
    d.rectangle([6, 6, W - 7, H - 7], outline=c_title, width=2)

    # banner superior
    d.rectangle([7, 7, W - 8, 40], fill=c_btn)
    centered(d, ["★  ANÚNCIO  ★"], f_tag, W / 2, 14, c_btn_txt)

    # X falso no canto
    d.rectangle([W - 34, 10, W - 12, 32], fill="#cc0000")
    centered(d, ["✕"], f_tag, W - 23, 12, "#ffffff")

    # título (com contorno pra dar "punch")
    tlines = wrap(d, title, f_title, W - 50)
    y = centered(d, tlines, f_title, W / 2, 58, c_title, gap=4,
                 stroke=2, stroke_fill="#000000")

    # corpo
    blines = wrap(d, body, f_body, W - 50)
    centered(d, blines, f_body, W / 2, y + 10, c_body, gap=4)

    # botão
    bw = int(draw_w := d.textlength(button, font=f_btn)) + 48
    bh = 50
    bx0, by0 = (W - bw) / 2, H - bh - 22
    d.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=10,
                        fill=c_btn, outline="#000000", width=2)
    centered(d, [button], f_btn, W / 2, by0 + 12, c_btn_txt)

    img.save(path)
    return W, H


def main():
    ads = Path("ads")
    ads.mkdir(exist_ok=True)
    for i, (ad, pal) in enumerate(zip(ADS, PALETTES), start=1):
        p = ads / f"fake-ad-{i:02d}.png"
        w, h = make_ad(p, *ad, pal)
        print(f"OK  {p.name}  {w}x{h}")
    print(f"\n{len(ADS)} anúncios gerados em ads/")


if __name__ == "__main__":
    main()

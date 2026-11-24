#!/usr/bin/env python3
"""Render a 1024x1024 newspaper infographic for Monday 23 November 2026.

Run: python3 draw.py  -> writes entry.png next to this file.
Only Pillow is required. Everything is drawn from scratch with PIL.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

CANVAS = 1024
MARGIN = 36

PAPER = (247, 242, 231)
INK = (26, 26, 24)
FAINT = (105, 98, 88)
RULE = (60, 56, 50)
ACCENT = (146, 32, 24)
PANEL_BG = (255, 253, 247)
PANEL_EDGE = (198, 190, 174)
TAG_BG = (26, 26, 24)
TAG_FG = (247, 242, 231)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def text_block(draw, xy, text, fnt, fill, max_width, leading):
    """Draw wrapped text starting at xy; return the y just below the block."""
    x, y = xy
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, y, x0, x1, width=1, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_masthead(draw):
    title = "THE DAILY LEDGER"
    tf = font(SERIF_BOLD, 78)
    tw = draw.textlength(title, font=tf)
    draw.text(((CANVAS - tw) / 2, 26), title, font=tf, fill=INK)
    hline(draw, 118, MARGIN, CANVAS - MARGIN, width=3)
    hline(draw, 124, MARGIN, CANVAS - MARGIN, width=1)
    meta = "MONDAY, 23 NOVEMBER 2026  •  SIX STORIES THAT SHAPED THE DAY  •  PRICE: FREE"
    mf = font(SANS_BOLD, 15)
    mw = draw.textlength(meta, font=mf)
    draw.text(((CANVAS - mw) / 2, 134), meta, font=mf, fill=FAINT)
    hline(draw, 162, MARGIN, CANVAS - MARGIN, width=2)


def draw_lead(draw, x, y, w, h):
    """The lead story: a wide panel with a red kicker and a big headline."""
    draw.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=PANEL_EDGE, width=2)
    draw.rectangle([x, y, x + w, y + 8], fill=ACCENT)
    kf = font(SANS_BOLD, 17)
    draw.text((x + 22, y + 22), "LEAD  •  CLIMATE  •  ANTALYA", font=kf, fill=ACCENT)
    hf = font(SERIF_BOLD, 40)
    y = text_block(
        draw, (x + 22, y + 52),
        "COP31 climate talks in Antalya end with no deal",
        hf, INK, w - 44, 48,
    )
    bf = font(SERIF, 21)
    text_block(
        draw, (x + 22, y + 10),
        "Negotiators in Turkey left the summit without an agreement after two "
        "weeks of talks, deferring the hardest decisions on finance and "
        "emissions to next year.",
        bf, INK, w - 44, 29,
    )


def draw_story(draw, x, y, w, h, tag, headline, body, head_size=23, body_size=17):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=PANEL_EDGE, width=2)
    tf = font(SANS_BOLD, 14)
    tw = draw.textlength(tag, font=tf) + 16
    draw.rectangle([x, y, x + tw, y + 28], fill=TAG_BG)
    draw.text((x + 8, y + 6), tag, font=tf, fill=TAG_FG)
    hf = font(SERIF_BOLD, head_size)
    ny = text_block(draw, (x + 16, y + 42), headline, hf, INK, w - 32, head_size + 7)
    bf = font(SERIF, body_size)
    text_block(draw, (x + 16, ny + 6), body, bf, INK, w - 32, body_size + 7)


def build():
    img = Image.new("RGB", (CANVAS, CANVAS), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)

    inner_w = CANVAS - 2 * MARGIN
    draw_lead(draw, MARGIN, 178, inner_w, 216)

    gap = 14
    top = 408
    col_w = (inner_w - gap) // 2
    row_h = 176
    stories = [
        (
            "UKRAINE",
            "Ukraine sinks Russian corvette Merkury off Benghazi",
            "Kyiv said its forces struck the warship in the Mediterranean "
            "near the Libyan coast, a rare long-range naval hit.",
        ),
        (
            "MARKETS",
            "Nvidia brings back Jensen Huang as CEO; S&P 500 jumps 4.8%",
            "The chipmaker's founder returns to the top job, and shares "
            "surged, lifting the wider US market sharply.",
        ),
        (
            "MIDDLE EAST",
            "Trump warns strikes on Iran may resume amid US blockade",
            "The president said military action could return in the new "
            "year as Washington tightens its blockade.",
        ),
        (
            "POLITICS",
            "Democrats win biggest House majority since 1992",
            "The party took 258 seats, its largest share of the chamber "
            "in more than three decades.",
        ),
        (
            "LAW",
            "FBI captures most-wanted fugitive 'El Chapo Isidro'",
            "Agents arrested the cartel figure in Sinaloa after a "
            "years-long manhunt, officials said. The arrest ends a search "
            "that stretched across years and several Mexican states.",
        ),
    ]
    positions = [
        (MARGIN, top),
        (MARGIN + col_w + gap, top),
        (MARGIN, top + row_h + gap),
        (MARGIN + col_w + gap, top + row_h + gap),
        (MARGIN, top + 2 * (row_h + gap)),
    ]
    for (tag, head, body), (sx, sy) in zip(stories, positions):
        wide = sx == MARGIN and sy == top + 2 * (row_h + gap)
        w = inner_w if wide else col_w
        draw_story(draw, sx, sy, w, row_h, tag, head, body)

    foot_y = top + 3 * row_h + 2 * gap + 12
    hline(draw, foot_y, MARGIN, CANVAS - MARGIN, width=2)
    ff = font(SANS, 14)
    note = "Sources: wire reports, 23 November 2026  •  Infographic generated with Python + Pillow"
    fw = draw.textlength(note, font=ff)
    draw.text(((CANVAS - fw) / 2, foot_y + 10), note, font=ff, fill=FAINT)

    img.save(OUT_PATH, format="PNG", optimize=True)
    print("wrote", OUT_PATH, img.size)


if __name__ == "__main__":
    build()

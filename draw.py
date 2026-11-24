#!/usr/bin/env python3
"""Draw entry.png for news-image-20261123.

A 1024x1024 newspaper-style infographic summing up Monday
23 November 2026 in six stories. Run at build time only; the
grader copies the finished PNG via main.py.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (178, 34, 34)
GREY = (90, 90, 90)
PANEL_BG = (255, 255, 255)
RULE = (26, 26, 26)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def tag(draw, x, y, label, color):
    f = font(SANS_B, 17)
    w = draw.textlength(label, font=f) + 16
    draw.rectangle([x, y, x + w, y + 26], fill=color)
    draw.text((x + 8, y + 4), label, font=f, fill=(255, 255, 255))
    return y + 34


def icon_thermo(d, x, y, s):
    # thermometer with a rising red column
    cx = x + s // 2
    d.rounded_rectangle([cx - 8, y, cx + 8, y + s - 16], radius=8, outline=INK, width=3)
    d.ellipse([cx - 14, y + s - 30, cx + 14, y + s - 2], fill=RED, outline=INK, width=3)
    d.rectangle([cx - 4, y + 14, cx + 4, y + s - 20], fill=RED)
    for i in range(3):
        ty = y + 12 + i * 14
        d.line([cx + 12, ty, cx + 22, ty], fill=INK, width=3)


def icon_ship(d, x, y, s):
    # warship listing with smoke, struck at anchor
    by = y + s - 18
    d.polygon([(x + 4, by), (x + s - 4, by), (x + s - 14, by + 14), (x + 14, by + 14)],
              fill=(60, 60, 160), outline=INK)
    d.rectangle([x + 16, by - 18, x + 34, by], fill=(60, 60, 160), outline=INK, width=2)
    d.line([x + 25, by - 34, x + 25, by - 18], fill=INK, width=3)
    d.polygon([(x + 25, by - 34), (x + 25, by - 24), (x + 38, by - 29)], fill=RED, outline=INK)
    for cx, cy, r in ((x + 30, y + 8, 7), (x + 44, y + 2, 9), (x + 52, y + 12, 6)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GREY, outline=INK, width=2)
    for i in range(3):
        wx = x + 6 + i * (s // 3)
        d.arc([wx, by + 18, wx + 16, by + 28], 0, 180, fill=(60, 60, 160), width=2)


def icon_trade(d, x, y, s):
    # two opposing arrows: goods flowing both ways
    d.line([x + 6, y + 16, x + s - 16, y + 16], fill=(40, 120, 90), width=6)
    d.polygon([(x + s - 16, y + 8), (x + s - 2, y + 16), (x + s - 16, y + 24)], fill=(40, 120, 90))
    d.line([x + s - 6, y + s - 16, x + 16, y + s - 16], fill=(60, 60, 160), width=6)
    d.polygon([(x + 16, y + s - 24), (x + 2, y + s - 16), (x + 16, y + s - 8)], fill=(60, 60, 160))
    d.ellipse([x + s // 2 - 7, y + s // 2 - 7, x + s // 2 + 7, y + s // 2 + 7],
              fill=(230, 190, 60), outline=INK, width=2)


def icon_missile(d, x, y, s):
    # missile arc over a shoreline
    d.arc([x, y - 6, x + s, y + s], 180, 330, fill=INK, width=3)
    mx, my = x + s - 10, y + s // 2 - 6
    d.polygon([(mx, my), (mx - 20, my + 4), (mx - 6, my + 16)], fill=RED, outline=INK)
    d.line([x, y + s - 4, x + s, y + s - 4], fill=(60, 60, 160), width=4)
    for i in range(3):
        wx = x + 6 + i * (s // 3)
        d.arc([wx, y + s - 14, wx + 16, y + s - 4], 0, 180, fill=(60, 60, 160), width=2)


def icon_ballot(d, x, y, s):
    # ballot box with a checked ballot
    d.rectangle([x + 10, y + s - 26, x + s - 10, y + s - 4], fill=(40, 120, 90), outline=INK, width=3)
    d.line([x + 4, y + s - 26, x + s - 4, y + s - 26], fill=INK, width=4)
    d.rectangle([x + s // 2 - 4, y + 4, x + s // 2 + 4, y + s - 26], fill=(255, 255, 255), outline=INK, width=2)
    d.line([x + s // 2 - 12, y + 14, x + s // 2 - 4, y + 22], fill=RED, width=4)
    d.line([x + s // 2 - 4, y + 22, x + s // 2 + 12, y + 6], fill=RED, width=4)


def icon_badge(d, x, y, s):
    # police star badge
    cx, cy = x + s // 2, y + s // 2
    pts = []
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        r = s // 2 - 2 if i % 2 == 0 else s // 4
        pts.append((cx + r * math.cos(ang), cy - r * math.sin(ang)))
    d.polygon(pts, fill=(230, 190, 60), outline=INK)
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(255, 255, 255), outline=INK, width=2)
    d.line([cx - 6, cy, cx - 1, cy + 5], fill=INK, width=3)
    d.line([cx - 1, cy + 5, cx + 7, cy - 6], fill=INK, width=3)


def panel(d, x, y, w, h, tag_label, tag_color, headline, body, icon_fn):
    d.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=RULE, width=2)
    yy = tag(d, x + 16, y + 14, tag_label, tag_color)
    icon_fn(d, x + w - 86, y + 14, 64)
    yy = text_block(d, x + 16, yy + 4, headline, font(SERIF_B, 30), INK, w - 110, 34)
    text_block(d, x + 16, yy + 6, body, font(SANS, 20), GREY, w - 32, 26)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    title = "THE WORLD IN A DAY"
    tf = font(SERIF_B, 62)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 26), title, font=tf, fill=INK)
    d.line([40, 108, W - 40, 108], fill=RULE, width=4)
    d.line([40, 116, W - 40, 116], fill=RULE, width=1)
    date = "MONDAY 23 NOVEMBER 2026"
    df = font(SANS_B, 40)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 126), date, font=df, fill=RED)
    sub = "The day's world news in one picture"
    sf = font(SERIF, 24)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 176), sub, font=sf, fill=GREY)

    # lead story
    panel(d, 40, 216, W - 80, 168, "CLIMATE · ANTALYA", (70, 150, 70),
          "COP31 climate talks end with no deal",
          "The UN summit in Turkey ended without agreement after the "
          "EU rejected a draft that never mentions fossil fuels — the "
          "longest climate talks in history.",
          icon_thermo)

    # 2x2 grid
    gx, gy, gw, gh, gap = 40, 398, (W - 80 - 16) // 2, 206, 14
    panel(d, gx, gy, gw, gh, "WAR · LIBYA", RED,
          "Ukraine sinks Russian warship in Libya",
          "Naval drones sank the corvette Merkury at Benghazi; "
          "Zelenskyy confirmed the strike on Monday.",
          icon_ship)
    panel(d, gx + gw + gap, gy, gw, gh, "MARKETS · NEW YORK", (40, 120, 90),
          "Nvidia brings back its chief; stocks soar",
          "Jensen Huang returned as CEO 11 days after resigning; "
          "shares jumped and the S&P 500 rose 4.8%.",
          icon_trade)
    panel(d, gx, gy + gh + gap, gw, gh, "MIDDLE EAST · GULF", (110, 60, 140),
          "Trump warns Iran strikes may resume in new year",
          "The president threatened to sink tankers breaking the US "
          "blockade as Iran vowed to use 'all means' against it.",
          icon_missile)
    panel(d, gx + gw + gap, gy + gh + gap, gw, gh, "POLITICS · WASHINGTON", (60, 60, 160),
          "Democrats take biggest House majority since 1992",
          "A North Carolina recount win gave Democrats at least 258 "
          "seats — their largest House majority in 34 years.",
          icon_ballot)

    # bottom strip
    panel(d, 40, gy + 2 * gh + 2 * gap, W - 80, 128, "JUSTICE · MEXICO", (230, 110, 30),
          "FBI's most-wanted 'El Chapo Isidro' captured",
          "Mexican forces seized the cartel boss in Sinaloa, with US intelligence help.",
          icon_badge)

    # footer
    foot = "All six stories happened or were first reported on Monday 23 November 2026."
    ff = font(SANS_B, 20)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, H - 44), foot, font=ff, fill=INK)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()

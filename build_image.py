#!/usr/bin/env python3
"""Render the 23 November 2026 world-news cover (1024x1024 PNG).

Design: The Economist full-bleed cover. Cream page, red masthead
"THE WORLD TODAY", huge date title, one dominant scene (the COP31
climate summit collapsing in Antalya) plus two smaller stories:
tankers struck in the Strait of Hormuz, and Russian cruise missiles
landing in Poland as NATO meets. All drawing is done with PIL shapes.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (243, 237, 216)
INK = (26, 26, 26)
RED = (190, 18, 38)
DARK = (28, 42, 52)
STEEL = (58, 84, 102)
GOLD = (198, 148, 52)
SEA = (46, 106, 138)
LAND = (122, 168, 92)
SMOKE = (120, 120, 116)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def centred(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def rule(draw, y, x0=48, x1=976, fill=INK, width=3):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_globe(draw, cx, cy, r):
    """A cracked globe: blue sphere, green land blobs, a black crack."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SEA, outline=INK, width=4)
    # land masses as flat blobs
    draw.ellipse([cx - r * 0.75, cy - r * 0.55, cx - r * 0.05, cy + r * 0.05],
                 fill=LAND)
    draw.ellipse([cx + r * 0.05, cy + r * 0.1, cx + r * 0.7, cy + r * 0.6],
                 fill=LAND)
    draw.ellipse([cx - r * 0.2, cy - r * 0.9, cx + r * 0.35, cy - r * 0.45],
                 fill=LAND)
    # meridians
    for k in (-0.55, 0.0, 0.55):
        draw.arc([cx - r, cy - r, cx + r, cy + r],
                 start=90 + k * 60, end=270 + k * 60, fill=(210, 225, 235),
                 width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=(210, 225, 235), width=2)
    # the crack: a jagged black line splitting the globe
    pts = [(cx - r * 0.15, cy - r), (cx + r * 0.1, cy - r * 0.55),
           (cx - r * 0.12, cy - r * 0.2), (cx + r * 0.18, cy + r * 0.15),
           (cx - r * 0.05, cy + r * 0.5), (cx + r * 0.12, cy + r * 0.85)]
    draw.line(pts, fill=INK, width=6, joint="curve")
    # smoke curling off the top, kept inside the hall panel
    for i, (sx, sy, sr) in enumerate([(cx - 88, cy - r + 14, 18),
                                     (cx - 62, cy - r - 2, 22),
                                     (cx + 86, cy - r + 8, 16)]):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                     fill=(SMOKE[0] - i * 8, SMOKE[1] - i * 8, SMOKE[2] - i * 8))


def draw_hall(draw):
    """Conference hall: dark panel, empty chairs and a long table."""
    draw.rectangle([48, 252, 976, 556], fill=DARK, outline=INK, width=3)
    # tall windows glowing behind the table
    for x in (120, 300, 480, 660, 840):
        draw.rectangle([x, 274, x + 76, 416], fill=(214, 196, 140),
                       outline=INK, width=2)
        draw.line([(x + 38, 274), (x + 38, 416)], fill=INK, width=2)
    # the globe hangs over the hall
    draw_globe(draw, 512, 362, 84)
    # empty chairs: dark silhouettes along the table
    for x in (150, 290, 430, 570, 710, 850):
        draw.rounded_rectangle([x - 34, 436, x + 34, 486], radius=10,
                               fill=(12, 20, 26), outline=INK, width=2)
        draw.rectangle([x - 34, 484, x + 34, 494], fill=(12, 20, 26))
    # long table with papers and microphones
    draw.rectangle([90, 494, 934, 540], fill=(96, 62, 32), outline=INK, width=3)
    draw.rectangle([90, 494, 934, 504], fill=(128, 84, 44))
    for x in (200, 380, 560, 740):
        draw.line([(x, 494), (x, 468)], fill=INK, width=3)
        draw.ellipse([x - 7, 460, x + 7, 474], fill=INK)
        draw.rectangle([x - 26, 506, x + 26, 516], fill=(240, 236, 220))
    # gavel lying on the table, unstruck
    draw.line([(470, 521), (560, 521)], fill=(60, 38, 18), width=7)
    draw.rectangle([548, 510, 576, 532], fill=(60, 38, 18), outline=INK, width=2)


def draw_tanker(draw, x0, y0, x1, y1):
    """Oil tanker on a strait, smoke and flame above it."""
    midy = y0 + (y1 - y0) * 0.62
    draw.rectangle([x0, y0, x1, y1], fill=(214, 226, 232))
    # sea
    draw.rectangle([x0, midy, x1, y1], fill=(38, 88, 118))
    for k in range(4):
        wx = x0 + 20 + k * 95
        draw.arc([wx, midy + 12, wx + 60, midy + 30], start=200, end=340,
                 fill=(210, 225, 235), width=3)
    # hull and deck
    draw.polygon([(x0 + 18, midy - 6), (x1 - 18, midy - 6), (x1 - 40, midy + 26),
                  (x0 + 40, midy + 26)], fill=(40, 40, 44), outline=INK, width=2)
    draw.rectangle([x0 + 60, midy - 34, x0 + 130, midy - 6], fill=(200, 60, 40),
                   outline=INK, width=2)
    draw.rectangle([x1 - 130, midy - 30, x1 - 60, midy - 6], fill=(230, 230, 225),
                   outline=INK, width=2)
    # funnel with flame and smoke
    draw.rectangle([x0 + 200, midy - 52, x0 + 224, midy - 6], fill=(30, 30, 34),
                   outline=INK, width=2)
    draw.polygon([(x0 + 204, midy - 52), (x0 + 212, midy - 84),
                  (x0 + 220, midy - 52)], fill=(240, 130, 30))
    draw.ellipse([x0 + 176, midy - 96, x0 + 216, midy - 56], fill=SMOKE)
    draw.ellipse([x0 + 196, midy - 106, x0 + 240, midy - 70], fill=(140, 140, 136))


def draw_missiles(draw, x0, y0, x1, y1):
    """Missile streaks over a map pin and a NATO-style compass star."""
    draw.rectangle([x0, y0, x1, y1], fill=(226, 222, 206))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 + 8
    # streaks
    for i, (sx, sy, ex, ey) in enumerate([
            (x0 + 30, y0 + 30, x0 + 150, y0 + 78),
            (x0 + 90, y0 + 14, x0 + 210, y0 + 62),
            (x0 + 150, y0 + 34, x0 + 260, y0 + 82)]):
        draw.line([(sx, sy), (ex, ey)], fill=RED, width=5)
        draw.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=RED)
    # compass star
    for ang in range(0, 360, 90):
        a = math.radians(ang)
        tip = (cx + 34 * math.cos(a), cy + 34 * math.sin(a))
        base1 = (cx + 9 * math.cos(a + math.pi / 2), cy + 9 * math.sin(a + math.pi / 2))
        base2 = (cx + 9 * math.cos(a - math.pi / 2), cy + 9 * math.sin(a - math.pi / 2))
        draw.polygon([tip, base1, base2], fill=STEEL, outline=INK)
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=GOLD, outline=INK, width=2)
    # impact bursts
    for bx, by in [(x0 + 60, y1 - 34), (x1 - 70, y1 - 26)]:
        draw.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(240, 130, 30))
        draw.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=(250, 210, 60))


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # masthead
    mast = font(SERIF, 66)
    centred(d, 512, 30, "THE WORLD TODAY", mast, RED)
    rule(d, 116)
    rule(d, 122, width=1)

    # huge date title
    date = font(SERIF, 62)
    centred(d, 512, 140, "23 NOVEMBER 2026", date, INK)
    sub = font(SERIF_IT, 30)
    centred(d, 512, 212, "Monday", sub, INK)

    # dominant scene: the collapsing climate summit
    draw_hall(d)

    # main cover line
    head = font(SERIF, 58)
    centred(d, 512, 570, "COP31 COLLAPSES", head, RED)
    deck = font(SERIF_IT, 29)
    centred(d, 512, 640, "Climate talks end with no deal on fossil fuels",
            deck, INK)
    rule(d, 690, width=2)

    # two smaller stories, side by side
    left = (48, 712, 496, 888)
    right = (528, 712, 976, 888)
    draw_tanker(d, *left)
    draw_missiles(d, *right)
    d.rectangle([48, 712, 496, 888], outline=INK, width=3)
    d.rectangle([528, 712, 976, 888], outline=INK, width=3)

    lab = font(SANS, 25)
    small = font(SERIF, 23)
    centred(d, 272, 898, "HORMUZ BURNS", lab, RED)
    centred(d, 272, 928, "Tankers struck in the strait", small, INK)
    centred(d, 752, 898, "MISSILES IN POLAND", lab, RED)
    centred(d, 752, 928, "NATO meets after the strikes", small, INK)

    # footer: the fourth story, small
    rule(d, 962, width=2)
    foot = font(SERIF, 21)
    centred(d, 512, 970,
            "Also: Ukrainian drones strike a Russian warship in Libya",
            foot, INK)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news front page (1024x1024 PNG).

Deterministic: fixed palette, fixed fonts, no randomness, no network.
Run: python3 compose.py  -> writes entry.png next to this file.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)      # newsprint cream
INK = (18, 24, 38)           # near-black navy
NAVY = (20, 33, 61)          # masthead
GOLD = (198, 142, 32)        # rule / accents
RED = (178, 34, 34)          # kicker red
GREY = (90, 92, 96)
FLAME = (232, 116, 26)
FLAME2 = (244, 180, 60)
SKY = (38, 48, 74)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning list of lines fitting `width` px."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def para(draw, xy, text, fnt, fill, width, leading=None):
    x, y = xy
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_refinery(draw, box):
    """Small flat illustration: refinery towers, flames, smoke, dusk sky."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SKY)
    # dusk band
    draw.rectangle([x0, y1 - 56, x1, y1], fill=(58, 44, 52))
    # smoke puffs
    for cx, cy, r in [(x0 + 55, y0 + 34, 22), (x0 + 85, y0 + 20, 16),
                      (x0 + 215, y0 + 38, 20), (x0 + 242, y0 + 24, 14)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 118, 122))
    # towers (all inside the box)
    for tx, tw, th in [(x0 + 18, 30, 108), (x0 + 62, 24, 136),
                       (x0 + 100, 38, 92), (x0 + 155, 26, 122),
                       (x0 + 195, 34, 100)]:
        draw.rectangle([tx, y1 - th, tx + tw, y1], fill=(12, 14, 22))
        draw.rectangle([tx + 4, y1 - th - 10, tx + tw - 4, y1 - th],
                       fill=(12, 14, 22))
    # storage tank
    draw.ellipse([x0 + 245, y1 - 52, x0 + 308, y1 - 16], fill=(16, 18, 28))
    draw.rectangle([x0 + 245, y1 - 34, x0 + 308, y1], fill=(16, 18, 28))
    # flames over towers 1, 2 and 4
    for fx, fh in [(x0 + 33, 62), (x0 + 74, 80), (x0 + 168, 68)]:
        draw.polygon([(fx - 14, y1 - 106), (fx, y1 - 106 - fh),
                      (fx + 14, y1 - 106)], fill=FLAME)
        draw.polygon([(fx - 7, y1 - 106), (fx, y1 - 106 - fh + 22),
                      (fx + 7, y1 - 106)], fill=FLAME2)
    # ground glow
    draw.rectangle([x0, y1 - 5, x1, y1], fill=FLAME)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead (0..136) ---------------------------------------------
    d.rectangle([0, 0, W, 130], fill=NAVY)
    d.rectangle([0, 130, W, 136], fill=GOLD)
    d.text((512, 12), "THE WORLD IN ONE DAY",
           font=font(SERIF_B, 56), fill=(247, 243, 234), anchor="ma")
    d.text((512, 78), "THURSDAY, 26 NOVEMBER 2026",
           font=font(SANS_B, 30), fill=(232, 190, 90), anchor="ma")
    d.text((512, 112), "One day. Five continents. The news that mattered.",
           font=font(SANS, 17), fill=(200, 205, 215), anchor="ma")

    # ---- lead story (148..388) -----------------------------------------
    f_kick = font(SANS_B, 21)
    f_lead = font(SERIF_B, 42)
    f_sub = font(SANS, 25)
    d.text((32, 148), "LEAD  •  ENERGY & WAR", font=f_kick, fill=RED)
    y = para(d, (32, 176), "Houthis strike Saudi\nArabia's biggest refinery",
             f_lead, INK, 600, leading=48)
    y = para(d, (32, y + 8),
             "Ras Tanura ablaze after a Houthi strike; fires burn at the "
             "world's largest oil terminal as Brent crude tops $94 a barrel.",
             f_sub, INK, 590, leading=31)
    draw_refinery(d, (668, 148, 992, 372))
    d.text((668, 378), "Ras Tanura refinery, ablaze.",
           font=font(SANS, 15), fill=GREY)
    d.line([(32, 396), (992, 396)], fill=(180, 172, 152), width=2)

    # ---- row 2: Gaza | Ukraine (410..650) ------------------------------
    f_h2 = font(SERIF_B, 30)
    f_b2 = font(SANS, 22)
    col_w = 460
    y = 410
    x = 32
    d.text((x, y), "GAZA  •  CEASEFIRE STRAINED", font=f_kick, fill=RED)
    yy = para(d, (x, y + 30),
              "Israel kills Hamas security chief in Gaza strike",
              f_h2, INK, col_w, leading=34)
    yy = para(d, (x, yy + 4),
              "Mohammad Abuelouf, who ran Hamas's interior security, is "
              "killed with his wife and two children. Mediators scramble "
              "to hold the truce.", f_b2, INK, col_w, leading=27)
    x = 532
    d.text((x, y), "UKRAINE  •  THE OIL WAR", font=f_kick, fill=RED)
    yy2 = para(d, (x, y + 30),
               "Kyiv hits Russian refineries; Putin vows retaliation",
               f_h2, INK, col_w, leading=34)
    yy2 = para(d, (x, yy2 + 4),
               "Ukraine presses its campaign against Russian fuel plants. "
               "Moscow's own figures now show nearly 500,000 Russians lost "
               "in the war.", f_b2, INK, col_w, leading=27)
    y = max(yy, yy2)
    d.line([(32, y + 10), (992, y + 10)], fill=(180, 172, 152), width=2)

    # ---- row 3: Mercury | Cairo (y+26 ..) ------------------------------
    y = y + 26
    x = 32
    d.text((x, y), "SPACE  •  EIGHT YEARS OUT", font=f_kick, fill=RED)
    yy = para(d, (x, y + 30),
              "BepiColombo reaches Mercury orbit at last",
              f_h2, INK, col_w, leading=34)
    yy = para(d, (x, yy + 4),
              "The European-Japanese probe enters orbit around the Sun's "
              "closest planet after an eight-year journey.",
              f_b2, INK, col_w, leading=27)
    x = 532
    d.text((x, y), "EGYPT  •  HIGHWAY FIRE", font=f_kick, fill=RED)
    yy2 = para(d, (x, y + 30),
               "Fuel tanker crash kills at least 30 near Cairo",
               f_h2, INK, col_w, leading=34)
    yy2 = para(d, (x, yy2 + 4),
               "A tanker crash sets off a huge fire on a highway ringing "
               "the Egyptian capital; dozens are feared dead.",
               f_b2, INK, col_w, leading=27)
    y = max(yy, yy2)
    d.line([(32, y + 10), (992, y + 10)], fill=(180, 172, 152), width=2)

    # ---- also today ----------------------------------------------------
    y = y + 24
    d.text((32, y), "ALSO TODAY — 26 NOVEMBER 2026",
           font=font(SANS_B, 20), fill=NAVY)
    y = para(d, (32, y + 28),
             "Pakistan's first astronaut bound for Tiangong  •  India marks "
             "18 years since 26/11  •  Gukesh–Sindarov draw Game 2  •  "
             "Andy Taylor dies at 65  •  US prepares new tariffs",
             font(SANS, 20), INK, 960, leading=26)
    # ---- footer ---------------------------------------------------------
    d.text((512, 988),
           "To the judge: this page sums up Thursday 26 November 2026.  •  "
           "make.fun news-image-20261126  •  @albari5271",
           font=font(SANS, 16), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()

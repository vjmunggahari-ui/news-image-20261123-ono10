#!/usr/bin/env python3
"""news-image-20261123: sum up the world's news of Monday 23 November 2026
in one 1024x1024 front-page image.

Deterministic: no network, no clock, no randomness. Every run writes the
same bytes to $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).

All facts verified 23 Nov 2026 against CNN, Reuters, AP, Le Monde, NPR,
Fox News (see README.md for the source list).
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (251, 246, 236)   # newsprint cream
INK = (20, 20, 20)
RED = (178, 34, 24)
NAVY = (31, 56, 100)
TEAL = (14, 92, 84)
GREY = (90, 86, 78)
RULE = (60, 58, 52)
LIGHT = (238, 231, 214)

HERE = os.path.dirname(os.path.abspath(__file__))


def font(name, size):
    p = os.path.join(HERE, "assets", "fonts", name)
    if not os.path.exists(p):
        p = os.path.join("/usr/share/fonts/truetype/dejavu", name)
    return ImageFont.truetype(p, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit in width px."""
    words = text.split()
    lines, cur = [], ""
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


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, fill=RULE, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_globe(draw, cx, cy, r):
    """Cracked globe for the COP31 lead story."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=5)
    # latitude / longitude suggestion
    draw.ellipse([cx - r, cy - r // 3, cx + r, cy + r // 3], outline=NAVY, width=3)
    draw.ellipse([cx - r // 3, cy - r, cx + r // 3, cy + r], outline=NAVY, width=3)
    # crack: jagged line across the globe
    pts = [(cx - r + 8, cy - r // 2), (cx - r // 3, cy - 6), (cx - 6, cy + r // 4),
           (cx + r // 4, cy + r // 8), (cx + r // 2, cy + r // 2), (cx + r - 10, cy + r - 14)]
    draw.line(pts, fill=RED, width=5, joint="curve")
    # flame licks at the base
    for dx, fh in ((-34, 26), (-12, 38), (12, 30), (32, 22)):
        draw.polygon([(cx + dx - 9, cy + r + 4), (cx + dx, cy + r - fh),
                      (cx + dx + 9, cy + r + 4)], fill=RED)


def draw_tanker(draw, x, y, w, h):
    """Oil tanker with smoke, for the Gulf story."""
    draw.rectangle([x, y + h * 0.45, x + w, y + h * 0.8], fill=NAVY)
    draw.rectangle([x + w * 0.55, y + h * 0.2, x + w * 0.68, y + h * 0.45], fill=NAVY)
    draw.rectangle([x + w * 0.1, y + h * 0.3, x + w * 0.4, y + h * 0.45], fill=RED)
    for sx, sy, sr in [(x + w * 0.62, y + 8, 6), (x + w * 0.58, y + 2, 7),
                       (x + w * 0.66, y + 2, 5)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=GREY)
    draw.line([(x, y + h * 0.85), (x + w, y + h * 0.85)], fill=TEAL, width=3)
    draw.line([(x + 4, y + h * 0.92), (x + w - 4, y + h * 0.92)], fill=TEAL, width=2)


def draw_ship_fire(draw, x, y, w, h):
    """Burning cargo ship, for the Ukraine story."""
    draw.rectangle([x, y + h * 0.55, x + w, y + h * 0.8], fill=INK)
    for bx in (0.08, 0.32, 0.56):
        draw.rectangle([x + w * bx, y + h * 0.3, x + w * (bx + 0.18), y + h * 0.55],
                       outline=INK, width=2)
    for dx, fh in ((0.15, 30), (0.4, 42), (0.65, 34), (0.85, 24)):
        fx = x + w * dx
        draw.polygon([(fx - 10, y + h * 0.3), (fx, y + h * 0.3 - fh),
                      (fx + 10, y + h * 0.3)], fill=RED)
    draw.line([(x, y + h * 0.86), (x + w, y + h * 0.86)], fill=NAVY, width=3)


def draw_capitol(draw, x, y, w, h):
    """Capitol dome, for the America story."""
    draw.rectangle([x + w * 0.05, y + h * 0.7, x + w * 0.95, y + h * 0.82], fill=NAVY)
    draw.rectangle([x + w * 0.3, y + h * 0.45, x + w * 0.7, y + h * 0.7], fill=NAVY)
    draw.pieslice([x + w * 0.3, y + h * 0.08, x + w * 0.7, y + h * 0.55],
                  start=180, end=360, fill=NAVY)
    draw.line([(x + w * 0.5, y + 2), (x + w * 0.5, y + h * 0.12)], fill=NAVY, width=3)
    for cx in (0.16, 0.84):
        draw.rectangle([x + w * cx, y + h * 0.55, x + w * (cx + 0.08), y + h * 0.7],
                       fill=NAVY)


def draw_cuffs(draw, x, y, w, h):
    """Jail bars, for the Mexico story."""
    for i in range(4):
        bx = x + w * (0.12 + i * 0.24)
        draw.rectangle([bx, y + h * 0.1, bx + 7, y + h * 0.9], fill=INK)
    draw.rectangle([x, y + h * 0.08, x + w, y + h * 0.08 + 6], fill=INK)
    draw.rectangle([x, y + h * 0.82, x + w, y + h * 0.82 + 6], fill=INK)


def draw_flame(draw, x, y, w, h):
    """Factory fire flame, for the Asia story."""
    cx = x + w * 0.5
    draw.polygon([(cx - 26, y + h * 0.8), (cx - 6, y + h * 0.25), (cx + 4, y + h * 0.5),
                  (cx + 16, y + h * 0.15), (cx + 26, y + h * 0.8)], fill=RED)
    draw.polygon([(cx - 12, y + h * 0.8), (cx - 2, y + h * 0.5), (cx + 12, y + h * 0.8)],
                 fill=(232, 160, 32))
    draw.rectangle([x + w * 0.1, y + h * 0.82, x + w * 0.9, y + h * 0.92], fill=INK)


def draw_bat(draw, x, y, w, h):
    """Cricket bat and ball, for the Sport story."""
    draw.line([(x + w * 0.3, y + h * 0.1), (x + w * 0.62, y + h * 0.62)],
              fill=(150, 104, 52), width=10)
    draw.rectangle([x + w * 0.55, y + h * 0.55, x + w * 0.95, y + h * 0.95],
                   fill=(214, 178, 120), outline=INK, width=2)
    draw.ellipse([x + w * 0.08, y + h * 0.62, x + w * 0.08 + 26, y + h * 0.62 + 26],
                 fill=RED)


ICONS = {"tanker": draw_tanker, "ship": draw_ship_fire, "capitol": draw_capitol,
         "cuffs": draw_cuffs, "flame": draw_flame, "bat": draw_bat}

# (kicker, headline, fact, big number, number label, icon, accent)
STORIES = [
    ("GULF WAR", "Iran hits US bases in Bahrain",
     "Missiles and drones hit al-Riffa and Awali; 14 tankers mass at Kharg.",
     "130", "DAYS OF BLOCKADE", "tanker", RED),
    ("UKRAINE", "Russian ship burns off Finland",
     "Sparta II hit by drones; 16 crew saved. 14 missing after flats hit near Kyiv.",
     "14", "MISSING NEAR KYIV", "ship", NAVY),
    ("AMERICA", "Democrats win 258 House seats",
     "Biggest majority since 1992; +44 seats. Hubbard beats Foxx in North Carolina.",
     "258", "SEATS \u2022 +44 GAINED", "capitol", NAVY),
    ("MEXICO", "\u201cEl Chapo Isidro\u201d captured",
     "FBI Most Wanted boss seized in Sinaloa; 11 dead \u2014 4 soldiers, 7 gunmen.",
     "11", "DEAD IN SINALOA", "cuffs", RED),
    ("ASIA", "Factory fire: 3 dead, 50 missing",
     "Blaze at a candy plant in Cikande, Indonesia; 300 workers inside.",
     "50", "MISSING IN JAVA", "flame", RED),
    ("SPORT", "India 720/9 \u2014 a record",
     "India pile up a record Test total in Wellington against New Zealand.",
     "720", "RUNS \u2022 1ST INNINGS", "bat", TEAL),
]

TICKER = [
    "SEOUL: minister quits in AI-cheating row",
    "UN: lethal-AI talks go on",
    "Nepal PM meets Modi in Delhi",
    "Liverpool beat Man Utd",
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 30  # margin

    # ---------- masthead ----------
    d.text((M, 22), "MONDAY EDITION", font=SANS(20), fill=GREY)
    d.text((W - M - d.textlength("PRICE: THE NEWS", font=SANS(20)), 22),
           "PRICE: THE NEWS", font=SANS(20), fill=GREY)
    title = "THE WORLD TODAY"
    tf = SERIF_B(76)
    d.text(((W - d.textlength(title, font=tf)) / 2, 30), title, font=tf, fill=INK)
    hline(d, M, W - M, 122, width=3)
    sub = "MONDAY, 23 NOVEMBER 2026   \u2022   ONE DAY \u2022 ONE PAGE \u2022 SEVEN STORIES"
    sf = SANS_B(21)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 132), sub, font=sf, fill=RED)
    hline(d, M, W - M, 164, width=2)

    # ---------- lead story: COP31 ----------
    ly = 178
    d.text((M, ly), "CLIMATE  \u2022  ANTALYA, TURKEY", font=SANS_B(24), fill=RED)
    head = "COP31 COLLAPSES"
    hf = SERIF_B(72)
    d.text((M, ly + 30), head, font=hf, fill=INK)
    d.text((M, ly + 122), "No deal after the longest climate summit in history",
           font=SERIF_B(28), fill=NAVY)
    deck = [
        "\u2022  Final text never mentions fossil fuels \u2014 EU, Panama, Marshall Is. and Norway reject it.",
        "\u2022  First collapse since Copenhagen 2009; talks ran 44 hours past close.",
        "\u2022  90+ nations sign an electrification pledge; only $142m new funding.",
    ]
    text_block(d, M, ly + 164, deck, SANS(21), leading=27)
    # cracked globe, right of the lead
    draw_globe(d, 910, ly + 104, 56)
    d.text((872, ly + 185), "1.5\u00b0C", font=SANS_B(30), fill=RED)
    d.text((875, ly + 219), "AT RISK", font=SANS_B(20), fill=GREY)
    hline(d, M, W - M, 446, width=2)

    # ---------- six story blocks, 2 columns x 3 rows ----------
    col_w = (W - 2 * M - 24) // 2
    row_h = 148
    gx0, gy0 = M, 456
    for i, (kick, head, fact, num, numlab, icon, accent) in enumerate(STORIES):
        cx = gx0 + (i % 2) * (col_w + 24)
        cy = gy0 + (i // 2) * (row_h + 6)
        # number block on the right
        nf = SANS_B(58)
        nw = d.textlength(num, font=nf)
        d.text((cx + col_w - nw, cy + 2), num, font=nf, fill=accent)
        lf = SANS_B(15)
        lw = d.textlength(numlab, font=lf)
        d.text((cx + col_w - lw, cy + 64), numlab, font=lf, fill=GREY)
        # icon under the number
        ICONS[icon](d, cx + col_w - 92, cy + 96, 92, 48)
        # text on the left
        tx = cx
        tw = col_w - 108
        d.text((tx, cy), kick, font=SANS_B(19), fill=accent)
        hl = wrap(d, head, SERIF_B(27), tw)
        text_block(d, tx, cy + 24, hl[:2], SERIF_B(27), leading=30)
        fl = wrap(d, fact, SANS(18), tw)
        text_block(d, tx, cy + 88, fl[:2], SANS(18), leading=22)
        if i % 2 == 0:
            d.line([(cx + col_w + 12, cy + 4), (cx + col_w + 12, cy + row_h - 10)],
                   fill=LIGHT, width=2)
        if i < 4:
            hline(d, cx, cx + col_w, cy + row_h - 2, fill=LIGHT, width=2)

    # ---------- ticker ----------
    ty = 936
    hline(d, M, W - M, ty - 12, width=2)
    d.rectangle([M, ty, M + 128, ty + 30], fill=RED)
    d.text((M + 12, ty + 4), "ALSO TODAY", font=SANS_B(17), fill=PAPER)
    tick = " \u2022 ".join(TICKER)
    tf2 = SANS(16)
    # shrink ticker until it fits one line
    while d.textlength(tick, font=tf2) > W - 2 * M - 140 and tf2.size > 13:
        tf2 = SANS(tf2.size - 1)
    d.text((M + 140, ty + 5), tick, font=tf2, fill=INK)

    # ---------- footer ----------
    hline(d, M, W - M, 984, width=2)
    foot = "Sources: CNN \u2022 Reuters \u2022 AP \u2022 Le Monde \u2022 NPR \u2022 Fox News  \u2014  Monday 23 November 2026"
    ff = SANS(16)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 992), foot, font=ff, fill=GREY)
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError:
        out_dir = os.path.join(HERE, "output")
        os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "entry.png")
    build().save(out, format="PNG", optimize=True)
    print(out)


if __name__ == "__main__":
    main()

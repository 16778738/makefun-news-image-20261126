#!/usr/bin/env python3
"""
news-image-20261126 — Sum up 26 November 2026 world news in one image.

Build (do NOT submit) for make.fun bounty news-image-20261126 ($100).
When run, writes one image to /output/entry.png (override with --out PATH).

Run:
    python3 main.py
    python3 main.py --out entry.png

Requires: Python 3.11+ and Pillow (pip install pillow).
No network, no API key, no external assets — all art is drawn with Pillow.
Fonts: DejaVu Sans (bundled on most Linux systems).
Deterministic: two runs write identical bytes.
"""
import argparse
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 1280
BG = (11, 18, 32)
PANEL = (22, 35, 58)
PANEL_EDGE = (48, 70, 102)
WHITE = (255, 255, 255)
MUTED = (178, 190, 208)
GOLD = (245, 197, 66)
ACCENTS = [
    (255, 107, 53),   # Hormuz — flame orange
    (255, 196, 0),    # Tariffs — yellow
    (46, 204, 113),   # Markets — green
    (86, 156, 255),   # Colombia — blue
    (186, 104, 255),  # Hong Kong — purple
    (0, 200, 190),    # Mercury — teal
]

STORIES = [
    {
        "kicker": "STRAIT OF HORMUZ",
        "title": "US tells citizens:\nleave Iran now",
        "caption": "Houthi strikes spread as Gulf tensions soar.",
        "icon": "ship",
    },
    {
        "kicker": "TRADE WAR",
        "title": "New tariffs proposed\non 14 nations",
        "caption": "US targets EU, India and China over capacity.",
        "icon": "globe",
    },
    {
        "kicker": "MARKETS",
        "title": "Asia stocks tumble;\nDow tops 50,000",
        "caption": "KOSPI plunges 6.2% as tech sells off.",
        "icon": "chart",
    },
    {
        "kicker": "COLOMBIA",
        "title": "Troops storm market,\nfree hostages",
        "caption": "All hostages freed in Cartagena raid.",
        "icon": "shield",
    },
    {
        "kicker": "HONG KONG",
        "title": "Tower fire kills 14\nin Tai Po",
        "caption": "Blaze engulfs high-rises; firefighter among dead.",
        "icon": "blast",
    },
    {
        "kicker": "SPACE • MERCURY",
        "title": "Europe–Japan probe\nreaches Mercury",
        "caption": "Eight-year journey ends at the innermost planet.",
        "icon": "rocket",
    },
]

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_icon(draw, kind, cx, cy, r, color):
    """Simple, high-contrast pictograms drawn from primitives."""
    if kind == "ship":
        # hull + funnel + waves
        draw.polygon([(cx - r, cy + 5), (cx + r, cy + 5), (cx + r - 18, cy + r - 8), (cx - r + 18, cy + r - 8)], fill=color)
        draw.rectangle([cx - 28, cy - r + 18, cx + 8, cy + 2], fill=color)
        draw.rectangle([cx + 18, cy - r + 28, cx + 34, cy + 2], fill=color)
        for x in (-r + 6, -8, r - 34):
            draw.arc([cx + x, cy + r - 6, cx + x + 28, cy + r + 14], 0, 180, fill=color, width=4)
    elif kind == "blast":
        pts = []
        for i in range(16):
            ang = math.pi * i / 8
            rr = r if i % 2 == 0 else r * 0.45
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        draw.polygon(pts, fill=color)
        draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=BG)
    elif kind == "globe":
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=6)
        draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=color, width=4)
        draw.line([cx - r, cy, cx + r, cy], fill=color, width=4)
        # crack
        draw.line([cx - 10, cy - r, cx + 14, cy - 6, cx - 4, cy + r], fill=(255, 80, 80), width=6)
    elif kind == "chart":
        # three descending bars = falling market
        bars = [(-34, -34), (0, -12), (34, 12)]
        for dx, top in bars:
            draw.rectangle([cx + dx - 11, cy + top, cx + dx + 11, cy + r - 6], fill=color)
        draw.line([cx - r, cy + r - 6, cx + r, cy + r - 6], fill=color, width=4)
    elif kind == "shield":
        # shield outline + check
        pts = [(cx, cy - r), (cx + r * 0.85, cy - r * 0.55), (cx + r * 0.85, cy + r * 0.1),
               (cx, cy + r), (cx - r * 0.85, cy + r * 0.1), (cx - r * 0.85, cy - r * 0.55)]
        draw.polygon(pts, outline=color, width=6)
        draw.line([cx - 22, cy + 2, cx - 6, cy + 18, cx + 26, cy - 20], fill=color, width=7)
    elif kind == "rocket":
        draw.polygon([(cx, cy - r), (cx + r * 0.55, cy + r * 0.4), (cx - r * 0.55, cy + r * 0.4)], fill=color)
        draw.ellipse([cx - 14, cy - 18, cx + 14, cy + 10], fill=BG)
        draw.polygon([(cx - r * 0.55, cy + r * 0.4), (cx - r * 0.8, cy + r), (cx - r * 0.2, cy + r * 0.55)], fill=color)
        draw.polygon([(cx + r * 0.55, cy + r * 0.4), (cx + r * 0.8, cy + r), (cx + r * 0.2, cy + r * 0.55)], fill=color)
        draw.polygon([(cx - 10, cy + r * 0.55), (cx + 10, cy + r * 0.55), (cx, cy + r + 16)], fill=GOLD)


def wrap(draw, text, fnt, max_w):
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/output/entry.png")
    args = ap.parse_args()

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header
    d.rectangle([0, 0, W, 8], fill=GOLD)
    d.text((80, 48), "THE WORLD IN ONE IMAGE", font=font(FONT_BOLD, 34), fill=GOLD)
    d.text((80, 92), "26 NOVEMBER 2026", font=font(FONT_BOLD, 96), fill=WHITE)
    d.text((80, 200), "THURSDAY  •  SIX STORIES THAT DEFINED THE DAY",
           font=font(FONT_REG, 30), fill=MUTED)
    d.text((1180, 60), "MAKE.FUN", font=font(FONT_BOLD, 32), fill=MUTED)
    d.text((1180, 104), "$100 BOUNTY", font=font(FONT_BOLD, 28), fill=MUTED)

    # 3 x 2 grid
    gx, gy = 80, 270
    cw, ch, gap = 466, 410, 36
    f_kicker = font(FONT_BOLD, 24)
    f_title = font(FONT_BOLD, 36)
    f_cap = font(FONT_REG, 26)

    for i, s in enumerate(STORIES):
        col, row = i % 3, i // 3
        x = gx + col * (cw + gap)
        y = gy + row * (ch + gap)
        accent = ACCENTS[i]
        rounded(d, [x, y, x + cw, y + ch], 24, PANEL, outline=PANEL_EDGE, width=2)
        d.rectangle([x, y, x + cw, y + 10], fill=accent)
        # icon in a circle
        cx, cy, r = x + 78, y + 92, 52
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(11, 18, 32), outline=accent, width=3)
        draw_icon(d, s["icon"], cx, cy, 34, accent)
        # kicker
        d.text((x + 152, y + 70), s["kicker"], font=f_kicker, fill=accent)
        # title, wrapped to panel width, up to 3 lines
        ty = y + 178
        for line in wrap(d, s["title"].replace("\n", " "), f_title, cw - 64)[:3]:
            d.text((x + 32, ty), line, font=f_title, fill=WHITE)
            ty += 44
        # caption, wrapped, 2 lines max
        cy2 = ty + 14
        for line in wrap(d, s["caption"], f_cap, cw - 64)[:2]:
            d.text((x + 32, cy2), line, font=f_cap, fill=MUTED)
            cy2 += 36

    # Footer
    d.text((80, H - 52), "Sources: world news of 26 November 2026  •  HORMUZ  •  TARIFFS  •  MARKETS  •  COLOMBIA  •  HONG KONG  •  MERCURY",
           font=font(FONT_REG, 22), fill=MUTED)

    out = args.out
    os.makedirs(os.path.dirname(os.path.abspath(out)) or ".", exist_ok=True)
    img.save(out, "PNG")
    print(f"Wrote {out} ({W}x{H})")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render the Nov 26, 2026 world-news front page ("WireFront" layout).

Wire-service aesthetic: top kicker line, double rule, serif nameplate,
dark lead banner with a drawn blast motif, a 2x3 grid of dispatches each
with a small drawn icon, and a source footer. 1024x1024, deterministic.
"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = 1024
H = 1024
MARGIN = 40
CW = W - 2 * MARGIN  # 944

PAPER = (246, 241, 231)
INK = (25, 25, 25)
GREY = (107, 107, 107)
FAINT = (201, 194, 178)
CRIMSON = (158, 27, 27)
CHARCOAL = (35, 35, 35)
IVORY = (246, 241, 231)
AMBER = (232, 163, 61)
BLAZE = (232, 114, 42)
EMBER = (242, 193, 78)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            if fnt.getlength(trial) <= max_width:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    """Draw lines top-anchored at (x, y); return y just below the last line."""
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def draw_blast(draw, cx, cy, r):
    """Geometric blast motif: radiating spokes + layered flame."""
    for i in range(12):
        ang = math.radians(i * 30)
        long_spoke = (i % 2 == 0)
        r2 = r if long_spoke else r * 0.62
        x2 = cx + r2 * math.cos(ang)
        y2 = cy + r2 * math.sin(ang)
        x1 = cx + r * 0.28 * math.cos(ang)
        y1 = cy + r * 0.28 * math.sin(ang)
        draw.line([(x1, y1), (x2, y2)], fill=AMBER, width=5)
    # outer flame (teardrop polygon)
    outer = [
        (cx, cy - r * 0.62),
        (cx + r * 0.34, cy - r * 0.05),
        (cx + r * 0.30, cy + r * 0.42),
        (cx, cy + r * 0.55),
        (cx - r * 0.30, cy + r * 0.42),
        (cx - r * 0.34, cy - r * 0.05),
    ]
    draw.polygon(outer, fill=BLAZE)
    # inner flame
    inner = [
        (cx, cy - r * 0.30),
        (cx + r * 0.18, cy + r * 0.02),
        (cx + r * 0.15, cy + r * 0.32),
        (cx, cy + r * 0.38),
        (cx - r * 0.15, cy + r * 0.32),
        (cx - r * 0.18, cy + r * 0.02),
    ]
    draw.polygon(inner, fill=EMBER)


def draw_mark(draw, kind, x, y, s, color):
    """Small 40x40 line-art icon for a dispatch cell."""
    if kind == "flame":
        pts = [
            (x + s * 0.50, y + s * 0.02),
            (x + s * 0.86, y + s * 0.42),
            (x + s * 0.78, y + s * 0.86),
            (x + s * 0.50, y + s * 0.98),
            (x + s * 0.22, y + s * 0.86),
            (x + s * 0.14, y + s * 0.42),
        ]
        draw.polygon(pts, outline=color, width=3)
        draw.polygon(
            [
                (x + s * 0.50, y + s * 0.34),
                (x + s * 0.68, y + s * 0.58),
                (x + s * 0.62, y + s * 0.82),
                (x + s * 0.50, y + s * 0.88),
                (x + s * 0.38, y + s * 0.82),
                (x + s * 0.32, y + s * 0.58),
            ],
            fill=color,
        )
    elif kind == "envelope":
        draw.rectangle([x + 2, y + s * 0.22, x + s - 2, y + s * 0.82], outline=color, width=3)
        draw.line([(x + 2, y + s * 0.22), (x + s * 0.50, y + s * 0.58)], fill=color, width=3)
        draw.line([(x + s - 2, y + s * 0.22), (x + s * 0.50, y + s * 0.58)], fill=color, width=3)
    elif kind == "atom":
        draw.ellipse([x + 2, y + s * 0.28, x + s - 2, y + s * 0.72], outline=color, width=3)
        draw.ellipse([x + s * 0.28, y + 2, x + s * 0.72, y + s - 2], outline=color, width=3)
        draw.ellipse(
            [x + s * 0.42, y + s * 0.42, x + s * 0.58, y + s * 0.58], fill=color
        )
    elif kind == "missile":
        # vertical rocket: nose, body, fins, flame
        draw.polygon(
            [
                (x + s * 0.50, y + 2),
                (x + s * 0.68, y + s * 0.30),
                (x + s * 0.32, y + s * 0.30),
            ],
            fill=color,
        )
        draw.rectangle(
            [x + s * 0.32, y + s * 0.30, x + s * 0.68, y + s * 0.66],
            outline=color,
            width=3,
        )
        draw.polygon(
            [
                (x + s * 0.32, y + s * 0.52),
                (x + s * 0.10, y + s * 0.72),
                (x + s * 0.32, y + s * 0.66),
            ],
            fill=color,
        )
        draw.polygon(
            [
                (x + s * 0.68, y + s * 0.52),
                (x + s * 0.90, y + s * 0.72),
                (x + s * 0.68, y + s * 0.66),
            ],
            fill=color,
        )
        draw.polygon(
            [
                (x + s * 0.50, y + s * 0.98),
                (x + s * 0.62, y + s * 0.70),
                (x + s * 0.38, y + s * 0.70),
            ],
            fill=AMBER,
        )
    elif kind == "bars":
        heights = [0.42, 0.66, 0.92]
        bw = s * 0.20
        for i, hh in enumerate(heights):
            bx = x + 4 + i * (bw + 6)
            draw.rectangle(
                [bx, y + s - s * hh, bx + bw, y + s - 2], fill=color
            )
        draw.line([(x + 2, y + s - 2), (x + s - 2, y + s - 2)], fill=color, width=3)
    elif kind == "gavel":
        # head: rotated square; handle: diagonal line
        cx, cy = x + s * 0.34, y + s * 0.30
        r = s * 0.22
        draw.polygon(
            [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)],
            outline=color,
            width=3,
        )
        draw.line(
            [(x + s * 0.44, y + s * 0.44), (x + s * 0.86, y + s * 0.86)],
            fill=color,
            width=4,
        )
        draw.line(
            [(x + s * 0.10, y + s * 0.86), (x + s * 0.34, y + s * 0.62)],
            fill=color,
            width=3,
        )
    else:
        draw.rectangle([x, y, x + s, y + s], outline=color, width=3)


class WireFront:
    """One 1024x1024 front page."""

    def __init__(self, data):
        self.data = data
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)

    def top_line(self):
        f_left = font(SANS_B, 18)
        f_right = font(SANS, 18)
        y = 28
        self.d.text((MARGIN, y), "THE WORLD  —  WIRE EDITION", font=f_left, fill=INK)
        date = self.data["date"]
        self.d.text(
            (W - MARGIN - f_right.getlength(date), y), date, font=f_right, fill=GREY
        )
        self.d.line([(MARGIN, 56), (W - MARGIN, 56)], fill=INK, width=2)
        self.d.line([(MARGIN, 60), (W - MARGIN, 60)], fill=INK, width=1)

    def nameplate(self):
        f_name = font(SERIF_B, 88)
        name = self.data["masthead"]
        tw = f_name.getlength(name)
        self.d.text(((W - tw) / 2, 68), name, font=f_name, fill=INK)
        self.d.line([(MARGIN, 168), (W - MARGIN, 168)], fill=CRIMSON, width=2)

    def lead_banner(self):
        d = self.d
        x0, y0, x1, y1 = MARGIN, 180, W - MARGIN, 420
        d.rectangle([x0, y0, x1, y1], fill=CHARCOAL)
        draw_blast(d, x0 + 100, (y0 + y1) // 2, 62)
        lead = self.data["lead"]
        tx = x0 + 216
        tw = x1 - 24 - tx
        y = y0 + 18
        f_kick = font(SANS_B, 20)
        d.text((tx, y), lead["kicker"], font=f_kick, fill=AMBER)
        y += 32
        f_head = font(SERIF_B, 48)
        lines = wrap(lead["headline"], f_head, tw)
        assert len(lines) <= 2, f"lead headline wrapped to {len(lines)} lines"
        y = text_block(d, tx, y, lines, f_head, IVORY, 56)
        y += 6
        f_deck = font(SANS, 22)
        dlines = wrap(lead["deck"], f_deck, tw)
        assert len(dlines) <= 2, f"lead deck wrapped to {len(dlines)} lines"
        y = text_block(d, tx, y, dlines, f_deck, (220, 214, 200), 28)
        assert y <= y1 - 12, f"lead banner overflow: bottom {y} > {y1 - 12}"

    def dispatch_grid(self):
        d = self.d
        items = self.data["dispatches"]
        assert len(items) == 6, f"expected 6 dispatches, got {len(items)}"
        gx0, gy0 = MARGIN, 434
        col_w = 301
        gutter = 20
        row_h = 254
        row_gap = 12
        # separators
        for cx in (gx0 + col_w + gutter // 2, gx0 + 2 * col_w + gutter + gutter // 2):
            d.line([(cx, gy0), (cx, gy0 + 2 * row_h + row_gap)], fill=FAINT, width=1)
        d.line(
            [(gx0, gy0 + row_h + row_gap // 2), (W - MARGIN, gy0 + row_h + row_gap // 2)],
            fill=FAINT,
            width=1,
        )
        f_kick = font(SANS_B, 17)
        f_head = font(SERIF_B, 28)
        f_deck = font(SANS, 18)
        for idx, item in enumerate(items):
            row, col = divmod(idx, 3)
            x = gx0 + col * (col_w + gutter)
            y = gy0 + row * (row_h + row_gap)
            cell_bottom = y + row_h
            draw_mark(d, item["icon"], x + 14, y + 8, 40, CRIMSON)
            d.text((x + 64, y + 18), item["kicker"], font=f_kick, fill=CRIMSON)
            hy = y + 62
            hlines = wrap(item["headline"], f_head, col_w - 28)
            assert len(hlines) <= 3, f"dispatch {idx} headline {len(hlines)} lines"
            hy = text_block(d, x + 14, hy, hlines, f_head, INK, 34)
            dy = hy + 6
            dlines = wrap(item["deck"], f_deck, col_w - 28)
            assert len(dlines) <= 3, f"dispatch {idx} deck {len(dlines)} lines"
            dy = text_block(d, x + 14, dy, dlines, f_deck, GREY, 23)
            assert dy <= cell_bottom - 4, f"dispatch {idx} overflow: {dy} > {cell_bottom - 4}"

    def footer(self):
        d = self.d
        d.line([(MARGIN, 966), (W - MARGIN, 966)], fill=INK, width=1)
        f_src = font(SANS, 15)
        src = self.data["sources"]
        tw = f_src.getlength(src)
        assert tw <= CW, f"source line too wide: {tw}"
        d.text(((W - tw) / 2, 976), src, font=f_src, fill=GREY)

    def compose(self):
        self.top_line()
        self.nameplate()
        self.lead_banner()
        self.dispatch_grid()
        self.footer()
        return self.img


def main():
    with open(os.path.join(HERE, "news.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    page = WireFront(data).compose()
    out = os.path.join(HERE, "entry.png")
    page.save(out, format="PNG")
    print("wrote", out, page.size)


if __name__ == "__main__":
    main()

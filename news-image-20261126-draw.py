#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261126 (pure Python stdlib only).

Generates a 1024x1024 newspaper-style poster summing up Thursday
26 November 2026: six verified stories, each with a pictogram, a
headline and a one-line detail. No third-party libraries: the PNG is
encoded by hand (zlib + struct) and the text is rendered with an
embedded 5x7 bitmap font scaled up, so every letter is crisp.

Run:  python3 news-image-20261126-draw.py [output-path]
Default output is entry.png next to this script.
"""

import math
import os
import struct
import sys
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (245, 241, 230)
INK = (26, 26, 26)
NAVY = (16, 35, 63)
GOLD = (217, 164, 65)
LIGHT = (201, 210, 222)
GREY = (68, 68, 68)
WHITE = (255, 255, 255)
CREAM = (255, 248, 231)
ORANGE = (255, 159, 28)
YELLOW = (255, 211, 77)
SMOKE = (232, 224, 208)

ACCENTS = [
    (179, 64, 42),    # 1 Ras Tanura - brick red
    (15, 107, 122),   # 2 Hormuz - sea teal
    (122, 31, 43),    # 3 Gaza - dark red
    (46, 74, 107),    # 4 Ukraine - steel blue
    (31, 58, 95),     # 5 Space - deep blue
    (183, 121, 31),   # 6 India - saffron
]

# ---------------------------------------------------------------- 5x7 font
# Each glyph is 7 rows of 5 bits, '#' = ink. Uppercase, digits and the
# punctuation used by the poster text.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '|': ("00100", "00100", "00100", "00100", "00100", "00100", "00100"),
}


def text_width(text, scale):
    """Pixel width of text at the given scale (6 units per char)."""
    return len(text) * 6 * scale - scale


def wrap_text(text, max_width, scale):
    """Greedy word wrap; returns list of lines fitting max_width."""
    unit = 6 * scale
    words = text.split(' ')
    lines, cur = [], ''
    for word in words:
        trial = word if not cur else cur + ' ' + word
        if len(trial) * unit - scale <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * w * h)

    def _set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self._set(xx, yy, color)

    def circle(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(r * r - dy * dy, 0)))
            for xx in range(cx - dx, cx + dx + 1):
                self._set(xx, cy + dy, color)

    def ring(self, cx, cy, r, thick, color, bg):
        self.circle(cx, cy, r, color)
        self.circle(cx, cy, r - thick, bg)

    def line(self, x0, y0, x1, y1, color, thick=1):
        steps = max(abs(x1 - x0), abs(y1 - y0), 1)
        r = max(thick // 2, 1)
        for i in range(steps + 1):
            x = round(x0 + (x1 - x0) * i / steps)
            y = round(y0 + (y1 - y0) * i / steps)
            self.circle(x, y, r, color)

    def polyline(self, points, color, thick=1):
        for (x0, y0), (x1, y1) in zip(points, points[1:]):
            self.line(x0, y0, x1, y1, color, thick)

    def polygon(self, points, color):
        # scanline fill
        ys = [p[1] for p in points]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            n = len(points)
            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    t = (y - y0) / (y1 - y0)
                    xs.append(x0 + t * (x1 - x0))
            xs.sort()
            for j in range(0, len(xs) - 1, 2):
                for x in range(int(math.ceil(xs[j])), int(xs[j + 1]) + 1):
                    self._set(x, y, color)

    def text(self, x, y, s, scale, color):
        for ch in s:
            glyph = FONT.get(ch)
            if glyph is None:
                raise ValueError('no glyph for %r' % ch)
            for row, bits in enumerate(glyph):
                for col, b in enumerate(bits):
                    if b == '1':
                        self.rect(x + col * scale, y + row * scale,
                                  scale, scale, color)
            x += 6 * scale

    def text_center(self, y, s, scale, color):
        self.text((self.w - text_width(s, scale)) // 2, y, s, scale, color)


def png_bytes(canvas):
    def chunk(kind, data):
        out = struct.pack('>I', len(data)) + kind + data
        return out + struct.pack('>I', zlib.crc32(kind + data) & 0xFFFFFFFF)

    ihdr = struct.pack('>IIBBBBB', canvas.w, canvas.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    for y in range(canvas.h):
        raw.append(0)  # filter: none
        raw += canvas.px[y * canvas.w * 3:(y + 1) * canvas.w * 3]
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
            + chunk(b'IDAT', zlib.compress(bytes(raw), 9))
            + chunk(b'IEND', b''))


# ---------------------------------------------------------------- pictograms
def icon_refinery(c, cx, cy, accent):
    c.rect(cx - 44, cy + 38, 88, 6, CREAM)                    # ground
    c.rect(cx - 40, cy - 10, 12, 48, CREAM)                  # chimneys
    c.rect(cx - 24, cy - 22, 12, 60, CREAM)
    c.rect(cx - 8, cy - 4, 12, 42, CREAM)
    c.polygon([(cx - 20, cy - 22), (cx - 12, cy - 22), (cx - 16, cy - 46)],
              YELLOW)                                         # flame
    c.circle(cx + 24, cy - 30, 9, SMOKE)                     # smoke
    c.circle(cx + 36, cy - 42, 11, SMOKE)
    c.circle(cx + 16, cy - 48, 7, SMOKE)
    c.circle(cx + 30, cy + 20, 15, CREAM)                    # tank
    c.rect(cx + 15, cy + 16, 30, 5, accent)


def icon_tanker(c, cx, cy, accent):
    c.circle(cx - 6, cy - 36, 13, ORANGE)                    # blast
    c.circle(cx - 6, cy - 36, 7, YELLOW)
    c.polygon([(cx - 46, cy + 6), (cx + 46, cy + 6), (cx + 36, cy + 30),
               (cx - 36, cy + 30)], CREAM)                   # hull
    c.rect(cx - 30, cy - 8, 60, 14, CREAM)                   # deck
    c.rect(cx + 18, cy - 26, 16, 18, CREAM)                  # bridge
    c.rect(cx - 46, cy + 40, 92, 4, CREAM)                   # waves
    c.rect(cx - 30, cy + 50, 60, 4, CREAM)


def icon_gaza(c, cx, cy, accent):
    c.rect(cx - 34, cy - 30, 68, 86, CREAM)                  # building
    for r in range(4):
        for col in range(3):
            c.rect(cx - 24 + col * 22, cy - 18 + r * 20, 9, 11, accent)
    c.polyline([(cx + 12, cy - 30), (cx + 2, cy - 8), (cx + 14, cy + 12),
                (cx + 0, cy + 34), (cx + 10, cy + 56)], accent, 4)  # crack
    c.circle(cx - 20, cy - 44, 9, SMOKE)                     # smoke
    c.circle(cx + 4, cy - 52, 11, SMOKE)
    c.polygon([(cx - 40, cy + 56), (cx - 28, cy + 56), (cx - 34, cy + 42)],
              CREAM)                                          # rubble
    c.polygon([(cx + 22, cy + 56), (cx + 38, cy + 56), (cx + 30, cy + 44)],
              CREAM)


def icon_drone(c, cx, cy, accent):
    c.circle(cx - 24, cy + 22, 16, CREAM)                    # tanks
    c.circle(cx + 24, cy + 22, 16, CREAM)
    c.rect(cx - 40, cy + 34, 80, 6, CREAM)
    c.polygon([(cx - 6, cy + 20), (cx + 6, cy + 20), (cx, cy + 2)],
              ORANGE)                                         # flame
    c.rect(cx - 9, cy - 48, 18, 9, CREAM)                    # drone body
    for sx in (-1, 1):
        for sy in (-1, 1):
            c.line(cx, cy - 44, cx + sx * 30, cy - 44 + sy * 12, CREAM, 3)
            c.circle(cx + sx * 30, cy - 44 + sy * 12, 6, YELLOW)


def icon_rocket(c, cx, cy, accent):
    for sx, sy in ((-40, -52), (38, -40), (-34, 44), (42, 30), (0, -58)):
        c.rect(cx + sx - 2, cy + sy, 4, 4, GOLD)              # stars
        c.rect(cx + sx, cy + sy - 2, 4, 4, GOLD)
    c.ring(cx, cy, 54, 3, GOLD, accent)                      # orbit ring
    c.polygon([(cx - 10, cy - 30), (cx + 10, cy - 30), (cx, cy - 52)],
              GOLD)                                           # nose
    c.rect(cx - 10, cy - 30, 20, 56, CREAM)                  # body
    c.polygon([(cx - 10, cy + 14), (cx - 24, cy + 32), (cx - 10, cy + 26)],
              CREAM)                                          # fins
    c.polygon([(cx + 10, cy + 14), (cx + 24, cy + 32), (cx + 10, cy + 26)],
              CREAM)
    c.circle(cx, cy - 8, 6, accent)                          # window
    c.polygon([(cx - 8, cy + 26), (cx + 8, cy + 26), (cx, cy + 48)],
              ORANGE)                                         # flame
    c.polygon([(cx - 4, cy + 26), (cx + 4, cy + 26), (cx, cy + 40)], YELLOW)


def icon_chakra(c, cx, cy, accent):
    cy -= 8
    c.ring(cx, cy, 36, 4, CREAM, accent)                     # wheel
    for k in range(24):                                       # spokes
        a = math.pi * 2 * k / 24
        c.line(cx, cy, cx + round(32 * math.cos(a)),
               cy + round(32 * math.sin(a)), CREAM, 2)
    c.circle(cx, cy, 7, CREAM)                               # hub
    c.rect(cx - 6, cy + 48, 12, 22, CREAM)                   # candle
    c.polygon([(cx - 5, cy + 48), (cx + 5, cy + 48), (cx, cy + 34)],
              YELLOW)                                         # flame


ICONS = [icon_refinery, icon_tanker, icon_gaza,
         icon_drone, icon_rocket, icon_chakra]

# ---------------------------------------------------------------- stories
# (kicker, headline, detail) - all verified from news sources dated
# 25-26 Nov 2026; see README.md for the source of each story.
STORIES = [
    ("MIDDLE EAST / ENERGY",
     "HOUTHIS CLAIM STRIKE ON RAS TANURA",
     "SAUDI ARABIA'S LARGEST REFINERY; SMOKE SEEN BY SATELLITE; OIL UP"),
    ("STRAIT OF HORMUZ",
     "TWO TANKERS HIT MINES IN HORMUZ",
     "IRAN SAYS THE SHIPS CAUGHT FIRE ON AN UNAUTHORISED ROUTE"),
    ("GAZA / CEASEFIRE",
     "ISRAEL KILLS HAMAS SECURITY CHIEF",
     "MOHAMMAD ABUELOUF, HIS WIFE AND TWO CHILDREN KILLED IN GAZA"),
    ("UKRAINE / RUSSIA",
     "UKRAINE STRIKES RUSSIAN REFINERIES",
     "PUTIN: RETALIATION IS INEVITABLE; REFINING DOWN 45% SINCE OCT."),
    ("SPACE / CHINA",
     "PAKISTAN'S FIRST ASTRONAUT IN ORBIT",
     "SHENZHOU-24 DOCKS AT TIANGONG; FIRST FOREIGN VISITOR"),
    ("INDIA",
     "INDIA MARKS CONSTITUTION DAY",
     "18 YEARS SINCE THE 26/11 MUMBAI ATTACKS; 166 LIVES REMEMBERED"),
]


def draw_panel(c, x, y, w, h, accent, icon, kicker, headline, detail):
    c.rect(x, y, w, h, WHITE)
    c.rect(x, y, w, 10, accent)                              # top strip
    c.rect(x, y + 10, 112, h - 10, accent)                   # icon column
    icon(c, x + 56, y + 130, accent)
    tx = x + 128
    c.text(tx, y + 30, kicker, 2, accent)
    lines = wrap_text(headline, w - 144, 3)
    ly = y + 58
    for ln in lines[:3]:
        c.text(tx, ly, ln, 3, INK)
        ly += 27
    dlines = wrap_text(detail, w - 144, 2)
    ly = y + 58 + 3 * 27 + 12
    for ln in dlines[:3]:
        c.text(tx, ly, ln, 2, GREY)
        ly += 19
    # thin frame
    c.rect(x, y, w, 2, (216, 210, 196))
    c.rect(x, y + h - 2, w, 2, (216, 210, 196))
    c.rect(x, y, 2, h, (216, 210, 196))
    c.rect(x + w - 2, y, 2, h, (216, 210, 196))


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'entry.png')
    c = Canvas(W, H, PAPER)

    # header
    c.rect(0, 0, W, 168, NAVY)
    c.text_center(28, "THURSDAY, 26 NOVEMBER 2026", 5, WHITE)
    c.rect((W - 220) // 2, 84, 220, 4, GOLD)
    c.text_center(100, "THE WORLD IN ONE IMAGE", 3, GOLD)
    c.text_center(132, "SIX STORIES THAT DEFINED THE DAY", 2, LIGHT)

    # six panels, 2 columns x 3 rows
    pw, ph, gap = 480, 250, 16
    x0, y0 = 24, 184
    for i, (kicker, headline, detail) in enumerate(STORIES):
        x = x0 + (i % 2) * (pw + gap)
        y = y0 + (i // 2) * (ph + gap)
        draw_panel(c, x, y, pw, ph, ACCENTS[i], ICONS[i],
                   kicker, headline, detail)

    # footer
    c.text_center(986, "SOURCES: REUTERS | XINHUA | NATURE | OBSERVER VOICE",
                  2, GREY)

    data = png_bytes(c)
    with open(out, 'wb') as f:
        f.write(data)
    print('wrote %s (%d bytes)' % (out, len(data)))


if __name__ == '__main__':
    main()

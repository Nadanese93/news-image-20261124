#!/usr/bin/env python3
"""News-image entry for make.fun news-image-20261124.

Draws a 1024x1024 newspaper front page summing up Tuesday 24 November
2026 world news, using only the Python standard library. All artwork is
drawn programmatically; text uses a 5x7 bitmap font defined below.
Deterministic: no randomness, no timestamps, no network.
"""
import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (246, 241, 229)
INK = (24, 24, 28)
NAVY = (24, 48, 96)
RED = (178, 34, 28)
GREY = (110, 110, 108)
DARKGREY = (70, 70, 72)
SEA = (38, 84, 128)
SKY = (178, 208, 224)
SAND = (196, 168, 120)
ORANGE = (232, 110, 24)
YELLOW = (240, 196, 40)
GREEN = (46, 120, 70)
WHITE = (255, 255, 255)
LIGHTGREY = (210, 208, 200)

# 5x7 bitmap font: each glyph is 7 rows of 5 characters, '#' = ink.
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
    '.': ("00000", "00000", "00000", "00000", "00000", "00000", "01100"),
    ',': ("00000", "00000", "00000", "00000", "00000", "00100", "01000"),
    '-': ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    "'": ("00100", "00100", "00000", "00000", "00000", "00000", "00000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    ':': ("00000", "00100", "00000", "00000", "00000", "00100", "00000"),
    ';': ("00000", "00100", "00000", "00000", "00000", "00100", "01000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '$': ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '*': ("00000", "00100", "10101", "01110", "10101", "00100", "00000"),
    # bullet, drawn as a solid block in the middle rows
    '\u2022': ("00000", "00000", "01110", "01110", "00000", "00000", "00000"),
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * w * h)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, color)

    def hline(self, x, y, w, color, thick=1):
        self.rect(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.rect(x, y, thick, h, color)

    def circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, color)

    def triangle(self, x0, y0, x1, y1, x2, y2, color):
        # filled triangle via scanline interpolation
        xs = sorted([(x0, y0), (x1, y1), (x2, y2)], key=lambda p: p[1])
        (ax, ay), (bx, by), (cx, cy) = xs
        if ay == cy:
            return
        for y in range(ay, cy + 1):
            if y < by:
                t1 = (y - ay) / (by - ay) if by != ay else 0.0
                xa = ax + (bx - ax) * t1
            else:
                t1 = (y - by) / (cy - by) if cy != by else 0.0
                xa = bx + (cx - bx) * t1
            t2 = (y - ay) / (cy - ay) if cy != ay else 0.0
            xb = ax + (cx - ax) * t2
            lo, hi = int(min(xa, xb)), int(max(xa, xb))
            for x in range(lo, hi + 1):
                self.set(x, y, color)

    def text(self, x, y, s, scale, color):
        cx = x
        for ch in s:
            glyph = FONT.get(ch, FONT[' '])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == '1':
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, color)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale):
        return len(s) * 6 * scale - scale if s else 0

    def text_center(self, y, s, scale, color):
        w = self.text_w(s, scale)
        self.text((self.w - w) // 2, y, s, scale, color)

    def wrap(self, s, scale, max_w):
        """Greedy word wrap; returns list of lines that fit max_w."""
        words = s.split(' ')
        lines = []
        cur = ''
        for word in words:
            trial = word if not cur else cur + ' ' + word
            if self.text_w(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines


def draw_hero_scene(c, x, y, w, h):
    """Sinking warship off the Benghazi coast."""
    # sky
    c.rect(x, y, w, h // 2, SKY)
    # pale sun
    c.circle(x + w - 110, y + 34, 26, (244, 214, 130))
    # distant coastline strip
    c.rect(x, y + h // 2 - 16, w, 16, SAND)
    c.text(x + 14, y + h // 2 - 14, "BENGHAZI", 2, INK)
    # sea
    c.rect(x, y + h // 2, w, h - h // 2, SEA)
    # wave dashes
    for wy in (y + h // 2 + 22, y + h // 2 + 52, y + h - 18):
        for wx in range(x + 20, x + w - 20, 64):
            c.rect(wx, wy, 34, 3, (150, 190, 220))
    # listing warship: hull sloping down to the right (sinking bow-first)
    hx, hy = x + 300, y + 78
    # hull as a thick slanted band, bow (right) lower and awash
    for i in range(0, 300, 2):
        drop = i * 36 // 300
        c.rect(hx + i, hy + drop, 2, 30, DARKGREY)
    # deck / superstructure (tilted with the hull)
    c.rect(hx + 50, hy - 22, 80, 22, GREY)
    c.rect(hx + 150, hy - 12, 55, 14, GREY)
    # mast leaning
    for i in range(0, 36):
        c.set(hx + 86 + i // 3, hy - 22 - i, DARKGREY)
        c.set(hx + 87 + i // 3, hy - 22 - i, DARKGREY)
    # funnel
    c.rect(hx + 190, hy - 26, 20, 26, INK)
    # orange fire at the bow / midship
    c.triangle(hx + 230, hy + 8, hx + 262, hy - 30, hx + 294, hy + 8, ORANGE)
    c.triangle(hx + 248, hy + 8, hx + 268, hy - 14, hx + 288, hy + 8, YELLOW)
    c.triangle(hx + 100, hy + 2, hx + 122, hy - 22, hx + 144, hy + 2, ORANGE)
    # grey smoke plumes rising from the fire, kept inside the scene
    c.circle(hx + 262, hy - 40, 14, GREY)
    c.circle(hx + 248, hy - 52, 18, LIGHTGREY)
    c.circle(hx + 280, hy - 58, 12, GREY)
    c.circle(hx + 122, hy - 30, 11, GREY)
    # small drone boats approaching from the left
    for dx, dy in ((x + 60, y + h // 2 + 30), (x + 150, y + h // 2 + 58),
                   (x + 90, y + h - 34)):
        c.rect(dx, dy, 34, 8, INK)
        c.rect(dx + 12, dy - 8, 10, 8, INK)
        c.rect(dx - 22, dy + 2, 20, 2, WHITE)
    # falling helicopter silhouette near the stern
    hx2, hy2 = x + w - 170, y + 30
    c.rect(hx2, hy2, 44, 10, INK)
    c.rect(hx2 + 44, hy2 + 2, 26, 4, INK)
    c.rect(hx2 + 8, hy2 - 10, 4, 10, INK)
    c.hline(hx2 - 8, hy2 - 12, 60, INK, 3)


def draw_globe(c, x, y, w, h):
    cx, cy, r = x + w // 2, y + h // 2, 20
    c.circle(cx, cy, r, (90, 150, 200))
    c.circle(cx - 6, cy - 5, 8, GREEN)
    c.circle(cx + 8, cy + 6, 6, GREEN)
    c.circle(cx + 9, cy - 9, 4, GREEN)
    # sun
    c.circle(x + w - 22, y + 12, 8, YELLOW)
    # red slash: no deal
    c.hline(x + 14, y + h - 8, w - 28, RED, 4)


def draw_fire(c, x, y, w, h):
    # factory block
    c.rect(x + 24, y + 26, 140, h - 26, DARKGREY)
    c.rect(x + 24, y + 26, 140, 6, INK)
    # windows
    for wx in range(x + 36, x + 150, 28):
        c.rect(wx, y + 38, 12, 10, YELLOW)
    # chimney
    c.rect(x + 178, y + 8, 18, h - 8, GREY)
    # flames
    c.triangle(x + 50, y + 28, x + 72, y + 2, x + 94, y + 28, ORANGE)
    c.triangle(x + 86, y + 28, x + 104, y + 10, x + 122, y + 28, YELLOW)
    c.triangle(x + 182, y + 10, x + 190, y - 2, x + 198, y + 10, ORANGE)
    # smoke
    c.circle(x + 222, y + 6, 9, GREY)


def draw_gaza(c, x, y, w, h):
    # broken skyline
    heights = (34, 20, 40, 14, 30, 24, 36)
    bx = x + 20
    for ht in heights:
        c.rect(bx, y + h - 8 - ht, 28, ht, DARKGREY)
        bx += 34
    # warning triangle
    tx, ty = x + w - 66, y + 4
    c.triangle(tx, ty + 36, tx + 18, ty, tx + 36, ty + 36, YELLOW)
    c.rect(tx + 15, ty + 12, 5, 13, INK)
    c.rect(tx + 15, ty + 28, 5, 5, INK)


def draw_chess(c, x, y, w, h):
    # 4x4 board
    bx, by, sq = x + 20, y + 4, 12
    for r in range(4):
        for col in range(4):
            colr = INK if (r + col) % 2 == 0 else WHITE
            c.rect(bx + col * sq, by + r * sq, sq, sq, colr)
    # king piece (white) and pawn (black) standing on the board
    kx, ky = x + 130, y + 6
    c.rect(kx + 6, ky + 26, 22, 7, WHITE)
    c.rect(kx + 10, ky + 11, 15, 15, WHITE)
    c.circle(kx + 17, ky + 7, 7, WHITE)
    c.rect(kx + 15, ky - 2, 4, 7, YELLOW)
    c.rect(kx + 12, ky + 2, 11, 4, YELLOW)
    px, py = x + 190, y + 18
    c.rect(px + 5, py + 20, 20, 7, INK)
    c.rect(px + 10, py + 9, 11, 11, INK)
    c.circle(px + 15, py + 5, 6, INK)


def draw_tow(c, x, y, w, h):
    # damaged ship under tow
    sx, sy = x + 50, y + 28
    c.rect(sx, sy, 160, 16, DARKGREY)
    c.rect(sx + 18, sy - 14, 52, 14, GREY)
    c.rect(sx + 105, sy - 8, 26, 8, GREY)
    c.triangle(sx + 130, sy + 16, sx + 144, sy - 2, sx + 158, sy + 16, ORANGE)
    # tow line to the tug
    for i in range(0, 80):
        c.set(sx + 160 + i, sy + 10 + i // 6, INK)
    tx, ty = x + w - 120, y + 40
    c.rect(tx, ty, 40, 12, INK)
    c.rect(tx + 9, ty - 10, 18, 10, INK)
    # sea line
    c.hline(x + 10, y + h - 8, w - 20, SEA, 3)


def draw_panel(c, x, y, w, h, art, headline, deck, source):
    c.rect(x, y, w, h, WHITE)
    # border
    c.hline(x, y, w, INK, 2)
    c.hline(x, y + h - 2, w, INK, 2)
    c.vline(x, y, h, INK, 2)
    c.vline(x + w - 2, y, h, INK, 2)
    art(c, x + 8, y + 6, w - 16, 56)
    c.hline(x + 8, y + 66, w - 16, LIGHTGREY, 1)
    lines = c.wrap(headline, 5, w - 20)
    ty = y + 74
    for ln in lines:
        c.text(x + 10, ty, ln, 5, INK)
        ty += 36
    dlines = c.wrap(deck, 2, w - 20)
    for ln in dlines:
        c.text(x + 10, ty, ln, 2, INK)
        ty += 16
    c.text(x + 10, y + h - 20, source, 2, RED)


def build():
    c = Canvas(W, H, PAPER)
    mx = 24
    cw = W - 2 * mx  # 976

    # ---- masthead ----
    c.text_center(14, "THE WORLD", 12, INK)
    c.hline(mx, 108, cw, INK, 4)
    c.hline(mx, 116, cw, INK, 2)
    c.text_center(128, "TUESDAY, 24 NOVEMBER 2026", 2, NAVY)
    c.text_center(150, "THE DAY'S WORLD NEWS IN ONE PICTURE", 2, INK)
    c.hline(mx, 172, cw, INK, 2)

    # ---- hero ----
    c.text(mx, 186, "WAR AT SEA - BENGHAZI, LIBYA", 2, RED)
    c.text(mx, 212, "UKRAINE SINKS RUSSIAN", 5, INK)
    c.text(mx, 252, "WARSHIP OFF LIBYA", 5, INK)
    c.text(mx, 300, "SEVEN SEA DRONES HIT THE CORVETTE MERKURY AND THE", 2, INK)
    c.text(mx, 319, "CARGO SHIP ANGARA, KYIV SAYS. A KA-27 HELICOPTER WAS DESTROYED.", 2, INK)
    draw_hero_scene(c, mx, 344, cw, 148)
    c.text(mx, 500, "SOURCES: CNN \u2022 THE WALL STREET JOURNAL \u2022 REUTERS \u2022 AP", 2, GREY)
    c.hline(mx, 522, cw, INK, 3)

    # ---- panels ----
    gap = 12
    pw3 = (cw - 2 * gap) // 3  # 317
    row1_y, row1_h = 534, 200
    row2_y, row2_h = 746, 200
    draw_panel(c, mx, row1_y, pw3, row1_h, draw_globe,
               "COP31 COLLAPSES",
               "ANTALYA TALKS END WITH NO FOSSIL-FUEL DEAL.",
               "BBC \u2022 CNN")
    draw_panel(c, mx + pw3 + gap, row1_y, pw3, row1_h, draw_fire,
               "24 DEAD IN FIRE",
               "CANDY FACTORY BLAZE IN BANTEN; 30 STILL MISSING",
               "REUTERS")
    draw_panel(c, mx + 2 * (pw3 + gap), row1_y, pw3, row1_h, draw_gaza,
               "GAZA TOXIC WASTELAND",
               "OXFAM: CONTAMINATION ACROSS 99% OF GAZA.",
               "OXFAM \u2022 CNN")
    pw2 = (cw - gap) // 2  # 482
    draw_panel(c, mx, row2_y, pw2, row2_h, draw_chess,
               "CHESS CROWN ON THE LINE",
               "GUKESH DEFENDS HIS TITLE AGAINST SINDAROV; GAME 1 TODAY IN GENEVA.",
               "CHESS.COM \u2022 FIDE")
    draw_panel(c, mx + pw2 + gap, row2_y, pw2, row2_h, draw_tow,
               "HIT SHIP REACHES PORT",
               "SPARTA II, STRUCK BY DRONES IN THE GULF, ARRIVES UNDER TOW.",
               "REUTERS")

    # ---- footer ----
    c.hline(mx, 956, cw, INK, 2)
    c.text_center(966, "ALL STORIES VERIFIED AGAINST THEIR OUTLETS", 2, INK)
    c.text_center(984, "CNN \u2022 BBC \u2022 REUTERS \u2022 OXFAM \u2022 CHESS.COM", 2, NAVY)
    return c


def write_png(c, path):
    raw = bytearray()
    stride = W * 3
    for y in range(H):
        raw.append(0)  # filter: none
        raw += c.px[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", comp)
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    os.chmod(path, 0o644)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    canvas = build()
    write_png(canvas, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()

"""Sum up 19 November 2026 in one image.

A pure-stdlib Python program. It draws a newspaper front page for
Thursday 19 November 2026 and writes it, deterministically, to
/output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png outside the grader).

No network, no randomness, no time, no external files: the same run
always writes the same bytes.

Stories, all reported on 19 November 2026:
  * Trump, Xi and Putin meet in Shenzhen and issue a four-point
    Declaration toward Peace, with no major deal on Ukraine.
  * The International Court of Justice rules 9-6 that Myanmar
    committed genocide against the Rohingya, in Gambia v. Myanmar.
  * COP31 ministers in Antalya try to unblock a final climate text.
  * The Gulf crisis widens around the Strait of Hormuz, and the IEA
    calls it the greatest threat ever seen to energy security.
  * Ukraine strikes the Crimea Bridge again; the EU proposes a
    45 billion loan for Ukraine in 2027.
  * Israeli forces cross the ceasefire line in central Gaza.
Also in the ticker: the Anthropic IPO, a record Van Gogh sale,
unrest in Bangladesh, Mongolia's president resigning, and the US
Senate rejecting an Iran war-powers resolution 51-48.
"""

import os
import struct
import zlib
from pathlib import Path

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 33, 61)
RED = (193, 39, 45)
GOLD = (217, 164, 65)
TEAL = (15, 118, 110)
BLUE = (37, 99, 235)
WHITE = (255, 255, 255)
GREY = (90, 96, 110)
LIGHT = (232, 226, 210)
DARK = (13, 22, 40)


def _chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(path, pixels):
    """Encode an RGB bytearray (W x H x 3) as a PNG, filter 0 rows."""
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        start = y * W * 3
        raw += pixels[start:start + W * 3]
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", ihdr)
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += _chunk(b"IEND", b"")
    Path(path).write_bytes(png)


class Canvas:
    def __init__(self):
        self.px = bytearray(PAPER * W * H)

    def set(self, x, y, colour):
        if 0 <= x < W and 0 <= y < H:
            i = (y * W + x) * 3
            self.px[i:i + 3] = bytes(colour)

    def rect(self, x, y, w, h, colour):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, colour)

    def disc(self, cx, cy, r, colour):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, colour)

    def ring(self, cx, cy, r, t, colour):
        for yy in range(cy - r - t, cy + r + t + 1):
            for xx in range(cx - r - t, cx + r + t + 1):
                d = ((xx - cx) ** 2 + (yy - cy) ** 2) ** 0.5
                if r - t <= d <= r + t:
                    self.set(xx, yy, colour)

    def line(self, x0, y0, x1, y1, t, colour):
        steps = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(steps + 1):
            x = round(x0 + (x1 - x0) * i / steps)
            y = round(y0 + (y1 - y0) * i / steps)
            self.disc(x, y, max(t // 2, 1), colour)

    def poly(self, points, colour):
        ys = [p[1] for p in points]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            for (x0, y0), (x1, y1) in zip(points, points[1:] + points[:1]):
                if y0 == y1:
                    continue
                if min(y0, y1) <= y < max(y0, y1):
                    xs.append(int(x0 + (y - y0) * (x1 - x0) / (y1 - y0)))
            xs.sort()
            for a, b in zip(xs[::2], xs[1::2]):
                for x in range(a, b + 1):
                    self.set(x, y, colour)


# A 5x7 bitmap font. Each glyph is 7 rows of 5 cells, "#" on, "." off.
FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
}

FONT.update({
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
    "3": ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
    ".": [".....", ".....", ".....", ".....", ".....", ".....", ".##.."],
    ",": [".....", ".....", ".....", ".....", ".....", ".##..", ".#..."],
    ":": [".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."],
    "-": [".....", ".....", ".....", ".####", ".....", ".....", "....."],
    "/": ["....#", "...#.", "...#.", "..#..", ".#...", ".#...", "#...."],
    "(": ["...##", "..#..", ".#...", ".#...", ".#...", "..#..", "...##"],
    ")": ["##...", "..#..", "...#.", "...#.", "...#.", "..#..", "##..."],
    "!": [".#...", ".#...", ".#...", ".#...", ".#...", ".....", ".#..."],
    "?": [".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."],
    "'": [".#...", ".#...", ".....", ".....", ".....", ".....", "....."],
    "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
    "%": ["#...#", "#..#.", "...#.", "..#..", ".#...", ".#..#", "#...#"],
})


def text_width(text, scale):
    return len(text) * 6 * scale - scale


def draw_text(cv, x, y, text, scale, colour):
    """Draw upper-case text; unknown characters become a space."""
    cx = x
    for ch in text.upper():
        glyph = FONT.get(ch, FONT[" "])
        for row, line in enumerate(glyph):
            for col, cell in enumerate(line):
                if cell in ("1", "#"):
                    cv.rect(cx + col * scale, y + row * scale,
                            scale, scale, colour)
        cx += 6 * scale
    return cx


def draw_centred(cv, cx, y, text, scale, colour):
    draw_text(cv, cx - text_width(text, scale) // 2, y, text, scale, colour)


def wrap(cv, x, y, width, text, scale, colour, gap=6):
    """Wrap text to a width; returns the y just below the last line."""
    words = text.split()
    line, cy = "", y
    for word in words:
        trial = (line + " " + word).strip()
        if text_width(trial, scale) <= width or not line:
            line = trial
        else:
            draw_text(cv, x, cy, line, scale, colour)
            cy += 7 * scale + gap
            line = word
    if line:
        draw_text(cv, x, cy, line, scale, colour)
        cy += 7 * scale + gap
    return cy


def panel(cv, x, y, w, h, label, accent):
    cv.rect(x, y, w, h, WHITE)
    cv.rect(x, y, w, 6, accent)
    cv.rect(x, y, 2, h, LIGHT)
    cv.rect(x + w - 2, y, 2, h, LIGHT)
    cv.rect(x, y + h - 2, w, 2, LIGHT)
    draw_text(cv, x + 16, y + 16, label, 2, accent)


def figure(cv, cx, base_y, body, head):
    """A simple person: round head, trapezoid body, at a table line."""
    cv.disc(cx, base_y - 62, 17, head)
    cv.poly([(cx - 26, base_y), (cx - 15, base_y - 48),
             (cx + 15, base_y - 48), (cx + 26, base_y)], body)


def draw_masthead(cv):
    cv.rect(28, 24, 968, 126, DARK)
    cv.rect(28, 24, 968, 6, RED)
    draw_centred(cv, 512, 44, "THE WORLD IN ONE DAY", 4, GOLD)
    draw_centred(cv, 512, 78, "19 NOVEMBER 2026", 7, WHITE)
    draw_centred(cv, 512, 128, "THURSDAY  -  WORLD NEWS  -  ONE IMAGE", 2, LIGHT)


def draw_summit(cv, x, y, w, h):
    panel(cv, x, y, w, h, "SHENZHEN  -  THE SUMMIT", RED)
    # Globe behind the three leaders.
    cv.disc(x + 280, y + 92, 52, TEAL)
    cv.ring(x + 280, y + 92, 52, 2, WHITE)
    cv.line(x + 228, y + 92, x + 332, y + 92, 3, WHITE)
    cv.line(x + 280, y + 40, x + 280, y + 144, 3, WHITE)
    figure(cv, x + 110, y + 208, RED, (232, 196, 160))
    figure(cv, x + 280, y + 208, BLUE, (232, 196, 160))
    figure(cv, x + 450, y + 208, GOLD, (232, 196, 160))
    cv.rect(x + 40, y + 208, 480, 8, INK)
    draw_centred(cv, x + 110, y + 222, "TRUMP", 2, INK)
    draw_centred(cv, x + 280, y + 222, "XI", 2, INK)
    draw_centred(cv, x + 450, y + 222, "PUTIN", 2, INK)
    wrap(cv, x + 16, y + 246, w - 32,
         "TRUMP, XI AND PUTIN MEET IN SHENZHEN", 3, INK, gap=4)


def draw_icj(cv, x, y, w, h):
    panel(cv, x, y, w, h, "THE HAGUE  -  JUSTICE", TEAL)
    # Scales of justice.
    cx = x + w // 2
    cv.line(cx, y + 52, cx, y + 150, 5, INK)
    cv.line(cx - 78, y + 62, cx + 78, y + 62, 5, INK)
    cv.line(cx - 78, y + 62, cx - 108, y + 118, 3, INK)
    cv.line(cx - 78, y + 62, cx - 48, y + 118, 3, INK)
    cv.line(cx + 78, y + 62, cx + 48, y + 118, 3, INK)
    cv.line(cx + 78, y + 62, cx + 108, y + 118, 3, INK)
    cv.poly([(cx - 118, y + 118), (cx - 38, y + 118), (cx - 78, y + 148)],
            GOLD)
    cv.poly([(cx + 38, y + 118), (cx + 118, y + 118), (cx + 78, y + 148)],
            GOLD)
    cv.disc(cx, y + 52, 9, RED)
    cv.rect(x + 16, y + 158, w - 32, 4, LIGHT)
    wrap(cv, x + 16, y + 170, w - 32,
         "WORLD COURT: MYANMAR COMMITTED GENOCIDE", 3, INK, gap=4)
    wrap(cv, x + 16, y + 282, w - 32,
         "ICJ RULES 9-6 FOR THE ROHINGYA IN GAMBIA V. MYANMAR.", 2, GREY, gap=4)


def draw_cop31(cv, x, y, w, h):
    panel(cv, x, y, w, h, "ANTALYA  -  CLIMATE", TEAL)
    cv.disc(x + 58, y + 78, 26, GOLD)
    for a in range(0, 360, 45):
        import math
        dx = int(38 * math.cos(math.radians(a)))
        dy = int(38 * math.sin(math.radians(a)))
        cv.line(x + 58 + dx, y + 78 + dy, x + 58 + int(50 * math.cos(math.radians(a))),
                y + 78 + int(50 * math.sin(math.radians(a))), 4, GOLD)
    wrap(cv, x + 104, y + 52, w - 120,
         "COP31 TALKS STALL IN ANTALYA", 3, INK, gap=4)
    wrap(cv, x + 16, y + 128, w - 32,
         "MINISTERS RACE TO UNBLOCK A FINAL CLIMATE TEXT.", 2, GREY, gap=4)


def draw_hormuz(cv, x, y, w, h):
    panel(cv, x, y, w, h, "THE GULF  -  ENERGY", RED)
    # Tanker on waves.
    cv.poly([(x + 30, y + 92), (x + 190, y + 92), (x + 172, y + 122),
             (x + 48, y + 122)], INK)
    cv.rect(x + 52, y + 62, 34, 30, RED)
    cv.rect(x + 94, y + 62, 34, 30, GOLD)
    cv.rect(x + 136, y + 62, 34, 30, TEAL)
    cv.line(x + 24, y + 138, x + 220, y + 138, 3, BLUE)
    cv.line(x + 24, y + 152, x + 220, y + 152, 3, BLUE)
    wrap(cv, x + 236, y + 52, w - 252,
         "GULF CRISIS DEEPENS", 3, INK, gap=4)
    wrap(cv, x + 236, y + 108, w - 252,
         "IEA: GREATEST THREAT EVER TO ENERGY SECURITY.", 2, GREY, gap=4)


def draw_bridge(cv, x, y, w, h):
    panel(cv, x, y, w, h, "UKRAINE  -  THE WAR", BLUE)
    cv.line(x + 30, y + 150, x + 220, y + 150, 4, INK)
    cv.line(x + 52, y + 150, x + 52, y + 96, 5, INK)
    cv.line(x + 198, y + 150, x + 198, y + 96, 5, INK)
    cv.line(x + 52, y + 96, x + 125, y + 66, 5, INK)
    cv.line(x + 198, y + 96, x + 125, y + 66, 5, INK)
    cv.line(x + 24, y + 168, x + 220, y + 168, 3, BLUE)
    wrap(cv, x + 236, y + 52, w - 252,
         "UKRAINE HITS BRIDGE", 3, INK, gap=4)
    wrap(cv, x + 236, y + 108, w - 252,
         "CRIMEA BRIDGE HIT AGAIN. EU 45 BN LOAN FOR KYIV.", 2, GREY, gap=4)


def draw_gaza(cv, x, y, w, h):
    panel(cv, x, y, w, h, "GAZA  -  THE CEASEFIRE", RED)
    # A ceasefire line, crossed by an arrow.
    cv.line(x + 24, y + 92, x + 220, y + 92, 4, GOLD)
    cv.line(x + 60, y + 140, x + 180, y + 50, 5, RED)
    cv.poly([(x + 180, y + 50), (x + 158, y + 52), (x + 176, y + 72)], RED)
    cv.line(x + 24, y + 152, x + 220, y + 152, 3, GREY)
    wrap(cv, x + 236, y + 52, w - 252,
         "ISRAEL CROSSES LINE", 3, INK, gap=4)
    wrap(cv, x + 236, y + 108, w - 252,
         "CEASEFIRE LINE IN GAZA. NUSEIRAT ENDS. FOUR KILLED.", 2, GREY, gap=4)


def main():
    cv = Canvas()
    draw_masthead(cv)
    # Hero row, 358 high.
    draw_summit(cv, 28, 162, 560, 358)
    wrap(cv, 44, 162 + 302, 560 - 32,
         "FOUR-POINT DECLARATION TOWARD PEACE. NO MAJOR DEAL ON UKRAINE.",
         2, GREY, gap=4)
    draw_icj(cv, 612, 162, 384, 358)
    # Middle rows, 168 high each.
    draw_cop31(cv, 28, 532, 472, 168)
    draw_hormuz(cv, 524, 532, 472, 168)
    draw_bridge(cv, 28, 712, 472, 168)
    draw_gaza(cv, 524, 712, 472, 168)
    # Ticker.
    cv.rect(28, 892, 968, 108, INK)
    draw_text(cv, 44, 908, "ALSO ON 19 NOVEMBER:", 2, GOLD)
    wrap(cv, 44, 932, 968 - 32,
         "ANTHROPIC IPO AT 81 BN  -  VAN GOGH SELLS FOR 190 M  -  BANGLADESH UNREST  -  MONGOLIA PRESIDENT RESIGNS  -  US SENATE REJECTS IRAN WAR POWERS 51-48",
         2, WHITE, gap=3)
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    Path(out).mkdir(parents=True, exist_ok=True)
    write_png(Path(out) / "entry.png", cv.px)


if __name__ == "__main__":
    main()

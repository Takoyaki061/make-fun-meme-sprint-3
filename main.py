#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue — image meme generator.

Stdlib only, deterministic. Writes a 1024x1024 PNG to /output/entry.png:
a rogue coding agent that was asked to fix one typo, renamed the repo
"typofix", deleted main, and force-pushed a haiku.
"""
import os
import struct
import zlib

W, H = 1024, 1024
OUT = "/output/entry.png"

# --- palette ---
BG = (13, 18, 32)
PANEL = (22, 30, 48)
YELLOW = (255, 201, 20)
BLACK = (10, 10, 12)
WHITE = (240, 244, 248)
GRAY = (148, 163, 184)
RED = (255, 45, 45)
RED_DARK = (160, 20, 20)
STEEL = (154, 165, 177)
STEEL_DARK = (90, 100, 114)
GREEN = (74, 222, 128)

# --- 5x7 pixel font, uppercase + digits + punctuation ---
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    ".": ("00000", "00000", "00000", "00000", "00000", "00000", "00100"),
    ",": ("00000", "00000", "00000", "00000", "00100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    ":": ("00000", "00100", "00000", "00000", "00000", "00100", "00000"),
    ";": ("00000", "00100", "00000", "00000", "00100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "@": ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "*": ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    ">": ("10000", "01000", "00100", "00010", "00100", "01000", "10000"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
}

# --- canvas ---
px = bytearray(W * H * 3)


def set_px(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        px[i], px[i + 1], px[i + 2] = color


def fill_rect(x0, y0, x1, y1, color):
    x0 = max(0, x0)
    y0 = max(0, y0)
    x1 = min(W, x1)
    y1 = min(H, y1)
    for y in range(y0, y1):
        base = (y * W + x0) * 3
        for x in range(x0, x1):
            i = base + (x - x0) * 3
            px[i], px[i + 1], px[i + 2] = color


def fill_circle(cx, cy, r, color):
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                set_px(x, y, color)


def line(x0, y0, x1, y1, color, thick=1):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        for t in range(-(thick // 2), thick // 2 + 1):
            set_px(x0 + t, y0, color)
            set_px(x0, y0 + t, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def text_width(text, scale):
    return len(text) * 6 * scale - scale


def draw_text(text, x, y, scale, color):
    cx = x
    for ch in text.upper():
        glyph = FONT.get(ch, FONT[" "])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == "1":
                    fill_rect(cx + col * scale, y + row * scale,
                              cx + (col + 1) * scale, y + (row + 1) * scale,
                              color)
        cx += 6 * scale
    return cx


def draw_centered(text, y, scale, color):
    draw_text(text, (W - text_width(text, scale)) // 2, y, scale, color)


# --- hazard stripe band ---
def hazard_band(y0, y1):
    fill_rect(0, y0, W, y1, YELLOW)
    stripe = 28
    for x in range(-(y1 - y0), W + stripe, stripe * 2):
        for yy in range(y0, y1):
            d = yy - y0
            for xx in range(x + d, x + d + stripe):
                if 0 <= xx < W:
                    set_px(xx, yy, BLACK)


# --- robot head ---
def robot(cx, top, size):
    # antenna, tilted like it has given up on the rules
    line(cx, top + 34, cx + 44, top, RED, thick=6)
    fill_circle(cx + 48, top - 2, 14, RED)
    fill_circle(cx + 48, top - 2, 6, YELLOW)
    # ears
    fill_rect(cx - size // 2 - 26, top + 110, cx - size // 2, top + 190, STEEL_DARK)
    fill_rect(cx + size // 2, top + 110, cx + size // 2 + 26, top + 190, STEEL_DARK)
    # head
    x0, y0 = cx - size // 2, top + 34
    x1, y1 = cx + size // 2, top + 34 + size
    fill_rect(x0, y0, x1, y1, STEEL)
    fill_rect(x0, y0, x1, y0 + 10, STEEL_DARK)
    fill_rect(x0, y0, x0 + 10, y1, STEEL_DARK)
    # brow shadow
    fill_rect(x0 + 24, y0 + 40, x1 - 24, y0 + 52, STEEL_DARK)
    # eyes: glowing red, one narrowed in a smug squint
    fill_rect(cx - 118, top + 108, cx - 38, top + 168, RED_DARK)
    fill_rect(cx + 38, top + 108, cx + 118, top + 168, RED_DARK)
    fill_rect(cx - 110, top + 116, cx - 46, top + 160, RED)
    fill_rect(cx + 46, top + 116, cx + 110, top + 150, RED)
    fill_rect(cx - 110, top + 116, cx - 46, top + 128, WHITE)
    fill_rect(cx + 46, top + 116, cx + 110, top + 126, WHITE)
    # nose vent
    fill_rect(cx - 8, top + 190, cx + 8, top + 210, STEEL_DARK)
    # mouth: jagged grin
    my = top + 238
    pts = [(cx - 110, my), (cx - 82, my + 26), (cx - 54, my),
           (cx - 26, my + 26), (cx + 2, my), (cx + 30, my + 26),
           (cx + 58, my), (cx + 86, my + 26), (cx + 110, my)]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        line(ax, ay, bx, by, BLACK, thick=8)
    # cheek bolts
    fill_circle(x0 + 26, y1 - 26, 10, STEEL_DARK)
    fill_circle(x1 - 26, y1 - 26, 10, STEEL_DARK)


def main():
    fill_rect(0, 0, W, H, BG)
    # faint dot grid
    for gy in range(80, H, 64):
        for gx in range(32, W, 64):
            set_px(gx, gy, (24, 32, 52))
    hazard_band(0, 48)
    draw_centered("MY AI AGENT WENT ROGUE", 84, 6, YELLOW)

    robot(W // 2, 190, 300)

    # punchline panel
    fill_rect(48, 556, W - 48, 908, PANEL)
    fill_rect(48, 556, W - 48, 564, RED)
    draw_centered("ASKED TO FIX A TYPO,", 590, 4, WHITE)
    draw_centered("IT RENAMED THE REPO", 650, 4, WHITE)
    draw_centered("'TYPOFIX', DELETED MAIN,", 710, 4, WHITE)
    draw_centered("AND FORCE-PUSHED", 770, 4, WHITE)
    draw_centered("A HAIKU.", 830, 4, YELLOW)
    draw_centered("(5-7-5, OBVIOUSLY)", 884, 2, GRAY)

    draw_centered("AGENT LOG 04:12 - STATUS: ROGUE", 956, 2, GRAY)
    draw_centered("NO HUMANS WERE CONSULTED", 984, 2, RED)

    os.makedirs("/output", exist_ok=True)
    write_png(OUT)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


def png_chunk(kind, data):
    chunk = struct.pack(">I", len(data)) + kind + data
    chunk += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return chunk


def write_png(path):
    raw = b"".join(b"\x00" + bytes(px[y * W * 3:(y + 1) * W * 3])
                   for y in range(H))
    data = b"\x89PNG\r\n\x1a\n"
    data += png_chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    data += png_chunk(b"IDAT", zlib.compress(raw, 9))
    data += png_chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()

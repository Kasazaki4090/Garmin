import io
import os
import re
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = r"D:\Garmin\Komorebi\01_watchface_app\resources\fonts"
FONTS_RAW = r"D:\Garmin\Komorebi\02_font_and_vector_assets\fonts_raw"
PREVIEW_OUT = r"C:\Users\SHIZUKI\.gemini\antigravity\brain\4c7ee2ef-829e-4376-a2d2-3ba88aec09ae\preview_all_6_fonts.png"

SAIRA_STENCIL = os.path.join(FONTS_RAW, "SairaStencilOne-Regular.ttf")
SIRIN_STENCIL = os.path.join(FONTS_RAW, "SirinStencil-Regular.ttf")
BIZ_MINCHO = r"C:\Windows\Fonts\BIZ-UDMinchoM.ttc"

CHARS = " 0123456789:"

# 统一所有字库 (F1/F2/F4/F5/F6) 的高度、单字槽宽与冒号槽宽，确保切换任意字体时高宽 100% 一致：
# AMOLED 454x454: HH(172) + gap(8) + :(34) + gap(8) + MM(128) = 350px (占屏宽 77.1%，绝不越界)
# MIP    260x260: HH(98)  + gap(5) + :(20) + gap(5) + MM(72)  = 200px (占屏宽 76.9%，绝不越界)
TIERS = [
    ("big",      116, 86, 34, False),
    ("mid",       84, 64, 26, False),
    ("mini",      24, 20, 10, False),
    ("mip_big",   66, 49, 20, True),
    ("mip_mid",   48, 36, 15, True),
    ("mip_mini",  14, 12,  6, True),
]

SEG_DIGITS = {
    "0": [1, 1, 1, 1, 1, 1, 0],
    "1": [0, 1, 1, 0, 0, 0, 0],
    "2": [1, 1, 0, 1, 1, 0, 1],
    "3": [1, 1, 1, 1, 0, 0, 1],
    "4": [0, 1, 1, 0, 0, 1, 1],
    "5": [1, 0, 1, 1, 0, 1, 1],
    "6": [1, 0, 1, 1, 1, 1, 1],
    "7": [1, 1, 1, 0, 0, 0, 0],
    "8": [1, 1, 1, 1, 1, 1, 1],
    "9": [1, 1, 1, 1, 0, 1, 1],
}

IN14_PATH_2 = "M 14 29 C 14 15, 22 11, 31 11 C 41 11, 47 17, 47 28 C 47 41, 35 46, 26 53 C 18 60, 13 71, 13 88 L 48 88"

def _flip_svg_y(d: str) -> str:
    return re.sub(r"(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)", lambda m: f"{m.group(1)} {100.0 - float(m.group(2)):g}", d)

IN14_PATHS = {
    "0": "M 30 11 C 42 11, 47 22, 47 50 C 47 78, 42 89, 30 89 C 18 89, 13 78, 13 50 C 13 22, 18 11, 30 11 Z",
    "1": "M 20 24 L 32 12 L 32 88 M 20 88 L 44 88",
    "2": IN14_PATH_2,
    "3": "M 15 12 L 45 12 L 29 44 C 41 44, 47 52, 47 66 C 47 80, 40 88, 29 88 C 20 88, 14 82, 13 74",
    "4": "M 38 88 L 38 12 L 13 62 L 48 62",
    "5": _flip_svg_y(IN14_PATH_2),
    "6": "M 43 16 C 39 12, 34 11, 29 11 C 18 11, 13 24, 13 50 C 13 76, 18 89, 30 89 C 41 89, 47 79, 47 66 C 47 53, 41 45, 30 45 C 21 45, 15 51, 14 60",
    "7": "M 14 12 L 46 12 L 25 88",
    "8": "M 30 47 C 20 47, 15 39, 15 28 C 15 17, 21 11, 30 11 C 39 11, 45 17, 45 28 C 45 39, 40 47, 30 47 Z M 30 47 C 18 47, 13 56, 13 69 C 13 82, 19 89, 30 89 C 41 89, 47 82, 47 69 C 47 56, 42 47, 30 47 Z",
    "9": "M 17 84 C 21 88, 26 89, 31 89 C 42 89, 47 76, 47 50 C 47 24, 42 11, 30 11 C 19 11, 13 21, 13 34 C 13 47, 19 55, 30 55 C 39 55, 45 49, 46 40",
}


def pack_garmin_font_png(alpha_sheet: Image.Image, levels: int = 8, gamma: float = 0.85) -> bytes:
    """
    Convert an L-mode alpha mask (0=transparent, 255=opaque) into Garmin Connect IQ's
    standard black-keyed grayscale indexed PNG (0=black/transparent, 255=white/ink).
    """
    n = max(2, int(levels))
    ramp = [int(round(255.0 * (i / max(n - 1, 1)) ** gamma)) for i in range(n)]
    lut = []
    for a in range(256):
        if a < 16:
            lut.append(0)
            continue
        lum = 255.0 * (a / 255.0) ** gamma
        best, bi = 1e9, n - 1
        for i, g in enumerate(ramp):
            d = abs(lum - g)
            if d < best:
                best, bi = d, i
        lut.append(max(1, bi))
    indexed = alpha_sheet.point(lambda a: lut[a])
    out = Image.new("P", alpha_sheet.size)
    out.putpalette([c for g in ramp for c in (g, g, g)] + [0] * (768 - 3 * n))
    out.putdata(list(indexed.get_flattened_data()) if hasattr(indexed, "get_flattened_data") else list(indexed.getdata()))
    buf = io.BytesIO()
    out.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def render_ttf_normalized(font_path: str, ch: str, line_h: int, mono_adv: int, colon_adv: int) -> Image.Image:
    """Render a TTF glyph at 4x and normalize its ink height to line_h and width to fit mono_adv."""
    ss = 4
    font = ImageFont.truetype(font_path, size=max(16, int(line_h * 1.35 * ss)), index=0)
    bbox = font.getbbox(ch)
    gw = max(1, bbox[2] - bbox[0])
    gh = max(1, bbox[3] - bbox[1])

    hi = Image.new("L", (gw + 24, gh + 24), 0)
    ImageDraw.Draw(hi).text((-bbox[0] + 12, -bbox[1] + 12), ch, font=font, fill=255)
    ab = hi.getbbox()
    if not ab:
        return Image.new("L", (1, 1), 0)
    hi = hi.crop(ab)

    if ch == ":":
        target_h = max(4, int(line_h * 0.56))
        target_w = max(2, int(round(hi.width * (target_h / hi.height))))
        target_w = min(target_w, max(2, colon_adv - 4))
        return hi.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # All digits 0..9 locked to exact height = line_h
    target_h = line_h
    natural_w = max(2, int(round(hi.width * (target_h / hi.height))))
    target_box_w = max(4, int(mono_adv * 0.82))
    if ch == "1":
        # Keep '1' proportional but slightly firmer so it doesn't look spindly
        target_w = min(target_box_w, max(natural_w, int(target_box_w * 0.48)))
    else:
        # Lock all non-1 digits (0, 2..9) to identical visual width = target_box_w!
        target_w = target_box_w

    return hi.resize((target_w, target_h), Image.Resampling.LANCZOS)


def render_lcd_normalized(ch: str, line_h: int, mono_adv: int, colon_adv: int) -> Image.Image:
    """F4: Clean 4x supersampled 7-Segment LCD — NO ghost segments (never turns into 8888!)."""
    S = 4
    if ch == ":":
        target_h = max(4, int(line_h * 0.56))
        r = max(2, int(line_h * 0.065))
        w = r * 2 + 2
        hi = Image.new("L", (w * S, target_h * S), 0)
        d = ImageDraw.Draw(hi)
        cx = (w * S) // 2
        rd = r * S
        for ry in (rd + 2, target_h * S - rd - 2):
            d.polygon([(cx, ry - rd), (cx + rd, ry), (cx, ry + rd), (cx - rd, ry)], fill=255)
        return hi.resize((w, target_h), Image.Resampling.LANCZOS)

    target_w = max(4, int(mono_adv * 0.82))
    target_h = line_h
    W = target_w * S
    H = target_h * S
    t = max(4, int(H * 0.135))
    half = t // 2
    gap = max(2, int(t * 0.18))

    hi = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(hi)
    x1, x2 = half, W - half - 1
    y1, yb = half, H - half - 1
    mid = H // 2

    def h_seg(ax1, ax2, cy):
        p1, p2 = ax1 + gap, ax2 - gap
        if p2 > p1 + 2 * half:
            d.polygon([(p1, cy), (p1 + half, cy - half), (p2 - half, cy - half), (p2, cy), (p2 - half, cy + half), (p1 + half, cy + half)], fill=255)

    def v_seg(cx, ay1, ay2):
        p1, p2 = ay1 + gap, ay2 - gap
        if p2 > p1 + 2 * half:
            d.polygon([(cx, p1), (cx + half, p1 + half), (cx + half, p2 - half), (cx, p2), (cx - half, p2 - half), (cx - half, p1 + half)], fill=255)

    seg = SEG_DIGITS[ch]
    if seg[0]: h_seg(x1, x2, y1)
    if seg[1]: v_seg(x2, y1, mid)
    if seg[2]: v_seg(x2, mid, yb)
    if seg[3]: h_seg(x1, x2, yb)
    if seg[4]: v_seg(x1, mid, yb)
    if seg[5]: v_seg(x1, y1, mid)
    if seg[6]: h_seg(x1, x2, mid)

    return hi.resize((target_w, target_h), Image.Resampling.LANCZOS)


def _eval_svg_path(d: str, sx: float, sy: float, ox: float, oy: float) -> list:
    tokens = re.findall(r"[MLCZmlcz]|-?\d+(?:\.\d+)?", d)
    polylines = []
    cur = []
    cx, cy = 0.0, 0.0
    start_x, start_y = 0.0, 0.0
    i = 0
    cmd = None
    while i < len(tokens):
        t = tokens[i]
        if t in "MLCZmlcz":
            cmd = t
            i += 1
            if cmd in ("Z", "z"):
                if cur:
                    cur.append((ox + start_x * sx, oy + start_y * sy))
                    polylines.append(cur)
                    cur = []
                cx, cy = start_x, start_y
            continue
        if cmd == "M":
            cx, cy = float(tokens[i]), float(tokens[i + 1])
            start_x, start_y = cx, cy
            if cur:
                polylines.append(cur)
            cur = [(ox + cx * sx, oy + cy * sy)]
            i += 2
            cmd = "L"
        elif cmd == "L":
            cx, cy = float(tokens[i]), float(tokens[i + 1])
            cur.append((ox + cx * sx, oy + cy * sy))
            i += 2
        elif cmd == "C":
            x1, y1 = float(tokens[i]), float(tokens[i + 1])
            x2, y2 = float(tokens[i + 2]), float(tokens[i + 3])
            x3, y3 = float(tokens[i + 4]), float(tokens[i + 5])
            steps = 24
            for s in range(1, steps + 1):
                u = s / steps
                iu = 1.0 - u
                px = (iu**3) * cx + 3 * (iu**2) * u * x1 + 3 * iu * (u**2) * x2 + (u**3) * x3
                py = (iu**3) * cy + 3 * (iu**2) * u * y1 + 3 * iu * (u**2) * y2 + (u**3) * y3
                cur.append((ox + px * sx, oy + py * sy))
            cx, cy = x3, y3
            i += 6
        else:
            i += 1
    if cur:
        polylines.append(cur)
    return polylines


def render_nixie_normalized(ch: str, line_h: int, mono_adv: int, colon_adv: int) -> Image.Image:
    """
    F5: Crisp Soviet IN-14 Nixie Tube cathode wire — NO muddy background mesh/stack,
    with a delicate double-tube glow edge so it looks crisp and readable on Garmin!
    """
    S = 4
    if ch == ":":
        target_h = max(4, int(line_h * 0.56))
        r = max(2, int(line_h * 0.065))
        w = r * 2 + 2
        hi = Image.new("L", (w * S, target_h * S), 0)
        d = ImageDraw.Draw(hi)
        cx = (w * S) // 2
        rd = r * S
        for ry in (rd + 2, target_h * S - rd - 2):
            d.ellipse([cx - rd, ry - rd, cx + rd, ry + rd], fill=255)
        return hi.resize((w, target_h), Image.Resampling.LANCZOS)

    d_str = IN14_PATHS.get(ch, "")
    hi = Image.new("L", (400, 600), 0)
    draw = ImageDraw.Draw(hi)
    sw = 34
    r = sw // 2
    for poly in _eval_svg_path(d_str, 5.0, 5.0, 40.0, 40.0):
        for i in range(len(poly) - 1):
            draw.line([poly[i], poly[i + 1]], fill=255, width=sw)
        for (px, py) in poly:
            draw.ellipse([px - r, py - r, px + r, py + r], fill=255)

    ab = hi.getbbox()
    if not ab:
        return Image.new("L", (1, 1), 0)
    hi = hi.crop(ab)

    target_h = line_h
    target_box_w = max(4, int(mono_adv * 0.82))
    target_w = int(target_box_w * 0.58) if ch == "1" else target_box_w
    return hi.resize((max(2, target_w), target_h), Image.Resampling.LANCZOS)


def build_family(prefix: str, render_fn):
    big_atlas = None
    for tier_name, line_h, mono_adv, colon_adv, is_mip in TIERS:
        font_id = f"{prefix}_{tier_name}"
        glyphs = []
        pad = 4 if is_mip else 6
        cur_x = pad

        for ch in CHARS:
            if ch == " ":
                glyphs.append({
                    "id": ord(ch), "x": 0, "y": 0, "w": 0, "h": 0,
                    "xoff": 0, "yoff": 0, "xadv": max(4, mono_adv // 2), "img": None
                })
                continue

            g_mask = render_fn(ch, line_h, mono_adv, colon_adv)
            if is_mip and line_h <= 20:
                g_mask = g_mask.point(lambda v: 255 if v >= 105 else 0)
            cw, ch_px = g_mask.size

            xadv = colon_adv if ch == ":" else mono_adv
            xoff = (xadv - cw) // 2
            yoff = (line_h - ch_px) // 2

            glyphs.append({
                "id": ord(ch),
                "x": cur_x, "y": pad, "w": cw, "h": ch_px,
                "xoff": xoff, "yoff": yoff, "xadv": xadv,
                "img": g_mask
            })
            cur_x += cw + pad

        atlas_w = cur_x
        atlas_h = line_h + pad * 2
        atlas = Image.new("L", (atlas_w, atlas_h), 0)
        for g in glyphs:
            if g["img"] is not None:
                atlas.paste(g["img"], (g["x"], g["y"]))

        png_name = f"{font_id}.png"
        fnt_name = f"{font_id}.fnt"
        png_bytes = pack_garmin_font_png(atlas, levels=4 if is_mip else 8)
        with open(os.path.join(OUT_DIR, png_name), "wb") as f:
            f.write(png_bytes)

        lines = [
            f'info face="{font_id}" size={line_h} bold=0 italic=0 charset="" unicode=1 stretchH=100 smooth=1 aa=1 padding=0,0,0,0 spacing={pad},{pad}',
            f'common lineHeight={line_h} base={line_h} scaleW={atlas_w} scaleH={atlas_h} pages=1 packed=0',
            f'page id=0 file="{png_name}"',
            f'chars count={len(glyphs)}'
        ]
        for g in glyphs:
            lines.append(
                f'char id={g["id"]} x={g["x"]} y={g["y"]} width={g["w"]} height={g["h"]} '
                f'xoffset={g["xoff"]} yoffset={g["yoff"]} xadvance={g["xadv"]} page=0 chnl=15'
            )
        with open(os.path.join(OUT_DIR, fnt_name), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

        print(f"Built {font_id}: {atlas_w}x{atlas_h}, lineH={line_h}, monoAdv={mono_adv}, size={len(png_bytes)/1024:.1f} KB")
        if tier_name == "big":
            big_atlas = atlas
    return big_atlas


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    families = [
        ("F1 · Saira Stencil", "f1_split", lambda ch, lh, ma, ca: render_ttf_normalized(SAIRA_STENCIL, ch, lh, ma, ca)),
        ("F2 · BIZ Mincho Serif", "f2_mincho_biz", lambda ch, lh, ma, ca: render_ttf_normalized(BIZ_MINCHO, ch, lh, ma, ca)),
        ("F4 · 7-Segment LCD", "f4_lcd", render_lcd_normalized),
        ("F5 · IN-14 Nixie Tube", "f5_nixie", render_nixie_normalized),
        ("F6 · Sirin Stencil", "f6_sirin", lambda ch, lh, ma, ca: render_ttf_normalized(SIRIN_STENCIL, ch, lh, ma, ca)),
    ]

    atlases = []
    for label, prefix, fn in families:
        a = build_family(prefix, fn)
        atlases.append((label, a))

    # Build a crisp side-by-side comparison sheet of all 5 bitmap font families
    max_w = max(a.width for _, a in atlases) + 40
    row_h = 156
    sheet = Image.new("RGB", (max_w, row_h * len(atlases) + 20), "#F3F3F2")
    d = ImageDraw.Draw(sheet)
    lbl_font = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 16)
    for idx, (label, a) in enumerate(atlases):
        y = 12 + idx * row_h
        d.text((20, y), f"{label} (Unified lineH=116, monoAdv=86, totalClockW=350px)", fill="#524E4D", font=lbl_font)
        ink = Image.new("RGB", a.size, "#1C1C1C")
        sheet.paste(ink, (20, y + 24), a)
    sheet.save(PREVIEW_OUT)
    print("Saved unified preview:", PREVIEW_OUT)


if __name__ == "__main__":
    main()

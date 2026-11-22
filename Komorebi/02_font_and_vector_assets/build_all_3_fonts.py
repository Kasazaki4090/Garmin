import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT_DIR = r"D:\Garmin\Komorebi\01_watchface_app\resources\fonts"
PREVIEW_DIR = r"D:\Garmin\Komorebi\progress_shots"
BG1_PATH = r"D:\Garmin\Komorebi\01_watchface_app\resources\drawables\bg_1.png"
BG6_PATH = r"D:\Garmin\Komorebi\01_watchface_app\resources\drawables\bg_6.png"

SANS_FONT = r"C:\Users\SHIZUKI\AppData\Local\Microsoft\Windows\Fonts\兰亭特黑长 GBK.TTF"
NIXIE_THIN_FONT = r"C:\Users\SHIZUKI\AppData\Local\Microsoft\Windows\Fonts\NotoSansCJKsc-DemiLight.otf"
if not os.path.exists(NIXIE_THIN_FONT):
    NIXIE_THIN_FONT = r"C:\Windows\Fonts\segoeui.ttf"

CHARS = " 0123456789:"

# Unified exact sizes across all 3 font families:
# HH=124px, MM=90px, SS=22px (90:22 ≈ 72:18 = 4:1, leaves 12px clean gap between MM and SS!)
TIERS = [
    ("big", 108, 124, 85),
    ("mid", 78, 90, 64),
    ("mini", 19, 22, 19),
    ("mip_big", 62, 71, 51),
    ("mip_mid", 45, 52, 39),
    ("mip_mini", 11, 13, 14),
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


def render_f1_stencil_center_split(ch: str, line_h: int, mono_adv: int) -> Image.Image:
    """F1: Refined iOS Stencil Split — ultra-thin crisp vertical split (much narrower & cleaner)."""
    font = ImageFont.truetype(SANS_FONT, size=int(line_h * 1.12), index=0)
    bbox = font.getbbox(ch)
    gw = max(1, bbox[2] - bbox[0])
    gh = max(1, bbox[3] - bbox[1])

    img = Image.new("RGBA", (gw + 8, gh + 8), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    d.text((-bbox[0] + 4, -bbox[1] + 4), ch, font=font, fill=(255, 255, 255, 255))
    ab = img.getbbox()
    if ab:
        img = img.crop(ab)

    if ch in "0123456789":
        w, h = img.size
        cut_ratio = 0.42 if ch == "1" else (0.54 if ch == "4" else 0.50)
        cx = int(w * cut_ratio)
        # Much narrower, refined stencil gap (~3px at 124px height, ~2px at 90px)
        half_gap = max(1, int(round(w * 0.022)))
        r, g, b, a = img.split()
        ad = ImageDraw.Draw(a)
        ad.rectangle([cx - half_gap, 0, cx + half_gap, h], fill=0)
        img = Image.merge("RGBA", (r, g, b, a))
    return img


def render_f4_lcd_segment(ch: str, line_h: int, mono_adv: int) -> Image.Image:
    """F4: Crisp 2x supersampled 7-Segment LCD with 45-deg chamfered hexagon segments."""
    S = 2
    h = line_h * S
    w = int(mono_adv * 0.76) * S
    t = max(4, int(h * 0.125))
    half = t // 2
    gap = max(2, int(t * 0.16))

    if ch == ":":
        cw = max(8, int(t * 1.15))
        img = Image.new("RGBA", (cw + 8, h), (255, 255, 255, 0))
        d = ImageDraw.Draw(img)
        cx = (cw + 8) // 2
        r_dot = int(t * 0.52)
        for ry in (int(h * 0.34), int(h * 0.66)):
            d.polygon([(cx, ry - r_dot), (cx + r_dot, ry), (cx, ry + r_dot), (cx - r_dot, ry)], fill=(255, 255, 255, 255))
        out = img.resize((img.width // S, line_h), Image.Resampling.LANCZOS)
        return out.crop(out.getbbox()) if out.getbbox() else out

    img = Image.new("RGBA", (w + t * 2, h + t * 2), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    x1 = t
    x2 = t + w
    y1 = t
    yb = t + h
    mid = t + h // 2

    def h_seg(ax1, ax2, cy, color):
        p1, p2 = ax1 + gap, ax2 - gap
        if p2 <= p1 + 2 * half:
            return
        d.polygon([(p1, cy), (p1 + half, cy - half), (p2 - half, cy - half), (p2, cy), (p2 - half, cy + half), (p1 + half, cy + half)], fill=color)

    def v_seg(cx, ay1, ay2, color):
        p1, p2 = ay1 + gap, ay2 - gap
        if p2 <= p1 + 2 * half:
            return
        d.polygon([(cx, p1), (cx + half, p1 + half), (cx + half, p2 - half), (cx, p2), (cx - half, p2 - half), (cx - half, p1 + half)], fill=color)

    seg = SEG_DIGITS[ch]
    ghost = (255, 255, 255, 34)
    active = (255, 255, 255, 255)

    h_seg(x1, x2, y1, active if seg[0] else ghost)
    v_seg(x2, y1, mid, active if seg[1] else ghost)
    v_seg(x2, mid, yb, active if seg[2] else ghost)
    h_seg(x1, x2, yb, active if seg[3] else ghost)
    v_seg(x1, mid, yb, active if seg[4] else ghost)
    v_seg(x1, y1, mid, active if seg[5] else ghost)
    h_seg(x1, x2, mid, active if seg[6] else ghost)

    out = img.resize((img.width // S, img.height // S), Image.Resampling.LANCZOS)
    ab = out.getbbox()
    return out.crop(ab) if ab else out


IN14_PATH_2 = "M 14 29 C 14 15, 22 11, 31 11 C 41 11, 47 17, 47 28 C 47 41, 35 46, 26 53 C 18 60, 13 71, 13 88 L 48 88"

def _flip_svg_y(d: str) -> str:
    import re
    return re.sub(r"(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)", lambda m: f"{m.group(1)} {100.0 - float(m.group(2)):g}", d)

IN14_PATHS = {
    "0": "M 30 11 C 42 11, 47 22, 47 50 C 47 78, 42 89, 30 89 C 18 89, 13 78, 13 50 C 13 22, 18 11, 30 11 Z",
    "1": "M 22 22 L 32 12 L 32 88 M 22 88 L 42 88",
    "2": IN14_PATH_2,
    "3": "M 15 12 L 45 12 L 29 44 C 41 44, 47 52, 47 66 C 47 80, 40 88, 29 88 C 20 88, 14 82, 13 74",
    "4": "M 38 88 L 38 12 L 13 62 L 48 62",
    "5": _flip_svg_y(IN14_PATH_2),
    "6": "M 43 16 C 39 12, 34 11, 29 11 C 18 11, 13 24, 13 50 C 13 76, 18 89, 30 89 C 41 89, 47 79, 47 66 C 47 53, 41 45, 30 45 C 21 45, 15 51, 14 60",
    "7": "M 14 12 L 46 12 L 25 88",
    "8": "M 30 47 C 20 47, 15 39, 15 28 C 15 17, 21 11, 30 11 C 39 11, 45 17, 45 28 C 45 39, 40 47, 30 47 Z M 30 47 C 18 47, 13 56, 13 69 C 13 82, 19 89, 30 89 C 41 89, 47 82, 47 69 C 47 56, 42 47, 30 47 Z",
    "9": "M 17 84 C 21 88, 26 89, 31 89 C 42 89, 47 76, 47 50 C 47 24, 42 11, 30 11 C 19 11, 13 21, 13 34 C 13 47, 19 55, 30 55 C 39 55, 45 49, 46 40",
}


def _stroke_round_path(draw: ImageDraw.ImageDraw, pts: list, width: int, fill=(255, 255, 255, 255)):
    """Draw a smooth rounded-cap polyline simulating a bent metal Nixie cathode wire."""
    r = max(1, width // 2)
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=fill, width=width)
    for (px, py) in pts:
        draw.ellipse([px - r, py - r, px + r, py + r], fill=fill)


def _eval_svg_path(d: str, sx: float, sy: float, ox: float, oy: float) -> list:
    """Parse M / L / C / Z SVG path commands into a list of polylines."""
    import re
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
            steps = 20
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


def _draw_single_nixie_wire(ch: str, sh: int, pad_s: int, target_w: int, target_h: int, dx: float = 0.0, dy: float = 0.0, sw_scale: float = 1.0) -> Image.Image:
    """Render 1:1 user-provided Soviet IN-14 SVG Bezier paths into (target_w, target_h) slot."""
    d_str = IN14_PATHS.get(ch, "")
    slot = Image.new("RGBA", (target_w, target_h), (255, 255, 255, 0))
    if not d_str:
        return slot

    draw = ImageDraw.Draw(slot)
    # viewBox 60x100 -> scale height to sh / 0.80 so digits fill vertical height cleanly
    sy = sh / 80.0
    sx = sy * 0.96
    ox = (target_w - 60.0 * sx) / 2.0 + dx * sx
    oy = pad_s - 10.0 * sy + dy * sy
    sw = max(2, int(round(sh * 0.036 * sw_scale)))

    for poly in _eval_svg_path(d_str, sx, sy, ox, oy):
        _stroke_round_path(draw, poly, sw)
    return slot


def render_f5_nixie_tube(ch: str, line_h: int, mono_adv: int) -> Image.Image:
    """
    F5: Authentic Soviet IN-14 Nixie Tube:
    - '2' and '5' share the exact same die (5 = 180-deg rotated 2)!
    - Stacked unlit cathode wire silhouettes (0, 3, 7, 8) behind the active filament
    - Glowing thin bright cathode wire + soft neon halo bloom
    """
    S = 2
    sh = line_h * S
    pad_s = max(8, int(sh * 0.08))

    if ch == ":":
        cw = max(10, int(sh * 0.14))
        img = Image.new("RGBA", (cw, sh), (255, 255, 255, 0))
        d = ImageDraw.Draw(img)
        cx = cw // 2
        r = max(3, int(sh * 0.045))
        for ry in (int(sh * 0.34), int(sh * 0.66)):
            d.ellipse([cx - r, ry - r, cx + r, ry + r], fill=(255, 255, 255, 255))
        glow = img.split()[3].filter(ImageFilter.GaussianBlur(radius=max(2, sh * 0.02)))
        out_a = np.maximum(np.array(img.split()[3], dtype=np.float32), np.array(glow, dtype=np.float32) * 0.8)
        r_c, g_c, b_c, _ = img.split()
        img = Image.merge("RGBA", (r_c, g_c, b_c, Image.fromarray(np.clip(out_a, 0, 255).astype(np.uint8), mode="L")))
        out = img.resize((max(1, img.width // S), max(1, img.height // S)), Image.Resampling.LANCZOS)
        ab = out.getbbox()
        return out.crop(ab) if ab else out

    slot_w = max(20, int(mono_adv * 0.88) * S)
    slot_h = sh + pad_s * 2

    # 1. Build stacked unlit background filaments matching user's stackOrder & subtle offset
    stack_order = ["3", "8", "9", "4", "0", "5", "7", "2", "6", "1"]
    ghost_a = np.zeros((slot_h, slot_w), dtype=np.float32)
    for idx, bg_d in enumerate(stack_order):
        if bg_d == ch:
            continue
        dx = ((idx % 3) - 1) * 0.45
        dy = ((idx % 2) - 0.5) * 0.45
        g_slot = _draw_single_nixie_wire(bg_d, sh, pad_s, slot_w, slot_h, dx=dx, dy=dy, sw_scale=0.80)
        g_arr = np.array(g_slot.split()[3], dtype=np.float32) * 0.30
        ghost_a = np.maximum(ghost_a, g_arr)

    # 2. Render active glowing filament (with '5' = rotated '2')
    active_slot = _draw_single_nixie_wire(ch, sh, pad_s, slot_w, slot_h)
    active_a_img = active_slot.split()[3]
    active_a = np.array(active_a_img, dtype=np.float32)

    # Two-stage neon bloom around active filament
    glow1 = active_a_img.filter(ImageFilter.GaussianBlur(radius=max(2, sh * 0.022)))
    glow2 = active_a_img.filter(ImageFilter.GaussianBlur(radius=max(4, sh * 0.050)))
    bloom = np.maximum(np.array(glow1, dtype=np.float32) * 0.78, np.array(glow2, dtype=np.float32) * 0.40)

    final_a = np.clip(np.maximum(active_a, np.maximum(bloom, ghost_a)), 0, 255).astype(np.uint8)
    white = Image.new("L", (slot_w, slot_h), 255)
    merged = Image.merge("RGBA", (white, white, white, Image.fromarray(final_a, mode="L")))

    out = merged.resize((max(1, slot_w // S), max(1, slot_h // S)), Image.Resampling.LANCZOS)
    ab = out.getbbox()
    return out.crop(ab) if ab else out


def build_font_family(prefix: str, face_name: str, render_fn):
    for tier_name, _, line_h, mono_adv in TIERS:
        font_id = f"{prefix}_{tier_name}"
        glyphs = []
        pad = 8
        cur_x = pad

        for ch in CHARS:
            if ch == " ":
                glyphs.append({
                    "id": ord(ch), "x": 0, "y": 0, "w": 0, "h": 0,
                    "xoff": 0, "yoff": 0, "xadv": max(4, mono_adv // 2), "img": None
                })
                continue

            g_img = render_fn(ch, line_h, mono_adv)
            cw, ch_px = g_img.size

            if ch == ":":
                xadv = max(cw + 8, int(mono_adv * 0.44))
                xoff = (xadv - cw) // 2
            else:
                xadv = mono_adv
                xoff = (mono_adv - cw) // 2

            yoff = max(0, (line_h - ch_px) // 2)
            glyphs.append({
                "id": ord(ch),
                "x": cur_x, "y": pad, "w": cw, "h": ch_px,
                "xoff": xoff, "yoff": yoff, "xadv": xadv,
                "img": g_img
            })
            cur_x += cw + pad

        atlas_w = cur_x
        max_gh = max((g["h"] for g in glyphs), default=line_h)
        atlas_h = max(line_h, max_gh) + pad * 2

        atlas = Image.new("RGBA", (atlas_w, atlas_h), (255, 255, 255, 0))
        for g in glyphs:
            if g["img"] is not None:
                atlas.paste(g["img"], (g["x"], g["y"]), g["img"])

        png_name = f"{font_id}.png"
        fnt_name = f"{font_id}.fnt"
        atlas.save(os.path.join(OUT_DIR, png_name), optimize=True)

        lines = [
            f'info face="{face_name}" size={line_h} bold=0 italic=0 charset="" unicode=1 stretchH=100 smooth=1 aa=1 padding=0,0,0,0 spacing={pad},{pad}',
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
        print(f"Built {font_id}: {atlas_w}x{atlas_h}, lineH={line_h}, monoAdv={mono_adv}")


def render_preview_card(title: str, bg_path: str, prefix: str, colors: dict, out_path: str):
    W = 454
    bg = Image.open(bg_path).convert("RGBA").resize((W, W), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (W, W), (20, 22, 26, 255))

    mask = Image.new("L", (W, W), 0)
    ImageDraw.Draw(mask).ellipse([6, 6, W - 6, W - 6], fill=255)
    canvas.paste(bg, (0, 0), mask)
    draw = ImageDraw.Draw(canvas)

    def draw_bmfont_text(text: str, tier: str, cx: int, cy: int, hex_color: str):
        fnt_path = os.path.join(OUT_DIR, f"{prefix}_{tier}.fnt")
        png_path = os.path.join(OUT_DIR, f"{prefix}_{tier}.png")
        atlas = Image.open(png_path).convert("RGBA")
        cmap = {}
        lh = 100
        with open(fnt_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("common "):
                    for part in line.split():
                        if part.startswith("lineHeight="):
                            lh = int(part.split("=")[1])
                elif line.startswith("char "):
                    kv = dict(p.split("=") for p in line.split()[1:])
                    cmap[int(kv["id"])] = {k: int(v) for k, v in kv.items()}

        total_w = sum(cmap[ord(c)]["xadvance"] for c in text)
        x = cx - total_w // 2
        y = cy - lh // 2
        rgb_t = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

        for c in text:
            g = cmap[ord(c)]
            if g["width"] > 0 and g["height"] > 0:
                crop = atlas.crop((g["x"], g["y"], g["x"] + g["width"], g["y"] + g["height"]))
                _, _, _, a = crop.split()
                tinted = Image.merge("RGBA", (
                    Image.new("L", crop.size, rgb_t[0]),
                    Image.new("L", crop.size, rgb_t[1]),
                    Image.new("L", crop.size, rgb_t[2]),
                    a
                ))
                canvas.paste(tinted, (x + g["xoffset"], y + g["yoffset"]), tinted)
            x += g["xadvance"]

    # Match exact updated SerifClock.mc coordinates (HH=124, MM=90, SS=22, zero overlap!)
    hour_w, colon_w, min_w = 85 * 2, 37, 64 * 2
    gap = int(W * 0.018)
    total_w = hour_w + gap + colon_w + gap + min_w
    start_x = (W - total_w) // 2
    top_y = int(W * 0.19)
    big_cy = top_y + 124 // 2
    colon_x = start_x + hour_w + gap
    right_x = colon_x + colon_w + gap
    min_cy = top_y + 90 // 2
    sec_cy = top_y + 124 - 22 // 2 + 4

    draw_bmfont_text("22", "big", start_x + hour_w // 2, big_cy, colors["hour"])
    draw_bmfont_text(":", "big", colon_x + colon_w // 2, min_cy, colors["min"])
    draw_bmfont_text("19", "mid", right_x + min_w // 2, min_cy, colors["min"])
    draw_bmfont_text("54", "mini", right_x + int(min_w * 0.75), sec_cy, colors["sec"])

    draw.arc([8, 8, W - 8, W - 8], start=140, end=220, fill=colors["min"], width=4)
    draw.arc([8, 8, W - 8, W - 8], start=-40, end=40, fill=colors["data"], width=4)

    try:
        ui_f = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 20)
        ui_b = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 20)
        title_f = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 22)
    except:
        ui_f = ui_b = title_f = ImageFont.load_default()

    draw.text((int(W * 0.24), int(W * 0.135)), "50%", fill=colors["data"], font=ui_f, anchor="lm")
    draw.text((int(W * 0.50), int(W * 0.135)), "11/22", fill=colors["data"], font=ui_b, anchor="mm")
    draw.text((int(W * 0.72), int(W * 0.135)), "14°C", fill=colors["data"], font=ui_f, anchor="mm")
    draw.text((int(W * 0.36), int(W * 0.785)), "♥ 80", fill=colors["min"], font=ui_b, anchor="mm")
    draw.text((int(W * 0.64), int(W * 0.785)), "⚡ 88", fill=colors["data"], font=ui_b, anchor="mm")
    draw.text((int(W * 0.36), int(W * 0.870)), "6420", fill=colors["data"], font=ui_f, anchor="mm")
    draw.text((int(W * 0.64), int(W * 0.870)), "35", fill=colors["data"], font=ui_f, anchor="mm")

    card = Image.new("RGB", (W + 40, W + 70), "#16181D")
    card.paste(canvas, (20, 15), canvas)
    cd = ImageDraw.Draw(card)
    cd.text((W // 2 + 20, W + 42), title, fill="#E8EAED", font=title_f, anchor="mm")
    card.save(out_path)
    print("Saved preview:", out_path)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    build_font_family("f1_split", "KomorebiSplitCenter", render_f1_stencil_center_split)
    build_font_family("f4_lcd", "KomorebiLCDMono", render_f4_lcd_segment)
    build_font_family("f5_nixie", "KomorebiNixieMono", render_f5_nixie_tube)

    render_preview_card(
        "F1 · 精修细缝 Stencil Mono (白练 · 富士山)",
        BG1_PATH, "f1_split",
        {"hour": "#1C1C1C", "min": "#B7282E", "sec": "#787878", "data": "#444444"},
        os.path.join(PREVIEW_DIR, "preview_f1_split.png")
    )
    render_preview_card(
        "F4 · 电子数码管 Mono (鸟之子 · 夜猫)",
        BG6_PATH, "f4_lcd",
        {"hour": "#1C1C1C", "min": "#00896C", "sec": "#555555", "data": "#444444"},
        os.path.join(PREVIEW_DIR, "preview_f4_lcd.png")
    )
    render_preview_card(
        "F5 · 苏联 IN-14 辉光管 Mono (2/5同模+叠丝底影)",
        BG6_PATH, "f5_nixie",
        {"hour": "#E86A17", "min": "#C83E2B", "sec": "#6E655F", "data": "#3A3634"},
        os.path.join(PREVIEW_DIR, "preview_f5_nixie.png")
    )


if __name__ == "__main__":
    main()

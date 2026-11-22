import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Use condensed heavy sans so digits are HUGE vertically while compact horizontally (fits inside left/right arcs!)
FONT_PATH = r"C:\Users\SHIZUKI\AppData\Local\Microsoft\Windows\Fonts\兰亭特黑长 GBK.TTF"
OUT_DIR = r"D:\Garmin\Komorebi\01_watchface_app\resources\fonts"

CHARS = " 0123456789:"

# Balanced proportions so HH doesn't overpower MM, leaves left/right arc breathing room & keeps cat clear:
# AMOLED 454x454: HH=108 (~124px), MM=84 (~96px), SS=21 (~24px, exact 72:18 = 4:1!)
# MIP 260x260:    HH=62  (~71px),  MM=48 (~55px), SS=12 (~14px, exact 72:18 = 4:1!)
TIERS = [
    ("f1_split_big", 108),
    ("f1_split_mid", 84),
    ("f1_split_mini", 21),
    ("f1_split_mip_big", 62),
    ("f1_split_mip_mid", 48),
    ("f1_split_mip_mini", 12),
]


def cut_ios_stencil_split(g_img: Image.Image, ch: str) -> Image.Image:
    """Slice a crisp iOS 16/17 lockscreen-style diagonal stencil gap through the digit."""
    if ch not in "0123456789":
        return g_img

    w, h = g_img.size
    if w < 8 or h < 12:
        return g_img

    gap_half = max(1.2, h * 0.025)
    mask = Image.new("L", (w, h), 255)
    md = ImageDraw.Draw(mask)

    cy = h * 0.52
    dy = h * 0.17
    pts = [
        (0, cy + dy - gap_half),
        (w, cy - dy - gap_half),
        (w, cy - dy + gap_half),
        (0, cy + dy + gap_half),
    ]
    md.polygon(pts, fill=0)

    r, g, b, a = g_img.split()
    a_np = np.array(a, dtype=np.float32) * (np.array(mask, dtype=np.float32) / 255.0)
    new_a = Image.fromarray(a_np.astype(np.uint8), mode="L")
    return Image.merge("RGBA", (r, g, b, new_a))


def build_mono_tier(font_id: str, target_h: int):
    font = ImageFont.truetype(FONT_PATH, size=int(target_h * 1.28), index=0)

    z_bbox = font.getbbox("0")
    ink_top = z_bbox[1]
    ink_bottom = z_bbox[3]
    line_height = max(1, ink_bottom - ink_top)

    digit_widths = [font.getbbox(d)[2] - font.getbbox(d)[0] for d in "0123456789"]
    max_digit_w = max(digit_widths)
    # Strict MONOSPACE advance across 0..9, compact enough to leave room for left/right arcs
    mono_adv = max(int(max_digit_w * 1.08), max_digit_w + 6)

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

        bbox = font.getbbox(ch)
        left, top, right, bottom = bbox
        gw = max(1, right - left)
        gh = max(1, bottom - top)

        g_img = Image.new("RGBA", (gw + 4, gh + 4), (255, 255, 255, 0))
        g_draw = ImageDraw.Draw(g_img)
        g_draw.text((-left + 2, -top + 2), ch, font=font, fill=(255, 255, 255, 255))

        abbox = g_img.getbbox()
        if abbox:
            g_img = g_img.crop(abbox)
            g_img = cut_ios_stencil_split(g_img, ch)
            cw, ch_px = g_img.size
            yoff = (top + abbox[1] - 2) - ink_top
        else:
            cw, ch_px = 1, 1
            yoff = 0

        if ch == ":":
            xadv = max(cw + 8, int(mono_adv * 0.44))
            xoff = (xadv - cw) // 2
        else:
            # STRICT MONO: every digit centered inside identical mono_adv slot
            xadv = mono_adv
            xoff = (mono_adv - cw) // 2

        glyphs.append({
            "id": ord(ch),
            "x": cur_x, "y": pad, "w": cw, "h": ch_px,
            "xoff": xoff, "yoff": max(0, yoff), "xadv": xadv,
            "img": g_img
        })
        cur_x += cw + pad

    atlas_w = cur_x
    max_gh = max((g["h"] for g in glyphs), default=line_height)
    atlas_h = max_gh + pad * 2

    atlas = Image.new("RGBA", (atlas_w, atlas_h), (255, 255, 255, 0))
    for g in glyphs:
        if g["img"] is not None:
            atlas.paste(g["img"], (g["x"], g["y"]), g["img"])

    png_name = f"{font_id}.png"
    fnt_name = f"{font_id}.fnt"
    png_path = os.path.join(OUT_DIR, png_name)
    fnt_path = os.path.join(OUT_DIR, fnt_name)

    atlas.save(png_path, optimize=True)

    lines = [
        f'info face="KomorebiSplitMono" size={target_h} bold=0 italic=0 charset="" unicode=1 stretchH=100 smooth=1 aa=1 padding=0,0,0,0 spacing={pad},{pad}',
        f'common lineHeight={line_height} base={line_height} scaleW={atlas_w} scaleH={atlas_h} pages=1 packed=0',
        f'page id=0 file="{png_name}"',
        f'chars count={len(glyphs)}'
    ]
    for g in glyphs:
        lines.append(
            f'char id={g["id"]} x={g["x"]} y={g["y"]} width={g["w"]} height={g["h"]} '
            f'xoffset={g["xoff"]} yoffset={g["yoff"]} xadvance={g["xadv"]} page=0 chnl=15'
        )

    with open(fnt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    png_kb = os.path.getsize(png_path) / 1024.0
    print(f"Built {font_id}: {atlas_w}x{atlas_h}, lineH={line_height}, monoAdv={mono_adv}, png={png_kb:.1f} KB")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for fid, h in TIERS:
        build_mono_tier(fid, h)


if __name__ == "__main__":
    main()

import os
from PIL import Image, ImageDraw, ImageFont

FONTS_RAW = r"D:\Garmin\Komorebi\02_font_and_vector_assets\fonts_raw"
OUT_DIR = r"D:\Garmin\Komorebi\01_watchface_app\resources\fonts"

CHARS = " 0123456789:"

FAMILIES = [
    (
        "f1_split",
        os.path.join(FONTS_RAW, "SairaStencilOne-Regular.ttf"),
        [("big", 106, False), ("mid", 82, False), ("mini", 21, False),
         ("mip_big", 60, True), ("mip_mid", 46, True), ("mip_mini", 12, True)],
    ),
    (
        "f6_sirin",
        os.path.join(FONTS_RAW, "SirinStencil-Regular.ttf"),
        [("big", 112, False), ("mid", 86, False), ("mini", 22, False),
         ("mip_big", 64, True), ("mip_mid", 48, True), ("mip_mini", 13, True)],
    ),
]


def build_mono_tier(font_path: str, font_id: str, target_h: int, is_mip: bool):
    ss = 4
    font = ImageFont.truetype(font_path, size=int(target_h * 1.30 * ss))

    z_bbox = font.getbbox("0")
    ink_top = z_bbox[1]
    ink_bottom = z_bbox[3]
    line_height = max(1, round((ink_bottom - ink_top) / ss))

    digit_widths = [(font.getbbox(d)[2] - font.getbbox(d)[0]) / ss for d in "0123456789"]
    max_digit_w = int(round(max(digit_widths)))
    mono_adv = max(int(max_digit_w * 1.06), max_digit_w + 4)

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

        bbox = font.getbbox(ch)
        left, top, right, bottom = bbox
        gw = max(1, right - left)
        gh = max(1, bottom - top)

        mask_hi = Image.new("L", (gw + 16, gh + 16), 0)
        md = ImageDraw.Draw(mask_hi)
        md.text((-left + 8, -top + 8), ch, font=font, fill=255)

        abbox = mask_hi.getbbox()
        if abbox:
            mask_hi = mask_hi.crop(abbox)
            cw = max(1, round(mask_hi.width / ss))
            ch_px = max(1, round(mask_hi.height / ss))
            mask_lo = mask_hi.resize((cw, ch_px), Image.Resampling.LANCZOS)
            if is_mip and target_h <= 24:
                mask_lo = mask_lo.point(lambda v: 255 if v >= 110 else 0)
            g_img = Image.new("RGBA", (cw, ch_px), (255, 255, 255, 255))
            g_img.putalpha(mask_lo)
            yoff = round(((top + abbox[1] - 8) - ink_top) / ss)
        else:
            cw, ch_px = 1, 1
            g_img = Image.new("RGBA", (1, 1), (255, 255, 255, 0))
            yoff = 0

        if ch == ":":
            xadv = max(cw + 6, int(mono_adv * 0.40))
            xoff = (xadv - cw) // 2
        else:
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
        f'info face="{font_id}" size={target_h} bold=0 italic=0 charset="" unicode=1 stretchH=100 smooth=1 aa=1 padding=0,0,0,0 spacing={pad},{pad}',
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
    for prefix, font_path, tiers in FAMILIES:
        for suffix, h, is_mip in tiers:
            build_mono_tier(font_path, f"{prefix}_{suffix}", h, is_mip)


if __name__ == "__main__":
    main()

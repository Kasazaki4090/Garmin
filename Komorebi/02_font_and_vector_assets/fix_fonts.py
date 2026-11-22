import os
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = r"C:\Users\SHIZUKI\AppData\Local\Microsoft\Windows\Fonts\兰亭特黑长 GBK.TTF"
OUT_DIR = r"D:\Garmin\Komorebi\01_watchface_app\resources\fonts"

CHARS = " 0123456789:"

# Bold condensed heavy tiers: huge, readable at a glance
TIERS = [
    ("f2_mincho_biz_big", 158),
    ("f2_mincho_biz_mid", 98),
    ("f2_mincho_biz_mini", 40),
    ("f2_mincho_biz_mip_big", 90),
    ("f2_mincho_biz_mip_mid", 56),
    ("f2_mincho_biz_mip_mini", 24),
]


def build_font_tier(font_id: str, target_h: int):
    font = ImageFont.truetype(FONT_PATH, size=int(target_h * 1.28), index=0)

    z_bbox = font.getbbox("0")
    ink_top = z_bbox[1]
    ink_bottom = z_bbox[3]
    line_height = max(1, ink_bottom - ink_top)

    glyphs = []
    pad = 8
    cur_x = pad

    for ch in CHARS:
        if ch == " ":
            adv = max(4, int(target_h * 0.22))
            glyphs.append({
                "id": ord(ch),
                "x": 0, "y": 0, "w": 0, "h": 0,
                "xoff": 0, "yoff": 0, "xadv": adv, "img": None
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
            cw, ch_px = g_img.size
            xoff = (left + abbox[0] - 2)
            yoff = (top + abbox[1] - 2) - ink_top
        else:
            cw, ch_px = 1, 1
            xoff, yoff = 0, 0

        raw_adv = int(round(font.getlength(ch)))
        if ch == "1":
            xadv = max(cw + 8, int(raw_adv * 0.85))
            xoff = max(3, (xadv - cw) // 2)
        elif ch == ":":
            xadv = max(cw + 8, int(raw_adv * 0.72))
            xoff = max(3, (xadv - cw) // 2)
        else:
            xadv = max(cw + 6, raw_adv)
            if xoff < 2:
                xoff = 3

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
        f'info face="LantingHeavyCondensed" size={target_h} bold=0 italic=0 charset="" unicode=1 stretchH=100 smooth=1 aa=1 padding=0,0,0,0 spacing={pad},{pad}',
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
    print(f"Built {font_id}: {atlas_w}x{atlas_h}, lineH={line_height}, png={png_kb:.1f} KB")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for fid, h in TIERS:
        build_font_tier(fid, h)


if __name__ == "__main__":
    main()

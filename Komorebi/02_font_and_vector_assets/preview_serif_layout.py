#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""离线复刻 SerifClock.mc 的排版数学，用已产出的 BMFont 字库把大时间画出来。

用途：机器上没有 Connect IQ 模拟器时，靠这张图判断「基线锚点 / 居中 / 三档比例」
是否成立；同时打印版面数字（块宽高、四周留白）供脚本自检是否溢出屏幕。
渲染规则与 CIQ 一致：黑色 = 色键透明，调色板亮度 = 墨迹强度，字形按主题色着色。

    python preview_serif_layout.py            # 输出 progress_shots/日期_F2_serif_layout.png
"""
from __future__ import annotations

import os
import re
import datetime
from PIL import Image, ImageDraw

FONTS_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "01_watchface_app", "resources", "fonts")
)
SHOT_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "progress_shots")
)

# 与 ThemeManager 默认值一致（THEME_PROTOCOL「昼·壱」白练 · 茜素）
THEMES = {
    "AMOLED": dict(bg=0xF3F3F2, hour=0x1C1C1C, min=0xB7282E, sec=0x787878),
    "MIP": dict(bg=0xFFFFFF, hour=0x000000, min=0xAA0000, sec=0x555555),
}

# SerifClock 的档位选择：屏高 >= 380 用 big/mid/mini，否则用 mip_*
BASELINES = {
    "AMOLED 454x454": (454, ("big", "mid", "mini"), "AMOLED"),
    "MIP 260x260": (260, ("mip_big", "mip_mid", "mip_mini"), "MIP"),
}


# ----------------------------------------------------------------------------------
# BMFont 解析（与 CIQ 读 .fnt 的字段一致）
# ----------------------------------------------------------------------------------
class Font:
    def __init__(self, path: str):
        text = open(path, encoding="utf-8").read()
        common = re.search(r"^common .*", text, re.M).group(0)
        self.line_height = int(re.search(r"lineHeight=(\d+)", common).group(1))
        self.base = int(re.search(r"\bbase=(\d+)", common).group(1))
        name = re.search(r'file="([^"]+)"', text).group(1)

        self.chars = {}
        for m in re.finditer(r"^char (.*?)$", text, re.M):
            kv = dict(re.findall(r"(\w+)=(-?\d+)", m.group(1)))
            self.chars[int(kv["id"])] = {
                "x": int(kv["x"]), "y": int(kv["y"]),
                "w": int(kv["width"]), "h": int(kv["height"]),
                "xo": int(kv["xoffset"]), "yo": int(kv["yoffset"]),
                "adv": int(kv["xadvance"]),
            }

        # 字库 PNG 是调色板图：先转 RGB 再取亮度，得到真正的墨迹强度（0~255）。
        # 直接 .convert("L") 会拿到调色板索引（0..3），几乎透明 —— CIQ 同理按亮度取值。
        sheet = Image.open(os.path.join(os.path.dirname(path), name)).convert("RGB").convert("L")
        self.sheet = sheet
        # CIQ antialias="true"：亮度即墨迹强度（0=透明），这里保留 0..255 连续值
        self.ink = {cid: g for cid, g in self.chars.items()}

    def text_width(self, s: str) -> int:          # Dc.getTextWidthInPixels
        return sum(self.chars.get(ord(c), {"adv": 0})["adv"] for c in s)

    def font_height(self) -> int:                 # Dc.getFontHeight（紧单元格契约）
        return self.line_height


def draw_text(canvas: Image.Image, cx: int, cy: int, font: Font, s: str, rgb):
    """复刻 dc.drawText(cx, cy, font, s, TEXT_JUSTIFY_CENTER | TEXT_JUSTIFY_VCENTER)。

    SDK 9.3 无 setTextBaseline()，渲染器只以「中心点」定位；紧字模下 lineHeight == base
    == 数字墨迹高，所以中心点即视觉中心，基线 = cy + base/2。
    """
    x = round(cx - font.text_width(s) / 2)
    y = round(cy + font.base / 2)
    pen = x
    for c in s:
        g = font.ink.get(ord(c))
        if g is None:
            continue                      # 超出 charset：CIQ 同样跳过，前进量已不可靠
        if g["w"] and g["h"]:
            tile = font.sheet.crop((g["x"], g["y"], g["x"] + g["w"], g["y"] + g["h"]))
            # 亮度 → alpha，再按主题色着色（黑底 + 色键即 CIQ 的 antialias 语义）
            layer = Image.new("RGBA", tile.size, rgb + (0,))
            layer.putalpha(tile)
            canvas.alpha_composite(layer, (pen + g["xo"], y - font.base + g["yo"]))
        pen += g["adv"]


# ----------------------------------------------------------------------------------
# SerifClock.draw 的版面复刻（改动渲染器时请同步这里）
# ----------------------------------------------------------------------------------
def draw_clock(canvas: Image.Image, w: int, h: int, fonts, theme: dict) -> dict:
    """与 SerifClock.draw 一一对应的版面复刻（改渲染器时请同步这里）。"""
    font_hour, font_min, font_sec = fonts
    hour_str, min_str, sec_str = "10", "09", "34"

    digit_h = font_hour.font_height()
    min_h = font_min.font_height()
    sec_h = font_sec.font_height()
    ms_gap = max(digit_h - min_h - sec_h, int(digit_h * 0.05))

    hour_w = font_hour.text_width(hour_str)
    colon_w = font_hour.text_width(":")
    min_w = font_min.text_width(min_str)
    sec_w = font_sec.text_width(sec_str)
    gap = int(font_hour.text_width("0") * 0.12)

    hour_block_w = hour_w + colon_w
    total_w = hour_block_w + gap + min_w
    start_x = (w - total_w) // 2
    top_y = (h - digit_h) // 2
    right_x = start_x + hour_block_w + gap
    big_cy = top_y + digit_h / 2

    draw_text(canvas, start_x + hour_w / 2, big_cy, font_hour, hour_str, hex_rgb(theme["hour"]))
    draw_text(canvas, start_x + hour_w + colon_w / 2, big_cy, font_hour, ":", hex_rgb(theme["min"]))

    min_top_y = top_y
    draw_text(canvas, right_x + min_w / 2, min_top_y + min_h / 2, font_min, min_str, hex_rgb(theme["min"]))

    sec_cy = min_top_y + min_h + ms_gap + sec_h / 2
    sec_right = right_x + min_w
    draw_text(canvas, sec_right - sec_w / 2, sec_cy, font_sec, sec_str, hex_rgb(theme["sec"]))

    return dict(digit_h=digit_h, min_h=min_h, sec_h=sec_h, ms_gap=int(ms_gap), total_w=total_w,
                start_x=start_x, top_y=top_y, right_x=right_x, block_bottom=int(sec_cy + sec_h / 2))


def hex_rgb(v: int) -> tuple[int, int, int]:
    return ((v >> 16) & 255, (v >> 8) & 255, v & 255)


def main() -> None:
    os.makedirs(SHOT_DIR, exist_ok=True)
    scale = 2
    tiles = []
    print(f"字库目录：{FONTS_DIR}")
    for label, (side, tiers, theme_key) in BASELINES.items():
        fonts = [Font(os.path.join(FONTS_DIR, f"f2_mincho_biz_{t}.fnt")) for t in tiers]
        theme = THEMES[theme_key]
        canvas = Image.new("RGBA", (side, side), hex_rgb(theme["bg"]) + (255,))
        info = draw_clock(canvas, side, side, fonts, theme)

        over = [k for k, v in (("左溢出", info["start_x"] < 0),
                               ("右溢出", info["start_x"] + info["total_w"] > side),
                               ("上溢出", info["top_y"] < 0),
                               ("下溢出", info["block_bottom"] > side)) if v]
        print(f"{label}: 行高 big/mid/mini = {info['digit_h']}/{info['min_h']}/{info['sec_h']} "
              f"分秒隙={info['ms_gap']} 版面宽={info['total_w']}/{side} "
              f"左右留白={info['start_x']} 上留白={info['top_y']} -> {'OK' if not over else ' / '.join(over)}")

        framed = canvas.convert("RGB").resize((side * scale, side * scale), Image.NEAREST)
        draw = ImageDraw.Draw(framed)
        draw.rectangle([0, 0, side * scale - 1, side * scale - 1], outline=(160, 160, 160))
        draw.text((8, 6), f"{label} · BIZ UDMincho (F2)", fill=(150, 40, 45))
        tiles.append(framed)

    gap_px = 24
    sheet = Image.new("RGB", (tiles[0].width * 2 + gap_px, max(t.height for t in tiles)), (36, 36, 38))
    sheet.paste(tiles[0], (0, 0))
    sheet.paste(tiles[1], (tiles[0].width + gap_px, 0))
    out = os.path.join(SHOT_DIR, f"{datetime.date.today():%Y-%m-%d}_F2_serif_layout.png")
    sheet.save(out)
    print(f"[ok] {out}")


if __name__ == "__main__":
    main()

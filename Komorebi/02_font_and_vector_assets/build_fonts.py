# -*- coding: utf-8 -*-
r"""Komorebi · Partition 2 —— TTF → Connect IQ 自定义字库 (.fnt + .png)

契约（见仓库根 DECISIONS.md / Docs_and_Specs/THEME_PROTOCOL.md）：
  * DEC-004：可见字符固定为「0-9 + 冒号」共 11 个（另配 1 个字宽空格，共 12 个字模），不得扩展；
    单套字库硬上限 8KB。
  * THEME_PROTOCOL：`F2` = 经典衬线 / 宋体·明朝体，本脚本先把 F2 打通。

产物格式为 BMFont Text 版（Garmin Connect IQ 直接吃），排版约定与参考项目
`reference\Segment34mkII\resources\fonts\*.fnt` 一致：
  lineHeight = base = 数字墨迹高度，基线落在字模单元格底部 ——
  于是 Monkey C 侧 `TEXT_BASELINE_FONT_BOTTOM` 就等于数字底边，排版可预测。
CIQ 位图字体不参与缩放，故按 DEC-006 双基准预烘焙六档固定字高（见 tier_heights：
同时受「34% 屏高」与 SegmentClock 的「72% 屏宽」两条版面约束反推）。

用法（在本目录下执行）：
  python build_fonts.py --list                                 # 看候选字体与授权
  python build_fonts.py --preview                              # 出对比图给 F2 选角（默认衬线组）
  python build_fonts.py --emit f2_mincho_biz                   # 全档位写入表盘工程 resources\fonts\
  python build_fonts.py --emit f2_mincho_biz --tiers mip_big   # 只出某一档
"""

from __future__ import annotations

import argparse
import datetime as dt
import io
import os
import sys

from PIL import Image, ImageDraw, ImageFont

# ----------------------------------------------------------------------------------
# 常量：契约相关，改动须同步 DECISIONS.md / THEME_PROTOCOL.md
# ----------------------------------------------------------------------------------
CHARSET = " 0123456789:"          # DEC-004：字宽空格 + 0-9 + 冒号（可见字符恰为 11 个）
VISIBLE_CHAR_COUNT = 11           # DEC-004 契约里的「11 字符」= 10 数字 + 冒号
SIZE_BUDGET_BYTES = 8 * 1024      # DEC-004：单套字库硬上限 8KB

assert sum(1 for c in CHARSET if not c.isspace()) == VISIBLE_CHAR_COUNT, "违反 DEC-004 字符集契约"

# DEC-006 双基准（宽 x 高）。CIQ 位图字体不会缩放，六档数字高度在构建期按基准屏烘死，
# 运行时只按屏幕大小挑档，绝不做拉伸（比例常量与 SegmentClock.mc 保持同步）。
BASELINES = {
    "amoled": (454, 454),     # → big / mid / mini
    "mip":    (260, 260),     # → mip_big / mip_mid / mip_mini
}
DIGIT_H_RATIO = 0.34          # SegmentClock.digitH = h * 0.34（大时字高上限）
MIN_RATIO = 0.72              # 小分字高 = big * 0.72
SEC_RATIO = 0.18              # 迷你秒字高 = big * 0.18
CLOCK_WIDTH_BUDGET = 0.72     # SegmentClock.maxW：大时间组合块横向 ≤ 屏宽 72%
BLOCK_GAP_RATIO = 0.12        # SerifClock：主体与分钟块的呼吸距离 = advance("0") * 0.12
TRACKING_DEFAULT = -0.15      # 明朝体侧余量大，默认收紧字距换回更多字高（--tracking 可覆盖）
TIER_NAMES = ("big", "mid", "mini", "mip_big", "mip_mid", "mip_mini")

# 墨迹灰阶与视觉 Gamma：CIQ antialias="true" 时按亮度做抗锯齿强度。
# 2 = 1-bit 硬边（最省）；4~8 = MIP 反射屏上边缘更稳；GAMMA<1 提亮细笔画。
INK_LEVELS = 4
GAMMA = 0.75

HERE = os.path.dirname(os.path.abspath(__file__))
APP_FONTS_DIR = os.path.normpath(
    os.path.join(HERE, "..", "01_watchface_app", "resources", "fonts")
)
PROGRESS_DIR = os.path.normpath(os.path.join(HERE, "..", "progress_shots"))

WIN_FONTS = r"C:\Windows\Fonts"
USER_FONTS = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Fonts")   # 用户级安装的字体

# ----------------------------------------------------------------------------------
# 候选字体表
#   redistribute=True  : 许可证允许把渲染出的点阵打包进 .prg（OFL / IPA Font License）
#   redistribute=False : 系统自带字体，仅用于「看看效果」的预览，禁止打包发布
#   axes               : 可变字体 (VF) 的设计轴取值
# ----------------------------------------------------------------------------------
CANDIDATES = {
    # ---- F2 衬线 / 宋体·明朝体 -------------------------------------------------
    "f2_mincho_biz": dict(
        group="serif", face="BIZ UDMincho Medium", path=os.path.join(WIN_FONTS, "BIZ-UDMinchoM.ttc"),
        index=0, redistribute=True, license="IPA OFL 1.0（可嵌入）",
        note="日本开源明朝体，笔画比宋体厚实，MIP 反射屏上不易断线（首选）",
    ),
    "f2_serif_notojp": dict(
        group="serif", face="Noto Serif JP Bold", path=os.path.join(WIN_FONTS, "NotoSerifJP-VF.ttf"),
        axes={"wght": 700}, redistribute=True, license="SIL OFL 1.1（可嵌入）",
        note="思源系高对比明朝衬线，细笔画锋利，AMOLED 上最优雅",
    ),
    "f2_serif_notosc": dict(
        group="serif", face="Noto Serif SC Bold", path=os.path.join(WIN_FONTS, "NotoSerifSC-VF.ttf"),
        axes={"wght": 700}, redistribute=True, license="SIL OFL 1.1（可嵌入）",
        note="中文思源宋，横细竖粗对比强，宋体味最正",
    ),
    "f2_mincho_yu": dict(
        group="serif", face="Yu Mincho Demibold", path=os.path.join(WIN_FONTS, "yumindb.ttf"),
        redistribute=False, license="Windows 系统字体（禁止再分发）",
        note="仅预览基准：雅黑同族明朝体，日系腕表感强",
    ),
    "f2_song_xbs": dict(
        group="serif", face="FZXiaoBiaoSong-B05", path=os.path.join(USER_FONTS, "FZXBSK.TTF"),
        redistribute=False, license="方正字体（商用需授权）",
        note="仅预览基准：小标宋，横细竖粗、衬线脚最锐利，标题感最强",
    ),
    "f2_song_fzshusong": dict(
        group="serif", face="FZShuSong-Z01", path=os.path.join(USER_FONTS, "FZSSK.TTF"),
        redistribute=False, license="方正字体（商用需授权）",
        note="仅预览基准：经典书宋，笔画最内敛，正文感强",
    ),
    "f2_song_stzhongsong": dict(
        group="serif", face="STZhongsong", path=os.path.join(WIN_FONTS, "STZHONGS.TTF"),
        redistribute=False, license="Windows 系统字体（禁止再分发）",
        note="仅预览基准：华文中宋，比常规宋体粗半档，小字号更稳",
    ),
    "f2_serif_cambria": dict(
        group="serif", face="Cambria Bold", path=os.path.join(WIN_FONTS, "cambriab.ttf"),
        redistribute=False, license="Windows 系统字体（禁止再分发）",
        note="仅预览基准：西文衬线等高等粗，屏幕可读性标杆",
    ),
    "f2_serif_palatino": dict(
        group="serif", face="Palatino Linotype Bold", path=os.path.join(WIN_FONTS, "palab.ttf"),
        redistribute=False, license="Windows 系统字体（禁止再分发）",
        note="仅预览基准：人文衬线，数字为旧体字（高低错落）",
    ),
    # ---- 对照组：当前表盘用的矢量段码风格 / 无衬线（便于横向比较） --------------
    "f3_sans_bizgothic": dict(
        group="sans", face="BIZ UDGothic Bold", path=os.path.join(WIN_FONTS, "BIZ-UDGothicB.ttc"),
        index=0, redistribute=True, license="IPA OFL 1.0（可嵌入）",
        note="F3 硬派黑体候选，对照组",
    ),
}


# ----------------------------------------------------------------------------------
# 字体加载与度量
# ----------------------------------------------------------------------------------
def load_font(cand: dict, px: int) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(cand["path"], size=px, index=cand.get("index", 0))
    axes = cand.get("axes")
    if axes:
        try:
            font.set_variation_by_axes(list(axes.values()))
        except Exception as exc:  # 非可变字体或轴名不匹配时直接忽略
            print(f"[warn] {cand['face']} 无法应用设计轴 {axes}: {exc}")
    return font


def ink_box(font: ImageFont.FreeTypeFont, ch: str) -> tuple[int, int, int, int]:
    """真实墨迹包围盒（相对基线左端锚点），不依赖 Pillow 的 advance 宽度。

    Pillow 的 textbbox 对部分 CJK/TTC 字体会给出「等于前进量」的横向盒子，
    直接拿来切图会留下大片透明区；这里把字画进亮度图逐像素取极值，得到紧贴的字模。
    """
    if ch.isspace():
        return (0, 0, 0, 0)
    pad = font.size // 2 + 8
    ox, oy = font.size + pad, font.size * 2 + pad      # 落笔点（基线左端）
    im = Image.new("L", (font.size * 3 + 2 * pad, font.size * 4 + 2 * pad), 0)
    ImageDraw.Draw(im).text((ox, oy), ch, font=font, fill=255, anchor="ls")
    bbox = im.getbbox()
    if not bbox:
        return (0, 0, 0, 0)
    return (bbox[0] - ox, bbox[1] - oy, bbox[2] - ox, bbox[3] - oy)


def measure(cand: dict, px: int) -> dict:
    """算出整串字符的排版表：以数字墨迹顶为 y 参考，基线落在单元格底部。"""
    font = load_font(cand, px)
    boxes = {ch: ink_box(font, ch) for ch in CHARSET}
    inked = [b for b in boxes.values() if b[2] > b[0]]     # 只统计真正有墨迹的字模（空格除外）

    digits = [boxes[ch] for ch in CHARSET if ch.isdigit()]
    top_ref = min(b[1] for b in inked)                     # 最高墨迹（相对基线，负值）
    bottom_max = max(b[3] for b in inked)                  # 最低墨迹（含下伸过冲，正值或 0）
    left_min = min(b[0] for b in inked)                    # 最左出锋（可能为负，统一平移进单元格）

    height = max(bottom_max - top_ref, 1)                  # lineHeight == base：字模单元格高
    digit_height = max(
        max(b[3] for b in digits) - min(b[1] for b in digits), 1
    )                                                      # 数字墨迹高（跨字体等大对齐用）
    glyphs = {}
    cursor = 0
    for ch in CHARSET:
        l, t, r, b = boxes[ch]
        w, h = max(r - l, 0), max(b - t, 0)
        adv = int(round(font.getlength(ch)))
        glyphs[ch] = dict(
            sheet_x=cursor, x=l - left_min, y=t - top_ref, width=w, height=h,
            xadvance=max(adv, 1),
        )
        cursor += max(w, 1) + 1                             # 1px 间隔，避免取样渗色
    glyphs[" "]["width"] = 0                               # 空格只贡献前进量（与参考项目 .fnt 写法一致）
    glyphs[" "]["height"] = int(height)
    return dict(font=font, px=px, line_height=int(height), top_ref=int(top_ref),
                baseline_y=-top_ref, digit_height=int(digit_height),
                glyphs=glyphs, sheet_width=max(cursor, 1))


def fit_pixel_size(cand: dict, target_digit_height: int) -> int:
    """二分搜索字号，使数字墨迹高度逼近目标像素高（保证不同字体视觉等大）。"""
    lo, hi = 8, target_digit_height * 3
    best = lo
    for _ in range(14):
        mid = (lo + hi) // 2
        h = measure(cand, mid)["digit_height"]
        if h <= target_digit_height:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
        if lo > hi:
            break
    return best


def clock_width_ratio(cand: dict, tracking: float) -> float:
    """大时间组合块（HH + : + 呼吸距 + MM）的宽度 ÷ 大时字高，与 SerifClock 排版数学一致。"""
    m = measure(cand, 400)                        # 高分辨率量一次比例，缩放不变
    dh = m["digit_height"]

    def adv(ch: str) -> float:
        return max(m["glyphs"][ch]["xadvance"] * (1 + tracking), m["glyphs"][ch]["width"] + 2) / dh

    r_hour = adv("1")
    return 2 * r_hour + adv(":") + BLOCK_GAP_RATIO * r_hour + 2 * MIN_RATIO * r_hour


def tier_heights(cand_key: str, tracking: float = TRACKING_DEFAULT) -> dict[str, int]:
    """六档数字墨迹高度（px）。取「屏高比例上限」与「横向预算上限」的较小值。

    衬线体天然比矢量段码宽（明朝体前进量 ≈ 0.62x 字高 vs 段码 0.46x），
    若只按 34% 屏高烘字，HH:MM 会顶满屏幕两侧并压到上下数据字段，
    因此这里同时遵守 SegmentClock 的 maxW = 72% 屏宽约束。
    """
    cand = CANDIDATES[cand_key]
    ratio = clock_width_ratio(cand, tracking)
    out: dict[str, int] = {}
    for label, (w_px, h_px) in BASELINES.items():
        prefix = "" if label == "amoled" else "mip_"
        by_height = int(h_px * DIGIT_H_RATIO)                       # 纵向：不超过 SegmentClock 字高
        by_width = int(w_px * CLOCK_WIDTH_BUDGET / ratio)           # 横向：不挤占数据字段
        big = max(24, min(by_height, by_width))
        out[prefix + "big"] = big
        out[prefix + "mid"] = max(12, round(big * MIN_RATIO))
        out[prefix + "mini"] = max(8, round(big * SEC_RATIO))
    return out


# ----------------------------------------------------------------------------------
# 产物生成：BMFont .fnt + RGBA .png
# ----------------------------------------------------------------------------------
def render_sheet(metrics: dict, tracking: float) -> Image.Image:
    sheet = Image.new("RGBA", (metrics["sheet_width"], metrics["line_height"]), (0, 0, 0, 0))
    draw = ImageDraw.Draw(sheet)
    font = metrics["font"]
    for ch, g in metrics["glyphs"].items():
        if g["width"] == 0 or g["height"] == 0:
            continue
        # 锚点取基线左端：单元格内墨迹左上角 = (sheet_x + xoffset, yoffset)
        draw.text((g["sheet_x"] + g["x"], metrics["baseline_y"]), ch,
                  font=font, fill=(255, 255, 255, 255), anchor="ls")
    return sheet


def pack_sheet(sheet: Image.Image, levels: int = INK_LEVELS) -> bytes:
    """把 RGBA 字模压成「黑底白字」的调色板 PNG —— CIQ 位图字体的标准形态。

    与 reference\\Segment34mkII 里全部 .png 一致：纯黑 = 透明（CIQ 以黑色为键），
    墨迹亮度 = 绘制强度；antialias="true" 时灰阶即抗锯齿信息。
    2 = 1-bit 硬边（最省）；4~8 在 MIP 反射屏上边缘更稳。用 --ink-levels 调整。
    """
    alpha = sheet.getchannel("A")
    n = max(2, int(levels))
    # 灰度级（256 档）→ 调色板索引：先按 Gamma 还原视觉亮度，再取最近的一档墨迹；
    # Alpha=0 强制落在索引 0（纯黑），避免抗锯齿残影在 CIQ 的黑色色键上显形。
    ramp = [int(round(255.0 * (i / max(n - 1, 1)) ** GAMMA)) for i in range(n)]
    lut = []
    for a in range(256):
        lum = 255.0 * (a / 255.0) ** GAMMA          # Alpha → 目标墨迹亮度（黑=透明）
        best, bi = 1e9, n - 1
        for i, g in enumerate(ramp):
            d = abs(lum - g)
            if d < best:
                best, bi = d, i
        lut.append(bi)
    indexed = alpha.point(lambda a: lut[a] if a > 0 else 0)   # L 图，像素值即调色板索引
    out = Image.new("P", sheet.size)
    out.putpalette([c for g in ramp for c in (g, g, g)] + [0] * (768 - 3 * n))
    out.putdata(list(indexed.get_flattened_data()) if hasattr(indexed, "get_flattened_data")
                else list(indexed.getdata()))
    buf = io.BytesIO()
    out.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def compose(cand_key: str, name: str, digit_height: int, tracking: float,
            ink_levels: int = INK_LEVELS) -> tuple[str, bytes]:
    """产出单个固定尺寸的 .fnt 文本与 .png 位图字节（CIQ 位图字体不缩放）。"""
    cand = CANDIDATES[cand_key]
    px = fit_pixel_size(cand, digit_height)
    metrics = measure(cand, px)

    png_bytes = pack_sheet(render_sheet(metrics, tracking), ink_levels)

    lines = [
        f'info face="{cand["face"]}" size={px} bold=0 italic=0 smooth=1 spacing=1,1',
        f'common lineHeight={metrics["line_height"]} base={metrics["line_height"]} '
        f'scaleW={metrics["sheet_width"]} scaleH={metrics["line_height"]} pages=1',
        f'page id=0 file="{name}.png"',
        f"chars count={len(CHARSET)}",
    ]
    for ch in CHARSET:
        g = metrics["glyphs"][ch]
        # --tracking 收紧字距；下限守住「墨迹宽 + 2px」，避免相邻数字碰在一起
        adv = max(int(round(g["xadvance"] * (1 + tracking))), g["width"] + 2, 1)
        lines.append(
            f'char id={ord(ch)} x={g["sheet_x"]} y=0 width={g["width"]} height={g["height"]} '
            f'xoffset={g["x"]} yoffset={g["y"]} xadvance={adv} page=0'
        )
    fnt_text = "\n".join(lines) + "\n"

    total = len(fnt_text.encode("utf-8")) + len(png_bytes)
    print(
        f"[{name}] {cand['face']} px={px} lineHeight={metrics['line_height']} "
        f"sheet={metrics['sheet_width']}x{metrics['line_height']} "
        f"fnt={len(fnt_text.encode('utf-8'))}B png={len(png_bytes)}B total={total}B"
    )
    if total > SIZE_BUDGET_BYTES:
        raise SystemExit(
            f"[error] {name} 体积 {total}B 超出 DEC-004 单套上限 {SIZE_BUDGET_BYTES}B —— "
            f"可降低该档数字高度（tier_heights 的比例/横向预算）、用 --ink-levels 2 压成硬边，或换更细的字体"
        )
    return fnt_text, png_bytes


def upsert_fonts_xml(outdir: str, names: list[str]) -> None:
    """把字库条目写进 resources/fonts/fonts.xml（已存在则原位替换/追加）。"""
    xml_path = os.path.join(outdir, "fonts.xml")
    entries = {
        n: f'    <font id="{n}" filename="{n}.fnt" antialias="true" filter=" 0123456789:" />'
        for n in names
    }
    if os.path.exists(xml_path):
        with open(xml_path, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        out, seen = [], set()
        for line in lines:
            hit = next((n for n in names if f'id="{n}"' in line), None)
            if hit:
                if hit not in seen:
                    out.append(entries[hit])
                    seen.add(hit)
            else:
                out.append(line)
        new = [n for n in names if n not in seen]
        if new:
            insert_at = next((i for i, l in enumerate(out) if "</fonts>" in l), len(out))
            out[insert_at:insert_at] = [entries[n] for n in new]
        body = "\n".join(out) + "\n"
    else:
        body = "<fonts>\n" + "\n".join(entries[n] for n in names) + "\n</fonts>\n"
    with open(xml_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)


def emit(cand_key: str, tiers: list[str], tracking: float, outdir: str,
         ink_levels: int = INK_LEVELS) -> None:
    cand = CANDIDATES[cand_key]
    if not cand["redistribute"]:
        print(f"[error] {cand_key} 为 {cand['license']}，只能预览，禁止打包进 .prg。"
              f"\n        请改用 --list 中标注「可嵌入」的候选。")
        raise SystemExit(2)
    heights = tier_heights(cand_key, tracking)
    unknown = [t for t in tiers if t not in TIER_NAMES]
    if unknown:
        raise SystemExit(f"[error] 未知档位 {unknown}，可选：{', '.join(TIER_NAMES)}")
    print(f"字高表（宽={CLOCK_WIDTH_BUDGET:.0%}屏宽 / 高={DIGIT_H_RATIO:.0%}屏高 双向拟合，tracking={tracking:+.2f}）："
          + " ".join(f"{t}={heights[t]}" for t in tiers))

    os.makedirs(outdir, exist_ok=True)
    names = []
    total_all = 0
    for tier in tiers:
        name = f"{cand_key}_{tier}"
        fnt_text, png_bytes = compose(cand_key, name, heights[tier], tracking, ink_levels)
        total_all += len(fnt_text.encode("utf-8")) + len(png_bytes)
        with open(os.path.join(outdir, f"{name}.fnt"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(fnt_text)
        with open(os.path.join(outdir, f"{name}.png"), "wb") as fh:
            fh.write(png_bytes)
        names.append(name)

    upsert_fonts_xml(outdir, names)
    print(f"[ok] 写入 {outdir}\\ （{len(names)} 档，合计 {total_all}B），并更新 fonts.xml")
    print("     Monkey C 引用：" + ", ".join(f"Rez.Fonts.{n}" for n in names))


# ----------------------------------------------------------------------------------
# 预览：把候选字体画成真实表盘尺寸，供肉眼挑字
# ----------------------------------------------------------------------------------
THEMES = {
    "昼·壱 F2-B0": dict(bg=(0xF3, 0xF3, 0xF2), hour=(0x1C, 0x1C, 0x1C),
                        minute=(0xB7, 0x28, 0x2E), sec=(0x78, 0x78, 0x78)),
    "夜·弐 F5-B6": dict(bg=(0x0C, 0x0C, 0x0C), hour=(0xF4, 0xDD, 0xA5),
                        minute=(0xCA, 0x7A, 0x2C), sec=(0x9E, 0x94, 0x78)),
}


_FONT_CACHE: dict = {}


def _ui_font(px: int) -> ImageFont.FreeTypeFont:
    key = ("ui", px)
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = ImageFont.truetype(os.path.join(WIN_FONTS, "msyh.ttc"), size=px)
    return _FONT_CACHE[key]


def _metrics(cand: dict, digit_height: int) -> dict:
    """带缓存的「数字墨迹高 → 度量表」。"""
    key = (cand["face"], -digit_height)
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = measure(cand, fit_pixel_size(cand, digit_height))
    return _FONT_CACHE[key]


def _text_width(cand: dict, digit_height: int, text: str) -> int:
    m = _metrics(cand, digit_height)
    return sum(int(round(m["glyphs"][c]["xadvance"])) for c in text if c in m["glyphs"])


def _blit(draw: ImageDraw.ImageDraw, x: int, baseline_y: int, text: str, cand: dict,
          digit_height: int, color: tuple[int, int, int]) -> None:
    """按 .fnt 的排版约定（基线=单元格底部）逐字符绘制，模拟真机 drawText。"""
    m = _metrics(cand, digit_height)
    for ch in text:
        g = m["glyphs"].get(ch)
        if g is None:
            continue
        if g["width"] and g["height"]:
            draw.text((x + g["x"], baseline_y), ch, font=m["font"], fill=color + (255,), anchor="ls")
        x += int(round(g["xadvance"]))


def mock_face(draw: ImageDraw.ImageDraw, ox: int, oy: int, size: int, cand: dict, th: dict,
              hour: str = "10", minute: str = "09", sec: str = "35") -> None:
    """复刻 SegmentClock.draw 的主从排版：时大字居左、分贴右上方、秒迷你垫底，整体居中。"""
    draw.rectangle([ox, oy, ox + size, oy + size], fill=th["bg"] + (255,))

    hour_h = int(size * 0.34)                            # 与 SegmentClock.mc 的 digitH 比例一致
    min_h = int(hour_h * 0.72)
    sec_h = max(int(hour_h * 0.18), 7)

    colon_w = int(_text_width(cand, hour_h, ":"))
    gap = int(_text_width(cand, hour_h, "0") * 0.10)
    hour_block = _text_width(cand, hour_h, hour) + colon_w
    min_block = _text_width(cand, min_h, minute)
    total = hour_block + gap + min_block
    start_x = ox + (size - total) // 2
    baseline = oy + (size + hour_h) // 2                 # 基线=单元格底部 → 数字底边

    _blit(draw, start_x, baseline, hour, cand, hour_h, th["hour"])
    x = start_x + _text_width(cand, hour_h, hour)
    _blit(draw, x, baseline, ":", cand, hour_h, th["minute"])
    x += colon_w + gap
    min_baseline = oy + (size - min_h) // 2 + min_h
    _blit(draw, x, min_baseline, minute, cand, min_h, th["minute"])
    sec_w = _text_width(cand, sec_h, sec)
    _blit(draw, x + min_block - sec_w, min_baseline + int(min_h * 0.62), sec, cand, sec_h, th["sec"])


def preview(group: str, digit_height: int) -> None:
    keys = [k for k, c in CANDIDATES.items() if c["group"] == group and os.path.exists(c["path"])]
    skipped = len([k for k, c in CANDIDATES.items() if c["group"] == group]) - len(keys)
    if skipped:
        print(f"[info] 跳过 {skipped} 套本机不存在的字体")
    os.makedirs(PROGRESS_DIR, exist_ok=True)

    panel, cols, gut = 300, len(THEMES), 26
    row_h = panel + 74
    sheet = Image.new("RGBA", (panel * cols + gut * (cols + 1), row_h * len(keys) + 56),
                      (26, 26, 28, 255))
    d = ImageDraw.Draw(sheet)
    label_font = _ui_font(20)

    for row, key in enumerate(keys):
        cand = CANDIDATES[key]
        y0 = 30 + row * row_h
        tag = "可嵌入" if cand["redistribute"] else "仅预览·不可发布"
        d.text((gut, y0 - 26), f"{key} — {cand['face']} [{tag}]  {cand['note']}",
               fill=(214, 214, 220, 255), font=label_font)
        for col, (tname, th) in enumerate(THEMES.items()):
            ox = gut + col * (panel + gut)
            mock_face(d, ox, y0, panel, cand, th)
            # 数字条：检查 0-9 与冒号的墨迹浓淡是否均匀
            _blit(d, ox + 14, y0 + panel - 12, "0123456789:", cand, 26, th["hour"])
            d.text((ox + 6, y0 + panel + 6), tname, fill=(160, 160, 166, 255), font=_ui_font(16))

    stamp = dt.date.today().isoformat()
    out = os.path.join(PROGRESS_DIR, f"{stamp}_F2_serif_candidates.png")
    sheet.convert("RGB").save(out)
    print(f"[ok] 对比图已输出：{out}   （候选 {len(keys)} 套 × 主题 {cols} 组，面板 {panel}px）")


# ----------------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description="Komorebi TTF → Connect IQ 字库构建器（仅 0-9 : ，≤8KB）")
    ap.add_argument("--list", action="store_true", help="列出候选字体与授权状态")
    ap.add_argument("--preview", action="store_true", help="生成肉眼挑字用的对比图")
    ap.add_argument("--group", default="serif", help="预览分组：serif / sans（默认 serif）")
    ap.add_argument("--emit", metavar="KEY", help="构建指定字体的全部档位并写入表盘工程 resources\\fonts\\")
    ap.add_argument("--tiers", default="big,mid,mini,mip_big,mip_mid,mip_mini",
                    help="逗号分隔的档位（默认全部），如 --tiers mip_big")
    ap.add_argument("--outdir", default=APP_FONTS_DIR, help="输出目录（默认表盘工程 resources\\fonts）")
    ap.add_argument("--height", type=int, default=150, help="预览图数字高度 px（仅 --preview 用）")
    ap.add_argument("--tracking", type=float, default=TRACKING_DEFAULT,
                    help=f"字距比例，负值收紧（默认 {TRACKING_DEFAULT:+.2f}；字号会按横向预算自动反推）")
    ap.add_argument("--ink-levels", type=int, default=INK_LEVELS,
                    help=f"墨迹灰阶数（2=1-bit 硬边，越大体积分越大，默认 {INK_LEVELS}）")
    args = ap.parse_args()

    missing = [k for k, c in CANDIDATES.items() if not os.path.exists(c["path"])]
    if missing:
        print(f"[warn] 本机缺少字体文件：{', '.join(missing)}（已跳过）")

    if args.list or not (args.preview or args.emit):
        print(f"字符集契约：'0-9 :' = {VISIBLE_CHAR_COUNT} 个可见字符（另配空格字模，共 {len(CHARSET)} 个）"
              f"| 单套体积上限 {SIZE_BUDGET_BYTES}B")
        print(f"版面约束：大时字高 ≤ {DIGIT_H_RATIO:.0%}屏高，组合块宽 ≤ {CLOCK_WIDTH_BUDGET:.0%}屏宽"
              f"| 基准 {BASELINES['amoled'][0]}x{BASELINES['amoled'][1]} / {BASELINES['mip'][0]}x{BASELINES['mip'][1]}"
              "（数字高度由这两条反推，见 tier_heights）\n")
        for k, c in CANDIDATES.items():
            flag = "OK " if c["redistribute"] else "预览"
            here = "" if os.path.exists(c["path"]) else "  ←本机缺失"
            fit = ""
            if c["redistribute"] and not here:
                th = tier_heights(k, args.tracking)
                fit = "  字高 big/mid/mini=" + "/".join(str(th[t]) for t in ("big", "mid", "mini")) \
                      + "  mip=" + "/".join(str(th[t]) for t in ("mip_big", "mip_mid", "mip_mini"))
            print(f"{flag:4s} {k:24s} {c['face']:26s} {c['license']}{fit}{here}")
        if not (args.preview or args.emit):
            print("\n下一步：--preview 看效果，或 --emit f2_mincho_biz 产出字库。")
        return

    if args.preview:
        preview(args.group, args.height)
    if args.emit:
        emit(args.emit, [t.strip() for t in args.tiers.split(",") if t.strip()],
             args.tracking, args.outdir, args.ink_levels)


if __name__ == "__main__":
    main()

"""版面对账：把 preview_serif_layout.py 画出的图与它自己算的版面数字做像素级比对。

验证的是「切片 + 居中公式 + 缩放」三者自洽（脚本复刻是否真的按数学落墨）；
CIQ 端真实绘制仍需模拟器 / 真机确认（本机无模拟器）。

    python check_serif_layout.py        # 全 PASS 退出码 0，否则 1
"""
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, r"D:\Garmin\Komorebi\02_font_and_vector_assets")
import preview_serif_layout as pv   # noqa: E402

SHOT = os.path.join(pv.SHOT_DIR, f"{__import__('datetime').date.today():%Y-%m-%d}_F2_serif_layout.png")
SIDE = 454
SCALE = 2
TOL = 3
# 只统计表盘内部：外圈是 1px 灰边框，左上是说明文字（灰色系），会污染色块包围盒
REGION = (10, 40, SIDE - 10, SIDE - 10)
SEC_EXCLUDE_DILATE = 5      # 截图放大 2x，5px ≈ 基准 2.5px：足够盖住深色笔画的抗锯齿毛边


def _dilate(mask: np.ndarray, radius: int) -> np.ndarray:
    """简易膨胀：把掩膜向外扩张 radius 像素（用于排除深色笔画的抗锯齿过渡环）。"""
    out = mask.copy()
    for _ in range(radius):
        shifted = out.copy()
        shifted[1:, :] |= out[:-1, :]
        shifted[:-1, :] |= out[1:, :]
        shifted[:, 1:] |= out[:, :-1]
        shifted[:, :-1] |= out[:, 1:]
        out = shifted
    return out


def color_mask(tile: np.ndarray, color_int: int, exclude_near=None, dilate: int = SEC_EXCLUDE_DILATE,
               window=None):
    """接近指定主题色的墨迹掩膜；exclude_near 命中的区域先膨胀 dilate 像素再从结果中扣除。

    秒钟是灰色（#787878），而深色小时笔画的抗锯齿过渡环正好也落在这族灰度上，
    不排除就会把「10」的毛边当成秒字墨迹，包围盒彻底失真。
    window=(x0,y0,x1,y1)：只看这块基准像素窗口（用来把同色的冒号从「分钟」里摘出去）。
    """
    target = np.array(pv.hex_rgb(color_int), dtype=int)
    bg = np.array(pv.hex_rgb(pv.THEMES["AMOLED"]["bg"]), dtype=int)
    arr = tile[:, :, :3].astype(int)
    mask = (np.abs(arr - target).sum(axis=2) < 150) & (np.abs(arr - bg).sum(axis=2) >= 90)
    x0, y0, x1, y1 = window or REGION
    keep = np.zeros_like(mask)
    keep[y0 * SCALE:y1 * SCALE, x0 * SCALE:x1 * SCALE] = True
    mask &= keep
    if exclude_near is not None:
        mask &= ~_dilate(exclude_near, dilate)
    return mask


def bbox_of(mask: np.ndarray):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return (xs.min() / SCALE, ys.min() / SCALE, xs.max() / SCALE + 1 / SCALE, ys.max() / SCALE + 1 / SCALE)


def main() -> None:
    img = Image.open(SHOT).convert("RGB")
    if img.size != (SIDE * SCALE * 2 + 24, SIDE * SCALE):
        raise SystemExit(f"[error] 预览图尺寸异常：{img.size}，请先运行 preview_serif_layout.py")
    tile = np.asarray(img.crop((0, 0, SIDE * SCALE, SIDE * SCALE)))

    fonts = [pv.Font(os.path.join(pv.FONTS_DIR, f"f2_mincho_biz_{t}.fnt"))
             for t in ("big", "mid", "mini")]
    canvas = Image.new("RGBA", (SIDE, SIDE), (*pv.hex_rgb(pv.THEMES["AMOLED"]["bg"]), 255))
    info = pv.draw_clock(canvas, SIDE, SIDE, fonts, pv.THEMES["AMOLED"])
    hour_w = fonts[0].text_width("10")

    th = pv.THEMES["AMOLED"]
    hour_mask = color_mask(tile, th["hour"])
    min_union_mask = color_mask(tile, th["min"])     # 冒号与分钟同色 → 并集（只用于「在右侧」断言）
    # 分钟单独量：冒号用 big 档绘制、下缘更低，混进来会把「分钟底边」拉低几十像素
    min_w = fonts[1].text_width("09")
    min_only_mask = color_mask(tile, th["min"], window=(int(info["right_x"]), 0,
                                                        int(info["right_x"] + min_w) + 2, SIDE))
    hour_box = bbox_of(hour_mask)
    min_union_box = bbox_of(min_union_mask)
    min_box = bbox_of(min_only_mask)
    if not hour_box or not min_box:
        raise SystemExit("[error] 图中找不到小时或分钟墨迹，先跑 preview_serif_layout.py")
    # 秒钟：灰色墨迹，先剔掉深色时/分笔画的抗锯齿毛边，否则包围盒会被污染
    sec_mask = color_mask(tile, th["sec"], exclude_near=hour_mask | min_union_mask)
    if sec_mask.sum() == 0:
        raise SystemExit("[error] 剔除毛边后找不到秒钟墨迹，检查 preview_serif_layout 是否画了秒")
    sec_box = bbox_of(sec_mask)

    print(f"版面：宽={info['total_w']} start_x={info['start_x']} top_y={info['top_y']} "
          f"字高={info['digit_h']}/{info['min_h']}/{info['sec_h']} 分秒隙={info['ms_gap']}")
    print(f"墨迹盒  小时={tuple(round(v) for v in hour_box)} 分钟={tuple(round(v) for v in min_box)} "
          f"冒号并集={tuple(round(v) for v in min_union_box)} 秒钟={tuple(round(v) for v in sec_box)}")

    min_cell_bottom = info["top_y"] + info["min_h"]
    rows = [
        ("小时左缘落在单元格内", hour_box[0], info["start_x"], lambda g, w: g >= w - TOL),
        ("小时右缘不越单元格", hour_box[2], info["start_x"] + hour_w, lambda g, w: g <= w + TOL),
        ("小时顶边 ≈ 版面顶边", hour_box[1], info["top_y"], lambda g, w: abs(g - w) <= TOL + 1),
        ("小时底边 ≈ 顶边+字高", hour_box[3], info["top_y"] + info["digit_h"], lambda g, w: abs(g - w) <= TOL + 1),
        ("冒号/分钟在小时右侧", min_union_box[0], hour_box[2], lambda g, w: g > w),
        ("分钟顶边 ≈ 版面顶边", min_box[1], info["top_y"], lambda g, w: abs(g - w) <= TOL + 1),
        ("秒字贴在分钟单元格下方", sec_box[1], min_cell_bottom + info["ms_gap"], lambda g, w: abs(g - w) <= TOL + 2),
        ("秒钟右缘对齐分钟块", sec_box[2], info["right_x"] + min_w, lambda g, w: abs(g - w) <= 6),
    ]
    ok = True
    for name, got, want, judge in rows:
        good = judge(got, want)
        ok &= good
        print(f"  [{'PASS' if good else 'FAIL'}] {name}: got={got:.0f} want≈{want:.0f}")

    print("\n像素级版面对账：" + ("全部通过（复刻与数学一致）" if ok else "存在偏差，见上"))
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()

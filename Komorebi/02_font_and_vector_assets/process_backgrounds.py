import os
from collections import deque
import numpy as np
from PIL import Image, ImageFilter

RAW_DIR = r"D:\Garmin\Komorebi\02_font_and_vector_assets\sd_raw"
OUT_HD_DIR = r"D:\Garmin\Komorebi\02_font_and_vector_assets\processed_rgba"
OUT_WATCH_DIR = r"D:\Garmin\Komorebi\01_watchface_app\resources\drawables"
PREVIEW_OUT = r"C:\Users\SHIZUKI\.gemini\antigravity\brain\0bd6e646-035f-4ddd-9257-c31f73b31512\transparent_check_preview.png"

WATCH_SIZE = (360, 135)

def estimate_paper_color(rgb: np.ndarray) -> np.ndarray:
    border = np.concatenate([rgb[0, :], rgb[-1, :], rgb[:, 0], rgb[:, -1]], axis=0)
    lum = border.mean(axis=1)
    sat = border.max(axis=1) - border.min(axis=1)
    cand = border[(lum > 220) & (sat < 25)]
    if len(cand) > 20:
        return np.median(cand, axis=0)
    return np.array([246.0, 244.0, 238.0], dtype=np.float32)


def remove_paper_background(img: Image.Image) -> Image.Image:
    """
    Watercolor-aware paper removal:
    1. Global soft alpha for flat/near-paper pixels (solves enclosed skies in b4/b5/b6).
    2. Protects high-saturation colors and dark ink strokes at full opacity.
    3. Protects interior snow/foam whites that sit inside dark/colored regions (not large flat paper).
    4. Smooth watercolor mist transparency + edge fade.
    """
    rgba = img.convert("RGBA")
    arr = np.array(rgba, dtype=np.float32)
    rgb = arr[:, :, :3]
    h, w, _ = rgb.shape

    bg_color = estimate_paper_color(rgb)
    diff = np.linalg.norm(rgb - bg_color[None, None, :], axis=2)
    lum = rgb.mean(axis=2)
    sat = rgb.max(axis=2) - rgb.min(axis=2)

    # 1. Identify large flat paper/sky regions globally via local variance + paper similarity
    #    (snow caps and sea foam are small/textured near ink lines; open sky is smooth & bright)
    gray = Image.fromarray(np.clip(lum, 0, 255).astype(np.uint8), mode="L")
    blur_small = np.array(gray.filter(ImageFilter.GaussianBlur(radius=6)), dtype=np.float32)
    local_var = np.abs(lum - blur_small)

    # Base alpha from color distance & saturation:
    # - High saturation (sat > 30) or dark ink (lum < 150) => opaque
    # - Near paper color (diff < 22) and low saturation (sat < 20) => transparent
    alpha_dist = np.clip((diff - 18.0) / 55.0, 0.0, 1.0)
    alpha_sat = np.clip((sat - 14.0) / 28.0, 0.0, 1.0)
    alpha_dark = np.clip((215.0 - lum) / 75.0, 0.0, 1.0)

    # Combine: keep if colorful OR dark OR textured interior white near ink
    alpha = np.maximum(alpha_sat, alpha_dark)
    alpha = np.maximum(alpha, alpha_dist * 0.85)

    # Protect small enclosed bright whites (like Fuji snow cap / wave foam) where local texture > 4.5
    # while letting smooth large open skies (b4 middle, b6 inside moon) go fully transparent
    smooth_sky = (diff < 26.0) & (sat < 22.0) & (local_var < 4.5)
    alpha[smooth_sky] = 0.0

    # Smooth the alpha mask slightly for seamless watercolor edges
    alpha_img = Image.fromarray(np.clip(alpha * 255.0, 0, 255).astype(np.uint8), mode="L")
    alpha_img = alpha_img.filter(ImageFilter.GaussianBlur(radius=1.0))
    alpha = np.array(alpha_img, dtype=np.float32) / 255.0

    # Re-enforce 0 alpha on very clean paper areas so dark themes have zero haze
    alpha[(diff < 16.0) & (sat < 16.0)] = 0.0

    # Gentle edge feathering on top (18%), bottom (22%), and sides (8%) so there's no hard rectangle cut
    y_grad = np.ones((h, 1), dtype=np.float32)
    top_fade_h = int(h * 0.18)
    bot_fade_h = int(h * 0.22)
    y_grad[:top_fade_h, 0] = np.linspace(0.0, 1.0, top_fade_h) ** 1.5
    y_grad[-bot_fade_h:, 0] = np.linspace(1.0, 0.0, bot_fade_h) ** 1.5

    x_grad = np.ones((1, w), dtype=np.float32)
    side_fade_w = int(w * 0.08)
    x_grad[0, :side_fade_w] = np.linspace(0.0, 1.0, side_fade_w) ** 1.3
    x_grad[0, -side_fade_w:] = np.linspace(1.0, 0.0, side_fade_w) ** 1.3

    alpha = alpha * y_grad * x_grad

    # Un-premultiply paper tint from semi-transparent watercolor edges (eliminates white halo on dark bg)
    out_rgb = rgb.copy()
    semi = (alpha > 0.02) & (alpha < 0.92)
    for c in range(3):
        est = (rgb[:, :, c] - bg_color[c] * (1.0 - alpha)) / np.maximum(alpha, 0.20)
        out_rgb[:, :, c] = np.where(semi, np.clip(est, 0, 255), rgb[:, :, c])

    out_arr = np.dstack([
        np.clip(out_rgb, 0, 255).astype(np.uint8),
        np.clip(alpha * 255.0, 0, 255).astype(np.uint8)
    ])
    return Image.fromarray(out_arr, mode="RGBA")


def main():
    os.makedirs(OUT_HD_DIR, exist_ok=True)
    os.makedirs(OUT_WATCH_DIR, exist_ok=True)

    processed_watch = []
    names = ["b1", "b2", "b3", "b4", "b5", "b6"]

    for idx, name in enumerate(names, start=1):
        in_path = os.path.join(RAW_DIR, f"{name}.png")
        if not os.path.exists(in_path):
            continue

        src = Image.open(in_path)
        hd_rgba = remove_paper_background(src)
        hd_out = os.path.join(OUT_HD_DIR, f"{name}_rgba.png")
        hd_rgba.save(hd_out, optimize=True)

        watch_rgba = hd_rgba.resize(WATCH_SIZE, Image.Resampling.LANCZOS)
        watch_out = os.path.join(OUT_WATCH_DIR, f"bg_{idx}.png")
        watch_rgba.save(watch_out, optimize=True)

        size_kb = os.path.getsize(watch_out) / 1024.0
        print(f"bg_{idx}.png -> {size_kb:.1f} KB")
        processed_watch.append((name, watch_rgba))

    if processed_watch:
        cw, ch = WATCH_SIZE
        pad = 16
        sheet = Image.new("RGB", (cw * 2 + pad * 3, (ch + pad) * len(processed_watch) + pad), "#22252A")
        for row, (name, im) in enumerate(processed_watch):
            y = pad + row * (ch + pad)
            day_bg = Image.new("RGB", (cw, ch), "#F3F3F2")
            day_bg.paste(im, (0, 0), im)
            sheet.paste(day_bg, (pad, y))
            night_bg = Image.new("RGB", (cw, ch), "#0B1013")
            night_bg.paste(im, (0, 0), im)
            sheet.paste(night_bg, (pad * 2 + cw, y))
        sheet.save(PREVIEW_OUT)


if __name__ == "__main__":
    main()

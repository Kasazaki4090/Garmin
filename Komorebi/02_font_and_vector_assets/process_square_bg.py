import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SQUARE_DIR = r"D:\Garmin\Komorebi\02_font_and_vector_assets\sd_raw\Square"
OUT_WATCH_DIR = r"D:\Garmin\Komorebi\01_watchface_app\resources\drawables"

SIZE = 454


def apply_readability_mist_mask(img: Image.Image) -> Image.Image:
    """
    Keep the full-screen 454x454 square watercolor artwork 100% continuous,
    but apply a super-soft paper-mist lift behind:
      1. Top status bar (y ~ 0.13)
      2. Center-upper clock hollow zone (y ~ 0.24..0.58)
      3. Bottom 2x2 data zone (y ~ 0.77..0.90)
    so dark/crimson digits & icons stay crisp without any ugly hard cutout box!
    """
    rgb = img.convert("RGB").resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    arr = np.array(rgb, dtype=np.float32)

    # Sample bright paper tint from top-center sky
    top_strip = arr[int(SIZE * 0.08):int(SIZE * 0.18), int(SIZE * 0.30):int(SIZE * 0.70)]
    paper_tint = np.percentile(top_strip.reshape(-1, 3), 85, axis=0)
    paper_tint = np.clip(paper_tint, 225.0, 250.0)

    # Build soft readability mask (0 = original artwork, 1 = soft mist lift)
    mask_img = Image.new("L", (SIZE, SIZE), 0)
    md = ImageDraw.Draw(mask_img)

    # 1. Clock zone soft ellipse
    md.ellipse([int(SIZE * 0.10), int(SIZE * 0.22), int(SIZE * 0.90), int(SIZE * 0.57)], fill=145)
    # 2. Top data zone soft pill
    md.rounded_rectangle([int(SIZE * 0.18), int(SIZE * 0.08), int(SIZE * 0.82), int(SIZE * 0.19)], radius=24, fill=140)
    # 3. Bottom data zone soft pill
    md.rounded_rectangle([int(SIZE * 0.22), int(SIZE * 0.74), int(SIZE * 0.78), int(SIZE * 0.92)], radius=32, fill=155)

    # Heavy Gaussian blur for zero visible border
    mask_soft = mask_img.filter(ImageFilter.GaussianBlur(radius=24))
    m = (np.array(mask_soft, dtype=np.float32) / 255.0)[:, :, None]

    # Blend artwork gently toward paper_tint in masked zones
    out = arr * (1.0 - m) + paper_tint[None, None, :] * m
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), mode="RGB")


def main():
    os.makedirs(OUT_WATCH_DIR, exist_ok=True)
    for idx in range(1, 7):
        in_path = os.path.join(SQUARE_DIR, f"b{idx}.png")
        if not os.path.exists(in_path):
            print(f"Missing: {in_path}")
            continue
        im = Image.open(in_path)
        out_im = apply_readability_mist_mask(im)
        out_path = os.path.join(OUT_WATCH_DIR, f"bg_{idx}.png")
        # Save as optimized RGB PNG (Garmin compiler automatically quantizes cleanly)
        out_im.save(out_path, optimize=True)
        kb = os.path.getsize(out_path) / 1024.0
        print(f"Saved full-screen bg_{idx}.png ({SIZE}x{SIZE}, {kb:.1f} KB)")


if __name__ == "__main__":
    main()

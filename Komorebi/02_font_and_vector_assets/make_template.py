import os
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = r"D:\Garmin\Komorebi\02_font_and_vector_assets"
TEMPLATE_CLEAN = os.path.join(OUT_DIR, "watchface_template_1024.png")
TEMPLATE_GUIDE = r"C:\Users\SHIZUKI\.gemini\antigravity\brain\0bd6e646-035f-4ddd-9257-c31f73b31512\watchface_template_guide.png"

S = 1024
CX, CY = S // 2, S // 2


def build_templates():
    # 1. Clean template for Flux / ControlNet / Inpainting:
    #    - Pure white (#FFFFFF) inside the safe text/clock/arcs zones (keep clean!)
    #    - Light grey (#E0E4E8) in the "artistic illustration ring & bottom stage" where scenery can grow
    #    - Black (#000000) outside the circular watch screen
    clean = Image.new("RGB", (S, S), (0, 0, 0))
    cd = ImageDraw.Draw(clean)

    # Full circular watch screen base = light grey (art zone)
    r_screen = 492
    cd.ellipse([CX - r_screen, CY - r_screen, CX + r_screen, CY + r_screen], fill=(225, 228, 232))

    # Left & Right progress arc channels (inner & outer ring padding)
    # Keep a clean white channel for left/right arcs (r = 455..485, left 135..225 deg, right -45..45 deg)
    arc_pad = 40
    cd.pieslice([CX - 488, CY - 488, CX + 488, CY + 488], start=132, end=228, fill=(255, 255, 255))
    cd.pieslice([CX - 488, CY - 488, CX + 488, CY + 488], start=-48, end=48, fill=(255, 255, 255))
    # Restore inner art zone inside r=436
    cd.ellipse([CX - 436, CY - 436, CX + 436, CY + 436], fill=(225, 228, 232))

    # Top status bar safe zone (battery, date, temp)
    cd.rounded_rectangle([210, 68, 814, 175], radius=45, fill=(255, 255, 255))

    # Center HUGE clock hollow zone (HH:MM + SS) — generous clean white stage!
    # x: 110..914, y: 195..580
    cd.rounded_rectangle([105, 195, 919, 575], radius=95, fill=(255, 255, 255))

    # Bottom 4-data matrix safe zone
    cd.rounded_rectangle([240, 770, 784, 938], radius=55, fill=(255, 255, 255))

    clean.save(TEMPLATE_CLEAN)

    # 2. Visual guide with clear annotations so the user can inspect exact layout
    guide = clean.copy()
    gd = ImageDraw.Draw(guide)

    # Draw watch bezel ring
    gd.ellipse([CX - 492, CY - 492, CX + 492, CY + 492], outline=(90, 95, 105), width=4)

    # Dashed/colored zone outlines
    gd.rounded_rectangle([210, 68, 814, 175], radius=45, outline=(70, 130, 180), width=3)
    gd.rounded_rectangle([105, 195, 919, 575], radius=95, outline=(183, 40, 46), width=4)
    gd.rounded_rectangle([240, 770, 784, 938], radius=55, outline=(70, 130, 180), width=3)

    # Left & Right progress arcs visualization
    gd.arc([CX - 472, CY - 472, CX + 472, CY + 472], start=138, end=222, fill=(46, 160, 140), width=14)
    gd.arc([CX - 472, CY - 472, CX + 472, CY + 472], start=-42, end=42, fill=(183, 40, 46), width=14)

    try:
        font_lg = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 36)
        font_sm = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 24)
        font_clk = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 210)
    except:
        font_lg = ImageFont.load_default()
        font_sm = font_lg
        font_clk = font_lg

    gd.text((CX, 122), "TOP ZONE: 50%   11/22   17°C", fill=(70, 130, 180), font=font_sm, anchor="mm")
    gd.text((CX - 110, 385), "12:34", fill=(215, 215, 218), font=font_clk, anchor="mm")
    gd.text((CX + 265, 455), "56", fill=(215, 215, 218), font=font_lg, anchor="mm")
    gd.text((CX, 225), "CLOCK HOLLOW ZONE (纯白留空区: 放超大 Mono 时钟)", fill=(183, 40, 46), font=font_sm, anchor="mm")
    gd.text((CX, 675), "MAIN SCENERY STAGE (主插画区: 山/海/竹/猫环绕底部与两侧)", fill=(80, 90, 105), font=font_lg, anchor="mm")
    gd.text((CX, 855), "BOTTOM DATA: HR 80 | BB 88 | 6.4k | 35", fill=(70, 130, 180), font=font_sm, anchor="mm")

    guide.resize((720, 720), Image.Resampling.LANCZOS).save(TEMPLATE_GUIDE)
    print("Saved:", TEMPLATE_CLEAN)
    print("Saved:", TEMPLATE_GUIDE)


if __name__ == "__main__":
    build_templates()

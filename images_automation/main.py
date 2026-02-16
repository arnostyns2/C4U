from PIL import Image, PngImagePlugin
import os
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIGURATIE
# ─────────────────────────────────────────────

INPUT_FOLDER  = "fotos"
OUTPUT_FOLDER = "output"
ICON_FILE     = "icon.png"

LOGO_SCALE = 0.08
MARGIN     = 20
UPSCALE_FACTOR = 1.15

BASE_NAME = "c4u-studio"

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG"}

# ─────────────────────────────────────────────
# SEO METADATA
# ─────────────────────────────────────────────

BRAND_NAME = "C4U Studio"
YEAR = datetime.now().year

IMAGE_TITLE = "Minimal Sculptural Easter Decor Piece"
IMAGE_DESCRIPTION = (
    "Modern architectural bunny ornament created using digital fabrication. "
    "A minimal sculptural decor object designed by C4U Studio."
)
IMAGE_KEYWORDS = (
    "minimal decor, modern easter decor, scandinavian decoration, "
    "design ornament, sculptural object, C4U Studio"
)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def upscale_image(img, factor):
    if factor == 1.0:
        return img
    new_width  = int(img.width * factor)
    new_height = int(img.height * factor)
    return img.resize((new_width, new_height), Image.LANCZOS)


def add_logo(photo, logo, scale, margin):
    photo = photo.convert("RGBA")

    logo_width  = int(photo.width * scale)
    logo_height = int(logo.height * (logo_width / logo.width))

    logo_resized = logo.resize((logo_width, logo_height), Image.LANCZOS)

    x = photo.width  - logo_width  - margin
    y = margin

    mask = logo_resized.split()[3] if logo_resized.mode == "RGBA" else None
    photo.paste(logo_resized, (x, y), mask)

    return photo


def add_png_metadata():
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Title", IMAGE_TITLE)
    meta.add_text("Description", IMAGE_DESCRIPTION)
    meta.add_text("Author", BRAND_NAME)
    meta.add_text("Copyright", f"© {YEAR} {BRAND_NAME}")
    meta.add_text("Keywords", IMAGE_KEYWORDS)
    return meta


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    if not os.path.isdir(INPUT_FOLDER):
        print(f"❌  Map '{INPUT_FOLDER}' niet gevonden.")
        return

    if not os.path.isfile(ICON_FILE):
        print(f"❌  '{ICON_FILE}' niet gevonden naast main.py.")
        return

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    logo = Image.open(ICON_FILE).convert("RGBA")
    print("✅ Logo geladen")

    all_files = [
        f for f in os.listdir(INPUT_FOLDER)
        if os.path.splitext(f)[1] in SUPPORTED_EXTENSIONS
    ]

    if not all_files:
        print("⚠️ Geen afbeeldingen gevonden.")
        return

    counter = 1

    for filename in sorted(all_files):
        input_path   = os.path.join(INPUT_FOLDER, filename)
        original_ext = os.path.splitext(filename)[1].lower()

        save_ext = ".jpg" if original_ext in {".jpeg", ".webp"} else original_ext
        new_name = f"{BASE_NAME}-{counter}{save_ext}"
        output_path = os.path.join(OUTPUT_FOLDER, new_name)

        try:
            img = Image.open(input_path)

            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA")

            img = upscale_image(img, UPSCALE_FACTOR)
            img = add_logo(img, logo, LOGO_SCALE, MARGIN)

            if save_ext == ".png":
                meta = add_png_metadata()
                img.save(output_path, "PNG", pnginfo=meta, optimize=True)

            else:
                img_rgb = img.convert("RGB")
                img_rgb.save(
                    output_path,
                    "JPEG",
                    quality=92,
                    optimize=True
                )

            print(f"✅ {filename} → {new_name}")
            counter += 1

        except Exception as e:
            print(f"❌ Fout bij {filename}: {e}")

    print("\n✨ Klaar! Metadata + logo + upscale toegepast.")


if __name__ == "__main__":
    main()

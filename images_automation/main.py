

from PIL import Image
import os

# ─────────────────────────────────────────────
# CONFIGURATIE
# ─────────────────────────────────────────────

INPUT_FOLDER  = "fotos"
OUTPUT_FOLDER = "output"
ICON_FILE     = "icon.png"

LOGO_SCALE = 0.08   # 8% van de breedte van de foto → klein maar zichtbaar
MARGIN     = 20     # pixels van de rand

SEO_NAMES = [
    "c4u-studio-3d-print",
    "c4u-studio-custom-figurine",
    "c4u-studio-3d-model",
    "c4u-studio-custom-design",
    "c4u-studio-handmade-model",
    "c4u-studio-3d-printed-art",
    "c4u-studio-miniature",
    "c4u-studio-custom-3d-figurine",
    "c4u-studio-resin-print",
    "c4u-studio-Belgium",
    "c4u-studio-personalized-gift",
    "c4u-studio-creative-print",
    "c4u-studio-design-studio",
    "c4u-studio-3d-product",
    "c4u-studio-unique-figurine",
]

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG"}

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def get_unique_name(base_name, extension, used_names):
    candidate = f"{base_name}{extension}"
    if candidate not in used_names:
        return candidate
    counter = 1
    while True:
        candidate = f"{base_name}-{counter}{extension}"
        if candidate not in used_names:
            return candidate
        counter += 1

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
    print(f"✅  Logo geladen")

    all_files = [f for f in os.listdir(INPUT_FOLDER)
                 if os.path.splitext(f)[1] in SUPPORTED_EXTENSIONS]

    if not all_files:
        print(f"⚠️  Geen afbeeldingen gevonden in '{INPUT_FOLDER}'.")
        return

    print(f"📂  {len(all_files)} foto(s) gevonden.\n")

    used_names = set()
    seo_index  = 0
    success    = 0

    for filename in sorted(all_files):
        input_path   = os.path.join(INPUT_FOLDER, filename)
        original_ext = os.path.splitext(filename)[1].lower()
        save_ext     = ".jpg" if original_ext in {".jpeg", ".webp"} else original_ext

        base_name = SEO_NAMES[seo_index % len(SEO_NAMES)]
        seo_index += 1
        new_name  = get_unique_name(base_name, save_ext, used_names)
        used_names.add(new_name)

        output_path = os.path.join(OUTPUT_FOLDER, new_name)

        try:
            img = Image.open(input_path)
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA")

            img_with_logo = add_logo(img, logo, LOGO_SCALE, MARGIN)

            if save_ext == ".png":
                img_with_logo.save(output_path, "PNG", optimize=True)
            else:
                img_with_logo.convert("RGB").save(output_path, "JPEG", quality=92, optimize=True)

            print(f"  ✅  {filename:40s}  →  {new_name}")
            success += 1

        except Exception as e:
            print(f"  ❌  {filename}  →  FOUT: {e}")

    print(f"\n─────────────────────────────────────────")
    print(f"  Klaar! {success} foto(s) verwerkt → '{OUTPUT_FOLDER}/'")

if __name__ == "__main__":
    main()

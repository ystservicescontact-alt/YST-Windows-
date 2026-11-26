"""Prepares photos for the animated explainers (run by hand, outputs are committed).

python3 tools/explainer_assets.py <scene> <source photo>
Writes src/photos/explainers/<scene>.jpg (the photo, cropped), <scene>-bg.jpg (blurred backdrop)
and, for scenes with a moving part, the cut-out sprite plus a photo with that part removed.
"""
import sys
from pathlib import Path
import numpy as np
import cv2
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw

OUT = Path(__file__).resolve().parent.parent / "src" / "photos" / "explainers"

# crop box in source pixels; photo is scaled so its height is 750 stage units (portrait) or fills 1200x750
SCENES = {
    "fapim": {"crop": (0, 300, 1512, 1900),
              "sprites": [
                  # the lever and neck of the handle rotate (the photo underneath is inpainted)
                  {"name": "sprite", "inpaint": True,
                   "poly": [(1140, 1128), (1228, 1128), (1224, 1185), (1198, 1442), (1172, 1474), (1104, 1474),
                            (1098, 1430), (1046, 1432), (1040, 1318), (1112, 1316), (1128, 1160)],
                   "box": (1030, 1110, 1240, 1490)},
                  # the open sash, stretched down from the top until the bottom gap closes
                  {"name": "sash", "poly": [(35, 300), (952, 300), (947, 1450), (243, 1450)],
                   "box": (0, 300, 960, 1460)},
              ]},
}


def save(img, name, q=86):
    img.save(OUT / name, quality=q, optimize=True)


def run(scene, src):
    spec = SCENES[scene]
    im = Image.open(src).convert("RGB")
    x0, y0, x1, y1 = spec["crop"]
    for sp in spec.get("sprites", []):
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).polygon(sp["poly"], fill=255)
        m = np.array(mask)
        alpha = Image.fromarray(m).filter(ImageFilter.GaussianBlur(1.2))
        cut = im.copy(); cut.putalpha(alpha)
        cut.crop(sp["box"]).save(OUT / f"{scene}-{sp['name']}.png", optimize=True)
        if sp.get("inpaint"):
            dil = cv2.dilate(m, np.ones((9, 9), np.uint8))
            bgr = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
            im = Image.fromarray(cv2.cvtColor(cv2.inpaint(bgr, dil, 9, cv2.INPAINT_TELEA), cv2.COLOR_BGR2RGB))
    crop = im.crop((x0, y0, x1, y1))
    w, h = crop.size
    target_h = 1100
    crop = crop.resize((round(w * target_h / h), target_h), Image.LANCZOS)
    save(crop, f"{scene}.jpg")
    bg = Image.open(src).convert("RGB").resize((1200, round(1200 * im.height / im.width)))
    top = max(0, (bg.height - 750) // 2)
    bg = bg.crop((0, top, 1200, top + 750)).filter(ImageFilter.GaussianBlur(26))
    save(ImageEnhance.Brightness(bg).enhance(0.5), f"{scene}-bg.jpg", 70)
    # stage placement (for the scene config): portrait photo 750 tall at x=40
    sw = round(750 * w / h)
    print(f"{scene}: photo stage width {sw} (x=40..{40 + sw}); scale {750 / h:.4f}; source offset {x0},{y0}")


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])

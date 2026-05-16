#!/usr/bin/env python3
"""Generate og-default.png (1200x630) for Futures series."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUTPUT = Path(__file__).resolve().parent / "og-default.png"

W, H = 1200, 630
BG = (20, 17, 15)          # #14110F
INK = (255, 255, 255)      # #FFFFFF
INK_SOFT = (216, 213, 209) # #D8D5D1
INK_MUTE = (166, 162, 157) # #A6A29D
ACCENT = (255, 54, 68)     # #FF3644
LINE = (45, 42, 39)        # #2D2A27

MINCHO_W6 = "/System/Library/Fonts/ヒラギノ明朝 ProN.ttc"   # W6 index 0
SANS_W3 = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
SANS_W7 = "/System/Library/Fonts/ヒラギノ角ゴシック W7.ttc"


def load(path: str, size: int, index: int = 0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.load_default()


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # red top bar
    d.rectangle([(0, 0), (W, 6)], fill=ACCENT)
    # bottom line
    d.rectangle([(0, H - 1), (W, H)], fill=LINE)

    # eyebrow EN
    f_eb = load(SANS_W7, 22)
    d.text((80, 90), "FUTURES NO KATACHI", font=f_eb, fill=ACCENT)
    # tracking spacing 擬似: 元テキストは既に十分

    # title (large mincho)
    f_title = load(MINCHO_W6, 124, index=0)
    d.text((80, 150), "未来のかたち", font=f_title, fill=INK)

    # series label
    f_sub = load(MINCHO_W6, 38, index=0)
    d.text((80, 320), "連載「Futures」全 100 話", font=f_sub, fill=INK_SOFT)

    # lead
    f_lead = load(SANS_W3, 24)
    d.text((80, 400), "2100 年に向けた長い坂を、100 話かけて歩く連載。", font=f_lead, fill=INK_MUTE)
    d.text((80, 440), "いま私たちが立っている時代の現在地を、暮らしの言葉で読み解いていきます。", font=f_lead, fill=INK_MUTE)

    # footer
    f_meta = load(SANS_W7, 18)
    d.text((80, H - 80), "5 PARTS  ／  8 QUESTIONS  ／  NPO 法人ミラツク", font=f_meta, fill=INK_SOFT)

    # right accent block
    d.rectangle([(W - 70, 0), (W, H)], fill=(30, 27, 25))
    f_v = load(SANS_W7, 18)
    d.text((W - 50, H - 200), "v2", font=f_v, fill=ACCENT)

    img.save(OUTPUT, "PNG", optimize=True)
    print(f"Wrote {OUTPUT} ({OUTPUT.stat().st_size:,} bytes, {W}x{H})")


if __name__ == "__main__":
    main()

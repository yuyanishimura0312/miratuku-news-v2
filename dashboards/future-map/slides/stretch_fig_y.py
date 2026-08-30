"""スライドの図を縦に伸ばす（y 座標だけを伸ばす。冪等）。

★なぜ要るか（実測 2026-08-31）。この3枚の図は viewBox 960x262（比 3.66:1）で、
  版面の器は約 1002x500（比 2.0:1）。幅は満たすが高さが 273/500 = 55% しかなく、
  図の下に 210-260px の白帯が残る。西村さんの指摘「余白の置き方が変」。

★白は移動では消えない。図の比を枠に合わせたときだけ消える。
  ただしこの3枚は生成器を持たない（s01 は公開HTMLから回収したもの）か、
  共有ファイルへの追記型で、座標が直書きされている。そこで**座標を直接伸ばす**。

★伸ばすのは y だけ。文字の寸法は CSS クラスが持つので触らない
  （`<g transform="scale(1,k)">` で包むと文字まで縦に潰れる）。
  円の半径 r・矢尻の marker（独自の viewBox を持つ）・x 座標も触らない。

★原点から下だけを伸ばす。0 から一律に伸ばすと、年の目盛ラベルまで下がって
  上に隙間ができる。原点は「年の目盛の下」に取る。

使い方:
    python3 stretch_fig_y.py --check          # 何がどう変わるかを見るだけ
    python3 stretch_fig_y.py --target 500     # 図の高さを 500 にする
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "futures-genealogy.html"

# 原点。ここから下を伸ばす。年の目盛ラベル（y≈20）と軸線の上端（y=27）より下。
ORIGIN = 27.0

# ★伸ばす対象の属性。x 系と r（半径）と font-size は入れない。
Y_ATTRS = ("y", "y1", "y2", "cy")


def make_scaler(k, origin=ORIGIN):
    def sy(v):
        return origin + (v - origin) * k
    return sy


def scale_path_d(d, sy):
    """path の d を伸ばす。M/L/Q の絶対座標のみ（このファイルにはそれしか無い）。

    ★命令ごとに座標の数が違う: M/L は (x,y)、Q は (x1,y1,x,y)。
      並びを取り違えると x を y として伸ばすので、命令を見て組で処理する。
    """
    out = []
    for token in re.findall(r"[MLQZmlqz]|-?[\d.]+", d):
        out.append(token)
    res = []
    i = 0
    cmd = None
    while i < len(out):
        t = out[i]
        if t in "MLQZmlqz":
            cmd = t
            res.append(t)
            i += 1
            continue
        if cmd in ("M", "L"):
            x, y = float(out[i]), float(out[i + 1])
            res.append(f"{x:g}"); res.append(f"{sy(y):g}")
            i += 2
        elif cmd == "Q":
            x1, y1, x, y = (float(out[i + j]) for j in range(4))
            res += [f"{x1:g}", f"{sy(y1):g}", f"{x:g}", f"{sy(y):g}"]
            i += 4
        else:                      # 想定外の命令は触らない
            res.append(t); i += 1
    # "M 1 2 L 3 4" の形へ戻す
    s = ""
    for t in res:
        if t in "MLQZmlqz":
            s += ("" if not s else " ") + t
        else:
            s += " " + t
    return s.strip()


def stretch_svg(svg, target_h):
    """1つの svg を伸ばして返す。(新しいsvg, 元の高さ, 新しい高さ) を返す。"""
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    if not m:
        return svg, None, None
    w, h = float(m.group(1)), float(m.group(2))
    if h >= target_h:
        return svg, h, h
    k = (target_h - ORIGIN) / (h - ORIGIN)
    sy = make_scaler(k)

    # ★defs は触らない。marker は自前の viewBox を持ち、伸ばすと矢尻が歪む。
    dm = re.search(r"<defs>.*?</defs>", svg, re.S)
    defs = dm.group(0) if dm else ""
    body = svg.replace(defs, "\x00DEFS\x00") if defs else svg

    def attr(mm):
        return f'{mm.group(1)}="{sy(float(mm.group(2))):g}"'
    body = re.sub(r'\b(' + "|".join(Y_ATTRS) + r')="(-?[\d.]+)"', attr, body)
    # rect の height は「差」なので原点を足さずに倍率だけ掛ける
    body = re.sub(r'\bheight="(-?[\d.]+)"',
                  lambda mm: f'height="{float(mm.group(1)) * k:g}"', body)
    body = re.sub(r'\sd="([^"]*)"',
                  lambda mm: ' d="' + scale_path_d(mm.group(1), sy) + '"', body)
    body = body.replace(f'viewBox="0 0 {m.group(1)} {m.group(2)}"',
                        f'viewBox="0 0 {w:g} {target_h:g}"')
    if defs:
        body = body.replace("\x00DEFS\x00", defs)
    return body, h, target_h


# 面ごとの目標。★器を実測して決めた値であって、決め打ちではない。
#   （fig-box に使える高さ × viewBox幅960 ÷ 描画幅1002）
# ★器の実測から余裕（CLEARANCE）を引く。図の最下段には出典キャプションがあり、
#   器いっぱいまで伸ばすと、すぐ下の凡例の赤い罫に串刺しになる（実測で確認）。
CLEARANCE = 28.0
TARGETS = [477.0 - CLEARANCE, 451.0 - CLEARANCE, 449.0 - CLEARANCE]


def main():
    targets = list(TARGETS)
    if "--target" in sys.argv:
        targets = [float(sys.argv[sys.argv.index("--target") + 1])] * len(TARGETS)
    check = "--check" in sys.argv

    html = SRC.read_text(encoding="utf-8")
    out = []
    pos = 0
    n = 0
    for m in re.finditer(r'<svg class="fig".*?</svg>', html, re.S):
        new, old_h, new_h = stretch_svg(m.group(0), targets[n] if n < len(targets) else targets[-1])
        out.append(html[pos:m.start()]); out.append(new); pos = m.end()
        n += 1
        print(f"  図{n}: 高さ {old_h:g} → {new_h:g}"
              + ("（既に足りているので触らない）" if old_h == new_h else ""))
    out.append(html[pos:])
    if check:
        print("--check のため書き込みませんでした。")
        return
    SRC.write_text("".join(out), encoding="utf-8")
    print(f"書き出しました: {SRC.name} ({SRC.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()

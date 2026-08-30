"""2枚目「方法の系譜」を futures-genealogy.html に足す（冪等）。

★1枚目と同じ年軸を使う。x = 164 + (年-1950) * 12.0（1枚目の実測から導出）。
  座標を手で書かないのは、2枚の図を並べたときに年が合っていないと
  「同じ時間軸で読める」という前提が崩れるため。

★この図はデータベースから作っていない。fs_methods 99件は系譜の欄
  (predecessor/successor/parent/school_association) が全件空で、97件が未検証だから。
  したがって各辺の根拠は外部の一次情報に置き、図の中で明示する。
  DB に入れる工程は別（決裁待ち）。

使い方: python3 build_slide02.py     （もう一度流しても二重に足さない）
"""
import re
from pathlib import Path

SRC = Path(__file__).with_name("futures-genealogy.html")

# ---- 1枚目から導出した年軸（実測: 1950→x=164 / 10年ごとに +120）----
X0, Y0 = 164.0, 1950
PER_YEAR = 12.0


def x(year: float) -> float:
    return X0 + (year - Y0) * PER_YEAR


# ---- レーン（縦の帯）----
# 上から: 計算する(hard) / 対話し学習する(soft) / それを受け取った学派
LANES = [
    ("計算する — hard systems", 31.0, 104.0, True),
    ("対話し学習する — soft systems", 111.0, 170.0, False),
    ("受け取った学派", 177.0, 250.0, True),
]

# ---- ノード（年・ラベル・y・注記）----
NODES = {
    "industrial": (1961, "Industrial Dynamics", 52.0, "Forrester / MIT"),
    "urban": (1969, "Urban Dynamics", 74.0, ""),
    "world": (1971, "World Dynamics", 96.0, ""),
    "checkland": (1981, "Systems Thinking, Systems Practice", 140.0, "Checkland / Lancaster"),
    "limits": (1972, "成長の限界（World3）", 200.0, "ローマクラブ"),
    "complexity": (1990, "複雑系/システム未来学", 228.0, ""),
}

# ---- 辺（起点・終点・根拠・図中のラベル）----
# 図の中に辺のラベルは置かない（1枚目にも無く、置くとノード名と重なる）。
# 4つ目の要素は「曲げの強さ」。0 だとほぼ直線。
EDGES = [
    ("world", "limits", "documented", 0.10),
    # ★1961→1981 は hard レーンのノード群を横切るので、大きく下へ迂回させる
    ("industrial", "checkland", "documented", -0.26),
    ("limits", "complexity", "original_curation", 0.08),
]

STROKE = {
    "person_chain": ("#CC1400", 2.0, None, 0.90),
    "documented": ("#3A3A3A", 1.8, "7 3", 0.72),
    "original_curation": ("#8A8A8A", 1.6, "1.2 3.6", 1.00),
}


def node_svg(key: str) -> str:
    year, label, cy, note = NODES[key]
    cx = x(year)
    s = (
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.6" fill="#CC1400" '
        f'stroke="#FFFFFF" stroke-width="1.6"/>\n'
        f'<text x="{cx + 9.6:.1f}" y="{cy + 4.6:.1f}" font-size="13px" font-weight="700" '
        f'fill="#0E0E0E" stroke="#FFFFFF" stroke-width="3.4" paint-order="stroke" '
        f'text-anchor="start" letter-spacing="-0.015em">{label}</text>\n'
        f'<text x="{cx - 12.6:.1f}" y="{cy + 4.0:.1f}" font-size="12px" fill="#595959" '
        f'font-family="Fira Code, monospace" font-weight="400" stroke="#FFFFFF" '
        f'stroke-width="3" paint-order="stroke" text-anchor="end" '
        f'letter-spacing="0.02em">{year}</text>\n'
    )
    if note:
        # 所属は本体より1段落として小さく、ラベルの下に置く
        s += (
            f'<text x="{cx + 9.6:.1f}" y="{cy + 17.0:.1f}" font-size="11px" fill="#707070" '
            f'stroke="#FFFFFF" stroke-width="2.6" paint-order="stroke" '
            f'text-anchor="start">{note}</text>\n'
        )
    return s


def edge_svg(src: str, dst: str, basis: str, bow: float) -> str:
    color, w, dash, op = STROKE[basis]
    x1, y1 = x(NODES[src][0]), NODES[src][2]
    x2, y2 = x(NODES[dst][0]), NODES[dst][2]
    # ノードの円（r=3.6）に食い込ませない
    dx, dy = x2 - x1, y2 - y1
    d = (dx * dx + dy * dy) ** 0.5 or 1.0
    x1 += dx / d * 5.5
    y1 += dy / d * 5.5
    x2 -= dx / d * 9.5
    y2 -= dy / d * 7.5
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    # 直線だと3本とも同じ向きに見えるので、中点を少し外へ振る
    cx_, cy_ = mx + dy * bow, my - dx * bow
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<path d="M{x1:.1f},{y1:.1f} Q{cx_:.1f},{cy_:.1f} {x2:.1f},{y2:.1f}" fill="none" '
        f'stroke="{color}" stroke-width="{w}" opacity="{op}"{da} '
        f'marker-end="url(#ah-{basis})"/>\n'
    )


def build_svg() -> str:
    p = ['<svg class="fig" viewBox="0 0 960 262" role="img" '
         'aria-label="方法の系譜。システムダイナミクスからシステム思考への展開と、'
         'それを受け取った学派">\n<defs>\n']
    for basis, (color, _w, _d, op) in STROKE.items():
        p.append(
            f'<marker id="ah-{basis}" viewBox="0 0 9 8" refX="8" refY="4" '
            f'markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="8" '
            f'orient="auto-start-reverse"><path d="M0,0.6 L9,4 L0,7.4 Z" fill="{color}" '
            f'opacity="{op:.2f}"/></marker>\n'
        )
    p.append("</defs>\n")

    # レーンの帯（1枚目と同じ #FAFAF7 の交互塗り + 赤の左端ティック）
    for name, top, bottom, shaded in LANES:
        if shaded:
            p.append(f'<rect x="4.0" y="{top:.1f}" width="944.0" '
                     f'height="{bottom - top:.1f}" fill="#FAFAF7"/>\n')
        p.append(f'<rect x="4.0" y="{top + 2:.1f}" width="2" '
                 f'height="{bottom - top - 4:.1f}" fill="#CC1400"/>\n')
        p.append(f'<text x="14.0" y="{top + 15.0:.1f}" font-size="11px" font-weight="700" '
                 f'fill="#707070" letter-spacing="0.04em">{name}</text>\n')

    # 年軸（1枚目と同じ位置・同じ色）
    for year in range(1950, 2011, 10):
        p.append(f'<line x1="{x(year):.1f}" y1="27.0" x2="{x(year):.1f}" y2="262.0" '
                 f'stroke="#ECECEC" stroke-width="1"/>\n')
        p.append(f'<text x="{x(year):.1f}" y="20.0" font-size="12px" fill="#595959" '
                 f'font-family="Fira Code, monospace" text-anchor="middle" '
                 f'letter-spacing="0.02em">{year}</text>\n')

    for e in EDGES:
        p.append(edge_svg(*e))
    for k in NODES:
        p.append(node_svg(k))
    p.append("</svg>")
    return "".join(p)


def swatch(basis: str) -> str:
    color, w, dash, op = STROKE[basis]
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<svg class="lg-swatch" viewBox="0 0 44 12" aria-hidden="true">'
            f'<line x1="1" y1="6" x2="43" y2="6" stroke="{color}" stroke-width="{w}" '
            f'opacity="{op:.2f}"{da}/></svg>')


def build_section() -> str:
    n_doc = sum(1 for e in EDGES if e[2] == "documented")
    n_cur = sum(1 for e in EDGES if e[2] == "original_curation")
    return f"""
<section class="slide" id="s02">
  <div class="slide-head">
    <img class="logo" alt="ミラツク" src="[LOGO]">
    <span class="center">方法の系譜 / Genealogy of Methods</span>
    <span class="num">02 / 02</span>
  </div>

  <div class="title-block">
    <p class="eyebrow">Futures Studies Database</p>
    <h1>未来を計算する方法から、未来を語り合う方法へ ── 分岐は1981年にある</h1>
    <div class="accent-stroke"></div>
    <p class="lead">学派の系譜（前頁）とは別に、<b>方法にも一本の線</b>がある。システムダイナミクスは未来を計算する道具として生まれ、ローマクラブの仕事で世界模型になり、やがて<b>探究の過程そのものを学習とみなす</b>ソフト・システムへ分岐した。横軸は前頁と同じ年である。</p>
  </div>

  <div class="body">
    <div class="fig-box">
{build_svg()}
      <p class="fig-cap">FIG. 02 — 方法の系譜 (横軸 = 年・前頁と共通 / 縦 = 計算する・対話し学習する・受け取った学派)</p>
    </div>

    <div class="legend"><span class="lg-head">線種 = 関係の裏づけ</span><span class="lg-item">{swatch('documented')}<b>文献に記述あり</b><span class="lg-note">{n_doc}本</span></span><span class="lg-item">{swatch('original_curation')}<b>編纂 (機械的裏づけなし)</b><span class="lg-note">{n_cur}本</span></span><span class="lg-item"><b>★人物関係の機械照合は0本</b><span class="lg-note">方法の層に系譜データが無いため</span></span></div>

    <div class="cols">
      <div>
        <h2 class="sec">読み取り方</h2>
        <ul class="reads"><li><b>錨は1961年</b>Forrester が1950年代半ばに始め、<b>Industrial Dynamics</b>(1961)が最初の体系。当DBの年(1956/1958)は<b>出典を持たない</b>ため使わない。</li><li><b>1971年に名前が変わる</b>ローマクラブのベルン会合に招かれ、対象が産業に留まらなくなって呼称が industrial から <b>system dynamics</b> へ。成長の限界(1972)はその後。</li><li><b>分岐は1981年</b>Checkland が <b>hard(世界を工学的に設計できるとする)と soft(探究の過程そのものを学習とみなす)</b> の区別を確立。計算から対話への移動がここにある。</li><li><b>学派になったのは2つだけ</b>ローマクラブと複雑系。後者への線は<b>当DBの記述のみ</b>が根拠の編纂である。</li></ul>
      </div>
      <div class="note">
        <h2 class="sec">この図から言えないこと</h2>
        <ul class="cannot"><li><strong>この系譜はDBに入っていない。</strong>方法99件は系譜の欄が<strong>全件空</strong>、97件が未検証。図は外部の一次情報から引いた。</li><li>Checkland の批判は <strong>hard systems 全般</strong>に向けられており、システムダイナミクスを名指ししたわけではない。</li><li><strong>Senge と Forrester の師弟関係は未確認</strong>のため線にしていない。Senge・Checkland は当DBに不在。</li><li>参加型未来手法(当DB 1970)へは線を引いていない。出典が無く、Checkland 1981 より前で<strong>年代が逆立ちする</strong>。</li></ul>
      </div>
    </div>
  </div>

  <div class="footer">
    <span class="src">出典 System Dynamics Society / MIT Sloan / Checkland 1981</span>
    <span>作成 2026-08-30 / 方法の層は未登録・DB集計ではない</span>
  </div>
</section>
"""


def main():
    html = SRC.read_text(encoding="utf-8")

    # ロゴは1枚目のものを使い回す（base64 を二重に持たない）
    m = re.search(r'<img class="logo" alt="ミラツク" src="(data:image/png;base64,[^"]+)">', html)
    if not m:
        raise SystemExit("1枚目のロゴが見つかりません")
    section = build_section().replace("[LOGO]", m.group(1))

    if 'id="s02"' in html:  # 冪等: 既にあるものを差し替える
        html = re.sub(r'\n<section class="slide" id="s02">.*?</section>\n',
                      "\n" + section.strip("\n") + "\n", html, flags=re.S)
    else:
        anchor = "</section>\n</div>"
        if anchor not in html:
            raise SystemExit("差し込み位置（</section></div>）が見つかりません")
        html = html.replace(anchor, "</section>\n" + section.strip("\n") + "\n</div>", 1)

    # 通し番号（1枚目は 01 / 01 のままなので直す）
    html = html.replace('<span class="num">01 / 01</span>', '<span class="num">01 / 02</span>')

    SRC.write_text(html, encoding="utf-8")
    print(f"書き出しました: {SRC} ({SRC.stat().st_size:,} bytes)")
    print(f"  辺 {len(EDGES)}本 / ノード {len(NODES)}件")


if __name__ == "__main__":
    main()

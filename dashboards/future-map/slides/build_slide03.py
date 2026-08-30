"""3枚目「1981年の分岐」を futures-genealogy.html に足す（冪等）。

2枚目で「分岐は1981年」と一行で書いたところを、一枚使って開く。
★問いは「システムは世界の側にあるのか、探究の側にあるのか」である。
  ここが変わると、未来を扱う道具の目的が「最適化」から「合意」へ移る。

接地:
  Checkland P (2000) Soft systems methodology: a thirty year retrospective.
    Systems Research and Behavioral Science 17(S1): S11-S58.
    DOI 10.1002/1099-1743(200011)17:1+<::AID-SRES374>3.0.CO;2-O
  Checkland P (1981) Systems Thinking, Systems Practice. Wiley.
  ★7段階の段階名は二次資料（Wikipedia）から採った。原典との逐語照合は未実施。
"""
import re
from pathlib import Path

SRC = Path(__file__).with_name("futures-genealogy.html")

INK, MUTE, RULE, ACCENT, SHADE = "#0E0E0E", "#707070", "#DEDEDE", "#CC1400", "#FAFAF7"

# 左右の対比。(見出し, [(項目, 中身), ...])
HARD = ("hard — システムは世界の側にある", [
    ("前提", "世界の一部を「システム」として取り出し、工学的に設計できる"),
    ("問い", "どうやるか（何をするかは既に決まっている）"),
    ("道具", "模型と計算。World3 のような世界模型"),
    ("判定", "定めた目的に対して最適化できたか"),
])
SOFT = ("soft — システムは探究の側にある", [
    ("前提", "何をすべきかが定まらない。探究の過程そのものを学習のシステムとする"),
    ("問い", "何をするか。そこから問う"),
    ("道具", "root definition・CATWOE・概念モデル・現実との比較"),
    ("判定", "実行可能で望ましい変化に関与者が合意できたか"),
])

STAGES = [
    ("1", "問題状況の把握"),
    ("2", "状況の表現"),
    ("3", "root definition\nの策定"),
    ("4", "概念モデルの構築"),
    ("5", "現実との比較"),
    ("6", "望ましい変化\nの特定"),
    ("7", "改善の行動"),
]
# ★3と4だけが概念の世界。5が「現実と比べる」段階であることから、そう読める。
CONCEPTUAL = {"3", "4"}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def panel(x0: float, w: float, title: str, rows, shaded: bool) -> str:
    p = []
    if shaded:
        p.append(f'<rect x="{x0:.1f}" y="14.0" width="{w:.1f}" height="132.0" fill="{SHADE}"/>')
    p.append(f'<rect x="{x0:.1f}" y="14.0" width="3" height="132.0" fill="{ACCENT}"/>')
    p.append(f'<text x="{x0 + 14:.1f}" y="32.0" font-size="13px" font-weight="700" '
             f'fill="{INK}" letter-spacing="-0.01em">{esc(title)}</text>')
    y = 56.0
    for label, value in rows:
        p.append(f'<text x="{x0 + 14:.1f}" y="{y:.1f}" font-size="10.5px" font-weight="700" '
                 f'fill="{MUTE}" letter-spacing="0.08em">{esc(label)}</text>')
        p.append(f'<text x="{x0 + 62:.1f}" y="{y:.1f}" font-size="12.5px" fill="#3A3A3A">'
                 f'{esc(value)}</text>')
        y += 22.0
    return "\n".join(p) + "\n"


def build_svg() -> str:
    p = ['<svg class="fig" viewBox="0 0 960 262" role="img" '
         'aria-label="1981年の分岐。hard systems と soft systems の対比と、SSM の7段階">\n']

    # 左右のパネル
    p.append(panel(4.0, 460.0, HARD[0], HARD[1], True))
    p.append(panel(496.0, 460.0, SOFT[0], SOFT[1], False))

    # 中央の分岐点
    p.append(f'<line x1="480" y1="14" x2="480" y2="146" stroke="{RULE}" stroke-width="1"/>\n')
    p.append(f'<circle cx="480" cy="80" r="5.4" fill="{ACCENT}" stroke="#FFFFFF" stroke-width="2"/>\n')
    p.append(f'<text x="480" y="60" font-size="13px" font-weight="700" fill="{ACCENT}" '
             f'font-family="Fira Code, monospace" text-anchor="middle" stroke="#FFFFFF" '
             f'stroke-width="3.4" paint-order="stroke">1981</text>\n')
    p.append(f'<text x="480" y="104" font-size="10.5px" fill="{MUTE}" text-anchor="middle" '
             f'stroke="#FFFFFF" stroke-width="3" paint-order="stroke">Checkland</text>\n')

    # 下段: SSM の7段階
    p.append(f'<text x="8" y="176.0" font-size="11px" font-weight="700" fill="{MUTE}" '
             f'letter-spacing="0.04em">SSM の7段階 — 3と4だけが概念の世界にある'
             f'（5が「現実と比べる」段階だから、そう読める）</text>\n')
    x, w, gap = 8.0, 128.0, 8.0
    for num, name in STAGES:
        conceptual = num in CONCEPTUAL
        fill = "#F4EDEA" if conceptual else "#FFFFFF"
        stroke = ACCENT if conceptual else RULE
        p.append(f'<rect x="{x:.1f}" y="186.0" width="{w:.1f}" height="52.0" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="1"/>\n')
        p.append(f'<text x="{x + 9:.1f}" y="203.0" font-size="12px" font-weight="700" '
                 f'fill="{ACCENT if conceptual else MUTE}" '
                 f'font-family="Fira Code, monospace">{num}</text>\n')
        lines = name.split("\n")
        ty = 203.0 if len(lines) == 1 else 199.0
        for i, ln in enumerate(lines):
            p.append(f'<text x="{x + 26:.1f}" y="{ty + i * 14:.1f}" font-size="11.5px" '
                     f'fill="{INK}">{esc(ln)}</text>')
        p.append("\n")
        if x + w + gap < 940:
            ax = x + w + 1.0
            p.append(f'<path d="M{ax:.1f},212 L{ax + gap - 2:.1f},212" stroke="{RULE}" '
                     f'stroke-width="1.4" marker-end="url(#ah3)"/>\n')
        x += w + gap

    # 7 から 1 へ戻る（循環である）
    p.append(f'<path d="M{x - w - gap + w / 2:.1f},240 C{x - 200:.1f},256 {90:.1f},256 '
             f'{72:.1f},240" fill="none" stroke="{RULE}" stroke-width="1.4" '
             f'stroke-dasharray="4 3" marker-end="url(#ah3)"/>\n')
    p.append(f'<text x="{(x - w) / 2:.1f}" y="254.0" font-size="10.5px" fill="{MUTE}" '
             f'text-anchor="middle" stroke="#FFFFFF" stroke-width="3" paint-order="stroke">'
             f'一度で終わらない。行動した結果がまた状況になる</text>\n')

    p.insert(1, f'<defs><marker id="ah3" viewBox="0 0 8 7" refX="7" refY="3.5" '
                f'markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="7" '
                f'orient="auto-start-reverse"><path d="M0,0.5 L8,3.5 L0,6.5 Z" '
                f'fill="{MUTE}" opacity="0.7"/></marker></defs>\n')
    p.append("</svg>")
    return "".join(p)


def build_section() -> str:
    return f"""
<section class="slide" id="s03">
  <div class="slide-head">
    <img class="logo" alt="ミラツク" src="[LOGO]">
    <span class="center">1981年の分岐 / The 1981 Split</span>
    <span class="num">03 / 03</span>
  </div>

  <div class="title-block">
    <p class="eyebrow">Futures Studies Database</p>
    <h1>システムは世界の側にあるのか、探究の側にあるのか</h1>
    <div class="accent-stroke"></div>
    <p class="lead">Checkland は、systems engineering をそのまま経営の状況へ移せないと分かったところから出発した。転回は<b>「システム」という語の置き場所</b>にある。世界の一部を切り出してシステムと呼ぶのをやめ、<b>探究の過程そのものをシステムとみなす</b>。ここで道具の目的が最適化から合意へ移る。</p>
  </div>

  <div class="body">
    <div class="fig-box">
{build_svg()}
      <p class="fig-cap">FIG. 03 — hard と soft の対比（上段）と、SSM の7段階（下段・段階名は二次資料による）</p>
    </div>

    <div class="cols">
      <div>
        <h2 class="sec">この分岐が変えたもの</h2>
        <ul class="reads"><li><b>問いの向きが変わる</b>hard は「どうやるか」を扱い、<b>何をするかは決まっている</b>という前提が要る。soft はそこを疑い<b>何をするかから問う</b>。</li><li><b>「うまくいった」の意味が変わる</b>hard は目的への最適化を問えるが、soft は問えない。代わりに<b>実行可能で望ましい変化に合意できたか</b>を見る。基準が計算の外にある。</li><li><b>模型が答えでなくなる</b>3・4の概念モデルは「世界がそうなっている」という主張ではなく、<b>現実と比べるための道具</b>。5で比較して初めて働く。</li><li><b>未来学に効く場所</b>シナリオが真偽で反証されないのは、hard の意味での模型ではないから。前提の明示・複数分岐・合意という評価はこの下流にある。</li></ul>
      </div>
      <div class="note">
        <h2 class="sec">この一枚から言えないこと</h2>
        <ul class="cannot"><li>Checkland が名指しした相手は <strong>systems engineering</strong> であり、システムダイナミクスではない。同一視して読まない。</li><li><strong>1981年は書物になった年</strong>で、思想が生まれた年ではない。成立はランカスターの長期のアクション・リサーチ（最初の研究は1969年）にある。</li><li><strong>7段階の名は二次資料から採った。</strong>原典との逐語照合は未実施。Mode 1 / 2 は確認できなかった。</li><li><strong>移動であって置換ではない。</strong>hard の系統は現在も使われており、優劣は述べていない。</li></ul>
      </div>
    </div>
  </div>

  <div class="footer">
    <span class="src">出典 Checkland 1981 Systems Thinking, Systems Practice / Checkland 2000 SRBS 17(S1)</span>
    <span>作成 2026-08-30 / 段階名は二次資料</span>
  </div>
</section>
"""


def main():
    html = SRC.read_text(encoding="utf-8")
    m = re.search(r'<img class="logo" alt="ミラツク" src="(data:image/png;base64,[^"]+)">', html)
    if not m:
        raise SystemExit("1枚目のロゴが見つかりません")
    section = build_section().replace("[LOGO]", m.group(1))

    if 'id="s03"' in html:
        html = re.sub(r'\n<section class="slide" id="s03">.*?</section>\n',
                      "\n" + section.strip("\n") + "\n", html, flags=re.S)
    else:
        anchor = "</section>\n</div>"
        if anchor not in html:
            raise SystemExit("差し込み位置が見つかりません")
        html = html.replace(anchor, "</section>\n" + section.strip("\n") + "\n</div>", 1)

    # 通し番号を3枚に直す
    html = html.replace('<span class="num">01 / 02</span>', '<span class="num">01 / 03</span>')
    html = html.replace('<span class="num">02 / 02</span>', '<span class="num">02 / 03</span>')

    SRC.write_text(html, encoding="utf-8")
    print(f"書き出しました: {SRC} ({SRC.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()

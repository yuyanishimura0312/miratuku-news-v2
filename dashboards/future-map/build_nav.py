"""future-map 配下の全ページに、同じ案内バーを入れる（冪等）。

★なぜ要るか（実測 2026-08-30）:
  20ページのうち **13ページにはナビが1本も無かった**。残る7ページも本数が 1〜8 とばらばらで、
  同じ行き先の呼び名が割れていた —— map.html は「18テーマ版へ／18テーマ版／未来像マップ／
  未来像マップ（メイン）へ」の4通り、domain-map-2026 は3通り、統合マップは v1 と v2 に割れていた。
  行き先が同じなら呼び名も1つにする。

設計:
  - 見た目は既存の .lk（丸ピル・var(--accent) の輪郭）を踏襲する。全ページが同じトークン名を
    使っており、暗色の future-tech-map-v2 では --accent が自動で明るい方に振れる。
    ★色を直書きしない理由がこれ。1枚だけ暗いページがあるため。
  - 現在地はリンクにせず、印を付ける（押しても動かないリンクを置かない）。
  - 群で分ける（統合マップ2026 / 18テーマ版 / 未来学）。13本を平らに並べても選べない。
  - 既存のばらばらなリンクは取り除いてから入れる（重複させない）。

対象外:
  - deep.html … 転送用のページ（本文が無い）
  - slides/*.html … A4のスライド。上にバーを足すと版面が崩れ、印刷にも出る。
    ★バーからスライドへは行けるが、スライドからは戻らない。ここは意図的に非対称。
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKIP = {"deep.html"}

# 群 → [(href, ラベル)]。★行き先1つにつき呼び名は1つ。
GROUPS = [
    ("統合マップ 2026", [
        ("dashboard.html", "ダッシュボード"),
        ("future-tech-map-v2.html", "統合マップ"),
        ("future-map-guide.html", "この地図の中身"),
        ("domain-map-2026.html", "領域の詳細"),
        ("roadmaps.html", "技術の詳細"),
        ("future-map-ai-human.html", "AIと人の領域"),
        ("signals-26.html", "シグナル一覧"),
        ("reference-2026.html", "資料編"),
    ]),
    ("18テーマ版", [
        ("map.html", "未来像マップ"),
        ("index.html", "シグナル一覧（18テーマ）"),
        ("research.html", "最新研究"),
        ("overlay-map.html", "重ね合わせ"),
    ]),
    ("未来学", [
        ("futures-library-index.html", "書庫"),
        ("slides/futures-genealogy.html", "系譜（スライド）"),
    ]),
]

STYLE = """<style>
/* 共通の案内バー。色はページ側のトークンを借りるので、暗色ページでも反転しない。 */
.fmnav{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;
  padding:10px clamp(14px,3vw,28px);border-bottom:1px solid var(--rule,#E4DCD2);
  background:var(--surface,#F7F4EE);font-family:var(--jp,"Noto Sans JP",sans-serif);line-height:1.6}
.fmnav .g{display:inline-flex;flex-wrap:wrap;align-items:center;gap:6px}
.fmnav .gl{font-size:10px;font-weight:700;letter-spacing:.14em;
  color:var(--ink-mute,#8A7868);margin-right:2px;white-space:nowrap}
.fmnav a,.fmnav .cur{font-size:11.5px;font-weight:700;border-radius:999px;
  padding:5px 12px;white-space:nowrap;text-decoration:none;display:inline-block}
.fmnav a{color:var(--accent,#783C28);border:1px solid var(--accent,#783C28)}
.fmnav a:hover{background:var(--accent,#783C28);color:var(--paper,#FAF8F5)}
.fmnav a:focus-visible{outline:2px solid var(--accent,#783C28);outline-offset:2px}
/* 現在地はリンクにしない。押しても動かないリンクを置かないため。 */
.fmnav .cur{color:var(--paper,#FAF8F5);background:var(--accent,#783C28);
  border:1px solid var(--accent,#783C28)}
.fmnav .sep{width:1px;align-self:stretch;background:var(--rule,#E4DCD2);margin:0 2px}
@media print{.fmnav{display:none}}
</style>
"""

BEGIN, END = "<!-- fmnav:begin -->", "<!-- fmnav:end -->"

# バーに載っていないページは、所属する項目を現在地として示す。
# ★載っていない＝現在地なし にすると、読者は自分がどこにいるか分からない。
PARENT = {
    "dashboard-v2.html": "dashboard.html",
    "futures-library-bell.html": "futures-library-index.html",
    "futures-library-kit.html": "futures-library-index.html",
    "futures-library-limits.html": "futures-library-index.html",
    "futures-library-methods.html": "futures-library-index.html",
    "futures-library-schools.html": "futures-library-index.html",
    # ★future-tech-map.html（v1）は意図的に入れていない。v2 と同じ地図の別版で、
    #   どちらを正とするかが決まっていない。決まるまで現在地を偽らない。
}


def build(cur: str, prefix: str) -> str:
    parts = [BEGIN, STYLE, '<nav class="fmnav" aria-label="未来マップの案内">']
    for gi, (gname, links) in enumerate(GROUPS):
        if gi:
            parts.append('<span class="sep" aria-hidden="true"></span>')
        parts.append('<span class="g"><span class="gl">' + gname + "</span>")
        for href, label in links:
            if href == cur:
                parts.append(f'<span class="cur" aria-current="page">{label}</span>')
            else:
                parts.append(f'<a href="{prefix}{href}">{label} →</a>')
        parts.append("</span>")
    parts.append("</nav>")
    parts.append(END)
    return "".join(parts)


def strip_old(html: str) -> tuple[str, int]:
    """既存のばらばらなリンクを取り除く。取り除いた本数を返す。"""
    n = len(re.findall(r'<a class="lk"', html))
    html = re.sub(r'<a class="lk"[^>]*>.*?</a>\s*', "", html, flags=re.S)
    # 空になったラッパー span を落とす
    html = re.sub(r'<span style="display:inline-flex;[^"]*">\s*</span>\s*', "", html)
    return html, n


def main():
    check = "--check" in sys.argv
    for p in sorted(HERE.glob("*.html")):
        if p.name in SKIP:
            print(f"  {p.name}: 対象外")
            continue
        html = p.read_text(encoding="utf-8")
        html, removed = strip_old(html)
        # 既に入っていれば入れ替える
        # ★前後の空白ごと取り除く。残したまま下で "\n" を2つ足すと、
        #   実行のたびに空行が積み上がり冪等でなくなる（実測: 1回につき2行）。
        html = re.sub(r"\s*" + re.escape(BEGIN) + r".*?" + re.escape(END) + r"\s*",
                      "", html, flags=re.S)
        m = re.search(r"<body[^>]*>", html)
        if not m:
            print(f"  {p.name}: ★<body> が見つからないので飛ばします")
            continue
        nav = build(PARENT.get(p.name, p.name), "")
        html = html[:m.end()] + "\n" + nav + "\n" + html[m.end():]
        if check:
            print(f"  {p.name}: 旧リンク {removed} 本を置換予定")
            continue
        p.write_text(html, encoding="utf-8")
        print(f"  {p.name}: 旧リンク {removed} 本を置換（{p.stat().st_size:,} bytes）")

    if check:
        print("--check のため書き込みませんでした。")


if __name__ == "__main__":
    main()

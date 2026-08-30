"""roadmaps.html の英語表記を日本語にする（冪等）。

★訳し直さない。統合マップ（future-tech-map-v2.html）が既に250件すべての日本語名と
  日本語のマイルストーン名を持っているので、それを持ってくる。
  別々に訳すと、同じ技術に2つの日本語名ができて、姉妹ページの間で食い違う。

対応の確認（このスクリプトが毎回やる）:
  - topic が 250/250 一致すること
  - マイルストーン列の (年, TRL前, TRL後) が完全一致すること
  ★一致しなければ止める。ずれた列を順番で当てると、別のマイルストーンの名前が付く。

英語を消さずに併記する理由:
  ロードマップ名は原語（英語）で検索されることがあり、消すと辿れなくなる。
  日本語を主、英語を従（小さく）にする。
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "roadmaps.html"
REF = HERE / "future-tech-map-v2.html"


def load_block(text: str, pattern: str):
    m = re.search(pattern, text, re.S)
    if not m:
        raise SystemExit(f"データ block が見つかりません: {pattern[:40]}")
    return json.loads(m.group(1)), m


def main():
    html = SRC.read_text(encoding="utf-8")
    ref = REF.read_text(encoding="utf-8")

    RM = {x["topic"]: x for x in json.loads(re.search(r"const RM\s*=\s*(\[.*?\]);", ref, re.S).group(1))}
    DATA, m = load_block(html, r"const DATA=(\[.*?\]);const DOMS=")

    # --- 対応の検査。ここを飛ばすと別物の名前が付く ---
    missing = [d["topic"] for d in DATA if d["topic"] not in RM]
    if missing:
        raise SystemExit(f"統合マップ側に無い topic が {len(missing)} 件: {missing[:5]}")
    for d in DATA:
        a = RM[d["topic"]]
        ka = [(x["y"], x.get("tb"), x.get("ta")) for x in a.get("ms", [])]
        kb = [(x["y"], x.get("tb"), x.get("ta")) for x in d.get("ms", [])]
        if ka != kb:
            raise SystemExit(f"マイルストーン列がずれています: {d['topic']}")
    print(f"対応を確認: {len(DATA)}/250 の topic とマイルストーン列が一致")

    # --- 差し替え ---
    n_ms = 0
    for d in DATA:
        a = RM[d["topic"]]
        if a.get("disp") and a["disp"] != d["disp"]:
            d["en"] = d["disp"]          # 原語は捨てずに従として残す
            d["disp"] = a["disp"]
        for i, x in enumerate(d.get("ms", [])):
            ja = a["ms"][i].get("name")
            if ja and ja != x["name"]:
                x["name_en"] = x["name"]
                x["name"] = ja
                n_ms += 1
        # ★scope の先頭に出ている英語の topic id を日本語名に置き換える
        #   （読者向けの文に内部の識別子が出ていた）
        d["scope"] = re.sub(
            r"^" + re.escape(d["topic"]) + r" の技術進化ロードマップ",
            f"{d['disp']}の技術進化ロードマップ", d["scope"])
        d["scope"] = d["scope"].replace("H3遠地平比率", "遠い地平の比率")
    print(f"ロードマップ名を日本語に: {sum(1 for d in DATA if d.get('en'))} 件")
    print(f"マイルストーン名を日本語に: {n_ms} 件")

    html = html[:m.start(1)] + json.dumps(DATA, ensure_ascii=False) + html[m.end(1):]

    # --- 描画側: 英語を従として出す ---
    def sub(old, new, label):
        nonlocal html
        if new in html:
            print(f"  済み: {label}")
            return
        if old not in html:
            raise SystemExit(f"見つかりません: {label}")
        html = html.replace(old, new, 1)
        print(f"  直した: {label}")

    sub('<div class="ct">${esc(r.disp)}</div>',
        '<div class="ct">${esc(r.disp)}</div>${r.en?`<div class="cen">${esc(r.en)}</div>`:\'\'}',
        "カードに原語を添える")
    sub('<div class="dtitle">${esc(r.disp)}</div>',
        '<div class="dtitle">${esc(r.disp)}</div>${r.en?`<div class="den2">${esc(r.en)}</div>`:\'\'}',
        "ドロワーに原語を添える")
    sub('<span class="mn">${esc(m.name)}</span>',
        '<span class="mn">${esc(m.name)}${m.name_en?`<span class="mnen">${esc(m.name_en)}</span>`:\'\'}</span>',
        "マイルストーンに原語を添える")

    # --- 原語の見た目（既存トークンだけで組む） ---
    css = ('.cen{font-family:var(--mono);font-size:10px;letter-spacing:.02em;'
           'color:var(--ink-faint);margin:-2px 0 6px}\n'
           '.den2{font-family:var(--mono);font-size:11px;letter-spacing:.02em;'
           'color:var(--ink-mute);margin:-4px 0 8px}\n'
           '.mnen{display:block;font-family:var(--mono);font-size:10px;'
           'color:var(--ink-faint);margin-top:2px;font-weight:400}\n')
    if ".cen{" not in html:
        anchor = ".tl .cnt{"
        html = html.replace(anchor, css + anchor, 1)
        print("  直した: 原語の見た目")
    else:
        print("  済み: 原語の見た目")

    # --- 画面の英語ラベル ---
    for a, b, label in [
        ('<div class="k">Roadmaps</div>', '<div class="k">ロードマップ</div>', "統計: Roadmaps"),
        ('<div class="k">Milestones</div>', '<div class="k">マイルストーン</div>', "統計: Milestones"),
        ('<div class="k">Domains</div>', '<div class="k">未来領域</div>', "統計: Domains"),
        ('<div class="k">Horizon</div>', '<div class="k">最遠の予定年</div>', "統計: Horizon"),
        ('<div class="eyebrow">TECHNOLOGY ROADMAPS · 技術ロードマップ集約</div>',
         '<div class="eyebrow">技術ロードマップ集約 · TECHNOLOGY ROADMAPS</div>', "eyebrow の語順"),
    ]:
        if b in html:
            print(f"  済み: {label}")
        elif a in html:
            html = html.replace(a, b, 1)
            print(f"  直した: {label}")

    SRC.write_text(html, encoding="utf-8")
    print(f"\n書き出しました: {SRC} ({SRC.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()

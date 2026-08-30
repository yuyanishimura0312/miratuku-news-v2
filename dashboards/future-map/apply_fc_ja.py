"""反証条件の日本語訳を、roadmaps.html と future-tech-map-v2.html の両方に当てる（冪等）。

★両方に当てるのは、同じ反証条件が2ページに出るため。片方だけ訳すと、
  同じマイルストーンの反証条件が2つの日本語で存在することになる。

★当てる前に自分で検査する（訳した側の自己申告を信用しない）。
  検査するのは「数字の並び」。反証条件は判定文であり、年・件数・単位・閾値が
  1つでも変われば判定そのものが変わる。文意の良し悪しは機械では見られないが、
  数字が動いていないことは機械で見られる。

使い方:
    python3 apply_fc_ja.py            # 検査して当てる
    python3 apply_fc_ja.py --check    # 検査だけして当てない
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGETS = ["roadmaps.html", "future-tech-map-v2.html"]
SRC_JSON = Path("/tmp/fc_to_translate.json")
JA_JSON = Path("/tmp/fc_translated.json")

# ページごとに DATA の入っている場所が違う
BLOCKS = {
    "roadmaps.html": r"const DATA=(\[.*?\]);const DOMS=",
    "future-tech-map-v2.html": r"const RM\s*=\s*(\[.*?\]);",
}


def digits(s: str):
    """数字の並び。年・件数・閾値が動いていないことを見るための指紋。"""
    return re.findall(r"\d+", s or "")


def main():
    if not JA_JSON.exists():
        raise SystemExit(f"訳が見つかりません: {JA_JSON}")
    src = {x["id"]: x["fc"] for x in json.loads(SRC_JSON.read_text(encoding="utf-8"))}
    ja = {x["id"]: x["ja"] for x in json.loads(JA_JSON.read_text(encoding="utf-8"))}

    print(f"原文 {len(src)} 件 / 訳 {len(ja)} 件")
    missing = sorted(set(src) - set(ja))
    if missing:
        print(f"★訳の無い id が {len(missing)} 件: {missing[:10]}")

    # --- 検査1: 数字の並びが保たれているか ---
    bad = []
    for i, s in src.items():
        if i not in ja:
            continue
        if digits(s) != digits(ja[i]):
            bad.append(i)
    print(f"数字の並びが変わったもの: {len(bad)} 件")
    for i in bad[:8]:
        print(f"  id={i}\n    原文: {src[i]}\n    訳文: {ja[i]}")

    # --- 検査2: 訳文が空・原文と同一でないか ---
    empty = [i for i in ja if not (ja[i] or "").strip()]
    if empty:
        print(f"★空の訳: {len(empty)} 件 {empty[:10]}")

    usable = {src[i]: ja[i] for i in ja if i in src and i not in bad and (ja[i] or "").strip()}
    print(f"当てられるもの: {len(usable)} / {len(src)}")

    if "--check" in sys.argv:
        print("--check のため当てません。")
        return
    if bad or missing or empty:
        print("★問題のあるものは当てません（残りだけ当てます）。")

    for name in TARGETS:
        p = HERE / name
        if not p.exists():
            print(f"  {name}: 見つからないので飛ばします")
            continue
        html = p.read_text(encoding="utf-8")
        m = re.search(BLOCKS[name], html, re.S)
        if not m:
            print(f"  {name}: データ block が見つかりません")
            continue
        DATA = json.loads(m.group(1))
        n = 0
        for d in DATA:
            for x in d.get("ms", []):
                fc = x.get("fc")
                if fc in usable and usable[fc] != fc:
                    x["fc_en"] = x.get("fc_en") or fc   # 原文を捨てない
                    x["fc"] = usable[fc]
                    n += 1
        html = html[:m.start(1)] + json.dumps(DATA, ensure_ascii=False) + html[m.end(1):]
        p.write_text(html, encoding="utf-8")
        print(f"  {name}: {n} 箇所を差し替え（{p.stat().st_size:,} bytes）")


if __name__ == "__main__":
    main()

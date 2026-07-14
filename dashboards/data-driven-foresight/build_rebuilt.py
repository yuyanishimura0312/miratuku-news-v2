#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deep Knowledge Foresight 本編の解体的再構築版を、本編公開意匠(向上版)で組版する。

- 外枠(top-bar/テーマ切替/TOC/reading-progress/JS)は原本編の機構を温存。
- <style> ブロックのみ /dm 向上版CSSに差し替え。
- カバー(sec00)とフッター免責を現在データ(2026-06-28)へ更新。
- 8章(sec01-08)を再構築版に差し替え(section id 保持=TOCアンカー維持)、図解SVGを注入。
- 出力は index_rebuilt.html (原 index.html は触らない / 公開は別途バックアップ後)。
"""
import os, re, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "index-v25-prerebuild.html")  # pristine v25 を土台に再構築 (置換が発火)
OUT  = os.path.join(HERE, "index_rebuilt.html")

CSS_ELEVATED = "/tmp/dkf_honpen_style_elevated.css"
CHAPTERS     = "/tmp/dkf_all_chapters.json"
FIGS_ALL     = "/tmp/dkf_figs_all.json"   # {fig_id: svg}

# ch番号 → 原本編 section id (TOCアンカー保持)
CH_ID = {1:"intro",2:"foundation-map",3:"three-foresight",4:"historical-findings",
         5:"convergence",6:"shallow-knowledge",7:"deep-knowledge",8:"invitation"}

def unescape(s, rounds=3):
    prev=s
    for _ in range(rounds):
        cur=html.unescape(prev)
        if cur==prev: return cur
        prev=cur
    return prev

def load():
    shell = open(SRC, encoding="utf-8").read()
    css   = open(CSS_ELEVATED, encoding="utf-8").read()
    chs   = json.load(open(CHAPTERS, encoding="utf-8"))
    figs  = json.load(open(FIGS_ALL, encoding="utf-8"))
    return shell, css, chs, figs

def build_chapter(n, ch, figs):
    cid   = CH_ID[n]
    title = unescape(ch.get("title",""))
    body  = unescape(ch.get("content_html",""))
    # 既存の <section ...> ラッパ / chapter-num / chapter-title を剥がして統一化
    body = re.sub(r'^\s*<section\b[^>]*>', '', body)
    body = re.sub(r'</section>\s*$', '', body)
    body = re.sub(r'<div class="chapter-num">.*?</div>', '', body, count=1, flags=re.S)
    body = re.sub(r'<h2 class="chapter-title">.*?</h2>', '', body, count=1, flags=re.S)
    # 図解プレースホルダ → SVG(figureで包む)
    def repl(m):
        fid=m.group(1)
        svg=figs.get(fid)
        if not svg:
            return f'<!-- MISSING FIG {fid} -->'
        svg=unescape(svg) if svg.lstrip().startswith('&lt;') else svg
        return (f'<figure class="diagram-wrap"><div class="diagram">{svg}</div></figure>')
    body = re.sub(r'\{\{FIG:([a-zA-Z0-9_-]+)\}\}', repl, body)
    head = (f'<div class="chapter-num">CHAPTER {n}</div>'
            f'<h2 class="chapter-title">{title}</h2>')
    return f'<section class="chapter" id="{cid}">{head}{body}</section>'

def main():
    shell, css, chs, figs = load()

    # 1) 原 <style> ブロック群を除去 → 向上版CSSを挿入
    #    (css ファイルは既に <style>...</style> で包まれているため二重包装しない)
    styled = re.sub(r'<style[^>]*>.*?</style>', '', shell, flags=re.S)
    css_block = css if css.lstrip().startswith('<style') else f'<style>\n{css}\n</style>'
    styled = styled.replace('</head>', f'{css_block}\n</head>', 1)
    shell = styled

    # 2) 8章領域(最初のchapter section 〜 最後のchapter section)を差し替え
    secs = list(re.finditer(r'<section\b.*?</section>', shell, re.S))
    # id付き8章を特定
    id_to_span = {}
    for m in secs:
        mid = re.search(r'id="([^"]+)"', m.group(0))
        if mid and mid.group(1) in CH_ID.values():
            id_to_span[mid.group(1)] = (m.start(), m.end())
    spans = [id_to_span[CH_ID[n]] for n in range(1,9) if CH_ID[n] in id_to_span]
    assert len(spans)==8, f"章section検出 {len(spans)}/8"
    region_start = spans[0][0]; region_end = spans[-1][1]
    new_chapters = "\n\n".join(build_chapter(n, chs[str(n)], figs) for n in range(1,9))
    shell = shell[:region_start] + new_chapters + shell[region_end:]

    # 3) カバー(sec00) の stale データ更新
    repls = [
      ("2026.05.17 · v25 · FORESIGHT &amp; DEEP KNOWLEDGE",
       "2026.06.28 · v26.1 · 解体的再構築 + 歴史変動サイクル層 · FORESIGHT &amp; DEEP KNOWLEDGE"),
      ("約500万レコード・70+のデータベース・三層の未来学アプローチ・歴史変動サイクルを横断する解析から辿り着いた未来洞察。",
       "597のデータベース・約6,340万行を横断し、三層の未来学アプローチと前方未来学(2030/2050/2070/2100)、歴史変動サイクルから再走した未来洞察。現在データ(2026年6月28日実測)で全所見を3観点の敵対的検証にかけ、射程・確度・反証条件を併記する。"),
      ("図解 23点 · 読了 約35分 · NPO法人ミラツク",
       "図解 27点 · 読了 約48分 · NPO法人ミラツク"),
      # og / meta
      ("約500万レコード・70+ DBが照らす", "597DB・約6,340万行が照らす"),
    ]
    for a,b in repls:
        shell = shell.replace(a,b)

    # 4) フッター免責の時点表現を更新
    shell = shell.replace(
      "本ページは2026年5月時点でのNPO法人ミラツクのデータベース構築状況・解析結果・未来洞察を要約したものです。引用された数値・規模は2026年5月のスナップショットであり、データベースは継続的に拡張・更新されています。",
      "本ページは2026年6月28日に現在データで再走したNPO法人ミラツクのデータベース構築状況・解析結果・未来洞察です(2026年5月公開版を解体的に再構築)。引用した数値・規模は2026年6月28日の実測であり、データベースは継続的に拡張・更新されています。各所見は3観点の敵対的独立検証を経て確定/要再検討に分類し、射程・確度・反証条件を併記しています。")

    open(OUT,"w",encoding="utf-8").write(shell)
    nfig = shell.count('class="diagram-wrap"')
    miss = re.findall(r'<!-- MISSING FIG ([^ ]+) -->', shell)
    print(f"[ok] {OUT} ({len(shell):,} bytes / 図解 {nfig} 点 / 章8)")
    if miss: print(f"[warn] 未注入図解: {miss}")

if __name__=="__main__":
    main()

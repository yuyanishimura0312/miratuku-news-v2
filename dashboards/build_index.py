#!/usr/bin/env python3
"""dashboards/ の索引を作る。

★ /dashboards/ に index.html が無く 404 になっていたため新設（2026-08-05）。
  個別ページは開けるのに一覧が無い、という状態は「どこに何があるか分からない」
  そのものなので、機械で作って以後は取りこぼさないようにする。

題名は各ファイルの <title> から読む（手で台帳を作らない＝二重管理しない）。
`_` で始まるものは部品・テンプレートなので載せない。
"""
from __future__ import annotations
import datetime, html, pathlib, re, subprocess

BASE = pathlib.Path(__file__).parent
OUT = BASE / "index.html"

# 題名の末尾に付く媒体名。索引では邪魔なので落とす。
TAIL = re.compile(r"\s*[|｜]\s*(miratuku[- ]news|Miratuku News|ミラツク.*)$", re.I)


def title_of(p: pathlib.Path) -> str:
    h = p.read_text(encoding="utf-8", errors="ignore")[:6000]
    m = re.search(r"<title>(.*?)</title>", h, re.S)
    if not m:
        return p.stem
    t = html.unescape(re.sub(r"\s+", " ", m.group(1)).strip())
    return TAIL.sub("", t).strip() or p.stem


def main() -> None:
    fs = [p for p in sorted(BASE.glob("*.html"))
          if not p.name.startswith("_") and p.name != "index.html"]
    rows = []
    for p in fs:
        t = title_of(p)
        st = p.stat()
        rows.append((p.name, t, datetime.date.fromtimestamp(st.st_mtime).isoformat(),
                     st.st_size))

    # 更新の新しい順に並べる。何が最近動いたかが、探すときの手がかりになる。
    rows.sort(key=lambda r: r[2], reverse=True)

    items = "\n".join(
        f'<li class="it" data-k="{html.escape((n + " " + t).lower())}">'
        f'<a href="{n}"><span class="t">{html.escape(t)}</span>'
        f'<span class="f">{html.escape(n)}</span></a>'
        f'<span class="d">{d}</span></li>'
        for n, t, d, _ in rows)

    doc = f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ダッシュボード索引 ｜ esse-sense ／ NPO法人ミラツク</title>
<link rel="icon" href="https://esse-sense.com/favicon.ico">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&family=Fira+Code:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{{
  --bg:#FFFFFF; --surface:#F7F7F5; --text:#121212; --text-secondary:#555555;
  --text-muted:#6B6B6B; --border:#D9D9D9; --border-light:#EEEEEE;
  --accent-warm:#CC1400;
  --font:"Noto Sans JP","Hiragino Sans",-apple-system,sans-serif;
  --mono:"Fira Code",SFMono-Regular,ui-monospace,monospace;
}}
[data-theme="dark"]{{
  --bg:#121212; --surface:#1A1A1A; --text:#E0E0E0; --text-secondary:#AAAAAA;
  --text-muted:#8A8A8A; --border:#333333; --border-light:#2A2A2A;
  --accent-warm:#FF4030;
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--text);font-family:var(--font);
  line-height:1.8;letter-spacing:.02em;font-feature-settings:"palt";
  -webkit-font-smoothing:antialiased}}
.top-bar{{position:sticky;top:0;z-index:50;display:flex;align-items:center;
  justify-content:space-between;height:48px;padding:0 22px;background:var(--bg);
  border-top:3px solid #121212;border-bottom:1px solid var(--border-light)}}
[data-theme="dark"] .top-bar{{border-top-color:var(--accent-warm)}}
.brand{{font-weight:900;font-size:13px;letter-spacing:.12em}}
.brand b{{color:var(--accent-warm)}}
.tbtn{{background:none;border:1px solid var(--border);padding:4px 12px;
  font-size:12px;color:var(--text-secondary);cursor:pointer;font-family:var(--font)}}
main{{max-width:860px;margin:0 auto;padding:34px 24px 90px}}
h1{{font-size:28px;font-weight:900;letter-spacing:-.015em;margin:0 0 10px}}
.lead{{font-size:14px;color:var(--text-secondary);max-width:62ch;margin:0 0 24px}}
.tools{{display:flex;gap:10px;align-items:center;position:sticky;top:48px;
  background:var(--bg);padding:12px 0;border-bottom:1px solid var(--border-light);z-index:40}}
#q{{flex:1;padding:9px 12px;font-size:14px;font-family:var(--font);
  border:1px solid var(--border);background:var(--bg);color:var(--text)}}
#q:focus{{outline:2px solid var(--accent-warm);outline-offset:1px}}
#cnt{{font-family:var(--mono);font-size:12px;color:var(--text-muted);white-space:nowrap}}
ul{{list-style:none;margin:0;padding:0}}
.it{{display:flex;align-items:baseline;gap:12px;padding:9px 2px;
  border-bottom:1px solid var(--border-light)}}
.it a{{flex:1;min-width:0;text-decoration:none;color:var(--text);
  display:flex;flex-direction:column;gap:1px}}
.it a:hover .t{{color:var(--accent-warm)}}
.it a:focus-visible{{outline:2px solid var(--accent-warm);outline-offset:2px}}
.t{{font-size:14.5px;font-weight:700;line-height:1.5}}
.f{{font-family:var(--mono);font-size:11px;color:var(--text-muted)}}
.d{{font-family:var(--mono);font-size:11px;color:var(--text-muted);white-space:nowrap}}
#zero{{padding:30px 0;color:var(--text-muted);font-size:14px}}
footer{{margin-top:40px;padding-top:16px;border-top:1px solid var(--border);
  font-size:12px;color:var(--text-muted)}}
@media(max-width:560px){{.d{{display:none}}}}
@media print{{.top-bar,.tools{{display:none}}}}
</style></head>
<body>
<div class="top-bar">
  <div class="brand">esse-sense <b>／</b> NPO法人ミラツク</div>
  <button class="tbtn" id="theme" type="button">ダーク</button>
</div>
<main>
<h1>ダッシュボード索引</h1>
<p class="lead">このディレクトリに置かれた {len(rows)} 点の一覧である。題名は各ページの
title から機械で読み取っており、手で作った台帳ではない。並びは更新の新しい順。
名前・題名のどちらでも絞り込める。</p>

<div class="tools">
  <input id="q" type="search" placeholder="題名・ファイル名で絞る（/ で移動）"
    aria-label="ダッシュボードを絞り込む">
  <span id="cnt" role="status" aria-live="polite">{len(rows)}件</span>
</div>

<ul id="list">
{items}
</ul>
<div id="zero" hidden>該当するものがありません。</div>

<footer>生成 {datetime.date.today().isoformat()}　／　esse-sense ／ NPO法人ミラツク
　｜　再生成は <span class="f">python3 dashboards/build_index.py</span></footer>
</main>
<script>
(function(){{
  var q=document.getElementById('q'), cnt=document.getElementById('cnt'),
      zero=document.getElementById('zero'),
      its=[].slice.call(document.querySelectorAll('.it'));
  function run(){{
    var v=q.value.trim().toLowerCase(), n=0;
    its.forEach(function(el){{
      var hit=!v||el.dataset.k.indexOf(v)>=0;
      el.hidden=!hit; if(hit) n++;
    }});
    cnt.textContent=n+'件'; zero.hidden=n>0;
  }}
  q.addEventListener('input',run);
  addEventListener('keydown',function(e){{
    if(e.key==='/'&&document.activeElement!==q){{q.focus();e.preventDefault();}}
  }});
  var b=document.getElementById('theme');
  function set(v){{document.documentElement.setAttribute('data-theme',v);
    localStorage.setItem('mn-theme',v); b.textContent=v==='dark'?'ライト':'ダーク';}}
  set(localStorage.getItem('mn-theme')||'light');
  b.addEventListener('click',function(){{
    set(document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark');}});
}})();
</script>
</body></html>
"""
    OUT.write_text(doc, encoding="utf-8")
    print(f"[ok] {OUT}  {len(rows)} 点  {len(doc):,} bytes")


main()

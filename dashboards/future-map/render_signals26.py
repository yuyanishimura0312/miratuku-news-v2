#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""シグナル一覧（26領域版）のページを書き出す。

★版面は index.html（18テーマ版）の CSS を**ビルド時に読んで再利用**する。
  写経すると片方を直したときにもう片方がずれるため、複製しない。

★18テーマ版が抱えていた事実誤りを持ち込まない:
  18テーマ版は「シグナルDB の 2020〜2026年の実データ」と3か所で述べているが、
  実測では signals の 99.4% が2026年で、このページが載せる178件の検知日は
  **2026-04-25〜07-19** に収まる。数えた値をそのまま書く。

★測っていないものを測ったと書かない:
  signal.db には Gwet AC1 = 0.5148 という一致度があるが、それは
  「シグナル → 型（5分類）」の作業の指標であって、**領域への割当の指標ではない**。
  領域割当の精度は測られていない。そう書く。
"""
import json
import os
import re
from datetime import datetime
from html import escape as esc

import build_signals26 as B

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.join(HERE, "index.html")
OUT = os.path.join(HERE, "signals-26.html")

EXTRA_CSS = """
/* ★このページ内だけの是正。サイト共通の --ink-mute (#8A7868) は白地で CR 3.99 と
   AA(4.5) に届かない。他ページのCSSは触らず、このページのトークンだけ darken する。
   （共通CSSを直すと index.html など全ページの見えが変わるため、ここでは行わない） */
:root{ --ink-mute:#6F5F51; }
.hero .wordmark small{ color:var(--ink-cite); }

/* ── 26領域版で足した部品 ── */
.t-meta{font:700 10.5px/1 var(--jp);letter-spacing:.12em;color:var(--paper);
  background:var(--accent);border-radius:999px;padding:5px 10px;display:inline-block}
.t-w{font:500 11.5px/1.5 var(--mono);color:var(--ink-cite)}
.t-labels{display:flex;flex-wrap:wrap;gap:5px;margin-top:10px}
.t-labels span{font:500 11px/1.5 var(--jp);color:var(--ink-soft);
  border:1px solid var(--rule);border-radius:999px;padding:3px 9px}
.c-cross{font:700 10px/1 var(--jp);letter-spacing:.08em;color:var(--accent);
  border:1px solid var(--accent);border-radius:3px;padding:3px 6px;display:inline-block}
.c-src{margin-top:9px;padding-top:8px;border-top:1px dashed var(--rule)}
.c-src a{display:block;font:400 11.5px/1.6 var(--jp);color:var(--ink-cite);
  text-decoration:none;border-bottom:1px solid transparent}
.c-src a:hover{color:var(--accent);border-bottom-color:var(--accent)}
.c-src .sm{font:500 10.5px/1.5 var(--mono);color:var(--ink-cite)}
.c-nosrc{margin-top:9px;font:400 11px/1.5 var(--jp);color:var(--ink-cite)}
.limits{margin:26px 0 0;padding:18px 20px;background:var(--surface-warm);
  border-left:3px solid var(--accent)}
.limits h2{font:700 13px/1.5 var(--jp);letter-spacing:.06em;color:var(--ink-strong);margin:0 0 10px}
.limits ul{margin:0;padding-left:1.1em}
.limits li{font:400 12.5px/1.9 var(--jp);color:var(--ink-soft);margin-bottom:5px}
.limits b{color:var(--accent)}
/* 「反潮流」ラベルは 9.5px 太字で CR 4.1。太字でも 14px 未満は AA 4.5 が要る */
.c-counter b{color:var(--ink-cite)}
"""


def chip_id(s):
    return re.sub(r"[^\w]", "_", s)


def main():
    data, metas, st = B.main()
    css = re.search(r"<style>(.*?)</style>", open(IDX, encoding="utf-8").read(), re.S).group(1)
    stamp = datetime.now().strftime("%Y-%m-%d")

    meta_counts = {}
    for d in data:
        meta_counts[d["meta"]] = meta_counts.get(d["meta"], 0) + 1
    chips = "".join(
        '<button type="button" class="chip" data-cat="%s">%s（%d）</button>'
        % (esc(m["name_ja"]), esc(m["name_ja"]), meta_counts.get(m["name_ja"], 0))
        for m in metas)

    payload = json.dumps({"data": data, "stats": st}, ensure_ascii=False)

    doc = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>シグナル一覧（26領域版）｜MIRA TUKU</title>
<meta name="description" content="未来×技術 統合マップ 2026 の26領域ごとに、シグナルDB から抽出したシグナルを一覧化。各シグナルに一次記事へのリンクを付けた。">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700;900&family=Noto+Serif+JP:wght@400;600&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
<style>{css}{EXTRA_CSS}</style>
</head>
<body data-preset="miratuku-earth">
<header class="hero">
<div class="wrap">
  <div class="kick">
    <div class="eyebrow">FUTURE DOMAINS &amp; SIGNALS &nbsp;·&nbsp; <a href="dashboard.html" style="color:var(--accent);border-bottom:1px solid var(--accent);padding-bottom:1px">ダッシュボード（全体像）へ →</a></div>
    <div class="wordmark"><img src="assets/miratuku-logo-h.png" alt="MIRA TUKU"><small>all rights reserved.</small></div>
  </div>
  <h1>シグナル一覧<small style="display:block;font-size:.42em;font-weight:700;color:var(--accent);letter-spacing:.04em;margin-top:6px">26領域版（2026年 GTA 準拠）｜18テーマ版はこちら → <a href="index.html" style="color:inherit;border-bottom:1px solid currentColor">シグナル一覧（18テーマ版）</a></small></h1>
  <p class="lead">未来予測 {st['corpus']:,} 件を束ねて浮かび上がった<b>26の領域</b>ごとに、シグナルDB（signal.db）から抽出したシグナルを並べています。各領域に <b>10 件ずつ</b>（延べ {st['slots']} 件・実数 {st['uniq']} 件）。領域は <b>8 つのメタ領域</b>に属します。★18テーマ版と違い、各シグナルには<b>一次記事へのリンク</b>を付けました（{st['with_src']}/{st['uniq']} 件）。</p>
  <div class="stats">
    <div class="stat"><div class="n">{st['domains']}<small>領域</small></div><div class="k">Domains</div></div>
    <div class="stat"><div class="n">{st['uniq']}<small>件</small></div><div class="k">Signals（実数）</div></div>
    <div class="stat"><div class="n">{st['metas']}<small>領域</small></div><div class="k">Meta Domains</div></div>
    <div class="stat"><div class="n">{st['dwin'][0][:7]}–{st['dwin'][1][5:7]}<small>月</small></div><div class="k">Detected</div></div>
  </div>
</div>
</header>

<div class="controls">
  <div class="wrap" id="filterbar">
    <span class="clabel">Filter</span>
    <button type="button" class="chip all" data-cat="all" data-on="1">すべて（{st['domains']}）</button>
    {chips}
  </div>
</div>

<main>
<div class="wrap">
  <div class="note">
    <span class="nlabel">指標の見方</span>
    <span class="li"><span class="dot" style="width:11px;height:11px"></span><span class="dot" style="width:8px;height:8px"></span><span class="dot" style="width:5px;height:5px"></span>&nbsp;影響度（重大→小）</span>
    <span class="li">H1/H2/H3 &nbsp;三つの地平（近未来／中期／長期）</span>
    <span class="li">CLA &nbsp;現象／体系的原因／世界観／神話</span>
    <span class="li">横断 &nbsp;複数の領域に現れるシグナル</span>
    <span class="txt">シグナルは PESTLE 構造化ニュースから抽出された実データです。断定ではなく「起こりうる兆し」の観測にすぎません。</span>
  </div>

  <div id="themes"></div>

  <div class="limits">
    <h2>★このページが言わないこと</h2>
    <ul>
      <li><b>領域への割当は機械的です。</b>{esc(st['method'])} による近傍分類で、人が1件ずつ確かめたものではありません。<b>この割当の精度は測られていません。</b>（signal.db には一致度 Gwet AC1 = 0.5148 の記録がありますが、それは「シグナル → 型（5分類）」という<b>別の作業</b>の指標です。領域割当の指標として読まないでください。）</li>
      <li><b>観測の窓は狭い。</b>ここに載る {st['uniq']} 件の検知日は <b>{st['dwin'][0]} 〜 {st['dwin'][1]}</b>（約3か月）に収まります。シグナルの期間表記は {st['win'][0]} 〜 {st['win'][1]}。長期の趨勢ではなく、<b>この窓で拾えたもの</b>です。</li>
      <li><b>延べと実数が違う。</b>延べ {st['slots']} 件のうち実数は {st['uniq']} 件で、<b>{st['cross']} 件は複数の領域に現れます</b>（カードに「横断」と表示）。一般的な内容のシグナルほど多くの領域に付きます。件数を足し上げないでください。</li>
      <li><b>時点のスナップショットです。</b>領域別シグナルは <b>{st['enr_stamp']}</b> に抽出したもので、その後に検知されたシグナルは入っていません。</li>
      <li><b>網羅ではありません。</b>各領域から複合スコア上位10件を採っているだけで、領域の全体像でも、重要度の順位でもありません。</li>
    </ul>
  </div>
</div>
</main>

<footer>
<div class="wrap">
  <div class="fnote">出典：未来×技術 統合マップ 2026 の<b>26領域</b>（未来予測 {st['corpus']:,} 件を束ねた区分）。シグナルは <b>signal.db</b>（PESTLE 構造化ニュース由来）の実データで、領域への割当は {esc(st['method'])}。一次記事は <b>pestle.db</b> の記事レコードへ解決したもので、<b>隔離済みの記事は除いてあります</b>。作成 {stamp}</div>
  <div class="fmark"><img src="assets/miratuku-logo-h.png" alt="MIRA TUKU"></div>
</div>
</footer>

<script>
const PAYLOAD = {payload};
const DATA = PAYLOAD.data;
const TYPE = {json.dumps(B.TYPE_JA, ensure_ascii=False)};
const IMP = {{critical:["重大",11],high:["大",8.5],medium:["中",6],low:["小",4]}};
const CLA = {json.dumps(B.CLA_JA, ensure_ascii=False)};
const TH = {json.dumps(B.TH_JA, ensure_ascii=False)};
const esc = s => (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");

function sigCard(s){{
  const im = IMP[s.impact] || ["—",6];
  const src = (s.src||[]).map(a =>
      `<a href="${{esc(a.u)}}" target="_blank" rel="noopener">${{esc(a.t)}}<span class="sm"> ${{esc(a.s)}} ${{esc(a.d)}}</span></a>`).join("");
  return `<article class="card">
    <div class="c-type">${{esc(TYPE[s.type] || s.type || "シグナル")}}</div>
    <h3 class="c-name">${{esc(s.name)}}</h3>
    <p class="c-desc">${{esc(s.desc)}}</p>
    <div class="c-meta">
      <span class="c-dot" style="width:${{im[1]}}px;height:${{im[1]}}px"></span><span>影響 ${{esc(im[0])}}</span>
      <span>${{esc(TH[s.h] || s.h || "")}}</span>
      <span>${{esc(CLA[s.cla] || "")}}</span>
      ${{s.score != null ? `<span class="c-nov">SCORE ${{s.score}}</span>` : ""}}
      ${{(s.cross && s.cross.length) ? `<span class="c-cross">横断 ${{s.cross.length}}領域</span>` : ""}}
    </div>
    ${{s.pestle && s.pestle.length ? `<div class="pestle">${{s.pestle.map(p=>`<span>${{esc(p)}}</span>`).join("")}}</div>` : ""}}
    ${{s.counter ? `<div class="c-counter"><b>反潮流</b> ${{esc(s.counter)}}</div>` : ""}}
    ${{src ? `<div class="c-src">${{src}}</div>` : `<div class="c-nosrc">★この兆しには一次記事のリンクが付いていません。</div>`}}
  </article>`;
}}

function render(){{
  document.getElementById("themes").innerHTML = DATA.map(d => `
  <section class="theme" data-cat="${{esc(d.meta)}}">
    <div class="t-head">
      <div class="t-num">${{String(d.id).padStart(2,"0")}}</div>
      <div class="t-body">
        <h2 class="t-title">${{esc(d.title)}}</h2>
        <div class="t-cat"><span class="t-meta">${{esc(d.meta)}}</span>
          <span class="t-w">未来予測 ${{d.weight.toLocaleString()}} 件から</span></div>
        <p class="t-ov">${{esc(d.ov)}}</p>
        <div class="t-labels">${{(d.labels||[]).map(l=>`<span>${{esc(l)}}</span>`).join("")}}</div>
      </div>
    </div>
    <div class="grid">${{d.signals.map(sigCard).join("")}}</div>
  </section>`).join("");
}}
render();

document.getElementById("filterbar").addEventListener("click", e => {{
  const b = e.target.closest(".chip"); if(!b) return;
  document.querySelectorAll(".chip").forEach(c => c.removeAttribute("data-on"));
  b.setAttribute("data-on","1");
  const cat = b.dataset.cat;
  document.querySelectorAll(".theme").forEach(t => {{
    t.classList.toggle("hidden", cat !== "all" && t.dataset.cat !== cat);
  }});
}});
</script>
</body>
</html>
"""
    open(OUT, "w", encoding="utf-8").write(doc)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")
    print(json.dumps(st, ensure_ascii=False))


if __name__ == "__main__":
    main()

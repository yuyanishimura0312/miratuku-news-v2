"""未来学の系譜デッキを「投影用」に組み直す（冪等・再実行で同じものが出る）。

★これまでの版は A4 横の【説明用】だった。1枚に図・読み取り方4項目・言えないこと4項目を
  同居させており、手元で読む資料としては良いが、投影すると誰も読めない。
  投影用は前提が違う ——
    - 遠くから見る（本文 24px 以下にしない。説明用は 11-13px だった）
    - 1枚に論点は1つ（説明用の1枚を、投影では3-4枚に開く）
    - 図は主役（画面の6割以上）
    - 16:9（A4横 1.414 でなく 1.778）
  ★説明用の情報は捨てず、話し手の手元資料として同じ内容を別に残す。

図は既存の3枚から取り出して使う（描き直さない）。座標系は 960x262 のまま拡大する。

ロゴは公式の素材を使う:
  assets/miratuku-logo-mark.png … マーク＋ワードマーク（表紙）
  assets/miratuku-logo-h.png    … 横組み（各ページの隅）
"""
import base64
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
# ★取り出し元は説明用に固定する。投影用（出力先）から読むと、2回目の実行で
#   図の並びが変わって別の図が入る。入力と出力を同じファイルにしない。
HANDOUT_FIRST = HERE / "futures-genealogy-handout.html"
SRC = HANDOUT_FIRST if HANDOUT_FIRST.exists() else HERE / "futures-genealogy.html"
OUT = HERE / "futures-genealogy.html"          # 投影用として置き換える
HANDOUT = HERE / "futures-genealogy-handout.html"   # 説明用は名前を変えて残す
ASSETS = HERE.parent / "assets"


def b64(p: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()


def figures(html: str):
    figs = re.findall(r'<svg class="fig".*?</svg>', html, re.S)
    if len(figs) < 3:
        raise SystemExit(f"図が3枚見つかりません（{len(figs)}枚）")
    return figs


CSS = """
:root{
  --bg:#FFFFFF; --ink:#0E0E0E; --ink-soft:#3A3A3A; --ink-mute:#6B6B6B;
  --ink-cite:#595959; --rule:#DEDEDE; --rule-light:#ECECEC;
  --surface:#FAFAF7; --accent:#CC1400;
  --sans:"Noto Sans JP","Hiragino Sans",-apple-system,sans-serif;
  --mono:"Fira Code","SF Mono",Menlo,monospace;
}
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
html,body{margin:0;padding:0;background:#2A2A2A}
body{font-family:var(--sans);color:var(--ink);font-feature-settings:"palt","kern"}
.deck{display:flex;flex-direction:column;align-items:center;gap:22px;padding:22px 0 64px}

/* 16:9。投影は画面いっぱいに出るので、内側の余白は広く取る。 */
.slide{
  width:1280px;height:720px;background:var(--bg);position:relative;
  padding:64px 76px 56px;display:grid;grid-template-rows:auto 1fr auto;gap:20px;
  box-shadow:0 10px 40px rgba(20,20,20,.5);
}
.slide.dark{background:#141210;color:#F4F1EC}
.slide.dark .eyebrow{color:#E0846A}
.slide.dark h2,.slide.dark .lead{color:#F4F1EC}
.slide.dark .foot{color:#9C948A;border-color:#332E29}

.eyebrow{font-size:15px;font-weight:700;letter-spacing:.2em;color:var(--accent);margin:0}
h1{font-size:70px;font-weight:900;line-height:1.32;letter-spacing:-.02em;margin:0}
h2{font-size:46px;font-weight:900;line-height:1.42;letter-spacing:-.015em;margin:0}
.lead{font-size:26px;line-height:1.85;color:var(--ink-soft);margin:0;max-width:34em}
.big{font-size:34px;line-height:1.7;font-weight:700;margin:0}
.mid{display:flex;flex-direction:column;justify-content:center;min-height:0}
.figwrap{display:flex;align-items:center;justify-content:center;min-height:0}
/* ★height:100% は祖先の高さが確定しないと auto に落ち、切り出した図の高さが決まらない。
   切り出した図は縦横比を明示して高さを確定させる（figcrop）。 */
.figwrap svg{width:100%;height:100%;max-height:100%;overflow:hidden}
.figwrap svg.figcrop{height:auto;aspect-ratio:96/10;align-self:center}

/* 数字を主役にする面 */
.nums{display:flex;gap:64px;align-items:flex-end}
.num{display:flex;flex-direction:column;gap:6px}
.num b{font-size:92px;font-weight:900;line-height:1;color:var(--accent);font-variant-numeric:tabular-nums}
.num span{font-size:20px;color:var(--ink-soft)}

ul.pts{margin:0;padding-left:1.1em;display:flex;flex-direction:column;gap:20px}
ul.pts li{font-size:27px;line-height:1.7}
ul.pts li b{color:var(--accent)}

.two{display:grid;grid-template-columns:1fr 1fr;gap:44px;align-items:start}
.card{border:1px solid var(--rule);border-left:5px solid var(--accent);
  background:var(--surface);padding:24px 26px}
.card h3{font-size:26px;font-weight:900;margin:0 0 14px}
.card p{font-size:20px;line-height:1.8;margin:0 0 10px;color:var(--ink-soft)}
.card p:last-child{margin-bottom:0}
.card .k{font-size:14px;font-weight:700;letter-spacing:.1em;color:var(--ink-mute);display:block}

.foot{display:flex;justify-content:space-between;align-items:flex-end;
  font-size:14px;color:var(--ink-cite);border-top:1px solid var(--rule);padding-top:14px}
.foot .src{max-width:74%;line-height:1.7}
.logo{position:absolute;right:76px;top:56px;height:30px;opacity:.92}
.slide.dark .logo{filter:brightness(0) invert(1);opacity:.85}
.pg{font-family:var(--mono);font-size:14px;color:var(--ink-cite)}

/* 表紙 */
/* 表紙。★justify-items:start だとフッターまで縮んで出典が折り返す。 */
.cover{grid-template-rows:1fr auto;align-content:center}
.cover>div:first-of-type{align-self:center}
.cover .mark{height:190px;margin-bottom:36px}
.cover h1{font-size:80px}

.navbar{position:fixed;left:50%;transform:translateX(-50%);bottom:16px;z-index:50;
  display:flex;gap:8px;align-items:center;background:#141210;color:#F4F1EC;
  padding:8px 14px;border-radius:999px;font-size:13px;font-family:var(--mono)}
.navbar button{background:none;border:1px solid #4A443C;color:#F4F1EC;border-radius:999px;
  padding:4px 12px;cursor:pointer;font-size:13px}
.navbar button:hover{background:#2A2620}

/* プレゼンモード：1枚だけを画面いっぱいに */
body.present{background:#000;overflow:hidden}
body.present .deck{padding:0;gap:0}
body.present .slide{display:none;box-shadow:none}
body.present .slide.active{display:grid;
  position:fixed;inset:0;width:100vw;height:100vh;
  padding:min(5vh,64px) min(6vw,76px) min(4.4vh,56px);
  /* 1280x720 を基準に、画面幅で線形に伸ばす */
  font-size:calc(100vw / 1280 * 16);
}
body.present .slide.active h1{font-size:calc(100vw/1280*70)}
body.present .slide.active .cover h1,body.present .slide.active.cover h1{font-size:calc(100vw/1280*80)}
body.present .slide.active h2{font-size:calc(100vw/1280*46)}
body.present .slide.active .lead{font-size:calc(100vw/1280*26)}
body.present .slide.active .big{font-size:calc(100vw/1280*34)}
body.present .slide.active ul.pts li{font-size:calc(100vw/1280*27)}
body.present .slide.active .num b{font-size:calc(100vw/1280*92)}
body.present .slide.active .num span{font-size:calc(100vw/1280*20)}
body.present .slide.active .card h3{font-size:calc(100vw/1280*26)}
body.present .slide.active .card p{font-size:calc(100vw/1280*20)}
body.present .slide.active .foot{font-size:calc(100vw/1280*14)}
body.present .slide.active .logo{height:calc(100vw/1280*30);right:min(6vw,76px);top:min(4.4vh,56px)}
body.present .navbar{opacity:.25}
body.present .navbar:hover{opacity:1}

@media print{
  @page{size:1280px 720px;margin:0}
  html,body{background:#fff}
  .deck{padding:0;gap:0}
  .slide{box-shadow:none;break-after:page;page-break-after:always}
  .navbar{display:none}
}
"""

NAV_JS = """
(function(){
  var slides=[].slice.call(document.querySelectorAll('.slide'));
  var i=0, present=false;
  var cur=document.getElementById('pgCur'), tot=document.getElementById('pgTot');
  if(tot) tot.textContent=slides.length;
  function show(){
    if(present){ slides.forEach(function(s,k){ s.classList.toggle('active',k===i); }); }
    else { slides[i] && slides[i].scrollIntoView({behavior:'smooth',block:'start'}); }
    if(cur) cur.textContent=i+1;
    try{ history.replaceState(null,'','#s'+String(i+1).padStart(2,'0')); }catch(e){}
  }
  function go(n){ i=Math.max(0,Math.min(slides.length-1,n)); show(); }
  window.nextSlide=function(){ go(i+1); };
  window.prevSlide=function(){ go(i-1); };
  window.togglePresent=function(){
    present=!present; document.body.classList.toggle('present',present); show();
  };
  window.toggleFull=function(){
    if(document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen();
  };
  document.addEventListener('keydown',function(e){
    if(/^(INPUT|TEXTAREA)$/.test((document.activeElement||{}).tagName||'')) return;
    var k=e.key;
    if(k==='ArrowRight'||k==='ArrowDown'||k===' '||k==='PageDown'||k==='j'||k==='l'){e.preventDefault();nextSlide();}
    else if(k==='ArrowLeft'||k==='ArrowUp'||k==='PageUp'||k==='k'||k==='h'){e.preventDefault();prevSlide();}
    else if(k==='p'||k==='P'){e.preventDefault();togglePresent();}
    else if(k==='f'||k==='F'){e.preventDefault();toggleFull();}
    else if(k==='Home'){e.preventDefault();go(0);}
    else if(k==='End'){e.preventDefault();go(slides.length-1);}
  });
  var m=(location.hash||'').match(/^#s(\\d+)/); if(m) go(parseInt(m[1],10)-1);
  show();
})();
"""


def slide(n: int, total: int, body: str, src: str, logo: str, dark=False, cls="") -> str:
    tone = " dark" if dark else ""
    return f"""
<section class="slide{tone} {cls}" id="s{n:02d}">
  <img class="logo" src="{logo}" alt="ミラツク">
  {body}
  <div class="foot"><span class="src">{src}</span><span class="pg">{n:02d} / {total:02d}</span></div>
</section>"""


def main():
    html = SRC.read_text(encoding="utf-8")
    fig1, fig2, fig3 = figures(html)

    # 説明用の版を別名で残す（捨てない）
    if not HANDOUT.exists():
        HANDOUT.write_text(html, encoding="utf-8")
        print(f"説明用を保存: {HANDOUT.name}")

    logo_h = b64(ASSETS / "miratuku-logo-h.png")
    logo_mark = b64(ASSETS / "miratuku-logo-mark.png")

    S = []
    T = 10

    # 1 表紙
    S.append(f"""
<section class="slide cover" id="s01">
  <div>
    <img class="mark" src="{logo_mark}" alt="ミラツク">
    <p class="eyebrow">FUTURES STUDIES DATABASE ／ 未来学の系譜</p>
    <h1>未来学は1つの系譜ではない</h1>
    <p class="lead" style="margin-top:26px">学派17と、それを結ぶ26本の線。<br>そして、方法にもう一本の線がある。</p>
  </div>
  <div class="foot"><span class="src">NPO法人ミラツク ／ 2026年8月30日</span><span class="pg">01 / {T:02d}</span></div>
</section>""")

    # 2 数字
    S.append(slide(2, T, """
  <div><p class="eyebrow">この地図が持っているもの</p>
    <h2>17の学派を、26本の線で結んだ</h2></div>
  <div class="mid"><div class="nums">
    <div class="num"><b>17</b><span>学派</span></div>
    <div class="num"><b>26</b><span>影響の線</span></div>
    <div class="num"><b>6</b><span>人物関係で裏づけ</span></div>
    <div class="num"><b>3</b><span>文献で裏づけ</span></div>
    <div class="num"><b>17</b><span>編纂（裏づけなし）</span></div>
  </div>
  <p class="big" style="margin-top:40px">線の3分の2は、<b style="color:var(--accent)">私たちの編纂判断</b>である。</p></div>
""", "出典 futures_studies.db（学派17・関係26）", logo_h))

    # 3 図1
    S.append(slide(3, T, f"""
  <div><p class="eyebrow">FIG.01</p><h2>学派の系譜 — 設立年 × 地域</h2></div>
  <div class="figwrap">{fig1}</div>
""", "線種＝関係の裏づけ（実線＝人物照合／破線＝文献／点線＝編纂）", logo_h))

    # 4 主張（暗転）
    S.append(slide(4, T, """
  <div><p class="eyebrow">読み方</p></div>
  <div class="mid">
    <h2 style="font-size:56px">距離は関係の近さであって、<br>影響の強さではない。</h2>
    <p class="lead" style="margin-top:34px;font-size:28px">26本すべてで関係の年が空欄である。<br>矢印は起点の学派の設立年から引いてある。</p>
  </div>
""", "この図から言えないこと（1／3）", logo_h, dark=True))

    # 5 方法の線
    S.append(slide(5, T, """
  <div><p class="eyebrow">もう一本の線</p>
    <h2>学派の系譜とは別に、<br>方法にも系譜がある</h2></div>
  <div class="mid"><ul class="pts">
    <li><b>1961</b>　Forrester『Industrial Dynamics』── 未来を計算する道具が生まれる</li>
    <li><b>1971</b>　ローマクラブがベルンに招く。呼称が <b>system dynamics</b> へ変わる</li>
    <li><b>1981</b>　Checkland が hard と soft を分ける ── 計算から対話へ</li>
  </ul></div>
""", "出典 System Dynamics Society ／ MIT Sloan ／ Checkland 1981", logo_h))

    # 6 図2
    S.append(slide(6, T, f"""
  <div><p class="eyebrow">FIG.02</p><h2>方法の系譜 — 前頁と同じ年軸</h2></div>
  <div class="figwrap">{fig2}</div>
""", "文献に記述あり 2本／編纂 1本。人物照合は 0本（方法の層は人物照合を持たない）", logo_h))

    # 7 分岐（主張）
    S.append(slide(7, T, """
  <div><p class="eyebrow">1981年</p></div>
  <div class="mid">
    <h2 style="font-size:56px">システムは世界の側にあるのか、<br>探究の側にあるのか。</h2>
    <p class="lead" style="margin-top:34px;font-size:28px">世界の一部を切り出してシステムと呼ぶのをやめ、<br><b>探究の過程そのものをシステムとみなす。</b></p>
  </div>
""", "Checkland 1981 Systems Thinking, Systems Practice", logo_h, dark=True))

    # 8 hard / soft
    S.append(slide(8, T, """
  <div><p class="eyebrow">分岐が変えたもの</p><h2>目的が「最適化」から「合意」へ移る</h2></div>
  <div class="mid"><div class="two">
    <div class="card">
      <h3>hard ── 世界の側にある</h3>
      <p><span class="k">問い</span>どうやるか（何をするかは決まっている）</p>
      <p><span class="k">道具</span>模型と計算。World3 のような世界模型</p>
      <p><span class="k">判定</span>定めた目的に対して最適化できたか</p>
    </div>
    <div class="card">
      <h3>soft ── 探究の側にある</h3>
      <p><span class="k">問い</span>何をするか。そこから問う</p>
      <p><span class="k">道具</span>root definition・CATWOE・概念モデル・比較</p>
      <p><span class="k">判定</span>実行可能で望ましい変化に合意できたか</p>
    </div>
  </div></div>
""", "Checkland 2000 SRBS 17(S1) ／ 7段階の詳細は配布資料に", logo_h))

    # 9 図3（★7段階の帯だけを切り出す。上段の hard/soft 対比は前頁のカードと重複する）
    fig3_stages = fig3.replace('viewBox="0 0 960 262"', 'viewBox="0 162 960 100"', 1)
    fig3_stages = fig3_stages.replace('<svg class="fig"', '<svg class="fig figcrop"', 1)
    S.append(slide(9, T, f"""
  <div><p class="eyebrow">FIG.03</p><h2>SSM の7段階 ── 3と4だけが概念の世界</h2></div>
  <div class="figwrap">{fig3_stages}</div>
  <p class="lead" style="font-size:24px">5が「現実と比べる」段階だから、3と4は概念の世界だと読める。一度で終わらず、行動した結果がまた状況になる。</p>
""", "段階名は二次資料による。原典との逐語照合は未実施", logo_h))

    # 10 言えないこと
    S.append(slide(10, T, """
  <div><p class="eyebrow">最後に</p><h2>この地図から言えないこと</h2></div>
  <div class="mid"><ul class="pts">
    <li><b>影響の強さは測っていない。</b>線の本数は根拠の種類であって、影響の大きさではない</li>
    <li><b>26本のうち17本は編纂</b>である。機械的な裏づけを持たない</li>
    <li><b>方法の層は、この地図の外の一次情報に接地している。</b>データベースは根拠の欄を持たない</li>
    <li><b>収録されている範囲</b>であって、未来学の全体像ではない</li>
  </ul></div>
""", "NPO法人ミラツク ／ 詳細と出典は配布資料 futures-genealogy-handout.html", logo_h, dark=True))

    out = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>未来学の系譜 — 投影用スライド</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700;900&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="deck">{''.join(S)}
</div>
<div class="navbar" role="toolbar" aria-label="スライド操作">
  <button onclick="prevSlide()" aria-label="前へ">◀</button>
  <span><span id="pgCur">1</span> / <span id="pgTot">10</span></span>
  <button onclick="nextSlide()" aria-label="次へ">▶</button>
  <button onclick="togglePresent()" title="P">投影</button>
  <button onclick="toggleFull()" title="F">全画面</button>
  <button onclick="window.print()" title="⌘P">印刷</button>
</div>
<script>{NAV_JS}</script>
</body>
</html>
"""
    OUT.write_text(out, encoding="utf-8")
    print(f"書き出しました: {OUT.name} ({OUT.stat().st_size:,} bytes / {T} 枚)")


if __name__ == "__main__":
    main()

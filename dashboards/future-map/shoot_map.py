#!/usr/bin/env python3
"""ブラウザで組み上がる地図を、そのまま1枚の画像にする。

対象は JavaScript が DOM を組み立てる地図なので、HTML を静的に切り出しても中身が無い。
実際に描画させてから撮る。撮る前にやることが3つある。

  1. 相対パス（ロゴ等）が壊れないよう <base> を差す
  2. 画面用の周辺（ヘッダ・説明・操作・引き出し・検索）を隠す
  3. 地図側が持っている fit() を呼んで、全体が入る倍率にする

★fit() はページ自身の関数を使う。こちらで倍率を計算し直すと、
  地図の座標系の取り決め（CW/CH と bbox の関係）を二重に持つことになる。
"""
import subprocess
import sys
import urllib.request
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/125 Safari/537.36"

INJECT = """
<style>
  /* 画面用の周辺を隠す。地図そのものと凡例だけ残す */
  .top, .hint, .frame, .ctl, .foot, #drawer, #scrim, #srch, #srchres,
  #minib, #miniv, .zoomctl, .diff, .howto { display:none !important; }
  html, body { background:#FFFFFF !important; margin:0 !important; padding:0 !important;
               overflow:hidden !important; }
    /* ★器を内側に取る。fit() は器の clientWidth/Height から倍率を出すので、
     器を小さくすれば倍率が下がり、外周に白が残る。ページの計算を触らずに余白を作れる。 */
  .scroll { position:fixed !important; top:56px !important; right:64px !important;
            bottom:64px !important; left:56px !important; width:auto !important;
            height:auto !important; overflow:hidden !important; }
  /* 凡例は残すが、地図に重ならないよう左下へ寄せる */
  #legend, .keyrow { position:fixed !important; left:16px !important; bottom:12px !important;
                     right:auto !important; top:auto !important; z-index:9 !important;
                     background:rgba(255,255,255,.92) !important; }
</style>
<script>
  (function(){
    function ready(){
      // ★fit() だけだと端が切れる。ノードの外に伸びるラベルが bbox に入らないため。
      //   ページ自身の倍率計算を使ったうえで、少しだけ引く。
      try {
        if (typeof fitZ === 'function' && typeof apply === 'function') {
          apply(fitZ() * 0.86);
          if (typeof center === 'function' && typeof bbox === 'function') center(bbox());
        } else if (typeof fit === 'function') { fit(); }
      } catch(e) {}
      document.title = 'SHOT-READY';
    }
    // 地図の組み立てが終わってから fit する。boot は非同期のことがあるので余裕を取る
    if (document.readyState === 'complete') setTimeout(ready, 2500);
    else window.addEventListener('load', function(){ setTimeout(ready, 2500); });
    // 描画後に再度合わせる（遅れて増える要素があるため）
    setTimeout(function(){ try {
      if (typeof fitZ === 'function' && typeof apply === 'function') {
        apply(fitZ() * 0.86);
        if (typeof center === 'function' && typeof bbox === 'function') center(bbox());
      }
    } catch(e) {} }, 5000);
  })();
</script>
"""


def main():
    url = sys.argv[1]
    out = Path(sys.argv[2])
    w = int(sys.argv[3]) if len(sys.argv) > 3 else 2400
    h = int(sys.argv[4]) if len(sys.argv) > 4 else 1500

    base = url.rsplit("/", 1)[0] + "/"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")

    if "<base" not in html:
        html = html.replace("<head>", f'<head><base href="{base}">', 1)
    html = html.replace("</body>", INJECT + "</body>", 1)

    tmp = Path("/tmp/_shot_src.html")
    tmp.write_text(html, encoding="utf-8")

    subprocess.run([
        CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
        f"--window-size={w},{h}",
        "--force-device-scale-factor=2",     # 文字を潰さないため2倍で描かせる
        "--virtual-time-budget=20000",       # JS の組み立てを待つ
        f"--screenshot={out}",
        f"file://{tmp}",
    ], capture_output=True)

    if out.exists():
        print(f"{out} ({out.stat().st_size:,} bytes / {w}x{h} @2x)")
    else:
        print("撮影に失敗しました")


if __name__ == "__main__":
    main()

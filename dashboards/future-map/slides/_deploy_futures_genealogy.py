"""未来学の系譜スライドを journal.emerging-future.org/future-map/slides/ へ FTP で配る。

公開URL: https://journal.emerging-future.org/future-map/slides/futures-genealogy.html
配置先:  /journal.emerging-future.org/future-map/slides/futures-genealogy.html

★2026-08-30 の経緯。このスライドは**本番に置かれた HTML だけが実体**で、ローカルにも
  Mac B（到達不可）にもソースが無かった。そこで本番から取得したものを
  future-map/slides/futures-genealogy.html として保存し、以後はこれをソースとする。
  ★したがって、この配布は「本番にあるものを本番へ戻す」ところから始まっている。
  他の場所に新しい版がある可能性を否定できないので、配る前に必ず本番を取得して
  差分を見ること（--check で取得だけ行う）。
"""
import subprocess
import sys
import hashlib
import re
import urllib.request
from ftplib import FTP, error_perm
from pathlib import Path

HOST = "ftp2.gmoserver.jp"
USER = "sd0177751@gmoserver.jp"
LOCAL = Path(__file__).with_name("futures-genealogy.html")
REMOTE_DIR = "/journal.emerging-future.org/future-map/slides"
REMOTE_FILE = f"{REMOTE_DIR}/futures-genealogy.html"
PUBLIC_URL = "https://journal.emerging-future.org/future-map/slides/futures-genealogy.html"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/125 Safari/537.36"


def get_password() -> str:
    r = subprocess.run(
        ["security", "find-generic-password", "-s", "onamae-ftp", "-w"],
        capture_output=True, text=True, check=True,
    )
    return r.stdout.strip()


def strip_injected(html: bytes) -> bytes:
    """★Cloudflare が挿し込む計測スクリプトを取り除く。

    これを残したまま比べると、内容が同一でも毎回「差分あり」になる（実測 359 bytes）。
    挿し込みは配信側で行われ、リクエストによって付いたり付かなかったりする。
    """
    return re.sub(
        rb'<script[^>]*cloudflareinsights\.com[^>]*>.*?</script>\s*', b"", html, flags=re.S
    )


def fetch_live() -> bytes | None:
    """本番の現物を取る。素の User-Agent では 403 が返るので付ける。"""
    try:
        req = urllib.request.Request(PUBLIC_URL, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            return strip_injected(r.read())
    except Exception as e:  # noqa: BLE001
        print(f"  本番の取得に失敗: {e}")
        return None


def ensure_dir(ftp: FTP, path: str):
    cur = ""
    for p in [p for p in path.split("/") if p]:
        cur = f"{cur}/{p}"
        try:
            ftp.cwd(cur)
        except error_perm:
            ftp.mkd(cur)


def main():
    if not LOCAL.exists():
        print(f"ERROR: ローカルにソースがありません: {LOCAL}")
        sys.exit(1)

    local_bytes = LOCAL.read_bytes()
    print(f"ローカル: {LOCAL.name} ({len(local_bytes):,} bytes / md5 {hashlib.md5(local_bytes).hexdigest()[:12]})")

    live = fetch_live()
    if live is not None:
        same = hashlib.md5(live).hexdigest() == hashlib.md5(local_bytes).hexdigest()
        print(f"本番:     {len(live):,} bytes / md5 {hashlib.md5(live).hexdigest()[:12]} … {'同一' if same else '★差分あり'}")
        if same:
            print("同一なので配布は不要です。")
            return
    if "--check" in sys.argv:
        print("--check のため配布しません。")
        return

    print(f"配布先: ftp://{HOST}{REMOTE_FILE}")
    ftp = FTP(HOST, timeout=60)
    ftp.login(USER, get_password())
    ftp.set_pasv(True)
    ensure_dir(ftp, REMOTE_DIR)
    with LOCAL.open("rb") as f:
        ftp.storbinary(f"STOR {REMOTE_FILE}", f)
    remote_size = ftp.size(REMOTE_FILE)
    ftp.quit()
    print(f"配布しました。remote {remote_size:,} bytes … {'一致' if remote_size == len(local_bytes) else '★不一致'}")

    after = fetch_live()
    if after is not None:
        ok = hashlib.md5(after).hexdigest() == hashlib.md5(local_bytes).hexdigest()
        print(f"再取得で確認: {'一致' if ok else '★不一致（CDN のキャッシュかもしれません）'}")


if __name__ == "__main__":
    main()

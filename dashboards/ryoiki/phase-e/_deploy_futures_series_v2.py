"""Deploy futures-series-v2 (index + ep001-100 + sitemap) to journal.emerging-future.org via FTP.

Target: https://journal.emerging-future.org/futures-series-v2/
"""
import subprocess
import sys
from ftplib import FTP, error_perm
from pathlib import Path

HOST = "ftp2.gmoserver.jp"
USER = "sd0177751@gmoserver.jp"
LOCAL_DIR = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series-v2")
REMOTE_DIR = "/journal.emerging-future.org/futures-series-v2"

UPLOAD_FILES = ["index.html", "articles.html", "sitemap.xml"] + [f"ep{n:03d}.html" for n in range(1, 101)]


def get_password() -> str:
    r = subprocess.run(
        ["security", "find-generic-password", "-s", "onamae-ftp", "-w"],
        capture_output=True, text=True, check=True,
    )
    return r.stdout.strip()


def ensure_dir(ftp: FTP, path: str):
    parts = [p for p in path.split("/") if p]
    cur = ""
    for p in parts:
        cur = f"{cur}/{p}"
        try:
            ftp.cwd(cur)
        except error_perm:
            ftp.mkd(cur)


def main():
    missing = [f for f in UPLOAD_FILES if not (LOCAL_DIR / f).exists()]
    if missing:
        print(f"ERROR: Missing local files: {missing[:5]}{'...' if len(missing) > 5 else ''}")
        sys.exit(1)

    total = sum((LOCAL_DIR / f).stat().st_size for f in UPLOAD_FILES)
    print(f"Local: {len(UPLOAD_FILES)} files, {total:,} bytes total")
    print(f"Target: ftp://{HOST}{REMOTE_DIR}/")

    print("Connecting...")
    ftp = FTP(HOST, timeout=180)
    ftp.login(USER, get_password())
    ftp.set_pasv(True)
    print(f"Connected as {USER}")

    print(f"Ensuring directory: {REMOTE_DIR}")
    ensure_dir(ftp, REMOTE_DIR)

    ok = 0
    mismatch = []
    for idx, name in enumerate(UPLOAD_FILES, 1):
        local = LOCAL_DIR / name
        remote = f"{REMOTE_DIR}/{name}"
        size = local.stat().st_size
        with local.open("rb") as f:
            ftp.storbinary(f"STOR {remote}", f)
        try:
            rsize = ftp.size(remote)
        except Exception:
            rsize = None
        match = (rsize == size)
        ok += 1 if match else 0
        if not match:
            mismatch.append((name, size, rsize))
        if idx % 20 == 0 or idx == len(UPLOAD_FILES):
            print(f"  [{idx}/{len(UPLOAD_FILES)}] uploaded ({ok} verified)")

    ftp.quit()
    print(f"\nDone. {ok}/{len(UPLOAD_FILES)} files size-matched.")
    if mismatch:
        print(f"Mismatches: {mismatch[:5]}")
    print(f"\nPublic URL: https://journal.emerging-future.org/futures-series-v2/")


if __name__ == "__main__":
    main()

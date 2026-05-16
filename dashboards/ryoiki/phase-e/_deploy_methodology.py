"""Deploy methodology.html to journal.emerging-future.org via FTP.

Target URL: https://journal.emerging-future.org/methodology/
Remote path: /journal.emerging-future.org/methodology/index.html
"""
import subprocess
import sys
from ftplib import FTP, error_perm
from pathlib import Path

HOST = "ftp2.gmoserver.jp"
USER = "sd0177751@gmoserver.jp"
LOCAL = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/methodology.html")
REMOTE_DIR = "/journal.emerging-future.org/methodology"
REMOTE_FILE = f"{REMOTE_DIR}/index.html"


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
    if not LOCAL.exists():
        print(f"ERROR: Local file not found: {LOCAL}")
        sys.exit(1)

    size = LOCAL.stat().st_size
    print(f"Local: {LOCAL.name} ({size:,} bytes)")
    print(f"Target: ftp://{HOST}{REMOTE_FILE}")

    print("Connecting...")
    ftp = FTP(HOST, timeout=60)
    ftp.login(USER, get_password())
    ftp.set_pasv(True)
    print(f"Connected as {USER}")

    print(f"Ensuring directory: {REMOTE_DIR}")
    ensure_dir(ftp, REMOTE_DIR)

    print(f"Uploading {LOCAL.name} -> {REMOTE_FILE}")
    with LOCAL.open("rb") as f:
        ftp.storbinary(f"STOR {REMOTE_FILE}", f)
    print(f"Upload OK ({size:,} bytes)")

    rsize = ftp.size(REMOTE_FILE)
    print(f"Remote size: {rsize:,} bytes ({'MATCH' if rsize == size else 'MISMATCH'})")

    ftp.quit()
    print("\nDone.")
    print(f"\nPublic URL: https://journal.emerging-future.org/methodology/")


if __name__ == "__main__":
    main()

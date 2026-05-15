"""Deploy foodag-2030-2100 report to journal.emerging-future.org/reports/foodag-2030-2100/

Target URLs:
  - https://journal.emerging-future.org/reports/foodag-2030-2100/
  - https://journal.emerging-future.org/reports/foodag-2030-2100/methodology.html

Remote paths:
  - /journal.emerging-future.org/reports/foodag-2030-2100/index.html
  - /journal.emerging-future.org/reports/foodag-2030-2100/methodology.html

Local source (copy then upload):
  - reports/foodag-2030-2100.html -> reports-public/foodag-2030-2100/index.html
  - reports/foodag-2030-2100-methodology.html -> reports-public/foodag-2030-2100/methodology.html
"""
import subprocess
import sys
from ftplib import FTP, error_perm
from pathlib import Path

HOST = "ftp2.gmoserver.jp"
USER = "sd0177751@gmoserver.jp"
LOCAL_DIR = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/reports-public/foodag-2030-2100")
REMOTE_DIR = "/journal.emerging-future.org/reports/foodag-2030-2100"
FILES = ["index.html"]  # methodology.html追加は v3 以降


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
            print(f"  mkdir {cur}")
            ftp.mkd(cur)


def main():
    for filename in FILES:
        local = LOCAL_DIR / filename
        if not local.exists():
            print(f"ERROR: Local file not found: {local}")
            sys.exit(1)
    sizes = {f: (LOCAL_DIR / f).stat().st_size for f in FILES}
    for f, s in sizes.items():
        print(f"Local: {f} ({s:,} bytes)")
    print(f"Target: ftp://{HOST}{REMOTE_DIR}/")

    print("Connecting...")
    ftp = FTP(HOST, timeout=120)
    ftp.login(USER, get_password())
    ftp.set_pasv(True)
    print(f"Connected as {USER}")

    print(f"Ensuring directory: {REMOTE_DIR}")
    ensure_dir(ftp, REMOTE_DIR)

    for filename in FILES:
        local = LOCAL_DIR / filename
        remote = f"{REMOTE_DIR}/{filename}"
        print(f"Uploading {filename} -> {remote}")
        with local.open("rb") as f:
            ftp.storbinary(f"STOR {remote}", f)
        rsize = ftp.size(remote)
        local_size = sizes[filename]
        match = "MATCH" if rsize == local_size else f"MISMATCH (remote={rsize:,} vs local={local_size:,})"
        print(f"  OK: remote {rsize:,} bytes [{match}]")

    ftp.quit()
    print("\nDone.")
    print(f"\nPublic URLs:")
    print(f"  本編: https://journal.emerging-future.org/reports/foodag-2030-2100/")
    print(f"  方法論: https://journal.emerging-future.org/reports/foodag-2030-2100/methodology.html")


if __name__ == "__main__":
    main()

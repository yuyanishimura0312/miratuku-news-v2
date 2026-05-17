"""Deploy index-v24.html as a permanent archive to journal.emerging-future.org/deep-knowledge-foresight/index-v24.html

One-time upload of v24 snapshot so old URL is preserved while index.html holds v25.
"""
import subprocess
from ftplib import FTP
from pathlib import Path

HOST = "ftp2.gmoserver.jp"
USER = "sd0177751@gmoserver.jp"
LOCAL = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/data-driven-foresight/index-v24.html")
REMOTE_FILE = "/journal.emerging-future.org/deep-knowledge-foresight/index-v24.html"


def get_password() -> str:
    r = subprocess.run(
        ["security", "find-generic-password", "-s", "onamae-ftp", "-w"],
        capture_output=True, text=True, check=True,
    )
    return r.stdout.strip()


def main():
    size = LOCAL.stat().st_size
    print(f"Local: {LOCAL.name} ({size:,} bytes)")
    ftp = FTP(HOST, timeout=60)
    ftp.login(USER, get_password())
    ftp.set_pasv(True)
    with LOCAL.open("rb") as f:
        ftp.storbinary(f"STOR {REMOTE_FILE}", f)
    rsize = ftp.size(REMOTE_FILE)
    print(f"Upload {size:,} bytes, Remote {rsize:,} bytes ({'MATCH' if rsize == size else 'MISMATCH'})")
    ftp.quit()
    print(f"Public URL: https://journal.emerging-future.org/deep-knowledge-foresight/index-v24.html")


if __name__ == "__main__":
    main()

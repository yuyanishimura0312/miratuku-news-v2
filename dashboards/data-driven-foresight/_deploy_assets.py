"""Deploy assets/* logos to FTP"""
import subprocess
from ftplib import FTP, error_perm
from pathlib import Path

HOST = "ftp2.gmoserver.jp"
USER = "sd0177751@gmoserver.jp"
LOCAL_DIR = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/data-driven-foresight/assets")
REMOTE_DIR = "/journal.emerging-future.org/deep-knowledge-foresight/assets"


def get_password() -> str:
    r = subprocess.run(["security", "find-generic-password", "-s", "onamae-ftp", "-w"],
                       capture_output=True, text=True, check=True)
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
    ftp = FTP(HOST, timeout=60)
    ftp.login(USER, get_password())
    ftp.set_pasv(True)
    ensure_dir(ftp, REMOTE_DIR)
    for f in sorted(LOCAL_DIR.glob("*")):
        if not f.is_file():
            continue
        remote = f"{REMOTE_DIR}/{f.name}"
        with f.open("rb") as fp:
            ftp.storbinary(f"STOR {remote}", fp)
        rsize = ftp.size(remote)
        print(f"  {f.name}: {f.stat().st_size:,} → {rsize:,} {'OK' if rsize == f.stat().st_size else 'MISMATCH'}")
    ftp.quit()
    print("Done")


if __name__ == "__main__":
    main()

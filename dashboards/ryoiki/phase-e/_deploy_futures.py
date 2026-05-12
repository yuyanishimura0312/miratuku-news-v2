"""Deploy futures-deploy/index.html to journal.emerging-future.org/futures/ via FTP.

Target URL: https://journal.emerging-future.org/futures/
Remote path: /journal.emerging-future.org/futures/index.html
"""
import subprocess
import sys
from ftplib import FTP, error_perm
from pathlib import Path

HOST = "ftp2.gmoserver.jp"
USER = "sd0177751@gmoserver.jp"
LOCAL_DIR = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-deploy")
REMOTE_DIR = "/journal.emerging-future.org/futures"


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


def upload(ftp: FTP, local: Path, remote: str):
    size = local.stat().st_size
    print(f"  ↑ {local.name:<30} ({size:>9,} bytes) → {remote}")
    with local.open("rb") as f:
        ftp.storbinary(f"STOR {remote}", f)
    rsize = ftp.size(remote)
    status = "OK" if rsize == size else f"MISMATCH ({rsize:,})"
    print(f"    {status}")


def main():
    files_to_upload = [
        "index.html",
        # assets — re-uploaded to ensure consistency
        "miratuku-logo-dark.png",
        "miratuku-logo-light.png",
        "miratuku-logo-white.png",
        "miratuku-mark-real.png",
        "miratuku-mark-white.png",
        "seed-motif.svg",
    ]

    # Only upload assets that exist locally
    files = []
    for name in files_to_upload:
        p = LOCAL_DIR / name
        if p.exists():
            files.append(p)
        else:
            print(f"  (skip, not found: {name})")

    if not files:
        print("ERROR: No files to upload.")
        sys.exit(1)

    print(f"Connecting to {HOST}...")
    ftp = FTP(HOST, timeout=60)
    ftp.login(USER, get_password())
    ftp.set_pasv(True)
    print(f"Connected as {USER}")

    print(f"Ensuring directory: {REMOTE_DIR}")
    ensure_dir(ftp, REMOTE_DIR)

    print(f"Uploading {len(files)} file(s):")
    for local in files:
        remote = f"{REMOTE_DIR}/{local.name}"
        upload(ftp, local, remote)

    ftp.quit()
    print("\nDone.")
    print(f"\nPublic URL: https://journal.emerging-future.org/futures/")


if __name__ == "__main__":
    main()

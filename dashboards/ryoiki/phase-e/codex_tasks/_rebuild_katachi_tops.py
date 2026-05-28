"""Rebuild 3 katachi series tops to ミラツク連載トップ正本型.

Targets:
- jigyo-no-katachi: index.html MISSING → create new
- henka-no-katachi: hero+newsletter only → add featured + parts-overview
- itonami-no-katachi: hero+newsletter only → add featured + parts-overview
"""
import subprocess
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TEMPLATE = Path("/Users/nishimura+/projects/research/journal-series-templates/series-top-template.html")

TARGETS = [
    {
        "name": "jigyo-no-katachi",
        "dir": Path("/Users/nishimura+/projects/apps/jigyo-no-katachi"),
        "new_url": "https://journal.emerging-future.org/jigyo/",
        "meta_hint": """
- 連載タイトル: 事業のかたち
- 英タイトル: Jigyo no Katachi — Where Academia Meets Business Decisions
- 副題: 学術が事業の前提に出会うとき
- 全話数: 100
- PART 構造: 5 PART × 18 領域 (kurashi top 同型で PART I〜V を構成)
- 最新話: ep100 (タイトルは ep100.html から取得)
- ep ファイル参照: ./ep{NUM}.html (同階層、ep001-a.html ep001-b.html 等は articles.html 側のみ)
- articles.html リンク: ./articles.html
- 共通 CSS: https://journal.emerging-future.org/shared/miratuku-series.css
- canonical 新 URL: https://journal.emerging-future.org/jigyo/
- ACTION: 既存 index.html は無いので、ミラツク連載トップ正本型で **新規生成**
""",
        "mode": "create",
    },
    {
        "name": "henka-no-katachi",
        "dir": Path("/Users/nishimura+/projects/apps/henka-no-katachi"),
        "new_url": "https://journal.emerging-future.org/henka/",
        "meta_hint": """
- 連載タイトル: 変化のかたち
- 英タイトル: Henka no Katachi — 100 Patterns of Social Change
- 副題: 5 メタ型 × 15 サブ型 × 3 底流のソーシャル・イノベーション論
- 全話数: 100
- PART 構造: 5 メタ型 (場 / 媒介 / 物語 / 支え / 開き) を PART I-V とする
- ep ファイル参照: ./ep{NUM}.html
- articles.html リンク: ./articles.html
- canonical 新 URL: https://journal.emerging-future.org/henka/
- ACTION: 既存 index.html を **ミラツク連載トップ正本型へ拡張** (現状 hero+newsletter のみ、featured + intro + parts-overview を追加)
""",
        "mode": "expand",
    },
    {
        "name": "itonami-no-katachi",
        "dir": Path("/Users/nishimura+/projects/apps/itonami-no-katachi"),
        "new_url": "https://journal.emerging-future.org/itonami/",
        "meta_hint": """
- 連載タイトル: いとなみのかたち
- 英タイトル: Itonami no Katachi — Daily Life Meets Academia
- 副題: 5 領域 × 20 話 (子育て / 食事 / 家事 / 余暇 / 買い物) の 100 話連載
- 全話数: 100
- PART 構造: 5 領域を PART I-V (子育て / 食事 / 家事 / 余暇 / 買い物)
- ep ファイル参照: ./ep{NUM}.html
- articles.html リンク: ./articles.html
- canonical 新 URL: https://journal.emerging-future.org/itonami/
- ACTION: 既存 index.html を **ミラツク連載トップ正本型へ拡張** (featured + intro + parts-overview 追加)
""",
        "mode": "expand",
    },
]


PROMPT_CREATE = """You are a precision editor creating a NEW series top (index.html) in ミラツク連載トップ正本型 canonical format.

CONTEXT:
- Series name: {name}
- New public URL: {new_url}
- Canonical template: {template_path}
- Working directory: {dir}
- Existing articles.html (use for episode metadata): {dir}/articles.html

META HINTS:
{meta_hint}

TARGET (ミラツク連載トップ正本型 = journal-series-template.md §2):
1. <header class="site-header">
2. <section class="hero">           — hero-inner / hero-eyebrow / hero-title / hero-en / hero-tagline / hero-cta
3. <section class="intro">          — 3 paragraphs introducing the series
4. <section class="featured">       — featured-card for the latest episode
5. <section class="parts-overview"> — PART grid (5 parts)
6. <section class="newsletter">     — メルマガ 2-step form
7. <footer class="site-footer">     — 4 columns + disclaimer + bottom

STEPS:
1. Read template at {template_path}.
2. Read existing articles.html in {dir} to extract:
   - PART titles & sub-descriptions
   - Latest episode (ep100) title & sub
3. Create NEW index.html at {dir}/index.html using canonical structure
4. ALL links to episodes: `./ep{{NUM}}.html`
5. canonical URL: {new_url}
6. og:url: {new_url}
7. CSS reference: <link rel="stylesheet" href="https://journal.emerging-future.org/shared/miratuku-series.css">
8. Newsletter form (kurashi pattern):
   - 2-step form (email → consent → submit)
   - Heading "Newsletter — メルマガ"
   - Description "{name} の新話を月 N 回お届けします。"

CONSTRAINTS:
- Do NOT modify ep### or articles.html files.
- Use class names from miratuku-series.css ONLY.
- Inline <style> minimal (variable overrides for accent color only if needed).
- Include skip-link / canonical / og:url / prefers-reduced-motion.

OUTPUT: Write to {dir}/index.html and output: "OK: {name} -> created NEW canonical index.html"
"""

PROMPT_EXPAND = """You are a precision editor expanding an existing series top to ミラツク連載トップ正本型 canonical format.

CONTEXT:
- Series name: {name}
- New public URL: {new_url}
- Canonical template: {template_path}
- Existing index.html (currently has hero + newsletter only): {dir}/index.html
- Working directory: {dir}

META HINTS:
{meta_hint}

CURRENT STATE: hero + newsletter only.
NEEDS: + intro (3 paragraphs) + featured (latest episode card) + parts-overview (5 PART grid).

STEPS:
1. Read existing index.html for current structure / metadata.
2. Read template at {template_path}.
3. Read articles.html in {dir} (or ep001.html / ep100.html) for episode/PART metadata.
4. INSERT these 3 sections into the EXISTING index.html between hero and newsletter:
   - <section class="intro"> with 3 paragraphs (preserve series voice)
   - <section class="featured"> with the latest episode card (link to ./ep100.html)
   - <section class="parts-overview"> with 5 PART grid (link to ./articles.html#part-i etc.)
5. UPDATE canonical to {new_url}
6. UPDATE og:url to {new_url}
7. Preserve existing hero / newsletter / site-header / site-footer

CONSTRAINTS:
- Do NOT modify ep### or articles.html files.
- Use class names from miratuku-series.css ONLY (hero-* / intro-* / featured-* / parts-overview-* / newsletter-*).
- Inline <style> minimal.
- Verify all 6 sections present after edit: site-header / hero / intro / featured / parts-overview / newsletter / site-footer.

OUTPUT: Modify {dir}/index.html in-place and output: "OK: {name} -> expanded to canonical (6 sections)"
"""


def run(target):
    name = target["name"]
    work_dir = target["dir"]
    index = work_dir / "index.html"
    backup = work_dir / "_backup_top" / "index.html"
    backup.parent.mkdir(exist_ok=True)
    if index.exists() and not backup.exists():
        shutil.copy(index, backup)

    if target["mode"] == "create":
        prompt = PROMPT_CREATE.format(
            name=name,
            new_url=target["new_url"],
            template_path=TEMPLATE,
            dir=work_dir,
            meta_hint=target["meta_hint"],
        )
    else:
        prompt = PROMPT_EXPAND.format(
            name=name,
            new_url=target["new_url"],
            template_path=TEMPLATE,
            dir=work_dir,
            meta_hint=target["meta_hint"],
        )

    try:
        result = subprocess.run(
            ["codex", "exec", "--cd", str(work_dir), "--skip-git-repo-check", prompt],
            capture_output=True, text=True, timeout=900,
        )
        new = index.read_text(encoding="utf-8") if index.exists() else ""
        has_hero = 'class="hero-inner"' in new or 'class="hero"' in new
        has_featured = 'class="featured-card"' in new or 'class="featured-inner"' in new
        has_parts = 'class="parts-overview"' in new
        has_newsletter = 'class="newsletter"' in new
        canon_ok = target["new_url"] in new
        all_ok = has_hero and has_featured and has_parts and has_newsletter and canon_ok
        return {
            "name": name,
            "status": "ok" if all_ok else "partial",
            "size": len(new),
            "hero": has_hero, "featured": has_featured, "parts": has_parts, "nl": has_newsletter, "canon": canon_ok,
            "returncode": result.returncode,
            "stdout_tail": (result.stdout or "")[-200:],
        }
    except Exception as e:
        return {"name": name, "status": "error", "exception": str(e)}


def main():
    print("=== Rebuild 3 katachi tops to ミラツク連載トップ正本型 ===")
    results = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        futs = [pool.submit(run, t) for t in TARGETS]
        for fut in as_completed(futs):
            r = fut.result()
            results.append(r)
            print(f"  [{r['name']}] {r['status']}  size={r.get('size', '-')}  hero={r.get('hero')} featured={r.get('featured')} parts={r.get('parts')} nl={r.get('nl')} canon={r.get('canon')}")


if __name__ == "__main__":
    main()

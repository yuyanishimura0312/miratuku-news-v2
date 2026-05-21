"""Rebuild 2 series tops to ミラツク連載トップ正本型 (canonical series top format).

Targets:
- futures-series-v2/index.html (flat ep001-100.html structure)
- toi-no-sairai/index.html (articles/ep001-100.html structure)

Approach:
- Backup existing index.html
- codex reads existing index + template, generates new index.html
- Existing episode-list HTML is moved to articles.html
"""
import subprocess
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

TEMPLATE = Path("/Users/nishimura+/projects/research/journal-series-templates/series-top-template.html")

TARGETS = [
    {
        "name": "futures-series-v2",
        "dir": Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series-v2"),
        "url": "https://journal.emerging-future.org/futures-series-v2/",
        "ep_path_pattern": "ep###.html",
        "meta_hint": """
- 連載タイトル: 未来のかたち
- 英タイトル: Futures (未来のかたち) 全100話
- 副題: 70年先を考えるとは、どういうことか
- 全話数: 100
- PART 構造: 既存 index.html から判定 (PART I-V の 5 部構成)
- 最新話: ep100 (タイトルは ep100.html から取得)
- ep ファイル参照: ./ep{NUM}.html (同階層)
- articles.html リンク: ./articles.html
- 共通 CSS: https://journal.emerging-future.org/shared/miratuku-series.css
""",
    },
    {
        "name": "toi-no-sairai",
        "dir": Path("/Users/nishimura+/projects/research/philosophical-questions-era-analysis/toi-no-sairai"),
        "url": "https://journal.emerging-future.org/philosophical-questions/series/",
        "ep_path_pattern": "articles/ep###.html",
        "meta_hint": """
- 連載タイトル: 問いの再来
- 英タイトル: The Return of Questions
- 副題: 哲学概念と歴史的変遷で読む100話 (Season 1)
- 全話数: 100
- PART 構造: 既存 index.html から判定 (PART 数を抽出)
- 最新話: ep100
- ep ファイル参照: articles/ep{NUM}.html
- articles.html リンク: ./articles.html
- 共通 CSS: https://journal.emerging-future.org/shared/miratuku-series.css
""",
    },
]


PROMPT = """You are a precision editor rebuilding the series top (index.html) of a NPO法人ミラツク連載 to the "ミラツク連載トップ正本型" canonical format.

CONTEXT:
- Series name: {name}
- Public URL: {url}
- Canonical format reference (read this fully): {template_path}
- Existing index.html (extract series metadata from this): {existing_index}
- Episode files: {ep_path_pattern} in same directory

TARGET FORMAT (ミラツク連載トップ正本型 = `~/.claude/rules/journal-series-template.md §2`):
```
1. <header class="site-header">
2. <section class="hero">           — hero-inner + hero-eyebrow + hero-title + hero-en + hero-tagline + hero-cta
3. <section class="intro">          — 導入 3 段落
4. <section class="featured">       — featured-card で最新話カード
5. <section class="parts-overview"> — PART 一覧グリッド
6. <section class="newsletter">     — メルマガ 2 ステップフォーム
7. <footer class="site-footer">     — 4 列 + disclaimer + bottom
```

META HINTS for this series:
{meta_hint}

STEPS:
1. Read the canonical template at {template_path} for the structural skeleton.
2. Read the existing index.html (path above) to extract:
   - 連載タイトル / 副題 / 英タイトル
   - 全話数 / PART 構造 (PART 名と説明)
   - 最新話のタイトル / サブタイトル / PART label
   - 連載の導入文 (3 段落分)
3. Read shared CSS class names from https://journal.emerging-future.org/shared/miratuku-series.css.
   Use these class names: hero / hero-inner / hero-eyebrow / hero-title / hero-en / hero-tagline / hero-cta / intro / intro-inner / featured / featured-inner / featured-card / featured-num / featured-num-total / featured-eyebrow / featured-title / featured-sub / featured-cta / parts-overview / parts-overview-inner / parts-overview-label / parts-overview-title / parts-overview-grid / parts-overview-card / parts-overview-card-num / parts-overview-card-title / parts-overview-card-sub / newsletter / newsletter-inner / newsletter-eyebrow / newsletter-title / newsletter-desc / nl-form / nl-step / nl-field / nl-btn / site-header / site-header-inner / site-brand / site-brand-text / site-nav / site-footer / site-footer-inner / site-footer-cols / site-footer-col / site-disclaimer / site-footer-bottom
4. Generate the NEW index.html. Replace {existing_index} entirely.
5. Move the OLD episode-list content (from existing index.html) into a separate articles.html file in the same directory (NEW file).
6. Both files must:
   - reference miratuku-series.css (shared CSS)
   - include the disclaimer block
   - include skip-link / canonical / og:url / prefers-reduced-motion
7. ep file links must match `{ep_path_pattern}` (e.g., ./ep001.html or articles/ep001.html)

OUTPUT: Two files written:
- {existing_index} (new ミラツク連載トップ正本型 index.html)
- {dir}/articles.html (new "全話一覧" list page)

After writing both, output one line:
"OK: {name} -> index.html (NEW canonical) + articles.html (NEW list)"

CONSTRAINTS:
- Do NOT modify any ep###.html file.
- Preserve all existing episode titles / subtitles / part labels exactly.
- Use ミラツク連載トップ正本型 class names ONLY (listed above).
- Do not invent episode count — extract from existing index.
- Do not include inline <style>; rely on miratuku-series.css. Use a small <style> only for series-specific accent color overrides if needed.
"""


def run(target):
    name = target["name"]
    work_dir = target["dir"]
    existing_index = work_dir / "index.html"
    backup = work_dir / "_backup_top" / "index.html"
    backup.parent.mkdir(exist_ok=True)
    if not backup.exists() and existing_index.exists():
        shutil.copy(existing_index, backup)

    prompt = PROMPT.format(
        name=name,
        url=target["url"],
        template_path=TEMPLATE,
        existing_index=existing_index,
        ep_path_pattern=target["ep_path_pattern"],
        meta_hint=target["meta_hint"],
        dir=work_dir,
    )

    try:
        result = subprocess.run(
            ["codex", "exec", "--cd", str(work_dir), "--skip-git-repo-check", prompt],
            capture_output=True, text=True, timeout=1200,
        )
        new_index = existing_index.read_text(encoding="utf-8")
        articles = (work_dir / "articles.html")
        has_canonical = ('class="hero-inner"' in new_index and
                         'class="featured-card"' in new_index and
                         'class="parts-overview"' in new_index)
        has_articles = articles.exists()
        return {
            "name": name,
            "status": "ok" if has_canonical and has_articles else "partial",
            "has_canonical_structure": has_canonical,
            "has_articles_html": has_articles,
            "returncode": result.returncode,
            "stdout_tail": (result.stdout or "")[-300:],
            "stderr_tail": (result.stderr or "")[-200:],
        }
    except Exception as e:
        return {"name": name, "status": "error", "exception": str(e)}


def main():
    print("=== Rebuild 2 series tops to ミラツク連載トップ正本型 ===")
    results = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        futs = [pool.submit(run, t) for t in TARGETS]
        for fut in as_completed(futs):
            r = fut.result()
            results.append(r)
            print(f"  [{r['name']}] {r['status']}  canonical={r.get('has_canonical_structure', '?')} articles={r.get('has_articles_html', '?')}")
            if r.get('stdout_tail'):
                tail = r['stdout_tail'].strip().split('\n')[-3:]
                for line in tail:
                    print(f"    | {line[:120]}")


if __name__ == "__main__":
    main()

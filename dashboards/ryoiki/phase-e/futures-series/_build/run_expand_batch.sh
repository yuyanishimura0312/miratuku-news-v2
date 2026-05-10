#!/bin/bash
set +e
OUT=/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build

codex exec --sandbox workspace-write --skip-git-repo-check - < "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b01_ep004-013.md" > "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b01_log.txt" 2>&1 && touch "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b01_done" &
echo "[launched] expand_b01 ep004-013"
codex exec --sandbox workspace-write --skip-git-repo-check - < "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b02_ep014-023.md" > "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b02_log.txt" 2>&1 && touch "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b02_done" &
echo "[launched] expand_b02 ep014-023"
codex exec --sandbox workspace-write --skip-git-repo-check - < "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b03_ep024-033.md" > "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b03_log.txt" 2>&1 && touch "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b03_done" &
echo "[launched] expand_b03 ep024-033"
codex exec --sandbox workspace-write --skip-git-repo-check - < "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b04_ep034-043.md" > "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b04_log.txt" 2>&1 && touch "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b04_done" &
echo "[launched] expand_b04 ep034-043"
codex exec --sandbox workspace-write --skip-git-repo-check - < "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b05_ep044-053.md" > "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b05_log.txt" 2>&1 && touch "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b05_done" &
echo "[launched] expand_b05 ep044-053"
codex exec --sandbox workspace-write --skip-git-repo-check - < "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b06_ep054-063.md" > "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b06_log.txt" 2>&1 && touch "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b06_done" &
echo "[launched] expand_b06 ep054-063"
codex exec --sandbox workspace-write --skip-git-repo-check - < "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b07_ep064-073.md" > "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b07_log.txt" 2>&1 && touch "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b07_done" &
echo "[launched] expand_b07 ep064-073"
codex exec --sandbox workspace-write --skip-git-repo-check - < "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b08_ep074-083.md" > "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b08_log.txt" 2>&1 && touch "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b08_done" &
echo "[launched] expand_b08 ep074-083"
codex exec --sandbox workspace-write --skip-git-repo-check - < "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b09_ep084-093.md" > "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b09_log.txt" 2>&1 && touch "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b09_done" &
echo "[launched] expand_b09 ep084-093"
codex exec --sandbox workspace-write --skip-git-repo-check - < "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b10_ep094-100.md" > "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b10_log.txt" 2>&1 && touch "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_b10_done" &
echo "[launched] expand_b10 ep094-100"

wait
echo "[ALL EXPAND BATCHES DONE]"
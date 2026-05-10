#!/bin/bash
set +e
OUT=/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build

codex exec --sandbox workspace-write --skip-git-repo-check - < "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_v2_b06a_ep054-056.md" > "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_v2_b06a_log.txt" 2>&1 && touch "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_v2_b06a_done" &
echo "[launched] expand_v2_b06a ep054-056"

wait
echo "[ALL EXPAND BATCHES DONE]"
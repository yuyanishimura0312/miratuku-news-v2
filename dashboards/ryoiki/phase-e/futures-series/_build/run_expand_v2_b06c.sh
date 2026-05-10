#!/bin/bash
set +e
OUT=/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build

codex exec --sandbox workspace-write --skip-git-repo-check - < "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_v2_b06c_ep061-063.md" > "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_v2_b06c_log.txt" 2>&1 && touch "/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build/expand_v2_b06c_done" &
echo "[launched] expand_v2_b06c ep061-063"

wait
echo "[ALL EXPAND BATCHES DONE]"
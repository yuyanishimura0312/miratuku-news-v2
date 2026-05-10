#!/bin/bash
set +e
cd /Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build
# 各バッチを10並列で実行
ls short_b*_ep*.md | sed 's/_ep.*//' | sort -u > /tmp/short_batch_ids.txt
while read bid; do
  prompt=$(ls "${bid}_ep"*.md | head -1)
  echo "[launch] $bid -> $prompt"
  codex exec --sandbox workspace-write --skip-git-repo-check - < "$prompt" > "${bid}_log.txt" 2>&1 && touch "${bid}_done" &
  # 並列度制御: アクティブジョブ10未満まで
  while [ $(jobs -r | wc -l) -ge 10 ]; do sleep 2; done
done < /tmp/short_batch_ids.txt
wait
echo "[ALL_SHORT_DONE]"
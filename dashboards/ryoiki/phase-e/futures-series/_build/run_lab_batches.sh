#!/bin/bash
set +e
cd /Users/nishimura+/projects/apps/miratuku-news-v2/dashboards/ryoiki/phase-e/futures-series/_build

ls lab_b*_ep*.md | sed 's/_ep.*//' | sort -u > /tmp/lab_batch_ids.txt
while read bid; do
  prompt=$(ls "${bid}_ep"*.md | head -1)
  echo "[launch] $bid"
  codex exec --sandbox workspace-write --skip-git-repo-check - < "$prompt" > "${bid}_log.txt" 2>&1 && touch "${bid}_done" &
  while [ $(jobs -r | wc -l) -ge 10 ]; do sleep 2; done
done < /tmp/lab_batch_ids.txt
wait
echo "[ALL_LAB_DONE]"
#!/usr/bin/env python3
"""各話に LAB（自然科学・工学）セクションを追加するためのCodexバッチを生成する。"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "_build"
DRAFTS = ROOT / "_drafts"
EPISODES = BUILD / "episodes.json"

PER_BATCH = 4  # 4話/Codex
EXCLUDE = {1, 4}  # ep001（既存公開）, ep004（LAB追加済み）

LAB_BRIEF = """\
# Codex 執筆ブリーフ — LAB セクション追加

連載「未来のかたち」の各話には、人文知（哲学・人類学・文学・神話・伝統知）を本文に織り込んだうえで、DEEPER（人文知の学術系譜）と SIGNAL（直近の現実世界の動き）の追記欄がある。今回はそこに新たに **LAB（科学の知から）** を加える。各話の本文テーマを踏まえ、対応する **自然科学・工学** の研究者・概念・年代を 400-600字で書く。

## 必須条件
- **字数: 400-600字**（1段落 or 短い2段落、合計）
- **文体**: 「〜である」調、主語「我々」（連載と統一）
- **領域**: 神経科学／認知科学／環境心理学／生態学／地球科学／医療工学／建築工学／情報科学／通信工学／AI・ロボティクス／システム工学／統計物理 などから、本文テーマに対応するものを選ぶ
- **必ず**: 研究者名 + 論文/書籍名 + 年代（西暦）の組を **最低3組** 入れる
- **平らな日本語で、具体的に**: 暮らしの言葉に翻訳しつつ自然科学・工学の系譜を示す

## 出力形式
各話を `=== EPNNN ===` で区切る。LAB 本文のみ書く（frontmatter なし、見出しなし）。

```
=== EP004 ===
場所の重さは、神経科学の言葉でも裏付けられつつある。ジョン・オキーフは1971年、海馬に特定の地点で発火する「場所細胞」を発見し、メイ＝ブリットとエドヴァルト・モーザーは2005年、内嗅皮質に空間を幾何学的に符号化する「格子細胞」を見出した。三人は2014年にノーベル生理学・医学賞を受けている。エレノア・マグワイアの『PNAS』2000年論文は、ロンドンの道を覚え続けたタクシー運転手の海馬後部が物理的に大きくなることを示した。場所を歩き覚えるという経験は、脳の構造そのものを書き換えている。

建築と通信の側でも、場所は具体性を取り戻している。ロジャー・ウルリッヒの『Science』1984年論文は、病院の窓から木が見えるだけで術後の回復が早まることを実証し、エドワード・O・ウィルソン『Biophilia』（1984）以来のバイオフィリック・デザインへとつながった。MIT Senseable City Labのカルロ・ラッティはセンサーデータから場所の使われ方を可視化し、IPFSやティム・バーナーズ＝リーのSolidは、データを再び土地と関係に結び直す試みを始めている。場所は哲学だけでなく、神経・建築・通信のレイヤーで同時に語られはじめている。

=== EP005 ===
（次の話）
...
```

## 厳守事項
- 各話 400-600字（少なすぎ・多すぎ不可）
- 思考過程・解説は出力しない、本文のみ
- Web検索を絶対に使わない（内部知識で書く）
- 各 `=== EPNNN ===` で必ず区切る
"""


def get_body(draft_path: Path) -> str:
    """BODY セクションを抽出する。"""
    text = draft_path.read_text(encoding="utf-8")
    m = re.search(r"# BODY\n(.*?)\n# DEEPER", text, re.DOTALL)
    return m.group(1).strip() if m else ""


def main():
    episodes = json.loads(EPISODES.read_text(encoding="utf-8"))

    targets = []
    for ep in episodes:
        n = ep["num"]
        if n in EXCLUDE:
            continue
        draft = DRAFTS / f"ep{n:03d}.md"
        if not draft.exists():
            continue
        # 既にLABがあれば除外
        if "# LAB" in draft.read_text(encoding="utf-8"):
            continue
        targets.append(ep)

    print(f"Targets: {len(targets)}")

    batches = [targets[i : i + PER_BATCH] for i in range(0, len(targets), PER_BATCH)]

    for bi, batch in enumerate(batches, 1):
        first_n = batch[0]["num"]
        last_n = batch[-1]["num"]
        prompt_path = BUILD / f"lab_b{bi:03d}_ep{first_n:03d}-{last_n:03d}.md"

        ep_blocks = []
        for ep in batch:
            n = ep["num"]
            body = get_body(DRAFTS / f"ep{n:03d}.md")
            humanities = ep.get("humanities", "")
            academic = ep.get("academic_field", "")
            ep_blocks.append(
                f"### 第{n}話「{ep['title']}」\n"
                f"- 人文知: {humanities}\n"
                f"- 学術領域: {academic}\n"
                f"- 本文（BODY）:\n```\n{body}\n```\n"
            )

        prompt = (
            LAB_BRIEF
            + "\n\n## 今回担当: "
            + f"第{first_n}話〜第{last_n}話 ({len(batch)}話)\n\n"
            + "\n".join(ep_blocks)
            + "\n\n## 出力指示\n"
            + f"上記{len(batch)}話すべてのLABセクションを書いてください。各話 `=== EPNNN ===` マーカーで区切ること。"
        )
        prompt_path.write_text(prompt, encoding="utf-8")

    # ランナースクリプト（10並列）
    runner_lines = ["#!/bin/bash", "set +e", f"cd {BUILD}", ""]
    runner_lines.append("ls lab_b*_ep*.md | sed 's/_ep.*//' | sort -u > /tmp/lab_batch_ids.txt")
    runner_lines.append("while read bid; do")
    runner_lines.append('  prompt=$(ls "${bid}_ep"*.md | head -1)')
    runner_lines.append('  echo "[launch] $bid"')
    runner_lines.append('  codex exec --sandbox workspace-write --skip-git-repo-check - < "$prompt" > "${bid}_log.txt" 2>&1 && touch "${bid}_done" &')
    runner_lines.append('  while [ $(jobs -r | wc -l) -ge 10 ]; do sleep 2; done')
    runner_lines.append("done < /tmp/lab_batch_ids.txt")
    runner_lines.append("wait")
    runner_lines.append('echo "[ALL_LAB_DONE]"')

    runner = BUILD / "run_lab_batches.sh"
    runner.write_text("\n".join(runner_lines), encoding="utf-8")
    runner.chmod(0o755)
    print(f"Runner: {runner}")
    print(f"Batches: {len(batches)} (per_batch={PER_BATCH})")


if __name__ == "__main__":
    main()

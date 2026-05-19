# Codex 大規模並列タスク ─ futures-series-v2 スタイル統一

## 目的

`futures-series-v2` の 100 話を `journal-essay-style.md` (ep007 正本型) に準拠させる残作業を、Codex 50-100 並列で実行する。

## 前提

- ms.css (miratuku-series.css) 共通参照は **完了済** (2026-05-19 Step 1b)
- disclaimer ブロックは **完了済** (Step 1)
- ep-actions / Hero lead 加筆 / KEY REFERENCE / SIGNAL / ep-hero-en の content-requiring 修正が残作業

## タスクグループ

### Group A: ep-hero-en 英文タイトル生成 (99 episodes)

ep001 のみ `<p class="ep-hero-en">The Future Is Not Predicted, It Is Drawn</p>` を持つ。残 99 話に同等の英文タイトルを 1 codex × 1 episode で生成・挿入する。

**Codex タスク仕様**:
- Input: `ep{NNN}.html`
- 抽出: `<h1 class="ep-hero-title">` (日本語) + `<h2 class="ep-hero-subtitle">` (補足)
- 生成: 1 文の英文タイトル
  - 句読点なし
  - Title Case
  - 8-15 単語
  - 隣接話と重複しないユニーク表現
- 挿入: `<p class="ep-hero-subtitle">` 直後に `<p class="ep-hero-en">{english}</p>` を追加
- 出力: 上書き保存

**並列度**: 99 codex 並列 (batch 10 × 10 wave 推奨)

### Group B: Hero lead 加筆 (100 episodes)

全話 lead が 145-172 字。規定 200-320 字へ拡張。

**Codex タスク仕様**:
- 既存 lead を維持しつつ 50-80 字加筆
- 「身体経験 → なぜそうなるかへの助走」構造を強化
- ep-hero-lead 内のみ修正

**並列度**: 100 codex (batch 10)

### Group C: SIGNAL list 形式変換 (100 episodes)

現状の自由形式 → `signal-list > signal-item > signal-num + signal-text` 構造化。

**Codex タスク仕様**:
- 既存 SIGNAL 内容を 3-4 項目に整理
- 各項目に `<strong>` で数値強調
- 書誌略記 (著者, 年, 誌名, 巻号: ページ) を末尾に追加

**並列度**: 100 codex (batch 10)

### Group D: KEY REFERENCE 完全形改訂 (100 episodes・最大コスト)

全話 3 件 / DOI ゼロ → 5-8 件 / DOI 必須 / top-tier journal ≥4 件。

**Codex タスク仕様** (Research Precision Protocol 厳守):
- Semantic Scholar / OpenAlex で DOI を検証してから記入
- 既存3件は維持 + 2-5 件追加
- 各件: `<li><strong>Author (year). "Title." Journal Vol(Issue): pages.</strong><span class="ref-doi">DOI: 10.xxxx ／ 日本語解説</span></li>`

**並列度**: 100 codex (batch 5・DOI lookup を含むため少なめ)

## 全体タイムライン

| Group | 並列数 | バッチ | 推定時間 |
|---|---|---|---|
| A: 英文タイトル | 99 | 10 × 10 wave | 30-45分 |
| B: Hero lead | 100 | 10 × 10 wave | 45-60分 |
| C: SIGNAL | 100 | 10 × 10 wave | 60-90分 |
| D: KEY REFERENCE | 100 | 5 × 20 wave | 3-4時間 |

合計: A+B+C+D = **約 5-7 時間** (50-100 codex 並列継続稼働時)

## 実行手順

```bash
# パイロット (Group A, 3 episodes)
python3 _orchestrate_codex_pilot.py

# 検証後、フルラン
python3 _orchestrate_codex_full.py --group A
python3 _orchestrate_codex_full.py --group B
python3 _orchestrate_codex_full.py --group C
python3 _orchestrate_codex_full.py --group D
```

## ガードレール

- 各 codex は **存在検証** を必須 (`~/.codex/AGENTS.md` Chapter 1 準拠)
- DOI は Semantic Scholar / OpenAlex 照合
- 出力レビュー: 各バッチ完了後にサンプル目視
- 失敗時の自動 retry (max 2 回)
- 各 episode の `_backup_codex/` にオリジナル退避

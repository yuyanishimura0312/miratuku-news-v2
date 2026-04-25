#!/usr/bin/env python3
"""
Bottom-up extraction of system thinking patterns from Great Figures DB.
No predefined archetypes — discovers patterns from data.
"""
import json
import os
import re
import math
import html as html_mod
from collections import Counter, defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "gf_consolidated.json"
OUTPUT_HTML = PROJECT_ROOT / "dashboards" / "gf.html"
OUTPUT_JSON = PROJECT_ROOT / "data" / "gf_system_patterns.json"

# Known archetypes for reference (not for forcing classification)
KNOWN_ARCHETYPES = {
    "成長の限界": "Limits to Growth",
    "負担の転嫁": "Shifting the Burden",
    "共有地の悲劇": "Tragedy of the Commons",
    "成功が成功を呼ぶ": "Success to the Successful",
    "うまくいかない修正": "Fixes that Fail",
    "エスカレーション": "Escalation",
    "目標の低下": "Eroding Goals",
    "成長と投資不足": "Growth and Underinvestment",
    "依存と中毒": "Addiction",
    "予期せぬ敵対者": "Accidental Adversaries",
}


# ============================================================
# Phase 1: Load & normalize
# ============================================================
def load_data():
    with open(DATA_PATH) as f:
        data = json.load(f)

    structures = []
    for s in data.get("structures", []):
        # Normalize two schemas
        rec = {
            "person": s.get("person_name_en") or s.get("figure_name_en", ""),
            "event": s.get("event_title_en") or s.get("reform_name_en", ""),
            "situation": s.get("situation_ja", ""),
            "options": s.get("options_ja", ""),
            "chosen": s.get("chosen_action_ja") or s.get("selected_option", ""),
            "reasoning": s.get("reasoning_ja", ""),
            "counterfactual": s.get("counterfactual_ja", ""),
            "constraints": s.get("constraints_ja", ""),
            "period": s.get("period", ""),
            "region": s.get("region", ""),
        }
        rec["all_text"] = " ".join([
            rec["situation"], rec["reasoning"],
            rec["counterfactual"], rec["constraints"]
        ])
        structures.append(rec)

    return {
        "structures": structures,
        "links": data.get("links", []),
        "concepts": data.get("concepts", []),
        "events": data.get("events", []),
    }


# ============================================================
# Phase 2: Bottom-up mechanism vocabulary extraction
# ============================================================

# Causal markers in Japanese
CAUSAL_MARKERS = [
    "ため", "により", "ことで", "結果", "帰結", "によって",
    "すればするほど", "につれて", "に伴い", "を生む", "を招く",
    "が促す", "が阻む", "を強化", "を弱体化", "と相まって",
    "の悪循環", "の好循環", "がもたらす", "に転じる", "を加速",
]

# Structural/systemic vocabulary markers
STRUCTURAL_MARKERS = [
    "構造", "メカニズム", "システム", "循環", "ループ",
    "フィードバック", "帰還", "均衡", "不均衡", "安定",
    "不安定", "閾値", "臨界", "転換", "変革", "崩壊",
    "蓄積", "侵食", "強化", "弱体", "依存", "自律",
    "集中", "分散", "統合", "分裂", "収斂", "発散",
]


def extract_mechanism_phrases(text, window=15):
    """Extract phrases around causal markers."""
    phrases = []
    for marker in CAUSAL_MARKERS:
        idx = 0
        while True:
            pos = text.find(marker, idx)
            if pos == -1:
                break
            start = max(0, pos - window)
            end = min(len(text), pos + len(marker) + window)
            phrase = text[start:end].strip()
            phrases.append(phrase)
            idx = pos + 1
    return phrases


def extract_ngrams(text, n_range=(2, 4)):
    """Extract character n-grams, filtering for meaningful structural/causal ones."""
    clean = re.sub(r'[。、．，！？\s\n\r「」『』（）()【】・：；\-—―…0-9０-９a-zA-Zａ-ｚＡ-Ｚ]', '', text)
    ngrams = Counter()

    # Stop-grams: common but meaningless fragments
    stop = {
        "する", "した", "して", "され", "から", "まで", "こと", "もの", "ない",
        "ある", "いる", "いた", "った", "って", "ての", "との", "での", "への",
        "によ", "にお", "おい", "おけ", "られ", "れた", "れる", "ける",
        "てい", "ている", "として", "という", "において", "における",
        "しか", "また", "さら", "ただ", "ただし", "しかし", "そして",
        "この", "その", "あの", "どの", "これ", "それ", "あれ",
        "的な", "的に", "性が", "性を", "性の", "能性", "可能", "可能性",
        "であ", "であり", "であった", "であっ", "であれ",
        "った場", "た場合", "場合",
        "が必", "が必要", "必要", "0年", "00年", "いう",
        "なけ", "なければ", "なく", "なっ", "なった", "なり",
    }

    for n in range(n_range[0], n_range[1] + 1):
        for i in range(len(clean) - n + 1):
            gram = clean[i:i+n]
            if gram in stop:
                continue
            # Must contain at least one kanji
            if not re.search(r'[\u4e00-\u9fff]', gram):
                continue
            # Must not be purely hiragana + 1 kanji particle pattern
            if n == 2 and re.match(r'^[\u3040-\u309f][\u4e00-\u9fff]$', gram):
                continue
            ngrams[gram] += 1
    return ngrams


def build_mechanism_vocabulary(structures):
    """Build vocabulary of mechanism words from all structures."""
    global_ngrams = Counter()
    causal_context_ngrams = Counter()

    for s in structures:
        text = s["all_text"]
        # Global n-grams
        ng = extract_ngrams(text)
        global_ngrams.update(ng)

        # N-grams near causal markers (higher weight)
        for phrase in extract_mechanism_phrases(text):
            cng = extract_ngrams(phrase)
            causal_context_ngrams.update(cng)

    # Score: causal context frequency * log(global frequency)
    # Penalize terms that appear everywhere (low specificity)
    mechanism_vocab = {}
    total_structures = len(structures)
    for gram, causal_freq in causal_context_ngrams.items():
        global_freq = global_ngrams.get(gram, 0)
        if global_freq >= 5 and causal_freq >= 3:
            # Document frequency: in how many structures does this appear?
            doc_freq = sum(1 for s in structures if gram in s["all_text"])
            # Penalize terms that appear in >70% of documents (too generic)
            if doc_freq > total_structures * 0.7:
                continue
            # IDF-like weight: rarer terms get higher scores
            idf = math.log(1 + total_structures / (1 + doc_freq))
            score = causal_freq * idf
            mechanism_vocab[gram] = {
                "score": round(score, 1),
                "causal_freq": causal_freq,
                "global_freq": global_freq,
                "doc_freq": doc_freq,
            }

    # Sort by score and take top 80
    sorted_vocab = sorted(mechanism_vocab.items(), key=lambda x: -x[1]["score"])[:80]
    return dict(sorted_vocab)


# ============================================================
# Phase 3: Build feature vectors & cluster
# ============================================================
def build_feature_vectors(structures, vocab):
    """Build binary feature vector per structure based on mechanism vocab."""
    vocab_list = list(vocab.keys())
    vectors = []
    for s in structures:
        text = s["all_text"]
        vec = [1 if term in text else 0 for term in vocab_list]
        vectors.append(vec)
    return vectors, vocab_list


def jaccard_similarity(v1, v2):
    """Jaccard similarity between two binary vectors."""
    intersection = sum(a & b for a, b in zip(v1, v2))
    union = sum(a | b for a, b in zip(v1, v2))
    return intersection / union if union > 0 else 0


def hierarchical_cluster(vectors, threshold=0.25):
    """Simple agglomerative clustering with Jaccard similarity."""
    n = len(vectors)
    # Each item starts as its own cluster
    clusters = {i: [i] for i in range(n)}
    active = set(range(n))

    # Precompute similarity matrix (upper triangle)
    sim_cache = {}
    for i in range(n):
        for j in range(i + 1, n):
            sim_cache[(i, j)] = jaccard_similarity(vectors[i], vectors[j])

    def cluster_sim(c1, c2):
        """Average linkage."""
        total = 0
        count = 0
        for i in clusters[c1]:
            for j in clusters[c2]:
                key = (min(i, j), max(i, j))
                total += sim_cache.get(key, 0)
                count += 1
        return total / count if count > 0 else 0

    while len(active) > 1:
        # Find most similar pair
        best_sim = -1
        best_pair = None
        active_list = sorted(active)
        for idx_a in range(len(active_list)):
            for idx_b in range(idx_a + 1, len(active_list)):
                a, b = active_list[idx_a], active_list[idx_b]
                sim = cluster_sim(a, b)
                if sim > best_sim:
                    best_sim = sim
                    best_pair = (a, b)

        if best_sim < threshold:
            break

        # Merge
        a, b = best_pair
        clusters[a] = clusters[a] + clusters[b]
        del clusters[b]
        active.remove(b)

    return {k: v for k, v in clusters.items() if len(v) >= 2}


# ============================================================
# Phase 4: Characterize clusters as system patterns
# ============================================================
def characterize_pattern(cluster_indices, structures, vocab_list, vectors):
    """Describe a cluster's common mechanism."""
    # Find most common vocab terms in this cluster
    term_counts = Counter()
    for idx in cluster_indices:
        for t_idx, present in enumerate(vectors[idx]):
            if present:
                term_counts[vocab_list[t_idx]] += 1

    n = len(cluster_indices)
    # Terms present in >40% of cluster members
    common_terms = [(term, cnt) for term, cnt in term_counts.most_common(20)
                    if cnt >= max(2, n * 0.3)]

    # Feedback direction analysis
    reinforcing_kw = ["拡大", "成長", "強化", "加速", "好循環", "増幅", "自己強化", "蓄積"]
    balancing_kw = ["抵抗", "制約", "限界", "均衡", "衰退", "縮小", "崩壊", "制限"]

    r_score = 0
    b_score = 0
    for idx in cluster_indices:
        text = structures[idx]["all_text"]
        r_score += sum(1 for kw in reinforcing_kw if kw in text)
        b_score += sum(1 for kw in balancing_kw if kw in text)

    if r_score > b_score * 1.5:
        feedback_type = "強化ループ優位"
    elif b_score > r_score * 1.5:
        feedback_type = "均衡ループ優位"
    else:
        feedback_type = "複合フィードバック"

    # Intervention depth (Meadows-inspired, bottom-up)
    shallow_kw = ["量", "数値", "増減", "調整", "配分"]
    structural_kw = ["構造", "制度", "ルール", "法", "組織"]
    paradigm_kw = ["価値観", "世界観", "パラダイム", "哲学", "信念", "思想", "理念"]

    depth_scores = {"パラメータ調整": 0, "構造変更": 0, "パラダイム転換": 0}
    for idx in cluster_indices:
        text = structures[idx].get("chosen", "") + " " + structures[idx].get("reasoning", "")
        depth_scores["パラメータ調整"] += sum(1 for kw in shallow_kw if kw in text)
        depth_scores["構造変更"] += sum(1 for kw in structural_kw if kw in text)
        depth_scores["パラダイム転換"] += sum(1 for kw in paradigm_kw if kw in text)
    primary_depth = max(depth_scores, key=depth_scores.get)

    # Match against known archetypes
    known_match = None
    cluster_text = " ".join(structures[idx]["all_text"] for idx in cluster_indices)
    for ja_name in KNOWN_ARCHETYPES:
        # Check if archetype-related terms appear
        if ja_name[:3] in cluster_text or ja_name[:4] in cluster_text:
            known_match = f"{ja_name} ({KNOWN_ARCHETYPES[ja_name]})"
            break

    # Auto-generate pattern name from top terms
    name_terms = [t[0] for t in common_terms[:3]]
    auto_name = "・".join(name_terms) + "の構造" if name_terms else "未分類パターン"

    return {
        "name": auto_name,
        "common_terms": common_terms,
        "feedback_type": feedback_type,
        "primary_depth": primary_depth,
        "depth_scores": depth_scores,
        "known_match": known_match,
        "size": n,
        "r_score": r_score,
        "b_score": b_score,
    }


# ============================================================
# Phase 5: Era mapping
# ============================================================
def build_era_map(events):
    """Map person_name_en -> era based on earliest event_year."""
    person_years = defaultdict(list)
    for e in events:
        name = e.get("person_name_en", "")
        year = e.get("event_year")
        if name and year is not None:
            person_years[name].append(year)

    era_map = {}
    for name, years in person_years.items():
        y = min(years)
        if y < -500:
            era_map[name] = "古代"
        elif y < 500:
            era_map[name] = "古典"
        elif y < 1500:
            era_map[name] = "中世"
        elif y < 1800:
            era_map[name] = "近世"
        elif y < 1950:
            era_map[name] = "近代"
        else:
            era_map[name] = "現代"
    return era_map


# ============================================================
# Phase 6: Concept network analysis
# ============================================================
def analyze_concept_network(links, concepts):
    """Analyze concept co-occurrence and link patterns."""
    concept_links = Counter()
    concept_types = defaultdict(Counter)
    concept_relevance = defaultdict(list)

    for l in links:
        cname = l.get("concept_name_en", "")
        if cname:
            concept_links[cname] += 1
            concept_types[cname][l.get("link_type", "unknown")] += 1
            rs = l.get("relevance_score")
            if rs:
                concept_relevance[cname].append(rs)

    # Build category map
    cat_map = {}
    for c in concepts:
        cat_map[c.get("name_en", "")] = c.get("category", "unknown")
        cat_map[c.get("name_ja", "")] = c.get("category", "unknown")

    # Person-concept co-occurrence
    person_concepts = defaultdict(set)
    for l in links:
        person = l.get("person_name_en", "")
        concept = l.get("concept_name_en", "")
        if person and concept:
            person_concepts[person].add(concept)

    # Concept pair co-occurrence
    pair_counts = Counter()
    for person, cset in person_concepts.items():
        clist = sorted(cset)
        for i in range(len(clist)):
            for j in range(i + 1, len(clist)):
                pair_counts[(clist[i], clist[j])] += 1

    # Category co-occurrence
    cat_cooccur = Counter()
    for person, cset in person_concepts.items():
        cats = set()
        for c in cset:
            cat = cat_map.get(c, "unknown")
            cats.add(cat)
        catlist = sorted(cats)
        for i in range(len(catlist)):
            for j in range(i + 1, len(catlist)):
                cat_cooccur[(catlist[i], catlist[j])] += 1

    top_concepts = []
    for cname, cnt in concept_links.most_common(20):
        avg_rel = sum(concept_relevance[cname]) / len(concept_relevance[cname]) if concept_relevance[cname] else 0
        cat = cat_map.get(cname, "unknown")
        top_concepts.append({
            "name": cname,
            "category": cat,
            "link_count": cnt,
            "avg_relevance": round(avg_rel, 1),
            "primary_link_type": concept_types[cname].most_common(1)[0][0] if concept_types[cname] else "",
        })

    return {
        "top_concepts": top_concepts,
        "top_pairs": pair_counts.most_common(15),
        "cat_cooccurrence": cat_cooccur.most_common(20),
    }


# ============================================================
# HTML Generation
# ============================================================
def h(text):
    if text is None:
        return ""
    return html_mod.escape(str(text))


CSS = """
:root {
  --bg: #FFFFFF; --card: #FFFFFF; --text: #121212; --text-secondary: #555555;
  --text-muted: #6B6B6B; --border: #D9D9D9; --border-light: #EEEEEE;
  --surface: #F7F7F5; --accent-warm: #CC1400; --accent-muted: rgba(204,20,0,0.06);
  --font: "Noto Sans JP", sans-serif; --font-serif: "Noto Serif JP", serif;
}
[data-theme="dark"] {
  --bg: #121212; --card: #1A1A1A; --text: #E0E0E0; --text-secondary: #AAAAAA;
  --text-muted: #8A8A8A; --border: #333333; --border-light: #2A2A2A;
  --surface: #1A1A1A; --accent-warm: #FF4444; --accent-muted: rgba(255,68,68,0.1);
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font); color: var(--text); background: var(--bg); line-height: 1.7; max-width: 1000px; margin: 0 auto; padding: 24px 20px 60px; }
.back { display: inline-block; margin-bottom: 20px; font-size: 0.82rem; color: var(--text-secondary); text-decoration: none; }
.back:hover { color: var(--text); }
h1 { font-family: var(--font-serif); font-size: 1.5rem; font-weight: 700; margin-bottom: 4px; }
.db-id { font-family: monospace; font-size: 0.72rem; font-weight: 700; color: var(--accent-warm); background: var(--accent-muted); padding: 2px 8px; margin-right: 8px; }
.subtitle { font-size: 0.84rem; color: var(--text-secondary); margin-bottom: 12px; line-height: 1.7; }
.desc { font-size: 0.84rem; color: var(--text); margin-bottom: 24px; line-height: 1.8; }
.overview { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 10px; margin-bottom: 28px; }
.overview-card { background: var(--surface); border: 1px solid var(--border-light); padding: 14px; text-align: center; }
.overview-value { font-family: var(--font-serif); font-size: 1.4rem; font-weight: 700; }
.overview-label { font-size: 0.7rem; color: var(--text-muted); margin-top: 2px; }
h2 { font-family: var(--font-serif); font-size: 1.2rem; font-weight: 700; margin: 36px 0 16px; padding-bottom: 8px; border-bottom: 2px solid var(--border); }
h3 { font-family: var(--font-serif); font-size: 1rem; font-weight: 700; margin: 24px 0 12px; }
.pattern-card { border: 1px solid var(--border); margin-bottom: 16px; }
.pattern-header { padding: 14px 18px; background: var(--surface); border-bottom: 1px solid var(--border-light); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; }
.pattern-name { font-family: var(--font-serif); font-size: 1rem; font-weight: 700; }
.pattern-badges { display: flex; gap: 6px; flex-wrap: wrap; }
.badge { font-size: 0.68rem; padding: 2px 8px; font-weight: 600; }
.badge-new { background: var(--accent-muted); color: var(--accent-warm); }
.badge-known { background: #e8f5e9; color: #2e7d32; }
[data-theme="dark"] .badge-known { background: #1b3a1b; color: #66bb6a; }
.badge-feedback { background: #e3f2fd; color: #1565c0; }
[data-theme="dark"] .badge-feedback { background: #0d2137; color: #64b5f6; }
.badge-depth { background: #fff3e0; color: #e65100; }
[data-theme="dark"] .badge-depth { background: #3e2200; color: #ffb74d; }
.pattern-body { padding: 14px 18px; }
.pattern-terms { font-size: 0.78rem; color: var(--text-secondary); margin-bottom: 12px; }
.pattern-terms span { display: inline-block; background: var(--surface); border: 1px solid var(--border-light); padding: 1px 6px; margin: 2px 2px; font-family: monospace; font-size: 0.74rem; }
.example-card { border-left: 3px solid var(--accent-warm); padding: 10px 14px; margin-bottom: 10px; background: var(--surface); }
.example-title { font-size: 0.82rem; font-weight: 600; margin-bottom: 4px; }
.example-text { font-size: 0.78rem; color: var(--text-secondary); line-height: 1.7; }
.example-meta { font-size: 0.7rem; color: var(--text-muted); margin-top: 4px; }
.bar-row { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; font-size: 0.78rem; }
.bar-label { min-width: 120px; text-align: right; color: var(--text-secondary); }
.bar-track { flex: 1; height: 20px; background: var(--surface); border: 1px solid var(--border-light); }
.bar-fill { height: 100%; background: var(--accent-warm); opacity: 0.7; }
.bar-value { min-width: 40px; font-family: monospace; color: var(--text-muted); }
.vocab-grid { display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 20px; }
.vocab-item { font-size: 0.76rem; padding: 3px 8px; background: var(--surface); border: 1px solid var(--border-light); }
.vocab-item .freq { font-family: monospace; color: var(--accent-warm); margin-left: 4px; font-size: 0.68rem; }
.concept-table { width: 100%; border-collapse: collapse; font-size: 0.78rem; }
.concept-table th { background: var(--surface); padding: 8px 10px; text-align: left; font-weight: 600; border-bottom: 1px solid var(--border); }
.concept-table td { padding: 8px 10px; border-bottom: 1px solid var(--border-light); }
.concept-table tr:hover td { background: var(--surface); }
.era-table { width: 100%; border-collapse: collapse; font-size: 0.76rem; margin-top: 8px; }
.era-table th, .era-table td { padding: 6px 8px; border: 1px solid var(--border-light); text-align: center; }
.era-table th { background: var(--surface); font-weight: 600; }
.era-table td.has { background: var(--accent-muted); font-weight: 700; }
.note { font-size: 0.78rem; color: var(--text-muted); line-height: 1.7; margin: 8px 0; }
.theme-toggle { position: fixed; top: 16px; right: 16px; background: var(--surface); border: 1px solid var(--border); padding: 6px 10px; cursor: pointer; font-size: 1rem; z-index: 10; }
"""


def generate_html(patterns, vocab, structures, era_map, concept_net, feedback_stats):
    """Generate the full dashboard HTML."""

    # Overview
    n_patterns = len(patterns)
    n_new = sum(1 for p in patterns if not p["char"]["known_match"])
    n_structures = len(structures)

    overview = "".join([
        f'<div class="overview-card"><div class="overview-value">{n_structures}</div><div class="overview-label">構造分析</div></div>',
        f'<div class="overview-card"><div class="overview-value">{n_patterns}</div><div class="overview-label">発見パターン</div></div>',
        f'<div class="overview-card"><div class="overview-value">{n_new}</div><div class="overview-label">新規発見</div></div>',
        f'<div class="overview-card"><div class="overview-value">{len(vocab)}</div><div class="overview-label">メカニズム語彙</div></div>',
    ])

    # Section 1: Discovered patterns
    patterns_html = ""
    for i, p in enumerate(patterns):
        char = p["char"]
        # Badges
        badges = ""
        if char["known_match"]:
            badges += f'<span class="badge badge-known">既知: {h(char["known_match"])}</span>'
        else:
            badges += '<span class="badge badge-new">新規発見</span>'
        badges += f'<span class="badge badge-feedback">{h(char["feedback_type"])}</span>'
        badges += f'<span class="badge badge-depth">{h(char["primary_depth"])}</span>'

        # Common terms
        terms_html = "".join(f'<span>{h(t[0])} ({t[1]})</span>' for t in char["common_terms"][:10])

        # Examples
        examples_html = ""
        for idx in p["indices"][:3]:
            s = structures[idx]
            era = era_map.get(s["person"], "不明")
            # Extract key sentence from reasoning
            reasoning = s["reasoning"]
            if reasoning:
                sentences = [sent.strip() for sent in reasoning.split("。") if len(sent.strip()) > 15]
                key_sentence = sentences[0] + "。" if sentences else reasoning[:200]
            else:
                key_sentence = s["situation"][:200]

            examples_html += f'''<div class="example-card">
<div class="example-title">{h(s["person"])} — {h(s["event"])}</div>
<div class="example-text">{h(key_sentence[:250])}</div>
<div class="example-meta">{h(era)}</div>
</div>'''

        patterns_html += f'''<div class="pattern-card">
<div class="pattern-header">
<div class="pattern-name">パターン{i+1}: {h(char["name"])}</div>
<div class="pattern-badges">{badges}</div>
</div>
<div class="pattern-body">
<div class="pattern-terms">共通メカニズム語彙: {terms_html}</div>
<div style="font-size:0.78rem;color:var(--text-muted);margin-bottom:10px">該当: {char["size"]}件 | 強化スコア: {char["r_score"]} / 均衡スコア: {char["b_score"]}</div>
{examples_html}
</div>
</div>'''

    # Section 2: Mechanism vocabulary
    vocab_html = '<div class="vocab-grid">'
    sorted_vocab = sorted(vocab.items(), key=lambda x: -x[1]["score"])[:50]
    for term, info in sorted_vocab:
        vocab_html += f'<div class="vocab-item">{h(term)}<span class="freq">{info["causal_freq"]}</span></div>'
    vocab_html += '</div>'

    # Section 3: Feedback analysis
    fb_html = ""
    for fb_type, count in sorted(feedback_stats.items(), key=lambda x: -x[1]):
        max_count = max(feedback_stats.values())
        pct = int(count / max_count * 100) if max_count > 0 else 0
        fb_html += f'''<div class="bar-row">
<div class="bar-label">{h(fb_type)}</div>
<div class="bar-track"><div class="bar-fill" style="width:{pct}%"></div></div>
<div class="bar-value">{count}</div>
</div>'''

    # Section 4: Depth analysis
    depth_counts = Counter()
    for p in patterns:
        depth_counts[p["char"]["primary_depth"]] += p["char"]["size"]
    depth_html = ""
    max_d = max(depth_counts.values()) if depth_counts else 1
    for depth_name in ["パラメータ調整", "構造変更", "パラダイム転換"]:
        cnt = depth_counts.get(depth_name, 0)
        pct = int(cnt / max_d * 100)
        depth_html += f'''<div class="bar-row">
<div class="bar-label">{h(depth_name)}</div>
<div class="bar-track"><div class="bar-fill" style="width:{pct}%"></div></div>
<div class="bar-value">{cnt}</div>
</div>'''

    # Section 5: Era cross-tabulation
    eras = ["古代", "古典", "中世", "近世", "近代", "現代"]
    era_pattern_matrix = defaultdict(lambda: defaultdict(int))
    for p in patterns:
        pname = p["char"]["name"]
        for idx in p["indices"]:
            era = era_map.get(structures[idx]["person"], "不明")
            if era in eras:
                era_pattern_matrix[pname][era] += 1

    era_table = '<table class="era-table"><thead><tr><th>パターン</th>'
    for era in eras:
        era_table += f'<th>{era}</th>'
    era_table += '<th>時代数</th></tr></thead><tbody>'
    for p in patterns:
        pname = p["char"]["name"]
        row = era_pattern_matrix[pname]
        era_count = sum(1 for e in eras if row[e] > 0)
        era_table += f'<tr><td style="text-align:left;font-size:0.74rem">{h(pname[:20])}</td>'
        for era in eras:
            cnt = row[era]
            cls = ' class="has"' if cnt > 0 else ''
            era_table += f'<td{cls}>{cnt if cnt > 0 else ""}</td>'
        era_table += f'<td><strong>{era_count}</strong></td></tr>'
    era_table += '</tbody></table>'

    # Section 6: Concept network
    concept_html = '<table class="concept-table"><thead><tr><th>概念</th><th>カテゴリ</th><th>リンク数</th><th>平均関連度</th><th>主リンク種</th></tr></thead><tbody>'
    for c in concept_net["top_concepts"]:
        concept_html += f'<tr><td>{h(c["name"])}</td><td>{h(c["category"])}</td><td>{c["link_count"]}</td><td>{c["avg_relevance"]}</td><td>{h(c["primary_link_type"])}</td></tr>'
    concept_html += '</tbody></table>'

    # Concept pairs
    pairs_html = ""
    if concept_net["top_pairs"]:
        pairs_html = '<h3>概念ペア共起（同一人物に紐付く概念ペア）</h3><table class="concept-table"><thead><tr><th>概念A</th><th>概念B</th><th>共起数</th></tr></thead><tbody>'
        for (a, b), cnt in concept_net["top_pairs"][:10]:
            pairs_html += f'<tr><td>{h(a)}</td><td>{h(b)}</td><td>{cnt}</td></tr>'
        pairs_html += '</tbody></table>'

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>歴史構造DB ― システム思考分析 | Insight News</title>
<link rel="icon" href="https://esse-sense.com/favicon.ico">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Noto+Serif+JP:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<button class="theme-toggle" onclick="document.documentElement.setAttribute('data-theme',document.documentElement.getAttribute('data-theme')==='dark'?'':'dark')">&#9789;</button>
<a class="back" href="app.html#section-databases">&larr; データベース一覧に戻る</a>
<h1><span class="db-id">GF</span>歴史構造DB ― システム思考分析</h1>
<p class="subtitle">176の歴史的意思決定からボトムアップにシステム構造パターンを発見する</p>
<p class="desc">歴史上の重要な意思決定176件のテキスト（状況・推論・反実仮想・制約）から、因果関係マーカー周辺の語彙を抽出し、メカニズムの類似性でクラスタリングしました。既知のシステムアーキタイプとの照合も行いますが、データから自然に浮かび上がるパターンを重視しています。</p>
<div class="overview">{overview}</div>

<h2>1. 発見されたシステムパターン</h2>
<p class="note">メカニズム語彙の共起パターンからクラスタリングで発見。各パターンに「既知アーキタイプとの対応」または「新規発見」を付与。</p>
{patterns_html}

<h2>2. メカニズム語彙マップ</h2>
<p class="note">因果関係マーカー（「〜ため」「〜により」「〜を生む」等）の周辺に頻出する構造的語彙。数値は因果文脈での出現回数。</p>
{vocab_html}

<h2>3. フィードバック構造の分布</h2>
<p class="note">各パターンのフィードバックループ方向性。「強化ループ優位」は自己増幅する構造、「均衡ループ優位」は安定/抑制に向かう構造。</p>
{fb_html}

<h2>4. 介入の深度分析</h2>
<p class="note">歴史上の意思決定を、Donella Meadowsのレバレッジポイント理論を参照枠として3段階に分類。</p>
{depth_html}

<h2>5. 時代横断パターンマップ</h2>
<p class="note">各パターンがどの時代に出現するか。4時代以上にまたがるパターンは「普遍的構造」の候補。</p>
{era_table}

<h2>6. 概念ネットワーク</h2>
<p class="note">1,053のリンクから、歴史的事例と最も結びつきの強い経営概念TOP20。</p>
{concept_html}
{pairs_html}

</body>
</html>"""


# ============================================================
# Main
# ============================================================
def main():
    print("Loading data...")
    data = load_data()
    structures = data["structures"]
    print(f"  {len(structures)} structures loaded")

    print("Phase 1: Extracting mechanism vocabulary...")
    vocab = build_mechanism_vocabulary(structures)
    print(f"  {len(vocab)} mechanism terms discovered")

    print("Phase 2: Building feature vectors & clustering...")
    vectors, vocab_list = build_feature_vectors(structures, vocab)
    clusters = hierarchical_cluster(vectors, threshold=0.25)
    print(f"  {len(clusters)} clusters found (threshold=0.25)")

    # If too few clusters, lower threshold
    if len(clusters) < 5:
        clusters = hierarchical_cluster(vectors, threshold=0.20)
        print(f"  Retry with 0.20: {len(clusters)} clusters")

    print("Phase 3: Characterizing patterns...")
    patterns = []
    for cid, indices in sorted(clusters.items(), key=lambda x: -len(x[1])):
        char = characterize_pattern(indices, structures, vocab_list, vectors)
        patterns.append({"indices": indices, "char": char})
    # Sort by size
    patterns.sort(key=lambda x: -x["char"]["size"])
    # Limit to top 12
    patterns = patterns[:12]
    print(f"  Top {len(patterns)} patterns characterized")

    print("Phase 4: Building era map...")
    era_map = build_era_map(data["events"])
    print(f"  {len(era_map)} persons mapped to eras")

    print("Phase 5: Analyzing concept network...")
    concept_net = analyze_concept_network(data["links"], data["concepts"])
    print(f"  Top concepts: {len(concept_net['top_concepts'])}")

    # Feedback stats
    feedback_stats = Counter()
    for p in patterns:
        feedback_stats[p["char"]["feedback_type"]] += p["char"]["size"]

    print("Phase 6: Generating HTML...")
    html = generate_html(patterns, vocab, structures, era_map, concept_net, feedback_stats)
    OUTPUT_HTML.write_text(html, encoding="utf-8")
    print(f"  Dashboard: {OUTPUT_HTML}")

    # Save patterns JSON
    json_output = {
        "patterns": [
            {
                "name": p["char"]["name"],
                "size": p["char"]["size"],
                "feedback_type": p["char"]["feedback_type"],
                "primary_depth": p["char"]["primary_depth"],
                "known_match": p["char"]["known_match"],
                "common_terms": p["char"]["common_terms"][:10],
                "examples": [
                    {"person": structures[idx]["person"], "event": structures[idx]["event"]}
                    for idx in p["indices"][:5]
                ],
            }
            for p in patterns
        ],
        "vocab_size": len(vocab),
        "top_vocab": [(k, v["score"]) for k, v in sorted(vocab.items(), key=lambda x: -x[1]["score"])[:30]],
    }
    with open(OUTPUT_JSON, "w") as f:
        json.dump(json_output, f, ensure_ascii=False, indent=2)
    print(f"  Patterns JSON: {OUTPUT_JSON}")

    print("\nDone!")


if __name__ == "__main__":
    main()

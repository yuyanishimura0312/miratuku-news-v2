# LLM Academic Papers Database

## Overview

Comprehensive SQLite database of landmark academic papers on Large Language Models (LLMs), organized into 15 research categories with full citation tracking and genealogical relationships.

**Location**: `/Users/nishimura+/projects/research/miratuku-news-v2/dashboards/data/llm_papers.db`

## Database Contents

### Summary Statistics
- **Total Papers**: 38 landmark papers
- **Categories**: 15 organized research areas
- **Lineage Relationships**: 37 predecessor-successor connections
- **Landmark Papers**: 17 papers marked as foundational
- **Citation Range**: 800–90,000 citations
- **Year Range**: 2013–2023
- **Average Popularity**: 15,526 citations per paper

### 15 Research Categories

1. **Foundations** (基盤)
   - Core architectures: Transformer, attention mechanisms, seq2seq, word2vec
   - Landmark: "Attention Is All You Need" (2017), Word2Vec (2013)

2. **Pre-training** (事前学習)
   - Foundation models: BERT, GPT-2, T5, XLNet
   - Landmark: BERT (2018), GPT-2 (2019)

3. **Scaling Laws** (スケーリング則)
   - Compute scaling relationships: Kaplan laws, Chinchilla, emergent abilities
   - Landmark: Scaling Laws for Neural LMs (2020), Chinchilla (2022)

4. **GPT Series** (GPTシリーズ)
   - OpenAI's progression: GPT-3, InstructGPT, GPT-4
   - Landmark: GPT-3 (2020), InstructGPT (2022), GPT-4 (2023)

5. **Open Models** (オープンモデル)
   - Community-released models: LLaMA, Mistral, DeepSeek
   - Landmark: LLaMA (2023)

6. **Training Methods** (学習手法)
   - Optimization approaches: RLHF, DPO, Constitutional AI
   - Landmark: RLHF/InstructGPT (2022), DPO (2023)

7. **Reasoning** (推論)
   - Multi-step thinking: Chain-of-Thought, Tree of Thoughts, self-consistency
   - Landmark: Chain-of-Thought (2022)

8. **Multimodal** (マルチモーダル)
   - Vision-language models: CLIP, LLaVA, GPT-4V, Gemini
   - Landmark: CLIP (2021)

9. **Long Context** (長文脈)
   - Extended sequence handling: RoPE, Mamba, state space models
   - Landmark: RoFormer/RoPE (2021)

10. **Efficiency** (効率化)
    - Parameter reduction: LoRA, quantization, mixture of experts
    - Landmark: LoRA (2021)

11. **Agents** (エージェント)
    - Interactive systems: ReAct, Toolformer, function calling
    - Landmark: ReAct (2022)

12. **Safety** (安全性)
    - Security and alignment: red teaming, jailbreaking, adversarial testing
    - Landmark: Red Teaming (2022)

13. **Evaluation** (評価)
    - Benchmarks: MMLU, HumanEval, HELM
    - Landmark: MMLU (2020)

14. **RAG** (検索拡張)
    - External knowledge: RAG, RETRO, in-context learning
    - Landmark: RAG (2020)

15. **Future** (将来)
    - Emerging directions: test-time compute, reasoning models, world models
    - Landmark: Reward Model Overoptimization (2023)

## Database Schema

### papers table
```sql
CREATE TABLE papers (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  authors TEXT,
  year INTEGER,
  venue TEXT,
  doi TEXT,
  arxiv_id TEXT,
  semantic_scholar_id TEXT,
  abstract TEXT,
  category TEXT,
  key_contribution TEXT,
  citation_count INTEGER DEFAULT 0,
  relevance_score REAL DEFAULT 0,
  is_landmark INTEGER DEFAULT 0
);
```

### categories table
```sql
CREATE TABLE categories (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  name_ja TEXT,
  description TEXT,
  parent_category_id INTEGER REFERENCES categories(id)
);
```

### lineage table
```sql
CREATE TABLE lineage (
  id INTEGER PRIMARY KEY,
  predecessor_paper_id INTEGER REFERENCES papers(id),
  successor_paper_id INTEGER REFERENCES papers(id),
  relationship TEXT
);
```

### Indexes
- `idx_papers_category`: Fast category lookup
- `idx_papers_year`: Fast temporal queries
- `idx_papers_citation`: Fast citation-based sorting

## Key Lineage Chains

### Foundation → Pre-training → GPT Series
```
Word2Vec (2013)
  → ELMo (2018)
    → Transformer (2017)
      → BERT (2018) / GPT-2 (2019)
        → GPT-3 (2020)
          → InstructGPT (2022)
            → GPT-4 (2023)
```

### Scaling Research
```
Scaling Laws for Neural LMs (2020)
  → Training Compute-Optimal LMs / Chinchilla (2022)
    → Emergent Abilities (2022)
      → Reward Model Overoptimization (2023)
```

### Reasoning Development
```
Chain-of-Thought (2022)
  → Tree of Thoughts (2023)
  → Self-Consistency (2022)
```

### Efficiency Innovations
```
LoRA (2021)
  → QLoRA (2023)
```

### Multimodal Integration
```
CLIP (2021)
  → LLaVA / Visual Instruction Tuning (2023)
```

## Most-Cited Papers (Top 10)

1. Word2Vec (2013) — 90,000 citations
2. Attention Is All You Need (2017) — 85,000 citations
3. BERT (2018) — 75,000 citations
4. Sequence to Sequence Learning (2014) — 65,000 citations
5. Exploring Transfer Learning/T5 (2019) — 32,000 citations
6. GPT-3 (2020) — 30,000 citations
7. GPT-2 (2019) — 30,000 citations
8. CLIP (2021) — 25,000 citations
9. ELMo (2018) — 25,000 citations
10. XLNet (2019) — 18,000 citations

## Using the Database

### Basic Queries

**Find all papers in a category**:
```sql
SELECT title, year, citation_count FROM papers 
WHERE category = 'Reasoning' 
ORDER BY citation_count DESC;
```

**Find landmark papers**:
```sql
SELECT title, category, year FROM papers 
WHERE is_landmark = 1 
ORDER BY category;
```

**Find papers by year**:
```sql
SELECT title, category FROM papers 
WHERE year = 2022 
ORDER BY citation_count DESC;
```

**Find papers by ArXiv ID**:
```sql
SELECT title, category, citation_count FROM papers 
WHERE arxiv_id = '1706.03762';
```

### Advanced Queries

**Find descendants of a paper** (what papers built on this):
```sql
SELECT DISTINCT p2.title, p2.category, p2.year
FROM lineage l
JOIN papers p1 ON l.predecessor_paper_id = p1.id
JOIN papers p2 ON l.successor_paper_id = p2.id
WHERE p1.title LIKE '%Chain-of-Thought%'
ORDER BY p2.year;
```

**Find ancestors of a paper** (what papers led to this):
```sql
SELECT DISTINCT p1.title, p1.category, p1.year
FROM lineage l
JOIN papers p1 ON l.predecessor_paper_id = p1.id
JOIN papers p2 ON l.successor_paper_id = p2.id
WHERE p2.title LIKE '%GPT-4%'
ORDER BY p1.year DESC;
```

**Papers by citation impact per category**:
```sql
SELECT category, 
    COUNT(*) as paper_count,
    AVG(citation_count) as avg_citations,
    MAX(citation_count) as max_citations
FROM papers
GROUP BY category
ORDER BY avg_citations DESC;
```

**Relevance scores within a category**:
```sql
SELECT title, year, relevance_score FROM papers 
WHERE category = 'Training Methods' 
ORDER BY relevance_score DESC;
```

## Companion Files

- **llm_papers_metadata.json**: Machine-readable schema and statistics
- **QUERY_EXAMPLES.md**: Additional SQL examples and patterns

## Data Quality

- **PRAGMA integrity_check**: PASSED
- **Foreign key constraints**: Active on lineage relationships
- **NULL handling**: Normalized citations, abstracts may be summarized
- **Citation counts**: Based on actual academic databases (Semantic Scholar references)

## Updates and Extensions

To add new papers:
```sql
INSERT INTO papers (
  title, authors, year, venue, arxiv_id, abstract,
  category, key_contribution, citation_count, is_landmark
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
```

To add lineage relationships:
```sql
INSERT INTO lineage (
  predecessor_paper_id, successor_paper_id, relationship
) VALUES (?, ?, 'predecessor');
```

## License

This database compiles publicly available academic paper metadata from open sources. Full papers should be accessed through their original venues (arXiv, conference proceedings, etc.).

---

**Created**: 2026-04-29
**Database Version**: 1.0
**Total Size**: ~800 KB
**Format**: SQLite 3

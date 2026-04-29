# AGI Papers Database - Usage Guide

Database Location: `/Users/nishimura+/projects/research/miratuku-news-v2/dashboards/data/agi_papers.db`

## Database Overview

A comprehensive AGI research papers database containing:
- **160 papers** across 12 research approaches
- **43 landmark papers** marking significant milestones
- **14 timeline entries** from 1950-2024
- **Complete citation metrics** and relevance scores
- **72 recent papers** (2020+) covering latest developments

## Schema

### papers table
```sql
- id (INTEGER PRIMARY KEY)
- title TEXT
- authors TEXT
- year INTEGER
- venue TEXT
- doi TEXT
- arxiv_id TEXT
- semantic_scholar_id TEXT
- abstract TEXT
- approach_category TEXT
- key_contribution TEXT
- citation_count INTEGER
- relevance_score REAL
- is_landmark INTEGER
```

### approaches table
- 12 research approach categories
- English and Japanese names
- Description and key insights
- Representative paper references

### timeline table
- Historical AI milestones (1950-2024)
- Description in both English and Japanese
- Significance assessment

## Research Approaches (12 Categories)

1. **Scaling Hypothesis** (スケーリング仮説) - 22 papers
   - Focus on compute/data scaling effects
   - Examples: Language model scaling laws

2. **Meta-Learning** (メタ学習と転移学習) - 22 papers
   - Few-shot learning, transfer learning
   - Foundation models, prompt engineering

3. **Safety & Alignment** (安全性とアライメント) - 21 papers
   - AI alignment, value alignment, reward modeling
   - Interpretability and robustness

4. **Theoretical Foundations** (理論的基礎) - 14 papers
   - Information theory, formal intelligence measures
   - Computational bounds and limits

5. **Embodied Cognition** (具象知見と認知) - 13 papers
   - Robotics, sensorimotor grounding
   - Embodied AI systems

6. **Reinforcement Learning** (強化学習) - 13 papers
   - Policy learning, Q-learning, actor-critic
   - Exploration-exploitation tradeoffs

7. **World Models** (世界モデル) - 11 papers
   - Predictive models, simulation
   - Environment understanding

8. **Brain-Inspired AI** (脳インスパイア型AI) - 10 papers
   - Neuromorphic computing, HTM
   - Brain simulation approaches

9. **Benchmarks & Evaluation** (ベンチマーク評価) - 10 papers
   - AGI evaluation metrics
   - Task benchmarks and assessment

10. **Neuro-Symbolic AI** (ニューロシンボリックAI) - 9 papers
    - Symbol grounding, hybrid approaches
    - Knowledge integration

11. **Multi-Agent Systems** (マルチエージェントシステム) - 8 papers
    - Agent cooperation, emergent behavior
    - Collective intelligence

12. **Cognitive Architectures** (認知アーキテクチャ) - 7 papers
    - SOAR, ACT-R, CLARION
    - Integrated cognitive models

## Key Statistics

- **Citation Range**: 160 - 95,000 citations
- **Average Citations**: 5,648
- **Most Cited**: "Attention Is All You Need" (2017, 95K citations)
- **Recent Coverage**: 45% of papers from 2020+
- **Landmark Density**: 26.9% are marked as landmark papers

## Query Examples

### Find top papers by citation count
```sql
SELECT title, authors, year, citation_count, approach_category
FROM papers
ORDER BY citation_count DESC
LIMIT 10;
```

### Papers by specific approach
```sql
SELECT title, year, citation_count
FROM papers
WHERE approach_category = 'scaling_hypothesis'
ORDER BY citation_count DESC;
```

### Recent landmark papers
```sql
SELECT title, authors, year, citation_count
FROM papers
WHERE is_landmark = 1 AND year >= 2020
ORDER BY year DESC;
```

### Timeline events
```sql
SELECT year, milestone_description_ja, milestone_description
FROM timeline
ORDER BY year;
```

### Citation distribution by approach
```sql
SELECT approach_category, 
       COUNT(*) as paper_count,
       ROUND(AVG(citation_count), 0) as avg_citations,
       MAX(citation_count) as max_citations
FROM papers
GROUP BY approach_category
ORDER BY paper_count DESC;
```

### Papers with abstracts in specific year range
```sql
SELECT title, year, abstract, approach_category
FROM papers
WHERE year BETWEEN 2020 AND 2023
  AND abstract IS NOT NULL
ORDER BY year DESC;
```

### Find landmark papers by approach
```sql
SELECT approach_category, COUNT(*) as landmark_count
FROM papers
WHERE is_landmark = 1
GROUP BY approach_category
ORDER BY landmark_count DESC;
```

### ArXiv paper search
```sql
SELECT title, authors, year, arxiv_id
FROM papers
WHERE arxiv_id IS NOT NULL
ORDER BY year DESC
LIMIT 20;
```

## Access Methods

### Using SQLite CLI
```bash
sqlite3 /Users/nishimura+/projects/research/miratuku-news-v2/dashboards/data/agi_papers.db
```

### Using Python
```python
import sqlite3
conn = sqlite3.connect('/Users/nishimura+/projects/research/miratuku-news-v2/dashboards/data/agi_papers.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM papers WHERE is_landmark = 1")
results = cursor.fetchall()
```

### Using Node.js
```javascript
const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('/Users/nishimura+/projects/research/miratuku-news-v2/dashboards/data/agi_papers.db');
db.all("SELECT * FROM approaches", (err, rows) => {
  console.log(rows);
});
```

## Data Quality

- **Title Coverage**: 100%
- **Author Coverage**: 100%
- **Year Coverage**: 100%
- **ArXiv ID Coverage**: 72.5%
- **Citation Data**: 100% (all papers have citation counts)
- **Category Assignment**: 100%
- **Abstract Coverage**: 30.6%

## Last Updated

- Database built: 2026-04-30
- Papers indexed: 160
- Landmark papers: 43
- Citation data: Current as of indexing

## Related Resources

- Semantic Scholar: https://www.semanticscholar.org/
- ArXiv: https://arxiv.org/
- Research Dashboard: ~/projects/research/research-dashboard/

## Notes for Researchers

1. **Citation counts** represent impact and accessibility in academic discourse
2. **Landmark papers** are manually marked based on historical significance
3. **Approach categories** sometimes overlap; papers can logically belong to multiple categories
4. **Recent papers** (2020+) may have lower citation counts due to recency bias
5. **Abstract field** is partially populated; use venue URLs for full paper access

---

For queries and research, consult the database schema and use appropriate SQL filters.

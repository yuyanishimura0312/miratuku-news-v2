
# LLM Papers Database - Query Helper Examples

## Find papers on a specific topic:
```sql
SELECT title, year, citation_count FROM papers 
WHERE category = 'Reasoning' 
ORDER BY citation_count DESC;
```

## Find paper descendants (what papers built on this):
```sql
SELECT DISTINCT p2.title, p2.category, p2.year
FROM lineage l
JOIN papers p1 ON l.predecessor_paper_id = p1.id
JOIN papers p2 ON l.successor_paper_id = p2.id
WHERE p1.title = 'Chain-of-Thought Prompting Elicits Reasoning in Large Language Models'
ORDER BY p2.year;
```

## Find landmark papers by category:
```sql
SELECT category, title, year FROM papers
WHERE is_landmark = 1
ORDER BY category, year DESC;
```

## Papers with highest relevance in each category:
```sql
SELECT DISTINCT category,
    (SELECT title FROM papers p2 
     WHERE p2.category = p1.category 
     ORDER BY p2.relevance_score DESC LIMIT 1) as top_paper
FROM papers p1
GROUP BY category;
```

## Citation impact by category:
```sql
SELECT category, 
    COUNT(*) as paper_count,
    AVG(citation_count) as avg_citations,
    MAX(citation_count) as max_citations
FROM papers
GROUP BY category
ORDER BY avg_citations DESC;
```

## Full lineage chain reconstruction:
```sql
WITH RECURSIVE lineage_chain AS (
  SELECT id, title, 0 as depth
  FROM papers
  WHERE title = 'Attention Is All You Need'
  
  UNION ALL
  
  SELECT p.id, p.title, lc.depth + 1
  FROM papers p
  JOIN lineage l ON p.id = l.successor_paper_id
  JOIN lineage_chain lc ON l.predecessor_paper_id = lc.id
)
SELECT title FROM lineage_chain ORDER BY depth;
```

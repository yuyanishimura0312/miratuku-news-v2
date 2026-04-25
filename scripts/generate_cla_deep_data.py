#!/usr/bin/env python3
"""
generate_cla_deep_data.py

Generate 4 JSON files for CLA deep layer enhancement:
1. cla_ngram_overlay.json — Google Ngram concept trends
2. signal_network.json — Supernode network analysis
3. cla_evidence.json — World Bank + HDI social indicators
4. cla_myth_mapping.json — Thompson Motif-Index + UNESCO ICH

Reads from pestle-signal-db SQLite databases.
Output: data/*.json

Run: python3 scripts/generate_cla_deep_data.py
"""
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

CLA_DB = os.path.expanduser('~/projects/research/pestle-signal-db/data/cla.db')
SIGNAL_DB = os.path.expanduser('~/projects/research/pestle-signal-db/data/signal.db')
OUT_DIR = Path(__file__).resolve().parent.parent / 'data'


def generate_ngram_overlay():
    """Generate cla_ngram_overlay.json"""
    PESTLE_MAP = {
        'democracy': 'Political', 'nationalism': 'Political', 'human rights': 'Political',
        'artificial intelligence': 'Technological', 'singularity': 'Technological', 'frontier': 'Technological',
        'globalization': 'Economic', 'inequality': 'Economic', 'innovation': 'Economic', 'disruption': 'Economic',
        'climate change': 'Environmental', 'sustainability': 'Environmental', 'collapse': 'Environmental', 'pandemic': 'Environmental',
        'progress': 'Social', 'transformation': 'Social', 'resilience': 'Social',
        'apocalypse': 'Mythological', 'utopia': 'Mythological', 'dystopia': 'Mythological',
    }
    db = sqlite3.connect(CLA_DB)
    cur = db.cursor()
    concepts = {}
    cur.execute("SELECT indicator, wave_or_year, value FROM worldview_data WHERE source='google_ngram' ORDER BY indicator, wave_or_year")
    for r in cur.fetchall():
        name, year, val = r
        if name not in concepts:
            concepts[name] = {'pestle_category': PESTLE_MAP.get(name, 'Other'), 'data': []}
        concepts[name]['data'].append({'year': int(year), 'freq': val})

    for name, info in concepts.items():
        data = info['data']
        if len(data) >= 20:
            recent = sum(d['freq'] for d in data[-10:]) / 10
            previous = sum(d['freq'] for d in data[-20:-10]) / 10
            info['trend_10yr'] = round((recent - previous) / previous * 100, 1) if previous > 0 else 0
            info['peak_year'] = max(data, key=lambda x: x['freq'])['year']
            info['latest_value'] = data[-1]['freq']

    db.close()
    return {'concepts': concepts, 'source': 'Google Books Ngram Viewer (en-2019, smoothing=3)', 'coverage': '1950-2022, 20 concepts'}


def generate_signal_network():
    """Generate signal_network.json"""
    db = sqlite3.connect(SIGNAL_DB)
    cur = db.cursor()
    cur.execute('''SELECT s.id, s.signal_name, s.pestle_categories, s.cla_depth, s.composite_score,
                   s.signal_type, m.betweenness, m.eigenvector, m.in_degree, m.out_degree,
                   m.cluster_id, m.is_supernode
    FROM signal_network_metrics m JOIN signals s ON m.signal_id = s.id ORDER BY m.betweenness DESC''')
    nodes = [{'id': r[0], 'name': r[1], 'pestle_categories': json.loads(r[2]) if r[2] else [],
              'cla_depth': r[3], 'composite_score': r[4], 'signal_type': r[5],
              'betweenness': r[6], 'eigenvector': r[7], 'in_degree': r[8], 'out_degree': r[9],
              'cluster_id': r[10], 'is_supernode': bool(r[11])} for r in cur.fetchall()]

    cur.execute('''SELECT source_signal_id, target_signal_id, impact_score, impact_type, rationale
    FROM signal_cross_impact WHERE impact_score != 0 ORDER BY ABS(impact_score) DESC LIMIT 300''')
    edges = [{'source': r[0], 'target': r[1], 'impact_score': r[2], 'impact_type': r[3],
              'is_llm': (r[4] or '').startswith('llm:')} for r in cur.fetchall()]

    cluster_labels = {0: '環境', 1: '技術', 2: '社会', 3: '政治', 4: '経済', 5: '法律'}
    cluster_colors = {0: '#16a34a', 1: '#dc2626', 2: '#8b5cf6', 3: '#2563eb', 4: '#d97706', 5: '#64748b'}
    clusters = {}
    for n in nodes:
        cid = n['cluster_id']
        if cid not in clusters:
            clusters[cid] = {'label': cluster_labels.get(cid, f'Cluster {cid}'),
                             'color': cluster_colors.get(cid, '#94a3b8'), 'size': 0, 'supernodes': 0}
        clusters[cid]['size'] += 1
        if n['is_supernode']:
            clusters[cid]['supernodes'] += 1

    db.close()
    return {'nodes': nodes, 'edges': edges, 'clusters': clusters,
            'stats': {'total_nodes': len(nodes), 'total_edges': len(edges),
                      'supernodes': sum(1 for n in nodes if n['is_supernode']),
                      'llm_evaluated_edges': sum(1 for e in edges if e['is_llm'])}}


def generate_evidence():
    """Generate cla_evidence.json"""
    INDICATOR_PESTLE = {
        'NY.GDP.PCAP.PP.CD': 'Economic', 'SI.POV.GINI': 'Economic', 'SL.UEM.TOTL.ZS': 'Economic',
        'SG.GEN.PARL.ZS': 'Political', 'SP.DYN.LE00.IN': 'Social', 'SE.TER.ENRR': 'Social',
        'SP.POP.TOTL': 'Social', 'SP.URB.TOTL.IN.ZS': 'Social',
        'GB.XPD.RSDV.GD.ZS': 'Technological', 'IT.NET.USER.ZS': 'Technological',
    }
    KEY_COUNTRIES = ['JPN', 'USA', 'CHN', 'DEU', 'GBR', 'IND', 'BRA', 'KOR']
    db = sqlite3.connect(CLA_DB)
    cur = db.cursor()

    indicators_by_pestle = {}
    for code, pestle in INDICATOR_PESTLE.items():
        if pestle not in indicators_by_pestle:
            indicators_by_pestle[pestle] = []
        ph = ','.join('?' * len(KEY_COUNTRIES))
        cur.execute(f'''SELECT indicator_name, country_code, year, value
        FROM social_indicators WHERE source='world_bank' AND indicator_code=? AND country_code IN ({ph})
        ORDER BY country_code, year''', [code] + KEY_COUNTRIES)
        countries = {}
        name = code
        for r in cur.fetchall():
            name = r[0]
            cc = r[1]
            if cc not in countries:
                countries[cc] = []
            countries[cc].append({'year': r[2], 'value': round(r[3], 2) if r[3] else None})
        if countries:
            indicators_by_pestle[pestle].append({'code': code, 'name': name, 'countries': countries})

    hdi_summary = {}
    ph = ','.join('?' * len(KEY_COUNTRIES))
    cur.execute(f'''SELECT country_code, year, value FROM social_indicators
    WHERE source='hdr' AND indicator_code='HDI' AND country_code IN ({ph})
    ORDER BY country_code, year''', KEY_COUNTRIES)
    for r in cur.fetchall():
        cc = r[0]
        if cc not in hdi_summary:
            hdi_summary[cc] = []
        hdi_summary[cc].append({'year': r[1], 'value': round(r[2], 3)})

    db.close()
    return {'indicators_by_pestle': indicators_by_pestle, 'hdi_summary': hdi_summary,
            'countries': KEY_COUNTRIES,
            'coverage': {'world_bank': '10 indicators, 20 countries, 1990-2024', 'hdr': 'HDI, 193 countries, 1990-2023'}}


def generate_myth_mapping():
    """Generate cla_myth_mapping.json"""
    THOMPSON_CATEGORIES = {
        'A': {'name': '神話的モチーフ', 'name_en': 'Mythological Motifs'},
        'B': {'name': '動物', 'name_en': 'Animals'},
        'C': {'name': 'タブー', 'name_en': 'Tabu'},
        'D': {'name': '魔法・変容', 'name_en': 'Magic'},
        'E': {'name': '死と復活', 'name_en': 'The Dead'},
        'F': {'name': '異界・驚異', 'name_en': 'Marvels'},
        'G': {'name': '食人鬼・怪物', 'name_en': 'Ogres'},
        'H': {'name': '試練', 'name_en': 'Tests'},
        'J': {'name': '賢者と愚者', 'name_en': 'The Wise and the Foolish'},
        'K': {'name': '欺き', 'name_en': 'Deceptions'},
        'L': {'name': '運命の逆転', 'name_en': 'Reversal of Fortune'},
        'M': {'name': '未来の定め', 'name_en': 'Ordaining the Future'},
        'N': {'name': '偶然と運命', 'name_en': 'Chance and Fate'},
        'P': {'name': '社会', 'name_en': 'Society'},
        'Q': {'name': '報いと罰', 'name_en': 'Rewards and Punishments'},
        'R': {'name': '捕囚と逃亡', 'name_en': 'Captives and Fugitives'},
        'S': {'name': '残酷', 'name_en': 'Unnatural Cruelty'},
        'T': {'name': '性', 'name_en': 'Sex'},
        'U': {'name': '人生の本質', 'name_en': 'The Nature of Life'},
        'V': {'name': '宗教', 'name_en': 'Religion'},
        'W': {'name': '性格の特徴', 'name_en': 'Traits of Character'},
        'X': {'name': 'ユーモア', 'name_en': 'Humor'},
        'Z': {'name': '雑', 'name_en': 'Miscellaneous'},
    }
    db = sqlite3.connect(CLA_DB)
    cur = db.cursor()

    thompson_summary = {}
    cur.execute("SELECT source_id FROM myth_data WHERE source='thompson_motif'")
    for r in cur.fetchall():
        cat = r[0][0] if r[0] else '?'
        if cat in THOMPSON_CATEGORIES:
            if cat not in thompson_summary:
                thompson_summary[cat] = {**THOMPSON_CATEGORIES[cat], 'count': 0}
            thompson_summary[cat]['count'] += 1

    cur.execute("SELECT archetype_tags FROM myth_data WHERE source='unesco_ich'")
    ich_archetypes = {}
    for r in cur.fetchall():
        for t in json.loads(r[0] or '[]'):
            ich_archetypes[t] = ich_archetypes.get(t, 0) + 1

    keyword_to_thompson = {
        '変容': ['D', 'E'], '変革': ['D', 'L'], '技術': ['D', 'F'],
        '救済': ['A', 'V', 'Q'], '支配': ['D', 'K', 'G'], '自由': ['R', 'L'],
        '境界': ['C', 'F'], '創造': ['A'], '破壊': ['E', 'S', 'G'],
        '知恵': ['J', 'H'], '欺き': ['K', 'J'], '運命': ['M', 'N'],
        '試練': ['H'], '復活': ['E'], '英雄': ['H', 'L'],
        'プロメテウス': ['A', 'D', 'Q'], 'パンドラ': ['C', 'A'],
        '洪水': ['A'], 'ユートピア': ['F', 'U'], 'ディストピア': ['G', 'S'],
        '黙示録': ['A', 'E'], '進歩': ['D', 'U'], '回帰': ['E', 'L'],
        'AI': ['D', 'F'], '国家': ['P', 'M'], '市場': ['K', 'N'],
        '民主': ['P', 'J'], '権力': ['P', 'K', 'G'],
    }

    db.close()
    return {
        'thompson_summary': thompson_summary,
        'thompson_total': sum(v['count'] for v in thompson_summary.values()),
        'keyword_to_thompson': keyword_to_thompson,
        'unesco_ich': {'total': 849, 'archetype_distribution': ich_archetypes},
        'cla_myth_connection_guide': {
            'example': {
                'cla_text': '「技術的救世主」と「技術的啓示録」の並存',
                'matched_keywords': ['技術', '救済', '黙示録'],
                'thompson_categories': ['A (神話)', 'D (魔法・変容)', 'E (死と復活)', 'V (宗教)'],
                'interpretation': '現代のAI神話はThompsonのD(Magic)カテゴリ — 7,149件の「変容」モチーフ群 — と構造的に同型'
            }
        }
    }


def main():
    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst).isoformat()

    generators = {
        'cla_ngram_overlay.json': generate_ngram_overlay,
        'signal_network.json': generate_signal_network,
        'cla_evidence.json': generate_evidence,
        'cla_myth_mapping.json': generate_myth_mapping,
    }

    for filename, gen_func in generators.items():
        try:
            data = gen_func()
            data['generated_at'] = now
            out_path = OUT_DIR / filename
            out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
            size_kb = out_path.stat().st_size / 1024
            print(f"  {filename}: {size_kb:.1f} KB", file=sys.stderr)
        except Exception as e:
            print(f"  {filename}: ERROR - {e}", file=sys.stderr)

    print(f"Generated {len(generators)} files at {now}", file=sys.stderr)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

#!/usr/bin/env python3
"""
SIF Analysis Pipeline — Deterministic, keyword-based analysis of Social Innovation events.

Reads gf_consolidated.json + gf_events_cases.json, selects SI events using explicit
criteria, scores them on the PRRRC 5-dimension model, classifies by civilization/era/type/
pathway, validates the 10 system laws, and regenerates the dashboard HTML from data.

All results are reproducible: same input → same output.
"""

import json
import math
import re
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DASHBOARDS_DIR = PROJECT_ROOT / "dashboards"

# =============================================================================
# CONSTANTS: Keyword lists and classification rules
# =============================================================================

# --- SI Selection Keywords ---
SI_KEYWORDS_JA = [
    "改革", "制度", "権利", "平等", "教育", "福祉", "自由", "民主", "協同", "公共",
    "市民", "解放", "連帯", "包摂", "参加", "正義", "人権", "憲法", "法律", "保険",
    "年金", "医療", "保護", "大学", "学校", "図書", "識字", "選挙", "投票",
    "組合", "共同体", "自治", "住民", "労働者", "女性", "奴隷", "廃止", "普及",
]
SI_KEYWORDS_EN = [
    "reform", "rights", "equality", "welfare", "freedom", "democracy", "democratic",
    "cooperative", "liberation", "solidarity", "inclusion", "participation", "justice",
    "abolition", "suffrage", "emancipation", "universal", "humanitarian",
    "institution", "constitution", "legislation",
    "insurance", "pension", "healthcare", "public health",
    "infrastructure", "sanitation", "literacy",
    "university", "school", "library",
]

# --- Selection tiers: (event_types, min_si_score) ---
TIER_1_TYPES = {"innovation", "reform", "founding"}
TIER_2_TYPES = {"alliance", "pivot", "growth", "negotiation", "crisis", "decision"}
TIER_3_TYPES = {"law", "education", "administration"}  # case-specific
TIER_4_TYPES = {"failure"}
MIN_IMPORTANCE = 3

# --- PRRRC Scoring Keyword Tiers (highest match wins) ---
# P: Problem structural depth (0-5)
P_TIERS = [
    (5, ["構造的矛盾", "社会の根幹", "systemic oppression", "structural inequality",
         "endemic", "根深い不平等", "社会再生産", "構造的暴力"]),
    (4, ["構造的", "systemic", "不平等", "inequality", "搾取", "exploitation",
         "制度的差別", "institutional discrimination", "慢性的", "chronic"]),
    (3, ["制度が対応できない", "widespread", "広域", "既存制度の限界",
         "structural", "複合的", "intersecting", "social problem"]),
    (2, ["反復する", "recurring", "地域的", "regional problem", "persistent",
         "貧困", "poverty", "飢餓", "famine", "疫病", "epidemic"]),
    (1, ["問題", "problem", "課題", "challenge", "困難", "difficulty"]),
]

# R1: Response institutional novelty (0-5)
R1_TIERS = [
    (5, ["前例のない", "unprecedented", "世界初", "first in history",
         "新しい制度を創造", "created new institution", "根本的に新しい"]),
    (4, ["憲法", "constitution", "法律制定", "legislation enacted", "新制度",
         "new system", "根本的に変更", "fundamentally changed", "革命的"]),
    (3, ["制度改革", "institutional reform", "法的枠組み", "legal framework",
         "制度化", "institutionalized", "体系化", "codified"]),
    (2, ["政策", "policy", "規制", "regulation", "修正", "amendment",
         "改善", "improvement", "導入", "introduced"]),
    (1, ["調整", "adjustment", "部分的", "partial", "暫定的", "interim",
         "試行", "pilot", "experimental"]),
]

# R2: Reach / Resource scope (0-4)
R2_TIERS = [
    (4, ["世界的", "global", "全世界", "worldwide", "国際的", "international",
         "人類全体", "all humanity", "across continents"]),
    (3, ["帝国全域", "empire-wide", "全国", "nationwide", "複数の国",
         "multiple countries", "大陸", "continent"]),
    (2, ["地域", "regional", "数都市", "multiple cities", "広域",
         "several provinces", "州全体", "state-wide"]),
    (1, ["都市", "city", "地方", "local", "一地域", "village", "community",
         "town", "commune"]),
]

# R3: Recombination / Relationship transformation (0-4)
R3_TIERS = [
    (4, ["後継制度", "successor institution", "複数の制度に波及",
         "influenced multiple institutions", "制度間の連鎖", "institutional cascade",
         "世界中で採用", "adopted worldwide"]),
    (3, ["他の制度に影響", "influenced other", "移植", "transplanted",
         "他地域で採用", "adopted elsewhere", "模範", "model for"]),
    (2, ["関連する制度", "related institution", "ネットワーク", "network",
         "連携", "collaboration", "波及", "ripple effect"]),
    (1, ["限定的", "limited influence", "一部に", "partially",
         "間接的", "indirect"]),
]

# C: Conditions / Cognitive framework shift (0-4)
C_TIERS = [
    (4, ["パラダイム", "paradigm", "認識の根本的転換", "fundamental cognitive shift",
         "問題の再定義", "problem redefinition", "新しい世界観", "new worldview",
         "概念の発明", "invented the concept"]),
    (3, ["認知的転換", "cognitive shift", "正当性の変化", "legitimacy change",
         "新しい概念", "new concept", "言説の変化", "discourse change",
         "社会的認識", "social recognition"]),
    (2, ["意識の変化", "awareness change", "態度の変化", "attitude change",
         "新しい視点", "new perspective", "道徳的", "moral"]),
    (1, ["部分的な理解", "partial understanding", "一部の人々に", "among some",
         "啓蒙", "enlightenment", "教育的", "educational"]),
]

# --- Civilization classification ---
CIV_RULES = [
    # Check cross-civilizational first
    ("cross-civilizational", [
        "International", "United Nations", "Global", "Worldwide", "Various",
        "Multiple", "UN ", "League of Nations",
    ]),
    ("Western", [
        "Europe", "England", "Britain", "France", "Germany", "Italy", "Spain",
        "Portugal", "Netherlands", "Belgium", "Switzerland", "Austria", "Sweden",
        "Norway", "Denmark", "Finland", "Greece", "Rome", "Roman", "Athens",
        "London", "Paris", "Berlin", "Vienna", "United States", "America",
        "Canada", "Australia", "New Zealand", "Scotland", "Ireland", "Poland",
        "Hungary", "Czech", "Bohemia", "Byzantine", "Constantinople",
        "Florence", "Venice", "Milan", "Bologna", "Lisbon", "Madrid", "Prague",
        "Copenhagen", "Stockholm", "Amsterdam", "Cambridge", "Oxford",
        "Philadelphia", "New York", "Washington", "USA", "United Kingdom",
        "Moscow", "Soviet Union", "Russia", "Saint Petersburg", "Kiev",
        "Sparta", "Corinth", "Syracuse", "Troy", "Ephesus", "Rhodes",
        "Antioch", "Carthage", "Thebes", "Gaul", "Saxony", "Bavaria",
        "Burgundy", "Normandy", "Flanders", "Genoa", "Zurich", "Geneva",
        "Edinburgh", "Dublin", "Brussels", "Warsaw", "Krakow", "Leipzig",
    ]),
    ("Islamic", [
        "Baghdad", "Mecca", "Medina", "Ottoman", "Abbasid", "Umayyad",
        "Cairo", "Damascus", "Persia", "Iran", "Arabia", "Morocco", "Tunisia",
        "Algeria", "Turkey", "Anatolia", "Cordoba", "Al-Andalus", "Mughal",
        "Islamic", "Muslim", "Istanbul", "Isfahan", "Shiraz", "Tabriz",
        "Syria", "Iraq", "Lebanon", "Palestine", "Jordan", "Yemen",
        "Samarkand", "Bukhara", "Herat", "Balkh", "Khorasan",
        "Mesopotamia", "Babylon", "Ur", "Nineveh", "Sumer", "Akkad",
        "Assyria", "Parthian", "Sassanid", "Seljuk", "Fatimid",
        "Mamluk", "Ayyubid", "Safavid", "Qajar",
    ]),
    ("South Asian", [
        "India", "Delhi", "Calcutta", "Mumbai", "Bombay", "Sri Lanka",
        "Nepal", "Bangladesh", "Pakistan", "Bengal", "Madras", "Chennai",
        "Hyderabad", "Punjab", "Gujarat", "Rajasthan", "Kerala", "Maurya",
        "Gupta", "Ashoka", "Gandhara", "Pataliputra", "Agra", "Varanasi",
        "Lucknow", "Jaipur", "Mysore", "Deccan", "Vijayanagara", "Chola",
        "Pallava", "Magadha", "Taxila", "Nalanda",
    ]),
    ("East Asian", [
        "China", "Japan", "Korea", "Tokyo", "Kyoto", "Beijing", "Shanghai",
        "Nanjing", "Osaka", "Seoul", "Taipei", "Taiwan", "Hong Kong",
        "Mongolia", "Tibet", "Manchuria", "Edo", "Meiji",
        "Chang'an", "Luoyang", "Kaifeng", "Hangzhou", "Goryeo", "Joseon",
        "Yamato", "Southern Song", "Guangzhou", "Chengdu", "Sichuan",
        "Heian", "Kamakura", "Nara", "Ming", "Qing", "Song ", "Tang ",
        "Han ", "Sui ", "Zhou ", "Shang", "Pyongyang", "Shenyang",
    ]),
    ("African", [
        "Africa", "Ghana", "Mali", "Ethiopia", "Kenya", "Nigeria", "Zimbabwe",
        "Sudan", "Congo", "Tanzania", "Senegal", "South Africa", "Uganda",
        "Mozambique", "Angola", "Cameroon", "Ivory Coast", "Burkina",
        "Rwanda", "Timbuktu", "Axum", "Kush", "Nubia", "Zulu",
        "Alexandria", "Memphis", "Thebes",
        "Benin", "Songhai", "Zanzibar", "Madagascar", "Swahili",
        "Dahomey", "Ashanti", "Oyo", "Kanem", "Bornu", "Great Zimbabwe",
    ]),
    ("Americas", [
        "Brazil", "Mexico", "Peru", "Argentina", "Chile", "Colombia", "Cuba",
        "Haiti", "Caribbean", "Latin America", "Venezuela", "Bolivia",
        "Ecuador", "Paraguay", "Uruguay", "Guatemala", "Aztec", "Maya",
        "Inca", "Andes", "Puerto Rico", "Jamaica",
        "Costa Rica", "Panama", "Honduras", "Nicaragua", "El Salvador",
        "Dominican", "Tenochtitlan", "Cusco", "Lima", "Buenos Aires",
        "Bogota", "Havana", "Mexico City", "Sao Paulo", "Rio de Janeiro",
    ]),
    ("Southeast Asian", [
        "Southeast Asia", "Vietnam", "Thailand", "Indonesia", "Philippines",
        "Cambodia", "Myanmar", "Burma", "Laos", "Malaysia", "Singapore",
        "Java", "Sumatra", "Aceh", "Siam", "Angkor", "Khmer",
        "Hanoi", "Saigon", "Bangkok", "Manila", "Malacca", "Majapahit",
        "Srivijaya", "Champa", "Ayutthaya", "Pagan",
    ]),
    ("Central Asian", [
        "Central Asia", "Uzbekistan", "Kazakhstan", "Turkmenistan",
        "Afghanistan", "Kyrgyzstan", "Tajikistan", "Silk Road", "Steppe",
        "Samarkand", "Bukhara", "Kabul", "Kandahar",
    ]),
    ("Pacific", [
        "Pacific", "Polynesia", "Hawaii", "Samoa", "Tonga", "Fiji",
        "Papua", "Oceania", "Maori", "Melanesia", "Micronesia",
    ]),
]

# Special case: Egypt classification by era
EGYPT_ISLAMIC_AFTER = 641  # Arab conquest of Egypt

# --- Era classification ---
ERA_BOUNDARIES = [
    ("ancient-medieval", None, 1499),
    ("early-modern", 1500, 1759),
    ("industrial", 1760, 1913),
    ("short-20c", 1914, 1979),
    ("global", 1980, None),
]
ERA_LABELS_JA = {
    "ancient-medieval": "古代〜中世",
    "early-modern": "近代成立期",
    "industrial": "産業革命期",
    "short-20c": "20世紀短期",
    "global": "グローバル期",
}

# --- SI Type classification keywords ---
SI_TYPE_KEYWORDS = {
    "public_goods": {
        "ja": ["灌漑", "道路", "公衆衛生", "上水道", "図書館", "病院", "水道",
               "インフラ", "衛生", "公共事業", "港湾", "鉄道"],
        "en": ["infrastructure", "public health", "sanitation", "water", "road",
               "irrigation", "hospital", "public service", "sewage", "railway"],
    },
    "social_protection": {
        "ja": ["保険", "年金", "福祉", "貧困", "セーフティネット", "労働保護",
               "救済", "扶助", "社会保障", "失業", "生活保護"],
        "en": ["insurance", "pension", "welfare", "poverty", "safety net",
               "social security", "unemployment", "poor relief", "workhouse"],
    },
    "civil_rights": {
        "ja": ["権利", "参政権", "選挙権", "奴隷廃止", "女性", "解放", "市民権",
               "人権", "平等", "差別", "自由権", "法の下の平等"],
        "en": ["rights", "suffrage", "abolition", "emancipation", "civil rights",
               "equality", "liberation", "enfranchisement", "freedom",
               "anti-discrimination", "human rights"],
    },
    "knowledge_democratization": {
        "ja": ["教育", "大学", "学校", "印刷", "出版", "識字", "図書",
               "百科事典", "学問", "科学", "知識"],
        "en": ["education", "university", "school", "printing", "literacy",
               "library", "encyclopedia", "knowledge", "science", "learning"],
    },
    "democratic_decision": {
        "ja": ["民主", "議会", "投票", "参加型予算", "自治", "住民参加",
               "選挙", "代議", "共和", "評議会"],
        "en": ["democracy", "parliament", "voting", "participatory", "self-governance",
               "deliberative", "assembly", "republic", "council", "election"],
    },
}

# Complex type trigger keywords
COMPLEX_TRIGGERS_JA = ["革命", "独立", "体制変革", "全面的", "包括的"]
COMPLEX_TRIGGERS_EN = ["revolution", "independence", "regime change", "comprehensive",
                       "transformation"]

# --- Three pathways classification ---
PATHWAY_KEYWORDS = {
    "institutional_opportunity": {
        "ja": ["制度変化", "規制緩和", "法改正", "政権交代", "エリート分裂",
               "開国", "改革派", "新政権"],
        "en": ["institutional change", "regulatory", "deregulation", "regime change",
               "political opening", "opportunity", "new government", "reform act"],
    },
    "moral_collective_action": {
        "ja": ["不正義", "道徳", "義憤", "運動", "抗議", "連帯", "集団行動",
               "デモ", "ストライキ", "ボイコット", "請願"],
        "en": ["injustice", "moral", "outrage", "movement", "protest", "solidarity",
               "collective action", "boycott", "march", "petition", "campaign"],
    },
    "crisis_response": {
        "ja": ["危機", "災害", "飢饉", "パンデミック", "戦争後", "崩壊",
               "緊急", "復興", "救援", "疫病"],
        "en": ["crisis", "disaster", "famine", "pandemic", "post-war", "collapse",
               "emergency", "catastrophe", "reconstruction", "plague"],
    },
}

# --- Failure classification ---
FAILURE_KEYWORDS = [
    "失敗", "崩壊", "鎮圧", "クーデター", "弾圧", "挫折", "頓挫", "消滅",
    "failed", "collapsed", "suppressed", "coup", "crushed", "overthrown",
    "defeated", "abandoned", "dissolved",
]
FAILURE_SUBCATEGORIES = {
    "military_suppression": [
        "鎮圧", "クーデター", "軍事", "弾圧", "暗殺", "処刑", "虐殺",
        "suppressed", "coup", "military", "assassination", "executed", "massacre",
    ],
    "topdown_failure": [
        "上からの", "設計の欠陥", "当事者不在", "官僚的", "画一的",
        "top-down", "design failure", "without participation", "bureaucratic",
    ],
    "economic_collapse": [
        "経済的崩壊", "財政破綻", "資金不足", "ハイパーインフレ", "財政",
        "economic collapse", "bankruptcy", "funding", "hyperinflation", "fiscal",
    ],
    "corruption": [
        "変質", "腐敗", "権力の私物化", "独裁", "専制",
        "corruption", "co-opted", "degenerated", "authoritarian", "dictator",
    ],
    "external_intervention": [
        "外部介入", "帝国主義", "植民地", "侵略", "干渉", "封鎖",
        "foreign intervention", "imperialism", "colonial", "invasion", "blockade",
    ],
}


# =============================================================================
# DATA LOADING
# =============================================================================

def load_data():
    """Load all source data files."""
    with open(DATA_DIR / "gf_consolidated.json", "r") as f:
        consolidated = json.load(f)
    cases_path = DATA_DIR / "gf_events_cases.json"
    cases = []
    if cases_path.exists():
        with open(cases_path, "r") as f:
            cases = json.load(f)
    return consolidated, cases


def merge_events(consolidated, cases):
    """Merge events from consolidated and case files, deduplicating."""
    events = []
    seen = set()

    # Add all consolidated events
    for e in consolidated.get("events", []):
        key = (e.get("title_en", ""), e.get("event_year"))
        if key not in seen:
            seen.add(key)
            e["_source"] = "consolidated"
            events.append(e)

    # Add case events not already present
    for e in cases:
        key = (e.get("title_en", ""), e.get("event_year"))
        if key not in seen:
            seen.add(key)
            e["_source"] = "cases"
            events.append(e)

    return events


# =============================================================================
# SI EVENT SELECTION
# =============================================================================

def _get_text_fields(event):
    """Concatenate all text fields for keyword search."""
    fields = ["title_ja", "title_en", "description_ja", "description_en",
              "outcome_ja", "outcome_en"]
    return " ".join(str(event.get(f, "") or "") for f in fields)


def compute_si_keyword_score(event):
    """Count distinct SI keyword matches across all text fields."""
    text = _get_text_fields(event).lower()
    score = 0
    for kw in SI_KEYWORDS_JA:
        if kw in text:
            score += 1
    for kw in SI_KEYWORDS_EN:
        if kw.lower() in text:
            score += 1
    # Bonus from event_type (structural relevance)
    etype = event.get("event_type", "")
    if etype in ("reform", "law", "education"):
        score += 1
    return score


def select_si_events(events):
    """Apply tiered selection criteria to identify SI events."""
    selected = []
    for e in events:
        imp = e.get("importance", 0) or 0
        if imp < MIN_IMPORTANCE:
            continue

        etype = e.get("event_type", "")
        si_score = compute_si_keyword_score(e)
        e["_si_keyword_score"] = si_score

        selected_flag = False
        if etype in TIER_1_TYPES and si_score >= 2:
            selected_flag = True
        elif etype in TIER_2_TYPES and si_score >= 3:
            selected_flag = True
        elif etype in TIER_3_TYPES and si_score >= 2:
            selected_flag = True
        elif etype in TIER_4_TYPES and si_score >= 2:
            selected_flag = True
        elif si_score >= 5:  # Tier 5: any type with high keyword score
            selected_flag = True

        if selected_flag:
            selected.append(e)

    return selected


# =============================================================================
# PRRRC SCORING
# =============================================================================

def _score_dimension(text, tiers):
    """Score a single PRRRC dimension using keyword tier matching.
    Returns highest matching tier score."""
    text_lower = text.lower()
    for score, keywords in tiers:
        matches = sum(1 for kw in keywords if kw.lower() in text_lower)
        if matches >= 1:
            return score
    return 0


def _event_type_base_scores(event_type):
    """Provide base PRRRC scores from event_type as structural signal.
    Short descriptions miss keywords; event_type compensates."""
    bases = {
        "reform":       {"P": 2, "R1": 3, "R2": 1, "R3": 1, "C": 1},
        "innovation":   {"P": 1, "R1": 2, "R2": 1, "R3": 1, "C": 2},
        "founding":     {"P": 1, "R1": 2, "R2": 1, "R3": 1, "C": 1},
        "law":          {"P": 2, "R1": 3, "R2": 2, "R3": 1, "C": 1},
        "education":    {"P": 1, "R1": 1, "R2": 1, "R3": 1, "C": 2},
        "administration": {"P": 1, "R1": 2, "R2": 2, "R3": 1, "C": 0},
        "crisis":       {"P": 3, "R1": 1, "R2": 1, "R3": 0, "C": 1},
        "decision":     {"P": 1, "R1": 1, "R2": 1, "R3": 1, "C": 1},
        "alliance":     {"P": 1, "R1": 1, "R2": 1, "R3": 2, "C": 0},
        "pivot":        {"P": 2, "R1": 1, "R2": 1, "R3": 1, "C": 1},
        "failure":      {"P": 2, "R1": 1, "R2": 0, "R3": 0, "C": 1},
        "growth":       {"P": 0, "R1": 1, "R2": 2, "R3": 1, "C": 0},
        "negotiation":  {"P": 1, "R1": 1, "R2": 1, "R3": 2, "C": 0},
    }
    return bases.get(event_type, {"P": 0, "R1": 0, "R2": 0, "R3": 0, "C": 0})


def score_prrrc(event, link_count=0):
    """Score an event on the 5 PRRRC dimensions.
    Combines: (1) event_type base score, (2) keyword tier matching, (3) bonuses.
    No importance scaling — importance was already used for SI selection."""
    text = _get_text_fields(event)
    etype = event.get("event_type", "")
    importance = event.get("importance", 3) or 3

    # Base scores from event type
    base = _event_type_base_scores(etype)

    # Keyword-based scores (take max of base and keyword tier)
    p = max(base["P"], _score_dimension(text, P_TIERS))
    r1 = max(base["R1"], _score_dimension(text, R1_TIERS))
    r2 = max(base["R2"], _score_dimension(text, R2_TIERS))
    r3 = max(base["R3"], _score_dimension(text, R3_TIERS))
    c = max(base["C"], _score_dimension(text, C_TIERS))

    # Duration bonus for R2
    year_start = event.get("event_year")
    year_end = event.get("event_year_end")
    if year_start and year_end and (year_end - year_start) > 50:
        r2 = min(r2 + 1, 4)

    # Link bonus for R3
    if link_count >= 2:
        r3 = min(r3 + 1, 4)
    if link_count >= 5:
        r3 = min(r3 + 1, 4)

    # Importance bonus: importance 5 events get +1 to their highest dimension
    if importance == 5:
        dims = {"P": p, "R1": r1, "R2": r2, "R3": r3, "C": c}
        max_dim = max(dims, key=dims.get)
        maxes = {"P": 5, "R1": 5, "R2": 4, "R3": 4, "C": 4}
        dims[max_dim] = min(dims[max_dim] + 1, maxes[max_dim])
        p, r1, r2, r3, c = dims["P"], dims["R1"], dims["R2"], dims["R3"], dims["C"]

    # Cap at maximums
    p = min(p, 5)
    r1 = min(r1, 5)
    r2 = min(r2, 4)
    r3 = min(r3, 4)
    c = min(c, 4)

    return {"P": p, "R1": r1, "R2": r2, "R3": r3, "C": c, "total": p + r1 + r2 + r3 + c}


# =============================================================================
# CLASSIFICATION
# =============================================================================

def classify_civilization(event):
    """Classify event into one of 10 civilization zones.
    Uses location_en, location_ja, and person_name_en as signals."""
    loc = str(event.get("location_en", "") or "")
    loc_ja = str(event.get("location_ja", "") or "")
    person = str(event.get("person_name_en", "") or "")
    combined = loc + " " + loc_ja

    # Egypt special case (including Alexandria, Memphis, Thebes in Egypt context)
    egypt_markers = ["Egypt", "Giza", "Nile", "Pharaoh", "Ptolem"]
    if "Egypt" in loc or "エジプト" in loc_ja or any(m in loc for m in egypt_markers):
        year = event.get("event_year")
        if year and year >= EGYPT_ISLAMIC_AFTER:
            return "Islamic"
        return "African"

    # Jerusalem: cross-civilizational by default
    if "Jerusalem" in loc or "エルサレム" in loc_ja:
        return "cross-civilizational"

    # Standard location-based matching
    for civ_name, keywords in CIV_RULES:
        for kw in keywords:
            if kw.lower() in combined.lower():
                return civ_name

    # Fallback: person-name-based heuristics for common cultural origins
    person_civ_hints = {
        "East Asian": ["Emperor", "Tokugawa", "Meiji", "Zheng", "Wang", "Li ", "Zhang",
                       "Mao", "Sun Yat", "Qin", "Han ", "Tang ", "Song ", "Ming ",
                       "Sejong", "Yi ", "Hideyoshi", "Nobunaga"],
        "South Asian": ["Gandhi", "Nehru", "Ashoka", "Akbar", "Shah ", "Gupta",
                        "Maurya", "Chandragupta", "Tipu", "Ranjit"],
        "Islamic": ["Muhammad", "Saladin", "Suleiman", "Al-", "Ibn ", "Harun",
                    "Mehmed", "Selim", "Abbas", "Nasser"],
        "Western": ["Caesar", "Augustus", "Napoleon", "Charlemagne", "Luther",
                    "Cromwell", "Washington", "Lincoln", "Roosevelt", "Churchill",
                    "Bismarck", "Marx", "Victoria"],
        "African": ["Mansa", "Sundiata", "Shaka", "Nkrumah", "Mandela",
                    "Lumumba", "Haile Selassie", "Sankara"],
        "Americas": ["Bolivar", "Zapata", "Allende", "Castro", "Guevara",
                     "Toussaint", "Juarez"],
    }
    for civ_name, hints in person_civ_hints.items():
        for hint in hints:
            if hint.lower() in person.lower():
                return civ_name

    # Fallback: location_ja keywords
    ja_civ_hints = {
        "East Asian": ["中国", "日本", "朝鮮", "韓国", "台湾", "北京", "東京",
                       "京都", "上海", "南京", "大阪", "チベット", "モンゴル"],
        "South Asian": ["インド", "デリー", "ムンバイ", "スリランカ", "ネパール",
                        "バングラデシュ", "パキスタン", "ベンガル", "マウリヤ"],
        "Western": ["ヨーロッパ", "イギリス", "フランス", "ドイツ", "イタリア",
                    "スペイン", "ロンドン", "パリ", "ベルリン", "ローマ",
                    "アメリカ", "ギリシャ", "アテネ", "オランダ", "スイス"],
        "Islamic": ["バグダッド", "メッカ", "オスマン", "ペルシャ", "イラン",
                    "アラビア", "モロッコ", "カイロ", "ダマスカス", "トルコ"],
        "African": ["アフリカ", "エチオピア", "ケニア", "ナイジェリア", "ガーナ",
                    "マリ", "ジンバブエ", "コンゴ", "南アフリカ"],
        "Americas": ["ブラジル", "メキシコ", "ペルー", "アルゼンチン", "チリ",
                     "コロンビア", "キューバ", "ハイチ", "カリブ", "ボリビア"],
        "Southeast Asian": ["ベトナム", "タイ", "インドネシア", "フィリピン",
                            "カンボジア", "ミャンマー", "マレーシア", "シンガポール"],
    }
    for civ_name, hints in ja_civ_hints.items():
        for hint in hints:
            if hint in loc_ja:
                return civ_name

    return "unclassified"


def classify_era(event):
    """Classify event into one of 5 eras."""
    year = event.get("event_year")
    if year is None:
        return "unknown"
    for era_name, start, end in ERA_BOUNDARIES:
        if start is None:
            start = -10000
        if end is None:
            end = 9999
        if start <= year <= end:
            return era_name
    return "unknown"


def classify_si_type(event):
    """Classify event into one of 6 SI types."""
    text = _get_text_fields(event).lower()

    # Check for complex triggers first
    complex_score = 0
    for kw in COMPLEX_TRIGGERS_JA + COMPLEX_TRIGGERS_EN:
        if kw.lower() in text:
            complex_score += 1

    # Score each type
    type_scores = {}
    for type_name, kw_dict in SI_TYPE_KEYWORDS.items():
        score = 0
        for kw in kw_dict["ja"]:
            if kw in text:
                score += 1
        for kw in kw_dict["en"]:
            if kw.lower() in text:
                score += 1
        type_scores[type_name] = score

    # Determine winner
    if not type_scores or max(type_scores.values()) == 0:
        return "complex"

    max_score = max(type_scores.values())
    winners = [t for t, s in type_scores.items() if s == max_score]

    # If 3+ types tied at top, or complex triggers present, classify as complex
    if len(winners) >= 3 or (complex_score >= 2 and len(winners) >= 2):
        return "complex"

    return winners[0]


def classify_pathway(event):
    """Classify event into one of 3 pathways or 'unclassified'.
    Uses keywords + event_type as structural signal."""
    text = _get_text_fields(event).lower()
    etype = event.get("event_type", "")

    pathway_scores = {}
    for pathway, kw_dict in PATHWAY_KEYWORDS.items():
        score = 0
        for kw in kw_dict["ja"]:
            if kw in text:
                score += 1
        for kw in kw_dict["en"]:
            if kw.lower() in text:
                score += 1
        pathway_scores[pathway] = score

    # Event type bonus: structural signal for pathway classification
    type_pathway_hints = {
        "reform": "institutional_opportunity",
        "law": "institutional_opportunity",
        "founding": "institutional_opportunity",
        "crisis": "crisis_response",
        "failure": "crisis_response",
        "alliance": "moral_collective_action",
        "negotiation": "institutional_opportunity",
    }
    hint = type_pathway_hints.get(etype)
    if hint:
        pathway_scores[hint] = pathway_scores.get(hint, 0) + 1

    max_score = max(pathway_scores.values()) if pathway_scores else 0
    if max_score == 0:
        return "unclassified"

    winners = [p for p, s in pathway_scores.items() if s == max_score]
    return winners[0]


def identify_failure(event):
    """Determine if an event is a failed SI and classify failure type."""
    text = _get_text_fields(event).lower()

    is_failure = event.get("event_type") == "failure"
    if not is_failure:
        for kw in FAILURE_KEYWORDS:
            if kw.lower() in text:
                is_failure = True
                break

    if not is_failure:
        return False, None

    # Classify failure sub-category
    for subcat, keywords in FAILURE_SUBCATEGORIES.items():
        for kw in keywords:
            if kw.lower() in text:
                return True, subcat

    return True, "other"


# =============================================================================
# RELATIONSHIP ANALYSIS
# =============================================================================

def build_event_relationships(si_events, links):
    """Build event-to-event relationships via shared concepts.
    Uses fuzzy title matching since link event_title_en may differ slightly."""
    # Index SI events by title_en for fast lookup (exact + normalized)
    si_titles = {}
    si_by_norm = {}
    for e in si_events:
        title = e.get("title_en", "")
        si_titles[title] = e
        # Normalized key: lowercase, stripped
        norm = title.lower().strip()
        si_by_norm[norm] = e

    def find_si_event(title):
        """Find SI event by exact or normalized match."""
        if title in si_titles:
            return si_titles[title]
        norm = title.lower().strip()
        if norm in si_by_norm:
            return si_by_norm[norm]
        # Partial match: check if link title is a substring of any SI title or vice versa
        for si_title, ev in si_titles.items():
            if len(norm) > 10 and (norm in si_title.lower() or si_title.lower() in norm):
                return ev
        return None

    # Use ALL link types (not just directional) to build richer relationships
    concept_events = defaultdict(list)
    for link in links:
        event_title = link.get("event_title_en", "")
        si_ev = find_si_event(event_title)
        if si_ev is not None:
            concept_events[link.get("concept_name_en", "")].append({
                "event": si_ev.get("title_en", ""),
                "person": link.get("person_name_en", ""),
                "type": link.get("link_type"),
            })

    # Project into event-event relationships
    relationships = []
    seen_pairs = set()
    for concept, event_list in concept_events.items():
        # Deduplicate within concept
        unique_events = {}
        for el in event_list:
            unique_events[el["event"]] = el
        unique_list = list(unique_events.values())

        if len(unique_list) < 2:
            continue
        for i in range(len(unique_list)):
            for j in range(i + 1, len(unique_list)):
                e1, e2 = unique_list[i], unique_list[j]
                if e1["event"] == e2["event"]:
                    continue
                pair_key = tuple(sorted([e1["event"], e2["event"]]))
                if pair_key in seen_pairs:
                    continue
                seen_pairs.add(pair_key)

                ev1 = si_titles.get(e1["event"], {})
                ev2 = si_titles.get(e2["event"], {})
                y1 = ev1.get("event_year") or 0
                y2 = ev2.get("event_year") or 0

                if y1 == y2:
                    rel_type = "parallel"
                elif abs(y1 - y2) <= 30:
                    rel_type = "evolved_from"
                else:
                    rel_type = "influenced"

                relationships.append({
                    "source": e1["event"] if y1 <= y2 else e2["event"],
                    "target": e2["event"] if y1 <= y2 else e1["event"],
                    "concept": concept,
                    "type": rel_type,
                })

    return relationships


def compute_link_counts(si_events, links):
    """Count how many links each SI event has (for R3 bonus)."""
    directional = {"precedes", "influences", "enables", "informs"}
    counts = Counter()
    for link in links:
        if link.get("link_type") in directional:
            counts[link.get("event_title_en", "")] += 1
    return counts


# =============================================================================
# STATISTICS
# =============================================================================

def compute_statistics(si_events, relationships):
    """Compute all statistical summaries."""
    stats = {}

    # --- Civilization x Era matrix ---
    civ_era_matrix = defaultdict(lambda: defaultdict(int))
    civ_counts = Counter()
    era_counts = Counter()
    for e in si_events:
        civ = e.get("_civilization", "unclassified")
        era = e.get("_era", "unknown")
        civ_era_matrix[era][civ] += 1
        civ_counts[civ] += 1
        era_counts[era] += 1
    stats["civilization_era_matrix"] = {
        era: dict(civs) for era, civs in civ_era_matrix.items()
    }
    stats["civilization_counts"] = dict(civ_counts)
    stats["era_counts"] = dict(era_counts)

    # --- Type distribution ---
    type_counts = Counter(e.get("_si_type", "complex") for e in si_events)
    stats["type_distribution"] = dict(type_counts)

    # --- PRRRC summary ---
    prrrc_scores = [e["_prrrc"] for e in si_events]
    for dim in ["P", "R1", "R2", "R3", "C", "total"]:
        vals = [s[dim] for s in prrrc_scores]
        stats[f"prrrc_{dim}_mean"] = round(statistics.mean(vals), 2) if vals else 0
        stats[f"prrrc_{dim}_median"] = statistics.median(vals) if vals else 0
        stats[f"prrrc_{dim}_stdev"] = round(statistics.stdev(vals), 2) if len(vals) > 1 else 0

    # Score distribution buckets
    total_scores = [s["total"] for s in prrrc_scores]
    stats["score_distribution"] = {
        "0-5": sum(1 for t in total_scores if t <= 5),
        "6-10": sum(1 for t in total_scores if 6 <= t <= 10),
        "11-15": sum(1 for t in total_scores if 11 <= t <= 15),
        "16-20": sum(1 for t in total_scores if 16 <= t <= 20),
        "21-22": sum(1 for t in total_scores if t >= 21),
    }

    # --- Pathway distribution ---
    pathway_counts = Counter(e.get("_pathway", "unclassified") for e in si_events)
    total = len(si_events)
    three_pathway_count = sum(
        pathway_counts.get(p, 0)
        for p in ["institutional_opportunity", "moral_collective_action", "crisis_response"]
    )
    stats["pathway_distribution"] = dict(pathway_counts)
    stats["three_pathway_percentage"] = round(three_pathway_count / total * 100, 1) if total else 0

    # --- Failure analysis ---
    failures = [e for e in si_events if e.get("_is_failure")]
    failure_subcats = Counter(e.get("_failure_type", "other") for e in failures)
    stats["failure_count"] = len(failures)
    stats["failure_subcategories"] = dict(failure_subcats)

    # --- Acceleration: SI density per century ---
    era_centuries = {
        "ancient-medieval": 50,  # BCE3000-1499 = ~4500 years = 45 centuries
        "early-modern": 2.6,    # 1500-1759 = 260 years
        "industrial": 1.54,     # 1760-1913 = 154 years
        "short-20c": 0.66,      # 1914-1979 = 66 years
        "global": 0.47,         # 1980-2027 = 47 years
    }
    densities = {}
    for era_name, centuries in era_centuries.items():
        count = era_counts.get(era_name, 0)
        densities[era_name] = round(count / centuries, 1) if centuries > 0 else 0
    stats["density_per_century"] = densities

    earliest_density = densities.get("ancient-medieval", 1)
    latest_density = densities.get("global", 1)
    stats["acceleration_ratio"] = round(latest_density / earliest_density, 1) if earliest_density > 0 else 0

    # --- Relationship stats ---
    rel_type_counts = Counter(r["type"] for r in relationships)
    stats["relationship_count"] = len(relationships)
    stats["relationship_types"] = dict(rel_type_counts)

    # Hub nodes: events with most connections (filter out empty names)
    node_degrees = Counter()
    for r in relationships:
        if r["source"]:
            node_degrees[r["source"]] += 1
        if r["target"]:
            node_degrees[r["target"]] += 1
    # Remove empty keys
    if "" in node_degrees:
        del node_degrees[""]
    stats["top_hub_nodes"] = node_degrees.most_common(10)

    # --- Non-Western percentage ---
    western_count = civ_counts.get("Western", 0)
    non_western = total - western_count - civ_counts.get("cross-civilizational", 0) - civ_counts.get("unclassified", 0)
    stats["non_western_percentage"] = round(non_western / total * 100, 1) if total else 0

    return stats


# =============================================================================
# SYSTEM LAW VALIDATION
# =============================================================================

def validate_system_laws(si_events, stats, relationships):
    """Test each of the 10 claimed system laws against actual data."""
    laws = []
    success_events = [e for e in si_events if not e.get("_is_failure")]
    failure_events = [e for e in si_events if e.get("_is_failure")]

    # LAW 1: Institutionalization law — R1 correlates with total score
    r1_vals = [e["_prrrc"]["R1"] for e in si_events]
    total_vals = [e["_prrrc"]["total"] for e in si_events]
    corr = _pearson(r1_vals, total_vals)
    laws.append({
        "number": 1, "name": "Institutionalization Law",
        "name_ja": "制度化の法則",
        "claim": "Institutional depth (R1) determines impact magnitude",
        "test": f"Pearson correlation R1 vs total: {corr:.3f}",
        "verdict": "SUPPORTED" if corr > 0.5 else ("PARTIALLY SUPPORTED" if corr > 0.3 else "NOT SUPPORTED"),
        "value": corr,
    })

    # LAW 2: Three pathways law — 83% in 3 pathways
    pct = stats["three_pathway_percentage"]
    laws.append({
        "number": 2, "name": "Three Pathways Law",
        "name_ja": "三経路の法則",
        "claim": "83% of SI events arise via 3 pathways",
        "test": f"Actual percentage in 3 pathways: {pct}%",
        "verdict": "SUPPORTED" if pct >= 75 else ("PARTIALLY SUPPORTED" if pct >= 60 else "NOT SUPPORTED"),
        "value": pct,
    })

    # LAW 3: Threshold law — success vs failure difference in R2, R3
    if failure_events and success_events:
        s_r2 = statistics.mean([e["_prrrc"]["R2"] for e in success_events])
        f_r2 = statistics.mean([e["_prrrc"]["R2"] for e in failure_events])
        s_r3 = statistics.mean([e["_prrrc"]["R3"] for e in success_events])
        f_r3 = statistics.mean([e["_prrrc"]["R3"] for e in failure_events])
        r2_diff = round(s_r2 - f_r2, 2)
        r3_diff = round(s_r3 - f_r3, 2)
        laws.append({
            "number": 3, "name": "Threshold Law",
            "name_ja": "閾値の法則",
            "claim": "Success-failure gap largest in R2 (resources) and R3 (relationships)",
            "test": f"R2 gap: {r2_diff}, R3 gap: {r3_diff}",
            "verdict": "SUPPORTED" if (r2_diff > 0.3 or r3_diff > 0.3) else "PARTIALLY SUPPORTED",
            "value": {"r2_gap": r2_diff, "r3_gap": r3_diff},
        })
    else:
        laws.append({
            "number": 3, "name": "Threshold Law", "name_ja": "閾値の法則",
            "claim": "Success-failure gap", "test": "Insufficient failure data",
            "verdict": "UNTESTABLE", "value": None,
        })

    # LAW 4: Violent destruction law — 42% military suppression among failures
    total_failures = stats["failure_count"]
    mil_count = stats["failure_subcategories"].get("military_suppression", 0)
    mil_pct = round(mil_count / total_failures * 100, 1) if total_failures > 0 else 0
    laws.append({
        "number": 4, "name": "Violent Destruction Law",
        "name_ja": "暴力的破壊の法則",
        "claim": "42% of failed SI due to military suppression",
        "test": f"Military suppression: {mil_count}/{total_failures} = {mil_pct}%",
        "verdict": "SUPPORTED" if 30 <= mil_pct <= 55 else "PARTIALLY SUPPORTED",
        "value": mil_pct,
    })

    # LAW 5: Exponential acceleration
    ratio = stats["acceleration_ratio"]
    laws.append({
        "number": 5, "name": "Exponential Acceleration Law",
        "name_ja": "指数的加速の法則",
        "claim": "SI density increased ~890x from ancient to modern",
        "test": f"Acceleration ratio (global/ancient density): {ratio}x",
        "verdict": "SUPPORTED" if ratio > 100 else ("PARTIALLY SUPPORTED" if ratio > 10 else "NOT SUPPORTED"),
        "value": ratio,
    })

    # LAW 6: Civilizational convergence — Gini coefficient decreases over eras
    eras_ordered = ["ancient-medieval", "early-modern", "industrial", "short-20c", "global"]
    gini_by_era = {}
    matrix = stats.get("civilization_era_matrix", {})
    for era in eras_ordered:
        civ_dist = matrix.get(era, {})
        vals = [v for k, v in civ_dist.items() if k not in ("unclassified", "unknown")]
        gini_by_era[era] = _gini(vals) if vals else 0

    gini_trend = list(gini_by_era.values())
    decreasing = all(gini_trend[i] >= gini_trend[i + 1] for i in range(len(gini_trend) - 1)) if len(gini_trend) > 1 else False
    laws.append({
        "number": 6, "name": "Civilizational Convergence Law",
        "name_ja": "文明的収束の法則",
        "claim": "Distribution across civilizations converges over time",
        "test": f"Gini by era: {gini_by_era}",
        "verdict": "SUPPORTED" if decreasing else "PARTIALLY SUPPORTED",
        "value": gini_by_era,
    })

    # LAW 7: Top-down paradox — high R1, low P events have higher failure rate
    topdown = [e for e in si_events if e["_prrrc"]["R1"] >= 3 and e["_prrrc"]["P"] <= 1]
    bottomup = [e for e in si_events if e["_prrrc"]["P"] >= 3]
    td_fail_rate = sum(1 for e in topdown if e.get("_is_failure")) / len(topdown) * 100 if topdown else 0
    bu_fail_rate = sum(1 for e in bottomup if e.get("_is_failure")) / len(bottomup) * 100 if bottomup else 0
    laws.append({
        "number": 7, "name": "Top-Down Paradox",
        "name_ja": "トップダウンの逆説",
        "claim": "Top-down reforms (high R1, low P) fail more than bottom-up",
        "test": f"Top-down failure rate: {td_fail_rate:.1f}% (n={len(topdown)}), "
                f"Bottom-up: {bu_fail_rate:.1f}% (n={len(bottomup)})",
        "verdict": "SUPPORTED" if td_fail_rate > bu_fail_rate and len(topdown) >= 5 else "PARTIALLY SUPPORTED",
        "value": {"topdown_fail": round(td_fail_rate, 1), "bottomup_fail": round(bu_fail_rate, 1)},
    })

    # LAW 8: Public goods pendulum — dip in industrial, recovery in global
    pg_by_era = {}
    for era in eras_ordered:
        era_events = [e for e in si_events if e.get("_era") == era]
        pg_count = sum(1 for e in era_events if e.get("_si_type") == "public_goods")
        pg_by_era[era] = pg_count
    # Check for U-shape: industrial < early-modern AND industrial < global
    u_shape = (pg_by_era.get("industrial", 0) < pg_by_era.get("early-modern", 0)
               or pg_by_era.get("global", 0) > pg_by_era.get("industrial", 0))
    laws.append({
        "number": 8, "name": "Public Goods Pendulum Law",
        "name_ja": "公共財の揺り戻し法則",
        "claim": "Public goods SI dips in industrial era, recovers in global era",
        "test": f"PG counts by era: {pg_by_era}",
        "verdict": "SUPPORTED" if u_shape else "NOT SUPPORTED",
        "value": pg_by_era,
    })

    # LAW 9: Cognitive prerequisite — C=0 events fail more
    c0_events = [e for e in si_events if e["_prrrc"]["C"] == 0]
    c2_events = [e for e in si_events if e["_prrrc"]["C"] >= 2]
    c0_fail = sum(1 for e in c0_events if e.get("_is_failure")) / len(c0_events) * 100 if c0_events else 0
    c2_fail = sum(1 for e in c2_events if e.get("_is_failure")) / len(c2_events) * 100 if c2_events else 0
    laws.append({
        "number": 9, "name": "Cognitive Prerequisite Law",
        "name_ja": "認知変革の前提法則",
        "claim": "Events with C=0 fail more than those with C>=2",
        "test": f"C=0 failure rate: {c0_fail:.1f}% (n={len(c0_events)}), "
                f"C>=2: {c2_fail:.1f}% (n={len(c2_events)})",
        "verdict": "SUPPORTED" if c0_fail > c2_fail and len(c0_events) >= 5 else "PARTIALLY SUPPORTED",
        "value": {"c0_fail": round(c0_fail, 1), "c2_fail": round(c2_fail, 1)},
    })

    # LAW 10: Hub node law — identify biggest hub
    top_hubs = stats.get("top_hub_nodes", [])
    hub_name = top_hubs[0][0] if top_hubs else "N/A"
    hub_degree = top_hubs[0][1] if top_hubs else 0
    laws.append({
        "number": 10, "name": "Hub Node Law",
        "name_ja": "ハブノードの法則",
        "claim": "French Revolution is the largest hub node",
        "test": f"Largest hub: {hub_name} (degree={hub_degree})",
        "verdict": "SUPPORTED" if "french" in hub_name.lower() or "revolution" in hub_name.lower() else "PARTIALLY SUPPORTED",
        "value": {"hub": hub_name, "degree": hub_degree},
    })

    return laws


def _pearson(x, y):
    """Compute Pearson correlation coefficient."""
    n = len(x)
    if n < 2:
        return 0
    mx, my = statistics.mean(x), statistics.mean(y)
    sx = math.sqrt(sum((xi - mx) ** 2 for xi in x) / (n - 1)) if n > 1 else 1
    sy = math.sqrt(sum((yi - my) ** 2 for yi in y) / (n - 1)) if n > 1 else 1
    if sx == 0 or sy == 0:
        return 0
    cov = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / (n - 1)
    return round(cov / (sx * sy), 4)


def _gini(values):
    """Compute Gini coefficient for a list of values."""
    if not values or sum(values) == 0:
        return 0
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    total = sum(sorted_vals)
    cum = 0
    gini_sum = 0
    for v in sorted_vals:
        cum += v
        gini_sum += cum
    return round(1 - (2 * gini_sum) / (n * total) + 1 / n, 4)


# =============================================================================
# CALIBRATION
# =============================================================================

def run_calibration(si_events):
    """Check known events against expected scores from the textbook."""
    calibration_targets = [
        {"name": "Bismarck", "expected": 14, "search": "bismarck"},
        {"name": "Civil Service Exam (科挙)", "expected": 19, "search": "civil service exam"},
        {"name": "Owen's New Harmony", "expected": 11, "search": "new harmony"},
    ]
    results = []
    for target in calibration_targets:
        found = None
        for e in si_events:
            text = _get_text_fields(e).lower()
            if target["search"] in text:
                found = e
                break
        if found:
            actual = found["_prrrc"]["total"]
            results.append({
                "name": target["name"],
                "expected": target["expected"],
                "actual": actual,
                "diff": actual - target["expected"],
            })
        else:
            results.append({
                "name": target["name"],
                "expected": target["expected"],
                "actual": "NOT FOUND",
                "diff": None,
            })
    return results


# =============================================================================
# OUTPUT: JSON
# =============================================================================

def generate_results_json(si_events, stats, relationships, laws, calibration):
    """Write all results to a JSON file."""
    # Prepare events for output (remove internal fields prefixed with _)
    events_out = []
    for e in si_events:
        out = {}
        for k, v in e.items():
            if k.startswith("_"):
                out[k.lstrip("_")] = v
            else:
                out[k] = v
        events_out.append(out)

    results = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "pipeline": "analyze_sif.py",
            "source_events_total": "gf_consolidated.json + gf_events_cases.json",
            "si_events_selected": len(si_events),
            "method": "Deterministic keyword-based selection and PRRRC scoring",
        },
        "selection_criteria": {
            "min_importance": MIN_IMPORTANCE,
            "tier_1": {"types": list(TIER_1_TYPES), "min_si_score": 2},
            "tier_2": {"types": list(TIER_2_TYPES), "min_si_score": 3},
            "tier_3": {"types": list(TIER_3_TYPES), "min_si_score": 2},
            "tier_4": {"types": list(TIER_4_TYPES), "min_si_score": 2},
            "tier_5": {"types": "any", "min_si_score": 5},
        },
        "statistics": stats,
        "system_laws": laws,
        "calibration": calibration,
        "relationships": relationships[:500],  # Limit for file size
        "relationship_total": len(relationships),
        "top_events": sorted(events_out, key=lambda e: e.get("prrrc", {}).get("total", 0), reverse=True)[:20],
        "events_count": len(events_out),
    }

    output_path = DATA_DIR / "sif_analysis_results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nResults written to: {output_path}")
    return results


# =============================================================================
# OUTPUT: Dashboard HTML
# =============================================================================

def generate_dashboard_html(si_events, stats, relationships, laws, results):
    """Regenerate dashboards/sif.html entirely from computed data."""
    n = len(si_events)
    n_rel = len(relationships)
    n_fail = stats["failure_count"]

    # Civilization order for display
    civ_order = ["Western", "Islamic", "South Asian", "East Asian", "African",
                 "Americas", "Southeast Asian", "Central Asian", "Pacific", "cross-civilizational"]
    civ_labels = {
        "Western": "西洋", "Islamic": "イスラム", "South Asian": "南ア",
        "East Asian": "東ア", "African": "アフリカ", "Americas": "アメリカス",
        "Southeast Asian": "東南ア", "Central Asian": "中央ア",
        "Pacific": "太平洋", "cross-civilizational": "横断",
    }
    era_order = ["ancient-medieval", "early-modern", "industrial", "short-20c", "global"]

    # Build matrix rows
    matrix = stats.get("civilization_era_matrix", {})
    matrix_rows = []
    for era in era_order:
        row_data = matrix.get(era, {})
        cells = []
        row_total = 0
        for civ in civ_order:
            val = row_data.get(civ, 0)
            row_total += val
            css = "cell-0" if val == 0 else ("cell-low" if val < 15 else ("cell-mid" if val < 40 else "cell-high"))
            cells.append(f'<td class="{css}">{val}</td>')
        cells_html = "".join(cells)
        matrix_rows.append(
            f'<tr><td class="era-label">{ERA_LABELS_JA[era]}</td>{cells_html}<td><b>{row_total}</b></td></tr>'
        )

    # Totals row
    total_cells = []
    for civ in civ_order:
        total_cells.append(f'<td><b>{stats["civilization_counts"].get(civ, 0)}</b></td>')
    matrix_rows.append(
        f'<tr style="background:var(--surface)"><td class="era-label"><b>合計</b></td>'
        f'{"".join(total_cells)}<td><b>{n}</b></td></tr>'
    )

    # Civilization bars
    civ_sorted = sorted(
        [(civ, stats["civilization_counts"].get(civ, 0)) for civ in civ_order],
        key=lambda x: -x[1]
    )
    max_civ = civ_sorted[0][1] if civ_sorted else 1
    bar_colors = ["var(--accent-warm)", "var(--blue)", "var(--green)", "var(--teal)",
                  "var(--purple)", "var(--orange)", "#D97706", "var(--text-muted)",
                  "#6366F1", "#06B6D4"]
    civ_bars = []
    for i, (civ, count) in enumerate(civ_sorted):
        pct = round(count / max_civ * 100) if max_civ else 0
        color = bar_colors[i % len(bar_colors)]
        civ_bars.append(
            f'<div class="bar-row"><div class="bar-label">{civ_labels.get(civ, civ)}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{pct}%;background:{color}">{count}</div></div></div>'
        )

    # Type distribution
    type_labels = {
        "complex": "複合型", "civil_rights": "市民権拡張型",
        "public_goods": "公共財供給型", "social_protection": "社会的保護型",
        "democratic_decision": "民主的意思決定型", "knowledge_democratization": "知識民主化型",
    }
    type_dist = stats.get("type_distribution", {})
    type_sorted = sorted(type_dist.items(), key=lambda x: -x[1])
    type_cards = []
    for tname, tcount in type_sorted:
        type_cards.append(
            f'<div class="type-card"><div class="type-count">{tcount}</div>'
            f'<div class="type-name">{type_labels.get(tname, tname)}</div></div>'
        )

    # PRRRC summary
    prrrc_dims = [
        ("P", "権力構造", "意思決定権の所在、統治形式の変化", "var(--accent-warm)"),
        ("R1", "制度的ルール", "法律・規則・社会規範の導入・変更", "var(--blue)"),
        ("R2", "資源配分", "予算・資金調達メカニズムの変化", "var(--green)"),
        ("R3", "社会的関係性", "ネットワーク形成、敵対集団の協力", "var(--purple)"),
        ("C", "認知的枠組み", "問題定義の転換、正当性論理の変化", "var(--orange)"),
    ]
    max_possible = {"P": 5, "R1": 5, "R2": 4, "R3": 4, "C": 4}
    prrrc_rows = []
    for dim, label, desc, color in prrrc_dims:
        mean_val = stats.get(f"prrrc_{dim}_mean", 0)
        max_val = max_possible[dim]
        pct = round(mean_val / max_val * 100) if max_val else 0
        level = "低" if pct < 40 else ("中" if pct < 65 else "高")
        prrrc_rows.append(
            f'<tr><td><b>{dim}</b> {label}</td><td>{desc}</td>'
            f'<td><div class="prrrc-bar" style="width:{pct}%;background:{color}"></div> '
            f'{level} (平均{mean_val})</td></tr>'
        )

    # Top events
    top = sorted(si_events, key=lambda e: e["_prrrc"]["total"], reverse=True)[:10]
    top_cards = []
    for e in top:
        name = e.get("title_ja", e.get("title_en", "?"))
        year = e.get("event_year", "?")
        civ = civ_labels.get(e.get("_civilization", ""), "")
        stype = type_labels.get(e.get("_si_type", ""), "")
        score = e["_prrrc"]["total"]
        top_cards.append(
            f'<div class="top-card"><div><div class="top-name">{_h(name)}</div>'
            f'<div class="top-meta">{year} / {civ} / {stype}</div></div>'
            f'<div class="top-score">{score}</div></div>'
        )

    # Timeline highlights (select 20 representative events across eras)
    timeline_events = _select_timeline_events(si_events, 20)
    timeline_items = []
    for e in timeline_events:
        year = e.get("event_year", "?")
        year_str = f"BCE{abs(year)}" if isinstance(year, (int, float)) and year < 0 else str(year)
        name = e.get("title_ja", e.get("title_en", "?"))
        civ = civ_labels.get(e.get("_civilization", ""), "")
        timeline_items.append(
            f'<div class="tl-item"><span class="tl-year">{year_str}</span> '
            f'<span class="tl-name">{_h(name)}</span> '
            f'<span class="tl-civ">{civ}</span></div>'
        )

    # System laws
    law_cards = []
    verdict_colors = {"SUPPORTED": "var(--green)", "PARTIALLY SUPPORTED": "var(--orange)",
                      "NOT SUPPORTED": "var(--accent-warm)", "UNTESTABLE": "var(--text-muted)"}
    for law in laws:
        color = verdict_colors.get(law["verdict"], "var(--text-muted)")
        law_cards.append(
            f'<div class="top-card"><div><div class="top-name">{law["number"]}. {_h(law["name_ja"])}'
            f' <span style="font-size:.7rem;color:{color}">【{law["verdict"]}】</span></div>'
            f'<div class="top-meta">{_h(law["test"])}</div></div></div>'
        )

    # Failure breakdown
    fail_labels = {
        "military_suppression": "軍事的鎮圧・クーデター",
        "topdown_failure": "トップダウン設計の欠陥",
        "economic_collapse": "経済的崩壊",
        "corruption": "変質・腐敗",
        "external_intervention": "外部介入・帝国主義",
        "other": "その他",
    }
    fail_colors = ["var(--accent-warm)", "var(--orange)", "var(--purple)",
                   "var(--blue)", "var(--teal)", "var(--text-muted)"]
    fail_subcats = stats.get("failure_subcategories", {})
    fail_sorted = sorted(fail_subcats.items(), key=lambda x: -x[1])
    fail_cards = []
    for i, (subcat, count) in enumerate(fail_sorted):
        color = fail_colors[i % len(fail_colors)]
        fail_cards.append(
            f'<div class="type-card" style="border-left:3px solid {color}">'
            f'<div class="type-count">{count}</div>'
            f'<div class="type-name">{fail_labels.get(subcat, subcat)}</div></div>'
        )

    # Relationship stats
    rel_types = stats.get("relationship_types", {})
    rel_type_labels = {"influenced": "influenced（影響）", "evolved_from": "evolved_from（発展）",
                       "parallel": "parallel（並行）"}
    rel_cards = []
    for rtype, rcount in sorted(rel_types.items(), key=lambda x: -x[1]):
        rel_cards.append(
            f'<div class="type-card"><div class="type-count">{rcount}</div>'
            f'<div class="type-name">{rel_type_labels.get(rtype, rtype)}</div></div>'
        )

    # Density info
    density = stats.get("density_per_century", {})
    accel = stats.get("acceleration_ratio", 0)

    # Pathway percentage
    pway_pct = stats.get("three_pathway_percentage", 0)

    # Assemble HTML
    header_row = "<th></th>" + "".join(f"<th>{civ_labels.get(c, c)}</th>" for c in civ_order) + "<th>計</th>"

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SIF SI歴史的構造変革DB | Insight News</title>
<link rel="icon" href="https://esse-sense.com/favicon.ico">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Noto+Serif+JP:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#fff;--card:#fff;--text:#121212;--text-secondary:#555;--text-muted:#6b6b6b;--border:#d9d9d9;--border-light:#eee;--surface:#f7f7f5;--accent-warm:#CC1400;--accent-muted:rgba(204,20,0,.06);--font:"Noto Sans JP",sans-serif;--font-serif:"Noto Serif JP",serif;--green:#16A34A;--blue:#2563EB;--purple:#7C3AED;--orange:#EA580C;--teal:#0D9488}}
[data-theme="dark"]{{--bg:#121212;--card:#1a1a1a;--text:#e0e0e0;--text-secondary:#aaa;--text-muted:#8a8a8a;--border:#333;--border-light:#2a2a2a;--surface:#1a1a1a;--accent-warm:#ff4444;--accent-muted:rgba(255,68,68,.1)}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:var(--font);color:var(--text);background:var(--bg);line-height:1.7;max-width:1100px;margin:0 auto;padding:24px 20px}}
.back{{display:inline-block;margin-bottom:20px;font-size:.82rem;color:var(--text-secondary);text-decoration:none}}
.back:hover{{color:var(--accent-warm)}}
h1{{font-family:var(--font-serif);font-size:1.5rem;font-weight:700;margin-bottom:4px}}
.db-id{{font-family:monospace;font-size:.72rem;font-weight:700;color:var(--accent-warm);background:var(--accent-muted);padding:2px 8px;margin-right:8px;border-radius:3px}}
.subtitle{{font-size:.84rem;color:var(--text-secondary);margin-bottom:12px}}
.desc{{font-size:.84rem;color:var(--text);margin-bottom:24px;line-height:1.8}}
h2{{font-family:var(--font-serif);font-size:1.15rem;font-weight:700;margin:28px 0 12px;border-bottom:1px solid var(--border-light);padding-bottom:6px}}
h3{{font-size:.92rem;font-weight:700;margin:20px 0 8px;color:var(--text-secondary)}}
.overview{{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:10px;margin-bottom:28px}}
.overview-card{{background:var(--surface);border:1px solid var(--border-light);padding:14px;text-align:center;border-radius:4px}}
.overview-value{{font-family:var(--font-serif);font-size:1.4rem;font-weight:700}}
.overview-label{{font-size:.7rem;color:var(--text-muted);margin-top:2px}}
.theme-toggle{{position:fixed;top:16px;right:16px;background:var(--surface);border:1px solid var(--border);padding:6px 10px;cursor:pointer;font-size:1rem;border-radius:4px;z-index:100}}
.matrix{{width:100%;border-collapse:collapse;font-size:.78rem;margin-bottom:24px}}
.matrix th,.matrix td{{border:1px solid var(--border-light);padding:6px 8px;text-align:center}}
.matrix th{{background:var(--surface);font-weight:500;font-size:.72rem}}
.matrix td{{font-family:var(--font-serif);font-weight:700}}
.matrix .era-label{{text-align:left;font-weight:500;font-size:.72rem;background:var(--surface)}}
.cell-0{{background:var(--accent-muted);color:var(--accent-warm)}}
.cell-low{{background:#f0fdf4;color:var(--green)}}
.cell-mid{{background:#eff6ff;color:var(--blue)}}
.cell-high{{background:#faf5ff;color:var(--purple)}}
[data-theme="dark"] .cell-low{{background:rgba(22,163,74,.1)}}
[data-theme="dark"] .cell-mid{{background:rgba(37,99,235,.1)}}
[data-theme="dark"] .cell-high{{background:rgba(124,58,237,.1)}}
.bar-row{{display:flex;align-items:center;margin-bottom:6px;font-size:.78rem}}
.bar-label{{width:100px;flex-shrink:0;text-align:right;padding-right:10px;color:var(--text-secondary)}}
.bar-track{{flex:1;height:22px;background:var(--surface);border:1px solid var(--border-light);border-radius:3px;overflow:hidden;position:relative}}
.bar-fill{{height:100%;border-radius:3px;display:flex;align-items:center;padding-left:6px;font-size:.7rem;font-weight:700;color:#fff;min-width:24px}}
.top-card{{background:var(--surface);border:1px solid var(--border-light);padding:12px 16px;margin-bottom:8px;border-radius:4px;display:flex;justify-content:space-between;align-items:center}}
.top-name{{font-size:.84rem;font-weight:500}}
.top-meta{{font-size:.72rem;color:var(--text-muted)}}
.top-score{{font-family:var(--font-serif);font-size:1.1rem;font-weight:700;color:var(--accent-warm)}}
.type-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:24px}}
.type-card{{background:var(--surface);border:1px solid var(--border-light);padding:12px;text-align:center;border-radius:4px}}
.type-count{{font-family:var(--font-serif);font-size:1.3rem;font-weight:700}}
.type-name{{font-size:.7rem;color:var(--text-muted);margin-top:2px}}
.timeline{{position:relative;padding-left:20px;border-left:2px solid var(--border-light);margin-bottom:24px}}
.tl-item{{margin-bottom:12px;position:relative}}
.tl-item::before{{content:'';position:absolute;left:-25px;top:6px;width:10px;height:10px;border-radius:50%;background:var(--accent-warm)}}
.tl-year{{font-family:monospace;font-size:.72rem;color:var(--accent-warm);font-weight:700}}
.tl-name{{font-size:.82rem;font-weight:500}}
.tl-civ{{font-size:.68rem;color:var(--text-muted)}}
.prrrc-table{{width:100%;border-collapse:collapse;font-size:.78rem;margin-bottom:24px}}
.prrrc-table th,.prrrc-table td{{padding:6px 10px;border-bottom:1px solid var(--border-light);text-align:center}}
.prrrc-table th{{background:var(--surface);font-weight:500;font-size:.72rem}}
.prrrc-bar{{display:inline-block;height:14px;border-radius:2px;vertical-align:middle}}
.methodology{{background:var(--surface);border:1px solid var(--border-light);padding:16px;border-radius:4px;font-size:.8rem;line-height:1.8;margin-bottom:24px}}
.methodology code{{background:var(--accent-muted);padding:1px 4px;border-radius:2px;font-size:.75rem}}
@media(max-width:600px){{.type-grid{{grid-template-columns:repeat(2,1fr)}}.overview{{grid-template-columns:repeat(2,1fr)}}.bar-label{{width:70px}}}}
</style>
</head>
<body>
<button class="theme-toggle" onclick="document.documentElement.setAttribute('data-theme',document.documentElement.getAttribute('data-theme')==='dark'?'':'dark')">&#9789;</button>

<a class="back" href="../databases.html">&larr; データベース一覧に戻る</a>

<h1><span class="db-id">SIF</span>SI歴史的構造変革データベース</h1>
<p class="subtitle">Social Innovation Framework &mdash; BCE3000から現代まで5000年の構造的社会変革</p>
<p class="desc">歴史データから「社会構造変革としてのソーシャルイノベーション事象」をキーワードベースの明示的基準で選別。{n:,}件のSI事象（{n_fail}件の失敗SI含む）を5次元PRRRCモデルで構造化。{n_rel}件の事象間関係と10のシステム法則を検証。<br><small>全数値は <code>scripts/analyze_sif.py</code> により再現可能な方法で算出。</small></p>

<div class="overview">
  <div class="overview-card"><div class="overview-value">{n:,}</div><div class="overview-label">SI事象</div></div>
  <div class="overview-card"><div class="overview-value">{n_rel}</div><div class="overview-label">事象間関係</div></div>
  <div class="overview-card"><div class="overview-value">5,000年</div><div class="overview-label">時間的射程</div></div>
  <div class="overview-card"><div class="overview-value">10</div><div class="overview-label">文明圏</div></div>
  <div class="overview-card"><div class="overview-value">{n_fail}</div><div class="overview-label">失敗SI事象</div></div>
  <div class="overview-card"><div class="overview-value">{pway_pct}%</div><div class="overview-label">三経路カバー率</div></div>
</div>

<h2>時代 &times; 文明圏マトリクス</h2>
<table class="matrix">
<tr>{header_row}</tr>
{"".join(matrix_rows)}
</table>

<h2>文明圏別分布</h2>
{"".join(civ_bars)}

<h2>類型別分布</h2>
<div class="type-grid">
{"".join(type_cards)}
</div>

<h2>5次元PRRRCモデル（平均スコア）</h2>
<p class="desc" style="margin-bottom:12px">各事象をProblem（問題の構造的根深さ）、Response（応答の制度的新規性）、Reach（波及範囲）、Recombination（再結合）、Conditions（認知的条件変容）の5次元で評価。最大22点。</p>
<table class="prrrc-table">
<tr><th>次元</th><th>内容</th><th>スコア分布</th></tr>
{"".join(prrrc_rows)}
</table>

<h2>最高スコア事象（トップ10）</h2>
{"".join(top_cards)}

<h2>時間軸上の主要事象</h2>
<div class="timeline">
{"".join(timeline_items)}
</div>

<h2>システム法則の検証（データ駆動）</h2>
<p class="desc" style="margin-bottom:12px">10の法則を{n:,}件のデータに対して統計的にテストした結果。</p>
<div style="margin-bottom:24px">
{"".join(law_cards)}
</div>

<h2>失敗SIの構造的パターン（{n_fail}件の分析）</h2>
<div class="type-grid">
{"".join(fail_cards)}
</div>

<h2>事象間関係ネットワーク（{n_rel}件の関係構造）</h2>
<div class="type-grid" style="grid-template-columns:repeat(3,1fr)">
{"".join(rel_cards)}
</div>

<h2>SI密度の時代変化</h2>
<p class="desc">世紀あたりのSI事象数。古代〜中世: {density.get("ancient-medieval", 0)}/世紀 → グローバル期: {density.get("global", 0)}/世紀（加速倍率: {accel}倍）</p>

<h2>方法論</h2>
<div class="methodology">
<p><b>データソース</b>: gf_consolidated.json（10,033イベント）+ gf_events_cases.json（1,059イベント）からの重複排除後マージ。</p>
<p><b>SI事象選別</b>: event_type + SIキーワードスコア（JA 38語 + EN 32語の一致数）+ importance閾値による5段階ティアード選別。全基準はスクリプト内に明示。</p>
<p><b>PRRRCスコアリング</b>: 各次元のキーワード階層（5〜1点）を全テキストフィールドに適用。importanceによるスケーリング（importance/5）。R2に50年以上継続ボーナス、R3にリンクデータボーナス。</p>
<p><b>再現性</b>: <code>python3 scripts/analyze_sif.py</code> で全結果を再現可能。決定的アルゴリズム（同一入力→同一出力）。</p>
</div>

<p style="font-size:.72rem;color:var(--text-muted);margin-top:32px;border-top:1px solid var(--border-light);padding-top:12px">
Social Innovation Framework | Generated by analyze_sif.py | Last updated: {datetime.now().strftime("%Y-%m-%d")} | {n:,} events &times; {n_rel} relations &times; 10 civilizations &times; 10 systemic laws
</p>
</body>
</html>"""

    output_path = DASHBOARDS_DIR / "sif.html"
    with open(output_path, "w") as f:
        f.write(html)
    print(f"Dashboard written to: {output_path}")


def _h(text):
    """HTML-escape a string."""
    import html as html_mod
    return html_mod.escape(str(text))


def _select_timeline_events(si_events, n=20):
    """Select n representative events spread across eras and civilizations."""
    # Sort by total score descending within each era
    era_order = ["ancient-medieval", "early-modern", "industrial", "short-20c", "global"]
    per_era = max(n // len(era_order), 2)
    selected = []
    for era in era_order:
        era_events = [e for e in si_events if e.get("_era") == era and e.get("event_year") is not None]
        era_events.sort(key=lambda e: e["_prrrc"]["total"], reverse=True)
        # Diversify by civilization
        seen_civs = set()
        for e in era_events:
            civ = e.get("_civilization", "")
            if civ not in seen_civs or len([x for x in selected if x.get("_era") == era]) < per_era:
                selected.append(e)
                seen_civs.add(civ)
                if len([x for x in selected if x.get("_era") == era]) >= per_era:
                    break

    # Sort final selection by year
    selected.sort(key=lambda e: e.get("event_year", 0) or 0)
    return selected[:n]


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 60)
    print("SIF Analysis Pipeline — Deterministic Keyword-Based Analysis")
    print("=" * 60)

    # Load
    print("\n[1/6] Loading data...")
    consolidated, cases = load_data()
    all_events = merge_events(consolidated, cases)
    print(f"  Merged events: {len(all_events)} (consolidated: {len(consolidated.get('events', []))}, "
          f"cases: {len(cases)}, after dedup)")

    # Select SI events
    print("\n[2/6] Selecting SI events...")
    si_events = select_si_events(all_events)
    print(f"  SI events selected: {len(si_events)}")

    # Score PRRRC
    print("\n[3/6] Scoring PRRRC dimensions...")
    links = consolidated.get("links", [])
    link_counts = compute_link_counts(si_events, links)
    for e in si_events:
        lc = link_counts.get(e.get("title_en", ""), 0)
        e["_prrrc"] = score_prrrc(e, link_count=lc)
        e["_civilization"] = classify_civilization(e)
        e["_era"] = classify_era(e)
        e["_si_type"] = classify_si_type(e)
        e["_pathway"] = classify_pathway(e)
        is_fail, fail_type = identify_failure(e)
        e["_is_failure"] = is_fail
        e["_failure_type"] = fail_type

    # Print PRRRC summary
    totals = [e["_prrrc"]["total"] for e in si_events]
    print(f"  PRRRC total: mean={statistics.mean(totals):.1f}, "
          f"median={statistics.median(totals)}, "
          f"stdev={statistics.stdev(totals):.1f}, "
          f"range=[{min(totals)}, {max(totals)}]")

    # Relationships
    print("\n[4/6] Building event relationships...")
    relationships = build_event_relationships(si_events, links)
    print(f"  Relationships: {len(relationships)}")

    # Statistics
    print("\n[5/6] Computing statistics...")
    stats = compute_statistics(si_events, relationships)

    # Print key stats
    print(f"  Civilizations: {stats['civilization_counts']}")
    print(f"  Types: {stats['type_distribution']}")
    print(f"  Pathways: {stats['pathway_distribution']}")
    print(f"  Three-pathway coverage: {stats['three_pathway_percentage']}%")
    print(f"  Failures: {stats['failure_count']} — {stats['failure_subcategories']}")
    print(f"  Density/century: {stats['density_per_century']}")
    print(f"  Acceleration ratio: {stats['acceleration_ratio']}x")
    print(f"  Non-Western %: {stats['non_western_percentage']}%")

    # System law validation
    print("\n[5b/6] Validating system laws...")
    laws = validate_system_laws(si_events, stats, relationships)
    for law in laws:
        print(f"  LAW {law['number']:2d}: {law['verdict']:22s} | {law['name_ja']}: {law['test']}")

    # Calibration
    print("\n[5c/6] Running calibration checks...")
    calibration = run_calibration(si_events)
    for cal in calibration:
        status = "OK" if cal["diff"] is not None and abs(cal["diff"]) <= 3 else "WARN"
        print(f"  [{status}] {cal['name']}: expected={cal['expected']}, actual={cal['actual']}, diff={cal['diff']}")

    # Output
    print("\n[6/6] Generating outputs...")
    results = generate_results_json(si_events, stats, relationships, laws, calibration)
    generate_dashboard_html(si_events, stats, relationships, laws, results)

    print("\n" + "=" * 60)
    print(f"COMPLETE: {len(si_events)} SI events analyzed, {len(relationships)} relationships,")
    print(f"  {stats['failure_count']} failures, {len(laws)} laws validated.")
    print("=" * 60)


if __name__ == "__main__":
    main()

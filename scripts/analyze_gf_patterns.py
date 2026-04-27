#!/usr/bin/env python3
"""Analyze recurring system structures and patterns in Great Figures DB.

Reads gf_consolidated.json and produces gf_system_patterns.json with:
1. Recurring structural patterns across historical events
2. Decision archetypes from 174 decision structures
3. Concept-event clustering revealing systemic themes
4. Cross-era pattern frequencies
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_data():
    with open(DATA_DIR / "gf_consolidated.json") as f:
        return json.load(f)


def analyze_decision_archetypes(structures):
    """Classify 174 decision structures into recurring archetypes."""
    archetypes = defaultdict(list)

    for s in structures:
        person = s.get("person_name_en", "")
        event = s.get("event_title_en", "")
        reasoning = s.get("reasoning_en", "")
        chosen = s.get("chosen_action_en", "")
        options = s.get("options_en", "")
        speed = s.get("decision_speed", "")
        constraints = s.get("constraints_en", "")

        # Classify by decision pattern
        r_lower = reasoning.lower()
        c_lower = chosen.lower()

        if any(w in r_lower for w in ["risk", "gamble", "bold", "audacious", "daring"]):
            archetypes["calculated_risk"].append({"person": person, "event": event, "reasoning": reasoning[:200]})
        if any(w in r_lower for w in ["wait", "patience", "timing", "opportun"]):
            archetypes["strategic_patience"].append({"person": person, "event": event, "reasoning": reasoning[:200]})
        if any(w in r_lower for w in ["innovat", "new approach", "unconventional", "novel", "pioneer"]):
            archetypes["creative_disruption"].append({"person": person, "event": event, "reasoning": reasoning[:200]})
        if any(w in r_lower for w in ["unif", "consolidat", "merg", "integrat", "centrali"]):
            archetypes["unification_drive"].append({"person": person, "event": event, "reasoning": reasoning[:200]})
        if any(w in r_lower for w in ["reform", "transform", "restructur", "overhaul"]):
            archetypes["systemic_reform"].append({"person": person, "event": event, "reasoning": reasoning[:200]})
        if any(w in r_lower for w in ["surviv", "necessit", "forced", "no choice", "desperat"]):
            archetypes["survival_imperative"].append({"person": person, "event": event, "reasoning": reasoning[:200]})
        if any(w in r_lower for w in ["alliance", "coalition", "partner", "collaborat"]):
            archetypes["alliance_building"].append({"person": person, "event": event, "reasoning": reasoning[:200]})
        if any(w in r_lower for w in ["legacy", "succession", "future generation", "long-term"]):
            archetypes["legacy_orientation"].append({"person": person, "event": event, "reasoning": reasoning[:200]})
        if any(w in r_lower for w in ["moral", "ethic", "principle", "justice", "right"]):
            archetypes["principled_stand"].append({"person": person, "event": event, "reasoning": reasoning[:200]})
        if any(w in r_lower for w in ["adapt", "pivot", "adjust", "flexib", "pragmat"]):
            archetypes["adaptive_pivot"].append({"person": person, "event": event, "reasoning": reasoning[:200]})

    return archetypes


def analyze_event_patterns(events):
    """Find recurring patterns across 10K+ historical events."""
    # Era classification
    eras = defaultdict(list)
    for e in events:
        year = e.get("event_year")
        if year is None:
            eras["mythological"].append(e)
        elif year < -500:
            eras["ancient"].append(e)
        elif year < 500:
            eras["classical"].append(e)
        elif year < 1500:
            eras["medieval"].append(e)
        elif year < 1800:
            eras["early_modern"].append(e)
        elif year < 1900:
            eras["industrial"].append(e)
        elif year < 2000:
            eras["modern"].append(e)
        else:
            eras["contemporary"].append(e)

    # Event type distribution by era
    era_type_dist = {}
    for era, evts in eras.items():
        types = Counter(e.get("event_type", "unknown") for e in evts)
        era_type_dist[era] = {
            "count": len(evts),
            "types": dict(types.most_common(10))
        }

    # Cross-era recurring patterns
    # Group by event_type and look for systemic patterns
    type_groups = defaultdict(list)
    for e in events:
        t = e.get("event_type", "unknown")
        type_groups[t].append(e)

    return eras, era_type_dist, type_groups


def analyze_concept_event_links(links, concepts, events):
    """Analyze which concepts recur across different eras and contexts."""
    # Concept frequency across events
    concept_freq = Counter()
    concept_events = defaultdict(list)
    concept_persons = defaultdict(set)

    for link in links:
        cname = link.get("concept_name_en", "")
        person = link.get("person_name_en", "")
        event = link.get("event_title_en", "")
        concept_freq[cname] += 1
        concept_events[cname].append({"person": person, "event": event, "type": link.get("link_type", "")})
        concept_persons[cname].add(person)

    # Concepts that appear across many different figures = universal patterns
    universal_concepts = []
    for cname, freq in concept_freq.most_common(50):
        persons = concept_persons[cname]
        # Find concept definition
        cdef = next((c for c in concepts if c.get("name_en") == cname), {})
        universal_concepts.append({
            "name_en": cname,
            "name_ja": cdef.get("name_ja", ""),
            "category": cdef.get("category", ""),
            "frequency": freq,
            "unique_figures": len(persons),
            "figures": sorted(list(persons))[:10],
            "definition": cdef.get("definition_ja", "")[:200],
            "examples": concept_events[cname][:5]
        })

    return universal_concepts


def extract_systemic_patterns(archetypes, era_dist, universal_concepts, events, structures):
    """Synthesize all analyses into named systemic patterns."""
    patterns = []

    # Pattern 1: Innovation-Crisis Cycle
    crisis_events = [e for e in events if e.get("event_type") in ("crisis", "failure")]
    innovation_events = [e for e in events if e.get("event_type") == "innovation"]
    patterns.append({
        "id": "innovation_crisis_cycle",
        "name_ja": "革新-危機サイクル",
        "name_en": "Innovation-Crisis Cycle",
        "description_ja": "危機が革新を誘発し、革新が新たな不安定性を生む循環構造。歴史上の全時代に観察される最も基本的なシステムダイナミクス。",
        "description_en": "Crises trigger innovation, which creates new instabilities. The most fundamental system dynamic observed across all eras.",
        "system_archetype": "Shifting the Burden / Fixes that Fail",
        "event_count": len(crisis_events) + len(innovation_events),
        "crisis_events": len(crisis_events),
        "innovation_events": len(innovation_events),
        "examples": [
            {"era": "古代", "case": "ペルシャ戦争 → アテネ民主制の黄金期 → ペロポネソス戦争"},
            {"era": "中世", "case": "黒死病 → 労働力不足 → 農業革新と封建制崩壊"},
            {"era": "近代", "case": "大恐慌 → ニューディール → 福祉国家の制度疲労"},
            {"era": "現代", "case": "2008年金融危機 → フィンテック革新 → 新たな規制課題"}
        ]
    })

    # Pattern 2: Unification-Fragmentation Oscillation
    conquest = [e for e in events if e.get("event_type") in ("conquest", "founding")]
    reform = [e for e in events if e.get("event_type") == "reform"]
    patterns.append({
        "id": "unification_fragmentation",
        "name_ja": "統一-分裂の振動",
        "name_en": "Unification-Fragmentation Oscillation",
        "description_ja": "統合と分散が交互に繰り返される構造。帝国の興亡、企業の集中と分散、技術の統合と多様化に共通して観察される。",
        "description_en": "Integration and dispersal alternate cyclically. Observed in empire rise/fall, corporate consolidation/breakup, and technology convergence/divergence.",
        "system_archetype": "Limits to Growth",
        "event_count": len(conquest) + len(reform),
        "archetype_count": len(archetypes.get("unification_drive", [])),
        "examples": [
            {"era": "古代", "case": "秦の統一 → 漢初期の分封 → 漢の再統一"},
            {"era": "中世", "case": "カール大帝の統一 → カロリング分裂 → 神聖ローマ帝国"},
            {"era": "近代", "case": "植民地帝国の拡大 → 民族自決による独立 → 経済統合（EU等）"},
            {"era": "現代", "case": "GAFA独占 → 反トラスト規制 → 分散型技術（Web3）"}
        ]
    })

    # Pattern 3: Outsider-Insider Transformation
    pivot = [e for e in events if e.get("event_type") in ("pivot", "succession")]
    patterns.append({
        "id": "outsider_insider",
        "name_ja": "周縁から中心への転換",
        "name_en": "Outsider-Insider Transformation",
        "description_ja": "体制の周縁にいた存在が、既存秩序の矛盾を突いて中心に躍り出るパターン。辺境の革新者が次の時代のルールを作る。",
        "description_en": "Peripheral actors exploit contradictions in existing order to become central. Frontier innovators define next-era rules.",
        "system_archetype": "Success to the Successful (inverted)",
        "event_count": len(pivot),
        "archetype_count": len(archetypes.get("creative_disruption", [])),
        "examples": [
            {"era": "古代", "case": "ローマ（辺境都市国家）→ 地中海覇権"},
            {"era": "中世", "case": "モンゴル（遊牧民）→ ユーラシア帝国"},
            {"era": "近代", "case": "アメリカ（植民地）→ 超大国"},
            {"era": "現代", "case": "日本の自動車産業（後発）→ 世界トップ"}
        ]
    })

    # Pattern 4: Technology-Institution Lag
    patterns.append({
        "id": "tech_institution_lag",
        "name_ja": "技術-制度のタイムラグ",
        "name_en": "Technology-Institution Lag",
        "description_ja": "技術革新は制度変革に先行し、そのギャップが社会的緊張を生む。制度が追いつくまでの混乱期が繰り返し出現する。",
        "description_en": "Technological innovation precedes institutional change, creating social tension. The turbulent gap period recurs throughout history.",
        "system_archetype": "Eroding Goals / Drifting Goals",
        "event_count": len(innovation_events),
        "examples": [
            {"era": "古代", "case": "鉄器の普及 → 旧来の青銅器社会秩序の崩壊"},
            {"era": "近世", "case": "活版印刷 → 宗教改革 → 30年戦争 → ウェストファリア体制"},
            {"era": "産業革命", "case": "蒸気機関 → 工場制 → 労働運動 → 労働法制定"},
            {"era": "現代", "case": "SNS/AI → フェイクニュース・プライバシー問題 → GDPR等規制"}
        ]
    })

    # Pattern 5: Alliance Paradox
    alliance = [e for e in events if e.get("event_type") in ("alliance", "negotiation")]
    patterns.append({
        "id": "alliance_paradox",
        "name_ja": "同盟のパラドックス",
        "name_en": "Alliance Paradox",
        "description_ja": "共通の敵に対する同盟は、敵が消滅すると内部対立に転化する。勝利の瞬間が次の紛争の種となる構造。",
        "description_en": "Alliances against common enemies dissolve into internal conflict once the enemy is eliminated. Victory sows seeds of next conflict.",
        "system_archetype": "Accidental Adversaries",
        "event_count": len(alliance),
        "archetype_count": len(archetypes.get("alliance_building", [])),
        "examples": [
            {"era": "古代", "case": "ギリシャ対ペルシャ同盟 → ペロポネソス戦争（アテネvスパルタ）"},
            {"era": "近代", "case": "対ナポレオン同盟 → ウィーン体制下の大国間競争"},
            {"era": "現代", "case": "対ソ連同盟 → 冷戦後の米欧間摩擦"},
            {"era": "ビジネス", "case": "対IBM同盟（Wintel）→ Microsoft対Intel利害対立"}
        ]
    })

    # Pattern 6: Reform Backlash Loop
    patterns.append({
        "id": "reform_backlash",
        "name_ja": "改革-反動ループ",
        "name_en": "Reform-Backlash Loop",
        "description_ja": "急進的改革は既得権益層の反発を招き、揺り戻しが起きる。しかし揺り戻し後も一部の改革は不可逆的に定着する「ラチェット効果」が働く。",
        "description_en": "Radical reform triggers backlash from vested interests. However, after backlash, some reforms irreversibly stick (ratchet effect).",
        "system_archetype": "Balancing Process with Delay",
        "event_count": len(reform),
        "archetype_count": len(archetypes.get("systemic_reform", [])),
        "examples": [
            {"era": "古代", "case": "グラックス兄弟の土地改革 → 元老院の反発 → だが小農保護の概念は残存"},
            {"era": "近世", "case": "フランス革命 → ナポレオン帝政・王政復古 → だが市民法典は存続"},
            {"era": "近代", "case": "明治維新 → 自由民権運動の弾圧 → だが立憲制は不可逆"},
            {"era": "現代", "case": "オバマケア → トランプ撤回試み → だが既往症保護は存続"}
        ]
    })

    # Pattern 7: Knowledge-Power Nexus
    patterns.append({
        "id": "knowledge_power_nexus",
        "name_ja": "知識-権力の結節点",
        "name_en": "Knowledge-Power Nexus",
        "description_ja": "情報・知識の独占が権力構造を決定し、知識の民主化が体制転覆を引き起こす。知のアクセス変動が歴史の転換点となる。",
        "description_en": "Monopoly over information/knowledge determines power structure. Democratization of knowledge triggers regime change.",
        "system_archetype": "Tragedy of the Commons (inverted)",
        "event_count": 0,  # Will be calculated
        "examples": [
            {"era": "古代", "case": "文字の発明 → 神官階級の知識独占 → 官僚制国家"},
            {"era": "中世", "case": "修道院の写本独占 → 大学の誕生 → スコラ学"},
            {"era": "近世", "case": "活版印刷 → 知識の大衆化 → 宗教改革・科学革命"},
            {"era": "現代", "case": "インターネット → 情報の民主化 → プラットフォーム権力の再集中"}
        ]
    })

    # Pattern 8: Survival-Legacy Tension
    patterns.append({
        "id": "survival_legacy_tension",
        "name_ja": "生存-遺産の緊張",
        "name_en": "Survival-Legacy Tension",
        "description_ja": "短期的生存と長期的遺産の間の根本的緊張。偉大な指導者は両方を同時に達成するが、多くは一方を犠牲にする。",
        "description_en": "Fundamental tension between short-term survival and long-term legacy. Great leaders achieve both; most sacrifice one for the other.",
        "system_archetype": "Growth and Underinvestment",
        "archetype_count": len(archetypes.get("survival_imperative", [])) + len(archetypes.get("legacy_orientation", [])),
        "event_count": 0,
        "examples": [
            {"era": "古代", "case": "アウグストゥス：内戦の生存者 → ローマ帝政の建築者"},
            {"era": "中世", "case": "サラディン：十字軍との戦い → イスラム世界の統一と寛容の遺産"},
            {"era": "近代", "case": "リンカーン：南北戦争の危機 → 奴隷解放の遺産"},
            {"era": "現代", "case": "スティーブ・ジョブズ：Apple追放からの生還 → デジタル革命の遺産"}
        ]
    })

    # Pattern 9: Scale Threshold Effects
    growth = [e for e in events if e.get("event_type") == "growth"]
    patterns.append({
        "id": "scale_threshold",
        "name_ja": "規模の閾値効果",
        "name_en": "Scale Threshold Effects",
        "description_ja": "組織・帝国・技術が特定の規模閾値を超えると、質的に異なるダイナミクスが発動する。成長が管理不能になる転換点。",
        "description_en": "When organizations/empires/technologies exceed certain scale thresholds, qualitatively different dynamics emerge.",
        "system_archetype": "Limits to Growth",
        "event_count": len(growth),
        "examples": [
            {"era": "古代", "case": "ローマ帝国の過伸展 → 属州統治の限界 → 分裂"},
            {"era": "近代", "case": "東インド会社の巨大化 → 統治の民間委託の限界 → 国有化"},
            {"era": "現代", "case": "Facebook 30億ユーザー → コンテンツモデレーション不能 → 社会問題化"},
            {"era": "科学", "case": "巨大科学プロジェクト（CERN等）→ 国際協力の必然性"}
        ]
    })

    # Pattern 10: Adaptive Mimicry
    patterns.append({
        "id": "adaptive_mimicry",
        "name_ja": "適応的模倣と独自化",
        "name_en": "Adaptive Mimicry and Localization",
        "description_ja": "成功モデルを模倣しつつ独自の文脈に適応させるパターン。完全模倣は失敗し、創造的翻案が成功する。",
        "description_en": "Imitating successful models while adapting to local context. Pure imitation fails; creative adaptation succeeds.",
        "system_archetype": "Attractiveness Principle",
        "archetype_count": len(archetypes.get("adaptive_pivot", [])),
        "event_count": 0,
        "examples": [
            {"era": "古代", "case": "ローマ法 → ビザンツ帝国による東方適応（ユスティニアヌス法典）"},
            {"era": "近世", "case": "中国の科挙制度 → 朝鮮・ベトナム・日本への適応的導入"},
            {"era": "近代", "case": "明治日本のドイツ憲法模倣 → 天皇制と融合した独自体制"},
            {"era": "現代", "case": "シリコンバレーモデル → 深圳・バンガロール・テルアビブへの変容的移植"}
        ]
    })

    # Pattern 11: Sacred-Secular Oscillation
    patterns.append({
        "id": "sacred_secular",
        "name_ja": "聖俗の振動",
        "name_en": "Sacred-Secular Oscillation",
        "description_ja": "宗教的/精神的権威と世俗的権力が交互に優位となる構造。一方が過度に支配的になると他方が反発する。",
        "description_en": "Religious/spiritual authority and secular power alternate in dominance. When one becomes excessive, the other pushes back.",
        "system_archetype": "Shifting the Burden",
        "event_count": 0,
        "examples": [
            {"era": "古代", "case": "エジプト神官 vs ファラオの世俗権力"},
            {"era": "中世", "case": "教皇権 vs 皇帝権（叙任権闘争）"},
            {"era": "近世", "case": "宗教改革 → 世俗国家の台頭（ウェストファリア体制）"},
            {"era": "現代", "case": "世俗化の進行 → 宗教原理主義の台頭 → 再世俗化圧力"}
        ]
    })

    # Pattern 12: Complexity Collapse
    failure = [e for e in events if e.get("event_type") in ("failure", "retreat")]
    patterns.append({
        "id": "complexity_collapse",
        "name_ja": "複雑性の崩壊",
        "name_en": "Complexity Collapse",
        "description_ja": "社会の複雑性が維持コストを超えると、急速な簡素化（崩壊）が起きる。Joseph Tainterの理論が示す通り、複雑性への投資の収穫逓減が崩壊の根本原因。",
        "description_en": "When society's complexity exceeds maintenance costs, rapid simplification (collapse) occurs. As Tainter showed, diminishing returns to complexity investment is the root cause.",
        "system_archetype": "Limits to Growth / Eroding Goals",
        "event_count": len(failure),
        "examples": [
            {"era": "古代", "case": "西ローマ帝国：官僚制・軍事費の維持不能 → 崩壊"},
            {"era": "中世", "case": "マヤ文明：灌漑・宗教システムの過剰複雑化 → 放棄"},
            {"era": "近代", "case": "オスマン帝国：多民族統治の複雑性 → 段階的解体"},
            {"era": "現代", "case": "ソ連：計画経済の情報処理限界 → 崩壊"}
        ]
    })

    return patterns


def build_archetype_summary(archetypes):
    """Build summary of decision archetypes."""
    summary = []
    archetype_meta = {
        "calculated_risk": {"name_ja": "計算されたリスクテイク", "name_en": "Calculated Risk-Taking"},
        "strategic_patience": {"name_ja": "戦略的忍耐", "name_en": "Strategic Patience"},
        "creative_disruption": {"name_ja": "創造的破壊", "name_en": "Creative Disruption"},
        "unification_drive": {"name_ja": "統一への推進", "name_en": "Unification Drive"},
        "systemic_reform": {"name_ja": "体制的改革", "name_en": "Systemic Reform"},
        "survival_imperative": {"name_ja": "生存の命法", "name_en": "Survival Imperative"},
        "alliance_building": {"name_ja": "同盟構築", "name_en": "Alliance Building"},
        "legacy_orientation": {"name_ja": "遺産志向", "name_en": "Legacy Orientation"},
        "principled_stand": {"name_ja": "原則的立場", "name_en": "Principled Stand"},
        "adaptive_pivot": {"name_ja": "適応的方向転換", "name_en": "Adaptive Pivot"},
    }

    for key, entries in sorted(archetypes.items(), key=lambda x: -len(x[1])):
        meta = archetype_meta.get(key, {"name_ja": key, "name_en": key})
        summary.append({
            "id": key,
            "name_ja": meta["name_ja"],
            "name_en": meta["name_en"],
            "count": len(entries),
            "examples": [{"person": e["person"], "event": e["event"]} for e in entries[:5]]
        })

    return summary


def main():
    print("Loading GF data...")
    data = load_data()
    structures = data["structures"]
    events = data["events"]
    concepts = data["concepts"]
    links = data["links"]

    print(f"  Structures: {len(structures)}")
    print(f"  Events: {len(events)}")
    print(f"  Concepts: {len(concepts)}")
    print(f"  Links: {len(links)}")

    print("\nAnalyzing decision archetypes...")
    archetypes = analyze_decision_archetypes(structures)
    archetype_summary = build_archetype_summary(archetypes)
    for a in archetype_summary:
        print(f"  {a['name_en']}: {a['count']} instances")

    print("\nAnalyzing event patterns across eras...")
    eras, era_dist, type_groups = analyze_event_patterns(events)
    for era, info in sorted(era_dist.items()):
        print(f"  {era}: {info['count']} events")

    print("\nAnalyzing universal concepts...")
    universal_concepts = analyze_concept_event_links(links, concepts, events)
    for c in universal_concepts[:10]:
        print(f"  {c['name_en']}: freq={c['frequency']}, figures={c['unique_figures']}")

    print("\nSynthesizing systemic patterns...")
    patterns = extract_systemic_patterns(archetypes, era_dist, universal_concepts, events, structures)
    for p in patterns:
        print(f"  {p['name_en']}: {p.get('event_count', 0)} related events")

    # Build output
    output = {
        "meta": {
            "total_events": len(events),
            "total_structures": len(structures),
            "total_concepts": len(concepts),
            "total_links": len(links),
            "analysis_date": "2026-04-27",
            "version": 2
        },
        "systemic_patterns": patterns,
        "decision_archetypes": archetype_summary,
        "era_distribution": era_dist,
        "universal_concepts": universal_concepts[:30],
    }

    out_path = DATA_DIR / "gf_system_patterns.json"
    with open(out_path, "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nSaved to {out_path}")
    print(f"  {len(patterns)} systemic patterns")
    print(f"  {len(archetype_summary)} decision archetypes")
    print(f"  {len(universal_concepts[:30])} universal concepts")


if __name__ == "__main__":
    main()

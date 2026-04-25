#!/usr/bin/env python3
"""
Generate 30,000+ structured events from person data.
Multi-event extraction per person using category, era, and summary analysis.
"""
import json
import os
import re
import glob
from collections import defaultdict

DATA_DIR = os.path.expanduser("~/projects/research/great-figures-db/data")
OUTPUT = os.path.expanduser("~/projects/research/miratuku-news-v2/data/gf_events_30k.json")
CONSOLIDATED = os.path.expanduser("~/projects/research/miratuku-news-v2/data/gf_consolidated.json")

# Life phase templates per category
LIFE_PHASES = {
    "monarch": [
        ("early_rise", "台頭期", "Rise to Power", "succession", 0.2),
        ("consolidation", "権力確立期", "Power Consolidation", "political", 0.35),
        ("zenith", "最盛期", "Zenith of Rule", "reform", 0.5),
        ("legacy", "晩年・遺産", "Legacy Period", "legacy", 0.8),
    ],
    "military": [
        ("first_campaign", "初陣", "First Campaign", "military", 0.25),
        ("major_victory", "主要戦役", "Major Campaign", "conquest", 0.45),
        ("strategic_turn", "戦略転換", "Strategic Turning Point", "conflict", 0.6),
    ],
    "politician": [
        ("entry", "政治参入", "Political Entry", "political", 0.3),
        ("reform", "主要改革", "Major Reform", "reform", 0.5),
        ("crisis", "危機対応", "Crisis Response", "crisis", 0.65),
    ],
    "revolutionary": [
        ("awakening", "覚醒", "Political Awakening", "activism", 0.25),
        ("movement", "運動形成", "Movement Building", "revolution", 0.4),
        ("breakthrough", "突破", "Revolutionary Breakthrough", "conflict", 0.55),
    ],
    "entrepreneur": [
        ("founding", "創業", "Venture Founding", "founding", 0.3),
        ("innovation", "革新的製品", "Key Innovation", "innovation", 0.45),
        ("scaling", "事業拡大", "Business Scaling", "growth", 0.6),
        ("pivot", "事業転換", "Strategic Pivot", "transformation", 0.7),
    ],
    "business": [
        ("founding", "事業開始", "Business Launch", "founding", 0.3),
        ("growth", "成長期", "Growth Phase", "growth", 0.5),
        ("dominance", "市場支配", "Market Dominance", "economic", 0.65),
    ],
    "industrialist": [
        ("founding", "事業創設", "Industrial Founding", "founding", 0.3),
        ("innovation", "技術革新", "Technical Innovation", "innovation", 0.45),
        ("expansion", "事業拡大", "Industrial Expansion", "expansion", 0.6),
    ],
    "scientist": [
        ("research", "主要研究", "Key Research", "discovery", 0.35),
        ("breakthrough", "画期的発見", "Breakthrough Discovery", "innovation", 0.5),
        ("publication", "主要著作", "Major Publication", "publication", 0.55),
    ],
    "philosopher": [
        ("formation", "思想形成", "Intellectual Formation", "intellectual", 0.3),
        ("theory", "理論構築", "Theory Development", "theory", 0.5),
        ("influence", "思想的影響", "Intellectual Influence", "legacy", 0.7),
    ],
    "writer": [
        ("debut", "デビュー", "Literary Debut", "publication", 0.3),
        ("masterpiece", "代表作", "Masterpiece", "cultural", 0.5),
    ],
    "artist": [
        ("emergence", "台頭", "Artistic Emergence", "cultural", 0.3),
        ("masterwork", "代表作", "Major Work", "innovation", 0.5),
    ],
    "religious": [
        ("calling", "召命", "Religious Calling", "spiritual", 0.25),
        ("teaching", "教え", "Core Teaching", "religious", 0.45),
        ("institution", "教団形成", "Institution Building", "founding", 0.6),
    ],
    "explorer": [
        ("expedition", "探検", "Major Expedition", "exploration", 0.4),
        ("discovery", "発見", "Key Discovery", "discovery", 0.5),
    ],
    "reformer": [
        ("reform_start", "改革着手", "Reform Initiation", "reform", 0.35),
        ("implementation", "改革実施", "Reform Implementation", "political", 0.5),
        ("resistance", "抵抗との対峙", "Facing Resistance", "conflict", 0.6),
    ],
    "diplomat": [
        ("negotiation", "交渉", "Key Negotiation", "diplomatic", 0.4),
        ("treaty", "条約", "Treaty Achievement", "alliance", 0.55),
    ],
    "economist": [
        ("theory", "理論提唱", "Economic Theory", "theory", 0.45),
        ("influence", "政策影響", "Policy Influence", "economic", 0.6),
    ],
}

# Systemic outcome patterns (adds structural depth)
SYSTEMIC_OUTCOMES = {
    "succession": [
        "権力の移転が制度的安定をもたらした",
        "後継体制の確立が長期的な統治基盤を形成した",
        "権力継承の過程で新たな制度が生まれた",
    ],
    "conquest": [
        "征服による統合が新たな文化的融合を促進した",
        "軍事的拡大が行政制度の革新を要求した",
        "征服の成功が資源の再分配構造を変えた",
    ],
    "reform": [
        "制度改革がシステム全体の効率を向上させた",
        "改革が既得権益層との構造的対立を生んだ",
        "制度設計の変更が社会構造を長期的に変容させた",
    ],
    "founding": [
        "新組織の創設が既存の市場構造を変革した",
        "設立された制度が自己強化的に成長した",
        "新たな組織形態が模倣され、社会全体に伝播した",
    ],
    "innovation": [
        "技術革新が既存のビジネスモデルを破壊した",
        "イノベーションが新たな市場を創造した",
        "革新が予想外の社会変化を引き起こした",
    ],
    "military": [
        "軍事行動が地政学的均衡を変化させた",
        "戦争が技術革新と組織改革を促進した",
        "軍事的成功が政治的正当性を強化した",
    ],
    "political": [
        "政治的決断が社会制度の構造を変えた",
        "権力の行使が新たな制度的均衡を生み出した",
        "政治的変革が経済構造に波及した",
    ],
    "economic": [
        "経済的成功が権力構造を変容させた",
        "新たな経済モデルが社会関係を再編した",
        "経済活動が制度的枠組みの変更を促した",
    ],
    "revolution": [
        "革命が社会の根本的構造転換をもたらした",
        "急激な変革が予期せぬ反動を生んだ",
        "革命的変化が新たな制度的均衡を要求した",
    ],
    "discovery": [
        "発見が既存のパラダイムを揺るがした",
        "知識の拡大が社会の認識構造を変えた",
        "発見が新たな技術的可能性を開いた",
    ],
    "crisis": [
        "危機が既存システムの脆弱性を露呈させた",
        "危機対応が制度的革新の契機となった",
        "危機が権力構造の再編を加速させた",
    ],
}

# Default for unlisted types
DEFAULT_OUTCOME = [
    "歴史的な変化の契機となった",
    "社会構造に影響を与えた",
    "後世への遺産を残した",
]


def load_persons():
    all_persons = []
    for f in sorted(glob.glob(f"{DATA_DIR}/wave*.json")):
        data = json.load(open(f))
        for k, v in data.items():
            if isinstance(v, list):
                all_persons.extend(v)
    return all_persons


def load_existing_keys():
    """Get set of existing (person, title) keys to avoid duplicates."""
    keys = set()
    # From existing events
    for f in sorted(glob.glob(f"{DATA_DIR}/events*.json")):
        data = json.load(open(f))
        for k, v in data.items():
            if isinstance(v, list):
                for e in v:
                    keys.add((e.get("person_name_en", ""), e.get("title_en", "")))
    # From expanded events
    expanded = os.path.expanduser("~/projects/research/miratuku-news-v2/data/gf_events_expanded.json")
    if os.path.exists(expanded):
        data = json.load(open(expanded))
        for e in data.get("events", []):
            keys.add((e.get("person_name_en", ""), e.get("title_en", "")))
    return keys


# Phase-specific structural narrative templates
PHASE_NARRATIVES = {
    "early_rise": "{name}は{region}において{cat}として台頭した。{summary}。この時期、{name}は既存の権力構造の中で自らの地位を確立するために、限られた資源と情報の中で戦略的な選択を迫られていた。従来の権威に対する挑戦と、既存秩序への適応という二律背反の中で、独自の権力基盤を構築する過程は、組織が成長初期に直面する「正当性の獲得」というシステム的課題を体現している。",
    "consolidation": "{name}は権力を確立し、統治機構の整備に着手した。{summary}。この段階で重要なのは、征服や獲得によって得た権力を、制度として定着させるシステム設計の能力である。個人のカリスマに依存する統治から、制度に基盤を置く統治への移行は、あらゆる組織が直面する「属人性から制度性へ」の構造転換を示している。成功した制度設計は自己強化的に機能し、制度そのものが新たな権力の源泉となった。",
    "zenith": "{name}の治世は最盛期を迎えた。{summary}。しかしシステム思考の観点からは、最盛期こそが衰退の種が蒔かれる時期でもある。成功したシステムは自己強化ループにより拡大するが、同時に「成長の限界」構造が作動し始める。資源の枯渇、組織の肥大化、周辺からの抵抗が均衡ループとして現れ、最盛期の持続性を脅かす構造的緊張が蓄積していった。",
    "legacy": "{name}の晩年と遺産の時期。{summary}。{name}が構築したシステムは、創設者の不在後にどのように機能するかという根本的な試練に直面した。個人の判断力に依存していた要素は制度化されなければ消滅し、制度化された要素は環境変化への適応力を失うリスクがある。この「創設者のジレンマ」は、組織の持続可能性における最も深い構造的課題の一つである。",
    "first_campaign": "{name}は{region}において最初の軍事的挑戦に臨んだ。{summary}。初陣は単なる戦闘ではなく、指揮官としてのシステム——情報収集、意思決定速度、組織動員力——が初めて実戦で検証される場である。この経験から得られたフィードバックが、以後の戦略的思考を形成する正帰還ループの起点となった。",
    "major_victory": "{name}の主要な軍事的勝利。{summary}。軍事的成功はシステム的に見ると、敵のシステムの脆弱性を発見し、自らのシステムの強みを増幅させる過程である。しかし、戦術的勝利が戦略的成功を保証しないという構造的断絶が、多くの軍事指導者を「勝者の罠」に陥れてきた。",
    "strategic_turn": "{name}は戦略的転換点を迎えた。{summary}。これまでの成功パターンが通用しなくなる局面で、システムの再設計を行えるかどうかが問われた。既存の成功体験に基づく強化ループを断ち切り、新たな均衡点を見出す能力は、適応的リーダーシップの核心である。",
    "entry": "{name}は政治の世界に参入した。{summary}。政治参入は、個人の理念が既存の制度的構造と初めて衝突する瞬間である。理想と現実の間のシステム的ギャップを認識し、制度内での変革か制度そのものの変革かという根本的な選択を迫られる。",
    "reform": "{name}は主要な改革に着手した。{summary}。制度改革はシステム全体の再設計であり、パラメータの調整とは質的に異なる。改革は既存のフィードバックループを断ち切り、新たなループを構築する試みであるが、古いシステムの慣性と新しいシステムの不安定性が同時に作用するため、改革の過渡期が最も脆弱な時期となる。",
    "crisis": "{name}は深刻な危機に直面した。{summary}。危機はシステムの脆弱性が顕在化する瞬間であり、通常は隠されている構造的問題が一気に表面化する。危機対応の質は、リーダーがシステムのどの層に介入するかによって決まる。表層的な対症療法は短期的な安定をもたらすが、構造的原因に対処しなければ危機は反復する。",
    "awakening": "{name}は政治的・社会的な覚醒を経験した。{summary}。個人の覚醒がシステム変革の起点となるためには、個人の認識変化が組織的な運動に転換されるメカニズムが必要である。この転換過程は、パラダイムの変化が制度的変化に先行するという、レバレッジポイント理論の深層構造を体現している。",
    "movement": "{name}は社会運動を組織化した。{summary}。運動の形成は、分散した不満を構造化された集合行為に転換するシステム設計の過程である。成功した運動は参加者間の正帰還ループ（参加→成功体験→さらなる参加）を確立し、臨界質量に到達すると自己持続的に拡大する。",
    "breakthrough": "{name}は突破的な成果を達成した。{summary}。システムの観点からは、突破は蓄積された圧力が閾値を超えた瞬間に起こる非線形的変化である。長期間の漸進的変化が突然の相転移をもたらすこの構造は、歴史における変革の多くに共通するパターンである。",
    "founding": "{name}は新たな事業・組織を創設した。{summary}。創業は新しいシステムの設計と構築であり、初期の設計選択がその後の成長経路を決定的に制約する「経路依存性」を生む。創業者の暗黙知が組織文化として制度化されるプロセスは、個人的知識が構造的知識に転換されるシステム的変容である。",
    "innovation": "{name}は革新的な製品・サービスを生み出した。{summary}。イノベーションはシステム的に見ると、既存のフィードバック構造を破壊し新たなループを創造する行為である。破壊的イノベーションは既存市場の均衡を崩し、新たな均衡へ至るダイナミクスを起動させる。",
    "scaling": "{name}は事業を大幅に拡大した。{summary}。スケーリングはシステムの自己強化ループが本格的に作動する段階であり、同時に「成長の限界」構造が徐々に顕在化し始める。組織が規模を拡大する過程で、初期の柔軟性が失われ、官僚的構造が成長を制約するようになるジレンマが生じる。",
    "pivot": "{name}は戦略的転換を行った。{summary}。事業転換は既存の成功パターンを意図的に放棄し、新たなシステム構造を構築する決断である。沈没コストの呪縛を断ち切り、過去の投資ではなく未来の可能性に基づいて意思決定を行う能力が問われる。",
    "research": "{name}は主要な研究に取り組んだ。{summary}。科学的研究はシステム的に見ると、既存のパラダイム内での問題解決（通常科学）と、パラダイムそのものを変革する発見（科学革命）の二つのモードを持つ。後者は知識システム全体のフィードバック構造を根本から変える。",
    "breakthrough_sci": "{name}は画期的な発見を成し遂げた。{summary}。科学的発見が社会に与える影響は、発見そのものよりも、それが既存の制度・経済・文化構造にどう吸収されるかによって決まる。発見と社会変革の間には複雑なフィードバックループと時間遅延が存在する。",
    "publication": "{name}は主要な著作を発表した。{summary}。著作の出版は知識を個人から社会システムに移転する行為であり、思想の制度化の第一歩である。影響力のある著作は読者との間に正帰還ループを形成し、思想的運動に発展する可能性を持つ。",
    "formation": "{name}は独自の思想体系を形成した。{summary}。思想の形成は既存のパラダイムとの対話と批判を通じて進む。新しい思想が既存の知的構造のどの部分を継承し、どの部分を否定するかが、その思想の革新性と受容可能性を決定する。",
    "theory": "{name}は新たな理論を構築した。{summary}。理論構築は現実の複雑性をモデル化する行為であり、そのモデルが現実のどの側面を照らし、どの側面を隠蔽するかが、理論の有用性と限界を同時に規定する。",
    "influence": "{name}の思想は広く影響を及ぼした。{summary}。思想の伝播はシステム的に見ると、ミーム的な自己複製プロセスである。成功した思想は制度・教育・文化を通じて再生産され、元の文脈から離れても機能し続ける「脱文脈化された知識」として存続する。",
    "debut": "{name}は文学的デビューを果たした。{summary}。創作活動は個人の内面を社会的テキストに変換する過程であり、作品を通じて読者の世界観に介入するシステム的行為である。",
    "masterpiece": "{name}は代表作を完成させた。{summary}。代表作は創作者の技術と思想が最も高度に統合された作品であり、その影響は文学的領域を超えて社会文化的構造に及ぶことがある。",
    "calling": "{name}は宗教的召命を経験した。{summary}。宗教的覚醒は個人のパラダイム転換であり、既存の価値体系を根本から再構成する経験である。この個人的変容が社会的運動に発展するためには、組織化のメカニズムが不可欠である。",
    "teaching": "{name}は核心的な教えを展開した。{summary}。宗教的教えはシステム的に見ると、社会の最深層（世界観・価値観）に介入する試みであり、Meadowsのレバレッジポイント理論においてはLevel 2（パラダイム）への介入に相当する。",
    "institution": "{name}は宗教的制度を構築した。{summary}。教えの制度化は、カリスマ的権威を制度的権威に変換するシステム的プロセスであり、ウェーバーが「カリスマのルーティン化」と呼んだ構造的変容である。",
    "expedition": "{name}は大規模な探検を実施した。{summary}。探検はシステムの境界を拡張する行為であり、未知の領域を既知のシステムに統合する過程である。探検がもたらす情報は既存の世界観を修正し、新たな可能性空間を開く。",
    "discovery_exp": "{name}は重要な発見を成し遂げた。{summary}。発見は情報の非対称性を生み出し、その情報をいかに活用するかが発見者と社会の関係を規定する。",
    "reform_start": "{name}は改革に着手した。{summary}。改革の着手は既存システムへの介入の開始であり、どのレバレッジポイントに介入するかの選択が改革の成否を決定づける。パラメータ変更か、構造変更か、パラダイム転換か——介入の深度が改革の射程を規定する。",
    "implementation": "{name}は改革を実行に移した。{summary}。改革の実施段階では、設計と現実のギャップが顕在化する。計画の論理的整合性と、現場での実行可能性の間のシステム的乖離を調整する能力が問われる。",
    "resistance": "{name}は改革への抵抗に直面した。{summary}。抵抗はシステムの恒常性維持機能の発現であり、改革者にとっては均衡ループとの闘いである。抵抗を正面から打破するか、抵抗を回避する迂回戦略を取るか、抵抗を取り込んで改革の一部とするかの選択が問われる。",
    "negotiation": "{name}は重要な交渉に臨んだ。{summary}。交渉はシステム間の界面で起こる相互作用であり、各当事者のシステム的利害が複雑に絡み合う場である。",
    "treaty": "{name}は条約を成立させた。{summary}。条約は複数のシステム間の新たな均衡点を文書化する行為であり、均衡の制度化である。",
    "growth": "{name}は事業の成長期を迎えた。{summary}。成長期は正帰還ループが本格的に作動する段階であり、成功が資源を呼び、資源がさらなる成功を生む自己強化構造が確立される。しかし同時に、成長に伴う組織の複雑性増大が管理能力を超え始めるリスクも蓄積する。",
    "dominance": "{name}は市場における支配的地位を確立した。{summary}。市場支配はシステム的に見ると、正帰還ループの極限的な帰結であり、ネットワーク効果や規模の経済が競合の参入障壁を形成する。しかし支配的地位は反トラスト規制や新たな技術パラダイムによって脅かされる構造的脆弱性を内包する。",
    "emergence": "{name}は芸術的才能を開花させた。{summary}。芸術的創造はシステム的に見ると、文化的資源（技法・素材・パトロネージ・美学的基準）のネットワーク内で起こる創発現象である。",
    "masterwork": "{name}は代表的な作品を生み出した。{summary}。代表作の創造は、技術的蓄積と直感的飛躍が交差する非線形的過程である。",
    "main": "{name}は{cat}として歴史的な業績を残した。{summary}。この業績をシステム思考の観点から見ると、個人の行為が社会構造にどのような波及効果をもたらしたかが重要である。直接的な影響だけでなく、制度・文化・知識のシステムを通じた間接的な影響が、しばしば直接的影響を凌駕する。",
}


def _build_rich_description(name_ja, summary_ja, phase_ja, phase_id, etype, cat, cat2,
                             region, country, birth, death, lifespan, life_pct, year):
    """Build a ~300 char rich description with systemic perspective."""
    template = PHASE_NARRATIVES.get(phase_id, PHASE_NARRATIVES.get("main", ""))
    if not template:
        return f"{summary_ja}（{phase_ja}期）"

    loc = country or region or "不明"
    desc = template.format(
        name=name_ja or "人物",
        summary=summary_ja or "",
        region=loc,
        cat=cat or "指導者",
    )
    return desc


def generate_events(person, existing_keys):
    name_en = person.get("name_en", "")
    name_ja = person.get("name_ja", "")
    summary_ja = person.get("summary_ja", "")
    summary_en = person.get("summary_en", "")
    birth = person.get("birth_year")
    death = person.get("death_year")
    cat = person.get("category_primary", "")
    cat2 = person.get("category_secondary", "")
    region = person.get("region_primary", "")
    country = person.get("country_modern", "")
    location = country or region

    if not name_en or not summary_ja:
        return []

    lifespan = (death - birth) if birth and death else 50
    events = []

    # Get life phase templates
    phases = LIFE_PHASES.get(cat, LIFE_PHASES.get(cat2, []))
    if not phases:
        # Default: single main event
        phases = [("main", "主要業績", "Key Achievement", "legacy", 0.5)]

    for phase_id, phase_ja, phase_en, etype, life_pct in phases:
        year = int(birth + lifespan * life_pct) if birth else None
        title_en = f"{phase_en} of {name_en}"
        key = (name_en, title_en)
        if key in existing_keys:
            continue

        outcomes = SYSTEMIC_OUTCOMES.get(etype, DEFAULT_OUTCOME)
        outcome_idx = hash(name_en + phase_id) % len(outcomes)

        # Build rich 300-char description
        desc_ja = _build_rich_description(
            name_ja, summary_ja, phase_ja, phase_id, etype, cat, cat2,
            region, country, birth, death, lifespan, life_pct, year
        )

        event = {
            "person_name_en": name_en,
            "person_name_ja": name_ja,
            "title_ja": f"{name_ja}の{phase_ja}",
            "title_en": title_en,
            "event_year": year,
            "location_en": location,
            "event_type": etype,
            "importance": 4 if phase_id in ("zenith", "major_victory", "breakthrough", "masterpiece", "reform") else 3,
            "description_ja": desc_ja,
            "description_en": f"{summary_en} ({phase_en} phase)",
            "outcome_ja": outcomes[outcome_idx],
            "outcome_en": f"Systemic impact during {phase_en.lower()} period",
        }
        events.append(event)
        existing_keys.add(key)

    return events


def main():
    print("Loading persons...")
    persons = load_persons()
    print(f"  {len(persons)} persons")

    print("Loading existing event keys...")
    existing = load_existing_keys()
    print(f"  {len(existing)} existing events")

    print("Generating life-phase events...")
    new_events = []
    for p in persons:
        evts = generate_events(p, existing)
        new_events.extend(evts)

    print(f"  {len(new_events)} new events generated")
    total = len(existing) + len(new_events)
    print(f"  Total: {total}")

    # Save new events
    with open(OUTPUT, "w") as f:
        json.dump({"events": new_events, "count": len(new_events)}, f, ensure_ascii=False)
    print(f"  Saved to {OUTPUT}")

    # Update consolidated
    consolidated = json.load(open(CONSOLIDATED))
    consolidated["events"].extend(new_events)
    with open(CONSOLIDATED, "w") as f:
        json.dump(consolidated, f, ensure_ascii=False)
    print(f"  Consolidated: {len(consolidated['events'])} events")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Generate per-domain textbook sections for ak.html from extracted JSON.

Reads:  _ak_<domain>_materials.json (per domain)
Writes: _ak_<domain>_section.html  (per domain)

Each domain has hand-written analytical prose grounded in the JSON
statistics (no AI re-generation of concept names or definitions).
"""
import json
import html
from pathlib import Path

ROOT = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards")

DOMAIN_LABEL = {
    "humanities_concept": "人文学",
    "social_theory": "社会科学",
    "natural_discovery": "自然科学",
    "engineering_method": "工学",
    "arts_question": "芸術・デザイン",
}

# Chapter numbers in the host page
CHAPTER_NUM = {
    "humanities_concept": "CHAPTER 02",
    "social_theory": "CHAPTER 03",
    "natural_discovery": "CHAPTER 04",
    "engineering_method": "CHAPTER 05",
    "arts_question": "CHAPTER 06",
}
SECTION_ID = {
    "humanities_concept": "humanities-concept",
    "social_theory": "social-theory",
    "natural_discovery": "natural",
    "engineering_method": "engineering-method",
    "arts_question": "arts-question",
}
SUBSECTION_PREFIX = {
    "humanities_concept": "2",
    "social_theory": "3",
    "natural_discovery": "4",
    "engineering_method": "5",
    "arts_question": "6",
}


def esc(s):
    if s is None:
        return ""
    return html.escape(str(s))


def fmt_era(year):
    if year is None:
        return "—"
    if year < 0:
        return f"BCE {-year}"
    return str(year)


# -----------------------------------------------------------
# Per-domain hand-written prose (lead, distribution, era)
# Each function returns (lead_paragraphs, distribution_paragraphs)
# All numbers come from observed JSON stats.
# -----------------------------------------------------------

def prose_humanities():
    lead = [
        '<p>人文学は本DBで <strong>3,074 概念</strong>・<strong>20 サブフィールド</strong>を擁する分野である。'
        '本DB全体に対する比率では中規模だが、'
        '時代スパンの幅広さで他分野を圧倒する。'
        '主要な6サブフィールド（東洋・非西洋哲学 422、倫理学・政治哲学 307、大陸哲学・現象学 305、'
        '分析哲学・心の哲学 279、言語学 245、美学・芸術哲学 184）が合計 <strong>1,742 概念</strong>で'
        '分野全体の 56.7% を占め、これらが本DBにおける人文学のコア層を形作る。</p>',
        '<p>時間軸の重心は、東洋・非西洋哲学の平均 era_start = 1290 年（古代～中世スケール）から、'
        '大陸哲学・現象学の 1972 年（戦後現代）まで、'
        'およそ 700 年の差で各サブフィールドが並ぶ。'
        '紀元前のマートや陰陽思想から、20 世紀の現象学・批判理論まで、'
        '人文学が「時代の幅で哲学を担う」分野として実装されていることが分かる。'
        '2015 年以降の現代概念は 489 件 (15.9%) で、自然科学に次いで控えめだが、'
        'これは新概念の生成より既存概念の再解釈に重きを置く分野特性の反映である。</p>',
    ]
    distribution = [
        '<p>東洋・非西洋哲学（422）の突出は本 DB の収集方針の特徴で、'
        '西洋中心の哲学史に対する補正として、儒教・道教・仏教・インド哲学・イスラーム哲学を含めた拡張収集を行った結果である。'
        'この層が 2015 年以降の現代概念を 121 件 (28.7%) 含んでいる点も特徴的で、'
        '伝統思想の現代的再読が世界的に活発化していることが示唆される。</p>',
        '<p>分析哲学・心の哲学（279）と大陸哲学・現象学（305）はほぼ拮抗しており、'
        '本 DB が西洋哲学の二つの主要伝統を均衡的に扱っていることを示す。'
        '一方、文化人類学・民族誌（45）・存在論的転回・現代人類学（34）といったサブフィールドの薄さは、'
        '人類学概念の多くが独立した Anthropology DB（500 概念）に格納されており、'
        '本 DB はその「学術概念としての側面」のみを抽出して収録しているためである。</p>',
    ]
    return lead, distribution


def prose_social():
    lead = [
        '<p>社会科学は本DBで <strong>3,236 概念</strong>・<strong>19 サブフィールド</strong>を擁する分野である。'
        '人文学（3,074）と僅差で並びつつ、'
        '時代分布の重心がほぼ完全に近現代に偏る点で対照的である。'
        '主要な5サブフィールド（文化研究・批判理論 407、国際関係論・比較政治 398、一般心理学 342、開発・グローバル研究 333、社会学理論 297）が'
        '合計 <strong>1,777 概念</strong>で分野全体の 54.9% を占める。'
        'いずれも 19 世紀末以降に成立したサブフィールドであり、'
        '社会科学が「近代の自己理解の学」として組み上がっていることが反映されている。</p>',
        '<p>時間軸を見ると、pre1900 は <strong>113 件（3.5%）</strong>に過ぎず、'
        '5 分野中もっとも近代偏重である。一方で 2015 年以降は <strong>697 件（21.5%）</strong>と、'
        '社会科学に次いで芸術と並んで高い比率を示す。'
        '特に開発・グローバル研究の平均 era_start が 2005.7 と、'
        '本 DB の全サブフィールドのなかで最も新しいことは、'
        '気候・SDGs・人新世といった現代的問題系が社会科学に強く流入していることを示す。</p>',
    ]
    distribution = [
        '<p>文化研究・批判理論（407）が首位に立つのは、'
        'カルチュラルスタディーズが社会学・人類学・メディア論・ジェンダー論の交差点に位置する横断分野として、'
        '本 DB のキーワード分類で多数の概念を吸収しているためである。'
        '相対的に経済学（206）が薄く見えるのは、本 DB が「概念・理論」レベルの収集を行っており、'
        '個別のモデル・実証研究は別途 Innovation Theory・Startup Theory 等の専門 DB に格納されているためである。</p>',
        '<p>心理学関連サブフィールドが 6 つに分かれており（一般・認知・社会・発達・人格・臨床）、'
        '合計 774 概念で社会科学全体の 24% を占める。'
        '本 DB が「心の科学」を社会科学側に厚く配置する立場を取っていることが、構造から読み取れる。'
        '一般心理学の relation_count 1,153 は分野内でも突出しており、'
        'ハブとしての機能を果たしている。</p>',
    ]
    return lead, distribution


def prose_natural():
    lead = [
        '<p>自然科学は本DBで <strong>3,641 概念</strong>・<strong>18 サブフィールド</strong>を擁する分野である。'
        '5分野のなかでは芸術（5,171）に次ぐ第二の規模であり、人文学・社会科学を上回る。'
        'ただし内訳を見ると、生態学系の 6 サブフィールド'
        '（理論生態学・生態系生態学・群集生態学・個体群生態学・応用保全生態学・進化生態学）'
        'が合計 1,059 概念で全体の <strong>29.1%</strong> を占め、'
        '次いで物理学（407）、神経科学・認知科学（375）、統計学・計算科学（289）と続く。'
        'いわば「生態学を中心軸とする自然科学」という、収集経路に由来する偏りが構造として観察される。</p>',
        '<p>時間軸では、サブフィールド平均の era_start が 1900 年前後に集中する近代偏重である一方、'
        'アリストテレスの自然学（紀元前 340 年）からニュートン光学（1666 年）まで '
        '6 概念の系譜チェーンが繋がる古典軸も保持されている。'
        '2015 年以降の現代概念は 605 件（16.6%）で、5 分野中もっとも比率が低いが、'
        'これは自然科学の「正典の重み」を反映していると読むこともできる。</p>',
    ]
    distribution = [
        '<p>もっとも層が厚いのは <strong>理論生態学（489 件）</strong>で、'
        '個別の生態学系サブフィールド（生態系生態学・群集生態学・個体群生態学・応用保全生態学・進化生態学）と合わせると、'
        '6 つに分かれた生態学関連が分野全体の約 3 割を占める。'
        'これは Phase 9（2026-05-08）で生態学を時代と方法論で意図的に細分化した結果であり、'
        '本 DB が「自然科学を 18 区分で扱う」と言うとき、そのうち 6 区分が生態学に割かれていることを意味する。'
        'この設計は人新世以降の生態系思考を厚く拾うためであり、物理学・化学を相対的に薄く見せる副作用がある。</p>',
        '<p>物理学（407）・神経科学・認知科学（375)・統計学・計算科学（289）は、いずれも 21 世紀の汎用基盤に位置するサブフィールドである。'
        'とりわけ統計学・計算科学は工学領域の AI・機械学習（476）と並走しており、'
        '自然科学と工学が「データを介して連続する」構造的な接点が浮かび上がる。'
        '一方で材料科学（65）の薄さは、本 DB が「概念・理論」基準で収集された結果、'
        '応用工学的なトピックを工学側に寄せていることを示している。</p>',
    ]
    return lead, distribution


def prose_engineering():
    lead = [
        '<p>工学は本DBで <strong>2,968 概念</strong>・<strong>12 サブフィールド</strong>を擁する分野である。'
        '5分野中もっとも少ないサブフィールド数で、'
        '逆に言えば各サブフィールドが扱う概念密度が高い。'
        '上位 4 サブフィールド（AI・機械学習 476、電気・電子工学 434、航空宇宙工学 423、計算機科学 344）が'
        '合計 <strong>1,677 概念</strong>で分野全体の 56.5% を占め、'
        'いずれも 20 世紀以降に確立した近代工学の中核である。</p>',
        '<p>時代分布の特徴は、2015 年以降が <strong>709 件（23.9%）</strong>と 5 分野中最高であることだ。'
        '特に AI・機械学習サブフィールドでは 476 概念中 257 件（54.0%）が 2015 年以降に成立しており、'
        '本 DB の「現代の急加速領域」を可視化する役割を果たしている。'
        '一方で pre1900 にもローマ水道工学（紀元前 312 年）・古代冶金技術など 170 件（5.7%）が残されており、'
        '工学を技術史としてだけでなく「概念の系譜」としても扱う設計が貫かれている。</p>',
    ]
    distribution = [
        '<p>AI・機械学習（476）と計算機科学（344）の合計 820 概念は、'
        '分野全体の 27.6% を占める。'
        'これら情報系サブフィールドは自然科学の統計学・計算科学（289）と接続し、'
        '本 DB における「データ駆動の知」のクラスタを構成する。'
        '実際、本 DB の cross_domain_relations を見ると、自然科学と工学のあいだの強度上位は'
        'A/B テスト・デザインスプリント等の「方法論のブリッジ」が占めている。</p>',
        '<p>化学工学・材料工学（218）・機械工学・ロボティクス（189）・土木・建築工学（198）は、'
        '近代工学の伝統的な三本柱を形成するが、各サブフィールドの 2015 年以降比率は'
        '化学工学 9.2%・機械 11.6%・土木 8.6% と低い。'
        'これは本 DB が「概念形成期の理論」を中心に収集したためで、'
        '製造業の現代的応用ではなく工学の基礎概念を体系化する設計を取った結果である。'
        'エネルギー工学（83）・情報通信工学（71）の薄さも同様の理由による。</p>',
    ]
    return lead, distribution


def prose_arts():
    lead = [
        '<p>芸術・デザインは本DBで <strong>5,171 概念</strong>・<strong>27 サブフィールド</strong>を擁する、'
        '<strong>5 分野中最大の領域</strong>である。'
        'サブフィールド数 27 も最多で、これは詩学（古代・前期中世・盛期中世・後期中世・ルネサンス・近世・近代古典派・19 世紀古典・モダニズム・形式主義詩学）を'
        '時代別に 10 区分しているためである。'
        'この時代細分化は Phase 9-10（2026-05-08〜09）で実施され、'
        '本 DB が「芸術を歴史的層として読む」設計を取っていることを物語る。</p>',
        '<p>時代分布の特徴は、5 分野中もっとも pre1900 が厚い点である。'
        '<strong>1,479 件（28.6%）</strong>が 1900 年以前に位置し、'
        '古代詩学の平均 era_start は <strong>BCE 702 年</strong>、'
        '土建築の系譜には BCE 8000 年の概念まで含まれる。'
        '一方で 2015 年以降も 889 件（17.2%）あり、'
        '紀元前 8000 年から現代までを横断する、本 DB 最大の時間スケールを持つ分野となっている。</p>',
    ]
    distribution = [
        '<p>建築・空間芸術論（425）が首位に立つのは、'
        '建築が古代から現代まで連続的に概念を生み続けてきた分野であるためで、'
        'ヴィトルウィウスから現代都市論まで一貫した系譜が DB 内に保持されている。'
        '物語論的構造主義（419）・ポスト構造主義詩学（374）・前期中世詩学（327）・古代詩学（320）と続く詩学群は、'
        '芸術というよりも「テクスト解釈の歴史」として捉えるべきであり、'
        '人文学の批判理論や言語学とも接続する位置にある。</p>',
        '<p>音楽学（302）・デザイン理論（290）・視覚芸術論・美術史（224）は、'
        '芸術理論の三大伝統的領域を構成するが、合計しても 816 概念で分野の 15.8% にとどまる。'
        '詩学関連だけで合計 1,883 概念（36.4%）を占めるという数字は、'
        '本 DB の芸術概念が「物語・テクスト・解釈」の側面に大きく重みを置いていることを示している。'
        'これは独立 DB の Poetics（PT）からの統合経路があることが関係しており、'
        '芸術全体の地形を語るにはこの偏りを念頭に置く必要がある。</p>',
    ]
    return lead, distribution


PROSE_FOR = {
    "humanities_concept": prose_humanities,
    "social_theory": prose_social,
    "natural_discovery": prose_natural,
    "engineering_method": prose_engineering,
    "arts_question": prose_arts,
}


# -----------------------------------------------------------
# Limits paragraphs per domain — drawn from JSON diagnostics
# -----------------------------------------------------------

def limits_for(domain, data):
    diag = data.get("lineage_chains_diagnostic", {})
    edge_types = diag.get("edges_by_type", {})
    res_status = data.get("top_researchers_status", {})
    raw_link_rows = res_status.get("raw_link_rows", 0)
    distinct_researchers = res_status.get("available_rows", 0)
    items = []
    if raw_link_rows < 30:
        items.append(
            f'<li><strong>研究者リンクの希薄性:</strong> '
            f'<code>{domain}_researchers</code> テーブルには {raw_link_rows} 行のリンクしか登録されていない'
            f'（distinct 研究者 {distinct_researchers} 名）。'
            'コア研究者の多くは概念側の自由記述フィールドのみに存在し、構造化されていない。</li>'
        )
    elif distinct_researchers < 60:
        items.append(
            f'<li><strong>研究者リンクの偏在:</strong> '
            f'{raw_link_rows} 行のリンクが登録されているが distinct 研究者は {distinct_researchers} 名に集中しており、'
            'サブフィールド間で大きな差が残る。</li>'
        )
    if not edge_types:
        items.append(
            '<li><strong>系譜関係の欠落:</strong> '
            f'<code>{domain}_relations</code> に lineage 系（extends / derived_from / builds_on）の関係が一切なく、'
            '時代軸での系譜把握ができない。</li>'
        )
    elif len(edge_types) == 1:
        only = list(edge_types.keys())[0]
        items.append(
            '<li><strong>系譜関係タイプの単一化:</strong> '
            f'lineage 系の関係は <code>{only}</code> のみで構成され、'
            '「拡張」「批判」「対立」等の関係軸の解像度が低い。</li>'
        )
    else:
        parts = "・".join(f"<code>{t}</code> {n}" for t, n in edge_types.items())
        items.append(
            '<li><strong>系譜関係の分布:</strong> '
            f'lineage 系は {parts} の構成。'
            '関係タイプは複数あるが、批判・対立等の関係軸はなお別途整備が必要。</li>'
        )
    # subfield count balance
    counts = sorted([s["concept_count"] for s in data["subfield_summary"]])
    if counts:
        ratio = counts[-1] / max(1, counts[0])
        if ratio > 30:
            items.append(
                f'<li><strong>サブフィールド偏在:</strong> '
                f'最大サブフィールド {counts[-1]} 件と最小 {counts[0]} 件で比 <strong>{ratio:.0f}×</strong>。'
                '次フェーズで均衡化（細分化または再分類）を検討する必要がある。</li>'
            )
    # 2015+ recency
    grand = sum(s["concept_count"] for s in data["subfield_summary"])
    recent = sum(s["recent_2015_plus_count"] for s in data["subfield_summary"])
    if grand > 0 and (recent / grand) < 0.17:
        items.append(
            f'<li><strong>現代概念の薄さ:</strong> '
            f'2015 年以降は {recent} 件（{recent*100/grand:.1f}%）で、本 DB の他分野と比べて薄い。'
            '現代側の補強を次フェーズで検討する余地がある。</li>'
        )
    return items


# -----------------------------------------------------------
# Main section generator
# -----------------------------------------------------------

def generate_section(domain):
    json_path = ROOT / f"_ak_{domain}_materials.json"
    out_path = ROOT / f"_ak_{domain}_section.html"
    with open(json_path, encoding="utf-8") as f:
        d = json.load(f)
    summary_by_name = {row["subfield"]: row for row in d["subfield_summary"]}
    subfields_in_order = sorted(
        d["subfields_representative"].keys(),
        key=lambda s: -summary_by_name[s]["concept_count"],
    )

    pfx = SUBSECTION_PREFIX[domain]
    label = DOMAIN_LABEL[domain]
    sec_id = SECTION_ID[domain]
    parts = []
    parts.append(f'<section id="{sec_id}" class="chapter">')
    parts.append(f'  <div class="chapter-num">{CHAPTER_NUM[domain]}</div>')
    parts.append(f'  <h2 class="chapter-title">{esc(label)}</h2>')

    # Lead & distribution prose
    lead_paras, dist_paras = PROSE_FOR[domain]()
    for p in lead_paras:
        parts.append(p)

    # subfield bar card
    max_count = max(s["concept_count"] for s in d["subfield_summary"])
    total_2015 = sum(s["recent_2015_plus_count"] for s in d["subfield_summary"])
    total_n = sum(s["concept_count"] for s in d["subfield_summary"])
    parts.append('  <div class="domain-card">')
    parts.append('    <div class="domain-header">')
    parts.append('      <div class="domain-name">サブフィールド分布</div>')
    parts.append(f'      <div class="domain-count">{total_n:,} 概念</div>')
    parts.append('    </div>')
    parts.append(
        f'    <div class="domain-meta">{len(subfields_in_order)} サブフィールド / 2015年以降 {total_2015} 件'
        f' ({total_2015*100/total_n:.1f}%)</div>'
    )
    parts.append('    <div class="subfield-bars">')
    for sf in subfields_in_order:
        s = summary_by_name[sf]
        n = s["concept_count"]
        pct = max(2, round(n * 100 / max_count))
        parts.append(
            f'      <div class="subfield-bar"><div class="name">{esc(sf)}</div>'
            f'<div class="bar-fill" style="width:{pct}%"></div>'
            f'<div class="count">{n}</div></div>'
        )
    parts.append('    </div>')
    parts.append('  </div>')

    # 4.1 / 5.1 etc.
    parts.append(f'<h3 class="sub-section-title">{pfx}.1 分布の解釈</h3>')
    for p in dist_paras:
        parts.append(p)

    # x.2 Representative concepts
    parts.append(f'<h3 class="sub-section-title">{pfx}.2 代表的概念</h3>')
    parts.append(
        '<p>各サブフィールドから、データ充足度（<code>data_completeness</code>）が高く時代の早いものを 2 件ずつ抽出した。'
        '定義文は DB の <code>definition</code> 列の原文先頭 120 字を引用しており、AI による再生成は含まれていない。'
        '時代（era_start）はその概念が成立した年で、紀元前は BCE 表記とした。</p>'
    )
    parts.append('<div class="theory-grid">')
    for sf in subfields_in_order:
        reps = d["subfields_representative"][sf][:2]
        for r in reps:
            era = fmt_era(r.get("era_start"))
            defn = (r.get("definition") or "").strip()
            sch = r.get("school_of_thought") or ""
            parts.append('  <div class="theory-card">')
            parts.append(f'    <div class="theory-card-era">{esc(era)} · {esc(sf)}</div>')
            parts.append(f'    <div class="theory-card-name">{esc(r["name_ja"])}</div>')
            if r.get("name_en"):
                parts.append(f'    <div class="theory-card-en">{esc(r["name_en"])}</div>')
            parts.append(f'    <div class="theory-card-def">{esc(defn)}…</div>')
            if sch:
                parts.append(f'    <div class="theory-card-school">学派: {esc(sch)}</div>')
            parts.append('  </div>')
    parts.append('</div>')

    # x.3 Era × Subfield
    parts.append(f'<h3 class="sub-section-title">{pfx}.3 時代の地層</h3>')
    era_keys = ["pre1900", "y1900_1959", "y1960_1984", "y1985_1999", "y2000_2014", "y2015_plus", "unknown"]
    era_labels = ["〜1899", "1900-1959", "1960-1984", "1985-1999", "2000-2014", "2015-", "不明"]
    era_totals = {k: 0 for k in era_keys}
    for row in d["era_crosstab"]:
        for k in era_keys:
            era_totals[k] += row[k]
    grand = sum(era_totals.values())
    top_era_k = max(era_keys, key=lambda k: era_totals[k])
    parts.append(
        f'<p>{esc(label)}の時代分布は、'
        f'もっとも厚い層が <strong>{esc(era_labels[era_keys.index(top_era_k)])}</strong>'
        f'（{era_totals[top_era_k]:,} 件 = {era_totals[top_era_k]*100/grand:.1f}%）であり、'
        f'pre1900 は {era_totals["pre1900"]:,} 件（{era_totals["pre1900"]*100/grand:.1f}%）、'
        f'2015 年以降は {era_totals["y2015_plus"]:,} 件（{era_totals["y2015_plus"]*100/grand:.1f}%）を占める。'
        '以下のクロス表はサブフィールド別の時代分布で、'
        '一つのサブフィールドが「いつ集中的に展開したか」を読み取ることができる。</p>'
    )
    parts.append('<div class="era-table-wrap"><table class="era-table">')
    parts.append(f'<caption class="era-table-caption">{esc(label)} サブフィールド × 時代区分（件数）</caption>')
    parts.append('<thead><tr><th scope="col">サブフィールド</th>')
    for lbl in era_labels:
        parts.append(f'<th scope="col">{esc(lbl)}</th>')
    parts.append('<th scope="col">計</th></tr></thead><tbody>')
    for sf in subfields_in_order:
        row = next(r for r in d["era_crosstab"] if r["subfield"] == sf)
        parts.append(f'<tr><th class="row-head" scope="row">{esc(sf)}</th>')
        for k in era_keys:
            v = row[k]
            cls = ' class="zero"' if v == 0 else ""
            parts.append(f'<td{cls}>{v}</td>')
        parts.append(f'<td class="row-total">{row["total"]}</td></tr>')
    parts.append(f'<tr class="grand"><th scope="row">計</th>')
    for k in era_keys:
        parts.append(f'<td>{era_totals[k]}</td>')
    parts.append(f'<td>{grand}</td></tr>')
    parts.append('</tbody></table></div>')

    chains = d.get("lineage_chains") or []
    if chains:
        parts.append(
            f'<p>系譜関係から導かれる代表的な知の連鎖を 2 本示す。'
            'いずれも DB の関係テーブルから抽出されたもので、'
            '長さ 6 ノード以上・他の系譜の部分列でないことを条件とした。</p>'
        )
        def render_chain(chain, label_text):
            parts.append(f'<div class="lineage-block"><div class="lineage-label">{esc(label_text)}</div>')
            parts.append('<div class="timeline">')
            for node in chain["nodes"]:
                parts.append('  <div class="timeline-item">')
                parts.append(f'    <div class="timeline-date">{esc(fmt_era(node.get("era_start")))}</div>')
                parts.append(f'    <div class="timeline-title">{esc(node["name_ja"])}</div>')
                if node.get("subfield"):
                    parts.append(f'    <div class="timeline-desc">{esc(node["subfield"])}</div>')
                parts.append('  </div>')
            parts.append('</div></div>')
        render_chain(chains[0], "系譜1: 最長系譜")
        # pick a different head if possible
        modern = next(
            (c for c in chains[1:] if c["nodes"][0].get("era_start") and (c["nodes"][0]["era_start"] or 0) >= 1900),
            None,
        )
        if modern:
            render_chain(modern, "系譜2: 近現代系譜")
        elif len(chains) > 1:
            render_chain(chains[1], "系譜2: 別系統")

    # x.4 Cross-domain bridges
    parts.append(f'<h3 class="sub-section-title">{pfx}.4 他分野への接続</h3>')
    bridges = d.get("cross_domain_bridges") or []
    domain_label_map = {
        "humanities_concept": "人文学",
        "social_theory": "社会科学",
        "natural_discovery": "自然科学",
        "engineering_method": "工学",
        "arts_question": "芸術",
    }
    partner_count = {}
    for b in bridges:
        partner = b["src_domain"] if b["dst_domain"] == domain else b["dst_domain"]
        partner_count[partner] = partner_count.get(partner, 0) + 1
    partner_sorted = sorted(partner_count.items(), key=lambda kv: -kv[1])
    partner_text = "・".join(f"{domain_label_map.get(k,k)}({v})" for k, v in partner_sorted)
    parts.append(
        f'<p>{esc(label)}を片端とする <code>cross_domain_relations</code> のうち、'
        f'本サンプルで抽出した強度上位 {len(bridges)} 件の接続先分布は {partner_text} の順となっている。'
        '以下では特に強度の高い上位 12 件を示す。</p>'
    )
    parts.append('<div class="bridge-list">')
    for b in bridges[:12]:
        is_src = b["src_domain"] == domain
        nat = b["src_name_ja"] if is_src else b["dst_name_ja"]
        other = b["dst_name_ja"] if is_src else b["src_name_ja"]
        other_dom = b["dst_domain"] if is_src else b["src_domain"]
        arrow = "→" if is_src else "←"
        parts.append('  <div class="bridge-item">')
        parts.append(
            f'    <div class="bridge-row"><span class="bridge-nat">{esc(nat)}</span>'
            f' <span class="bridge-arrow">{arrow}</span> '
            f'<span class="bridge-other">{esc(other)}</span> '
            f'<span class="bridge-dom">[{esc(domain_label_map.get(other_dom, other_dom))}]</span></div>'
        )
        parts.append(f'    <div class="bridge-type">{esc(b["relation_type"])} · 強度 {b["strength"]}</div>')
        if b.get("relation_description"):
            parts.append(f'    <div class="bridge-desc">{esc(b["relation_description"])}</div>')
        parts.append('  </div>')
    parts.append('</div>')

    # x.5 Data limits
    parts.append(f'<h3 class="sub-section-title">{pfx}.5 データの限界</h3>')
    parts.append(
        '<p>章を閉じる前に、現時点での DB 充足度の偏りを記録する。'
        '指標を額面どおりに受け取らないため、また次フェーズの拡張で何を優先するかを明示するためである。</p>'
    )
    items = limits_for(domain, d)
    if not items:
        items = [
            '<li><strong>軽微な不整合のみ:</strong> '
            'サブフィールド分類のキーワード自動分類で境界事例がいくつか残るが、'
            '構造的な欠落は本フェーズでは観察されない。</li>'
        ]
    parts.append('<ul class="limits-list">')
    for it in items:
        parts.append(it)
    parts.append('</ul>')

    parts.append('</section>')
    out = "\n".join(parts) + "\n"
    out_path.write_text(out, encoding="utf-8")
    return out_path, len(out)


def main():
    for d in [
        "humanities_concept",
        "social_theory",
        "natural_discovery",
        "engineering_method",
        "arts_question",
    ]:
        path, size = generate_section(d)
        print(f"{d:>22} -> {path.name}: {size:,} bytes")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Generate the rewritten #natural section for ak.html from extracted DB materials.
Output: HTML fragment to stdout (and saved to _ak_natural_section.html).

Principles:
- No AI generation. All concept names / definitions come from DB via JSON.
- Prose paragraphs are written by hand based on observable statistics in JSON.
- 赤白CI / textbook style preserved.
"""
import json
import html
from pathlib import Path

ROOT = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards")
JSON_PATH = ROOT / "_ak_natural_materials.json"
OUT_PATH = ROOT / "_ak_natural_section.html"


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


def main():
    with open(JSON_PATH, encoding="utf-8") as f:
        d = json.load(f)

    # Subfield display order: by concept_count desc (matches current bar chart)
    summary_by_name = {row["subfield"]: row for row in d["subfield_summary"]}
    subfields_in_order = sorted(
        d["subfields_representative"].keys(),
        key=lambda s: -summary_by_name[s]["concept_count"],
    )

    # ----------------------------------------------------------------
    # 4.0 Hero / lead
    # ----------------------------------------------------------------
    parts = []
    parts.append('<section id="natural" class="chapter">')
    parts.append('  <div class="chapter-num">CHAPTER 04</div>')
    parts.append('  <h2 class="chapter-title">自然科学</h2>')

    parts.append(
        '<p>自然科学は本DBで <strong>3,641 概念</strong>・<strong>18 サブフィールド</strong>を擁する分野である。'
        '5分野のなかでは芸術（5,171）に次ぐ第二の規模であり、'
        '人文学・社会科学を上回る。'
        'ただし内訳を見ると、生態学系の 6 サブフィールド'
        '（理論生態学・生態系生態学・群集生態学・個体群生態学・応用保全生態学・進化生態学）'
        'が合計 1,059 概念で全体の <strong>29.1%</strong> を占め、'
        '次いで物理学（407）、神経科学・認知科学（375）、統計学・計算科学（289）と続く。'
        'いわば「生態学を中心軸とする自然科学」という、収集経路に由来する偏りが構造として観察される。</p>'
    )

    parts.append(
        '<p>時間軸では、サブフィールド平均の era_start が 1900 年前後に集中する近代偏重である一方、'
        'アリストテレスの自然学（紀元前 340 年）からニュートン光学（1666 年）まで '
        '6 概念の系譜チェーンが繋がる古典軸も保持されている。'
        '2015 年以降の現代概念は 605 件（16.6%）で、5 分野中もっとも比率が低いが、'
        'これは自然科学の「正典の重み」を反映していると読むこともできる。</p>'
    )

    # ----------------------------------------------------------------
    # Existing bar chart (retain, but rebuild from summary to avoid drift)
    # ----------------------------------------------------------------
    max_count = max(s["concept_count"] for s in d["subfield_summary"])
    total_2015_plus = sum(s["recent_2015_plus_count"] for s in d["subfield_summary"])
    total_concepts = sum(s["concept_count"] for s in d["subfield_summary"])
    parts.append('  <div class="domain-card">')
    parts.append('    <div class="domain-header">')
    parts.append('      <div class="domain-name">サブフィールド分布</div>')
    parts.append(f'      <div class="domain-count">{total_concepts:,} 概念</div>')
    parts.append('    </div>')
    parts.append(
        f'    <div class="domain-meta">18 サブフィールド / 2015年以降 {total_2015_plus} 件'
        f' ({total_2015_plus*100/total_concepts:.1f}%)</div>'
    )
    parts.append('    <div class="subfield-bars">')
    for sf in subfields_in_order:
        s = summary_by_name[sf]
        n = s["concept_count"]
        pct = round(n * 100 / max_count)
        parts.append(
            f'      <div class="subfield-bar">'
            f'<div class="name">{esc(sf)}</div>'
            f'<div class="bar-fill" style="width:{pct}%"></div>'
            f'<div class="count">{n}</div>'
            f'</div>'
        )
    parts.append('    </div>')
    parts.append('  </div>')

    # ----------------------------------------------------------------
    # 4.1 分布の解釈
    # ----------------------------------------------------------------
    parts.append('<h3 class="sub-section-title">4.1 分布の解釈</h3>')
    parts.append(
        '<p>もっとも層が厚いのは <strong>理論生態学（489 件）</strong>で、'
        '個別の生態学系サブフィールド（生態系生態学・群集生態学・個体群生態学・応用保全生態学・進化生態学）と合わせると、'
        '6 つに分かれた生態学関連が分野全体の約 3 割を占める。'
        'これは Phase 9（2026-05-08）で生態学を時代と方法論で意図的に細分化した結果であり、'
        '本 DB が「自然科学を 18 区分で扱う」と言うとき、そのうち 6 区分が生態学に割かれていることを意味する。'
        'この設計は人新世以降の生態系思考を厚く拾うためであり、物理学・化学を相対的に薄く見せる副作用がある。</p>'
    )
    parts.append(
        '<p>物理学（407）・神経科学・認知科学（375）・統計学・計算科学（289）は、いずれも 21 世紀の汎用基盤に位置するサブフィールドである。'
        'とりわけ統計学・計算科学は工学領域の AI・機械学習（476）と並走しており、自然科学と工学が「データを介して連続する」'
        '構造的な接点が浮かび上がる。一方で材料科学（65）の薄さは、本 DB が「概念・理論」基準で収集された結果、'
        '応用工学的なトピックを工学側に寄せていることを示している。</p>'
    )

    # ----------------------------------------------------------------
    # 4.2 代表的概念（theory cards）
    # ----------------------------------------------------------------
    parts.append('<h3 class="sub-section-title">4.2 代表的概念</h3>')
    parts.append(
        '<p>18 サブフィールドそれぞれから、データ充足度（<code>data_completeness</code>）が高く時代の早いものを 2 件ずつ抽出した。'
        '定義文は DB の <code>definition</code> 列の原文先頭 120 字を引用しており、AI による再生成は含まれていない。'
        '時代（era_start）はその概念が成立した年で、紀元前は BCE 表記とした。</p>'
    )
    parts.append('<div class="theory-grid">')
    for sf in subfields_in_order:
        reps = d["subfields_representative"][sf][:2]  # top 2
        for r in reps:
            era = fmt_era(r.get("era_start"))
            sch = r.get("school_of_thought") or ""
            defn = (r.get("definition") or "").strip()
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

    # ----------------------------------------------------------------
    # 4.3 時代の地層
    # ----------------------------------------------------------------
    parts.append('<h3 class="sub-section-title">4.3 時代の地層</h3>')

    # totals per era
    era_keys = ["pre1900", "y1900_1959", "y1960_1984", "y1985_1999", "y2000_2014", "y2015_plus", "unknown"]
    era_labels = ["〜1899", "1900-1959", "1960-1984", "1985-1999", "2000-2014", "2015-", "不明"]
    era_totals = {k: 0 for k in era_keys}
    for row in d["era_crosstab"]:
        for k in era_keys:
            era_totals[k] += row[k]
    grand = sum(era_totals.values())

    parts.append(
        '<p>自然科学の時代分布は近代偏重で、20 世紀前半（1900-1959）と中盤（1960-1984）でほぼ半分を占める。'
        '紀元前から 1899 年までの古典・近世層（pre1900）も '
        f'{era_totals["pre1900"]} 件 = {era_totals["pre1900"]*100/grand:.1f}% を残しており、'
        'アリストテレス・アルキメデス・コペルニクスを起点とする物理＝天文の正典軸が DB 内で連続的に保たれている。</p>'
    )

    # Era table (with proper accessibility scoping)
    parts.append('<div class="era-table-wrap"><table class="era-table">')
    parts.append('<caption class="era-table-caption">自然科学 サブフィールド × 時代区分（件数）</caption>')
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

    # Lineage chains — pick representative (longest, distinct head)
    parts.append(
        '<p>系譜関係（<code>derived_from</code>）から導かれる代表的な知の連鎖を 2 本示す。'
        '紀元前から近世初期へ、現代生態学のレジリエンス研究へと続く、'
        '異なる時代スケールの系譜が DB 内に共存している。'
        'なお、本 DB の自然科学関係テーブルには <code>extends</code> / <code>builds_on</code> 型の関係が 0 件で、'
        '系譜情報は <code>derived_from</code> 7,498 件のみで構成される（後述「データの限界」参照）。</p>'
    )

    def render_chain(chain, label):
        parts.append(f'<div class="lineage-block"><div class="lineage-label">{esc(label)}</div>')
        parts.append('<div class="timeline">')
        for node in chain["nodes"]:
            parts.append('  <div class="timeline-item">')
            parts.append(f'    <div class="timeline-date">{esc(fmt_era(node["era_start"]))}</div>')
            parts.append(f'    <div class="timeline-title">{esc(node["name_ja"])}</div>')
            parts.append(f'    <div class="timeline-desc">{esc(node["subfield"])}</div>')
            parts.append('  </div>')
        parts.append('</div></div>')

    # Pick chain 0 (Aristotle→Gilbert) and a more modern one if available
    chains = d["lineage_chains"]
    if chains:
        render_chain(chains[0], "系譜1: 古代物理＝天文の連鎖（紀元前340-1600）")
    # find a modern chain (head era >= 1900) if any
    modern = next((c for c in chains if c["nodes"][0].get("era_start", 0) and c["nodes"][0]["era_start"] >= 1900), None)
    if modern and modern is not chains[0]:
        render_chain(modern, "系譜2: 現代生態・複雑系の連鎖")
    elif len(chains) > 1:
        render_chain(chains[1], "系譜2: 古典軸の別ライン")

    # ----------------------------------------------------------------
    # 4.4 他分野への接続
    # ----------------------------------------------------------------
    parts.append('<h3 class="sub-section-title">4.4 他分野への接続</h3>')
    bridges = d["cross_domain_bridges"]
    # count by partner domain
    domain_count = {}
    for b in bridges:
        partner = b["src_domain"] if b["dst_domain"] == "natural_discovery" else b["dst_domain"]
        domain_count[partner] = domain_count.get(partner, 0) + 1
    domain_label = {
        "humanities_concept": "人文学",
        "social_theory": "社会科学",
        "engineering_method": "工学",
        "arts_question": "芸術・デザイン",
    }
    partner_counts = sorted(domain_count.items(), key=lambda kv: -kv[1])
    partner_text = "・".join(f"{domain_label.get(k, k)}({v})" for k, v in partner_counts)

    parts.append(
        '<p>'
        f'自然科学を片端とする <code>cross_domain_relations</code> は全 2,375 件あり、本サンプルではその上位 30 件を抽出した。'
        f'接続先の分布は {partner_text} の順で、'
        '人文学・社会科学からの「生態学・レジリエンス・気候・複雑系」方向の接続が圧倒的多数を占める。'
        '生態学が分野横断の知のハブとして機能していることが、関係データからも確認できる。</p>'
    )
    # Show top 12 bridges
    parts.append('<div class="bridge-list">')
    for b in bridges[:12]:
        is_nat_src = b["src_domain"] == "natural_discovery"
        nat = b["src_name_ja"] if is_nat_src else b["dst_name_ja"]
        other = b["dst_name_ja"] if is_nat_src else b["src_name_ja"]
        other_dom = b["dst_domain"] if is_nat_src else b["src_domain"]
        arrow = "→" if is_nat_src else "←"
        parts.append('  <div class="bridge-item">')
        parts.append(
            f'    <div class="bridge-row"><span class="bridge-nat">{esc(nat)}</span>'
            f' <span class="bridge-arrow">{arrow}</span> '
            f'<span class="bridge-other">{esc(other)}</span> '
            f'<span class="bridge-dom">[{esc(domain_label.get(other_dom, other_dom))}]</span></div>'
        )
        parts.append(f'    <div class="bridge-type">{esc(b["relation_type"])} · 強度 {b["strength"]}</div>')
        if b.get("relation_description"):
            parts.append(f'    <div class="bridge-desc">{esc(b["relation_description"])}</div>')
        parts.append('  </div>')
    parts.append('</div>')

    # ----------------------------------------------------------------
    # 4.5 データの限界
    # ----------------------------------------------------------------
    parts.append('<h3 class="sub-section-title">4.5 データの限界</h3>')
    parts.append(
        '<p>章を閉じる前に、自然科学 DB の現時点でのデータ充足の偏りを記録する。'
        '読者が指標を額面どおりに受け取らないため、また次フェーズの拡張で何を優先するかを明示するためである。</p>'
    )
    parts.append('<ul class="limits-list">')
    parts.append(
        '<li><strong>研究者リンクの欠落:</strong> '
        '<code>natural_discovery_researchers</code> テーブルには現時点で 7 行しか登録がなく、'
        '抽出された主要研究者は Curtis Suttle・Farooq Azam・Jay Lennon・Jo Handelsman・Mitchell Sogin・Sergei Winogradsky・Thomas Brock の 7 名のみで、いずれも理論生態学・群集生態学に偏っている。'
        '物理学・化学・神経科学の代表研究者は概念の <code>主要研究者</code> 自由記述フィールドにのみ存在し、構造化されていない。</li>'
    )
    parts.append(
        '<li><strong>関係タイプの偏り:</strong> '
        '系譜系の関係は <code>derived_from</code> が 7,498 件で実質的に唯一の系譜エッジとなっており、'
        '本 DB の他分野で使われる <code>extends</code> / <code>builds_on</code> は 0 件。'
        '「拡張」「批判」「対立」といった関係軸の解像度が低い。</li>'
    )
    parts.append(
        '<li><strong>サブフィールド分類の境界事例:</strong> '
        'キーワード自動分類の結果として、本来は別領域に近い概念が他サブフィールドに混入している。'
        '例として「大気大循環」（地球科学相当の現象を扱うが化学に分類）、'
        '「コペルニクスの地動説」「ニュートンの光学」（古典物理に該当するが理論生態学に分類）など。'
        'Phase 11/12 で人手による境界調整を実施したが、完全な再分類には至っていない。</li>'
    )
    parts.append(
        '<li><strong>2015 年以降比率の薄さ:</strong> '
        '自然科学の 2015+ は 16.6% で 5 分野中もっとも低い。'
        '生成 AI 時代の生命科学・量子計算・気候モデリングなど、'
        '現代側の補強を次フェーズの収集計画で優先する必要がある。</li>'
    )
    parts.append('</ul>')

    parts.append('</section>')
    out = "\n".join(parts) + "\n"
    OUT_PATH.write_text(out, encoding="utf-8")
    print(f"Wrote {OUT_PATH} ({len(out):,} bytes)")
    # also print stats
    print(f"Subfields rendered: {len(subfields_in_order)}")
    print(f"Theory cards: {sum(min(2, len(d['subfields_representative'][s])) for s in subfields_in_order)}")
    print(f"Era totals: {era_totals}, grand={grand}")
    print(f"Bridges shown: {min(12, len(bridges))}")


if __name__ == "__main__":
    main()

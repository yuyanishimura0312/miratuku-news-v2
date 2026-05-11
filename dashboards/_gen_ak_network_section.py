#!/usr/bin/env python3
"""Generate enhanced Chapter 08 (関係ネットワーク) for ak.html."""
import json
import html
from pathlib import Path

ROOT = Path("/Users/nishimura+/projects/apps/miratuku-news-v2/dashboards")
MAT = json.load(open(ROOT / "_ak_network_materials.json", encoding="utf-8"))

DOMAIN_LABEL = {
    "humanities_concept": "人文学",
    "social_theory": "社会科学",
    "natural_discovery": "自然科学",
    "engineering_method": "工学",
    "arts_question": "芸術",
}
ORDER = ["humanities_concept", "social_theory", "natural_discovery", "engineering_method", "arts_question"]


def esc(s):
    return html.escape(str(s)) if s is not None else ""


def gen():
    parts = []
    parts.append('<section id="network" class="chapter">')
    parts.append('  <div class="chapter-num">CHAPTER 08</div>')
    parts.append('  <h2 class="chapter-title">関係ネットワーク</h2>')

    # Build pair lookup
    pair_lookup = {}
    for p in MAT["pair_matrix"]:
        pair_lookup[(p["a"], p["b"])] = p["count"]
        pair_lookup[(p["b"], p["a"])] = p["count"]
    total_5core = sum(p["count"] for p in MAT["pair_matrix"])
    total_cd = MAT["total_cross_domain_relations"]
    rt = MAT["relation_types"]
    top_rt = sorted(rt.items(), key=lambda kv: -kv[1])[:5]
    top_hubs = MAT["top_hubs"]

    parts.append(
        '<p>本 DB の関係ネットワークは、分野内関係（同じ分野内の系譜・対立・拡張など）と'
        f'分野横断関係（<code>cross_domain_relations</code>）から成る。'
        f'横断関係は全体で <strong>{total_cd:,} 件</strong>登録されているが、'
        f'このうち本ダッシュボードが扱う 5 分野（人文学・社会科学・自然科学・工学・芸術）の'
        f'相互間に直接張られているのは <strong>{total_5core:,} 件</strong>であり、'
        f'残りの約 {(total_cd-total_5core)*100/total_cd:.0f}% は innovation_theory・startup_theory・business_models 等の'
        '中間ハブ DB 経由の接続である。'
        '5 分野直接接続は Phase 11 で意図的に追加されたもので、'
        '異分野の概念がハブを介さず直に結ばれる経路を確保している。</p>'
    )

    # ---- 5x5 matrix ----
    parts.append('<h3 class="sub-section-title">8.1 5分野ペア・マトリクス</h3>')
    parts.append(
        '<p>下表は 5 分野相互の <code>cross_domain_relations</code> 件数を対称マトリクスで示したものである。'
        '色が濃いほど結合密度が高い。'
        '芸術・人文学のペアが最も密で 609 件、自然科学はどの分野とも 50 件以下と相対的に疎であることが読み取れる。</p>'
    )
    max_pair = max(p["count"] for p in MAT["pair_matrix"])
    parts.append('<div class="era-table-wrap"><table class="matrix-table">')
    parts.append('<caption class="era-table-caption">5分野間 cross_domain_relations 件数</caption>')
    parts.append('<thead><tr><th scope="col"></th>')
    for d in ORDER:
        parts.append(f'<th scope="col">{esc(DOMAIN_LABEL[d])}</th>')
    parts.append('</tr></thead><tbody>')
    for a in ORDER:
        parts.append(f'<tr><th class="row-head" scope="row">{esc(DOMAIN_LABEL[a])}</th>')
        for b in ORDER:
            if a == b:
                parts.append('<td class="diag">—</td>')
            else:
                v = pair_lookup.get((a, b), 0)
                intensity = round(v * 100 / max_pair)
                parts.append(
                    f'<td class="matrix-cell" style="--intensity:{intensity}">{v}</td>'
                )
        parts.append('</tr>')
    parts.append('</tbody></table></div>')

    parts.append(
        '<p>マトリクスから 3 つの構造的傾向が浮かぶ。'
        '<strong>第一に、芸術系を中心とした密な三角</strong>（芸術 ↔ 人文学 609、芸術 ↔ 社会科学 437、人文学 ↔ 社会科学 271）'
        'が左上から中央にかけて形成されており、'
        '人文・社会・芸術の三領域が互いに概念を共有していることが分かる。'
        '<strong>第二に、工学は社会科学・芸術と中規模で結合するが</strong>'
        '（工学 ↔ 社会科学 127、工学 ↔ 芸術 218）、'
        '自然科学とは 53 件と意外に薄い。'
        '<strong>第三に、自然科学はどの分野とも 50 件以下にとどまり</strong>、'
        '他分野からの参照は受けるが直接接続が薄い「専門島」になっていることが見える。</p>'
    )

    # ---- Top hubs ----
    parts.append('<h3 class="sub-section-title">8.2 ハブ概念ランキング</h3>')
    parts.append(
        '<p>cross_domain_relations のなかで、もっとも多くの他分野概念と接続している概念を上位 20 件抽出した。'
        '接続数は <code>source_id</code> と <code>target_id</code> の両方の出現を合算している。'
        '社会科学の新制度主義（94 件接続）を頂点に、'
        '制度論・実践論・プラットフォーム経済などの「組織と社会の境界に位置する概念」が上位を占める。'
        'これは本 DB が経営学・スタートアップ理論との接続経路を通じて'
        '社会科学概念に多数の参照を集める構造を持つためで、'
        '純粋な学問的中心性というより収集経路の反映と読むのが妥当である。</p>'
    )
    parts.append('<div class="bridge-list">')
    for h in top_hubs[:20]:
        parts.append('  <div class="bridge-item">')
        parts.append(
            f'    <div class="bridge-row">'
            f'<span class="bridge-nat">{esc(h["name_ja"])}</span>'
            f' <span class="bridge-dom">[{esc(DOMAIN_LABEL.get(h["domain"], h["domain"]))}]</span>'
            f'</div>'
        )
        parts.append(f'    <div class="bridge-type">接続 {h["connections"]} 件</div>')
        parts.append('  </div>')
    parts.append('</div>')

    # ---- Relation type ----
    parts.append('<h3 class="sub-section-title">8.3 関係タイプの分布</h3>')
    parts.append(
        f'<p>{total_cd:,} 件の関係は意味の異なる複数のタイプに分かれており、'
        '<code>applied_to</code>（応用される）・<code>thematic_overlap</code>（主題が重なる）・'
        '<code>informs</code>（影響を与える）の 3 つが上位を占める。'
        '上位 5 タイプの構成は以下のとおりである。</p>'
    )
    parts.append('<div class="era-table-wrap"><table class="era-table">')
    parts.append('<caption class="era-table-caption">関係タイプ上位 5（cross_domain_relations）</caption>')
    parts.append('<thead><tr><th scope="col">関係タイプ</th><th scope="col">件数</th><th scope="col">構成比</th></tr></thead><tbody>')
    for rt_name, n in top_rt:
        parts.append(
            f'<tr><th scope="row" class="row-head"><code>{esc(rt_name)}</code></th>'
            f'<td class="row-total">{n:,}</td>'
            f'<td>{n*100/total_cd:.1f}%</td></tr>'
        )
    others = total_cd - sum(n for _, n in top_rt)
    parts.append(
        f'<tr><th scope="row" class="row-head">その他</th>'
        f'<td>{others:,}</td>'
        f'<td>{others*100/total_cd:.1f}%</td></tr>'
    )
    parts.append(f'<tr class="grand"><th scope="row">合計</th><td>{total_cd:,}</td><td>100.0%</td></tr>')
    parts.append('</tbody></table></div>')

    parts.append(
        '<p>応用関係（<code>applied_to</code>）と主題重複（<code>thematic_overlap</code>）の二大カテゴリが約 36% を占める一方で、'
        '理論的基盤（<code>theoretical_foundation</code> 10.0%）や'
        '方法論的基盤（<code>methodological_foundation</code> 3.2%）といった'
        '系譜的・継承的関係も明示的にコードされている。'
        '関係タイプを区別できる設計のおかげで、本 DB は「単に繋がっている」という以上の質的情報を保持する。</p>'
    )

    parts.append('</section>')
    out = "\n".join(parts) + "\n"
    Path(ROOT / "_ak_network_section.html").write_text(out, encoding="utf-8")
    print(f"Wrote _ak_network_section.html: {len(out):,} bytes")


if __name__ == "__main__":
    gen()

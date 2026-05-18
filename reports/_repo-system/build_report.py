#!/usr/bin/env python3
"""
/repo system — レポート生成 CLI

- design_rules.db を参照してテーマを取得
- templates/report.html を展開して HTML レポートを書き出す
- 入力: JSON ファイル (sections / cover meta / theme 指定)
- 出力: ~/projects/apps/miratuku-news-v2/reports/<slug>.html

依存: Python 3 標準ライブラリのみ (Jinja2 不要)
使い方:
  python3 build_report.py --input my-report.json --output my-report.html
  python3 build_report.py --input my-report.json --theme essesense
  python3 build_report.py --list-themes
  python3 build_report.py --list-rules essesense
"""

import argparse
import json
import os
import re
import sqlite3
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORTS_DIR = ROOT.parent
DB_PATH = ROOT / "design_rules.db"
TEMPLATES_DIR = ROOT / "templates"
DATA_DIR = ROOT / "data"        # 編集機能: 生成時の spec JSON を slug 単位で保存
DEFAULT_TEMPLATE = "report.html"  # advisory-report-default
DATA_DIR.mkdir(exist_ok=True)


# ====================================================================
# DB ヘルパー
# ====================================================================
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _esc(s):
    """HTML エスケープ。None は空文字へ。"""
    if s is None:
        return ""
    return (str(s)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;"))


def get_theme(theme_id):
    with db() as c:
        row = c.execute("SELECT * FROM themes WHERE theme_id = ?", (theme_id,)).fetchone()
        if not row:
            sys.exit(f"[error] theme '{theme_id}' not found in design_rules.db")
        return dict(row)


def get_brand_assets(theme_id):
    """テーマに紐づくロゴ assets を辞書で返す (cover-top / header / cover-art)。"""
    with db() as c:
        rows = c.execute("SELECT asset_id, file_path FROM assets WHERE theme_id = ?",
                         (theme_id,)).fetchall()
    assets = {r["asset_id"]: r["file_path"] for r in rows}
    if theme_id == "miratuku":
        return {
            "brand_mark_top":    assets.get("miratuku-mark-white", ""),
            "brand_mark_header": assets.get("miratuku-mark", ""),
            "cover_logo":        assets.get("miratuku-logo", ""),
        }
    if theme_id == "essesense":
        wm = assets.get("esse-sense-wordmark", "")
        return {
            "brand_mark_top":    wm,
            "brand_mark_header": wm,
            "cover_logo":        wm,
        }
    # fallback
    first = next(iter(assets.values()), "")
    return {"brand_mark_top": first, "brand_mark_header": first, "cover_logo": first}


def list_themes():
    with db() as c:
        rows = c.execute("""
            SELECT theme_id, display_name, base_color, accent_color, description, status
            FROM themes ORDER BY theme_id
        """).fetchall()
    print(f"{'theme_id':<14}{'name':<14}{'base':<10}{'accent':<10}status")
    print("-" * 70)
    for r in rows:
        print(f"{r['theme_id']:<14}{r['display_name']:<14}{r['base_color']:<10}"
              f"{r['accent_color']:<10}{r['status']}")
        print(f"  {r['description']}\n")


def list_templates():
    with db() as c:
        rows = c.execute("""
            SELECT template_id, display_name, file_path, default_pages, purpose
            FROM report_templates ORDER BY template_id
        """).fetchall()
    print(f"{'template_id':<32}{'pages':<7}name / purpose")
    print("-" * 80)
    for r in rows:
        print(f"{r['template_id']:<32}{r['default_pages']:<7}{r['display_name']}")
        if r['purpose']:
            print(f"  ↳ {r['purpose']}")


def list_components():
    with db() as c:
        rows = c.execute("""
            SELECT component_id, display_name, html_class, purpose
            FROM components ORDER BY component_id
        """).fetchall()
    print(f"{'component_id':<22}{'class':<22}name")
    print("-" * 90)
    for r in rows:
        print(f"{r['component_id']:<22}{r['html_class']:<22}{r['display_name']}")


def list_rules(theme_id=None):
    with db() as c:
        if theme_id:
            rows = c.execute("""
                SELECT theme_id, category, rule_text, rationale, enforcement
                FROM design_rules
                WHERE theme_id IS NULL OR theme_id = ?
                ORDER BY (theme_id IS NULL) DESC, category, rule_id
            """, (theme_id,)).fetchall()
        else:
            rows = c.execute("""
                SELECT theme_id, category, rule_text, rationale, enforcement
                FROM design_rules ORDER BY category, rule_id
            """).fetchall()
    if not rows:
        print(f"[info] no rules for theme '{theme_id}'")
        return
    for r in rows:
        scope = f"[{r['theme_id'] or 'common'}]"
        print(f"{scope:<14}[{r['enforcement']:<6}][{r['category']:<10}] {r['rule_text']}")
        if r['rationale']:
            print(f"  ↳ {r['rationale']}")


# ====================================================================
# 簡易テンプレートエンジン
#   - {{ var }}            変数展開 (HTML エスケープ既定 ON)
#   - {{ var|safe }}       生 HTML として展開 (本文 body_html 等)
#   - {% if x %}...{% endif %}                 条件
#   - {% for x in list %}...{% endfor %}       反復 (nested 対応・depth counter)
#   - filter: "%02d"|format(n) / "%s"|format(s)
# ====================================================================
class Tpl:
    def __init__(self, src):
        self.src = src

    def render(self, ctx):
        out = self.src
        out = self._for(out, ctx)
        out = self._if(out, ctx)
        out = self._vars(out, ctx)
        return out

    def _vars(self, s, ctx):
        def sub(m):
            expr = m.group(1).strip()
            raw = False
            if expr.endswith("|safe"):
                raw = True
                expr = expr[:-5].strip()
            val = self._eval(expr, ctx)
            return str(val) if raw else _esc(val)
        return re.sub(r'\{\{\s*([^{}]+?)\s*\}\}', sub, s)

    def _if(self, s, ctx):
        # ネスト if は最内側から処理
        pat = re.compile(r'\{\%\s*if\s+(\w+)\s*\%\}((?:(?!\{\%\s*if\s).)*?)\{\%\s*endif\s*\%\}', re.S)
        while True:
            m = pat.search(s)
            if not m:
                break
            cond, body = m.group(1).strip(), m.group(2)
            keep = body if ctx.get(cond) else ""
            s = s[:m.start()] + keep + s[m.end():]
        return s

    def _find_matching_endfor(self, s, start):
        """start 位置の {% for %} に対応する {% endfor %} を depth counter で探す。"""
        for_re = re.compile(r'\{\%\s*for\s+\w+\s+in\s+\w+\s*\%\}')
        end_re = re.compile(r'\{\%\s*endfor\s*\%\}')
        depth = 1
        pos = start
        while depth > 0:
            f = for_re.search(s, pos)
            e = end_re.search(s, pos)
            if not e:
                return -1, -1
            if f and f.start() < e.start():
                depth += 1
                pos = f.end()
            else:
                depth -= 1
                if depth == 0:
                    return e.start(), e.end()
                pos = e.end()
        return -1, -1

    def _for(self, s, ctx):
        for_open = re.compile(r'\{\%\s*for\s+(\w+)\s+in\s+(\w+)\s*\%\}')
        while True:
            m = for_open.search(s)
            if not m:
                break
            varname, listname = m.group(1), m.group(2)
            body_start = m.end()
            end_start, end_end = self._find_matching_endfor(s, body_start)
            if end_start < 0:
                # 未対応な {% endfor %} なし → 残骸として除去
                s = s[:m.start()] + s[m.end():]
                continue
            body = s[body_start:end_start]
            items = ctx.get(listname, []) or []
            chunks = []
            for item in items:
                local = dict(ctx)
                local[varname] = item
                chunks.append(self._vars(self._if(self._for(body, local), local), local))
            s = s[:m.start()] + "".join(chunks) + s[end_end:]
        return s

    def _eval(self, expr, ctx):
        # filter: "%02d"|format(n) / "%s"|format(s)
        m = re.match(r'^"([^"]+)"\|format\(([^)]+)\)$', expr)
        if m:
            fmt, var = m.group(1), m.group(2).strip()
            val = self._eval(var, ctx)
            try:
                if "d" in fmt:
                    return fmt % int(val)
                if "f" in fmt:
                    return fmt % float(val)
                return fmt % val
            except (TypeError, ValueError):
                return str(val)
        # attribute access: page.num / page.body_html
        if "." in expr:
            head, *rest = expr.split(".")
            val = ctx.get(head)
            for k in rest:
                if val is None:
                    return ""
                val = val.get(k) if isinstance(val, dict) else getattr(val, k, "")
            return val if val is not None else ""
        # plain var
        return ctx.get(expr, "")


# ====================================================================
# レポート組み立て
# ====================================================================
def build_pages_html(pages_spec):
    """
    pages_spec: [{'num': 2, 'body_html': '...'}, ...]
    そのまま template に渡せる構造に整える。num は 02 から始まる想定。
    """
    return list(pages_spec)


def build_context(spec, theme_id):
    """JSON 仕様 + テーマ ID から template 用 context dict を作る"""
    theme = get_theme(theme_id)
    brand = get_brand_assets(theme_id)

    pages = build_pages_html(spec.get("pages", []))
    page_total = len(pages) + 1  # cover を含めた総数

    ctx = {
        "doc_title": spec.get("doc_title", "ANSWER+ Premium レポート"),
        "theme_css": theme["css_file"],

        # ブランド表示
        "brand_wordmark":    spec.get("brand_wordmark",
                                      "esse-sense" if theme_id == "essesense" else "MIRA TUKU"),
        "brand_mark_top":    brand["brand_mark_top"],
        "brand_mark_header": brand["brand_mark_header"],
        "cover_logo":        brand["cover_logo"],

        # 表紙
        "badge_tag":     spec.get("badge_tag", "ADVISORY REPORT"),
        "badge_date":    spec.get("badge_date", f"ANSWER+ Premium ｜ {date.today().strftime('%Y年%m月')}"),
        "cover_eyebrow": spec.get("cover_eyebrow",
                                  f"ADVISORY REPORT　｜　{date.today().strftime('%B %Y').upper()}"),
        "cover_title_html":      spec.get("cover_title_html", "").replace("\n", "<br>"),
        "cover_en":              spec.get("cover_en", ""),
        "cover_subtitle":        spec.get("cover_subtitle", ""),
        "cover_for":             spec.get("cover_for", ""),
        "cover_meta_left_html":  spec.get("cover_meta_left_html", ""),
        "cover_meta_right_html": spec.get("cover_meta_right_html", ""),
        "org_name":              spec.get("org_name",
                                         "esse-sense" if theme_id == "essesense" else "NPO法人ミラツク"),

        # ヘッダー/フッター
        "header_title":    spec.get("header_title", spec.get("doc_title", "")),
        "header_subtitle": spec.get("header_subtitle", "ADVISORY REPORT"),
        "footer_jp":       spec.get("footer_jp", spec.get("doc_title", "")),

        # ページ
        "pages":      pages,
        "page_total": page_total,
    }
    return ctx, theme


def get_template_path(template_id):
    """report_templates テーブルから file_path を取得し絶対パス化。"""
    with db() as c:
        row = c.execute("SELECT file_path FROM report_templates WHERE template_id = ?",
                        (template_id,)).fetchone()
    if not row:
        return ROOT / "templates" / DEFAULT_TEMPLATE
    return ROOT / row["file_path"] if not row["file_path"].startswith("/") else Path(row["file_path"])


def render(spec, theme_id, template_id=None):
    ctx, theme = build_context(spec, theme_id)
    tpl_id = template_id or spec.get("template_id", "advisory-report-default")
    tpl_path = get_template_path(tpl_id)
    if not tpl_path.exists():
        sys.exit(f"[error] template file not found: {tpl_path}")
    src = tpl_path.read_text(encoding="utf-8")
    return Tpl(src).render(ctx), theme


# ====================================================================
# 履歴記録
# ====================================================================
def record_history(theme_id, template_id, output_path, title, spec):
    with db() as c:
        c.execute("""
            INSERT INTO generation_history (theme_id, template_id, output_path, title, source_data)
            VALUES (?, ?, ?, ?, ?)
        """, (theme_id, template_id, str(output_path), title,
              json.dumps(spec, ensure_ascii=False)[:8000]))
        c.commit()


# ====================================================================
# 自動判定 (heuristic routing)
#   入力テキスト or spec JSON からテーマ + テンプレを推定
#   - キーワードマッチによる重み付きスコアリング
#   - 構造シグナル (pages 数 / 章数 / 文字数 / フィールド組合せ) も加味
# ====================================================================
ROUTING_RULES = {
    # (theme, template): [ ("kw", weight), ... ]
    ("essesense", "advisory-report-default"): [
        ("esse-sense", 5), ("赤白CI", 4), ("純白", 3), ("株式会社", 3),
        ("外部企業", 4), ("クライアント向け", 4), ("役員向け", 3), ("事業判断", 3),
        ("アドバイザリー", 5), ("コンサル", 3), ("事業仮説", 3), ("進出戦略", 4),
        ("共同研究", 3), ("ANSWER+", 3), ("Premium", 2),
    ],
    ("miratuku", "advisory-report-default"): [
        ("ミラツク", 4), ("NPO法人", 5), ("warm cream", 5), ("wine", 3),
        ("進捗報告", 5), ("進捗書", 5), ("期内", 3), ("NPO 報告", 4),
        ("NOSIGNER", 4), ("公式進捗", 4), ("年次報告", 3),
    ],
    ("ep007", "journal-essay-ep007"): [
        ("連載", 4), ("kurashi", 5), ("keiei", 5), ("henka", 5), ("jigyo", 5),
        ("itonami", 5), ("futures", 4), ("ep007", 6), ("Judson", 4), ("drop cap", 4),
        ("DEEPER", 4), ("SIGNAL", 3), ("KEY REFERENCE", 4),
        ("QUESTION FOR NEXT", 4), ("第", 2), ("話", 2), ("散文", 3),
        ("ジャーナル", 3), ("読者向け", 3), ("エッセイ", 4),
    ],
    ("ep007", "series-top"): [
        ("連載トップ", 6), ("シリーズ案内", 5), ("PART 一覧", 5),
        ("全N話", 4), ("インデックス", 3), ("連載入口", 5), ("hero", 1),
    ],
    ("textbook", "textbook"): [
        ("教科書", 6), ("総説", 4), ("網羅的", 4), ("学習用", 4),
        ("章立て", 2), ("サイドバー目次", 5), ("ダーク切替", 4),
        ("大規模解説", 5), ("2万字", 4), ("textbook.html", 5),
    ],
    ("textbook", "dashboard"): [
        ("ダッシュボード", 6), ("DB可視化", 5), ("DB ダッシュボード", 6),
        ("集計", 3), ("指標一覧", 4), ("SVG 図解", 3),
    ],
}


def get_context_snapshot():
    """文脈情報を辞書で返す: 直近生成・最終テーマ・cwd・data/ 状態"""
    snapshot = {
        "cwd": str(Path.cwd()),
        "recent_generations": [],
        "last_theme": None,
        "last_template": None,
        "saved_specs": [],
        "theme_frequency": {},
    }
    with db() as c:
        rows = c.execute("""
            SELECT generated_at, theme_id, template_id, output_path, title
            FROM generation_history ORDER BY generated_at DESC LIMIT 10
        """).fetchall()
        for r in rows:
            snapshot["recent_generations"].append({
                "at": r["generated_at"], "theme": r["theme_id"],
                "template": r["template_id"], "title": r["title"] or "",
                "path": Path(r["output_path"]).name,
            })
        if rows:
            snapshot["last_theme"] = rows[0]["theme_id"]
            snapshot["last_template"] = rows[0]["template_id"]
        # テーマ別頻度 (直近 10 件)
        for r in rows:
            snapshot["theme_frequency"][r["theme_id"]] = \
                snapshot["theme_frequency"].get(r["theme_id"], 0) + 1
    # data/ に保存済みの spec 一覧
    snapshot["saved_specs"] = [p.stem for p in sorted(DATA_DIR.glob("*.json"))]
    return snapshot


def detect_route(text, use_context=True):
    """テキスト or spec JSON 文字列からテーマ+テンプレ候補をスコアリングして返す。
    use_context=True なら generation_history を直近活動シグナルとして加算する。"""
    # spec JSON が渡されたら値部分を抽出
    if text.strip().startswith("{"):
        try:
            spec = json.loads(text)
            blob = " ".join([str(v) for v in spec.values() if isinstance(v, (str, int, float))])
            blob += " " + " ".join(spec.keys())
            n_pages = len(spec.get("pages") or [])
            n_chapters = len(spec.get("chapters") or [])
            theme_hint = spec.get("theme", "")
            template_hint = spec.get("template_id") or spec.get("template", "")
        except json.JSONDecodeError:
            blob = text
            n_pages = n_chapters = 0
            theme_hint = template_hint = ""
    else:
        blob = text
        n_pages = n_chapters = 0
        theme_hint = template_hint = ""

    # 明示指定があれば最強優先
    if theme_hint and template_hint:
        return [((theme_hint, template_hint), 999, "明示指定 (spec.theme + spec.template_id)")], blob

    scores = {}
    matched = {}
    for (theme, tpl), rules in ROUTING_RULES.items():
        score = 0
        hits = []
        for kw, w in rules:
            if kw.lower() in blob.lower():
                score += w
                hits.append(kw)
        # 構造ボーナス
        if tpl == "advisory-report-default" and 8 <= n_pages <= 15:
            score += 3; hits.append(f"(pages={n_pages})")
        if tpl == "textbook" and (n_chapters >= 5 or n_pages >= 10):
            score += 3; hits.append(f"(chapters={n_chapters})")
        if tpl == "journal-essay-ep007" and n_pages == 1:
            score += 2; hits.append("(single-page essay)")
        # 明示テーマヒント
        if theme_hint == theme:
            score += 5
            hits.append("theme-hint")
        if template_hint == tpl:
            score += 5
            hits.append("template-hint")
        if score > 0:
            scores[(theme, tpl)] = score
            matched[(theme, tpl)] = hits

    # 文脈シグナル: generation_history を活動シグナルとして加算
    if use_context:
        ctx = get_context_snapshot()
        # 直近 10 件のテーマ頻度をスコアに反映 (max +3)
        for (theme, tpl), score in list(scores.items()):
            freq = ctx["theme_frequency"].get(theme, 0)
            if freq > 0:
                bonus = min(freq, 3)
                scores[(theme, tpl)] += bonus
                matched[(theme, tpl)].append(f"recent={freq}")
        # 「前と同じ」「いつも」「同じ形式」等の継続キューを検出
        cont_cues = ["前と同じ", "いつも", "同じ形式", "前回", "さっき", "this same"]
        if any(c in blob for c in cont_cues) and ctx["last_theme"]:
            key = (ctx["last_theme"], ctx["last_template"])
            scores[key] = scores.get(key, 0) + 8
            matched.setdefault(key, []).append(f"継続キュー → last={ctx['last_theme']}/{ctx['last_template']}")

    ranked = sorted(scores.items(), key=lambda x: -x[1])
    return [(k, v, ", ".join(matched[k])) for k, v in ranked], blob


def detect_print(text):
    """--detect サブコマンド出力"""
    ranked, _ = detect_route(text)
    if not ranked:
        print("[detect] no signal matched. fallback recommended: theme=essesense, template=advisory-report-default")
        return None, None
    print(f"{'#':<3}{'theme':<12}{'template':<32}{'score':<8}signals")
    print("-" * 100)
    for i, (route, score, hits) in enumerate(ranked[:5], 1):
        theme, tpl = route
        conf = "高" if score >= 12 else "中" if score >= 6 else "低"
        print(f"{i:<3}{theme:<12}{tpl:<32}{score:<5}[{conf}] {hits}")
    top = ranked[0][0]
    print()
    print(f"[recommended] theme={top[0]} / template={top[1]}")
    return top


def inject_edit_widget(html):
    """生成 HTML に統合ツールバー (PRINT + EDIT) と編集機能 JS を注入する。"""
    widget = '''
<!-- /repo unified toolbar (画面のみ・印刷時非表示) -->
<style>
.repo-toolbar {
  position: fixed; top: 18px; right: 18px; z-index: 9999;
  display: inline-flex; background: #FFFFFF;
  border: 1px solid rgba(18,18,18,0.16);
  box-shadow: 0 6px 20px rgba(0,0,0,0.14);
  font-family: "Inter", "Noto Sans JP", sans-serif; overflow: hidden;
}
.repo-toolbar button {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 16px; background: transparent; color: #121212;
  border: 0; border-right: 1px solid rgba(18,18,18,0.12);
  cursor: pointer; font: 600 12px/1.2 inherit; letter-spacing: 0.10em;
  transition: background 0.15s ease, color 0.15s ease;
}
.repo-toolbar button:last-child { border-right: 0; }
.repo-toolbar button:hover { background: rgba(204,20,0,0.06); color: #CC1400; }
.repo-toolbar button.is-primary { background: #CC1400; color: #FFFFFF; border-right-color: #CC1400; }
.repo-toolbar button.is-primary:hover { background: #A01000; color: #FFFFFF; }
.repo-toolbar button:focus-visible { outline: 2px solid #CC1400; outline-offset: -2px; }
.repo-toolbar small { display: block; font-size: 9px; letter-spacing: 0.20em; opacity: 0.85; font-weight: 500; margin-bottom: 2px; }
body.edit-mode [contenteditable="true"] { outline: 2px dashed #CC1400; outline-offset: 2px; cursor: text; }
body.edit-mode [contenteditable="true"]:hover { background: rgba(204,20,0,0.04); }
body.edit-mode [contenteditable="true"]:focus { background: rgba(204,20,0,0.08); outline-style: solid; }
@media print { .repo-toolbar { display: none !important; } }
</style>
<div class="repo-toolbar pr-no-print" role="toolbar" aria-label="レポートツールバー">
  <button type="button" class="is-primary" onclick="window.print()" aria-label="PDF として保存">
    <span><small>PRINT&nbsp;/&nbsp;PDF</small>保存</span>
  </button>
  <button type="button" onclick="toggleEdit()" aria-label="編集モード切替">
    <span><small>EDIT&nbsp;MODE</small><span id="editFabLabel">編集</span></span>
  </button>
</div>
<script>
(function(){
  // 編集対象: 表紙タイトル / chapter-title / lead / 段落 / 章番号 / メタ
  var EDITABLE_SEL = [
    ".pr-cover-title", ".pr-cover-subtitle", ".pr-cover-en", ".pr-cover-for-name",
    ".pr-cover-meta-left", ".pr-cover-meta-right",
    ".pr-chapter-title", ".pr-chapter-en", ".pr-section-label",
    ".pr-lead p", ".pr-body-text p", ".pr-qa-body", ".pr-qa-block h4",
    ".pr-info-value", ".pr-info-meta",
    ".pr-researcher-head", ".pr-researcher-affil", ".pr-researcher-theme", ".pr-researcher-note",
    ".pr-disclaimer-block", ".pr-sign-name", ".pr-sign-role",
    ".ep-hero-title", ".ep-hero-subtitle", ".ep-hero-lead", ".ep-body p",
    ".chapter-title", ".chapter-en"
  ].join(",");
  window.toggleEdit = function(){
    var on = document.body.classList.toggle("edit-mode");
    var lbl = document.getElementById("editFabLabel");
    if (lbl) lbl.textContent = on ? "終了 (⌘S 保存)" : "編集";
    document.querySelectorAll(EDITABLE_SEL).forEach(function(el){
      el.setAttribute("contenteditable", on ? "true" : "false");
    });
    if (on) {
      window.addEventListener("keydown", saveOnCmdS);
      console.log("[/repo edit] 編集モード ON。Cmd+S で HTML を再ダウンロード。");
    } else {
      window.removeEventListener("keydown", saveOnCmdS);
    }
  };
  function saveOnCmdS(e){
    if ((e.metaKey || e.ctrlKey) && e.key === "s") {
      e.preventDefault();
      // contenteditable=false に戻してから出力 (ノイズ排除)
      document.querySelectorAll('[contenteditable]').forEach(function(el){
        el.removeAttribute("contenteditable");
      });
      document.body.classList.remove("edit-mode");
      var html = "<!DOCTYPE html>\\n" + document.documentElement.outerHTML;
      var blob = new Blob([html], {type:"text/html;charset=utf-8"});
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      var stem = (location.pathname.split("/").pop() || "report.html").replace(/\\.html$/, "");
      var ts = new Date().toISOString().replace(/[:.]/g,"-").slice(0,19);
      a.download = stem + "-edited-" + ts + ".html";
      a.click();
      console.log("[/repo edit] HTML をダウンロードしました: " + a.download);
      // 編集モード再ON (作業継続のため)
      setTimeout(toggleEdit, 100);
    }
  }
})();
</script>
'''
    if "</body>" in html:
        return html.replace("</body>", widget + "\n</body>")
    return html + widget


def save_spec(slug, spec):
    """生成元 spec を data/<slug>.json に保存（編集機能用）"""
    spec_path = DATA_DIR / f"{slug}.json"
    spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    return spec_path


def load_spec(slug):
    """data/<slug>.json から spec を読み出す"""
    spec_path = DATA_DIR / f"{slug}.json"
    if not spec_path.exists():
        sys.exit(f"[error] saved spec not found: {spec_path}\n"
                 f"  list available with: build_report.py --list-saved")
    return json.loads(spec_path.read_text(encoding="utf-8")), spec_path


def list_saved():
    """data/*.json と generation_history を結合して履歴表示"""
    saved = sorted(DATA_DIR.glob("*.json"))
    if not saved:
        print("[info] no saved specs in data/")
        return
    print(f"{'slug':<40}{'theme':<12}{'template':<32}generated")
    print("-" * 110)
    with db() as c:
        for p in saved:
            slug = p.stem
            try:
                spec = json.loads(p.read_text(encoding="utf-8"))
                theme = spec.get("theme", "?")
                tpl = spec.get("template_id", spec.get("template", "?"))
            except Exception:
                theme, tpl = "?", "?"
            row = c.execute("""
                SELECT generated_at FROM generation_history
                WHERE output_path LIKE ? ORDER BY generated_at DESC LIMIT 1
            """, (f"%{slug}%",)).fetchone()
            gen = row["generated_at"] if row else "(never)"
            print(f"{slug:<40}{theme:<12}{tpl:<32}{gen}")


def edit_spec(slug):
    """spec を $EDITOR で開く。保存後 regenerate するか確認"""
    import subprocess
    spec, spec_path = load_spec(slug)
    editor = os.environ.get("EDITOR") or os.environ.get("VISUAL") or "vim"
    print(f"[edit] opening {spec_path} in {editor}")
    subprocess.run([editor, str(spec_path)])
    print(f"[edit] saved. Run regenerate to apply: ")
    print(f"  python3 {Path(__file__).name} --regenerate {slug} --open")


def edit_set(slug, key_path, value):
    """spec の特定キーを inline 更新 (dot-path 対応)"""
    spec, spec_path = load_spec(slug)
    keys = key_path.split(".")
    target = spec
    for k in keys[:-1]:
        if isinstance(target, list):
            target = target[int(k)]
        else:
            target = target.setdefault(k, {})
    last = keys[-1]
    # 値の型を推測 (JSON parseable → as-is, else string)
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        parsed = value
    if isinstance(target, list):
        target[int(last)] = parsed
    else:
        target[last] = parsed
    spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[ok] set {key_path} = {parsed!r}  in {spec_path}")


def regenerate(slug, theme_override=None, template_override=None, open_after=False,
               no_editable=False):
    """data/<slug>.json から再生成"""
    spec, _ = load_spec(slug)
    theme_id = theme_override or spec.get("theme", "essesense")
    # spec に保存されている _output_path があれば優先 (theme-suffix を再現)
    out_hint = spec.get("_output_path")
    out_path = Path(out_hint) if out_hint else (REPORTS_DIR / f"{slug}.html")
    html, theme = render(spec, theme_id, template_override)
    if not no_editable:
        html = inject_edit_widget(html)
    out_path.write_text(html, encoding="utf-8")
    print(f"[ok] regenerated {out_path}  (theme={theme_id})")
    record_history(theme_id, template_override or spec.get("template_id", "advisory-report-default"),
                   out_path, spec.get("doc_title", ""), spec)
    if open_after:
        import subprocess
        subprocess.run(["open", str(out_path)])


# ====================================================================
# CLI
# ====================================================================
def main():
    ap = argparse.ArgumentParser(description="/repo report generator")
    ap.add_argument("--input", "-i", help="input JSON spec file")
    ap.add_argument("--output", "-o", help="output HTML file (default: reports/<slug>.html)")
    ap.add_argument("--theme", "-t", default="essesense",
                    help="theme id (miratuku / essesense / ep007 / textbook). default: essesense")
    ap.add_argument("--template", default=None,
                    help="report template id (advisory-report-default / journal-essay-ep007 / series-top / textbook / dashboard)")
    ap.add_argument("--slug", help="slug for default output filename")
    ap.add_argument("--list-themes",    action="store_true", help="list available themes")
    ap.add_argument("--list-templates", action="store_true", help="list available report templates")
    ap.add_argument("--list-rules", nargs="?", const="*", metavar="THEME_ID",
                    help="list design rules (optionally filtered by theme)")
    ap.add_argument("--list-components", action="store_true", help="list available components")
    ap.add_argument("--list-saved",     action="store_true", help="list saved specs in data/")
    # 編集機能
    ap.add_argument("--edit", metavar="SLUG", help="open saved spec in $EDITOR")
    ap.add_argument("--edit-set", nargs=3, metavar=("SLUG","KEY","VALUE"),
                    help="set spec field by dot-path (e.g. cover_title_html '新タイトル')")
    ap.add_argument("--regenerate", metavar="SLUG", help="regenerate HTML from saved spec")
    ap.add_argument("--retrofit", metavar="HTML_PATH",
                    help="既存 HTML に編集 widget を後付け注入する (in-place 書換)")
    ap.add_argument("--detect", metavar="DESCRIPTION_OR_JSON",
                    help="入力テキストまたは JSON spec からテーマ+テンプレを自動判定")
    ap.add_argument("--auto", action="store_true",
                    help="--input と併用: theme/template を auto-detect して生成")
    ap.add_argument("--context", action="store_true",
                    help="現在の文脈情報を出力 (直近生成 / 最終テーマ / data/ 状態 / cwd)")
    ap.add_argument("--open", action="store_true", help="open output in default browser")
    ap.add_argument("--no-editable", action="store_true",
                    help="disable in-browser inline editing toggle (default: enabled)")
    args = ap.parse_args()

    if args.list_themes:     list_themes();      return
    if args.list_templates:  list_templates();   return
    if args.list_components: list_components();  return
    if args.list_saved:      list_saved();       return
    if args.list_rules:
        list_rules(None if args.list_rules == "*" else args.list_rules); return

    # 編集系
    if args.edit:
        edit_spec(args.edit); return
    if args.edit_set:
        slug, key, val = args.edit_set
        edit_set(slug, key, val); return
    if args.regenerate:
        regenerate(args.regenerate, args.theme if args.theme != "essesense" else None,
                   args.template, open_after=args.open, no_editable=args.no_editable); return
    if args.context:
        ctx = get_context_snapshot()
        print(f"[context] cwd: {ctx['cwd']}")
        print(f"[context] 最終テーマ: {ctx['last_theme'] or '(なし)'} / 最終テンプレ: {ctx['last_template'] or '(なし)'}")
        print(f"[context] 直近 10 件テーマ頻度: {ctx['theme_frequency']}")
        print(f"[context] data/ 保存済み spec: {len(ctx['saved_specs'])} 件")
        for slug in ctx["saved_specs"][:10]:
            print(f"  - {slug}")
        print(f"[context] 直近生成履歴:")
        for g in ctx["recent_generations"][:10]:
            print(f"  {g['at'][:16]}  {g['theme']:<11}{g['template']:<32}{g['title'][:40]}")
        return

    if args.detect:
        # ファイルパスなら読み込み、テキストならそのまま
        p = Path(args.detect)
        text = p.read_text(encoding="utf-8") if p.exists() and p.suffix == ".json" else args.detect
        detect_print(text); return

    if args.retrofit:
        retrofit_path = Path(args.retrofit)
        if not retrofit_path.exists():
            sys.exit(f"[error] HTML file not found: {retrofit_path}")
        original = retrofit_path.read_text(encoding="utf-8")
        # 既存 widget (新旧両方) を除去してから注入 (冪等)
        cleaned = re.sub(
            r'\n?<!-- /repo (edit widget|unified toolbar)[\s\S]*?</script>\n?',
            '', original, count=1)
        # 旧 .print-fab ボタンも除去
        cleaned = re.sub(
            r'\n?<!-- 画面のみ.*?-->\s*<button[^>]*class="print-fab[^"]*"[\s\S]*?</button>\n?',
            '', cleaned, count=1)
        updated = inject_edit_widget(cleaned)
        retrofit_path.write_text(updated, encoding="utf-8")
        print(f"[ok] retrofitted edit widget into {retrofit_path}")
        if args.open:
            import subprocess
            subprocess.run(["open", str(retrofit_path)])
        return

    if not args.input:
        ap.error("--input is required (or use --list-themes / --list-rules)")

    input_path = Path(args.input)
    if not input_path.exists():
        sys.exit(f"[error] input file not found: {input_path}")
    try:
        spec = json.loads(input_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"[error] invalid JSON in {input_path}: line {e.lineno}, col {e.colno}: {e.msg}")
    except OSError as e:
        sys.exit(f"[error] cannot read {input_path}: {e}")

    # --auto: テーマ+テンプレを spec から自動判定
    if args.auto:
        ranked, _ = detect_route(json.dumps(spec, ensure_ascii=False))
        if ranked and ranked[0][1] >= 3:
            top_theme, top_tpl = ranked[0][0]
            if not args.theme or args.theme == "essesense":  # default 値の上書きのみ
                args.theme = top_theme
            if not args.template:
                args.template = top_tpl
            print(f"[auto] detected theme={top_theme} / template={top_tpl} (score={ranked[0][1]})")
        else:
            print(f"[auto] no strong signal. using defaults (theme={args.theme}, template=advisory-report-default)")

    # テーマ上書き (JSON 側でも指定可能、CLI 引数が優先)
    theme_id = args.theme or spec.get("theme", "essesense")

    # 出力先決定
    if args.output:
        out_path = Path(args.output)
    else:
        slug = args.slug or spec.get("slug") or Path(args.input).stem
        suffix = "-essesense" if theme_id == "essesense" else "-miratuku"
        out_path = REPORTS_DIR / f"{slug}{suffix}.html"

    html, theme = render(spec, theme_id, args.template)
    if not args.no_editable:
        html = inject_edit_widget(html)
    out_path.write_text(html, encoding="utf-8")
    tpl_id = args.template or spec.get("template_id", "advisory-report-default")
    print(f"[ok] wrote {out_path}  (theme={theme_id}, template={tpl_id}, pages={len(spec.get('pages', []))+1})")

    # 編集機能: spec を data/<slug>.json に保存 (output_path も埋め込んで再生成時に再現)
    saved_slug = args.slug or spec.get("slug") or input_path.stem
    spec_to_save = dict(spec)
    spec_to_save["_output_path"] = str(out_path)
    spec_to_save["theme"] = theme_id
    spec_to_save["template_id"] = tpl_id
    spec_path = save_spec(saved_slug, spec_to_save)
    print(f"[edit] spec saved → {spec_path}")
    print(f"       edit:       python3 {Path(__file__).name} --edit {saved_slug}")
    print(f"       regenerate: python3 {Path(__file__).name} --regenerate {saved_slug} --open")

    record_history(theme_id, tpl_id, out_path, spec.get("doc_title", ""), spec)

    if args.open:
        import subprocess
        subprocess.run(["open", str(out_path)])


if __name__ == "__main__":
    main()

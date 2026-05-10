#!/usr/bin/env python3
"""
Re-theme all SVG colors in deep-knowledge-book v2 to be theme-aware.
Replaces hardcoded fill/stroke values with CSS variables that switch on data-theme.
Also rewrites the figure CSS so SVG inserts blend with dark/light themes.
"""
import re
from pathlib import Path

DST = Path("/tmp/journal-upload/deep-knowledge/index.html")
content = DST.read_text(encoding="utf-8")

# 1) Inject SVG-aware CSS variables into :root and [data-theme="light"]
new_root_vars = """
  /* === SVG diagram tokens (theme-aware) === */
  --svg-bg:       transparent;
  --svg-card:     #261C16;
  --svg-card-alt: #1F1612;
  --svg-text:     #F2EDE6;
  --svg-text-2:   #C9C2B8;
  --svg-text-3:   #8E867D;
  --svg-line:     #4A3A2C;
  --svg-line-soft:#2E2218;
}"""
# Replace the closing brace of :root with our additions (before the closing })
content = content.replace(
    "  --green: var(--mt-10);\n  --orange: var(--mt-9);\n  --blue: var(--mt-12);\n}",
    "  --green: var(--mt-10);\n  --orange: var(--mt-9);\n  --blue: var(--mt-12);\n" + new_root_vars,
    1,
)

# Insert into [data-theme="light"] block
light_extra = """  --svg-bg:       transparent;
  --svg-card:     #FFFFFF;
  --svg-card-alt: #FAF6F0;
  --svg-text:     #2A1F18;
  --svg-text-2:   #5A4838;
  --svg-text-3:   #8B7A66;
  --svg-line:     #D9CFBF;
  --svg-line-soft:#E8E0D0;
"""
content = re.sub(
    r'(\[data-theme="light"\] \{[^}]*?--surface:\s*#F2EBDD;\s*)\}',
    r'\1\n' + light_extra + '}',
    content,
    count=1,
    flags=re.DOTALL,
)

# 2) Rewrite figure CSS so SVGs blend with the dark page (warm card)
old_figure_css = '''figure {
  margin: 36px 0;
  background: #FFFFFF;
  border: 1px solid var(--line);
  border-radius: 2px;
  padding: 28px 24px 22px;
  box-shadow: 0 4px 18px rgba(0,0,0,0.18);
}
[data-theme="light"] figure { background: #FFFFFF; box-shadow: 0 2px 10px rgba(122, 64, 51, 0.08); }
figure svg { display: block; margin: 0 auto; }
figure figcaption {
  font-family: var(--sans) !important; font-size: 0.82rem !important;
  color: #555 !important; margin-top: 16px !important;
  letter-spacing: 0.04em !important; text-align: center;
  border-top: 1px dashed #D9D9D9; padding-top: 12px;
}'''
new_figure_css = '''figure {
  margin: 36px 0;
  background: var(--bg-soft);
  border: 1px solid var(--line);
  border-radius: 2px;
  padding: 28px 24px 22px;
  box-shadow: 0 4px 18px rgba(0,0,0,0.18);
  color: var(--svg-text);
}
[data-theme="light"] figure { background: #FFFFFF; box-shadow: 0 2px 10px rgba(122, 64, 51, 0.08); }
figure svg { display: block; margin: 0 auto; }
figure svg text, figure svg tspan { font-family: var(--serif); }
figure figcaption {
  font-family: var(--sans) !important; font-size: 0.82rem !important;
  color: var(--svg-text-2) !important; margin-top: 16px !important;
  letter-spacing: 0.04em !important; text-align: center;
  border-top: 1px dashed var(--svg-line); padding-top: 12px;
}'''
content = content.replace(old_figure_css, new_figure_css, 1)

# 3) Replace SVG fills/strokes with theme tokens.
# Strategy: only replace inside <svg>...</svg> blocks to avoid touching CSS or non-SVG hex codes.
def replace_in_svg(svg_text):
    s = svg_text
    # Light text/lines (text-1 / text-2 / text-3)
    repls = [
        # Solid colors
        (r'fill="#121212"',     r'fill="var(--svg-text)"'),
        (r'stroke="#121212"',   r'stroke="var(--svg-text)"'),
        (r'fill="#555555"',     r'fill="var(--svg-text-2)"'),
        (r'fill="#555"',        r'fill="var(--svg-text-2)"'),
        (r'fill="#666"',        r'fill="var(--svg-text-2)"'),
        (r'stroke="#666"',      r'stroke="var(--svg-text-2)"'),
        (r'fill="#6B6B6B"',     r'fill="var(--svg-text-2)"'),
        (r'fill="#888"',        r'fill="var(--svg-text-3)"'),
        (r'stroke="#888"',      r'stroke="var(--svg-text-3)"'),
        (r'fill="#999"',        r'fill="var(--svg-text-3)"'),
        (r'stroke="#999"',      r'stroke="var(--svg-text-3)"'),
        (r'fill="#444"',        r'fill="var(--svg-text-2)"'),
        (r'stroke="#444"',      r'stroke="var(--svg-text-2)"'),
        # Light fills (white circles, card backgrounds inside SVG)
        (r'fill="#FFFFFF"',     r'fill="var(--svg-card)"'),
        (r'fill="#FFF"',        r'fill="var(--svg-card)"'),
        (r'fill="#fff"',        r'fill="var(--svg-card)"'),
        (r'stroke="#FFFFFF"',   r'stroke="var(--svg-card)"'),
        (r'stroke="#FFF"',      r'stroke="var(--svg-card)"'),
        # Light borders
        (r'stroke="#D9D9D9"',   r'stroke="var(--svg-line)"'),
    ]
    for pat, rep in repls:
        s = re.sub(pat, rep, s)
    return s

# Iterate over each <svg ...>...</svg> block and apply replacements
def svg_block_sub(m):
    return replace_in_svg(m.group(0))

content = re.sub(r'<svg\b.*?</svg>', svg_block_sub, content, flags=re.DOTALL)

DST.write_text(content, encoding="utf-8")

# Verify
hardcoded = re.findall(r'<svg\b.*?</svg>', content, flags=re.DOTALL)
remaining = []
for blk in hardcoded:
    for pat in [r'fill="#121212"', r'fill="#555"', r'fill="#FFFFFF"', r'fill="#FFF"', r'fill="#fff"',
                r'stroke="#121212"', r'fill="#888"', r'fill="#999"', r'fill="#666"']:
        m = re.findall(pat, blk)
        if m:
            remaining.append((pat, len(m)))

print(f"Total SVGs: {len(hardcoded)}")
print(f"Remaining hardcoded values inside SVGs: {sum(n for _, n in remaining)}")
for pat, n in remaining[:10]:
    print(f"  {pat}: {n}")
print(f"Output size: {DST.stat().st_size:,} bytes")

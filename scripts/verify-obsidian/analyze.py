#!/usr/bin/env python3
"""Analyze a run.mjs result: Reading-vs-Live-Preview mismatches and text contrast.

Usage: python3 scripts/verify-obsidian/analyze.py [.verify]
Prints a report, writes <dir>/index.html (findings, contrast table, screenshot pairs),
and exits 1 if any checked property differs between the two views.
"""
import html
import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else ".verify")
RUN = json.loads((OUT / "measure.json").read_text())
DATA = RUN["data"]

# element -> properties that must match between Reading view and Live Preview
CHECK = {
    **{f"h{i}": ["font-size", "color"] for i in range(1, 7)},
    "hr": ["border-top-width", "border-top-color"],
    "codeFrame": ["background-color", "border-top-width", "border-top-color", "border-top-left-radius"],
    "codeText": ["font-size", "font-family", "line-height", "color"],
    "inlineCode": ["font-size", "font-family", "color", "background-color", "border-top-width",
                   "border-top-color", "border-top-left-radius", "padding-top", "padding-left"],
    "th": ["font-size", "color"], "td": ["font-size", "color"],
    "cellPad": ["padding-top", "padding-left"], "tdCode": ["font-size"],
    "tag": ["font-size", "color", "background-color"],
    "quoteRule": ["border-left-width", "border-left-color"], "quoteText": ["color"],
    "mark": ["color", "background-color"], "link": ["color"], "unresolved": ["color"],
    "calloutNote": ["color"], "calloutNoteBg": ["background-color"],
}
LABELS = {"body": "正文", **{f"h{i}": f"H{i}" for i in range(1, 7)}, "link": "链接", "unresolved": "失效链接",
          "quoteText": "引用", "inlineCode": "行内代码", "codeText": "代码块", "mark": "高亮", "tag": "标签",
          "th": "表头", "td": "表格", "calloutNote": "Note 标题"}
FAINT = {"unresolved", "h6"}          # de-emphasized text: flag below 3.0 instead of 4.3


def rgba(s):
    n = [float(x) for x in re.findall(r"[\d.]+", s or "")]
    return (n + [1.0])[:4] if len(n) >= 3 else None


def over(fg, bg):
    a = fg[3]
    return [fg[i] * a + bg[i] * (1 - a) for i in range(3)] + [1.0]


def contrast(a, b):
    def lum(c):
        ch = [v / 255 for v in c[:3]]
        ch = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in ch]
        return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]
    x, y = sorted([lum(a), lum(b)], reverse=True)
    return (x + 0.05) / (y + 0.05)


themes = {p.stem: tomllib.loads(p.read_text()) for p in (ROOT / "shared/palettes").glob("*.toml")}


def variant_info(cls):
    prefix, slug = cls.split("-", 1)
    t = next(t for t in themes.values() if t["prefix"] == prefix)
    v = next(v for v in t["variants"] if v["slug"] == slug)
    return t["name"], v["label"], v["palette"]["bg"]


# --- 1. consistency
mismatches = []
for v in [x["cls"] for x in RUN["variants"]]:
    r, l = DATA[f"{v}/reading"], DATA[f"{v}/live"]
    for el, props in CHECK.items():
        for p in props:
            a, b = (r.get(el) or {}).get(p), (l.get(el) or {}).get(p)
            if a is None and b is None:
                continue
            if a is None or b is None or a.replace(" ", "") != b.replace(" ", ""):
                mismatches.append((v, el, p, a, b))
    full = [bool(t and t.get("width") == t.get("parentWidth")) for t in (r.get("table"), l.get("table"))]
    if full[0] != full[1]:
        mismatches.append((v, "table", "width", "full" if full[0] else "content", "full" if full[1] else "content"))

# --- 2. contrast (Reading view, against the variant's real page background)
contrast_rows = []
for v in [x["cls"] for x in RUN["variants"]]:
    theme, label, bg_hex = variant_info(v)
    page = [int(bg_hex[i:i + 2], 16) for i in (1, 3, 5)] + [1.0]
    r = DATA[f"{v}/reading"]

    def c(el, bg_from=None):
        fg = rgba((r.get(el) or {}).get("color"))
        if not fg:
            return None
        bg = page
        if bg_from and (src := rgba((r.get(bg_from[0]) or {}).get(bg_from[1]))):
            bg = over(src, page)
        return round(contrast(over(fg, bg), bg), 2)

    vals = {"body": c("body"), **{h: c(h) for h in [f"h{i}" for i in range(1, 7)]}, "link": c("link"),
            "unresolved": c("unresolved"), "quoteText": c("quoteText"),
            "inlineCode": c("inlineCode", ("inlineCode", "background-color")),
            "codeText": c("codeText", ("codeFrame", "background-color")),
            "mark": c("mark", ("mark", "background-color")), "tag": c("tag", ("tag", "background-color")),
            "th": c("th"), "td": c("td"), "calloutNote": c("calloutNote", ("calloutNoteBg", "background-color"))}
    vals = {k: x for k, x in vals.items() if x}
    low = sorted([(k, x) for k, x in vals.items() if x < (3.0 if k in FAINT else 4.3)], key=lambda kv: kv[1])
    contrast_rows.append((v, theme, label, vals.get("body"), min(vals.items(), key=lambda kv: kv[1]), low))

# --- text report
print(f"Reading vs Live Preview: {len(mismatches)} mismatch(es) across {len(RUN['variants'])} variant(s)")
for v, el, p, a, b in mismatches:
    print(f"  {v:16} {el:12} {p:22} reading={a}  live={b}")
print("\nContrast (Reading view):")
for v, theme, label, body, (mk, mv), low in contrast_rows:
    print(f"  {v:16} body {body}  min {LABELS[mk]} {mv}  " + (", ".join(f"{LABELS[k]} {x}" for k, x in low) or "ok"))

# --- HTML report
SECTIONS = [("top", "标题"), ("text", "文字样式与链接"), ("quote-code", "引用与代码"), ("tables", "表格"),
            ("callouts", "Callout"), ("tags", "标签与表格内格式")]
esc = html.escape
mm_html = ("".join(f"<tr><td>{esc(v)}</td><td>{esc(el)}</td><td><code>{esc(p)}</code></td><td>{esc(str(a))}</td><td>{esc(str(b))}</td></tr>"
                   for v, el, p, a, b in mismatches)
           if mismatches else '<tr><td colspan="5"><span class="pill ok">无差异</span></td></tr>')
ct_html = "".join(
    f"<tr><td>{esc(theme)} · {esc(label)}</td><td>{body}</td><td>{LABELS[mk]} {mv}</td><td>"
    + ("、".join(f'<span class="{"lowfaint" if k in FAINT else "low"}">{LABELS[k]} {x}</span>' for k, x in low)
       or '<span class="pill ok">无</span>') + "</td></tr>"
    for v, theme, label, body, (mk, mv), low in contrast_rows)
groups = {}
for x in RUN["variants"]:
    theme, label, _ = variant_info(x["cls"])
    groups.setdefault(theme, []).append(f'<button class="v" type="button" data-v="{x["cls"]}" aria-pressed="false">{esc(label)}</button>')
picker = "".join(f'<div class="group"><span class="lbl">{esc(t)}</span>{"".join(b)}</div>' for t, b in groups.items())
first = RUN["variants"][0]["cls"]
# only sections whose screenshots exist (a heading missing from the note is skipped by run.mjs)
available = {x["cls"]: [k for k, _ in SECTIONS if (OUT / "shots" / f"{x['cls']}-reading-{k}.png").exists()]
             for x in RUN["variants"]}
page = f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mod 主题渲染核验</title>
<style>
:root {{ --bg:#f3f4f6; --surface:#fff; --ink:#1d2330; --muted:#5d6576; --line:#d9dde5; --accent:#3b5bdb;
  --ok:#2f7d4f; --warn:#a3620b; --bad:#b4232c; --chip:#e8ebf2;
  --font:"IBM Plex Sans","PingFang SC","Hiragino Sans GB",system-ui,sans-serif; --mono:"JetBrains Mono",ui-monospace,Menlo,monospace; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#15181f; --surface:#1d212b; --ink:#e3e6ee; --muted:#9aa2b4; --line:#2e3442;
  --accent:#8ea6ff; --ok:#6fcf97; --warn:#e3b25e; --bad:#f08a8f; --chip:#272c38; color-scheme:dark; }} }}
body {{ margin:0; background:var(--bg); color:var(--ink); font:15px/1.65 var(--font); padding:32px max(16px,env(safe-area-inset-left)); }}
.wrap {{ max-width:1240px; margin:0 auto; display:grid; gap:36px; }}
h1 {{ font-size:1.75rem; margin:0; font-weight:600; }} h2 {{ font-size:1.2rem; margin:0 0 10px; font-weight:600; }}
h3 {{ font-size:.8rem; margin:0; letter-spacing:.06em; text-transform:uppercase; color:var(--muted); }}
.meta {{ color:var(--muted); font-size:.9rem; margin:6px 0 0; }} code {{ font-family:var(--mono); font-size:.86em; }}
.box {{ overflow-x:auto; background:var(--surface); border:1px solid var(--line); border-radius:10px; }}
table {{ border-collapse:collapse; width:100%; font-size:.88rem; font-variant-numeric:tabular-nums; }}
th,td {{ text-align:left; padding:8px 12px; border-bottom:1px solid var(--line); vertical-align:top; }}
th {{ color:var(--muted); font-size:.78rem; }} tr:last-child td {{ border-bottom:none; }}
.low {{ color:var(--bad); white-space:nowrap; }} .lowfaint {{ color:var(--warn); white-space:nowrap; }}
.pill {{ font-size:.75rem; font-weight:600; padding:2px 8px; border-radius:999px; background:var(--chip); }} .ok {{ color:var(--ok); }}
.picker {{ display:grid; gap:10px; margin-bottom:20px; }} .group {{ display:flex; flex-wrap:wrap; gap:8px; align-items:center; }}
.lbl {{ width:9.5em; color:var(--muted); font-size:.85rem; }}
button.v {{ font:inherit; font-size:.85rem; padding:5px 12px; border-radius:999px; border:1px solid var(--line); background:var(--surface); color:var(--ink); cursor:pointer; }}
button.v[aria-pressed="true"] {{ background:var(--accent); border-color:var(--accent); color:var(--surface); }}
#gallery {{ display:grid; gap:28px; }} .pair {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-top:10px; }}
figure {{ margin:0; display:grid; gap:6px; min-width:0; }} figcaption {{ font-size:.8rem; color:var(--muted); }}
img {{ width:100%; height:auto; border:1px solid var(--line); border-radius:8px; display:block; }}
@media (max-width:760px) {{ .pair {{ grid-template-columns:1fr; }} .lbl {{ width:100%; }} }}
</style>
<div class="wrap">
<header><h1>Mod 主题渲染核验</h1>
<p class="meta">测试笔记 <code>{esc(RUN["note"])}</code> · {len(RUN["variants"])} 个变体 × 阅读视图 / 编辑视图</p></header>
<section><h2>阅读视图 vs 编辑视图差异</h2><div class="box"><table>
<thead><tr><th>变体</th><th>元素</th><th>属性</th><th>阅读视图</th><th>编辑视图</th></tr></thead><tbody>{mm_html}</tbody></table></div></section>
<section><h2>阅读视图对比度</h2><p class="meta">正文类低于 4.3:1 标红，H6 与失效链接低于 3:1 标黄；标签、高亮、callout 标题、代码按各自底色叠加后计算。</p>
<div class="box"><table><thead><tr><th>变体</th><th>正文</th><th>最低项</th><th>偏低项</th></tr></thead><tbody>{ct_html}</tbody></table></div></section>
<section><h2>截图对比</h2><div class="picker" id="picker">{picker}</div><div id="gallery"></div></section>
</div>
<script>
const SECTIONS = {json.dumps(SECTIONS, ensure_ascii=False)}, AVAILABLE = {json.dumps(available)};
function show(v) {{
  document.querySelectorAll('button.v').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.v === v)));
  document.getElementById('gallery').innerHTML = SECTIONS.filter(([k]) => AVAILABLE[v].includes(k)).map(([k, n]) => `<div><h3>${{n}}</h3><div class="pair">
    <figure><img loading="lazy" src="shots/${{v}}-reading-${{k}}.png" alt=""><figcaption>阅读视图</figcaption></figure>
    <figure><img loading="lazy" src="shots/${{v}}-live-${{k}}.png" alt=""><figcaption>编辑视图（Live Preview）</figcaption></figure></div></div>`).join('');
}}
document.getElementById('picker').addEventListener('click', e => {{ const b = e.target.closest('button.v'); if (b) show(b.dataset.v); }});
show({json.dumps(first)});
</script>
"""
(OUT / "index.html").write_text(page)
print(f"\nReport: {OUT / 'index.html'}")
sys.exit(1 if mismatches else 0)

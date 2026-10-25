#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Generate every theme file from shared/palettes/<palette>.toml, shared/lamplit.toml
and scripts/templates/.

Outputs (never edit by hand — edit the TOML or the templates, then rerun):
    typora/<palette>/<palette>-mod-<variant>.css    one Typora theme per palette variant
    obsidian/lamplit/theme.css + manifest.json      one Obsidian theme, every palette as a scheme

Usage:
    ./scripts/gen-themes.py            # (re)write all outputs
    ./scripts/gen-themes.py --check    # exit 1 if any output is stale

Template placeholders:
    {{c:NAME}}    var(--<prefix>-<color>)     NAME = role, canonical color, or palette name
    {{rgb:NAME}}  var(--<prefix>-<color>-rgb)
    {{hex:NAME}}  the color's literal hex value
    {{r:NAME}}    a role's literal value (alphas, shadows, ...)
    {{UPPER}}     file-level values (theme name, version, palette block, ...)
    {{#KEY=VALUE}} ... {{/KEY}}   kept only when role KEY equals VALUE
"""
import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PALETTES = ROOT / "shared/palettes"
TEMPLATES = ROOT / "scripts/templates"
HEADINGS = ["h1", "h2", "h3", "h4", "h5", "h6"]


def rgb_triple(hex_color: str) -> str:
    return ", ".join(str(int(hex_color[i:i + 2], 16)) for i in (1, 3, 5))


class Ctx:
    """Name resolution for one variant on one platform."""

    def __init__(self, theme: dict, variant: dict, platform: str):
        self.theme, self.variant, self.p = theme, variant, theme["prefix"]
        self.roles = dict(theme["roles"])
        self.roles.update(zip(HEADINGS, theme["roles"]["headings"]))
        self.roles.update(variant.get("overrides", {}))
        self.roles.update(variant.get(f"{platform}_overrides", {}))
        self.aliases = theme.get("aliases", {})
        self.palette = variant["palette"]

    def color(self, name: str) -> str:
        """Role / canonical / palette name -> palette color name."""
        seen = set()
        while name in self.roles and name not in seen and name not in self.palette:
            seen.add(name)
            name = self.roles[name]
        name = self.aliases.get(name, name)
        if name not in self.palette and name != "mark-bg":
            raise KeyError(f"{self.theme['slug']}/{self.variant['slug']}: no color '{name}'")
        return name

    def hex(self, name: str) -> str:
        return self.palette[self.color(name)]

    def rgb(self, name: str) -> str:
        c = self.color(name)
        if c not in self.theme["rgb"]:
            raise KeyError(f"{self.theme['slug']}: '{c}' needs to be listed in rgb = [...]")
        return f"var(--{self.p}-{c}-rgb)"

    def palette_lines(self, indent: str) -> list[str]:
        p, rows = self.p, []
        for name, value in self.palette.items():
            rows.append((f"--{p}-{name}", value))
        yellow = self.palette[self.aliases.get("yellow", "yellow")]
        rows.append((f"--{p}-mark-bg", f"rgba({rgb_triple(yellow)}, {self.roles['mark_alpha']})"))
        for name in self.theme["rgb"]:
            rows.append((f"--{p}-{name}-rgb", rgb_triple(self.palette[name])))
        width = max(len(k) for k, _ in rows) + 1
        return [f"{indent}{(k + ':').ljust(width)} {v};" for k, v in rows]

    def render(self, template: str, extra: dict) -> str:
        def cond(m):
            key, want, body = m.group(1), m.group(2), m.group(3)
            return body if str(self.roles.get(key)) == want else ""

        out = re.sub(r"\{\{#([\w-]+)=([\w-]+)\}\}\n?(.*?)\{\{/\1\}\}\n?", cond, template, flags=re.S)

        def sub(m):
            kind, _, name = m.group(1).partition(":")
            if not name:
                return extra[kind]
            if kind == "c":
                return f"var(--{self.p}-{self.color(name)})"
            if kind == "rgb":
                return self.rgb(name)
            if kind == "hex":
                return self.hex(name)
            if kind == "r":   # role values may themselves contain placeholders
                return re.sub(r"\{\{([^{}#/]+)\}\}", sub, str(self.roles[name]))
            raise KeyError(m.group(0))

        out = re.sub(r"\{\{([^{}]+)\}\}", sub, out)
        if "{{" in out:
            raise ValueError("unresolved placeholder")
        return out


def load_themes() -> list[dict]:
    themes = []
    for path in sorted(PALETTES.glob("*.toml")):
        theme = tomllib.loads(path.read_text())
        theme["slug"] = path.stem
        themes.append(theme)
    return themes


def mermaid_vars(ctx: Ctx, mode: str) -> str:
    """Typora's Mermaid variables: the default theme on light variants; on dark ones an empty
    --mermaid-theme plus a node fill (30% accent over the background) to derive a theme from."""
    if mode == "light":
        return "    --mermaid-theme:             default;"
    accent, bg = (rgb_triple(ctx.hex(n)).split(", ") for n in ("accent", "bg"))
    fill = ", ".join(str(round(int(a) * 0.3 + int(b) * 0.7)) for a, b in zip(accent, bg))
    return "\n".join([
        '    --mermaid-theme:             "";',
        f"    --node-fill:                 rgb({fill});",
        f"    --node-text-color:           {ctx.hex('fg')};",
        f"    --cluster-fill:              {ctx.hex('bg-hl')};   /* Mermaid note background */",
    ])


def typora_outputs(theme: dict) -> dict[Path, str]:
    template = (TEMPLATES / "typora.css.tmpl").read_text()
    outputs = {}
    for v in theme["variants"]:
        ctx = Ctx(theme, v, "typora")
        if "search_select_alpha" in ctx.roles:
            sel_bg = f"rgba({rgb_triple(ctx.hex('search'))}, {ctx.roles['search_select_alpha']})"
            sel_text = ctx.hex(ctx.roles["search_select_text"])
        else:
            sel_bg, sel_text = ctx.hex("search"), ctx.hex("bg")
        extra = {
            "THEME": theme["name"], "SLUG": theme["slug"], "VERSION": theme["typora_version"],
            "VARIANT_LABEL": v["label"], "VARIANT_SLUG": v.get("file_slug", v["slug"]),
            "MODE_NOTE": "  (light)" if v["mode"] == "light" else "",
            "CHARACTER": f" — {v['character']}" if v.get("character") else "",
            "TAGLINE": "".join(f" * {line}\n" for line in theme["tagline"]),
            "PALETTE": "\n".join(ctx.palette_lines("    ")),
            "SEARCH_SELECT_BG": sel_bg, "SEARCH_SELECT_TEXT": sel_text,
            "MERMAID": mermaid_vars(ctx, v["mode"]),
        }
        name = f"{theme['slug']}-mod-{v.get('file_slug', v['slug'])}.css"
        outputs[ROOT / "typora" / theme["slug"] / name] = ctx.render(template, extra)
    return outputs


RULE = " * " + "=" * 60


# ---------------------------------------------------------------- Lamplit (single theme)
# Every palette becomes a Style Settings scheme. The template is rendered once: placeholders
# turn into semantic variables (--ll-accent, --ll-h2, …) that each variant block defines,
# and the template's style-conditional blocks are handled by kind:
#   rule groups        -> kept for every style, scoped with :where() (specificity unchanged)
#   declaration groups -> moved into the variant blocks of the variants using that style
#   inline values      -> become per-variant variables (--ll-cond-N)
COND = re.compile(r"\{\{#([\w-]+)=([\w-]+)\}\}(\n?)(.*?)\{\{/\1\}\}(\n?)", re.S)


def ll_var(p: str, kind: str, name: str) -> str:
    n = name.replace("_", "-")
    return f"var(--{p}-{n}-rgb)" if kind == "rgb" else f"var(--{p}-{n})"


def split_selectors(sel: str) -> list[str]:
    parts, depth, cur = [], 0, ""
    for ch in sel:
        depth += (ch == "(") - (ch == ")")
        if ch == "," and depth == 0:
            parts.append(cur); cur = ""
        else:
            cur += ch
    return [x.strip() for x in parts + [cur] if x.strip()]


def scope_rules(css: str, scope: list[str]) -> str:
    """Prefix every rule's selectors with :where(scope); keep comments and declarations."""
    def one(sel: str) -> str:
        m = re.match(r"body((?::[\w-]+(?:\([^)]*\))?|\.[\w-]+)*)", sel)
        if m:   # attach to the existing body compound
            return f"body{m.group(1)}:where({', '.join(scope)}){sel[m.end():]}"
        return f":where({', '.join('body' + x for x in scope)}) {sel}"

    def rule(m):
        head, body = m.group(1), m.group(2)
        cut = head.rfind("*/") + 2 if "*/" in head else 0
        lead, sel = head[:cut], head[cut:]
        ws = re.match(r"\s*", sel).group(0)
        return f"{lead}{ws}{',\n'.join(one(x) for x in split_selectors(sel))} {{{body}}}"
    return re.sub(r"([^{}]*)\{([^{}]*)\}", rule, css)


def lamplit_outputs(themes: list[dict]) -> dict[Path, str]:
    cfg = tomllib.loads((ROOT / "shared/lamplit.toml").read_text())
    P = cfg["prefix"]
    order = {s: i for i, s in enumerate(cfg["schemes"])}
    schemes = sorted(themes, key=lambda t: order[t["slug"]])
    vid = lambda t, v: f"{t['prefix']}-{v['slug']}"
    by_mode = {}
    for mode in ("dark", "light"):
        lst = [(t, v) for t in schemes for v in t["variants"] if v["mode"] == mode]
        lst.sort(key=lambda tv: vid(*tv) != cfg[f"default_{mode}"])   # default first, rest in scheme order
        by_mode[mode] = lst
    ctxs = {vid(t, v): Ctx(t, v, "obsidian") for t in schemes for v in t["variants"]}
    classes = {m: [f".{P}-{vid(t, v)}" for t, v in lst] for m, lst in by_mode.items()}

    def scope_for(key: str, value: str) -> list[str]:
        out = []
        for mode, lst in by_mode.items():
            for i, (t, v) in enumerate(lst):
                if str(ctxs[vid(t, v)].roles.get(key)) != value:
                    continue
                out.append(f".theme-{mode}.{P}-{vid(t, v)}")
                if i == 0:   # default variant: also when no scheme class is set (no Style Settings)
                    out.append(f".theme-{mode}:not({', '.join(classes[mode])})")
        return out

    template = (TEMPLATES / "obsidian.css.tmpl").read_text()
    used: dict[tuple[str, str], None] = {}

    def to_vars(text: str) -> str:
        def sub(m):
            kind, _, name = m.group(1).partition(":")
            if not name:
                return m.group(0)                       # {{UPPER}} handled later
            if kind not in ("c", "rgb", "r"):
                raise KeyError(f"Lamplit does not support {{{{{kind}:…}}}}")
            used[(kind, name)] = None
            return ll_var(P, kind, name)
        return re.sub(r"\{\{([^{}#/]+)\}\}", sub, text)

    # 1. style-conditional blocks
    decl_groups, cond_vars, pieces, pos = [], [], [], 0
    matches = list(COND.finditer(template))
    i = 0
    while i < len(matches):
        m = matches[i]
        pieces.append(to_vars(template[pos:m.start()]))
        key, val, nl1, body, nl2 = m.groups()
        if "{" in re.sub(r"\{\{[^{}]*\}\}", "", body):            # rule group
            pieces.append(scope_rules(to_vars(body), scope_for(key, val)) + nl2)
            pos = m.end(); i += 1
        elif nl1:                                                  # declaration group
            decl_groups.append((key, val, to_vars(body)))
            pos = m.end(); i += 1
        else:                                                      # inline alternatives
            run = [m]
            while i + len(run) < len(matches) and matches[i + len(run)].start() == run[-1].end() \
                    and matches[i + len(run)].group(1) == key:
                run.append(matches[i + len(run)])
            name = f"cond-{len(cond_vars) + 1}"
            cond_vars.append((name, key, {r.group(2): to_vars(r.group(4)) for r in run}))
            pieces.append(f"var(--{P}-{name})")
            pos = run[-1].end(); i += len(run)
    pieces.append(to_vars(template[pos:]))
    body_css = "".join(pieces)

    # 2. per-variant blocks: semantic variables + this variant's declaration groups / inline values
    def tokens(ctx: Ctx) -> list[tuple[str, str]]:
        rows = []
        for kind, name in used:
            n = name.replace("_", "-")
            if kind == "r":
                if name not in ctx.roles or ctx.roles[name] == "":
                    continue
                raw = str(ctx.roles[name])          # placeholders inside role values -> semantic vars
                rows.append((f"--{P}-{n}", re.sub(r"\{\{(\w+):([\w-]+)\}\}",
                                                  lambda m: ll_var(P, m.group(1), m.group(2)), raw)))
                continue
            if name in ctx.roles and ctx.roles[name] == "":
                continue                                   # role unused by this palette's styles
            if name == "mark-bg":
                value = f"rgba({rgb_triple(ctx.hex('yellow'))}, {ctx.roles['mark_alpha']})"
            else:
                value = ctx.hex(name)
            rows.append((f"--{P}-{n}-rgb", rgb_triple(value)) if kind == "rgb" else (f"--{P}-{n}", value))
        base = ["bg", "bg-dark", "bg-hl", "gutter", "fg", "fg-dim", "comment", "selection", "mark-bg",
                "blue", "cyan", "teal", "green", "yellow", "orange", "red", "magenta"]
        def key(row):
            n = row[0][len(P) + 3:].removesuffix("-rgb")
            return (base.index(n) if n in base else len(base), n, row[0].endswith("-rgb"))
        return sorted(rows, key=key)

    blocks = ["/* " + "=" * 60, " * Schemes (one block per palette variant)", " *",
              f" * Dark mode:  body.theme-dark  + {P}-<palette>-<variant> (Style Settings: dark scheme)",
              f" * Light mode: body.theme-light + {P}-<palette>-<variant> (Style Settings: light scheme)",
              " * Each block defines the semantic variables the rules below use.", RULE + " */"]
    for mode, lst in by_mode.items():
        for i, (t, v) in enumerate(lst):
            ctx = ctxs[vid(t, v)]
            rows = tokens(ctx)
            for name, key, alts in cond_vars:
                if str(ctx.roles.get(key)) in alts:
                    rows.append((f"--{P}-{name}", alts[str(ctx.roles.get(key))]))
            width = max(len(k) for k, _ in rows) + 1
            lines = [f"    {(k + ':').ljust(width)} {val};" for k, val in rows]
            for key, val, body in decl_groups:
                if str(ctx.roles.get(key)) == val:
                    lines.append(body.rstrip("\n"))
            sel = f"body.theme-{mode}.{P}-{vid(t, v)}"
            if i == 0:
                sel = f"body.theme-{mode},\n" + sel
            char = f" — {v['character']}" if v.get("character") else ""
            note = " (default)" if i == 0 else ""
            blocks += ["", f"/* --- {mode.title()}: {t['short_name']} · {v['label']}{note}{char} --- */", "",
                       sel + " {", *lines, "}"]

    # 3. Style Settings, header, manifest
    def option_lines(mode):
        out = []
        for t, v in by_mode[mode]:
            out += ["      -", f"        label: {t['short_name']} · {v['label']}", f"        value: {P}-{vid(t, v)}"]
        return out
    settings = ["/* @settings", "", f"name: {cfg['name']}", "id: lamplit", "settings:"]
    for mode in ("dark", "light"):
        settings += ["  -", f"    id: {P}-{mode}-scheme", f"    title: {mode.title()} Mode Scheme",
                     f"    description: Palette used when Obsidian is in {mode} mode",
                     "    type: class-select", f"    default: {P}-{cfg['default_' + mode]}", "    options:",
                     *option_lines(mode)]
    settings += ["  -", f"    id: {P}-hide-folder-icons", "    title: Hide Folder Icons",
                 "    description: Hide the folder icons in the file explorer",
                 "    type: class-toggle", "    default: false", "", "*/"]
    header = "\n".join([
        "/* " + "=" * 60, f" * {cfg['name']} — Obsidian Theme",
        *[f" * {line}" for line in cfg["tagline"]],
        " * Schemes: " + " · ".join(f"{t['short_name']} ({', '.join(v['label'] for v in t['variants'])})" for t in schemes),
        " * Requires: Style Settings plugin to choose schemes (otherwise the defaults apply)",
        " * GENERATED by scripts/gen-themes.py from shared/lamplit.toml, shared/palettes/*.toml",
        " * and scripts/templates/obsidian.css.tmpl — edit those, not this file.",
        RULE + " */"])
    extra = {"HEADER": header, "SETTINGS": "\n".join(settings), "PALETTES": "\n".join(blocks), "P": P}
    css = re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: extra[m.group(1)], body_css)
    if "{{" in css:
        raise ValueError("Lamplit: unresolved placeholder")
    manifest = {"name": cfg["name"], "version": cfg["obsidian_version"], "minAppVersion": cfg["min_app_version"],
                "author": cfg["author"], "authorUrl": cfg["author_url"]}
    out_dir = ROOT / "obsidian" / "lamplit"
    out_dir.mkdir(parents=True, exist_ok=True)
    return {out_dir / "theme.css": css,
            out_dir / "manifest.json": json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"}


def main() -> None:
    check = "--check" in sys.argv[1:]
    outputs: dict[Path, str] = {}
    themes = load_themes()
    for theme in themes:
        outputs.update(typora_outputs(theme))
    outputs.update(lamplit_outputs(themes))
    stale = []
    for path, text in outputs.items():
        rel = path.relative_to(ROOT)
        if check:
            if not path.exists() or path.read_text() != text:
                stale.append(str(rel))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)   # a new palette's typora/<palette>/
            path.write_text(text)
            print(f"  wrote {rel}")
    if check:
        if stale:
            sys.exit("stale (rerun scripts/gen-themes.py):\n  " + "\n  ".join(stale))
        print(f"  all {len(outputs)} generated files are up to date")


if __name__ == "__main__":
    main()

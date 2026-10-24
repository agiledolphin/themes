#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Generate every theme file from shared/palettes/<theme>.toml + scripts/templates/.

Outputs (never edit by hand — edit the TOML or the templates, then rerun):
    typora/<theme>/<theme>-mod-<variant>.css
    obsidian/<theme>/theme.css + manifest.json

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
            if kind == "r":
                return str(self.roles[name])
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
        }
        name = f"{theme['slug']}-mod-{v.get('file_slug', v['slug'])}.css"
        outputs[ROOT / "typora" / theme["slug"] / name] = ctx.render(template, extra)
    return outputs


RULE = " * " + "=" * 60


def obsidian_settings(theme: dict) -> str:
    p, noun, desc = theme["prefix"], theme["settings_noun"], theme["settings_desc_noun"]
    lines = ["/* @settings", "", f"name: {theme['name']}", f"id: {theme['slug']}", "settings:"]
    for mode in ("dark", "light"):
        vs = [v for v in theme["variants"] if v["mode"] == mode]
        lines += ["  -", f"    id: {p}-{mode}-{noun}",
                  f"    title: {mode.title()} Mode {noun.title()}",
                  f"    description: Color {desc} used when Obsidian is in {mode} mode",
                  "    type: class-select", f"    default: {p}-{vs[0]['slug']}", "    options:"]
        for v in vs:
            lines += ["      -", f"        label: {v['label']}", f"        value: {p}-{v['slug']}"]
    lines += ["  -", f"    id: {p}-hide-folder-icons", "    title: Hide Folder Icons",
              "    description: Hide the folder icons in the file explorer",
              "    type: class-toggle", "    default: false", "", "*/"]
    return "\n".join(lines)


def alternatives(variants: list[dict]) -> str:
    slugs = [v["slug"] for v in variants]
    return slugs[0] if len(slugs) == 1 else "{" + "|".join(slugs) + "}"


def obsidian_outputs(theme: dict) -> dict[Path, str]:
    template = (TEMPLATES / "obsidian.css.tmpl").read_text()
    p, slug = theme["prefix"], theme["slug"]
    dark = [v for v in theme["variants"] if v["mode"] == "dark"]
    light = [v for v in theme["variants"] if v["mode"] == "light"]
    header = "\n".join([
        "/* " + "=" * 60, f" * {theme['name']} — Obsidian Theme",
        *[f" * {line}" for line in theme["tagline"]],
        " * Variants: " + " · ".join(v["label"] for v in dark) + " (dark) · "
        + " · ".join(v["label"] for v in light) + " (light)",
        " * Requires: Style Settings plugin for variant switching",
        f" * GENERATED by scripts/gen-themes.py from shared/palettes/{slug}.toml",
        " * and scripts/templates/obsidian.css.tmpl — edit those, not this file.",
        RULE + " */"])
    blocks = ["/* " + "=" * 60, " * Palettes", " *",
              f" * Dark mode:  body.theme-dark  + {p}-{alternatives(dark)}",
              f" * Light mode: body.theme-light + {p}-{alternatives(light)}",
              " *", f" * Default dark = {dark[0]['label']}; default light = {light[0]['label']}.",
              RULE + " */"]
    for group in (dark, light):
        for i, v in enumerate(group):
            ctx = Ctx(theme, v, "obsidian")
            note = " (default)" if i == 0 else ""
            char = f" — {v['character']}" if v.get("character") else ""
            sel = f"body.theme-{v['mode']}.{p}-{v['slug']}"
            if i == 0:
                sel = f"body.theme-{v['mode']},\n" + sel
            blocks += ["", f"/* --- {v['mode'].title()}: {v['label']}{note}{char} --- */", "",
                       sel + " {", *ctx.palette_lines("    "), "}"]
    extra = {"HEADER": header, "SETTINGS": obsidian_settings(theme),
             "PALETTES": "\n".join(blocks), "P": p}
    rendered = {Ctx(theme, v, "obsidian").render(template, extra) for v in theme["variants"]}
    if len(rendered) != 1:
        raise ValueError(f"{slug}: a per-variant override changes the shared Obsidian rules")
    manifest = {"name": theme["name"], "version": theme["obsidian_version"],
                "minAppVersion": theme["min_app_version"], "author": theme["author"],
                "authorUrl": theme["author_url"]}
    out_dir = ROOT / "obsidian" / slug
    return {out_dir / "theme.css": rendered.pop(),
            out_dir / "manifest.json": json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"}


def main() -> None:
    check = "--check" in sys.argv[1:]
    outputs: dict[Path, str] = {}
    for theme in load_themes():
        outputs.update(typora_outputs(theme))
        outputs.update(obsidian_outputs(theme))
    stale = []
    for path, text in outputs.items():
        rel = path.relative_to(ROOT)
        if check:
            if not path.exists() or path.read_text() != text:
                stale.append(str(rel))
        else:
            path.write_text(text)
            print(f"  wrote {rel}")
    if check:
        if stale:
            sys.exit("stale (rerun scripts/gen-themes.py):\n  " + "\n  ".join(stale))
        print(f"  all {len(outputs)} generated files are up to date")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate the Wonderland Mod Typora themes from the shared template.

Palettes are read from obsidian/wonderland/theme.css, so both platforms always
share identical colors. To change Wonderland's Typora output, edit the template
(scripts/templates/wonderland-typora.css.tmpl) or the Obsidian palettes, then
rerun this script — never edit typora/wonderland/*.css by hand.

Usage:
    ./scripts/gen-wonderland-typora.py           # (re)write the three CSS files
    ./scripts/gen-wonderland-typora.py --check   # exit 1 if any file is stale
"""
import re
import sys
from pathlib import Path

VERSION = "1.1.0"  # Typora version; tracked separately from the Obsidian manifest

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "scripts/templates/wonderland-typora.css.tmpl"
PALETTE_SRC = ROOT / "obsidian/wonderland/theme.css"
OUT_DIR = ROOT / "typora/wonderland"

# (file slug, display name, palette block marker in theme.css, mode note, character)
VARIANTS = [
    ("underground", "Underground", "Dark: Underground", "",
     "the INKlings' sewers; darkest, coldest"),
    ("office-district", "Office District", "Dark: Office", "",
     "Tokyo at night above ground; a shade lighter, warmer"),
    ("lab", "Lab", "Light: Lab", "  (light)",
     "the System's sterile laboratory; cold white"),
]


def palette(src: str, marker: str) -> dict:
    start = src.index(marker)
    body = src[src.index("{", start):src.index("}", start)]
    return {k: v.strip() for k, v in re.findall(r"--wl-([a-z-]+):\s*([^;]+);", body)}


def render(template: str, src: str, slug, name, marker, mode, character) -> str:
    out = (template.replace("{{VERSION}}", VERSION).replace("{{NAME}}", name)
           .replace("{{SLUG}}", slug).replace("{{MODE_NOTE}}", mode)
           .replace("{{CHARACTER}}", character))
    values = palette(src, marker)
    out = re.sub(r"\{\{([a-z-]+)\}\}", lambda m: values[m.group(1)], out)
    if "{{" in out:
        sys.exit(f"unfilled placeholder in {slug}")
    return out


def main() -> None:
    check = "--check" in sys.argv[1:]
    template = TEMPLATE.read_text()
    src = PALETTE_SRC.read_text()
    stale = []
    for slug, name, marker, mode, character in VARIANTS:
        path = OUT_DIR / f"wonderland-mod-{slug}.css"
        css = render(template, src, slug, name, marker, mode, character)
        if check:
            if not path.exists() or path.read_text() != css:
                stale.append(path.name)
        else:
            path.write_text(css)
            print(f"  wrote {path.relative_to(ROOT)}")
    if check:
        if stale:
            sys.exit("stale (rerun the generator): " + ", ".join(stale))
        print("  all Wonderland Typora files are up to date")


if __name__ == "__main__":
    main()

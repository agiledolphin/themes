# Lamplit Wonderland for Typora

A Typora theme inspired by the **Hard-Boiled Wonderland** half of Haruki Murakami's *Hard-Boiled Wonderland and the End of the World* (《世界尽头与冷酷仙境》): a cold, deadpan, faintly surreal Tokyo — rain-dark streets, the INKlings' flooded underground, skull-lined laboratories — where the warm brass of a desk lamp or a whisky bar is the only warmth in the room.

Three variants are provided as separate CSS files. Colors match the Wonderland scheme in the Obsidian theme Lamplit.

---

## Screenshots

> *(coming soon)*

---

## Variants

| File | Mode | Background | Character |
|------|------|------------|-----------|
| `lamplit-wonderland-underground.css`     | Dark  | `#121218` | The INKlings' sewers — darkest, coldest |
| `lamplit-wonderland-office-district.css` | Dark  | `#1f1a14` | Tokyo at night above ground — a shade lighter, warmer |
| `lamplit-wonderland-lab.css`             | Light | `#eef0f2` | The System's sterile laboratory — cold white |

## Color roles

| Role | Used for |
|------|----------|
| Brass | the one warm accent: H2, blockquote rule, table header, task checkboxes, active file in the sidebar |
| Cyan  | H1, inline code |
| Steel | links, H3, TOC links |
| Blood | errors, deleted lines, HTML tags in code |
| Moss  | strings, H5 |

---

## Features

- **Restrained palette** — desaturated indigo-black grounds and cool grey-white text, with brass as the single warm accent rather than neon
- **Heading hierarchy** — H1–H6 in cyan → brass → steel → teal → moss → comment
- **Chinese-first typography** — PingFang SC → Hiragino Sans GB → Noto Serif SC, comfortable line height
- **Code blocks** — syntax highlighting via both highlight.js and CodeMirror classes, same color roles as the Obsidian version
- **Transparent blockquotes** with a brass rule (steel for nested quotes)
- **Rounded grid tables** — brass header text and underline, brass row hover, no zebra striping
- **Full element coverage** — task lists, footnotes, math, Mermaid diagrams, YAML front matter, TOC
- **Print / PDF export** — optimized layout with page-break hints

---

## Installation

### Automatic (sync script)

```bash
./scripts/sync-typora.sh wonderland
```

### Manual

1. Locate your Typora themes directory:
   - **macOS**: `~/Library/Application Support/abnerworks.Typora/themes/`
   - **Windows**: `%APPDATA%\Typora\themes\`
   - **Linux**: `~/.config/Typora/themes/`
2. Copy one or more of the CSS files above into that directory
3. Open **Typora → Preferences → Appearance** and select the variant

---

## License

MIT

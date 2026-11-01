# Lamplit Bauhaus for Typora

A Typora theme after the Bauhaus (1919–1933): the three primaries on warm paper white or black, flat solid blocks and square corners. Prose uses only red, yellow and blue plus black, white and grey; the secondaries of Johannes Itten's colour wheel (taught in the Bauhaus preliminary course) colour code only.

Two variants are provided as separate CSS files, named after the school's first two homes. Colors match the Bauhaus scheme in the Obsidian theme Lamplit.

---

## Screenshots

> *(coming soon)*

---

## Variants

| File | Mode | Background | Text |
|------|------|------------|------|
| `lamplit-bauhaus-weimar.css` | Dark  | `#161616` | `#ece8de` |
| `lamplit-bauhaus-dessau.css` | Light | `#f3f0e7` | `#1c1c1c` |

## Color roles

| Role | Weimar | Dessau | Used for |
|------|--------|--------|----------|
| Red    | `#ff5a4e` | `#c4262e` | H1, the accent: cursor, blockquote rule, task checkboxes, the open file |
| Blue   | `#6f9dff` | `#1f4f9c` | links, H2, tags, table header |
| Signal yellow | `#ffd23f` | `#f2c014` | the solid `==highlight==` block |
| Yellow | `#ffd23f` | `#876700` | H3 in Weimar; code properties and warnings (darkened in Dessau to read as text) |
| Orange | `#ff9a3c` | `#ad5106` | search hits, numbers (code) |
| Green  | `#6cc070` | `#2e7d32` | strings (code) |
| Violet | `#b48cff` | `#6a3fa0` | keywords (code) |
| Teal   | `#4fc1b8` | `#00756e` | inline code |

Text accents read at 4.6:1 or better against their background, and look-alike colors stay at a color difference of ΔE ≥ 26.

---

## Features

- **Primaries only in prose** — red, yellow and blue plus black, white and grey; orange, green, violet and teal appear in code only
- **Solid highlight** — `==highlighted==` text is a solid yellow block with dark text, not a tint
- **Square corners** — code blocks, tables, inline code, highlights, blockquotes and front matter have no rounding
- **Heading hierarchy** — H1 red → H2 blue → H3 yellow (Weimar) or bold black (Dessau) → text tones → comment
- **Chinese-first typography** — PingFang SC → Hiragino Sans GB → Noto Serif SC, comfortable line height
- **Code blocks** — syntax highlighting via both highlight.js and CodeMirror classes, same color roles as the Obsidian version
- **Transparent blockquotes** with a red rule (blue for nested quotes)
- **Square grid tables** — blue header text and underline, row hover tint, no zebra striping
- **Full element coverage** — task lists, footnotes, math, Mermaid diagrams, YAML front matter, TOC
- **Print / PDF export** — optimized layout with page-break hints

---

## Installation

### Automatic (sync script)

```bash
./scripts/sync-typora.sh bauhaus
```

### Manual

1. Locate your Typora themes directory:
   - **macOS**: `~/Library/Application Support/abnerworks.Typora/themes/`
   - **Windows**: `%APPDATA%\Typora\themes\`
   - **Linux**: `~/.config/Typora/themes/`
2. Copy one or both CSS files into that directory
3. Open **Typora → Preferences → Appearance** and select the variant

---

## License

MIT

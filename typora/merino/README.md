# Merino Mod for Typora

A clean, neutral Typora theme after the **Merino Light** and **Merino Dark** terminal themes: a white or near-black ground, near-black or cool light text, and crisp accents (GitHub Primer colors). The terminal palette has no teal or orange, so teal is the midpoint of its cyan and green, and orange is Primer's orange.

Two variants are provided as separate CSS files. Colors match the Merino scheme in the Obsidian theme Lamplit.

---

## Screenshots

> *(coming soon)*

---

## Variants

| File | Mode | Background | Text |
|------|------|------------|------|
| `merino-mod-light.css` | Light | `#ffffff` | `#1f2328` |
| `merino-mod-dark.css`  | Dark  | `#0d1117` | `#e6edf3` |

## Color roles

| Role | Light | Dark | Used for |
|------|-------|------|----------|
| Blue    | `#0969da` | `#58a6ff` | the accent: links, H1, blockquote rule, task checkboxes, active file in the sidebar |
| Magenta | `#8250df` | `#bc8cff` | the second voice: H2, table header, nested quotes, code keywords |
| Cyan    | `#1b7c83` | `#39c5cf` | H3, inline code |
| Orange  | `#bc4c00` | `#f0883e` | search hits, numbers |
| Red     | `#cf222e` | `#ff7b72` | errors, deleted lines, HTML tags in code |
| Green   | `#116329` | `#3fb950` | strings, H4 |

Every accent reads at 4.5:1 or better against its background, and look-alike colors stay at a color difference of ΔE ≥ 16.

---

## Features

- **Neutral grounds** — pure white in light mode, near-black in dark mode
- **Heading hierarchy** — H1–H6 in blue → magenta → cyan → green → yellow → comment
- **Chinese-first typography** — PingFang SC → Hiragino Sans GB → Noto Serif SC, comfortable line height
- **Code blocks** — syntax highlighting via both highlight.js and CodeMirror classes, same color roles as the Obsidian version
- **Transparent blockquotes** with a blue rule (magenta for nested quotes)
- **Rounded grid tables** — magenta header text and underline, row hover tint, no zebra striping
- **Full element coverage** — task lists, footnotes, math, Mermaid diagrams, YAML front matter, TOC
- **Print / PDF export** — optimized layout with page-break hints

---

## Installation

### Automatic (sync script)

```bash
./scripts/sync-typora.sh merino
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

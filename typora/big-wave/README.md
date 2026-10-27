# Lamplit Big Wave for Typora

A summer-ocean Typora theme after the cover of Tatsuro Yamashita's *Big Wave* (1984): the deep-navy tube of a breaking wave, white spray, a cobalt sky, the coral script of the title and a yellow surfboard. The cover gives blue, white, coral and yellow; palm green, sunset orange and red come from the same 80s city-pop summer.

Two variants are provided as separate CSS files. Colors match the Big Wave scheme in the Obsidian theme Lamplit.

---

## Screenshots

> *(coming soon)*

---

## Variants

| File | Mode | Background | Text |
|------|------|------------|------|
| `lamplit-big-wave-pipeline.css` | Dark  | `#0e1a30` | `#dbe5f2` |
| `lamplit-big-wave-spray.css`    | Light | `#f4f7fb` | `#18264a` |

## Color roles

| Role | Pipeline | Spray | Used for |
|------|----------|-------|----------|
| Coral  | `#ff8fa3` | `#bd4762` | the title color: H1, table header, nested quotes, code keywords |
| Cobalt | `#6ea0ff` | `#1f4fbf` | the accent: links, H2, blockquote rule, task checkboxes, active file in the sidebar |
| Aqua   | `#5fd4e0` | `#007283` | H3, inline code, tags |
| Board  | `#e6cf7e` | `#7e6200` | `==highlighted==` text, H5 |
| Sunset | `#ff9f5a` | `#b8500f` | search hits, numbers |
| Palm   | `#8fd18a` | `#2f7a2a` | strings, H4 |
| Red    | `#ff6b6b` | `#c0303a` | errors, deleted lines |

Every accent reads at 4.6:1 or better against its background, and look-alike colors stay at a color difference of ΔE ≥ 21. In Spray the surfboard yellow has to darken to a mustard to stay readable on white.

---

## Features

- **Ocean grounds** — deep navy in dark mode, blue-white spray in light mode
- **Heading hierarchy** — H1–H6 in coral → cobalt → aqua → palm → board yellow → comment
- **Chinese-first typography** — PingFang SC → Hiragino Sans GB → Noto Serif SC, comfortable line height
- **Code blocks** — syntax highlighting via both highlight.js and CodeMirror classes, same color roles as the Obsidian version
- **Transparent blockquotes** with a cobalt rule (coral for nested quotes)
- **Rounded grid tables** — coral header text and underline, row hover tint, no zebra striping
- **Full element coverage** — task lists, footnotes, math, Mermaid diagrams, YAML front matter, TOC
- **Print / PDF export** — optimized layout with page-break hints

---

## Installation

### Automatic (sync script)

```bash
./scripts/sync-typora.sh big-wave
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

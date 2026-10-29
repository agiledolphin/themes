# Lamplit Impression for Typora

A misty Typora theme after Claude Monet's *Impression, Sunrise* (1872): the harbour of Le Havre at dawn, cool grey-blue and grey-green haze, dark boats, and one orange sun with its reflection on the water. As in the painting, the sun is the only warm, saturated color; everything else is cool and muted. The light variant is kept airy: a grey-green white ground, surfaces that differ by a breath of mist, slate (not black) text and pale tints.

Two variants are provided as separate CSS files. Colors match the Impression scheme in the Obsidian theme Lamplit.

---

## Screenshots

> *(coming soon)*

---

## Variants

| File | Mode | Background | Text |
|------|------|------------|------|
| `lamplit-impression-havre.css` | Dark  | `#1c272c` | `#d6dfe2` |
| `lamplit-impression-brume.css` | Light | `#f4f6f5` | `#2a3842` |

## Color roles

| Role | Havre | Brume | Used for |
|------|-------|-------|----------|
| Sun    | `#f07a45` | `#b4471f` | the one warm note: H1, table header, blockquote rule, cursor, active file, numbers |
| Harbour | `#82a3c8` | `#355f86` | links, H2 |
| Water  | `#6cbcc4` | `#1f6f7a` | H3, inline code, tags |
| Lilac  | `#aa9ad6` | `#62538f` | H4, code keywords, search hits, nested quotes |
| Ochre  | `#dcb27a` | `#835e1d` | `==highlighted==` text, H5 |
| Shore  | `#a6bd7e` | `#4f6b2c` | strings |
| Madder | `#e86060` | `#b2373b` | errors, deleted lines |

Every accent reads at 4.5:1 or better against its background, and look-alike colors stay at a color difference of ΔE ≥ 20. In Brume the sun has to deepen to a vermilion to work as text, so it glows less than in Havre.

---

## Features

- **Misty grounds** — slate grey-green in dark mode, an airy grey-green white in light mode with surfaces only a breath apart
- **One warm note** — the sun (H1, table header, cursor, active file) is the only saturated color; everything else stays cool and muted
- **Heading hierarchy** — H1–H6 in sun → harbour blue → water cyan → lilac → ochre → comment
- **Chinese-first typography** — PingFang SC → Hiragino Sans GB → Noto Serif SC, comfortable line height
- **Code blocks** — syntax highlighting via both highlight.js and CodeMirror classes, same color roles as the Obsidian version
- **Transparent blockquotes** with a sun rule (lilac for nested quotes)
- **Rounded grid tables** — sun header text and underline, row hover tint, no zebra striping
- **Full element coverage** — task lists, footnotes, math, Mermaid diagrams, YAML front matter, TOC
- **Print / PDF export** — optimized layout with page-break hints

---

## Installation

### Automatic (sync script)

```bash
./scripts/sync-typora.sh impression
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

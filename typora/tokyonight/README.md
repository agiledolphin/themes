# TokyoNight for Typora

A Typora theme based on the [TokyoNight](https://github.com/folke/tokyonight.nvim) color palette by folke. Four variants are provided as separate CSS files, each with its own full palette.

---

## Screenshots

> *(coming soon)*

---

## Variants

| File | Mode | Background | Character |
|------|------|------------|-----------|
| `tokyonight-storm.css` | Dark  | `#24283b`  | Blue-grey, standard dark |
| `tokyonight-night.css` | Dark  | `#1a1b26`  | Deep, near-black |
| `tokyonight-moon.css`  | Dark  | `#222436`  | Blue-purple tint |
| `tokyonight-day.css`   | Light | `#e1e2e7`  | Low-saturation light |

---

## Features

- **Four independent variants** — each with its own complete palette, not approximated
- **Heading hierarchy** — H1–H6 in distinct accent colors (blue → cyan → teal → green → yellow → comment)
- **Chinese-first typography** — PingFang SC → Hiragino Sans GB → Noto Serif SC, comfortable line height
- **Code blocks** — syntax highlighting via both highlight.js and CodeMirror classes
- **Full element coverage** — blockquotes, tables, task lists, footnotes, math, Mermaid diagrams, YAML front matter, TOC
- **Sidebar polish** — file panel active highlight, hover color, and outline panel active (bold) / hover (background + underline) states
- **Print / PDF export** — optimized layout with page-break hints

---

## Installation

### Automatic (sync script)

If you have cloned this repository:

```bash
./scripts/sync-typora.sh
# or sync a single variant:
./scripts/sync-typora.sh tokyonight-storm
```

The script copies the CSS files to Typora's themes directory automatically.

### Manual

1. Locate your Typora themes directory:
   - **macOS**: `~/Library/Application Support/abnerworks.Typora/themes/`
   - **Windows**: `%APPDATA%\Typora\themes\`
   - **Linux**: `~/.config/Typora/themes/`
2. Copy one or more of the following files into that directory:
   - `tokyonight-storm.css`
   - `tokyonight-night.css`
   - `tokyonight-moon.css`
   - `tokyonight-day.css`
3. Open **Typora → Preferences → Appearance** and select the desired variant

---

## Switching Variants

Each variant is a standalone CSS file. To switch variants, select a different theme in **Preferences → Appearance**. Typora applies the change immediately without restart.

For automatic dark/light switching, pair a dark variant with Typora's **Auto** appearance mode and use the OS-level dark/light toggle.

---

## Font Recommendations

- **Body text**: PingFang SC / Hiragino Sans GB / Noto Serif SC / Georgia
- **Monospace**: [JetBrains Mono](https://www.jetbrains.com/lp/mono/) or [Fira Code](https://github.com/tonsky/FiraCode)

---

## Credits

- Color palette: [tokyonight.nvim](https://github.com/folke/tokyonight.nvim) by [@folke](https://github.com/folke)

---

## License

MIT

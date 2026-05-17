# Catppuccin for Typora

A Typora theme based on the [Catppuccin](https://catppuccin.com) color palette. Four flavors are provided as separate CSS files, each with its own complete palette.

---

## Screenshots

> *(coming soon)*

---

## Variants

| File | Mode | Background | Character |
|------|------|------------|-----------|
| `catppuccin-mocha.css`     | Dark  | `#1e1e2e`  | Deep navy, the darkest flavor |
| `catppuccin-macchiato.css` | Dark  | `#24273a`  | Slightly lighter navy |
| `catppuccin-frappe.css`    | Dark  | `#303446`  | Cool dark grey-blue |
| `catppuccin-latte.css`     | Light | `#eff1f5`  | Warm parchment light |

---

## Features

- **Four independent flavors** — each with its own complete palette, not approximated
- **Heading hierarchy** — H1–H6 in distinct accent colors (lavender → blue → cyan → teal → green → comment)
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
# or sync a single flavor:
./scripts/sync-typora.sh catppuccin-mocha
```

The script copies the CSS files to Typora's themes directory automatically.

### Manual

1. Locate your Typora themes directory:
   - **macOS**: `~/Library/Application Support/abnerworks.Typora/themes/`
   - **Windows**: `%APPDATA%\Typora\themes\`
   - **Linux**: `~/.config/Typora/themes/`
2. Copy one or more of the following files into that directory:
   - `catppuccin-mocha.css`
   - `catppuccin-macchiato.css`
   - `catppuccin-frappe.css`
   - `catppuccin-latte.css`
3. Open **Typora → Preferences → Appearance** and select the desired flavor

---

## Switching Flavors

Each flavor is a standalone CSS file. To switch flavors, select a different theme in **Preferences → Appearance**. Typora applies the change immediately without restart.

For automatic dark/light switching, pair a dark flavor with Typora's **Auto** appearance mode and use the OS-level dark/light toggle.

---

## Font Recommendations

- **Body text**: PingFang SC / Hiragino Sans GB / Noto Serif SC / Georgia
- **Monospace**: [JetBrains Mono](https://www.jetbrains.com/lp/mono/) or [Fira Code](https://github.com/tonsky/FiraCode)

---

## Credits

- Color palette: [Catppuccin](https://catppuccin.com) by the Catppuccin org

---

## License

MIT

# Lamplit for Obsidian

Reading by lamplight (青灯夜读). Lamplit is one Obsidian theme that carries four palettes as schemes — **Wonderland**, **Merino**, **TokyoNight** and **Catppuccin** — so you switch palettes in [Style Settings](https://github.com/mgmeyers/obsidian-style-settings) instead of switching themes. Dark and light mode each get their own scheme, and they can come from different palettes.

---

## Schemes

| Palette | Scheme | Mode | Background | Character |
|---------|--------|------|------------|-----------|
| Wonderland | Underground | Dark | `#121218` | The INKlings' sewers — darkest, coldest (default dark) |
| Wonderland | Office District | Dark | `#1a1a20` | Tokyo at night above ground — a shade lighter, warmer |
| Wonderland | Lab | Light | `#eef0f2` | The System's sterile laboratory — cold white (default light) |
| Merino | Dark | Dark | `#0d1117` | Near-black ground, cool light text |
| Merino | Light | Light | `#ffffff` | White ground, near-black text |
| TokyoNight | Storm | Dark | `#24283b` | Blue-grey, standard dark |
| TokyoNight | Night | Dark | `#1a1b26` | Deep, near-black |
| TokyoNight | Moon | Dark | `#222436` | Blue-purple tint |
| TokyoNight | Day | Light | `#e1e2e7` | Low-saturation light |
| Catppuccin | Mocha | Dark | `#1e1e2e` | Deep navy, the darkest flavor |
| Catppuccin | Macchiato | Dark | `#24273a` | Slightly lighter navy |
| Catppuccin | Frappé | Dark | `#303446` | Cool dark grey-blue |
| Catppuccin | Latte | Light | `#eff1f5` | Warm parchment light |

Wonderland is an original palette inspired by the "Hard-Boiled Wonderland" half of Haruki Murakami's *Hard-Boiled Wonderland and the End of the World*: restrained indigo-black grounds, cool grey-white text, and a single warm brass accent. Merino follows the Merino Light / Merino Dark terminal themes (GitHub Primer colors): neutral white and near-black grounds with crisp accents. TokyoNight and Catppuccin follow their official palettes.

Each palette keeps its own character beyond color:

- **File explorer** — Wonderland, Merino and TokyoNight mark the open file with an accent tint and a left bar; Catppuccin uses solid fills (lavender on hover, mauve for the open file).
- **Context menus** — the selected item follows the same language: an accent tint, or a solid lavender fill for Catppuccin.

---

## Choosing schemes (Style Settings)

1. Install **Style Settings** from the Community Plugins list.
2. Open **Settings → Style Settings → Lamplit**.
3. Pick a **Dark Mode Scheme** (9 options) and a **Light Mode Scheme** (4 options).

Without Style Settings, Lamplit uses **Wonderland · Underground** in dark mode and **Wonderland · Lab** in light mode.

---

## Features

- **Full Obsidian variable mapping** — backgrounds, text, links, code, headings, tags, callouts, checkboxes, graph, ribbon
- **Reading view and Live Preview look the same** — headings, code blocks (frame, size, font, line height), inline code, tables, blockquotes, tags, highlights and links are driven by the same variables in both views
- **Callouts** — all 13 official types with semantic colors; titles and icons take the per-type hue
- **Task list** — 7 states with custom circular checkboxes: `x`, `/`, `-`, `>`, `?`, `!`
- **Tables** — sized to their content, rounded frame, single grid lines, 14px text
- **Search highlights** — one dedicated search color per palette (Wonderland cyan, Merino orange, TokyoNight orange, Catppuccin peach), distinct from highlighted text and the selection
- **Context menus** — a darker surface than the editor; destructive items such as Delete turn red when selected
- **Chinese-first typography** — PingFang SC → Hiragino Sans GB → Noto Serif SC
- **Hide Folder Icons** toggle in Style Settings

> **Note (macOS):** Obsidian uses native system menus on macOS by default, and themes cannot style those. To see the themed context menus, turn off **Settings → Interface → Advanced → Native menus**.

---

## Installation

1. Copy `theme.css` and `manifest.json` to `<your-vault>/.obsidian/themes/Lamplit/`
2. Open **Settings → Appearance → Themes** and select **Lamplit**

---

## Credits

- Palettes: [tokyonight.nvim](https://github.com/folke/tokyonight.nvim) by [@folke](https://github.com/folke); [Catppuccin](https://catppuccin.com) by the Catppuccin org; Merino after the Merino Light / Dark terminal themes (GitHub Primer colors); Wonderland is original
- Design reference: [Minimal](https://github.com/kepano/obsidian-minimal) by [@kepano](https://github.com/kepano)

---

## License

MIT

# TokyoNight for Obsidian

A clean, full-featured Obsidian theme based on the [TokyoNight](https://github.com/folke/tokyonight.nvim) color palette by folke. Supports all four variants — Storm, Night, Moon, and Day — independently selectable for dark and light modes via the [Style Settings](https://github.com/mgmeyers/obsidian-style-settings) plugin.

---

## Screenshots

> *(coming soon)*

---

## Variants

| Variant | Mode | Background | Character |
|---------|------|------------|-----------|
| Storm   | Dark | `#24283b`  | Blue-grey, standard dark |
| Night   | Dark | `#1a1b26`  | Deep, near-black |
| Moon    | Dark | `#222436`  | Blue-purple tint |
| Day     | Light | `#e1e2e7` | Low-saturation light |

Each variant carries its own full palette — colors are not approximated or shared between variants.

---

## Features

- **Independent scheme selection** for dark mode and light mode
- **Automatic switching** based on system appearance
- **Full Obsidian variable mapping** — backgrounds, text, links, code, headings, tags, callouts, checkboxes, graph, ribbon, and more
- **Heading hierarchy** — H1–H6 in distinct accent colors (blue → cyan → teal → green → yellow → comment)
- **Unified workspace** — editor, file explorer, tab bar, ribbon, and status bar share a consistent background
- **Readable typography** — Chinese-first font stack (PingFang SC → Hiragino Sans GB → Noto Serif SC), comfortable line height
- **Callout colors** — all 13 official Obsidian callout types covered with semantic palette mapping (note/info/todo → blue, tip → cyan, success → green, warning → orange, failure/danger/bug → red, example → magenta, quote → comment, etc.)
- **Task list** — 7 states with custom circular checkboxes: unchecked, checked, in-progress (`/`), cancelled (`-`), rescheduled (`>`), questionable (`?`), important (`!`); styled in both reading and live preview modes
- **Consistent inline styles** — highlighted text and inline code render identically in reading and editing modes
- **File explorer polish** — folder icon coloring, hover gradient, active file highlight

---

## Installation

### From Obsidian Community Themes

1. Open **Settings → Appearance → Themes**
2. Click **Manage** and search for `TokyoNight`
3. Click **Install and use**

### Manual

1. Download `theme.css` and `manifest.json`
2. Copy both files to `<your-vault>/.obsidian/themes/TokyoNight/`
3. Open **Settings → Appearance → Themes** and select **TokyoNight**

---

## Variant Switching (Style Settings)

Install the [Style Settings](https://github.com/mgmeyers/obsidian-style-settings) plugin to switch variants independently for each mode.

1. Install **Style Settings** from the Community Plugins list
2. Open **Settings → Style Settings → TokyoNight**
3. Set **Dark Mode Scheme** (default: Storm) and **Light Mode Scheme** (default: Day)

Without Style Settings, the theme defaults to **Storm** in dark mode and **Day** in light mode.

---

## Font Recommendations

The theme is designed around these font stacks — install for the best experience:

- **Body text**: PingFang SC / Hiragino Sans GB / Noto Serif SC
- **Monospace**: [JetBrains Mono](https://www.jetbrains.com/lp/mono/) or [Fira Code](https://github.com/tonsky/FiraCode)

---

## Credits

- Color palette: [tokyonight.nvim](https://github.com/folke/tokyonight.nvim) by [@folke](https://github.com/folke)
- Design reference: [Minimal](https://github.com/kepano/obsidian-minimal) by [@kepano](https://github.com/kepano)

---

## License

MIT

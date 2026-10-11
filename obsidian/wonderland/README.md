# Wonderland Mod for Obsidian

An Obsidian theme inspired by the **Hard-Boiled Wonderland** half of Haruki Murakami's *Hard-Boiled Wonderland and the End of the World* (《世界尽头与冷酷仙境》): a cold, deadpan, faintly surreal Tokyo — rain-dark streets, the INKlings' flooded underground, skull-lined laboratories — where the warm brass of a desk lamp or a whisky bar is the only warmth in the room.

The palette is deliberately restrained: desaturated indigo-black grounds, cool grey-white text, and a single warm brass accent, rather than neon cyberpunk.

---

## Screenshots

> *(coming soon)*

---

## Variants

| Variant         | Mode  | Background | Character |
|-----------------|-------|------------|-----------|
| Underground     | Dark  | `#121218`  | The INKlings' sewers — darkest, coldest (default dark) |
| Office District | Dark  | `#1a1a20`  | Tokyo at night above ground — a shade lighter, warmer |
| Lab             | Light | `#eef0f2`  | The System's sterile laboratory — cold white |

## Color roles

| Role | Color | Used for |
|------|-------|----------|
| Brass  | lamp / bar light | UI accent: checkboxes, tags, folder icons, active file bar, cursor, table header, H2 |
| Cyan   | encrypted data   | H1, property keys, tip callouts |
| Steel  | cold blue        | links, H3, note/info callouts |
| Blood  | INKlings, skulls | errors, danger/bug callouts, `[!]` tasks |
| Moss   | damp underground | success, strings, H5 |
| Bone   | unicorn skull    | tooltips (graphite in Lab) |

---

## Features

- **Independent scheme selection** for dark mode and light mode via Style Settings
- **Full Obsidian variable mapping** — backgrounds, text, links, code, headings, tags, callouts, checkboxes, graph, ribbon
- **Restrained file explorer** — brass gradient on hover; the open file gets a brass tint plus a left accent bar instead of a solid fill
- **Callouts** — all 13 official types with semantic colors; titles and icons take the per-type hue
- **Consistent blockquotes** — Reading mode and Live Preview share the same variables (transparent background, brass left border)
- **Task list** — 7 states with custom circular checkboxes: `x`, `/`, `-`, `>`, `?`, `!`
- **Rounded grid tables** — brass header text and underline, brass row hover, no zebra striping
- **Chinese-first typography** — PingFang SC → Hiragino Sans GB → Noto Serif SC

---

## Installation

### Manual

1. Copy `theme.css` and `manifest.json` to `<your-vault>/.obsidian/themes/Wonderland Mod/`
2. Open **Settings → Appearance → Themes** and select **Wonderland Mod**

### Sync script

```bash
./scripts/sync-obsidian.sh <vault-path> wonderland
```

---

## Variant Switching (Style Settings)

1. Install the [Style Settings](https://github.com/mgmeyers/obsidian-style-settings) plugin
2. Open **Settings → Style Settings → Wonderland Mod**
3. Set **Dark Mode Scheme** to Underground (default) or Office District

Without Style Settings, the theme uses **Underground** in dark mode and **Lab** in light mode.

---

## License

MIT

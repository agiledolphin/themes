# Lamplit

Reading by lamplight (青灯夜读). Seven color palettes for [Obsidian](https://obsidian.md) and [Typora](https://typora.io), generated from one set of sources.

- **Obsidian**: one theme, **Lamplit**, that carries every palette as a scheme. Dark and light mode each pick their own scheme in [Style Settings](https://github.com/mgmeyers/obsidian-style-settings).
- **Typora**: one theme file per palette variant, named `lamplit-<palette>-<variant>.css`.

## Palettes

| Palette | Dark | Light | After |
|---------|------|-------|-------|
| [Wonderland](typora/wonderland/README.md) | Underground, Office District | Lab | Original, inspired by Haruki Murakami's *Hard-Boiled Wonderland and the End of the World* |
| [Merino](typora/merino/README.md) | Dark | Light | The Merino Light / Dark terminal themes (GitHub Primer colors) |
| [Big Wave](typora/big-wave/README.md) | Pipeline | Spray | The cover of Tatsuro Yamashita's *Big Wave* (1984) |
| [Impression](typora/impression/README.md) | Havre | Brume | Claude Monet's *Impression, Sunrise* (1872) |
| [Bauhaus](typora/bauhaus/README.md) | Weimar | Dessau | The Bauhaus school: three primaries, solid blocks, square corners |
| [TokyoNight](typora/tokyonight/README.md) | Storm, Night, Moon | Day | [tokyonight.nvim](https://github.com/folke/tokyonight.nvim) (official palette) |
| [Catppuccin](typora/catppuccin/README.md) | Mocha, Macchiato, Frappé | Latte | [Catppuccin](https://catppuccin.com) (official palette) |

Screenshots are still to come. Details for each platform: [Lamplit for Obsidian](obsidian/lamplit/README.md) and the Typora README linked from each palette above.

## Installation

The themes are not in the Obsidian or Typora theme galleries yet, so install them from this repository:

```bash
git clone https://github.com/agiledolphin/themes.git
cd themes
```

`sync-obsidian.sh` needs [uv](https://docs.astral.sh/uv/) to read the theme name, and `sync-typora.sh` only knows Typora's macOS folder. Otherwise, use the manual steps.

### Obsidian

```bash
./scripts/sync-obsidian.sh /path/to/your/vault
```

Or copy `theme.css` and `manifest.json` from `obsidian/lamplit/` to `<your-vault>/.obsidian/themes/Lamplit/`.

Then:

1. Open **Settings → Appearance → Themes** and select **Lamplit**.
2. Install **Style Settings** from the Community Plugins list.
3. Open **Settings → Style Settings → Lamplit** and pick a **Dark Mode Scheme** and a **Light Mode Scheme**.

Without Style Settings, Lamplit uses Wonderland · Underground in dark mode and Wonderland · Lab in light mode.

### Typora

```bash
./scripts/sync-typora.sh              # every theme
./scripts/sync-typora.sh big-wave     # one palette (a folder name under typora/)
```

Or copy the `lamplit-*.css` files from `typora/<palette>/` directly into Typora's themes folder, without a subfolder:

- **macOS**: `~/Library/Application Support/abnerworks.Typora/themes/`
- **Windows**: `%APPDATA%\Typora\themes\`
- **Linux**: `~/.config/Typora/themes/`

Then restart Typora and choose a **Lamplit …** theme from the **Themes** menu. Each variant is a separate theme, so Typora does not switch between dark and light by itself.

### Updating

Run `git pull`, then the sync scripts again. Reload the theme in Obsidian and reselect it in Typora.

## Development

Every theme file is generated. Do not edit `obsidian/lamplit/theme.css`, `obsidian/lamplit/manifest.json` or `typora/<palette>/*.css` by hand.

| Source | Holds |
|--------|-------|
| `shared/palettes/<palette>.toml` | a palette's variants, colors, color roles and style switches |
| `shared/lamplit.toml` | Lamplit's name, version, default schemes and palette order |
| `scripts/templates/` | the CSS shared by all palettes |

```bash
./scripts/gen-themes.py           # regenerate every theme (runs through uv)
./scripts/gen-themes.py --check   # exit 1 if any output is stale
```

To add a palette, create `shared/palettes/<palette>.toml`, add its name to `schemes` in `shared/lamplit.toml`, and run the generator.

`scripts/verify-obsidian/` checks the real rendering in Obsidian: Reading view against Live Preview, text contrast, and differences from an earlier run. See [CLAUDE.md](CLAUDE.md) for the conventions and the verification workflow, and [THEMES_PLAN.md](THEMES_PLAN.md) for status and current versions.

## Credits

- Palettes: [tokyonight.nvim](https://github.com/folke/tokyonight.nvim) by [@folke](https://github.com/folke); [Catppuccin](https://catppuccin.com) by the Catppuccin org
- Design reference: [Minimal](https://github.com/kepano/obsidian-minimal) by [@kepano](https://github.com/kepano)

## License

[MIT](LICENSE)

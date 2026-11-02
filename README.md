# Lamplit

English · [简体中文](README.zh-CN.md)

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

The themes are not in the Obsidian or Typora theme galleries yet. There are three ways to install them, and none of them needs an account.

### Option 1: one command (macOS, Linux)

Needs `curl` and `unzip`. Run the same command again to update.

```bash
# Obsidian: pass the path to your vault
curl -fsSL https://raw.githubusercontent.com/agiledolphin/themes/main/install.sh | bash -s -- obsidian /path/to/your/vault

# Typora: every theme
curl -fsSL https://raw.githubusercontent.com/agiledolphin/themes/main/install.sh | bash -s -- typora

# Typora: only some palettes
curl -fsSL https://raw.githubusercontent.com/agiledolphin/themes/main/install.sh | bash -s -- typora big-wave impression
```

The script installs the latest release. It only writes to the theme folders, and it is short enough to [read first](install.sh).

### Option 2: download a release

From the [latest release](https://github.com/agiledolphin/themes/releases/latest):

- **Obsidian**: unzip `Lamplit-obsidian.zip` into `<your-vault>/.obsidian/themes/`, so that you get `themes/Lamplit/theme.css`. In Finder, press Cmd+Shift+. to show the hidden `.obsidian` folder.
- **Typora**: unzip `Lamplit-typora.zip` and copy the `.css` files you want directly into Typora's themes folder, without a subfolder:
  - **macOS**: `~/Library/Application Support/abnerworks.Typora/themes/`
  - **Windows**: `%APPDATA%\Typora\themes\`
  - **Linux**: `~/.config/Typora/themes/`

### Option 3: from a clone

```bash
git clone https://github.com/agiledolphin/themes.git
cd themes
./scripts/sync-obsidian.sh /path/to/your/vault
./scripts/sync-typora.sh              # every theme (macOS only)
./scripts/sync-typora.sh big-wave     # one palette (a folder name under typora/)
```

This installs the current `main`. To update, run `git pull` and the sync scripts again.

### After installing

**Obsidian**

1. Restart Obsidian, open **Settings → Appearance → Themes** and select **Lamplit**.
2. Install **Style Settings** from the Community Plugins list.
3. Open **Settings → Style Settings → Lamplit** and pick a **Dark Mode Scheme** and a **Light Mode Scheme**.

Without Style Settings, Lamplit uses Wonderland · Underground in dark mode and Wonderland · Lab in light mode.

**Lamplit does not show up?** It is listed in the theme dropdown under **Settings → Appearance → Themes**, not under **Manage**, which only searches the community gallery. Obsidian silently skips a theme whose folder name differs from the `name` in its `manifest.json`, even by case, so check that the folder is exactly `Lamplit`, and that it holds `theme.css` and `manifest.json` directly.

**Typora**

Restart Typora and choose a **Lamplit …** theme from the **Themes** menu. Each variant is a separate theme, so Typora does not switch between dark and light by itself.

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

To cut a release, run `./scripts/package-release.sh`, which builds the two archives into `dist/` and prints the `gh release create` command.

`scripts/verify-obsidian/` checks the real rendering in Obsidian: Reading view against Live Preview, text contrast, and differences from an earlier run. See [CLAUDE.md](CLAUDE.md) for the conventions and the verification workflow, and [THEMES_PLAN.md](THEMES_PLAN.md) for status and current versions.

## Credits

- Palettes: [tokyonight.nvim](https://github.com/folke/tokyonight.nvim) by [@folke](https://github.com/folke); [Catppuccin](https://catppuccin.com) by the Catppuccin org
- Design reference: [Minimal](https://github.com/kepano/obsidian-minimal) by [@kepano](https://github.com/kepano)
- Icons: [Lucide](https://lucide.dev), the set Obsidian itself uses

## License

[MIT](LICENSE)

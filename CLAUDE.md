# Themes Workspace

Design workspace for Typora and Obsidian themes. Three themes, each on both platforms:
TokyoNight Mod (`tn-`), Catppuccin Mod (`cp-`), Wonderland Mod (`wl-`, original palette
inspired by Murakami's "Hard-Boiled Wonderland"). Status, to-dos and current versions
live in `THEMES_PLAN.md` — keep it updated when work lands.

## Directory layout

```
themes/
├── obsidian/<theme>/        # theme.css + manifest.json + README.md
├── typora/<theme>/          # <theme>-mod-<variant>.css (one file per variant) + README.md
├── shared/tokens/base.css   # reference values only — NOT imported by any theme
├── scripts/
│   ├── sync-obsidian.sh     # ./scripts/sync-obsidian.sh <vault-path> [theme]
│   └── sync-typora.sh       # ./scripts/sync-typora.sh [theme]
└── THEMES_PLAN.md
```

Every theme file is self-contained (no `@import`): Obsidian loads a single `theme.css`, and
Typora files are copied flat into Typora's themes directory, so relative imports would break.

## Obsidian

- One `theme.css` per theme holds all variants. Variants are Style Settings `class-select`
  options (`@settings` block at the top). Each theme has several dark variants + exactly one
  light variant, selected independently per mode.
- Palette blocks: `body.theme-dark, body.theme-dark.<prefix>-<variant>` (first block is the
  default) and `body.theme-light, body.theme-light.<prefix>-<variant>`. Dark palettes MUST sit
  on `theme-dark` — app.css applies light-mode rules (e.g. `mix-blend-mode: darken` on callouts)
  to `theme-light`, which silently breaks dark colors.
- Below the palettes, one `body.theme-dark, body.theme-light` block maps palette vars onto
  Obsidian's own variables. Prefer setting Obsidian variables over hardcoding colors on a
  selector: Reading mode and Live Preview often read the same variable through different
  selectors (e.g. `--blockquote-background-color` for `.markdown-rendered blockquote` and
  `.HyperMD-quote`), so a selector-only override makes the two modes disagree.
- `--<prefix>-<color>-rgb` vars and `--callout-color` hold bare RGB triples (`195, 154, 95`)
  for `rgba()`. Wherever app.css uses such a var as a plain color, wrap it: `rgb(var(...))`.
- When a color doesn't apply, check what app.css actually does: extract it with
  `npx asar extract /Applications/Obsidian.app/Contents/Resources/obsidian.asar <dir>` and grep.
- Sync to the user's vault for testing: `./scripts/sync-obsidian.sh ~/notebook`.

## Typora

- Themes directory: `~/Library/Application Support/abnerworks.Typora/themes/`
- One standalone CSS file per variant, named `<theme>-mod-<variant>.css`; the palette is
  declared in that file's `:root`. `--bg-color` must be set in `:root` (it drives `#write`).
- Wonderland's three files are generated from one template with palettes read from the
  Obsidian `theme.css`; if you change Wonderland colors, keep both platforms identical.
- After syncing, reselect the theme in Preferences → Appearance (or restart Typora).

## Design conventions

- All colors go through CSS custom properties; never hardcode a hex outside the palette blocks.
- Chinese body text: PingFang SC → Hiragino Sans GB → Noto Serif SC.
- Typora content width ≤ 860px (960px on ≥1400px screens).
- Text contrast: accents ≥ ~4.3:1 against the background; faint/comment text may be ~3.3:1.

## Versioning & commits

- Versions live in each Obsidian `manifest.json` and in the `Version:` line of each Typora
  file header; Obsidian and Typora versions are tracked separately. Bump only the platform
  that changed (patch for fixes, minor for feature batches) and update the table in
  `THEMES_PLAN.md`.
- Commit style: `feat(obsidian): …`, `fix(typora): …`, `docs: …`, `chore: …`.

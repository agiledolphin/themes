# Themes Workspace

Design workspace for software themes (Typora, Obsidian, etc.).

## Directory layout

```
themes/
├── shared/
│   ├── tokens/base.css      # shared CSS variables (typography, spacing, radius)
│   └── palettes/            # color palette files (.yaml or .css)
├── typora/
│   └── <theme-name>/
│       ├── <theme-name>.css # main theme (Typora reads this)
│       ├── assets/          # fonts, images referenced by CSS
│       └── README.md
├── obsidian/                # future
├── scripts/
│   └── sync-typora.sh       # copies CSS to Typora's themes directory
└── CLAUDE.md
```

## Typora

- Typora themes directory: `~/Library/Application Support/abnerworks.Typora/themes/`
- A theme is a single `.css` file; a companion folder with the same name holds assets
- Sync command: `./scripts/sync-typora.sh <theme-name>` (or omit name to sync all)
- Typora must reload themes (Preferences → Appearance → Open Theme Folder then reselect) after copy

## Design conventions

- All colors go through CSS custom properties defined in `:root`
- Import shared tokens at the top of each theme CSS with a comment, then override as needed
- Chinese body text: prefer system fonts (PingFang SC → Hiragino Sans GB → Noto Serif SC)
- Keep `--content-width` ≤ 860px for comfortable reading
- Light and dark variants share a base file; suffix dark variant with `-dark.css`

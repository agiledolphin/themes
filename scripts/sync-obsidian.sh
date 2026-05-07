#!/usr/bin/env bash
# Sync Obsidian themes from workspace to a vault's .obsidian/themes/ directory.
# Usage:
#   ./scripts/sync-obsidian.sh <vault-path>              # sync all theme folders
#   ./scripts/sync-obsidian.sh <vault-path> tokyonight   # sync one theme

VAULT="${1:-}"
SRC=./obsidian

if [[ -z "$VAULT" ]]; then
    echo "Usage: $0 <vault-path> [theme-name]"
    echo "Example: $0 ~/Documents/MyVault"
    exit 1
fi

DEST="$VAULT/.obsidian/themes"

if [[ ! -d "$VAULT/.obsidian" ]]; then
    echo "Not an Obsidian vault (no .obsidian directory): $VAULT"
    exit 1
fi

mkdir -p "$DEST"

sync_theme() {
    local name="$1"
    local src_dir="$SRC/$name"

    if [[ ! -d "$src_dir" ]]; then
        echo "Theme folder '$name' not found in $SRC"
        exit 1
    fi

    if [[ ! -f "$src_dir/manifest.json" ]]; then
        echo "Missing manifest.json in $src_dir"
        exit 1
    fi

    # Read theme display name from manifest
    local display_name
    display_name=$(python3 -c "import json,sys; print(json.load(open('$src_dir/manifest.json'))['name'])" 2>/dev/null || echo "$name")

    local dest_dir="$DEST/$display_name"
    mkdir -p "$dest_dir"

    cp "$src_dir/manifest.json" "$dest_dir/manifest.json"
    cp "$src_dir/theme.css"     "$dest_dir/theme.css"
    echo "  synced: $display_name  →  $dest_dir"
}

if [[ -n "$2" ]]; then
    sync_theme "$2"
else
    for d in "$SRC"/*/; do
        [[ -d "$d" ]] || continue
        sync_theme "$(basename "$d")"
    done
fi

echo ""
echo "Done. In Obsidian: Settings → Appearance → Themes → select TokyoNight."
echo "Install the Style Settings plugin to switch variants and modes."

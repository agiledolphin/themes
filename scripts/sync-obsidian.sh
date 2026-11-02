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

    # Obsidian skips a theme unless its folder name equals the manifest's "name" exactly
    # (case-sensitive), so the folder is named from the manifest, never from the repo folder.
    local display_name
    display_name=$(sed -n 's/^[[:space:]]*"name":[[:space:]]*"\([^"]*\)".*/\1/p' "$src_dir/manifest.json" | head -n 1)
    if [[ -z "$display_name" ]]; then
        echo "No \"name\" found in $src_dir/manifest.json"
        exit 1
    fi

    # A folder differing only by case stays as it is on a case-insensitive disk: rename it.
    local wanted existing
    wanted=$(echo "$display_name" | tr '[:upper:]' '[:lower:]')
    for existing in "$DEST"/*/; do
        existing=$(basename "$existing")
        if [[ "$existing" != "$display_name" && "$(echo "$existing" | tr '[:upper:]' '[:lower:]')" == "$wanted" ]]; then
            mv "$DEST/$existing" "$DEST/$existing.renaming"
            if [[ -e "$DEST/$display_name" ]]; then
                mv "$DEST/$existing.renaming" "$DEST/$existing"
                echo "  note: $existing/ is ignored by Obsidian; delete it, $display_name/ is the real one"
            else
                mv "$DEST/$existing.renaming" "$DEST/$display_name"
                echo "  renamed: $existing/ → $display_name/"
            fi
        fi
    done

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
echo "Done. In Obsidian: Settings → Appearance → Themes → select the theme to apply."
echo "Install the Style Settings plugin to switch variants per mode."

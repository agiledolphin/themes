#!/usr/bin/env bash
# Sync Typora themes from workspace to Typora's themes directory.
# Usage:
#   ./scripts/sync-typora.sh              # sync all theme folders
#   ./scripts/sync-typora.sh tokyonight   # sync one theme folder by name

TYPORA_THEMES=~/Library/Application\ Support/abnerworks.Typora/themes
SRC=./typora

if [[ ! -d "$TYPORA_THEMES" ]]; then
    echo "Typora themes directory not found: $TYPORA_THEMES"
    exit 1
fi

sync_folder() {
    local folder="$SRC/$1"
    if [[ ! -d "$folder" ]]; then
        echo "Theme folder '$1' not found in $SRC"
        exit 1
    fi

    local count=0

    # Copy every .css file in the folder to Typora's themes root
    while IFS= read -r -d '' css_file; do
        local theme_name
        theme_name=$(basename "$css_file")
        cp "$css_file" "$TYPORA_THEMES/$theme_name"
        echo "  synced: $theme_name"
        (( count++ ))
    done < <(find "$folder" -maxdepth 1 -name "*.css" -print0 | sort -z)

    # Symlink shared assets folder if it exists
    if [[ -d "$folder/assets" ]]; then
        local asset_dest="$TYPORA_THEMES/$1"
        rm -rf "$asset_dest"
        ln -sf "$(cd "$folder/assets" && pwd)" "$asset_dest"
        echo "  linked assets → $asset_dest/"
    fi

    echo "  ($count CSS files synced from $1/)"
}

if [[ -n "$1" ]]; then
    sync_folder "$1"
else
    for d in "$SRC"/*/; do
        [[ -d "$d" ]] || continue
        sync_folder "$(basename "$d")"
    done
fi

echo ""
echo "Done. In Typora: Preferences → Appearance → select theme to apply."

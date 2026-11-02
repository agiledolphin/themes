#!/usr/bin/env bash
# Install Lamplit from the latest GitHub Release, without cloning the repository.
# Needs bash, curl and unzip. On Windows, use the manual steps in the README.
#
#   curl -fsSL https://raw.githubusercontent.com/agiledolphin/themes/main/install.sh | bash -s -- obsidian /path/to/vault
#   curl -fsSL https://raw.githubusercontent.com/agiledolphin/themes/main/install.sh | bash -s -- typora
#   curl -fsSL https://raw.githubusercontent.com/agiledolphin/themes/main/install.sh | bash -s -- typora big-wave impression
#
# Run again to update. Nothing else in the themes folders is touched.

set -euo pipefail

BASE_URL="${LAMPLIT_BASE_URL:-https://github.com/agiledolphin/themes/releases/latest/download}"

die() { echo "Error: $*" >&2; exit 1; }

usage() {
    echo "Usage: install.sh obsidian <vault-path>"
    echo "       install.sh typora [palette ...]"
    exit 1
}

# Download an archive and unpack it into $WORK/unpacked.
fetch() {
    curl -fsSL -o "$WORK/$1" "$BASE_URL/$1" || die "could not download $BASE_URL/$1"
    unzip -q "$WORK/$1" -d "$WORK/unpacked"
}

install_obsidian() {
    local vault="${1:-}"
    [[ -n "$vault" ]] || usage
    [[ -d "$vault/.obsidian" ]] || die "not an Obsidian vault (no .obsidian folder): $vault"

    fetch Lamplit-obsidian.zip
    local themes="$vault/.obsidian/themes" existing
    mkdir -p "$themes"

    # Obsidian skips a theme unless its folder name equals the manifest's "name" exactly, and
    # a folder differing only by case stays as it is on a case-insensitive disk: rename it.
    for existing in "$themes"/*/; do
        existing=$(basename "$existing")
        if [[ "$existing" != "Lamplit" && "$(echo "$existing" | tr '[:upper:]' '[:lower:]')" == "lamplit" ]]; then
            mv "$themes/$existing" "$themes/$existing.renaming"
            if [[ -e "$themes/Lamplit" ]]; then
                mv "$themes/$existing.renaming" "$themes/$existing"
                echo "Note: $existing/ is ignored by Obsidian; delete it, Lamplit/ is the real one"
            else
                mv "$themes/$existing.renaming" "$themes/Lamplit"
            fi
        fi
    done

    mkdir -p "$themes/Lamplit"
    cp "$WORK"/unpacked/Lamplit/* "$themes/Lamplit/"
    echo "Installed Lamplit into $themes/Lamplit"
    echo "Next: restart Obsidian, then choose Lamplit in Settings → Appearance → Themes."
}

install_typora() {
    local themes
    case "$(uname -s)" in
        Darwin) themes="$HOME/Library/Application Support/abnerworks.Typora/themes" ;;
        Linux)  themes="${XDG_CONFIG_HOME:-$HOME/.config}/Typora/themes" ;;
        *)      die "unsupported system; use the manual steps in the README" ;;
    esac
    [[ -d "$themes" ]] || die "Typora's themes folder not found: $themes (open Typora once first)"

    fetch Lamplit-typora.zip
    local src="$WORK/unpacked/Lamplit-typora" palette file count=0
    shopt -s nullglob
    if [[ $# -eq 0 ]]; then
        set -- ""
    fi
    for palette in "$@"; do
        local files=("$src"/lamplit-"${palette:+$palette-}"*.css)
        [[ ${#files[@]} -gt 0 ]] || die "unknown palette: $palette"
        for file in "${files[@]}"; do
            cp "$file" "$themes/"
            count=$((count + 1))
        done
    done
    echo "Installed $count Typora theme(s) into $themes"
    echo "Next: restart Typora, then choose a Lamplit theme from the Themes menu."
}

main() {
    command -v curl >/dev/null || die "curl is required"
    command -v unzip >/dev/null || die "unzip is required"
    WORK=$(mktemp -d)
    trap 'rm -rf "$WORK"' EXIT

    local target="${1:-}"
    [[ $# -gt 0 ]] && shift
    case "$target" in
        obsidian) install_obsidian "$@" ;;
        typora)   install_typora "$@" ;;
        *)        usage ;;
    esac
}

# Everything runs from here, so a truncated download executes nothing.
main "$@"

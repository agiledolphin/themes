#!/usr/bin/env bash
# Build the release archives into dist/ (git-ignored):
#   Lamplit-obsidian.zip   Lamplit/ with theme.css, manifest.json, LICENSE
#   Lamplit-typora.zip     Lamplit-typora/ with every lamplit-*.css, LICENSE
# install.sh downloads these from the latest GitHub Release.
# Usage: ./scripts/package-release.sh

set -euo pipefail
cd "$(dirname "$0")/.."

./scripts/gen-themes.py --check

# The folder name must equal the manifest's "name" (Obsidian skips the theme otherwise).
name=$(sed -n 's/^[[:space:]]*"name":[[:space:]]*"\([^"]*\)".*/\1/p' obsidian/lamplit/manifest.json | head -n 1)
version=$(sed -n 's/^[[:space:]]*"version":[[:space:]]*"\([^"]*\)".*/\1/p' obsidian/lamplit/manifest.json | head -n 1)

stage=dist/.stage
rm -rf dist
mkdir -p "$stage/$name" "$stage/$name-typora"

cp obsidian/lamplit/theme.css obsidian/lamplit/manifest.json LICENSE "$stage/$name/"
cp typora/*/lamplit-*.css LICENSE "$stage/$name-typora/"

(cd "$stage" && zip -qr "../$name-obsidian.zip" "$name" && zip -qr "../$name-typora.zip" "$name-typora")
rm -rf "$stage"

echo "Built for v$version:"
ls -1 dist/
echo ""
echo "To publish:"
echo "  gh release create v$version dist/*.zip --title \"$name $version\" --notes \"…\""

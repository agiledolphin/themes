#!/usr/bin/env bash
# Publish the Obsidian theme to agiledolphin/lamplit, the repository the Obsidian community
# directory reads: the theme files in its root and a GitHub release tagged exactly like the
# manifest's version (no "v"), with manifest.json and theme.css attached. Everything in that
# repository comes from here; never edit it directly.
# Usage: ./scripts/publish-lamplit.sh
# LAMPLIT_COMMIT_TRAILERS, if set, is appended to the commit message.

set -euo pipefail
cd "$(dirname "$0")/.."
REPO=agiledolphin/lamplit
SRC=$PWD

./scripts/gen-themes.py --check

version=$(sed -n 's/^[[:space:]]*"version":[[:space:]]*"\([^"]*\)".*/\1/p' obsidian/lamplit/manifest.json | head -n 1)
[[ -n "$version" ]] || { echo "No version in obsidian/lamplit/manifest.json"; exit 1; }
if gh release view "$version" --repo "$REPO" >/dev/null 2>&1; then
    echo "Release $version already exists in $REPO: bump obsidian_version first."
    exit 1
fi

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
gh repo clone "$REPO" "$work" -- --quiet
cd "$work"
git checkout -q -B main

cp "$SRC"/obsidian/lamplit/{theme.css,manifest.json,README.md,screenshot.png} "$SRC/LICENSE" .
git add -A
if ! git diff --cached --quiet; then
    message="Lamplit $version"
    [[ -z "${LAMPLIT_COMMIT_TRAILERS:-}" ]] || message+=$'\n\n'"$LAMPLIT_COMMIT_TRAILERS"
    git commit -q -m "$message"
    git push -q origin main
fi

gh release create "$version" manifest.json theme.css --repo "$REPO" --target main \
    --title "Lamplit $version" --notes "See https://github.com/agiledolphin/themes/releases for what changed."
echo "Published $REPO $version"

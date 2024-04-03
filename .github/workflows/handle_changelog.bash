#!/bin/bash

root="$(git rev-parse --show-toplevel)"
changelog="$root/changelog/CHANGELOG"
changelog_tmp="$(mktemp)"
release_notes="$root/changelog/release_notes.txt"
sidebar="$root/mysite/templates/sidebar.html"

new_notes="$(date +"%Y-%m-%d"): $(cat "$release_notes")"
old_notes="$(head -n +1 "$changelog")"

[[ -s $release_notes ]] || exit 0

cat <<- EOF >> "$changelog_tmp"
$new_notes
$(cat "$changelog")
EOF

mv -f "$changelog_tmp" "$changelog"

sed_params=(
  -r -i
  -e "s|(Most recent update).*|\1 $new_notes|"
  -e "s|(Previous update).*|\1 $old_notes|"
)
sed "${sed_params[@]}" "$sidebar"

cat "$changelog"

truncate -s 0 "$release_notes"

chmod -R 744 .ssh
cp -r .ssh ~/

git config --global user.email "git@github.com"
git config --global user.name "auto-changelog"

git add .
git commit -m "auto-update changelog"
git push -u origin HEAD

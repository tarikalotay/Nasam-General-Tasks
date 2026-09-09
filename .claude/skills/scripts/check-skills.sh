#!/usr/bin/env bash
# Validate the Nasam skill bundles before they are committed or uploaded to claude.ai.
#
# Checks, in order:
#   1. frontmatter   — every SKILL.md has name + description, and name matches its directory
#   2. secrets       — no live credentials (this repo is public; the ClickUp token leaked once)
#   3. machine paths — no hardcoded personal home directories
#   4. drift         — injected shared context matches _shared/nasam-business-context.md
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

fail=0
note() { printf '  %s\n' "$1"; fail=1; }

# Skills are the directories holding a SKILL.md; scripts/ and _shared/ are tooling, not bundles.
mapfile -t skills < <(find . -mindepth 2 -maxdepth 2 -name SKILL.md -printf '%h\n' | sed 's|^\./||' | sort)
if [ ${#skills[@]} -eq 0 ]; then echo "error: no SKILL.md found under $(pwd)"; exit 1; fi

echo "== frontmatter =="
for s in "${skills[@]}"; do
  f="$s/SKILL.md"
  [ "$(head -1 "$f")" = "---" ] || note "$f: does not start with a YAML frontmatter fence"
  name=$(awk 'NR>1 && /^---$/{exit} NR>1 && /^name:/{sub(/^name:[[:space:]]*/,""); print; exit}' "$f")
  desc=$(awk 'NR>1 && /^---$/{exit} NR>1 && /^description:/{print "y"; exit}' "$f")
  [ -n "$name" ] || note "$f: missing 'name:' in frontmatter"
  [ -n "$desc" ] || note "$f: missing 'description:' in frontmatter"
  [ -z "$name" ] || [ "$name" = "$s" ] || note "$f: name '$name' does not match directory '$s'"
done

echo "== secrets =="
# Full-length credential shapes only, so documenting a redacted prefix stays allowed.
secret_re='pk_[0-9]{6,}_[A-Za-z0-9]{24,}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,}|sk-[A-Za-z0-9]{32,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{20,}'
if hits=$(grep -rEn --exclude-dir=scripts "$secret_re" . 2>/dev/null); then
  while IFS= read -r line; do note "credential-shaped string: ${line%%:*}"; done <<<"$hits"
fi

echo "== machine paths =="
if hits=$(grep -rEn --exclude-dir=scripts '(/Users/[a-z][a-z0-9_.-]+|/home/[a-z][a-z0-9_.-]+)/' . 2>/dev/null \
          | grep -vE '/(Users|home)/(you|USER|<user>|\$\{?USER)'); then
  while IFS= read -r line; do note "hardcoded home directory: $line"; done <<<"$hits"
fi

echo "== shared context drift =="
./scripts/sync-shared.sh --check || fail=1

echo
if [ "$fail" -eq 0 ]; then
  echo "PASS — ${#skills[@]} skills: ${skills[*]}"
else
  echo "FAIL — fix the items above"
fi
exit "$fail"

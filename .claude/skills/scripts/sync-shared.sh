#!/usr/bin/env bash
# Inject the canonical Nasam business context into each consuming SKILL.md.
#
# Account skills upload to claude.ai as self-contained bundles — one skill cannot read another's
# files — so shared context has to live inline in each SKILL.md. This script keeps those inline
# copies generated from one source instead of hand-maintained (which is how they drifted before).
#
#   ./sync-shared.sh          rewrite the injected blocks
#   ./sync-shared.sh --check  exit 1 if any block is stale (no writes)
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
exec python3 - "$@" <<'PY'
import re, sys, pathlib

CHECK = "--check" in sys.argv[1:]
root = pathlib.Path.cwd()
source = root / "_shared" / "nasam-business-context.md"
# skill -> region of the source file to inline
CONSUMERS = {"ux-discovery": "full", "ux-touch": "short"}

text = source.read_text(encoding="utf-8")
regions = {
    m.group(1): m.group(2).strip("\n")
    for m in re.finditer(
        r"<!-- REGION:([a-z-]+) -->\n(.*?)\n<!-- /REGION:\1 -->", text, re.S
    )
}
missing = set(CONSUMERS.values()) - set(regions)
if missing:
    sys.exit(f"error: {source} has no region(s): {', '.join(sorted(missing))}")

stale, wrote = [], []
for skill, region in sorted(CONSUMERS.items()):
    path = root / skill / "SKILL.md"
    if not path.exists():
        sys.exit(f"error: consumer {skill} has no SKILL.md")
    body = path.read_text(encoding="utf-8")
    begin = f"<!-- BEGIN:nasam-business-context ({region}) -->"
    end = "<!-- END:nasam-business-context -->"
    # (?:.*?\n)? so a freshly-added, still-empty marker pair also matches.
    pattern = re.compile(
        re.escape(begin) + r"\n(?:.*?\n)?" + re.escape(end), re.S
    )
    if not pattern.search(body):
        sys.exit(
            f"error: {path} is missing the marker pair\n"
            f"  {begin}\n  ...\n  {end}\n"
            f"Add it where the context belongs, then re-run."
        )
    # A literal \g in the replacement would be read as a group reference, so pass a function.
    block = f"{begin}\n{regions[region]}\n{end}"
    updated = pattern.sub(lambda _m: block, body, count=1)
    if updated == body:
        continue
    if CHECK:
        stale.append(skill)
    else:
        path.write_text(updated, encoding="utf-8")
        wrote.append(skill)

if CHECK:
    if stale:
        sys.exit(
            "error: injected context is stale in: "
            + ", ".join(stale)
            + "\nRun .claude/skills/scripts/sync-shared.sh to regenerate."
        )
    print(f"shared context in sync ({len(CONSUMERS)} skills)")
else:
    print(f"updated: {', '.join(wrote) if wrote else 'nothing (already in sync)'}")
PY

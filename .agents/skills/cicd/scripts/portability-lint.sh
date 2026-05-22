#!/usr/bin/env bash
# Portability lint: catch path leaks and per-user config dependencies in
# committed docs/configs before they ship in a PR. Antigravityd's recurring bug
# class.
#
# Usage: portability-lint.sh [--all]
#   default: lint files modified vs HEAD (staged + unstaged)
#   --all:   lint all tracked files
#
# Exits 0 if clean, 1 if any leak is found.

set -euo pipefail

mode="${1:-diff}"
case "$mode" in
    --all)
        mapfile -d '' -t files < <(git ls-files -z -- ':(exclude)*.lock' 2>/dev/null)
        ;;
    diff|--diff)
        mapfile -d '' -t files < <(git diff --diff-filter=AMR -z --name-only HEAD -- ':(exclude)*.lock' 2>/dev/null)
        ;;
    *)
        echo "Usage: $(basename "$0") [--all]" >&2; exit 2
        ;;
esac

if [ ${#files[@]} -eq 0 ]; then
    echo "(no files to check)"
    exit 0
fi

# ----- Check 1: hard-coded /home/<user>/... paths -----
hits1=""
if [ ${#files[@]} -gt 0 ]; then
    hits1=$(grep -HnE '/home/[a-z][a-z0-9_-]+/' "${files[@]}" 2>/dev/null || true)
fi

# ----- Check 2: per-user dotfile *config* refs in committed docs/configs -----
# Carve-outs (allowed, NOT flagged):
#   - ~/.agents/skills/<x>/scripts/   vendored tool calls
#   - ~/.culture/                     Culture mesh data this skill is supposed to read
md_yaml=()
for file in "${files[@]}"; do
    if [[ "$file" =~ \.(md|ya?ml|toml|json|jsonc)$ ]]; then
        md_yaml+=("$file")
    fi
done

hits2=""
if [ ${#md_yaml[@]} -gt 0 ]; then
    hits2=$(grep -HnE '~/\.[A-Za-z]' "${md_yaml[@]}" 2>/dev/null \
        | grep -vE '~/\.agents/skills/[^[:space:]"]+/scripts/' \
        | grep -vE '~/\.culture/' \
        || true)
fi

fail=0
if [ -n "$hits1" ]; then
    echo "❌ Hard-coded /home/<user>/ paths:"
    echo "$hits1" | sed 's/^/    /'
    echo "   Fix: use ../sibling, repo URL, or \$WORKSPACE/sibling instead."
    fail=1
fi
if [ -n "$hits2" ]; then
    [ "$fail" -eq 1 ] && echo
    echo "❌ Per-user ~/.<dotfile> config refs in committed doc/config:"
    echo "$hits2" | sed 's/^/    /'
    echo "   Allowed carve-outs: ~/.agents/skills/.../scripts/ (tool calls), ~/.culture/ (mesh data)."
    echo "   Otherwise: commit a repo-local config or document a portable lookup."
    fail=1
fi

[ "$fail" -eq 0 ] && echo "✓ portability lint clean (${#files[@]} files checked)"
exit $fail

#!/usr/bin/env bash
# Local CI: runs the unit tests of a branch in a temporary worktree.
#   scripts/ci.sh            the current checkout
#   scripts/ci.sh <branch>   another branch, without touching the current checkout
set -uo pipefail

run_tests() { python3 -m unittest discover -s tests -t . 2>&1 | tail -n 3; return "${PIPESTATUS[0]}"; }

if [[ $# -eq 0 ]]; then
    label="$(git rev-parse --abbrev-ref HEAD) @ $(git rev-parse --short HEAD)"
    run_tests; status=$?
else
    label="$1 @ $(git rev-parse --short "$1")"
    dir="$(mktemp -d)"
    git worktree add -q --detach "$dir" "$1" || exit 2
    (cd "$dir" && run_tests); status=$?
    git worktree remove --force "$dir"
fi
if [[ $status -eq 0 ]]; then echo "CI: PASS ($label)"; else echo "CI: FAIL ($label)"; fi
exit "$status"

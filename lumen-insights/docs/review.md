# Review checklist

A branch waiting for review is named in its ticket (`branch`, `review: waiting`). The reviewer checks:

- [ ] The ticket and its spec (docs/specs/) are linked
- [ ] Tests are added or updated
- [ ] `scripts/ci.sh <branch>` passes before the merge
- [ ] The ticket says what QA should check

The reviewer writes the outcome in the ticket's log, then merges into `develop` with `--no-ff`.

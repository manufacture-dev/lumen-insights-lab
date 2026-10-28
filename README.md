# Lumen Insights lab

A fictional repository for hands-on workshops on agentic organisations. Lumen Retail, its people and its data are invented.

This repository is the kit: it builds the training repository with a dated history. Participants work on the training repository, inside an isolated [Taxiway](https://github.com/taxiway-sh/taxiway) lab, never on this one.

## What the training repository looks like

A small retail analytics module: dashboard KPIs (revenue, orders, average basket, top products) and their CSV export, in Python with no dependency; tests use `unittest`.

- **Tickets in the repository.** `work/` is the ticket board: one Markdown file per ticket, with its status, acceptance criteria and log. Each status change is a commit, so `git log -p work/<file>` is the ticket's history.
- **History.** Three months of commits by four roles (product owner, dev lead, developer, QA), from 20 July to 23 October 2026. Git flow: `main` at release 1.3.0 (tag `v1.3.0`), work on `develop`.
- **Branches waiting for review**, named in their tickets:
  - `feature/2-retention-cohort`: `scripts/ci.sh` passes.
  - `fix/3-refund-basket`: `scripts/ci.sh` fails.
- **Current practices.** A short `CLAUDE.md`, one personal skill (`spec-from-ticket`), ticket templates, a review checklist, a local CI script, a release process with a go from product and QA, manual QA with test plans and a regression checklist.

| # | Type | Status | Subject |
|---|---|---|---|
| 1 | Story | ready-for-qa | Export the dashboard KPIs to CSV |
| 2 | Story | in-review | Monthly retention cohorts |
| 3 | Bug | in-review | Average basket too low when an order is fully refunded |
| 4 | Story | ready-for-dev | Growth versus the previous period |
| 5 | Story | refinement | Filter top products by category |
| 6 | Chore | in-progress | Release 1.4 |

## Layout

| Path | What |
|---|---|
| `lumen-insights/` | The files of the training repository, as on `develop` |
| `versions/` | Earlier versions of ticket files, replayed by the history |
| `branches/` | The files each review branch adds or changes |
| `build_lab.py` | Builds the training repository with its history |

## Use

1. Build it and publish it as a **private** repository, which Taxiway will read as the lab's source:

   ```bash
   python3 -I build_lab.py ./lumen-insights
   cd lumen-insights
   git remote add origin https://github.com/<owner>/lumen-insights.git
   git push -u origin --all && git push origin --tags
   ```

2. Create the lab. Taxiway mirrors the repository on the host and clones it into an isolated VM; the agent commits and pushes there, nothing goes back to GitHub. No GitHub token is needed in the lab.

   ```bash
   taxiway up atelier --type claude-code --driver lima \
     --repo https://github.com/<owner>/lumen-insights --repo-ref develop \
     --set auth_mode=api-key --set claude-code-version=<release>
   taxiway shell atelier
   ```

3. To run the workshop again from scratch: `taxiway rm atelier`, then `taxiway up` again. The lab's copy starts over from the published repository.

# Lumen Insights lab

A fictional repository for hands-on workshops on agentic organisations. Lumen Retail, its people and its data are invented.

This repository is the kit: it builds the training repository, with a dated history, and seeds it on GitHub with labels, issues and pull requests. Participants work on the seeded repository, never on this one.

## What the training repository looks like

A small retail analytics module: dashboard KPIs (revenue, orders, average basket, top products) and their CSV export, in Python with no runtime dependency.

- **History.** Three months of commits by three roles (dev lead, developer, QA), from 20 July to 23 October 2026. Git flow: `main` at release 1.3.0 (tag `v1.3.0`), work on `develop`.
- **Branches waiting for review.**
  - `feature/2-retention-cohort`: CI green.
  - `fix/3-refund-basket`: CI red.
- **Current practices.** A short `CLAUDE.md`, one personal skill (`spec-from-issue`), PR and story templates, a CI workflow, a release process with a go from product and QA, manual QA with test plans and a regression checklist.
- **Issues and pull requests.**

| # | Type | Status | Subject |
|---|---|---|---|
| 1 | Story | ready-for-qa | Export the dashboard KPIs to CSV |
| 2 | Story | in-review | Monthly retention cohorts |
| 3 | Bug | in-review | Average basket too low when an order is fully refunded |
| 4 | Story | ready-for-dev | Growth versus the previous period |
| 5 | Story | refinement | Filter top products by category |
| 6 | Chore | in-progress | Release 1.4 |
| 7 | PR | open | Monthly retention cohorts (`feature/2-retention-cohort`) |
| 8 | PR | open | Fix average basket with fully refunded orders (`fix/3-refund-basket`) |

## Layout

| Path | What |
|---|---|
| `lumen-insights/` | The files of the training repository, as on `develop` |
| `branches/` | The files each review branch adds or changes |
| `github/` | Labels, issues (with their comments) and pull requests to create |
| `build_lab.py` | Builds the training repository locally, with its history |
| `seed_github.py` | Builds it, creates it on GitHub as a private repository and seeds it |

## Use

Build locally only:

```bash
python3 -I build_lab.py /tmp/lumen-insights
```

Create and seed on GitHub, with the GitHub CLI (`gh`) logged in:

```bash
python3 -I seed_github.py <owner>/lumen-insights
```

Run it on a new, empty repository only: the script checks that the issue and PR numbers match those in the history and the documents. Pushing the two review branches triggers CI: #7 turns green, #8 red.

## Before a workshop

- Give the people who drive access to the seeded repository (collaborators), or prepare a machine with the repository cloned, `gh auth login` done and Claude Code up to date.
- The workshop works on a branch, for example `agentic/workshop`. To run it again, delete that branch. To start from scratch, comments and labels included, seed a new repository.
- Seed the repository the evening before, so that the pull requests have waited a day.

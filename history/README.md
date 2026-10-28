# Session history

Six Claude Code sessions of the Lumen team, from 20 July to 23 October 2026, as Claude Code 2.1.311 writes them (`~/.claude/projects/<project>/<session-id>.jsonl`). They give a lab a past to learn from: what people asked, what the assistant did, and what they corrected.

| Date | Role | Branch | Session |
|---|---|---|---|
| 2026-07-20 | dev lead | `main` | Revenue and orders KPIs for a period |
| 2026-07-29 | product owner | `main` | Draft the top products story (saves a memory) |
| 2026-09-15 | developer | `main` | Top products by revenue |
| 2026-10-14 | developer | `feature/1-kpi-csv-export` | Spec for the KPI CSV export |
| 2026-10-20 | developer | `develop` | Merge the CSV export into develop |
| 2026-10-23 | dev lead | `fix/3-refund-basket` | Fix the average basket with refunds |

What runs through them: corrections that come back from one session to the next, a merge whose consequences show up afterwards, and a memory saved in July that later sessions still read.

## Build

```bash
python3 -I history/build_history.py history/projects
```

`sessions.py` holds the sessions as readable data; `build_history.py` turns them into transcripts. Ids and timestamps derive from the sessions, so a rebuild gives the same files. `projects/` also gets `memory/`, the project memory as the sessions left it.

## Install in a lab

The lab's project folder is named after its working directory (`/lab/work/lumen-insights`):

```bash
limactl shell taxiway-<lab> mkdir -p .claude/projects/-lab-work-lumen-insights/memory
limactl copy history/projects/*.jsonl taxiway-<lab>:.claude/projects/-lab-work-lumen-insights/
limactl copy history/projects/memory/* taxiway-<lab>:.claude/projects/-lab-work-lumen-insights/memory/
```

Install before starting the session that should read them. In a lab that already has a project memory, append the line of `memory/MEMORY.md` to the existing index instead of replacing it. `limactl copy` keeps the files' dates, which are those of each session's last entry. Git does not keep them: rebuild (above) before installing from a fresh clone. The sessions are fictional; they hold no secret and no real data.

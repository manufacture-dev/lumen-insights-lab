"""Build the Lumen Insights training repository, with three months of dated history.

    python3 -I build_lab.py <target-dir>

The target must not exist. The result has `main` (release 1.3.0, tag v1.3.0),
`develop` (the KPI CSV export of ticket #1 merged without review, the ticket
board in work/) and two branches waiting for review:
`feature/2-retention-cohort` (tests pass) and `fix/3-refund-basket` (a new
test fails). Tickets are files in work/, and each status change is a commit.
Everything in it is fictional.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
TREE = KIT / "lumen-insights"
VERSIONS = KIT / "versions"
BRANCHES = KIT / "branches"

PEOPLE = {
    "lead": ("Dev Lead", "dev-lead@lumen.example"),
    "dev": ("Developer", "developer@lumen.example"),
    "qa": ("QA Engineer", "qa@lumen.example"),
    "po": ("Product Owner", "product-owner@lumen.example"),
}

T1 = "work/001-kpi-csv-export.md"
T2 = "work/002-retention-cohorts.md"
T3 = "work/003-average-basket-refunds.md"


def v(path, n):
    """An earlier version of a tree file, kept under versions/."""
    return (path, VERSIONS / path.replace(".md", f".v{n}.md"))


# Each step: ("commit", date, who, message, files) on the current branch,
# ("branch", name, start), ("checkout", name), ("merge", date, who, branch), ("tag", name, date).
# A file is a path in the tree, a (path, source) pair, or a branch overlay ("@<dir>").
STEPS = [
    ("commit", "2026-07-20T10:12", "lead", "Initial KPI module: revenue and orders for a period",
     ["README.md", "pyproject.toml", ".gitignore", "CLAUDE.md", ("scripts/ci.sh", VERSIONS / "scripts/ci.sh"),
      "src/lumen_insights/__init__.py", "src/lumen_insights/data.py", "src/lumen_insights/kpis.py",
      "tests/__init__.py", "tests/helpers.py", "tests/test_kpis.py", "tests/test_data.py",
      "data/sales_sample.csv"]),
    ("commit", "2026-08-05T15:40", "lead", "Add the ticket board, its templates and the review checklist",
     ["work/README.md", "work/templates/story.md", "work/templates/bug.md", "docs/review.md"]),
    ("commit", "2026-08-19T11:05", "qa", "QA: regression checklist and top products test plan",
     ["qa/README.md", "qa/regression-checklist.md", "qa/test-plans/top-products.md"]),
    ("commit", "2026-09-02T09:30", "lead", "docs: release process", ["docs/release.md"]),
    ("commit", "2026-09-24T17:20", "lead", "Add the spec-from-ticket skill and Claude Code settings",
     [".claude/skills/spec-from-ticket/SKILL.md", ".claude/settings.json"]),
    ("commit", "2026-10-01T16:00", "lead", "Release 1.3.0", ["CHANGELOG.md"]),
    ("tag", "v1.3.0", "2026-10-01T16:05"),
    ("branch", "develop", "main"),
    ("commit", "2026-10-08T09:20", "po", "work: #1 KPI CSV export, #4 growth, #5 top products by category",
     [v(T1, 1), "work/004-growth-previous-period.md", "work/005-top-products-by-category.md"]),
    ("commit", "2026-10-13T14:00", "lead", "work(#1): ready-for-dev", [v(T1, 2)]),
    ("branch", "feature/1-kpi-csv-export", "develop"),
    ("commit", "2026-10-14T10:45", "dev", "docs: spec for #1 KPI CSV export",
     ["docs/specs/1-kpi-csv-export.md", v(T1, 3)]),
    ("checkout", "develop"),
    ("commit", "2026-10-15T16:30", "lead", "work(#2): ready-for-dev", [v(T2, 1)]),
    ("checkout", "feature/1-kpi-csv-export"),
    ("commit", "2026-10-16T14:10", "dev", "feat: export the KPIs of a period to CSV (#1)",
     ["src/lumen_insights/export.py", "tests/test_export.py"]),
    ("checkout", "develop"),
    ("merge", "2026-10-20T18:15", "dev", "feature/1-kpi-csv-export"),
    ("commit", "2026-10-20T18:20", "dev", "work(#1): ready-for-qa", [T1]),
    ("commit", "2026-10-21T10:40", "qa", "work(#3): average basket too low with refunds, found testing #1",
     [v(T3, 1)]),
    ("commit", "2026-10-21T15:10", "lead", "work(#6): release 1.4", ["work/006-release-1-4.md"]),
    ("branch", "feature/2-retention-cohort", "develop"),
    ("commit", "2026-10-22T11:30", "dev", "feat: monthly retention cohorts (#2)", ["@feature-2-retention-cohort"]),
    ("checkout", "develop"),
    ("commit", "2026-10-22T11:45", "dev", "work(#2): in-review", [T2]),
    ("branch", "fix/3-refund-basket", "develop"),
    ("commit", "2026-10-23T16:50", "lead", "fix: average basket ignores fully refunded orders (#3)",
     ["@fix-3-refund-basket"]),
    ("checkout", "develop"),
    ("commit", "2026-10-23T17:00", "lead", "work(#3): in-review", [T3]),
    ("commit", "2026-10-23T17:30", "lead", "ci: find a branch that exists only on origin", ["scripts/ci.sh"]),
]


def git(repo, *args, when=None, who="lead"):
    env = dict(os.environ)
    if when:
        name, email = PEOPLE[who]
        stamp = when + ":00+02:00"
        env.update(GIT_AUTHOR_NAME=name, GIT_AUTHOR_EMAIL=email, GIT_COMMITTER_NAME=name,
                   GIT_COMMITTER_EMAIL=email, GIT_AUTHOR_DATE=stamp, GIT_COMMITTER_DATE=stamp)
    subprocess.run(["git", "-C", str(repo), *args], check=True, env=env, stdout=subprocess.DEVNULL)


def sources(entry):
    if isinstance(entry, tuple):
        yield entry
    elif entry.startswith("@"):
        root = BRANCHES / entry[1:]
        for p in sorted(root.rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts:
                yield str(p.relative_to(root)), p
    else:
        yield entry, TREE / entry


def commit(repo, when, who, message, files):
    paths = []
    for entry in files:
        for rel, src in sources(entry):
            dest = repo / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            paths.append(rel)
    git(repo, "add", "--", *paths)
    git(repo, "commit", "-q", "-m", message, when=when, who=who)


def build(target):
    repo = Path(target)
    if repo.exists():
        sys.exit(f"{repo} already exists")
    repo.mkdir(parents=True)
    git(repo, "init", "-q", "-b", "main")
    for step in STEPS:
        kind = step[0]
        if kind == "commit":
            commit(repo, *step[1:])
        elif kind == "tag":
            git(repo, "tag", "-a", step[1], "-m", f"Release {step[1][1:]}", when=step[2])
        elif kind == "branch":
            git(repo, "checkout", "-q", "-b", step[1], step[2])
        elif kind == "checkout":
            git(repo, "checkout", "-q", step[1])
        elif kind == "merge":
            git(repo, "merge", "-q", "--no-ff", step[3], "-m", f"Merge branch '{step[3]}' into develop",
                when=step[1], who=step[2])
    git(repo, "branch", "-q", "-d", "feature/1-kpi-csv-export")
    print(f"built {repo}: main, develop, feature/2-retention-cohort, fix/3-refund-basket, tag v1.3.0")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    build(sys.argv[1])

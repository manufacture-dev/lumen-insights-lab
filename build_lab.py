"""Build the Lumen Insights lab repository, with three months of dated history.

    python3 -I build_lab.py <target-dir>

The target must not exist. The result has `main` (release 1.3.0, tag v1.3.0),
`develop` (the KPI CSV export of issue #1 merged without a PR) and two branches
waiting for review: `feature/2-retention-cohort` (green) and
`fix/3-refund-basket` (its new test fails, so CI is red).
Everything in it is fictional.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent
TREE = LAB / "lumen-insights"
BRANCHES = LAB / "branches"

PEOPLE = {
    "lead": ("Dev Lead", "dev-lead@lumen.example"),
    "dev": ("Developer", "developer@lumen.example"),
    "qa": ("QA Engineer", "qa@lumen.example"),
}

# (date, author, message, files from the tree)
MAIN = [
    ("2026-07-20T10:12:00", "lead", "Initial KPI module: revenue and orders for a period",
     ["README.md", "pyproject.toml", ".gitignore", "CLAUDE.md", ".github/workflows/ci.yml",
      "src/lumen_insights/__init__.py", "src/lumen_insights/data.py", "src/lumen_insights/kpis.py",
      "tests/conftest.py", "tests/test_kpis.py", "tests/test_data.py", "data/sales_sample.csv"]),
    ("2026-08-05T15:40:00", "lead", "Add PR and story templates",
     [".github/pull_request_template.md", ".github/ISSUE_TEMPLATE/story.md"]),
    ("2026-08-19T11:05:00", "qa", "QA: regression checklist and top products test plan",
     ["qa/README.md", "qa/regression-checklist.md", "qa/test-plans/top-products.md"]),
    ("2026-09-02T09:30:00", "lead", "docs: release process", ["docs/release.md"]),
    ("2026-09-24T17:20:00", "lead", "Add the spec-from-issue skill and Claude Code settings",
     [".claude/skills/spec-from-issue/SKILL.md", ".claude/settings.json"]),
    ("2026-10-01T16:00:00", "lead", "Release 1.3.0", ["CHANGELOG.md"]),
]
FEATURE_1 = [
    ("2026-10-14T10:45:00", "dev", "docs: spec for #1 KPI CSV export", ["docs/specs/1-kpi-csv-export.md"]),
    ("2026-10-16T14:10:00", "dev", "feat: export the KPIs of a period to CSV (#1)",
     ["src/lumen_insights/export.py", "tests/test_export.py"]),
]
FEATURE_2 = ("2026-10-22T11:30:00", "dev", "feat: monthly retention cohorts (#2)", "feature-2-retention-cohort")
FIX_3 = ("2026-10-23T16:50:00", "lead", "fix: average basket ignores fully refunded orders (#3)", "fix-3-refund-basket")


def git(repo, *args, when=None, who="lead"):
    env = dict(os.environ)
    if when:
        name, email = PEOPLE[who]
        env.update(GIT_AUTHOR_NAME=name, GIT_AUTHOR_EMAIL=email, GIT_COMMITTER_NAME=name,
                   GIT_COMMITTER_EMAIL=email, GIT_AUTHOR_DATE=when + "+02:00", GIT_COMMITTER_DATE=when + "+02:00")
    subprocess.run(["git", "-C", str(repo), *args], check=True, env=env, stdout=subprocess.DEVNULL)


def copy(src_root, rel, repo):
    dest = repo / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_root / rel, dest)


def commit(repo, when, who, message, files, root=TREE):
    for rel in files:
        copy(root, rel, repo)
    git(repo, "add", "--", *files)
    git(repo, "commit", "-q", "-m", message, when=when, who=who)


def overlay(repo, branch_dir):
    root = BRANCHES / branch_dir
    files = [str(p.relative_to(root)) for p in sorted(root.rglob("*")) if p.is_file()]
    return root, files


def build(target):
    repo = Path(target)
    if repo.exists():
        sys.exit(f"{repo} already exists")
    repo.mkdir(parents=True)
    git(repo, "init", "-q", "-b", "main")
    for when, who, message, files in MAIN:
        commit(repo, when, who, message, files)
    git(repo, "tag", "-a", "v1.3.0", "-m", "Release 1.3.0", when="2026-10-01T16:05:00")
    git(repo, "checkout", "-q", "-b", "develop")
    git(repo, "checkout", "-q", "-b", "feature/1-kpi-csv-export")
    for when, who, message, files in FEATURE_1:
        commit(repo, when, who, message, files)
    git(repo, "checkout", "-q", "develop")
    git(repo, "merge", "-q", "--no-ff", "feature/1-kpi-csv-export", "-m",
        "Merge branch 'feature/1-kpi-csv-export' into develop", when="2026-10-20T18:15:00", who="dev")
    git(repo, "branch", "-q", "-d", "feature/1-kpi-csv-export")
    for (when, who, message, branch_dir), branch in ((FEATURE_2, "feature/2-retention-cohort"),
                                                     (FIX_3, "fix/3-refund-basket")):
        git(repo, "checkout", "-q", "-b", branch, "develop")
        root, files = overlay(repo, branch_dir)
        commit(repo, when, who, message, files, root=root)
    git(repo, "checkout", "-q", "develop")
    print(f"built {repo}: main, develop, feature/2-retention-cohort, fix/3-refund-basket, tag v1.3.0")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    build(sys.argv[1])

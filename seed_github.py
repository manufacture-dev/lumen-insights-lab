"""Create the Lumen Insights lab on GitHub: repository, branches, labels, issues and PRs.

    python3 -I seed_github.py <owner>/<name> [<work-dir>]

Needs the GitHub CLI (`gh`) logged in with the right to create a repository
under <owner>. Builds the repository with build_lab.py in <work-dir> (default
./lumen-insights), creates it as a PRIVATE repository, pushes every branch and
the tag, sets `develop` as default branch, then creates the labels, issues #1-#6
(with their comments) and the PRs #7 and #8, in that order so that the numbers
match the ones the history and the documents use. Run it on a new, empty
repository only.
"""
import subprocess
import sys
import time
from pathlib import Path

LAB = Path(__file__).resolve().parent
GH = LAB / "github"
COMMENT = "\n<!-- comment -->\n"


def run(*args, cwd=None, capture=False):
    out = subprocess.run(args, cwd=cwd, check=True, text=True, capture_output=capture)
    return out.stdout.strip() if capture else None


def parse(path):
    head, body = path.read_text().split("\n---\n", 1)
    meta = dict(line.split(": ", 1) for line in head.splitlines())
    body, *comments = body.split(COMMENT)
    return meta, body.strip(), [c.strip() for c in comments]


def expect(url, number):
    got = int(url.rstrip("/").rsplit("/", 1)[1])
    if got != number:
        sys.exit(f"expected #{number}, got #{got}: run on a new, empty repository")


def main(repo, work_dir="lumen-insights"):
    work = Path(work_dir)
    run(sys.executable, "-I", str(LAB / "build_lab.py"), str(work))
    run("gh", "repo", "create", repo, "--private",
        "--description", "Lumen Insights: training lab for an agentic organisation (fictional)")
    run("git", "remote", "add", "origin", f"https://github.com/{repo}.git", cwd=work)
    run("git", "push", "-q", "-u", "origin", "main", "develop", "feature/2-retention-cohort",
        "fix/3-refund-basket", "--tags", cwd=work)
    run("gh", "repo", "edit", repo, "--default-branch", "develop")
    for line in (GH / "labels.tsv").read_text().splitlines():
        name, color, description = line.split("\t")
        run("gh", "label", "create", name, "--repo", repo, "--color", color, "--description", description, "--force")
    for path in sorted((GH / "issues").glob("*.md")):
        meta, body, comments = parse(path)
        url = run("gh", "issue", "create", "--repo", repo, "--title", meta["title"], "--body", body,
                  *[a for label in meta["labels"].split(", ") for a in ("--label", label)], capture=True)
        expect(url, int(path.stem))
        for comment in comments:
            run("gh", "issue", "comment", url, "--body", comment)
        print(f"issue {url}")
    for path in sorted((GH / "prs").glob("*.md")):
        meta, body, _ = parse(path)
        url = run("gh", "pr", "create", "--repo", repo, "--base", "develop", "--head", meta["head"],
                  "--title", meta["title"], "--body", body, capture=True)
        expect(url, int(path.stem))
        print(f"pr {url}")
        time.sleep(1)
    print(f"done: https://github.com/{repo} (CI runs on the two PR branches: #7 green, #8 red)")


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__)
    main(*sys.argv[1:])

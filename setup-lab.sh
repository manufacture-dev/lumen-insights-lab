#!/usr/bin/env bash
# Prepare a fresh Taxiway lab for the workshop, from the host, after `taxiway up` and `taxiway auth`:
# browser for acceptance tests, simulated session history, workshop branch, checks.
#   ./setup-lab.sh [lab]        (default: atelier)
set -euo pipefail
LAB="${1:-atelier}"
VM="taxiway-$LAB"
KIT="$(cd "$(dirname "$0")" && pwd)"
REPO=/lab/work/lumen-insights
PROJECTS='$HOME/.claude/projects/-lab-work-lumen-insights'
in_vm() { limactl shell --workdir "$REPO" "$VM" bash -lc "$1"; }

echo "== browser: agent-browser + Playwright's arm64 Chromium (Chrome for Testing has no linux-arm64 build)"
in_vm 'sudo npm i -g agent-browser@0.34.0 >/dev/null 2>&1
cd /tmp && sudo npx -y playwright@1.56.1 install-deps chromium >/dev/null 2>&1 && npx -y playwright@1.56.1 install chromium >/dev/null 2>&1
CHROME=$(ls -d $HOME/.cache/ms-playwright/chromium-*/chrome-linux/chrome | head -1)
# As Playwright does by default in a VM: Chromium without its own sandbox; the VM is the fence.
printf "export AGENT_BROWSER_EXECUTABLE_PATH=%s\nexport AGENT_BROWSER_ARGS=--no-sandbox\n" "$CHROME" | sudo tee /etc/profile.d/agent-browser.sh >/dev/null
mkdir -p $HOME/.config/taxiway && touch $HOME/.config/taxiway/env
grep -q AGENT_BROWSER $HOME/.config/taxiway/env || printf "AGENT_BROWSER_EXECUTABLE_PATH=%s\nAGENT_BROWSER_ARGS=--no-sandbox\n" "$CHROME" >> $HOME/.config/taxiway/env
mkdir -p $HOME/.claude/skills/agent-browser'
limactl copy "$HOME/.agents/skills/agent-browser/SKILL.md" "$VM:/home/$(whoami).guest/.claude/skills/agent-browser/SKILL.md" >/dev/null

echo "== history: six simulated past sessions for brick 7"
python3 -I "$KIT/history/build_history.py" >/dev/null
in_vm "mkdir -p $PROJECTS/memory"
for f in "$KIT"/history/projects/*.jsonl; do limactl copy "$f" "$VM:/home/$(whoami).guest/.claude/projects/-lab-work-lumen-insights/" >/dev/null; done
for f in "$KIT"/history/projects/memory/*.md; do
  [ "$(basename "$f")" = MEMORY.md ] && continue
  limactl copy "$f" "$VM:/home/$(whoami).guest/.claude/projects/-lab-work-lumen-insights/memory/" >/dev/null
done
in_vm "cat >> $PROJECTS/memory/MEMORY.md" < "$KIT/history/projects/memory/MEMORY.md"
in_vm "touch -r $PROJECTS/memory/tickets-in-tracker.md $PROJECTS/memory/MEMORY.md 2>/dev/null || true"

echo "== workshop branch"
in_vm 'git checkout -q develop && (git checkout -q -b agentic/workshop 2>/dev/null || git checkout -q agentic/workshop) && git branch --show-current'

echo "== checks"
in_vm 'git log --oneline | wc -l | xargs echo commits:
scripts/ci.sh fix/3-refund-basket | tail -1
scripts/ci.sh feature/2-retention-cohort | tail -1
claude mcp list 2>&1 | tail -1
ls $HOME/.claude/projects/-lab-work-lumen-insights/*.jsonl | wc -l | xargs echo "history sessions:"
(PYTHONPATH=src nohup python3 -m lumen_insights.web --port 8000 >/tmp/web.log 2>&1 &); sleep 2
agent-browser open "http://127.0.0.1:8000/?start=2026-09-01&end=2026-09-30" >/dev/null && agent-browser get text body | head -3; agent-browser close >/dev/null
for p in $(pgrep -f "lumen_insights[.]web"); do kill $p; done; true'
echo "== ready. Next, live: taxiway access; taxiway record start $LAB; taxiway shell $LAB"

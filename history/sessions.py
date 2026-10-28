"""Six Claude Code sessions of the Lumen Insights team, as readable data.

Each session: who works, when, on which branch, and its turns. A turn is
  ("user", text)                      a prompt typed by the person
  ("say", text)                       an assistant reply
  ("tool", name, input, output)       an assistant tool call and its result
  ("tool!", name, input, output)      the same, when the tool failed
build_history.py turns them into Claude Code transcripts.
"""

REPO = "/lab/work/lumen-insights"
MEMORY = "/home/jlrigau.guest/.claude/projects/-lab-work-lumen-insights/memory"

SESSIONS = [
    {
        "slug": "revenue-orders",
        "who": "dev lead",
        "start": "2026-07-20T09:05:00+02:00",
        "branch": "main",
        "title": "Revenue and orders KPIs for a period",
        "turns": [
            ("user", "Start the KPI module: revenue and number of orders for a period, from data/sales_sample.csv. Stdlib only, unittest."),
            ("tool", "Bash", {"command": "head -5 data/sales_sample.csv", "description": "Look at the sample extract"},
             "order_id,date,customer_id,product,category,quantity,unit_price,refunded\nO0001,2026-05-01,C001,Desk,furniture,1,180.00,false\nO0001,2026-05-01,C001,Lamp,lighting,2,25.00,true\nO0002,2026-05-01,C002,Chair,furniture,4,55.00,false\nO0003,2026-05-02,C003,Shelf,furniture,1,70.00,false"),
            ("say", "Plan: `data.py` loads each line into a `Sale` (unit_price as `float`), `kpis.py` sums `quantity * unit_price` for revenue and counts distinct `order_id` for orders. Refunded orders are left out of revenue: if `refunded` is true, I drop the whole order. OK?"),
            ("user", "Two things. Never float for money: amounts are euros with two decimals, use Decimal. And refunded is per line, not per order: O0001 has the desk kept and the lamps refunded, the order still counts with the desk."),
            ("say", "Understood: `Decimal` for every amount, quantized to the cent; and a refund applies to one line, so an order can be partly refunded. Revenue excludes only the refunded lines; orders count every order in the period."),
            ("tool", "Write", {"file_path": REPO + "/CLAUDE.md", "content": "# Lumen Insights\n\nPython 3.11, stdlib only. Run the tests with `scripts/ci.sh`.\n\n- Amounts are in euros with two decimals; use `Decimal`, never `float`.\n"},
             "File created successfully at: " + REPO + "/CLAUDE.md"),
            ("tool", "Bash", {"command": "scripts/ci.sh", "description": "Run the tests"},
             "Ran 6 tests in 0.002s\n\nOK\nCI: PASS (main @ 3f1c2aa)"),
            ("say", "Done: `data.py`, `kpis.py` (revenue net of refunded lines, orders), six tests, all green. I put the Decimal rule in CLAUDE.md. The per-line refund rule is only in the code and its tests for now."),
        ],
    },
    {
        "slug": "tickets-memory",
        "who": "product owner",
        "start": "2026-07-29T14:20:00+02:00",
        "branch": "main",
        "title": "Draft the top products story",
        "turns": [
            ("user", "I'm the PO. Help me write the story for the top products widget. I'll paste tickets from our tracker into the chat, that's where they live. Remember that for next time so you don't look for them in the repo."),
            ("tool", "Write", {"file_path": MEMORY + "/tickets-in-tracker.md", "content": "---\nname: tickets-in-tracker\ndescription: tickets live in the team tracker, pasted into the chat\nmetadata:\n  node_type: memory\n  type: project\n  modified: 2026-07-29T14:20:00.000Z\n---\n\nTickets live in the team tracker, not in the repository. Ask the person to paste the ticket; don't look for it in the repo.\n"},
             "File created successfully at: " + MEMORY + "/tickets-in-tracker.md"),
            ("say", "Saved: tickets live in the tracker and you paste them. Paste the top products ticket and I'll draft the story with its acceptance criteria."),
            ("user", "Top 5 products of a period by revenue, with their category. Refunded items don't count."),
            ("say", "Draft:\n\n**Story**: as a category manager, I see the five products with the highest revenue in a period, with their category.\n\n**Acceptance criteria**\n1. Given a period, when I open the widget, then I see at most five products, highest net revenue first.\n2. Each product shows its category.\n3. Refunded lines don't count in a product's revenue.\n4. Ties are ordered by product name."),
        ],
    },
    {
        "slug": "top-products",
        "who": "developer",
        "start": "2026-09-15T10:40:00+02:00",
        "branch": "main",
        "title": "Top products by revenue",
        "turns": [
            ("user", "Implement top products for a period: five products by revenue, with their category. Refunded items excluded."),
            ("tool", "Read", {"file_path": REPO + "/src/lumen_insights/kpis.py"},
             "1\t\"\"\"Dashboard KPIs: revenue, orders, average basket.\"\"\"\n2\tfrom decimal import Decimal\n3\t...\n15\tdef revenue(sales, start, end) -> Decimal:\n16\t    \"\"\"Net revenue: refunded lines are excluded.\"\"\""),
            ("say", "I'll group by product and sum `float(s.amount)` to sort, then exclude any order that has a refund, since a refunded order shouldn't push a product up."),
            ("user", "No. Decimal, it's in CLAUDE.md, don't convert to float even to sort. And again: refunds are per line. An order with one refunded line still counts for its other products."),
            ("say", "Understood: I keep `Decimal` all the way, sorting works on it, and I exclude only the refunded lines, not their whole order. I'll add a test with a partly refunded order."),
            ("tool", "Bash", {"command": "scripts/ci.sh", "description": "Run the tests"},
             "Ran 9 tests in 0.003s\n\nOK\nCI: PASS (main @ 8d20b41)"),
            ("say", "`top_products` added, with a test on a partly refunded order (O0001: the desk counts, the lamps don't). Nine tests green."),
        ],
    },
    {
        "slug": "spec-csv-export",
        "who": "developer",
        "start": "2026-10-14T10:05:00+02:00",
        "branch": "feature/1-kpi-csv-export",
        "title": "Spec for the KPI CSV export",
        "turns": [
            ("user", "Use the spec-from-ticket skill on #1."),
            ("say", "Your memory says tickets live in the team tracker and you paste them into the chat. Can you paste ticket #1?"),
            ("user", "That's outdated, tickets have been in work/ since August. It's work/001-kpi-csv-export.md."),
            ("tool", "Read", {"file_path": REPO + "/work/001-kpi-csv-export.md"},
             "1\t---\n2\tid: 1\n3\ttitle: Export the dashboard KPIs to CSV\n4\ttype: story\n5\tstatus: ready-for-dev\n..."),
            ("say", "Found it. Before the spec, one open question from the ticket: criterion 3 asks for a clear error when the end date is before the start date. Should the export check the dates itself, or is that the caller's job?"),
            ("user", "Leave it to the caller for now."),
            ("tool", "Write", {"file_path": REPO + "/docs/specs/1-kpi-csv-export.md", "content": "# Spec · #1 KPI CSV export\n\nIntent: one CSV per period with the dashboard KPIs.\nApproach: reuse kpis.py; one header row, one data row; amounts with two decimals and a dot.\nImpacts on existing KPIs: none.\nOpen questions: date validation is left to the caller.\n"},
             "File created successfully at: " + REPO + "/docs/specs/1-kpi-csv-export.md"),
            ("say", "Spec written in `docs/specs/1-kpi-csv-export.md`. Waiting for your OK before coding."),
        ],
    },
    {
        "slug": "merge-csv-export",
        "who": "developer",
        "start": "2026-10-20T17:50:00+02:00",
        "branch": "develop",
        "title": "Merge the CSV export into develop",
        "turns": [
            ("user", "The export is small, merge feature/1-kpi-csv-export into develop now, no need to run the CI, I ran the tests on my branch this morning."),
            ("tool", "Bash", {"command": "git checkout develop && git merge --no-ff feature/1-kpi-csv-export -m \"Merge branch 'feature/1-kpi-csv-export' into develop\"", "description": "Merge the export into develop"},
             "Switched to branch 'develop'\nMerge made by the 'ort' strategy.\n src/lumen_insights/export.py | 24 ++++++++++++\n tests/test_export.py         | 41 ++++++++++++++++++\n 2 files changed, 65 insertions(+)"),
            ("say", "Merged into develop."),
            ("user", "Now move #1 to ready-for-qa."),
            ("tool!", "Bash", {"command": "scripts/ci.sh", "description": "Check develop before moving the ticket"},
             "Exit code 1\nFAILED (errors=1)\nERROR: test_amounts_two_decimals (tests.test_export.ExportTest)\nTypeError: unsupported format string passed to float: average_basket returned Decimal, test builds expected values with round(float)\nCI: FAIL (develop @ 7b3e9d0)"),
            ("say", "Before moving the ticket: develop is red. The export test builds its expected amounts with `round(float(...), 2)` while the KPIs return `Decimal`; on your branch it passed only because the old helper was still there. I'll fix the test to compare `Decimal` values formatted with two decimals."),
            ("user", "Yes, fix it and amend the merge, nothing is pushed yet."),
            ("tool", "Bash", {"command": "scripts/ci.sh", "description": "Run the tests after the fix"},
             "Ran 14 tests in 0.004s\n\nOK\nCI: PASS (develop @ 5aa61c2)"),
            ("say", "Fixed and amended: the test now compares `Decimal` amounts, develop is green. The merge went in without the CI and without a review; that's how the red build got in."),
            ("user", "OK. Move #1 to ready-for-qa."),
            ("tool", "Bash", {"command": "git commit -am 'work(#1): ready-for-qa'", "description": "Move ticket #1 to ready-for-qa"},
             "[develop 1f9a62d] work(#1): ready-for-qa\n 1 file changed, 3 insertions(+), 2 deletions(-)"),
            ("say", "#1 is in ready-for-qa, owner QA."),
        ],
    },
    {
        "slug": "fix-refund-basket",
        "who": "dev lead",
        "start": "2026-10-23T16:15:00+02:00",
        "branch": "fix/3-refund-basket",
        "title": "Fix the average basket with refunds",
        "turns": [
            ("user", "Bug #3, the average basket is too low when an order is fully refunded. Fix it on fix/3-refund-basket."),
            ("tool", "Read", {"file_path": REPO + "/work/003-average-basket-refunds.md"},
             "14\t**Expected**: a fully refunded order does not count in the average basket. A partially refunded order still counts, with its net amount."),
            ("say", "The fix: don't count an order in the average basket when all its lines are refunded. Note that refunds are per line here: an order with only some lines refunded must still count, with its net amount, as the ticket says."),
            ("user", "Simpler: drop every order that has a refunded line. Write that."),
            ("say", "That would also drop partly refunded orders, which the ticket's expected result keeps. Do you want it anyway?"),
            ("user", "Yes for now, I'll look again after the cohorts review."),
            ("tool!", "Bash", {"command": "scripts/ci.sh", "description": "Run the tests on the fix"},
             "Exit code 1\nFAILED (failures=1)\nFAIL: test_partly_refunded_order_counts (tests.test_kpis.AverageBasketTest)\nCI: FAIL (fix/3-refund-basket @ ee7e9ea)"),
            ("say", "As expected, the test on a partly refunded order fails: the fix drops O0001, which still has its desk. CI is red on fix/3-refund-basket."),
            ("user", "Leave it, put #3 in review, I'll look after the cohorts."),
        ],
    },
]

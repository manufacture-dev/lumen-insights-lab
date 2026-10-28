# QA

How QA works on Lumen Insights today.

1. Start from a ticket in `work/` with `status: ready-for-qa`. Read its acceptance criteria and what it says QA should check.
2. Write the test plan in `qa/test-plans/<n>-<slug>.md`, one test case per acceptance criterion, plus edge cases.
3. Run it by hand on `develop` with the sample data.
4. A failing case becomes a bug ticket in `work/`, linked to the story. Blocking bugs are also sent to the developer directly.
5. When everything passes, set the ticket to `status: done` and note it in the release ticket.
6. After the release, add the feature to the regression checklist.

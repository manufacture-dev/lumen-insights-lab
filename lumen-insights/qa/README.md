# QA

How QA works on Lumen Insights today.

1. Start from an issue labelled `status:ready-for-qa`. Read the acceptance criteria and the PR "For QA" section.
2. Write the test plan in `qa/test-plans/<n>-<slug>.md`, one test case per acceptance criterion, plus edge cases.
3. Run it by hand on the `develop` build with the sample data.
4. A failing case becomes a bug issue (`type:bug`), linked to the story. Blocking bugs are also sent to the developer directly.
5. When everything passes, move the issue to `status:done` and note it in the release issue.
6. After the release, add the feature to the regression checklist.

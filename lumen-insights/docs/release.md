# Release process

- Git flow: features and fixes are merged into `develop`; a release is cut from `develop` to `main` every two weeks, on Wednesday.
- A release ticket (type `chore`, "Release x.y") in `work/` lists what goes in.
- Going to `main` needs the go of the product owner and of QA, written in the release ticket.
- Before the go, QA runs the manual regression checklist ([qa/regression-checklist.md](../qa/regression-checklist.md)).
- After the release, QA adds the new features to the checklist.

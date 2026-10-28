# Ticket board

One file per ticket, `<nnn>-<slug>.md`. The header holds the fields, the body the description, the acceptance criteria and a log.

| Field | Values |
|---|---|
| `type` | story, bug, chore |
| `status` | refinement → ready-for-dev → in-progress → in-review → ready-for-qa → done |
| `owner` | the role working on it now |
| `branch` | the branch carrying the change, once there is one |
| `review` | `waiting` (since a date), then the reviewer's outcome |

To move a ticket: change `status` and `updated`, add a line to the log (`- <date> · <role>: <what happened>`), and commit with the message `work(#<n>): <status>`. The history of a file is the history of its ticket: `git log -p work/<file>`.

Stories use [templates/story.md](templates/story.md), bugs [templates/bug.md](templates/bug.md).

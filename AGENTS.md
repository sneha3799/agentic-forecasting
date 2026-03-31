Files in `./planning-docs` provide additional context about projects we're working on that use this repo, such as bootcamps, competitions, or other research projects. We can also use files in this directory to store plans, do brainstorming, and otherwise record notes.

## Key planning-docs files

### planning-notes.md
For quick planning, decision tracking, and making sure we agree on what to work on next. Prepend date-stamped notes / log entries so that the most recent information is at the top.

### bootcamp-project-charter.md
The project charter — the agreement between Ethan and the project management office. This describes scope, methods, datasets, and design principles at a program level. Keep it free of implementation and technical architecture details.

### technical-design.md
**The technical source of truth.** Captures all significant architectural decisions, library selections, interface designs, and build plans.

**Maintenance contract (critical):** This document MUST be kept up to date at all times. Any time an architectural decision is made, revised, or reversed — in a coding session, a planning conversation, or a commit — `technical-design.md` must be updated in the same session. Do not let decisions live only in chat logs or planning notes. If you make a technical decision or learn that a prior decision has changed, update this file immediately before moving on.

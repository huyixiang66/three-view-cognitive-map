# Three-View Cognitive Map — Project Agent Instructions

This project uses project-butler memory files. Treat these files as the shared source of truth across AI coding assistants.

## Daily Workflow

- `end session` — save progress and next steps
- `continue` — resume next time
- `status` — check current project state

## Session Start

At the start of a task, read the project memory files that exist:

- `PROJECT.md`
- `session-handoff.md`
- `TODO.md`
- `UPDATE_LOG.md`
- `DOCS.md`
- `STRUCTURE.md`
- `CLAUDE.md`
- `.claude/project-profile.json`
- `.claude/profile-pending.json`

## Primary Triggers

| Intent | Action |
|--------|--------|
| End session / wrap up | Save progress, refresh next steps, record changes |
| Continue | Read session-handoff.md + PROJECT.md + TODO.md + logs |
| Check status | Show compact dashboard: Project, Active Work, Recent Change, Next Best Step |

## Advanced Triggers

| Intent | Action |
|--------|--------|
| Review constitution | Show `.claude/candidates.md` for confirmation |
| Sync wiki | Force rescan and update PROJECT.md |
| Organize files | Scan files and reorganize per STRUCTURE.md |
| Change language | Update language setting, rewrite management files |
| Continue full context | Full project trajectory recovery |

## End Session Protocol

1. Write `log/session-YYYY-MM-DD-{slug}.md`
2. Update `session-handoff.md`
3. Update `PROJECT.md` if structure changed
4. Update `TODO.md`
5. Append candidates to `.claude/candidates.md`
6. Organize new/changed files per STRUCTURE.md
7. Archive new docs under docs/ and update DOCS.md
8. If significant milestone, prepend entry to UPDATE_LOG.md
9. Output short summary

## File Roles

| File | Role |
|------|------|
| CLAUDE.md | Human-confirmed project rules |
| PROJECT.md | Current project overview |
| session-handoff.md | Next-session pickup point |
| TODO.md | Active task list |
| STRUCTURE.md | File organization rules |
| UPDATE_LOG.md | Milestone history |
| DOCS.md | Document index |
| log/session-*.md | Session logs |
| .claude/candidates.md | Candidate long-term rules |
| .claude/project-profile.json | Project profile config |
| .claude/profile-pending.json | Pending profile updates |

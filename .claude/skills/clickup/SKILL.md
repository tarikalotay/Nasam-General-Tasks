---
name: clickup
description: Create and manage ClickUp tasks for project tracking. Use when (1) logging completed work to tasks, (2) planning new features or milestones, (3) creating bug reports or tech debt tasks, (4) updating task status after code changes, (5) breaking down work into subtasks. Triggers on mentions of ClickUp, task creation, project tracking, or work planning.
---

# ClickUp

Read [references/clickup-api.md](references/clickup-api.md) for endpoints and auth.
Read [references/task-templates.md](references/task-templates.md) for description formats.

## Setup (once per machine)

This skill needs two things that are **not** in the repo:

1. `CLICKUP_TOKEN` in your shell environment — your own ClickUp personal token, never a shared one.
2. `references/clickup-ids.local.md` — the workspace, list, member and doc IDs.
   Copy `references/clickup-ids.example.md` to it and fill in the real values.

Both are deliberately kept out of git. See the reference file for why.

If either is missing, say so and stop — do not guess a list ID or post to the wrong list.

## Workflows

### Update Existing Task

1. Get task ID from context (branch, conversation, or ask)
2. Update status to next stage
3. Add completion comment with PR link

### Log Work Retroactively (no task existed)

1. Run `git log --oneline -20` to see recent commits
2. Run `git diff main...HEAD --stat` to see scope of changes
3. Draft task with Problem/Solution/What Ships from git context
4. Create task with status `shipped`
5. Show user for approval before creating

### Plan New Work

1. Determine list by domain (see `clickup-ids.local.md`)
2. Draft task with Problem/Solution/What Ships format
3. For milestones: plan subtasks for each deliverable
4. Show user for approval before creating

### Report Bug or Tech Debt

Use appropriate template from task-templates.md.

## Enforcement

**Always require:**
- Specific name: `[Action] [Thing] [Context]`
- Problem statement in description
- Done criteria

**Reject:**
- Vague names like "Backend", "Demo", "Update"
- Tasks without descriptions
- Creating without user approval

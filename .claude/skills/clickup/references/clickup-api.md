# ClickUp API Reference

**Official Docs**: https://developer.clickup.com/reference/

When you hit an error or need a new endpoint, consult the official docs and update this file.

## Authentication

The token comes from the environment. **Never write a token into this file** — an earlier version
of this reference carried a live personal token in plaintext, and it synced to every machine and
account that had the skill.

```bash
# In ~/.zshrc, ~/.bashrc, or a local .env that is gitignored — not here:
export CLICKUP_TOKEN="pk_..."      # ClickUp → Settings → Apps → API Token (personal, per-person)
```

Every script that uses it should fail loudly rather than silently sending an empty header:

```bash
: "${CLICKUP_TOKEN:?set CLICKUP_TOKEN — ClickUp → Settings → Apps → API Token}"
```

All requests: `-H "Authorization: $CLICKUP_TOKEN"`

Tokens are **per person**, not per team. Requests are attributed to whoever owns the token, so
sharing one makes every task look like it came from that person. Get your own.

## IDs

Workspace, space, list, member and doc IDs live in **`clickup-ids.local.md`**, which is gitignored.
Copy `clickup-ids.example.md` to `clickup-ids.local.md` and fill in the real values from ClickUp.

They are kept out of git because this repository is public — the IDs alone are not secret enough to
be dangerous, but together they map the internal engineering structure and the team roster, and
none of that needs to be on the public internet to make the skill work.

## Statuses (Engineering Space)

`backlog` → `scoping` → `in design` → `in development` → `in review` → `testing` →
`ready for deployment` → `shipped`

Also: `cancelled`

## Priority

1=urgent, 2=high, 3=normal, 4=low

## Task Operations

### Create Task

```bash
curl -H "Authorization: $CLICKUP_TOKEN" \
     -H "Content-Type: application/json" \
     -X POST \
     -d '{"name":"NAME","markdown_description":"DESC","assignees":[USER_ID],"priority":3,"status":"backlog"}' \
     "https://api.clickup.com/api/v2/list/{LIST_ID}/task"
```

### Create Subtask

Same as task, add `"parent":"{PARENT_TASK_ID}"` to payload.

### Update Task

```bash
curl -H "Authorization: $CLICKUP_TOKEN" \
     -H "Content-Type: application/json" \
     -X PUT \
     -d '{"status":"in development"}' \
     "https://api.clickup.com/api/v2/task/{TASK_ID}"
```

Fields: `name`, `description`, `markdown_description`, `status`, `priority`, `assignees`

### Get Task

```bash
curl -H "Authorization: $CLICKUP_TOKEN" \
     "https://api.clickup.com/api/v2/task/{TASK_ID}?include_subtasks=true"
```

### Get Tasks from List

```bash
curl -H "Authorization: $CLICKUP_TOKEN" \
     "https://api.clickup.com/api/v2/list/{LIST_ID}/task?include_subtasks=true"
```

Filters: `statuses[]=value`, `assignees[]=id`, `priorities[]=num`

### Delete Task

```bash
curl -H "Authorization: $CLICKUP_TOKEN" -X DELETE \
     "https://api.clickup.com/api/v2/task/{TASK_ID}"
```

### Add Comment

```bash
curl -H "Authorization: $CLICKUP_TOKEN" \
     -H "Content-Type: application/json" \
     -X POST \
     -d '{"comment_text":"TEXT"}' \
     "https://api.clickup.com/api/v2/task/{TASK_ID}/comment"
```

## Document Operations

`{WORKSPACE_ID}` below comes from `clickup-ids.local.md`.

### Get Doc Pages

```bash
curl -H "Authorization: $CLICKUP_TOKEN" \
     "https://api.clickup.com/api/v3/workspaces/{WORKSPACE_ID}/docs/{DOC_ID}/pages"
```

### Update Page

```bash
curl -H "Authorization: $CLICKUP_TOKEN" \
     -H "Content-Type: application/json" \
     -X PUT \
     -d '{"content":"MARKDOWN","content_edit_mode":"replace","content_format":"text/md"}' \
     "https://api.clickup.com/api/v3/workspaces/{WORKSPACE_ID}/docs/{DOC_ID}/pages/{PAGE_ID}"
```

**Page content is markdown-only and lossy — it cannot author rich blocks:**
- A write rebuilds the whole page from markdown. Modes: `replace` rewrites everything;
  `append`/`prepend` only add at the page start/end — there is no cell/section-level edit, so
  changing one table cell means re-sending the whole page.
- Task **card embeds** (`[](https://app.clickup.com/t/ID)`, empty text) and **mention chips**
  (`[@x](#user_mention#ID)`, `[task](#task_mention#ID)`) exist only as UI-authored blocks. Writing
  their markdown does NOT recreate them: empty-text embeds are stripped, and a `#..._mention#` link
  round-trips to a dead `http://#..._mention#` plain link (no chip, no server-side name resolution
  — wrong display text is kept verbatim).
- So a write to a page that holds cards or chips DESTROYS them across every cell (cards vanish,
  chips become dead links), not just the cell you meant to edit. For a doc with rich blocks, don't
  write — hand the user task URLs to paste in the UI (a pasted task URL becomes a card; `@` + task
  name becomes a chip). Plain text, plain `[text](url)` links, and `![](img)` images do round-trip
  safely.

### Create Page

```bash
curl -H "Authorization: $CLICKUP_TOKEN" \
     -H "Content-Type: application/json" \
     -X POST \
     -d '{"name":"PAGE NAME","content":"MARKDOWN","content_format":"text/md"}' \
     "https://api.clickup.com/api/v3/workspaces/{WORKSPACE_ID}/docs/{DOC_ID}/pages"
```

Returns `201` with the new page `id`. Add `"parent_page_id":"{ID}"` to nest under another page.

### Remove a Page

No delete endpoint — `DELETE .../pages/{PAGE_ID}` returns `405`. To hide a page, PUT
`{"archived": true}` on it (`200`; drops out of the default page listing).

## Notes

- Rate limit: 100 req/min
- Max 100 tasks per page response
- Subtask limit: 1000 per parent

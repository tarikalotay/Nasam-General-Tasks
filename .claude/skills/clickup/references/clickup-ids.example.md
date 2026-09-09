# ClickUp IDs — template

Copy this file to `clickup-ids.local.md` (gitignored) and replace the placeholders with the real
values from ClickUp. The skill reads the `.local.md` copy; this file is only the shape.

Where to find each value: open the resource in ClickUp and read the ID out of the URL, or call
`GET https://api.clickup.com/api/v2/team` for the workspace and
`GET https://api.clickup.com/api/v2/space/{SPACE_ID}/list` for the lists.

## Workspace & Space

| Resource         | ID                |
| ---------------- | ----------------- |
| Workspace        | `<workspace-id>`  |
| Engineering Space| `<space-id>`      |

## Lists (by domain)

One list per domain — route a task by what it touches, not by who is writing it.

| List                  | ID          |
| --------------------- | ----------- |
| Dashboard             | `<list-id>` |
| Integrations          | `<list-id>` |
| Fulfillment           | `<list-id>` |
| Products              | `<list-id>` |
| Inventory             | `<list-id>` |
| Cloud & Operations    | `<list-id>` |
| Pricing               | `<list-id>` |
| Sellers, Orgs & Users | `<list-id>` |
| Code Base             | `<list-id>` |
| Vendor                | `<list-id>` |
| Auth                  | `<list-id>` |
| Invoicing             | `<list-id>` |
| Docs                  | `<list-id>` |
| HR                    | `<list-id>` |

## Team Members

Needed for the `assignees` field. One row per person.

| Name              | ID            |
| ----------------- | ------------- |
| `<name>`          | `<member-id>` |

## Known Documents

| Document                       | ID         |
| ------------------------------ | ---------- |
| WBR (Weekly Business Review)   | `<doc-id>` |
| Design Documents               | `<doc-id>` |
| PRDs                           | `<doc-id>` |
| Fulfillment Design             | `<doc-id>` |
| Inventory Design               | `<doc-id>` |
| Product Overview               | `<doc-id>` |

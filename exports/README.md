# Brands Leads exports

## `Nasam_Brands_Leads_High-Urgent_<date>.xlsx`

Every lead in the ClickUp **Brands Leads** list (Nasam Growth) whose status has moved
past `lead` and whose priority is **High** or **Urgent**.

Regenerate with:

```bash
export CLICKUP_API=pk_...                       # ClickUp personal API token
python3 scripts/export_brands_leads.py \
        --websites exports/lead_websites_<date>.json \
        --out exports/
```

`--exclude-status` and `--priority` change the filter; run with `-h` for the details.

## `lead_websites_<date>.json`

The website found for each lead that had an empty `URL` field on its ClickUp task,
with where it came from:

| source | meaning |
|---|---|
| `ClickUp activity` | a rep had already written the site in a task comment |
| `Contact email domain (activity)` | taken from a contact's work email domain in the comments |
| `Domain check` | the brand slug resolved to a live Saudi store (title/language verified) |
| `Web search` | found by search and checked by hand |

`confidence: medium` means the match is plausible but worth a human glance before
it is used for outreach.

Write these back into ClickUp (only fills empty `URL` fields, never overwrites):

```bash
python3 scripts/fill_lead_websites.py exports/lead_websites_<date>.json --dry-run
python3 scripts/fill_lead_websites.py exports/lead_websites_<date>.json
```

#!/usr/bin/env python3
"""Export the ClickUp "Brands Leads" list to a formatted .xlsx.

Default filter (what sales asked for): every lead whose status is NOT "lead"
and whose priority is High or Urgent.

    export CLICKUP_API=pk_...            # personal API token
    python3 scripts/export_brands_leads.py --out exports/

Options:
    --exclude-status lead                statuses to drop (repeatable)
    --priority high --priority urgent    priorities to keep (repeatable; omit for all)
    --list-id 901809161015               ClickUp list to export

Requires: openpyxl.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

BRANDS_LEADS_LIST = "901809161015"          # Nasam Growth › Brands Leads
RIYADH = timezone(timedelta(hours=3))
STATUS_ORDER = ["lead", "opportunity", "propose", "meeting", "approved",
                "postpone", "rejected", "churned", "complete"]
PRIORITY_ORDER = ["urgent", "high", "normal", "low"]
DATA_SHEET = "High & Urgent Leads"
ARIAL = "Arial"

HEADERS = ["#", "Lead / Brand", "Status", "Priority", "Assignee(s)", "Lead Source",
           "Contact Person", "Phone", "City", "Website", "Own site (candidate)",
           "Website source", "Confidence", "Started Date", "Closing Date", "Due Date",
           "Created", "Last Updated", "Last Update (note)", "ClickUp Link", "Task ID"]
WIDTHS = [5, 34, 13, 10, 20, 20, 18, 16, 14, 34, 30, 22, 11, 12, 12, 12, 12, 13, 46, 30, 12]
DATE_COLS = {14, 15, 16, 17, 18}
WEB_COL, OWN_COL, LINK_COL = 10, 11, 20


def fetch_tasks(list_id, token):
    """Page through the ClickUp list endpoint (100 tasks/page) with backoff."""
    tasks, page = [], 0
    while True:
        url = (f"https://api.clickup.com/api/v2/list/{list_id}/task"
               f"?page={page}&subtasks=true&include_closed=true&order_by=created&reverse=true")
        req = urllib.request.Request(url, headers={"Authorization": token})
        for attempt in range(5):
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    data = json.loads(r.read().decode())
                break
            except Exception:
                if attempt == 4:
                    raise
                time.sleep(2 ** attempt)
        batch = data.get("tasks", [])
        tasks.extend(batch)
        print(f"  page {page}: {len(batch)} (total {len(tasks)})", file=sys.stderr)
        if data.get("last_page") or not batch:
            return tasks
        page += 1


def ms_to_date(v):
    return datetime.fromtimestamp(int(v) / 1000, RIYADH).replace(tzinfo=None) if v else None


def custom_field(task, name):
    for f in task.get("custom_fields", []):
        if f["name"] == name:
            return f.get("value")
    return None


def from_description(task, key):
    """Leads imported from the Mahally/Salla sheets carry `Key: value` lines."""
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", task.get("description") or "", re.M)
    return m.group(1).strip() if m else None


def build_workbook(tasks, rows, priorities, websites=None):
    wb = Workbook()
    ws = wb.active
    ws.title = DATA_SHEET

    head_fill = PatternFill("solid", fgColor="1F3864")
    head_font = Font(name=ARIAL, size=10, bold=True, color="FFFFFF")
    body_font = Font(name=ARIAL, size=10)
    link_font = Font(name=ARIAL, size=10, color="0563C1", underline="single")
    thin = Side(style="thin", color="D9D9D9")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    prio_fill = {"urgent": PatternFill("solid", fgColor="F8CBAD"),
                 "high": PatternFill("solid", fgColor="FCE4D6")}
    band = PatternFill("solid", fgColor="F7F9FC")

    for c, h in enumerate(HEADERS, 1):
        cell = ws.cell(row=1, column=c, value=h)
        cell.font, cell.fill, cell.border = head_font, head_fill, border
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(c)].width = WIDTHS[c - 1]
    ws.row_dimensions[1].height = 28

    websites = websites or {}
    for i, t in enumerate(rows, 1):
        source = custom_field(t, "Lead Sorce") or []
        found = websites.get(t["id"], {})
        values = [
            i,
            t["name"].strip(),
            t["status"]["status"],
            (t.get("priority") or {}).get("priority", ""),
            ", ".join(a["username"].strip() for a in t.get("assignees", [])),
            ", ".join(u["username"].strip() for u in source) if isinstance(source, list) else "",
            custom_field(t, "Contact Person") or "",
            from_description(t, "Phone") or "",
            from_description(t, "City") or "",
            custom_field(t, "URL") or found.get("website", ""),
            found.get("own_site", ""),
            found.get("source", ""),
            found.get("confidence", ""),
            ms_to_date(custom_field(t, "Started Date")),
            ms_to_date(custom_field(t, "Closing Date")),
            ms_to_date(t.get("due_date")),
            ms_to_date(t.get("date_created")),
            ms_to_date(t.get("date_updated")),
            " ".join((custom_field(t, "Last Update") or "").split()),
            t["url"],
            t["id"],
        ]
        r = i + 1
        for c, v in enumerate(values, 1):
            cell = ws.cell(row=r, column=c, value=v)
            cell.font, cell.border = body_font, border
            cell.alignment = Alignment(
                vertical="top",
                horizontal="center" if c in (1, 3, 4, 13) or c in DATE_COLS else "left")
            if c in DATE_COLS:
                cell.number_format = "yyyy-mm-dd"
            if i % 2 == 0 and c != 4:
                cell.fill = band
        if values[3] in prio_fill:
            ws.cell(row=r, column=4).fill = prio_fill[values[3]]
        for col in (WEB_COL, OWN_COL, LINK_COL):
            url = values[col - 1]
            if url:
                link = ws.cell(row=r, column=col)
                link.hyperlink = url
                link.font = link_font

    last = len(rows) + 1
    ws.auto_filter.ref = f"A1:{get_column_letter(len(HEADERS))}{last}"
    ws.freeze_panes = "C2"
    add_summary(wb, tasks, rows, priorities, last)
    return wb


def add_summary(wb, tasks, rows, priorities, last):
    """Counts are COUNTIFS formulas so they follow edits to the data sheet."""
    sm = wb.create_sheet("Summary")
    sm.column_dimensions["A"].width = 26
    for col in "BCD":
        sm.column_dimensions[col].width = 13
    sm.column_dimensions["E"].width = 70

    head_fill = PatternFill("solid", fgColor="1F3864")
    head_font = Font(name=ARIAL, size=10, bold=True, color="FFFFFF")
    body_font = Font(name=ARIAL, size=10)
    bold = Font(name=ARIAL, size=10, bold=True)
    note = Font(name=ARIAL, size=9, italic=True, color="595959")
    thin = Side(style="thin", color="D9D9D9")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    sm["A1"] = "Nasam — Brands Leads export"
    sm["A1"].font = Font(name=ARIAL, size=13, bold=True, color="1F3864")
    meta = [
        ("Source", "ClickUp › Nasam Growth › Brands Leads (list 901809161015)"),
        ("Filter", 'Status is NOT "lead"  AND  Priority is '
                   + " or ".join(p.title() for p in priorities)),
        ("Leads in list", len(tasks)),
        ("Leads exported", f"='{DATA_SHEET}'!A{last}"),
        ("Pulled", datetime.now(RIYADH).strftime("%Y-%m-%d %H:%M (Riyadh)")),
    ]
    for r, (k, v) in enumerate(meta, 3):
        sm.cell(row=r, column=1, value=k).font = bold
        cell = sm.cell(row=r, column=2, value=v)
        cell.font = body_font
        cell.alignment = Alignment(horizontal="left")
    sm.merge_cells("B4:E4")

    sm["A9"] = "Breakdown — status × priority"
    sm["A9"].font = bold
    header = sm.cell(row=10, column=1, value="Status")
    header.font, header.fill, header.border = head_font, head_fill, border
    for j, p in enumerate(priorities + ["Total"], 2):
        cell = sm.cell(row=10, column=j, value=p.title())
        cell.font, cell.fill, cell.border = head_font, head_fill, border
        cell.alignment = Alignment(horizontal="center")

    present = [s for s in STATUS_ORDER if any(t["status"]["status"] == s for t in rows)]
    rng_s, rng_p = f"'{DATA_SHEET}'!$C$2:$C${last}", f"'{DATA_SHEET}'!$D$2:$D${last}"
    span = get_column_letter(1 + len(priorities))
    for i, s in enumerate(present):
        r = 11 + i
        cell = sm.cell(row=r, column=1, value=s)
        cell.font, cell.border = body_font, border
        for j in range(2, 2 + len(priorities)):
            c = sm.cell(row=r, column=j,
                        value=f'=COUNTIFS({rng_s},$A{r},{rng_p},{get_column_letter(j)}$10)')
            c.font, c.border = body_font, border
            c.alignment = Alignment(horizontal="center")
        tot = sm.cell(row=r, column=2 + len(priorities), value=f"=SUM(B{r}:{span}{r})")
        tot.font, tot.border = bold, border
        tot.alignment = Alignment(horizontal="center")

    trow = 11 + len(present)
    sm.cell(row=trow, column=1, value="Total").font = bold
    sm.cell(row=trow, column=1).border = border
    for j in range(2, 3 + len(priorities)):
        col = get_column_letter(j)
        cell = sm.cell(row=trow, column=j, value=f"=SUM({col}11:{col}{trow - 1})")
        cell.font, cell.border = bold, border
        cell.alignment = Alignment(horizontal="center")

    web = trow + 2
    sm.cell(row=web, column=1, value="Website coverage").font = bold
    rng_w = f"'{DATA_SHEET}'!$J$2:$J${last}"
    rng_own = f"'{DATA_SHEET}'!$K$2:$K${last}"
    rng_src = f"'{DATA_SHEET}'!$L$2:$L${last}"
    coverage = [("Leads with a website", f'=COUNTIF({rng_w},"?*")'),
                ("Leads with no website", f'=COUNTBLANK({rng_w})'),
                ("  already on the task",
                 f'=COUNTIFS({rng_w},"?*",{rng_src},"")'
                 f'+COUNTIF({rng_src},"Domain check (own site)")'),
                ("  from ClickUp activity", f'=COUNTIF({rng_src},"ClickUp activity")'),
                ("  from a contact email domain",
                 f'=COUNTIF({rng_src},"Contact email domain (activity)")'),
                ("  from a domain check", f'=COUNTIF({rng_src},"Domain check")'),
                ("  from a web search", f'=COUNTIF({rng_src},"Web search")'),
                ("Mahally listing with an own-site candidate",
                 f'=COUNTIF({rng_own},"?*")')]
    for offset, (k, formula) in enumerate(coverage):
        sm.cell(row=web + 1 + offset, column=1, value=k).font = body_font
        cell = sm.cell(row=web + 1 + offset, column=2, value=formula)
        cell.font, cell.border = body_font, border
        cell.alignment = Alignment(horizontal="center")

    n = web + len(coverage) + 3
    for offset, text in enumerate([
        f'Notes: counts are COUNTIFS formulas over the "{DATA_SHEET}" sheet, '
        "so they follow any row you delete or re-filter.",
        "Phone and City are parsed from the ClickUp task description and are blank "
        "where the task carries no description.",
        "Dates are shown in Riyadh time (UTC+3). Blank means the field is empty in ClickUp.",
        'Website source is blank when the URL was already on the ClickUp task. "Domain check" '
        "and \"Web search\" rows were found by this script and written back to ClickUp; "
        "confidence medium means the match is plausible but worth a human glance.",
        '"Own site (candidate)" is for leads whose ClickUp URL is only a Mahally directory '
        "listing: the brand's own store, found by domain check and NOT written to ClickUp.",
    ]):
        sm.cell(row=n + offset, column=1, value=text).font = note


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list-id", default=BRANDS_LEADS_LIST)
    ap.add_argument("--exclude-status", action="append", default=None,
                    help='default: lead')
    ap.add_argument("--priority", action="append", default=None,
                    help="priorities to keep; default: urgent, high")
    ap.add_argument("--websites", help="JSON map task_id -> {website, source, confidence} "
                                       "to fill in for leads with no URL on the task")
    ap.add_argument("--out", default=".", help="output directory or file path")
    args = ap.parse_args()

    token = os.environ.get("CLICKUP_API")
    if not token:
        sys.exit("CLICKUP_API is not set (ClickUp personal API token).")

    excluded = set(args.exclude_status if args.exclude_status is not None else ["lead"])
    priorities = args.priority if args.priority is not None else ["urgent", "high"]

    print(f"Fetching list {args.list_id} …", file=sys.stderr)
    tasks = fetch_tasks(args.list_id, token)
    rows = [t for t in tasks
            if t["status"]["status"] not in excluded
            and (t.get("priority") or {}).get("priority") in priorities]
    rows.sort(key=lambda t: (priorities.index(t["priority"]["priority"]),
                             STATUS_ORDER.index(t["status"]["status"]),
                             t["name"].strip().lower()))

    out = args.out
    if os.path.isdir(out) or out.endswith("/"):
        os.makedirs(out, exist_ok=True)
        out = os.path.join(
            out, f"Nasam_Brands_Leads_High-Urgent_{datetime.now(RIYADH):%Y-%m-%d}.xlsx")
    websites = json.load(open(args.websites)) if args.websites else {}
    build_workbook(tasks, rows, priorities, websites).save(out)
    print(f"{len(rows)} of {len(tasks)} leads → {out}")


if __name__ == "__main__":
    main()

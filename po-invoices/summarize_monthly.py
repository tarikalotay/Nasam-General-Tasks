#!/usr/bin/env python3
"""Aggregate pos_invoices_sorted_by_brand.csv into a per-month, per-brand summary.

Grouping is by PO order month. Amounts are summed as exact decimals; commission
is the sum of the per-PO commissions already rounded in the detail file.
"""

import csv
from collections import defaultdict
from decimal import Decimal

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def fmt(d: Decimal) -> str:
    return format(d.normalize(), "f")


def main() -> None:
    agg = defaultdict(lambda: {"pos": 0, "units": 0, "req": Decimal(0),
                               "rec": Decimal(0), "com": Decimal(0)})
    with open("pos_invoices_sorted_by_brand.csv", newline="") as f:
        for r in csv.DictReader(f):
            m, _, y = r["order_date"].split("/")
            key = ((int(y), int(m)), r["brand"])
            a = agg[key]
            a["pos"] += 1
            a["units"] += int(r["units"])
            a["req"] += Decimal(r["requested_sar"])
            a["rec"] += Decimal(r["received_sar"])
            a["com"] += Decimal(r["commission_sar"])

    total_rows = sum(a["pos"] for a in agg.values())
    assert total_rows == 199, f"expected 199 rows aggregated, got {total_rows}"

    out = "pos_invoices_monthly_summary.csv"
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["month", "brand", "pos", "units",
                    "requested_sar", "received_sar", "commission_sar"])
        for ((y, m), brand) in sorted(agg):
            a = agg[((y, m), brand)]
            w.writerow([f"{y}-{m:02d}", brand, a["pos"], a["units"],
                        fmt(a["req"]), fmt(a["rec"]), fmt(a["com"])])

    print(f"OK: wrote {out} with {len(agg)} rows")
    # Pivot printout: commission (and received) per brand per month.
    brands = ["Marah", "SONDOS", "Wadi Halfa"]
    months = sorted({k[0] for k in agg})
    print(f"\n{'Month':<9}" + "".join(f"{b + ' com':>13}" for b in brands) + f"{'Total com':>13}{'Total rec':>13}")
    gtot = {"com": Decimal(0), "rec": Decimal(0)}
    for ym in months:
        coms = [agg.get((ym, b), {"com": Decimal(0)})["com"] for b in brands]
        rec = sum(agg.get((ym, b), {"rec": Decimal(0)})["rec"] for b in brands)
        gtot["com"] += sum(coms)
        gtot["rec"] += rec
        label = f"{MONTHS[ym[1] - 1]} {ym[0]}"
        print(f"{label:<9}" + "".join(f"{fmt(c):>13}" for c in coms) + f"{fmt(sum(coms)):>13}{fmt(rec):>13}")
    print(f"{'TOTAL':<9}" + " " * 39 + f"{fmt(gtot['com']):>13}{fmt(gtot['rec']):>13}")


if __name__ == "__main__":
    main()

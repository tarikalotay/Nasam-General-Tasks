#!/usr/bin/env python3
"""Generate PO listing sorted by brand + per-PO commission invoices.

Source data: closed purchase orders (Jul 19 - Aug 6, 2026) from the Nasam PO
screen. PO headers (numbers, brands, channels, dates, FCs) verified against
the Nasam purchase_orders view; requested/received amounts taken from the PO
screen. All amounts are SAR.

Commission rates (per client agreement): Wadi Halfa 4%, SONDOS 6%.
Marah has no commission rate on file, so no Marah invoices are generated.
Commission is charged on the received (fulfilled) value, exclusive of VAT.
"""

import csv
import os
from decimal import Decimal, ROUND_HALF_UP

INVOICE_DATE = "2026-08-17"

COMMISSION_RATES = {
    "Wadi Halfa": Decimal("0.04"),
    "SONDOS": Decimal("0.06"),
}

# (brand, po_number, channel, order_date, delivered_date, fc, units,
#  requested_sar, received_sar, accept_pct, fulfill_pct, outcome)
PO_ROWS = [
    ("Marah", "13WKUXGQ", "Amazon Retail", "2026-08-06", "2026-08-12", "JED4", 8, "364.80", "364.80", 100, 100, "Delivered"),
    ("Marah", "17WV7XMX", "Amazon Retail", "2026-08-06", "2026-08-11", "RDF1", 10, "456.00", "456.00", 100, 100, "Delivered"),
    ("Marah", "53LUQGQJ", "Amazon Retail", "2026-08-06", "2026-08-12", "JED4", 10, "110.00", "110.00", 100, 100, "Delivered"),
    ("Marah", "5249UCBK", "Amazon Retail", "2026-07-26", "2026-07-28", "RUH8", 45, "247.50", "247.50", 100, 100, "Delivered"),
    ("Marah", "64TUIPCQ", "Amazon Retail", "2026-07-26", "2026-08-09", "JED4", 70, "385.00", "385.00", 100, 100, "Delivered"),
    ("Marah", "7CS7ZUYR", "Amazon Retail", "2026-07-19", "2026-07-29", "JED4", 222, "2310.00", "2310.00", 100, 100, "Delivered"),
    ("Marah", "6Z9UWMBO", "Amazon Retail", "2026-07-19", "2026-07-29", "RUH8", 95, "577.50", "577.50", 100, 100, "Delivered"),
    ("Marah", "65T5PXVI", "Amazon Retail", "2026-07-19", "2026-07-28", "RDF1", 10, "330.00", "330.00", 100, 100, "Delivered"),
    ("SONDOS", "1F6WGJRN", "Amazon Retail", "2026-08-02", "2026-08-04", "RDF1", 4, "244.80", "244.80", 100, 100, "Delivered"),
    ("SONDOS", "2VS58KHE", "Amazon Retail", "2026-07-26", "2026-07-28", "RDF1", 2, "122.40", "122.40", 100, 100, "Delivered"),
    ("SONDOS", "5249UCBK", "Amazon Retail", "2026-07-26", "2026-07-28", "RUH8", 2, "23.50", "23.50", 100, 100, "Delivered"),
    ("SONDOS", "64TUIPCQ", "Amazon Retail", "2026-07-26", "2026-08-09", "JED4", 18, "135.00", "270.00", 100, 200, "Delivered"),
    ("SONDOS", "6Z9UWMBO", "Amazon Retail", "2026-07-19", "2026-07-29", "RUH8", 6, "45.00", "45.00", 100, 100, "Delivered"),
    ("SONDOS", "7CS7ZUYR", "Amazon Retail", "2026-07-19", "2026-07-29", "JED4", 26, "256.80", "128.40", 100, 50, "Shortage"),
    ("Wadi Halfa", "PO2600651634", "Ninja Retail", "2026-08-03", "2026-08-13", "RUH8", 238, "2008.60", "2008.60", 100, 100, "Delivered"),
    ("Wadi Halfa", "PO2600651819", "Ninja Retail", "2026-08-03", "2026-08-13", "JED4", 140, "1215.17", "1215.17", 100, 100, "Delivered"),
    ("Wadi Halfa", "PO2600629370", "Ninja Retail", "2026-07-27", "2026-08-13", "RUH8", 116, "780.95", "240.91", 100, 31, "Shortage"),
    ("Wadi Halfa", "PO2600629540", "Ninja Retail", "2026-07-27", "2026-08-13", "JED4", 62, "396.78", "68.06", 100, 17, "Shortage"),
    ("Wadi Halfa", "6WAWK77S", "Amazon Retail", "2026-07-26", "2026-08-11", "RUH8", 32, "674.24", "948.15", 100, 141, "Delivered"),
    ("Wadi Halfa", "PO2600607394", "Ninja Retail", "2026-07-20", "2026-08-13", "RUH8", 240, "2196.96", "1633.44", 100, 74, "Shortage"),
    ("Wadi Halfa", "PO2600607555", "Ninja Retail", "2026-07-20", "2026-08-13", "JED4", 130, "1190.02", "884.78", 100, 74, "Shortage"),
    ("Wadi Halfa", "5EOBBQRQ", "Amazon Retail", "2026-07-19", "2026-07-26", "RUH8", 24, "218.64", "0.00", 0, 0, "Rejected"),
    ("Wadi Halfa", "8ZI1SK8E", "Amazon Retail", "2026-07-19", "2026-07-26", "JED4", 49, "446.39", "0.00", 0, 0, "Rejected"),
]

BRAND_CODES = {"Wadi Halfa": "WH", "SONDOS": "SND", "Marah": "MRH"}
BRAND_DIRS = {"Wadi Halfa": "wadi_halfa", "SONDOS": "sondos"}


def money(value):
    return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def commission_for(brand, received):
    rate = COMMISSION_RATES.get(brand)
    if rate is None:
        return None
    return money(Decimal(received) * rate)


def write_sorted_pos(root):
    rows = sorted(PO_ROWS, key=lambda r: (r[0], r[3], r[1]))
    path = os.path.join(root, "pos_sorted_by_brand.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "brand", "po_number", "channel", "order_date", "delivered_date",
            "fulfillment_center", "units", "requested_sar", "received_sar",
            "accept_pct", "fulfill_pct", "outcome", "commission_rate_pct",
            "commission_sar",
        ])
        for brand, po, channel, odate, ddate, fc, units, req, rec, acc, ful, outcome in rows:
            rate = COMMISSION_RATES.get(brand)
            comm = commission_for(brand, rec)
            w.writerow([
                brand, po, channel, odate, ddate, fc, units,
                money(req), money(rec), acc, ful, outcome,
                f"{rate * 100:.0f}" if rate is not None else "N/A",
                comm if comm is not None else "N/A",
            ])
    return path


def write_invoice(root, number, brand, po_row):
    brand_, po, channel, odate, ddate, fc, units, req, rec, acc, ful, outcome = po_row
    rate = COMMISSION_RATES[brand]
    received = money(rec)
    comm = commission_for(brand, rec)
    directory = os.path.join(root, "invoices", BRAND_DIRS[brand])
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, f"{number}_{po}.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["field", "value"])
        w.writerow(["invoice_number", number])
        w.writerow(["invoice_date", INVOICE_DATE])
        w.writerow(["bill_to", brand])
        w.writerow(["po_number", po])
        w.writerow(["channel", channel])
        w.writerow(["po_date", odate])
        w.writerow(["delivered_date", ddate])
        w.writerow(["fulfillment_center", fc])
        w.writerow(["po_outcome", outcome])
        w.writerow([])
        w.writerow(["description", "units", "requested_sar", "received_sar", "commission_rate_pct", "amount_sar"])
        w.writerow([
            f"Commission on PO {po} ({outcome.lower()} value)",
            units, money(req), received, f"{rate * 100:.0f}", comm,
        ])
        w.writerow([])
        w.writerow(["total_due_sar", comm])
        w.writerow(["currency", "SAR"])
        w.writerow(["note", "Commission charged on received (fulfilled) value. Amounts exclusive of VAT."])
        if outcome == "Rejected":
            w.writerow(["remark", "PO rejected - no units received, no commission due."])
    return number, brand, po, received, rate, comm, path


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    sorted_path = write_sorted_pos(root)
    print(f"wrote {sorted_path}")

    invoice_records = []
    for brand in ("Wadi Halfa", "SONDOS"):
        brand_rows = sorted(
            (r for r in PO_ROWS if r[0] == brand),
            key=lambda r: (r[3], r[1]),
        )
        for i, row in enumerate(brand_rows, start=1):
            number = f"INV-2026-{BRAND_CODES[brand]}-{i:03d}"
            invoice_records.append(write_invoice(root, number, brand, row))

    summary_path = os.path.join(root, "invoices", "invoices_summary.csv")
    with open(summary_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "invoice_number", "invoice_date", "client", "po_number",
            "received_sar", "commission_rate_pct", "commission_sar", "file",
        ])
        totals = {}
        for number, brand, po, received, rate, comm, path in invoice_records:
            w.writerow([
                number, INVOICE_DATE, brand, po, received,
                f"{rate * 100:.0f}", comm, os.path.relpath(path, root),
            ])
            totals[brand] = totals.get(brand, Decimal("0")) + comm
        w.writerow([])
        for brand, total in totals.items():
            w.writerow([f"TOTAL {brand}", "", "", "", "", "", money(total), ""])
    print(f"wrote {summary_path} ({len(invoice_records)} invoices)")
    for brand, total in totals.items():
        print(f"  {brand}: SAR {money(total)}")


if __name__ == "__main__":
    main()

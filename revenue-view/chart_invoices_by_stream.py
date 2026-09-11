#!/usr/bin/env python3
"""Stacked columns: Nasam invoiced revenue by month, split by stream. Renders HTML -> PNG."""
import subprocess, os, html

SP = os.path.dirname(os.path.abspath(__file__))
DATA = [  # month, AM fees, commission, setup, discounts (negative)
    ("May25", 0, 1205.29, 0, 0),
    ("Jun25", 0, 1153.53, 0, 0),
    ("Jul25", 0, 649.79, 500.00, 0),
    ("Aug25", 1500.00, 1941.66, 0, 0),
    ("Sep25", 1875.00, 3433.48, 0, 0),
    ("Oct25", 5752.68, 4223.02, 3000.00, 0),
    ("Nov25", 15550.00, 6090.44, 9750.00, 0),
    ("Dec25", 16500.00, 5447.73, 0, 0),
    ("Jan26", 16500.00, 9363.00, 2400.00, -2050.20),
    ("Feb26", 13119.04, 8898.63, 0, -2500.00),
    ("Mar26", 14774.19, 7351.34, 5000.00, 0),
    ("Apr26", 16000.00, 5685.72, 8800.50, -3000.00),
    ("May26", 14999.95, 6956.48, 0, 0),
    ("Jun26", 7749.99, 4493.46, 4000.00, 0),
    ("Jul26", 4600.00, 2698.95, 0, 0),
    ("Aug26", 4000.00, 8694.60, 0, 0),
]
SERIES = [("AM fees", "#2a78d6"), ("Commission", "#eb6834"), ("Setup", "#1baf7a")]
DISC = ("Discounts", "#898781")
SURFACE, INK, INK2, MUTED, GRID, BASE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"

W, H = 1180, 700
ML, MR, MT, MB = 76, 26, 122, 96
PW, PH = W - ML - MR, H - MT - MB
YMAX, YMIN = 32000, -4000
BAR, GAP, RAD = 24, 2, 4
band = PW / len(DATA)
y = lambda v: MT + (YMAX - v) / (YMAX - YMIN) * PH
zero = y(0)
s = []
a = s.append

a(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
  f'font-family="system-ui,-apple-system,Segoe UI,sans-serif">')
a(f'<rect width="{W}" height="{H}" fill="{SURFACE}"/>')
a(f'<text x="{ML}" y="46" font-size="21" font-weight="650" fill="{INK}">Nasam invoiced revenue by month</text>')
a(f'<text x="{ML}" y="70" font-size="13" fill="{INK2}">Every issued invoice, May 2025 to August 2026. SAR, excluding VAT.</text>')

# legend
lx = ML
for name, col in SERIES + [DISC]:
    a(f'<rect x="{lx}" y="88" width="10" height="10" rx="2" fill="{col}"/>')
    label = "Discounts (deducted)" if name == "Discounts" else name
    a(f'<text x="{lx+16}" y="97" font-size="12.5" fill="{INK2}">{label}</text>')
    lx += 16 + len(label) * 7.1 + 22

# gridlines + y ticks
for t in range(0, YMAX + 1, 8000):
    yy = y(t)
    a(f'<line x1="{ML}" y1="{yy:.1f}" x2="{ML+PW}" y2="{yy:.1f}" stroke="{GRID if t else BASE}" stroke-width="1"/>')
    a(f'<text x="{ML-12}" y="{yy+4:.1f}" font-size="11.5" fill="{MUTED}" text-anchor="end" '
      f'style="font-variant-numeric:tabular-nums">{t:,}</text>')

for i, (mon, *vals) in enumerate(DATA):
    x = ML + i * band + (band - BAR) / 2
    pos = vals[:3]
    disc = vals[3]
    total = sum(pos) + disc
    # stacked positive segments, bottom-up, 2px surface gap between them
    cursor = 0.0
    top_idx = max((j for j, v in enumerate(pos) if v > 0), default=None)
    for j, v in enumerate(pos):
        if v <= 0:
            continue
        y0, y1 = y(cursor + v), y(cursor)
        h = max(y1 - y0 - (GAP if cursor > 0 else 0), 1.2)
        r = RAD if j == top_idx else 0
        a(f'<path d="M{x} {y0+r} a{r} {r} 0 0 1 {r} {-r} h{BAR-2*r} a{r} {r} 0 0 1 {r} {r} '
          f'v{h-r:.2f} h{-BAR} Z" fill="{SERIES[j][1]}"/>' if r else
          f'<rect x="{x}" y="{y0:.2f}" width="{BAR}" height="{h:.2f}" fill="{SERIES[j][1]}"/>')
        cursor += v
    if disc < 0:  # deduction below the baseline
        h = y(disc) - zero - GAP
        a(f'<path d="M{x} {zero+GAP:.2f} h{BAR} v{h-RAD:.2f} a{RAD} {RAD} 0 0 1 {-RAD} {RAD} '
          f'h{-(BAR-2*RAD)} a{RAD} {RAD} 0 0 1 {-RAD} {-RAD} Z" fill="{DISC[1]}"/>')
    # net total on the cap
    a(f'<text x="{x+BAR/2:.1f}" y="{y(cursor)-9:.1f}" font-size="11.5" fill="{INK2}" '
      f'text-anchor="middle" style="font-variant-numeric:tabular-nums">{total:,.0f}</text>')
    a(f'<text x="{x+BAR/2:.1f}" y="{MT+PH+22:.1f}" font-size="12" fill="{MUTED}" '
      f'text-anchor="middle">{mon}</text>')

# callout on the shape that matters
a(f'<text x="140" y="248" font-size="12.5" fill="{INK2}">AM fees held near 16,500 a month, then</text>')
a(f'<text x="140" y="266" font-size="12.5" fill="{INK2}">fell away from June as clients churned.</text>')
a(f'<text x="140" y="284" font-size="12.5" fill="{INK2}">Nothing has replaced them.</text>')

a(f'<text x="{ML}" y="{H-46}" font-size="11.5" fill="{MUTED}">AM fees 132,921 · commission 78,287 · setup 33,451 · discounts −7,550 · total 237,108 across 157 invoices</text>')
a(f'<text x="{ML}" y="{H-28}" font-size="11.5" fill="{MUTED}">Excludes drafts and pass-throughs rebilled at cost: Cloud Shelf recharges and 16,534 of marketing for Sep 2025, which carried no management fee. Nothing issued yet in Sep 2026.</text>')
a('</svg>')

svg = "\n".join(s)
open(f"{SP}/chart.html", "w").write(
    f'<!doctype html><meta charset="utf-8"><body style="margin:0;background:{SURFACE}">{svg}</body>')
open(f"{SP}/invoices_by_stream.svg", "w").write(svg)
png = f"{SP}/nasam_invoices_by_stream.png"
subprocess.run(["/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "--headless", "--no-sandbox",
                "--hide-scrollbars", "--force-device-scale-factor=2",
                f"--window-size={W},{H+140}", f"--screenshot={png}", f"{SP}/chart.html"],
               check=True, capture_output=True)   # taller window: headless clips the last ~90px
from PIL import Image
im = Image.open(png)
im.crop((0, 0, W * 2, H * 2)).save(png)           # crop back to the SVG box
print("PNG", png, os.path.getsize(png), "bytes")
print("totals check:", [round(sum(r[1:]), 2) for r in DATA])
print("grand total:", round(sum(sum(r[1:]) for r in DATA), 2))

# mapping.py — what the Nasam PLATFORM says about each organization: which channels carry
# commission, and the monthly fee. Nasam fixed this mapping in the platform in Sep 2026, so the
# platform — not the rate card — is the source of truth for "is this channel commissioned".
#
# Read from: تعديل المنظمة (Edit Organization) → per-channel toggle العمولة سارية (commission
# active) / بلا عمولة (no commission), plus الرسوم الشهرية (monthly fee).
# A channel switched to بلا عمولة still syncs its orders and still appears in the dashboards; only
# its commission is folded out of the invoice. So its GMV stays visible here and its commission is
# zero — that is a billing switch, not a deactivation.
#
# HOW TO REFRESH (weekly run): pull the per-organization channel flags and the monthly fee from the
# platform read layer and paste them into ORGS below, moving AS_OF. Keys are platform brand names.
# Nothing is inferred here: an organization absent from ORGS has NOT been read off the platform, and
# validate() reports it as unconfirmed rather than letting build.py's rate-card defaults pass as
# verified.
#
# FIRST AUTHORISED RUN — the mapping's own view is not identified yet. The two mcp_read views this
# repo already uses are `revenue` and `purchase_orders`; neither carries the commission flag or the
# monthly fee. So on the first run with the connector live, list what mcp_read exposes and find the
# organization/channel view before writing any query — do not guess a table name. What is needed,
# one row per organization and channel:
#     organization (brand) · channel · commission active (bool) · monthly fee on the organization
# Then fill ORGS and re-run build.py; the mapping check compares it against the billing by itself.
# Everything Sonbol below was read off the dialog by eye and should be re-read from the view on that
# first run, so the whole table comes from one source.
AS_OF = '2026-09-13'
SOURCE = 'Nasam platform — تعديل المنظمة (per-channel commission toggle + الرسوم الشهرية)'

ORGS = {
    # Sonbol: read off the dialog Tarik shared 13 Sep 2026. Salla is the SaaS-app channel and is
    # switched to بلا عمولة; the four marketplace channels are live for commission.
    'Sonbol': dict(seen='2026-09-13', fee=8000.0,
                   channels={'Amazon': True, 'Namshi': True, 'Noon': True, 'Trendyol': True,
                             'Salla': False}),
}


def commission_on(brand, channel):
    """True = العمولة سارية, False = بلا عمولة, None = not read off the platform yet."""
    o = ORGS.get(brand)
    return None if not o else o['channels'].get(channel)


def fee(brand):
    o = ORGS.get(brand)
    return None if not o else o.get('fee')


def confirmed():
    return set(ORGS)


def pairs():
    return [(b, c, on) for b, o in sorted(ORGS.items()) for c, on in sorted(o['channels'].items())]


def validate(known_pairs, gmv_month, comm_month, fee_month, months, saas_set, closed_month,
             shared_fee=frozenset()):
    """Compare the platform mapping against what the workbook actually shows.

    known_pairs  set of (brand, channel) the workbook has any figure for
    gmv_month    (brand, channel, month) -> sales
    comm_month   (brand, channel, month) -> commission billed
    fee_month    brand -> {month: monthly fee billed for the brand's client}
    saas_set     build.py's rate-card SAAS pairs, for conflict detection
    closed_month last fully closed month, e.g. '2026-08'
    shared_fee   brands whose client bills one fee across several brands, so the fee check on them
                 is a client-level comparison and is labelled as such

    Returns a list of (severity, brand, channel, finding) — severity 'x' needs a decision,
    'i' is informational.
    """
    out = []
    for b, c, on in pairs():
        g = gmv_month.get((b, c, closed_month), 0.0)
        cm = sum(comm_month.get((b, c, m), 0.0) for m in months)
        cmc = comm_month.get((b, c, closed_month), 0.0)
        if on:
            if (b, c) in saas_set:
                out.append(('x', b, c, 'platform says commission active, rate card treats it as SaaS at 0% — one of the two is stale'))
            if (b, c) not in known_pairs:
                out.append(('i', b, c, 'mapped and commission active on the platform, but no sales and no invoice yet'))
            elif g > 0.005 and abs(cmc) < 0.005:
                out.append(('x', b, c, f'commission active and {g:,.0f} of sales in {closed_month}, but no commission billed that month'))
        else:
            if (b, c) not in saas_set:
                out.append(('i', b, c, 'platform switched commission off — the rate card has no 0% line for it'))
            if abs(cm) > 0.005:
                out.append(('x', b, c, f'platform says بلا عمولة, yet {cm:,.2f} of commission is billed in the window'))
    for b, o in sorted(ORGS.items()):
        f = o.get('fee')
        if not f: continue
        billed = fee_month.get(b, {})
        got = billed.get(closed_month, 0.0)
        if abs(got) < 0.005:
            ever = sum(billed.values())
            out.append(('x', b, '—', f'platform monthly fee {f:,.0f} is not billed in {closed_month}'
                                    + (f' (billed {ever:,.2f} across the window)' if abs(ever) > 0.005 else ' — never billed in the window')
                                    + (' · fee is billed at client level across several brands' if b in shared_fee else '')))
        elif abs(got - f) > 0.005:
            out.append(('x', b, '—', f'platform monthly fee {f:,.0f}, billed {got:,.2f} in {closed_month}'
                                    + (' · fee is billed at client level across several brands' if b in shared_fee else '')))
    unconf = sorted({b for b, c in known_pairs} - confirmed())
    if unconf:
        out.append(('i', ', '.join(unconf), '—', 'not read off the platform yet — still on rate-card defaults'))
    return out

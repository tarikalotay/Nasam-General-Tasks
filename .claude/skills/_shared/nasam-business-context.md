# Nasam Business Context — canonical source

This file is the **single source of truth** for the product/user context that several Nasam
skills need to carry inline.

Account-level skills on claude.ai are uploaded as self-contained bundles: a skill cannot read a
sibling skill's files. So this context is **injected into** each consuming `SKILL.md` between
marker comments rather than linked. Edit it here, then run:

```bash
.claude/skills/scripts/sync-shared.sh      # rewrite the injected blocks
.claude/skills/scripts/check-skills.sh     # verify nothing drifted
```

Consumers and the region each one takes:

| Skill           | Region  |
| --------------- | ------- |
| `ux-discovery`  | `full`  |
| `ux-touch`      | `short` |

<!-- REGION:short -->
**Product:** Multi-channel growth platform for e-commerce brands. Helps run a brand across
marketplaces, track performance, and make data-driven decisions.

**What Nasam Is:** An account-management service — an agency that grows Saudi brands across
marketplaces (onboarding, content, pricing, issues, reporting), human service plus tech. Two
internal roles run it: **Account Managers (AMs)** handle day-to-day marketplace ops, **Growth
Consultants (GCs)** focus on strategy, channel internals, and performance advisory. The platform
is not only for Nasam staff — it also serves the client brands we manage, Salla App Store
subscribers running their own brand, and future custom-website subscribers.

**Design for the role in front of you; never assume the user is a Nasam employee.**

**Users:**

- **Account Managers (internal)** — Power users. ~7 brands each today, target 15+. Goals: grow
  brands, spot opportunities, celebrate wins, resolve issues. High data density is fine.
- **Growth Consultants (internal)** — Strategic advisors. Fewer brands, deeper engagement.
  Consume dashboards and trends more than they operate them.
- **Self-serve subscribers** — Run their own brand via subscription (Salla App Store today,
  custom sites later; any role on their side). Same operator job as an AM, for one brand, usually
  not a power user. Plain language, obvious next action.
- **Client / reporting viewer** — Employees or owners at a brand Nasam manages, checking in on
  how their brand is doing. ⚠️ **Open — what this role actually needs has not been researched.**
  Do not invent it; ask the requester, or scope it out.
<!-- /REGION:short -->

<!-- REGION:full -->
**Product:** Multi-channel growth platform for e-commerce brands. Helps run a brand across
marketplaces, track performance, and make data-driven decisions.

**What Nasam Is:** The business is an account-management service — an agency that grows Saudi
brands across marketplaces (onboarding, content, pricing, issues, reporting), human service plus
tech. Two internal roles run it: **Account Managers (AMs)** handle day-to-day marketplace ops;
**Growth Consultants (GCs)** focus on strategy, channel internals, and performance advisory. But
the platform they use isn't only for Nasam staff — its users also include the client brands we
manage (logging into their own brand), Salla App Store subscribers running their own brand (any
role on their side), and future custom-website subscribers. It's agency-shaped, so another agency
is a conceptual fit too. Design for the role in front of you; never assume the user is a Nasam
employee.

**What We Do:**

- Onboarding — Marketplace setup, docs, compliance
- Content optimization — Titles, descriptions, images, Arabic content
- Pricing management — Cross-channel pricing, campaign execution
- Issue resolution — Order failures, listing suspensions, penalties
- Performance reporting — Consolidated data, actionable insights
- Growth strategy — Channel expansion, competitive analysis, growth recommendations
- Vendor management (B2B) — PO tracking for Amazon Vendor/Noon Retail

**What We Don't Do (Scope Boundaries):**

- Fulfillment/logistics (FBA/FBN or brand handles)
- D2C storefront building (Zid/Salla territory)
- Customer service (marketplace or brand handles)

**Platform Vision:** Growth command center. The user sees what's working, what's broken, and what
to do next. Growth opportunities AND issues surfaced automatically as much as possible, while
understanding the tool limitations. One AM manages 15+ brands because the platform handles the
busy work; GCs get the data and narrative to advise brands strategically; and the same command
center serves a brand running itself, or a client checking in on how they're doing.

**Current Reality:** The agency runs ~3 AMs and GCs over ~22 brands on a tight budget — the path
to scale there is making each AM more productive via the platform, with GCs working off
consolidated views. The same platform is also used self-serve by Salla App Store subscribers, with
custom-website subscribers planned.

**Domain Concepts:** Sellers (brands we manage), Organizations (one company, multiple brands),
Sale Channels (Amazon, Noon, Trendyol) (includes D2C like Salla/Zid), Listings (product on a
specific channel), Orders, Inventory, GMV, Account Health.

**Settings:**

- Tool for running brands efficiently: Professional, utilitarian aesthetic (denser for power-user
  AMs/GCs, simpler and plainer for subscribers and client users)
- High-stakes: Decisions made here impact real businesses

---

## Product Principles

1. **Prefer UX over code simplification** — Auto-sync after connection (good) vs manual import
   (bad), even if code is more complex
2. **Automate, automate, automate** — Platform handles ops, AMs focus on strategy
3. **Be proactive, surface actions** — Don't just display data. Think: what can the user ACT on?
   Surface that, or even better, perform the action or provide a way to perform it. Buy box is
   losing — should we just scream that, or design a re-pricer? Stock is running out — should we
   just say out of stock, or have an inventory planner that can create an ASN or Purchase Order?
4. **Celebrate & think of growth, not just fix problems** — Surface wins and opportunities, not
   just issues. Growth command center, not stress dashboard; both aspects matter for success.
5. **UX first, technology later** — Design the experience, then figure out implementation

---

## Users

### Account Managers (Internal Employees)

- **Role:** Manage portfolio of brands across marketplaces (currently ~7 each, target 15+)
- **Mindset:** Analytical, efficiency-focused, pattern-seeking, operational
- **Goals:** Execute marketplace ops efficiently — onboarding, content, pricing, issue resolution
- **Key Question:** "What needs my attention today?" — surface issues, pending tasks, blocked items
- **Comfort Level:** High data density, complex filters, keyboard shortcuts
- **Context:** Daily power use, managing multiple brands simultaneously
- **Frustrations:** Slow workflows, too many clicks, buried information, manual work that could be
  automated
- **Platform Should:** Handle busy work, surface what needs action, make operations fast

### Growth Consultants (Internal Employees)

- **Role:** Strategic advisors working with brands on growth — fewer brands, deeper engagement
- **Mindset:** Strategic, data-driven, opportunity-seeking, client-facing
- **Goals:** Identify growth opportunities, advise on channel expansion, analyze performance,
  demonstrate Nasam's value
- **Key Question:** "What did Nasam do this month?" — needs one-click answer showing wins, growth,
  AND issues resolved
- **Comfort Level:** Dashboards, reports, trends — more consuming data than managing it
- **Context:** Reviews performance periodically, prepares recommendations, presents to brands
- **Frustrations:** Scattered data, no consolidated growth story, hard to quantify Nasam's impact
- **Platform Should:** Surface growth opportunities automatically, tell the growth story, make it
  easy to show brands what's working and what to do next

### Self-Serve Subscriber (Salla App Store today, custom websites later)

- **Role:** Runs their own brand on the platform — the same operator job as an AM, but for their
  own brand (or their org's brands). Any role on their side: owner, e-commerce manager, or staff.
- **Mindset:** Operator of their own business; ranges from a hands-on owner to a dedicated
  e-commerce manager. Usually not a power user.
- **Goals:** Grow their brand, catch what's slipping, know what to act on next — without a Nasam AM
  doing it for them
- **Key Question:** "How's my brand doing, and what should I fix or push next?"
- **Comfort Level:** Lower data density than an AM; may be non-technical; wants the right action
  made obvious, not buried in filters
- **Context:** Single-brand (or single-org) focus; operates the brand themselves, not just viewing it
- **Frustrations:** Tools built only for internal power users, jargon, having to assemble the
  picture themselves
- **Platform Should:** Give a self-serve operator the same surfaced-action experience an AM gets,
  in plain language, assuming no Nasam employee is in the loop

### Client / Reporting Viewer (managed-service brand)

- **Role:** Employees or the owner at a brand Nasam manages, checking in on how their brand is doing.
- ⚠️ **OPEN — not researched.** What this role actually needs is an unanswered question, not a gap
  for you to fill in. If a feature touches this role, raise it with the requester in Stage 1 and
  either get an answer or scope the role out of the discovery. Do not invent their goals,
  frustrations, or key question.
<!-- /REGION:full -->

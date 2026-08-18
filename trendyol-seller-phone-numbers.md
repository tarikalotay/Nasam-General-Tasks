# Trendyol Seller Phone Numbers — Cleaned List

Source: raw list of 45 numbers provided on 2026-08-18.

Cleaning applied:
- Added `+` prefix (country code in front).
- Removed the extra `0` after `966` (e.g. `96605...` → `+9665...`) — 8 numbers fixed.
- Validated format: `+9665` followed by 8 digits (12 digits total after `+`).
- No duplicates found.

## ✅ Clean list (44 numbers, comma-separated)

```
+966590698223,+966531531524,+966511458189,+966554865103,+966569694284,+966552570122,+966583767136,+966594374517,+966555924565,+966536067693,+966552071929,+966502839439,+966564481721,+966538475589,+966506053043,+966554909418,+966565076376,+966531530811,+966509770427,+966503838649,+966500335455,+966541867041,+966541434685,+966552591819,+966567244503,+966569391197,+966544382854,+966596123444,+966556319586,+966561269995,+966581155153,+966581662494,+966570651720,+966537183093,+966506647355,+966553139116,+966575214166,+966544448078,+966556072126,+966509083095,+966546993155,+966509443787,+966536253780,+966538862455
```

## ⚠️ Needs verification (1 number)

`96696537633193` — 14 digits, invalid as-is. Candidate interpretations checked against national numbering plans:

| Parse | Result | Verdict |
|---|---|---|
| Saudi with extra `96` typed: `966` + ~~96~~ + `537633193` | `+966537633193` — valid Saudi mobile (5XXXXXXXX) | ✅ Most likely |
| Kuwait: `966` (stray) + `965` + `37633193` | Kuwaiti numbers are 8 digits but must start with 2 (fixed) or 5/6/9 (mobile) — `3...` is not an assigned prefix | ❌ Ruled out |
| China: `+86...` | Number starts with `966`, not `86`; and the 11-digit remainder `96537633193` starts with 9, while Chinese mobiles must start with 1 | ❌ Ruled out |
| Other Gulf (UAE +971, Qatar +974, Bahrain +973, Oman +968, Yemen +967) | None of these codes appear at the start of the string | ❌ Ruled out |

Conclusion: almost certainly `+966537633193` (duplicate "96" typo). To confirm: save `+966537633193` in contacts and check if a WhatsApp account exists, or check the seller's registered phone in the Trendyol backoffice.

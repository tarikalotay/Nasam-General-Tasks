# Trendyol seller-outreach email — design brief (v3: big-brand, bilingual, direct)

Owner: Tarik Alotay (Business Development Executive, Trendyol, Saudi Arabia)
Goal: maximise reply / WhatsApp conversion from a personalised mass email inviting
marketplace sellers in Saudi Arabia to open a store on Trendyol. Read mostly in mail apps.

Design and planning: Fable · Execution: Opus · Quality check: Fable.

v3 changes (after review of v1):
- Redesigned to the standard of Apple, Samsung, Amazon, X and Starlink mass emails (see §2).
- Incentives removed: no benefits list, no fee / ads / campaign / peak-season promises.
- Message made direct: one ask (store link + CR number) in the first paragraph and in the steps.
- Bilingual: Arabic and English. Shared hero, stats, steps, CTA, signature and footer carry both
  languages; the personal message is split into two columns (Arabic right, English left on PC;
  Arabic first, then English on phone).
- PC preview rendered at a reading-pane width (960px) so the email is legible, not lost in a canvas.

---

## 1. Brand tokens (sampled from the Trendyol "About us" deck)

| Token | Value | Use |
|---|---|---|
| Orange | `#FF6720` | Hero field, primary buttons, numerals, accent labels |
| Orange dark | `#E5581A` | Borders on orange, pressed states |
| Peach tint | `#FFF3EC` | CTA panel background |
| Ink | `#181818` | Headlines, stats band background, wordmark |
| Body | `#434343` | Body copy |
| Muted | `#7A7A7A` | Captions, footer |
| Line | `#E6E6E6` | Dividers |
| Off-white | `#FAFAFA` | App-showcase section, footer background |
| Page | `#F2F2F2` | Page background behind the 680px column |
| White | `#FFFFFF` | Message and steps sections |

Typography: Latin `'Inter','Helvetica Neue',Helvetica,Arial,sans-serif`; Arabic
`'Noto Sans Arabic','Segoe UI',Tahoma,Arial,sans-serif`. Google Fonts `<link>` in the head (not `@import`, which Gmail can choke on) for both
(`Inter:wght@400;500;600;700;800` and `Noto+Sans+Arabic:wght@400;500;600;700`).
Trendyol's Arabic wordmark spelling is `ترينديول`. Logo rules as before: black lowercase
wordmark on white/off-white, white on orange, never stretched or recoloured.

Assets (all in `assets/`, 2x for retina):

| File | Size | Display | Use |
|---|---|---|---|
| `trendyol-logo-extended.png` | 400×133 | 200px wide | Top bar: extended lockup, wordmark + orange .com tag (Wikimedia Commons, Trendyol trademark) |
| `trendyol-logo.png` | 716×163 | unused | Plain wordmark from the deck, kept for reference |
| `hero-hand-phone.jpg` | 640×697 | 100% of cell, max 320px wide | Hero image, already flattened on `#FF6720` |
| `app-hand-phone.jpg` | 640×792 | 100% of cell, max 320px wide | App showcase, flattened on `#FAFAFA` to match its band |
| `whatsapp-icon-orange.png` | 96×96 | 20px | Icon in the white hero button |
| `whatsapp-icon-white.png` | 96×96 | 20px | Icon in the orange CTA button |

---

## 2. What the big-brand standard looks like, and how v3 applies it

| Standard (Apple, Samsung, Amazon, X, Starlink) | v3 |
|---|---|
| One column, 600–680px, mobile-first, full-bleed colour sections, no card chrome | 680px column, square full-width sections: white / orange / white / ink / off-white / white / peach / white / off-white |
| Big headline (32–44px), one-line subhead, one CTA above the fold | Hero: 12px eyebrow, Arabic H1 34px (phone) / 42px (PC), English H1 30/38px, then the white WhatsApp button, then the product image |
| Product imagery as the hero, device-in-hand shots | Deck cover shot (hand + phone with Trendyol splash) in the hero; Saudi app in hand in the showcase |
| Very short copy, scannable modules, big numbers | Message = 3 short paragraphs + 2-item ask per language; stats band with 3 numbers; 3 one-line steps |
| High-contrast rounded buttons, repeated at the end | White-on-orange button in hero, orange button + outline button in the CTA panel |
| Generous spacing (40–56px section padding) | 48px top/bottom on PC, 36px on phone; 24px side on phone |
| Logo alone in the top bar; small grey legal footer | Centered wordmark top bar; bilingual footer with opt-out |

---

## 3. Content (final copy)

Merge fields: `{{seller_name}}` only, plus `{{seller_name_url}}` (URL-encoded seller name, derived by the script).

Subject line (A/B):
- A: `{{seller_name}} × Trendyol: open your store · افتحوا متجركم على ترينديول`
- B: `Tarik from Trendyol · طارق من ترينديول — {{seller_name}}`

Preheader (hidden): `Reply with your store link and CR number. I'll handle the rest. · أرسلوا رابط متجركم ورقم السجل التجاري وسأتولى الباقي.`

### 3.1 Top bar (white, centered)
Extended logo `assets/trendyol-logo-extended.png`, 200px wide, alt `trendyol.com`, padding 24px top/bottom.

### 3.2 Hero (orange `#FF6720`, everything centered)
- Eyebrow (12px/18, SemiBold, letter-spacing 1.5px on the Latin part, colour `#FFE0D2`):
  `SELLER INVITATION · دعوة للبائعين`
- Seller name line (English, Inter 800, 28px/34 phone, 32px/38 PC, white, letter-spacing 0.5px): `{{seller_name}}`
- Arabic H1 (`dir="rtl" lang="ar"`, Noto Sans Arabic 700, 34px/44 phone, 42px/54 PC, white):
  `افتحوا متجركم على ترينديول`
- English H1 (Inter 700, 30px/36 phone, 38px/44 PC, white, 8px below the Arabic H1):
  `Open your store on Trendyol.`
- Both H1s sit in a nested table `max-width:600px`; on PC each fits on one line, on phone they wrap to two balanced lines.
- Primary button (white `#FFFFFF` background, orange text, radius 12px, `max-width:340px`, width 100%,
  padding 14px 20px, orange WhatsApp icon 20px + 8px gap), two-line label:
  line 1 Inter 600 16px `Message me on WhatsApp`, line 2 Noto Sans Arabic 500 14px `dir="rtl"` `راسلني على واتساب`
  → `https://wa.me/966550184495?text=Hi%20Tarik%2C%20this%20is%20{{seller_name_url}}.%20We%27d%20like%20to%20join%20Trendyol.`
- Hero image row: `assets/hero-hand-phone.jpg`, `width="320"` attribute, `style="width:100%; max-width:320px; height:auto; display:block; margin:0 auto"`,
  alt `Trendyol app on a phone`, 28px above it, **0px below it** (the hand bleeds off the bottom edge of the orange).
- Hero padding: 40px 32px 0 on PC, 36px 24px 0 on phone.

### 3.3 Personal message (white, two columns)
Arabic column (right on PC, first on phone; `dir="rtl" lang="ar"`, text right-aligned, Noto Sans Arabic 16px/28, colour `#434343`):
> مرحباً فريق {{seller_name}}،
>
> أنا **طارق**، مسؤول تطوير الأعمال في ترينديول. لاحظنا حضوركم القوي في قنوات البيع، ونريد منتجاتكم على ترينديول.
>
> **للبدء، ردّوا على هذا الإيميل أو راسلوني على واتساب وأرسلوا:**
> 1. رابط متجركم
> 2. رقم السجل التجاري
>
> سأفتح متجركم وأجهّز منتجاتكم للبيع. يستغرق التسجيل من أسبوع إلى أسبوعين.

English column (left on PC, second on phone; `dir="ltr" lang="en"`, left-aligned, Inter 16px/26, `#434343`):
> Hi {{seller_name}} team,
>
> I'm **Tarik**, Business Development Executive at Trendyol. We saw your strong presence across sales channels, and we want your products on Trendyol.
>
> **To start, reply to this email or message me on WhatsApp with:**
> 1. Your store link
> 2. Your CR number
>
> I'll open your store and get your catalogue live. Onboarding takes 1–2 weeks.

Bold = Inter/Noto 700, colour `#181818`. The numbered items are a 2-column table (numeral cell
28px wide, orange 16px Bold, bare numerals `1` `2` without dots; in the Arabic column the table is `dir="rtl"` so numerals sit on the right).

### 3.4 Stats band (ink `#181818`, three stats)
Title row (centered, 12px/18 SemiBold letter-spaced on the Latin part, colour `#FF6720`): `TRENDYOL IN THE GULF · ترينديول في الخليج` (year lives in the labels and footnote so the title stays on one line on phone)
Each stat: number (Inter 800, 44px/48, white), English label (Inter 13px/18, `#FFB38A`), Arabic label
(Noto 13px/22, `#FFB38A`, `dir="rtl"`), all centered.
- `4M+` — `Active shoppers in the Gulf` — `متسوق نشط في الخليج`
- `35M` — `Units sold in 2025` — `منتج مُباع في 2025`
- `#2` — `Saudi Arabia: our 2nd-largest market worldwide` — `السعودية ثاني أكبر أسواقنا عالمياً`
Footnote (11px/16, `#9A9A9A`, centered): `Trendyol Gulf figures, 2025 · أرقام ترينديول في الخليج، 2025`

### 3.5 App showcase (off-white `#FAFAFA`, centered)
- Title (Inter 700 22px/28 ink, manual break for balanced lines): `Your products,` / `in the Trendyol app.`
- Arabic title (Noto 700 22px/34 ink, `dir="rtl"`): `منتجاتكم في تطبيق ترينديول`
- Image: `assets/app-hand-phone.jpg`, `width="320"`, `max-width:320px; width:100%`, alt `Trendyol app in Saudi Arabia`, 24px above, 0 below (bleeds off the section's bottom edge).

### 3.6 How it works (white)
Title (centered, Inter 700 22px/28 ink): `How it works · كيف تبدأ`
Three rows, each: numeral cell 44px wide (Inter 800 28px/32 orange) + text cell with an English line
(Inter 600 16px/24 ink) and an Arabic line beneath (Noto 400 15px/26 `#434343`, `dir="rtl"`, right-aligned... **no**: keep the Arabic line left-aligned in the same cell but with `dir="rtl"` so it reads correctly; alignment follows the cell = left).
1. `Send your store link and CR number.` / `أرسلوا رابط متجركم ورقم السجل التجاري.`
2. `We open your store and list your catalogue. 1–2 weeks.` / `نفتح متجركم ونضيف منتجاتكم. من أسبوع إلى أسبوعين.`
3. `Start selling to 4M+ Gulf shoppers.` / `ابدأوا البيع لأكثر من 4 ملايين متسوق في الخليج.`
Rows separated by 1px `#E6E6E6` lines, 16px padding above and below each row.

### 3.7 CTA panel (peach `#FFF3EC`, centered)
- Line 1 (Inter 600 18px/26 ink, manual break): `Reply to this email` / `or message me on WhatsApp.`
- Line 2 (Noto 600 18px/30 ink, `dir="rtl"`, manual break): `ردّوا على هذا الإيميل` / `أو راسلوني على واتساب.`
- Primary button (orange `#FF6720`, white text, radius 12px, max-width 340px, padding 14px 20px, white WhatsApp icon), two-line label as in the hero. Same wa.me link.
- Secondary button (white, 2px `#FF6720` border, orange text, radius 12px, padding 12px 20px), two-line label:
  `Reply to this email` / `الرد على هذا الإيميل`
  → `mailto:tarik.alotay@trendyol.com?subject={{seller_name_url}}%20x%20Trendyol%20%E2%80%94%20let%27s%20start`
- Phone line (13px/20 muted, `white-space:nowrap`): `+966 55 018 4495`
12px between buttons, 16px above the phone line.

### 3.8 Signature (white)
Row: 48px orange disc with white `TA` (Inter 700 18px) | text block:
- `Tarik Alotay` (Inter 600 16px/24 ink; the intro uses the first name only)
- `Business Development Executive · مسؤول تطوير الأعمال` (Inter 14px/22 `#434343`; the Arabic part in a `dir="rtl"` no-wrap span)
- `Trendyol, Saudi Arabia · ترينديول، السعودية` (same treatment)
- `tarik.alotay@trendyol.com · +966 55 018 4495` (Inter 13px/20 muted; both links `#434343`, no underline; phone `white-space:nowrap`)

### 3.9 Footer (off-white `#FAFAFA`, centered, 12px)
- `Trendyol · Riyadh, Saudi Arabia · ترينديول، الرياض` (`#7A7A7A`)
- EN (12px/18 `#7A7A7A`): `You're receiving this one-time invitation because your store is publicly listed on marketplaces in Saudi Arabia. Not interested? Reply "unsubscribe" and I won't write again.`
- AR (Noto 12px/22 `#7A7A7A`, `dir="rtl"`): `تصلكم هذه الدعوة لمرة واحدة لأن متجركم مُدرج علناً في منصات البيع بالسعودية. غير مهتمين؟ ردّوا بكلمة «إلغاء» ولن أراسلكم مجدداً.`
- `© 2026 Trendyol`

---

## 4. Layout and responsive rules

- Outer table 100% `#F2F2F2`; inner column `width="680"` attribute + `style="width:100%; max-width:680px"`,
  centered. No border radius on sections (full-bleed look); the page background shows the column edge on PC.
- Section padding: 48px 32px on PC; `.sec-pad` → 36px 24px on ≤ 620px. Hero and showcase have 0 bottom padding.
- **Two-column message (hybrid inline-block, no media query needed for the split):**
  - Wrapper `<td dir="rtl" align="center" style="font-size:0; line-height:0; text-align:center;">`
    inside the white section's padded cell.
  - Two `<div class="col">`: `display:inline-block; width:100%; max-width:308px; vertical-align:top;`
    (616px inner ÷ 2). First div = Arabic (`dir="rtl" lang="ar"`, text right), second = English
    (`dir="ltr" lang="en"`, text left). Because the wrapper is `dir="rtl"`, Arabic sits on the
    right on PC and stacks first on phone.
  - Each div holds a single-cell table (`dir` = its language, `width="100%"`) whose cell carries
    typography. Gutter: Arabic cell `padding-left:14px`, English cell `padding-right:14px`.
  - Outlook (Word) fallback around the two divs:
    `<!--[if mso]><table role="presentation" width="100%" dir="rtl" cellpadding="0" cellspacing="0" border="0"><tr><td width="50%" valign="top"><![endif]-->` …
    `<!--[if mso]></td><td width="50%" valign="top"><![endif]-->` … `<!--[if mso]></td></tr></table><![endif]-->`
  - Media query ≤ 620px: `.col { max-width:100% !important; }`, gutters → 0, English cell gets
    `padding-top:28px !important; border-top:1px solid #E6E6E6;` and the Arabic cell `padding-bottom:28px !important`.
- **Stats band:** same hybrid pattern with three `<div class="stat">` at `max-width:205px`
  (`dir="ltr"` wrapper, centered). Media query ≤ 620px: `.stat { max-width:100% !important; }`
  and 24px padding between stacked stats. Without media query support the 205px blocks wrap one
  per row at phone width anyway.
- Buttons: bulletproof anchors (`display:block`, padding on the `<a>`), `bgcolor` + `border-radius`
  on the cell; the WhatsApp icon `display:inline-block; vertical-align:middle` before the English label;
  Arabic label on its own line via `<br>` inside a `<span dir="rtl" lang="ar">`.
- Images: `border="0"`, `display:block`, explicit `width` attribute, `height:auto`, alt text. No background images.
- Type sizes on phone via the media query only where stated (H1s). Everything else is fluid.
- `color-scheme: light` meta tags; `bgcolor` on every filled cell so dark mode does not invert the orange or ink bands.
- `<html lang="en">`; every Arabic container carries `lang="ar" dir="rtl"`.

## 5. Engineering rules

- Tables only (`role="presentation"`, `cellpadding="0" cellspacing="0" border="0"`), inline CSS.
  `<style>` only for: Google Fonts `@import`, resets, and the single `@media only screen and (max-width:620px)` block.
- No JavaScript, no SVG, no flex/grid, no `position`, no `<div>` layout beyond the `.col` / `.stat`
  inline-block wrappers and the preheader.
- Every merge field exactly as named in §3. Relative `assets/...` image paths (README covers hosting).
- Five `<img>` total: logo, hero, app showcase, two WhatsApp icons.

## 6. Render outputs (Playwright)

- `output/trendyol-seller-email-phone.png` — viewport 390×844, deviceScaleFactor 2, full page.
- `output/trendyol-seller-email-desktop.png` — **viewport 960×800**, deviceScaleFactor 2, full page
  (reading-pane width: the email fills ~70% of the frame).
- `output/email-okwan-sample.html` — merged sample.
- Fonts for rendering from `assets/fonts/local-fonts.css` (offline), injected only by the render script.

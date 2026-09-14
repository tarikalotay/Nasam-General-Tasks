# Trendyol seller-outreach email — design brief

Owner: Tarik Alotay (Business Development Executive, Trendyol, Saudi Arabia)
Goal: maximise reply / WhatsApp conversion from a personalised mass email inviting
marketplace sellers in Saudi Arabia to open a store on Trendyol.

Design and planning: Fable · Execution: Opus · Quality check: Fable.

---

## 1. Brand study (source: Trendyol "About us" deck, Dec 2025 data)

Sampled directly from the deck pages:

| Token | Value | Where it comes from |
|---|---|---|
| Orange (primary) | `#FF6720` | Cover page, all stat numbers, icons, headings |
| Orange (dark, pressed/borders) | `#E5581A` | Derived, ~10% darker |
| Peach tint (soft panels) | `#FFF3EC` | Lightened from the deck's `#FBCBB5` chart tint |
| Peach border | `#FFD9C7` | Derived |
| Ink (headlines, logo) | `#181818` | Wordmark and headline text |
| Body text | `#434343` | Body copy on slides |
| Muted text | `#7A7A7A` | Captions, footnotes (`#A7A7A7` on deck, darkened for AA contrast) |
| Line / divider | `#E6E6E6` | Card borders |
| Off-white page | `#FAFAFA` | Every slide background |
| Card white | `#FFFFFF` | Cards, tiles |
| Accent blue (unused) | `#058DC7` | One callout band. Not used, to keep the email single-accent |

Typography: the deck is set entirely in **Inter** (Regular, Medium, SemiBold, Bold, Black).
Email stack: `'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif` with a Google Fonts
link for clients that load web fonts (Apple Mail, iOS Mail, Outlook for Mac). Arabic line
uses `'Noto Sans Arabic', 'Segoe UI', Tahoma, Arial, sans-serif`.

Logo: black lowercase wordmark `trendyol` on white or off-white, or white wordmark on
orange. Never stretched, never recoloured. Minimum clear space = height of the "t".
Orange is used as a solid field, not as gradients. Corners are softly rounded
(cards ~12px, buttons ~10px, the `.com` tag in the logo is a rounded rectangle).

Voice from the deck: confident, number-led, short sentences, "we" + "our partners",
big stat + small label pattern.

Note: Trendyol's consumer website uses `#F27A1A`; the official deck supplied for this
task uses `#FF6720`. The template follows the deck. Swapping is a single find-replace.

---

## 2. Conversion strategy (why the email is built this way)

1. **Personal, not corporate.** One named sender, first-person copy, a signature card.
   Mass-personalised via merge fields `{{seller_name}}`, `{{category}}`, `{{item_count}}`.
2. **Relevance in the first two lines.** The seller's own category and catalogue size
   appear before any Trendyol facts. No competitor marketplaces are named
   ("sales channels" only), per brief.
3. **Proof, then offer, then ask.** Four Gulf stats → concrete seller benefits →
   three-step "how it works" → two CTAs.
4. **Low-friction ask.** Step 1 tells the seller exactly what to send
   (store link + CR number), so a reply is a 30-second job. WhatsApp deep link has a
   pre-filled message; the mailto has a pre-filled subject.
5. **Urgency that is true.** Q4 peak (Legendary Friday in November) with the deck's
   real peak-day numbers. No fake deadlines.
6. **Trust and deliverability.** Real title, real phone, real Trendyol address, plain
   opt-out line, no image-only content, alt text everywhere, text-to-image ratio high.
7. **Bilingual welcome.** One short Arabic line near the CTA so Arabic-first sellers
   know they can reply in Arabic.

---

## 3. Content (final copy)

Subject line (A/B):
- A: `{{seller_name}} + Trendyol: your {{category}} range in front of 4M+ Gulf shoppers`
- B: `Tarik from Trendyol — a quick idea for {{seller_name}}`

Preheader (hidden): `I saw your {{item_count}} items in {{category}}. Let's get them selling on Trendyol before the Q4 peak season.`

### Header
Trendyol wordmark (black) left; small muted text right: `Seller invitation · Saudi Arabia`.

### Hero (solid orange field, white text)
- Eyebrow (12px, letter-spaced, 80% white): `A PERSONAL INVITATION`
- H1 (30px desktop / 26px mobile, Bold, white): `{{seller_name}}, let's bring your products to 4M+ Gulf shoppers`
- Sub (16px, 90% white): `From Trendyol's Business Development team in Riyadh.`

### Personal intro (white card)
> Hi {{seller_name}} team,
>
> I'm **Tarik Alotay**, Business Development Executive at Trendyol. We saw your amazing presence across sales channels in **{{category}}**, with **{{item_count}} items** live, and we're keen to bring that success to Trendyol.
>
> Trendyol is Türkiye's leading e-commerce platform, serving 40M+ active shoppers across 35 countries, and Saudi Arabia is now our second-largest market worldwide. I'd like to personally onboard your store, get your catalogue listed, and give you campaign support from day one.

### Stats (2×2 tiles, peach tint, orange number + muted label)
Section title: `Trendyol in the Gulf, 2025`
- `4M+` — Active shoppers
- `35M` — Units sold
- `~$1B` — Marketing invested
- `15K` — Gulf influencers
Footnote (12px muted): `Trendyol Gulf figures, 2025.`

### What you get (checklist, orange check discs)
Section title: `What you get as a Trendyol seller`
1. **No setup or monthly fees.** A category-based commission only when you sell.
2. **A dedicated account manager (me)** for onboarding, listing and campaigns.
3. **Seller Center in English and Arabic** with real-time dashboards, campaign tools and seller ads. 150K+ sellers used ads in 2025, with returns up to 12×.
4. **Peak-season firepower.** On Legendary Friday we reached 5M daily active users and 3.5M units sold in a single day. Join now to be live for Q4.

### How it works (3 numbered steps, orange numerals)
Section title: `How it works`
1. **Reply or WhatsApp me.** Send your store link and CR number. That's all I need to start.
2. **I open your store and help list your catalogue.** Onboarding usually takes 1–2 weeks.
3. **Go live with campaign support.** Homepage visibility, discount tools and ads from our team.

### CTA block (peach panel)
- Title: `Ready when you are`
- Text: `Two ways to start. Pick whichever is easier:`
- Primary button (orange, white WhatsApp icon + label): `Message me on WhatsApp`
  → `https://wa.me/966550184495?text=Hi%20Tarik%2C%20this%20is%20{{seller_name_url}}.%20We%27d%20like%20to%20join%20Trendyol.`
- Secondary button (white, orange 2px border, orange text): `Reply to this email`
  → `mailto:tarik.alotay@trendyol.com?subject={{seller_name_url}}%20x%20Trendyol%20%E2%80%94%20let%27s%20start`
- Small line (13px muted): `+966 55 018 4495 · English or Arabic, whichever you prefer.`
- Arabic line (14px, RTL, dir="rtl"): `يسعدني التواصل بالعربية أيضاً`

### Signature card (white card, thin line)
- Avatar disc: orange circle, white initials `TA` (no photo available)
- `Tarik Alotay` (16px SemiBold ink)
- `Business Development Executive · Trendyol, Saudi Arabia` (14px body)
- `tarik.alotay@trendyol.com · +966 55 018 4495` (13px muted; both as links)

### Footer (muted, 12px, centered)
- `Trendyol · Riyadh, Saudi Arabia`
- `You're receiving this one-time invitation because your store is publicly listed on marketplaces in Saudi Arabia. Not interested? Reply "unsubscribe" and I won't write again.`
- `© 2026 Trendyol`

---

## 4. Layout and responsive rules

- Hybrid table layout, container `max-width:600px; width:100%`, centered on `#FAFAFA`.
- Card padding 32px desktop, 20px on ≤620px. Section gap 28px.
- Stat tiles are a 2×2 table at every width (each 50%), so they never rely on media queries.
- Buttons stack vertically at every width, centered, `width:100%; max-width:340px`,
  min-height 48px, font 16px SemiBold, radius 10px. Tap target ≥ 44px.
- Type scale: H1 30/36 desktop → 26/32 mobile; section titles 20/26; body 16/26;
  small 13/20; stat numbers 30/34 Bold orange; step numerals 22px Bold orange.
- Colour contrast: body `#434343` on white = 9.7:1; white on `#FF6720` for 16px+ bold text.
- Images: `trendyol-logo.png` (display width 132px, 2x asset), `trendyol-logo-white.png`
  (unused by default, available), `whatsapp-icon-white.png` (display 20px). All with alt text,
  `border:0; display:block`. No background images. Only three image requests total.
- Dark-mode: declare `color-scheme: light` meta tags and set `bgcolor` attributes so clients
  do not invert the orange field.

## 5. Email-client engineering rules for the build

- Tables only (`role="presentation"`, `cellpadding="0" cellspacing="0" border="0"`), inline
  CSS for everything that matters. `<style>` only for the Google Fonts `@import`, resets and
  the single `@media only screen and (max-width:620px)` block.
- Buttons: bulletproof anchors (padding on the `<a>`, `display:inline-block`) inside a
  table cell with `bgcolor` and `border-radius`.
- Preheader: hidden div with `display:none;font-size:1px;max-height:0;overflow:hidden` plus
  whitespace padding characters.
- Every `{{merge_field}}` appears exactly as written in section 3. `{{seller_name_url}}` is the
  URL-encoded seller name (render script derives it).
- Relative image paths `assets/...` for local preview and render; README explains replacing
  with hosted URLs before sending.
- Validate: no `<div>`-only layout, no flex/grid, no JavaScript, no SVG inline, no `position`.

## 6. Render outputs (Playwright)

- `output/trendyol-seller-email-phone.png` — viewport 390×844, deviceScaleFactor 2, full page.
- `output/trendyol-seller-email-desktop.png` — viewport 1280×800, deviceScaleFactor 2, full page.
- `output/email-okwan-sample.html` — the merged sample.
- Fonts for rendering come from `assets/fonts/local-fonts.css` (Inter + Noto Sans Arabic,
  offline), injected only by the render script, never shipped in the email.

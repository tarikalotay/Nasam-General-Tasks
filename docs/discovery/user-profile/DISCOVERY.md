# User Profile (Localized Names, Phone) - UX Discovery

**Status:** Proposed · **Requested by:** Tarik · **Date:** 2026-09-05
**Revision:** contact email and the live name preview were removed at the requester's decision; the profile holds names + phone only.
**Repos affected:** `Nasam-co/nasam` (API + DB), `Nasam-co/nasam-frontend-v2` (UI)

## Outcome

**Business goal:**
1. Stop showing mixed-language greetings such as "مساء الخير يا Tarik" (Arabic sentence, English name). The greeting should read naturally in whichever language the user chose.
2. Have a reliable way to reach every platform user (phone) when something urgent happens with a brand — a listing suspension, an account-health penalty, a failed campaign — and the person needs to be contacted outside the app.

**Success metrics:**
- 0 greetings where the name script does not match the UI language for users who filled a name in that language.
- % of active users with a phone number on file (target: 100% of internal AMs/GCs within 2 weeks of release, then client and Salla users over time).
- % of users with at least one localized name (AR or EN) on file.

## Problem Statement

Nasam stores only one "full name" and one login email per user, so the platform cannot address the user correctly in both Arabic and English and has no phone number to reach them when a brand emergency happens outside the app.

## Target User

**Primary:** Every logged-in user — Nasam AMs and GCs, client-brand users, Salla App Store subscribers. Nobody is excluded; the same profile screen serves all roles.
**Secondary:** Admins who manage users (the existing "تعديل المستخدم / Edit user" dialog in image 2) — they need to see and correct the same fields.

**Context:** Occasional. A user opens their profile once at the start (to fill it in) and then rarely — when a phone number changes, or when they notice their name is shown wrong. It must be quick, obvious, and forgiving; nobody will "learn" this screen.

## Jobs-to-be-Done

- **Functional:** "Let me tell the platform how to write my name in Arabic and in English, and how to reach me."
- **Emotional:** "The product knows who I am and talks to me properly in my language." A greeting with the wrong-script name reads as sloppy; the right one reads as care.
- **Social:** For AMs and GCs whose names appear to clients (in reports, in the sidebar when screen-sharing), the name should look professional in both scripts.
- **For Nasam (the business):** "When a brand is on fire at 11pm, I can call the person responsible."

## Current State (from screenshots)

- **Image 1 — sidebar footer:** avatar initial + name ("Tarik") + email. Clicking it opens a menu with Appearance (light/dark), Language (English/العربية), and Logout. There is no "profile" entry.
- **Image 2 — admin "Edit user" dialog:** Email (read-only, "cannot be changed") + Full name (single field, currently holding an Arabic name "محمد العدوي"). One name field, no language distinction, no phone.
- **Image 3 — home page greeting:** "مساء الخير يا Tarik" — Arabic time-of-day greeting concatenated with the single stored name, which is in Latin script. The same user with the UI in English would get "Good evening, محمد" for an Arabic-named user.

Root cause: one free-text `fullName` field with no language, and the greeting simply interpolates it.

## Solution Concept

**Direction:** Add a self-service **Profile** dialog reachable from the sidebar user menu (and by clicking the name/avatar row). It holds two localized name fields (Arabic, English), the login email (read-only), and an optional phone number with a country-code selector. Everywhere the platform shows the user's name (greeting, sidebar, admin user list, reports), it uses a single `displayName(user, locale)` rule that picks the name matching the current UI language and falls back sensibly.

**Key insight:** The greeting bug is not a greeting bug — it is a data-model bug. Fixing it means storing names per language, and the profile screen is simply the place where users supply that data. Solving the naming problem gives us a natural, non-intrusive moment to also ask for contact details.

**Alternatives considered:**
- *Transliterate the name automatically* (Tarik → طارق). Rejected: transliteration of personal names is unreliable and people are sensitive about how their name is spelled. Users must own their names.
- *Add the fields only to the admin "Edit user" dialog.* Rejected: it does not scale to Salla self-serve subscribers, who have no Nasam admin, and it makes AMs' contact info someone else's chore.
- *Full-page `/profile` route with sections (security, notifications, etc.).* Deferred: we have four fields today; a dialog matching the existing "Edit user" pattern (image 2) is the minimum. A page can replace it later if more settings accumulate.

## User Flow

### Entry points
1. **Sidebar user menu** (image 1) — new first item "الملف الشخصي / My profile" above Appearance. The name/avatar row itself also opens the profile on click.
2. **Completion nudge** — a dismissible, one-line prompt on the home page under the greeting for users with **no phone number**: "أضف رقم جوالك حتى نتمكن من التواصل معك في الحالات الطارئة" / "Add your phone so we can reach you in urgent cases" with an "Add" link that opens the profile focused on the phone field. Shown at most once per session, gone permanently once a phone is saved or after being dismissed 3 times.

### Happy path
1. User clicks their name in the sidebar footer → menu opens → "My profile".
2. Profile dialog opens with current values prefilled (see migration below for how existing names are split).
3. User edits Arabic name, English name, phone (country code selector defaults to Saudi Arabia +966, or to the user's already-saved country).
4. "Save" → inline validation → success toast "تم حفظ الملف الشخصي" / "Profile saved" → dialog closes.
5. Sidebar name and home greeting update immediately with no reload (refetch or optimistic update of the current-user store).

### Alternative paths
- Admin edits another user via the existing "Edit user" dialog: the same field set appears there (login email still read-only). Admin changes follow the same validation.
- User switches UI language after saving: sidebar and greeting switch to the other-language name automatically.

### Edge cases
- **Only one name filled** (e.g. Arabic only, UI in English): show the Arabic name rather than nothing. A name in the "wrong" script is better than an empty greeting, and it nudges nothing — the user chose not to fill English.
- **Neither localized name filled** (legacy users before migration, or migration could not classify): fall back to the legacy `fullName`. Never render "مساء الخير يا" with nothing after it — if all names are empty, drop the name part: "مساء الخير" / "Good evening".
- **Existing full name is mixed script** ("Mohamed العدوي"): migration leaves both localized names empty and keeps `fullName` as the fallback; the user will be asked to fill them.
- **Phone entered with a leading 0 or with the country code typed into the number** (common for +966 05x…): normalize with a phone library (libphonenumber) before validation; store E.164 (`+9665xxxxxxxx`) plus ISO country (`SA`). Display formatted for humans.
- **Phone already used by another user:** allow it (a brand owner and their assistant may share a business line). No uniqueness constraint.
- **Very long or emoji-laden names:** trim, max 100 chars per name, reject control characters.

### Error states
- **Arabic name contains no Arabic letters** (e.g. user types "Tarik" into the Arabic field): block save with "الاسم العربي يجب أن يُكتب بحروف عربية" / "Arabic name must be written in Arabic letters". This is the single most important validation — it is the only thing that structurally prevents image 3 from recurring.
- **English name contains Arabic letters:** symmetric error "English name must be written in Latin letters".
- **Invalid phone for the selected country:** "رقم الجوال غير صحيح لهذه الدولة" / "This number is not valid for the selected country".
- **Network / server failure on save:** keep the dialog open with values intact, show an error toast, allow retry.

### Empty state
First open after release: localized names prefilled by migration where possible, phone empty with the country selector on +966. Optional fields carry helper text explaining *why* we ask (see Content Needs) — this is the difference between "another form" and "they want to reach me if my store has a problem".

## Information Architecture

The dialog is one screen, no tabs. Order reflects what the user came for and what we want most.

### Primary (must see immediately)
- **Arabic name** — text input, `dir="rtl"`, placeholder with an example ("محمد العدوي"). Helper: "يُستخدم عندما تكون واجهة المنصة بالعربية".
- **English name** — text input, `dir="ltr"`, placeholder ("Mohamed Eladawy"). Helper: "Used when the platform is in English".
- **Phone** — country-code selector (flag + dial code, searchable by country name in both languages) + number input, `dir="ltr"` even in the Arabic UI (phone numbers are always LTR). Helper explains the emergency-contact purpose.
- **Save / Cancel** buttons, Save disabled until something changed and valid.

### Secondary (supporting context)
- **Login email** — read-only, with the existing note "لا يمكن تغيير البريد الإلكتروني" (same as image 2). Keeps the user oriented about which account this is.

### Tertiary (on demand)
- Nothing hidden. Three inputs and a read-only email do not need progressive disclosure. Resist adding role, avatar upload, password change here for now — those are separate tasks.

### Navigation placement
- Sidebar footer menu (image 1): **My profile · Appearance · Language · Logout**, in that order. Profile is first because it is an action on "me"; the other three are preferences and stay where users know them.
- Admin user management (image 2): same fields inside the existing "Edit user" dialog, replacing the single "Full name" input with the two localized names, and adding phone below the email. Admin dialog keeps its title and layout otherwise. The Role ("الدور") control and all other existing settings in that dialog are out of scope and stay as they are; they will be handled in a later task.

## Key Interactions

- **Open:** click name/avatar row or "My profile" menu item → dialog (desktop) / full-screen bottom sheet (mobile, < 640px).
- **Names:** each input forces its own text direction regardless of UI language, so an Arabic user typing their English name does not fight the cursor.
- **Phone:** selecting a country updates the dial-code prefix and validation rules; pasting a full international number ("+966 55 123 4567") auto-selects the country. Number field accepts Arabic-Indic digits (٠١٢…) and converts them to Latin digits on blur.
- **Save:** validates on submit (not on every keystroke) to avoid red errors while typing; after the first failed submit, fields re-validate on change so errors clear as they are fixed.
- **Dirty-close guard:** closing with unsaved changes asks "تجاهل التغييرات؟ / Discard changes?".
- **After save:** the current-user store updates, sidebar and greeting re-render, dialog closes, toast confirms. No page reload.
- **Keyboard:** Tab order top-to-bottom as listed, Enter submits, Esc closes (with guard).
- **Mobile:** same fields stacked; country selector opens as a full-height searchable list; Save is a sticky bottom button.

## Data Model & API (implementation notes)

Field names are a proposal; the implementer should align with existing conventions in `Nasam-co/nasam`.

**`users` table — new nullable columns:**

| Column | Type | Notes |
|---|---|---|
| `name_ar` | varchar(100) | Arabic-script name |
| `name_en` | varchar(100) | Latin-script name |
| `phone_e164` | varchar(20) | E.164, e.g. `+966551234567` |
| `phone_country` | char(2) | ISO 3166-1 alpha-2, e.g. `SA` |

- Keep the existing `full_name` (mandatory) untouched as the fallback. Do not rename or drop it in this task.
- **One-time migration/backfill:** for each user, if `full_name` is entirely Arabic script (plus spaces) → copy into `name_ar`; if entirely Latin → copy into `name_en`; otherwise leave both null. This makes the feature "work" for most users on day one without asking anything.

**API:**
- `GET /me` — returns the four new fields alongside the existing ones.
- `PATCH /me` — accepts the four fields; server-side validation: script check per name, phone parsed/validated with libphonenumber for the given country. Login email is not accepted here.
- Admin `PATCH /users/:id` — same fields, same validation, existing authorization.

**Visual palette:** stay on the existing Nasam UI palette as seen in the current app (dark sidebar, cream surfaces, neutral borders, dark-ink primary button, red only for errors and logout). Do not introduce green accent colors, badges, or highlights; the mockups in `mockups/` follow this.

**Display rule (single shared helper, used everywhere a user's name is rendered):**

```
displayName(user, locale):
  if locale == 'ar' and user.name_ar   → user.name_ar
  if locale == 'en' and user.name_en   → user.name_en
  if user.name_ar or user.name_en      → whichever exists
  else                                 → user.full_name
```

The home greeting must use this helper and must omit the "يا {name}" / ", {name}" segment entirely when it returns empty.

## Design Decisions

- **Two explicit name fields instead of one name + transliteration:** people own the spelling of their name; automatic transliteration would create a worse version of the same bug.
- **Script validation on the name fields is a hard error, not a warning:** it is the only mechanism that structurally prevents mixed-script greetings; a warning would be ignored.
- **All new fields optional:** the request is explicit that existing data stays mandatory and new data is optional. Making phone mandatory would block login-critical flows for Salla subscribers who just want to look around. The nudge covers the gap for now; mandatory phone for internal roles can be a follow-up policy decision.
- **Dialog, not a page:** matches the existing "Edit user" pattern (image 2), lowest effort, and four fields do not justify a route. Revisit when avatar, password, notification settings, or 2FA land.
- **Same fields in the admin dialog:** an AM lead should be able to fix a colleague's phone or an admin fix a client's name without asking them to log in.
- **Country selector defaults to +966:** the customer base is Saudi; Turkey (Trendyol) and UAE (Noon) users pick theirs once and it is remembered.
- **Phone stored as E.164 + ISO country, never as typed:** so it is dialable, comparable, and can later feed SMS/WhatsApp alerts without cleanup.
- **Non-Nasam assumption respected:** copy never says "Nasam will call you"; it says "so we can reach you". A Salla subscriber's "we" is their own team/organization.

## Heuristics Notes

- **Visibility of system status:** immediate sidebar/greeting update after save, plus a success toast.
- **Match between system and real world:** country flags + dial codes, and each name field in its own script direction.
- **Error prevention:** direction forcing per field, digit normalization, country auto-detect on paste — most errors are prevented before validation runs.
- **User control:** dirty-close guard, Cancel always available, nothing saved until Save.
- **Consistency:** reuses the "Edit user" dialog layout and the read-only-email note that users have already seen.
- **Accessibility:** every input has a visible label (not placeholder-only), errors are associated with fields via `aria-describedby`, the country selector is keyboard-navigable and searchable, contrast follows the existing light/dark themes. Screen readers announce the save toast.
- **Cognitive load:** four fields, one screen, no tabs, helper text explains *why* only where a user might hesitate (names, phone).

## Critique & Risks

- **Users may not fill it.** Mitigation: migration backfills names for the majority; the nudge targets phone specifically; admins can fill gaps for internal staff.
- **Nudge fatigue.** Cap at 3 dismissals, then stop forever. Do not turn this into a modal.
- **Script validation false positives:** names with apostrophes, hyphens, or diacritics ("Al-Otaibi", "محمّد"). Validation must allow punctuation, spaces, and Arabic diacritics; the check is "contains at least one letter of the expected script and no letters of the other script", not "only letters of the expected script".
- **Non-Arabic, non-Latin names** (e.g. a Turkish colleague with "İ", or a Cyrillic name): Latin extended is Latin — accept it in the English field. Anything else is out of scope; the legacy full name still works as a fallback.
- **Phone verification is absent:** a typo silently produces an unreachable number. Acceptable for v1; OTP verification is a natural follow-up once SMS alerts exist.
- **Privacy:** the phone number is personal data. They should be visible only to the user and to admins with user-management rights, not to other users of the same organization by default. Confirm with the existing permissions model.

## Content Needs

**Labels (AR / EN):**
- الملف الشخصي / My profile
- الاسم بالعربية / Name in Arabic
- الاسم بالإنجليزية / Name in English
- البريد الإلكتروني (تسجيل الدخول) / Login email
- رقم الجوال (اختياري) / Phone number (optional)
- الدولة / Country
- حفظ / Save · إلغاء / Cancel

**Helper text:**
- Names: "يُستخدم عندما تكون واجهة المنصة بالعربية" / "Used when the platform is in English"
- Phone: "حتى نتمكن من التواصل معك بسرعة في الحالات الطارئة المتعلقة بمتجرك" / "So we can reach you quickly if something urgent happens with your store"

**Nudge (home page):** "أضف رقم جوالك حتى نتمكن من التواصل معك في الحالات الطارئة · إضافة" / "Add your phone so we can reach you in urgent cases · Add"

**Errors:**
- "الاسم العربي يجب أن يُكتب بحروف عربية" / "Arabic name must be written in Arabic letters"
- "الاسم الإنجليزي يجب أن يُكتب بحروف لاتينية" / "English name must be written in Latin letters"
- "رقم الجوال غير صحيح لهذه الدولة" / "This number is not valid for the selected country"
- "تعذّر الحفظ، حاول مرة أخرى" / "Could not save, please try again"

**Confirmations:**
- "تم حفظ الملف الشخصي" / "Profile saved"
- "تجاهل التغييرات؟" / "Discard changes?"

**Tone:** plain, human, no jargon. "We" means the user's organization, not Nasam specifically.

## Open Questions (for Tarik)

1. **Who can see the phone number?** Proposed: the user themselves + admins with user-management rights. Should org owners see their own staff's numbers?
2. **Should phone become mandatory for Nasam AMs/GCs** after a grace period? Optional for everyone in v1 as requested.
3. **Phone verification (OTP)** — out of scope for v1; flag if you want it now.
4. **Country list:** all countries, or a short list (SA, AE, KW, QA, BH, OM, EG, TR, JO) first with "more" below? Proposed: full list, GCC + Turkey + Egypt pinned at the top.

## Implementation Checklist

- [ ] DB migration: four nullable columns on `users` + backfill script splitting `full_name` by script
- [ ] API: extend `GET /me`, `PATCH /me`, admin `PATCH /users/:id` with validation (script check, libphonenumber, email format)
- [ ] Shared `displayName(user, locale)` helper (backend for emails/reports, frontend for UI) and greeting updated to omit the name segment when empty
- [ ] Frontend: Profile dialog + "My profile" menu item + clickable sidebar name row
- [ ] Frontend: admin "Edit user" dialog gets the same fields
- [ ] Frontend: home-page phone nudge with dismissal cap
- [ ] i18n keys for all labels/errors above (AR + EN)
- [ ] Tests: script validation edge cases (diacritics, hyphens, mixed), phone normalization (leading 0, Arabic digits, pasted +country), displayName fallbacks, greeting with empty name

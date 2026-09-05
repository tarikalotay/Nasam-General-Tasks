# User Profile — UX Touch (FE addition + BE data check)

**Type:** UX touch — an addition to shipped UI (sidebar user menu, home greeting, admin "Edit user" dialog).
**Where it ships:** `Nasam-co/nasam-frontend-v2`. The backend (`Nasam-co/nasam`) is checked only for whether the data fields exist; if they do not, a small schema/API addition is a prerequisite (see "Backend data check").
**Companion doc:** `DISCOVERY.md` in this folder holds the full reasoning, copy, and validation rules. This file is the placement-level design an implementer works from.
**Mockups:** `mockups/` in this folder (rendered PNGs).

> Note on grounding: this session could not read either Nasam-co repository (cross-owner access is blocked from a session started on this repo). The "existing feature" section below is reconstructed from the three screenshots in the request. The implementer must confirm component names and data flow in the frontend session before building; every place that needs confirmation is marked **[verify]**.

---

## 1. Existing feature (what the user sees today)

**Sidebar footer (image 1).** Bottom of the dark-green sidebar shows an avatar initial, the user's name, and their email. Clicking it opens a popover with three things: Appearance (light/dark segmented control), Language (English/العربية segmented control), and a red "تسجيل الخروج / Logout" row. There is no way to view or edit one's own details.

**Home page header (image 3).** Right-to-left layout: brand switcher dropdown ("جميع البراندات"), then a large greeting "مساء الخير يا Tarik" with the date under it, then the "النبض" (Pulse) section. The greeting interpolates the single stored name into an Arabic sentence, so a Latin-script name reads mixed.

**Admin "Edit user" dialog (image 2).** Cream dialog with title "تعديل المستخدم", subtitle "تحديث معلومات وإعدادات المستخدم لـ {email}", a disabled Email field with the note "لا يمكن تغيير البريد الإلكتروني", and a single "الاسم الكامل / Full name" input. Role and other settings follow below **[verify]**.

**Data available to the FE today [verify]:** a current-user object with at least `id`, `email`, `fullName` (or `name`), `role`, and the UI locale from the language toggle. No phone, no per-language names.

---

## 2. The need (from the request)

- Users should be able to open their profile from the main page by clicking their name.
- They can add an **Arabic name**, an **English name**, a **contact email**, and a **phone number with country code**.
- Existing data (full name, login email) stays **mandatory**; the new fields are **optional**.
- Goal 1: stop the mixed-language greeting (image 3).
- Goal 2: have contact details ("contacts") for emergency cases.

---

## 3. Placement

### 3a. Sidebar user menu → add "My profile" as the first row
- **Above:** nothing; it is the first item in the popover.
- **Below:** the existing Appearance section, then Language, then the divider and Logout. The three existing controls do not move.
- Row style matches the Logout row (icon + label), with a user icon. Optional "جديد / New" pill for the first release; remove after a few weeks.
- The name/avatar row in the footer itself also opens the profile dialog (not just the popover). Rationale: "click his name" is the requested entry point and the row already looks clickable.

### 3b. Profile dialog (new)
- Same dialog shell as the admin "Edit user" dialog: cream surface, title + one-line subtitle, close "✕" on the inline-start side, fields stacked, Save primary + Cancel ghost at the bottom **[verify: reuse the same Dialog component]**.
- Field order, top to bottom:
  1. Name in Arabic (`dir="rtl"` forced)
  2. Name in English (`dir="ltr"` forced)
  3. Live preview line: "سيظهر اسمك كالتالي: مساء الخير يا طارق" / "You will appear as: Good evening, Tarik" — rendered with the same greeting function the home page uses, in the current UI locale
  4. Login email (disabled, existing note under it)
  5. Contact email (optional)
  6. Phone: country-code selector + number input (optional)
  7. Save / Cancel
- Width: same as "Edit user" (~520px). Height fits without scrolling on a 768px-tall laptop; on smaller viewports the dialog body scrolls, header and buttons stay fixed.

### 3c. Home greeting → use the localized name
- No new UI. The greeting component calls `displayName(user, locale)` (see DISCOVERY.md) instead of `user.fullName`. When the helper returns empty, the sentence drops the name part: "مساء الخير" / "Good evening".
- **Phone nudge (small addition):** a single-line soft banner directly under the date, only for users with no phone on file. Text + "إضافة / Add" link that opens the profile dialog with the phone field focused + dismiss "✕". Warm cream background, thin border, no icon larger than the text. Hidden once a phone is saved or after 3 dismissals (persist the dismissal count per user, not per device **[verify: where per-user UI prefs are stored]**).
- Placement rationale: it sits between the greeting and Pulse so it reads as part of "about you", not as an alert about the brand.

### 3d. Admin "Edit user" dialog → same fields
- Replace the single "Full name" input with "Name in Arabic" + "Name in English".
- Add Phone and Contact email below the email field, before Role.
- Keep the legacy full name readable somewhere only if the two localized names are both empty (e.g. as placeholder text in the Arabic/English inputs, "Migrated from: {fullName}"), so admins understand what the migration did.

---

## 4. Information

| Item | Level | Notes |
|---|---|---|
| Arabic name, English name | Primary | The reason the user is here. Each in its own script direction. |
| Live greeting preview | Primary | Answers "why two names" without a paragraph of help text. |
| Phone (+country) | Primary | The business's second goal. Helper text explains the emergency purpose. |
| Login email (read-only) | Secondary | Orientation only. |
| Contact email | Secondary | Optional; helper explains it is a fallback channel. |

Data relations: the names feed the sidebar footer, home greeting, admin user list, and any place the user's name is printed (reports, activity logs) **[verify: list the call sites of `fullName`]**. Phone and contact email are shown only in the profile and the admin dialog.

---

## 5. Interactions

- **Defaults:** country selector = saved country, else Saudi Arabia (+966). Name fields prefilled from the backfill migration (see DISCOVERY.md).
- **Validation timing:** on submit; after the first failed submit, per-field on change. Save button is disabled until the form is dirty; it is not disabled by validation (users should be able to click Save and see what is wrong).
- **Script rule:** Arabic field must contain Arabic letters and no Latin letters; English field the reverse. Spaces, hyphens, apostrophes, and Arabic diacritics are allowed. Error copy in DISCOVERY.md.
- **Phone:** libphonenumber (or the library already in the FE **[verify]**) parses against the selected country; pasted "+966…" auto-selects the country; Arabic-Indic digits converted on blur; stored as E.164 + ISO country.
- **Save success:** toast "تم حفظ الملف الشخصي / Profile saved", dialog closes, current-user store is updated (optimistic or refetch) so sidebar + greeting change without reload.
- **Dirty close:** "تجاهل التغييرات؟ / Discard changes?" confirm on ✕, Esc, or overlay click.
- **Keyboard:** Tab order as listed, Enter submits, Esc closes with guard.
- **Match existing patterns:** same input, label, helper, and error styling as the "Edit user" dialog; same toast component; same segmented/pill styles for the "New" tag as used elsewhere **[verify]**.

---

## 6. Edge cases

- **No localized names yet (legacy user):** greeting and sidebar use `fullName`; dialog shows empty localized inputs with the migrated value as placeholder.
- **Only one localized name:** used in both languages rather than showing nothing.
- **Both names empty and `fullName` empty:** greeting drops the name segment; sidebar shows the email.
- **Contact email = login email:** allowed, soft hint, no error.
- **Same phone on two users:** allowed.
- **Extremely long name:** 100-char max per field; sidebar truncates with ellipsis and full name on hover/title.
- **Feature degrades gracefully:** if the BE does not yet return the new fields, the FE treats them as null and everything behaves exactly as today. Ship the FE behind that null-tolerance so it can go out before/with the BE change.

---

## 7. Responsiveness

- **< 640px:** dialog becomes a full-height bottom sheet; header sticky at top, Save/Cancel sticky at bottom, body scrolls. Country selector opens a full-screen searchable list. Phone row stays two columns (selector fixed width, number flexes).
- **Sidebar collapsed / mobile drawer:** the "My profile" row stays first in the popover; the footer row still opens the profile.
- **Home nudge on mobile:** wraps to two lines; "Add" link goes to the end of the text, dismiss stays at the inline-end.

---

## 8. Backend data check (`Nasam-co/nasam`) — do this first

Answer these before building the FE, in the FE/BE session that has repo access:

1. **User entity / table:** does it already have any of `name_ar`, `name_en`, `phone`, `phone_country`, `contact_email` (or similar)? Search for `phone` and `nameAr` / `name_ar` in the user model, migrations, and DTOs. If any exist, reuse them and their validation.
2. **Current-user endpoint** (`GET /me` or `GET /auth/me` **[verify path]**): which fields does it return? The FE needs the five new fields here.
3. **Self-update endpoint:** is there a `PATCH /me` (or `PUT /users/me`)? If only the admin `PATCH /users/:id` exists, a self-scoped update endpoint is required, with the login email excluded from the accepted body.
4. **Admin update DTO:** add the same five fields and validation (script check, libphonenumber, email format).
5. **Identity source:** if names come from an external IdP (Google Workspace, Auth0, Salla OAuth) on every login, make sure the login sync does not overwrite `name_ar` / `name_en` — it should only touch the legacy `fullName`.
6. **Backfill:** one-off script/migration splitting `fullName` into `name_ar` or `name_en` by script (details in DISCOVERY.md). Confirm the migration tooling (Prisma, TypeORM, Knex, raw SQL) **[verify]**.
7. **Locale:** how does the BE know the user's UI language for emails/notifications? If it stores one, `displayName` should be implemented once on the BE too (for email templates) and once on the FE.
8. **Privacy:** who can read phone/contact email via existing user-list endpoints? Restrict to self + admin roles; do not leak to organization-wide user listings.

---

## 9. Frontend implementation map (`Nasam-co/nasam-frontend-v2`) — what to look for

- Sidebar footer / user menu component (renders avatar, name, email, appearance, language, logout).
- Home page header / greeting component (time-of-day greeting + date).
- Admin user management "Edit user" dialog and its form schema.
- Current-user hook/store (`useMe`, `useCurrentUser`, auth context) and the API client for it.
- i18n dictionaries (AR/EN) — add the keys listed in DISCOVERY.md "Content Needs".
- Any existing phone/country input; otherwise add libphonenumber-js (small) plus a country list with AR/EN names.
- Shared `displayName(user, locale)` helper in a utils module; replace direct `fullName` reads.
- Per-user UI preference storage for the nudge dismissal count.

---

## 10. Prompt for the frontend session

Start a new session with `Nasam-co/nasam-frontend-v2` as the source, add `Nasam-co/nasam` for the backend check, and paste:

> Implement the user profile feature described in `tarikalotay/Nasam-General-Tasks` → `docs/discovery/user-profile/UX-TOUCH.md` and `DISCOVERY.md` (branch `claude/user-profile-contact-info-ahup85`; mockups in `mockups/`). First run the "Backend data check" section against `Nasam-co/nasam` and report which fields/endpoints already exist. Then build the FE: "My profile" entry in the sidebar user menu + clickable footer row, the profile dialog (Arabic name, English name, read-only login email, optional contact email, phone with country code), the `displayName(user, locale)` helper wired into the greeting and sidebar, the same fields in the admin Edit-user dialog, and the phone nudge on the home page. Existing full name and login email stay mandatory; all new fields are optional. Match the existing dialog, input, and toast components; add AR/EN i18n keys. If the BE lacks the fields, make the FE null-tolerant and list the exact BE changes needed.

#!/usr/bin/env python3
"""make-eml.py — package the merged sample as a standard .eml message.

The HTML references the five images through Content-IDs and the images travel
inside the file as inline parts, so the .eml opens in Outlook, Apple Mail,
Thunderbird or Gmail (drag into a compose window) with the logo and photos intact.
Run after render.js:  python3 make-eml.py
"""
import re, sys, json
from pathlib import Path
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

ROOT = Path(__file__).resolve().parent
merged = (ROOT / "output" / "email-okwan-sample.html").read_text(encoding="utf-8")
data = json.loads((ROOT / "sample-data.json").read_text(encoding="utf-8"))
seller = data["seller_name"]

# Images referenced by the template -> Content-IDs
cids = {}
def to_cid(m):
    f = m.group(1)
    cids.setdefault(f, f.replace(".", "-") + "@trendyol.email")
    return f'src="cid:{cids[f]}"'
html = re.sub(r'src="assets/([^"]+)"', to_cid, merged)
assert 'src="assets/' not in html

plain = f"""{seller}
افتحوا متجركم على ترينديول
Open your store on Trendyol.

مرحباً فريق {seller}،
أنا طارق، مسؤول تطوير الأعمال في ترينديول. لاحظنا حضوركم القوي في قنوات البيع ونريد منتجاتكم على ترينديول.
للبدء، ردّوا على هذا الإيميل أو راسلوني على واتساب وأرسلوا:
1. رابط متجركم
2. رقم السجل التجاري
سأفتح متجركم وأجهّز منتجاتكم للبيع. يستغرق التسجيل من أسبوع إلى أسبوعين.

Hi {seller} team,
I'm Tarik, Business Development Executive at Trendyol. We saw your strong presence across sales channels, and we want your products on Trendyol.
To start, reply to this email or message me on WhatsApp with:
1. Your store link
2. Your CR number
I'll open your store and get your catalogue live. Onboarding takes 1–2 weeks.

WhatsApp: https://wa.me/{data['sender_phone_e164']}
Email: {data['sender_email']} · {data['sender_phone_display']}

Tarik Alotay
Business Development Executive · Trendyol, Saudi Arabia
"""

msg = EmailMessage()
msg["From"] = f"Tarik Alotay <{data['sender_email']}>"
msg["To"] = "eng.talotay@gmail.com"
msg["Subject"] = f"{seller} × Trendyol: open your store · افتحوا متجركم على ترينديول"
msg["Date"] = formatdate(localtime=True)
msg["Message-ID"] = make_msgid(domain="trendyol.email")
msg["X-Unsent"] = "1"          # Outlook opens the file in compose mode so it can be sent as-is
msg["MIME-Version"] = "1.0"
msg.set_content(plain)
msg.add_alternative(html, subtype="html")
related = msg.get_payload()[1]  # the text/html part becomes multipart/related once images are attached
for f, cid in cids.items():
    p = ROOT / "assets" / f
    sub = "png" if f.endswith(".png") else "jpeg"
    related.add_related(p.read_bytes(), maintype="image", subtype=sub, cid=f"<{cid}>", filename=f, disposition="inline")

out = ROOT / "output" / "email-okwan.eml"
out.write_bytes(bytes(msg))
print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB) with {len(cids)} inline images")

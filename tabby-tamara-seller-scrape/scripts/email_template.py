#!/usr/bin/env python3
"""Render the Nasam-branded recruiting email (Arabic, RTL) from live scrape figures."""
import csv, json, sys

F = "'Tajawal','Segoe UI',Tahoma,Arial,sans-serif"
TEAL, GOLD, CREAM, SAND = "#163e4b", "#a6721c", "#f6f0e5", "#e7dcc8"
GREEN, RED, MUTED, FAINT = "#1e6b45", "#a3341f", "#6b7975", "#96908a"


def stats():
    el = list(csv.DictReader(open("eligible.csv", encoding="utf-8-sig")))
    ne = list(csv.DictReader(open("not_eligible.csv", encoding="utf-8-sig")))
    d = {
        "eligible": len(el),
        "not_eligible": len(ne),
        "total": len(el) + len(ne),
        "email": sum(1 for r in el if r["Emails"]),
        "phone": sum(1 for r in el if r["Phone Numbers"] or r["WhatsApp"]),
        "high": sum(1 for r in el if r["Potential"] == "High"),
        "medium": sum(1 for r in el if r["Potential"] == "Medium"),
        "both": sum(1 for r in el if r["On Tabby"] and r["On Tamara"]),
    }
    ind = {}
    for r in el:
        ind[r["Industry"]] = ind.get(r["Industry"], 0) + 1
    d["top_industries"] = sorted(ind.items(), key=lambda x: -x[1])[:6]
    return d


def card(num, label, sub, color=TEAL):
    return f'''<td width="25%" valign="top" style="padding:5px"><table width="100%" cellpadding="0" cellspacing="0" bgcolor="{CREAM}" style="border:1px solid {SAND};border-radius:12px"><tbody><tr><td align="center" style="padding:13px 6px;font-family:{F}"><div style="font-size:24px;font-weight:800;color:{color}">{num}</div><div style="font-size:11px;color:{MUTED};margin-top:2px">{label}</div><div style="font-size:10.5px;color:{FAINT};margin-top:5px">{sub}</div></td></tr></tbody></table></td>'''


def section(title, note=""):
    n = f'<span style="color:{MUTED};font-weight:400;font-size:12px"> — {note}</span>' if note else ""
    return f'''<div style="font-size:13px;font-weight:800;color:{TEAL};margin-bottom:10px">{title}{n}</div>'''


def box(inner, bg=CREAM, border=SAND):
    return f'''<table dir="rtl" width="100%" cellpadding="0" cellspacing="0" bgcolor="{bg}" style="border:1px solid {border};border-radius:12px"><tbody><tr><td style="padding:14px 16px;line-height:1.85;font-family:{F};font-size:12.5px;color:{TEAL}">{inner}</td></tr></tbody></table>'''


SIGNATURE = f'''<table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;font-family:{F};font-size:14px"><tbody><tr>
<td style="vertical-align:middle;padding:4px 4px 4px 22px" dir="ltr">
  <div style="font-family:'trebuchet ms',sans-serif;font-size:17px;font-weight:bold;color:{TEAL};line-height:1.25;letter-spacing:0.2px">Tarik Alotay</div>
  <div style="font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#6b7975;line-height:1.5;padding-top:1px">[المسمّى الوظيفي]</div>
  <div style="height:9px;line-height:9px;font-size:0px">&nbsp;</div>
  <table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse"><tbody>
  <tr><td style="padding:2px 0 2px 12px;font-family:Arial,Helvetica,sans-serif;font-size:11px;font-weight:bold;color:#87a09a;letter-spacing:0.4px;white-space:nowrap;vertical-align:middle">MOBILE</td><td style="padding:2px 0;font-family:Arial,Helvetica,sans-serif;font-size:13px;color:{TEAL};vertical-align:middle">+966 5X XXX XXXX</td></tr>
  <tr><td style="padding:2px 0 2px 12px;font-family:Arial,Helvetica,sans-serif;font-size:11px;font-weight:bold;color:#87a09a;letter-spacing:0.4px;white-space:nowrap;vertical-align:middle">OFFICE</td><td style="padding:2px 0;font-family:Arial,Helvetica,sans-serif;font-size:13px;color:{TEAL};vertical-align:middle">+966 53 289 4245</td></tr>
  <tr><td style="padding:2px 0 2px 12px;font-family:Arial,Helvetica,sans-serif;font-size:11px;font-weight:bold;color:#87a09a;letter-spacing:0.4px;white-space:nowrap;vertical-align:middle">EMAIL</td><td style="padding:2px 0;font-family:Arial,Helvetica,sans-serif;font-size:13px;color:{TEAL};vertical-align:middle">tarik.alotay@nasam.co</td></tr>
  <tr><td style="padding:2px 0 2px 12px;font-family:Arial,Helvetica,sans-serif;font-size:11px;font-weight:bold;color:#87a09a;letter-spacing:0.4px;white-space:nowrap;vertical-align:middle">WEB</td><td style="padding:2px 0;font-family:Arial,Helvetica,sans-serif;font-size:13px;vertical-align:middle"><a href="https://www.nasam.co/" style="color:{TEAL};text-decoration:none;font-weight:bold;border-bottom:1px solid #d0bfaa;padding-bottom:1px">www.nasam.co</a></td></tr>
  </tbody></table>
</td>
<td style="width:2px;background:{TEAL};font-size:0px;line-height:0">&nbsp;</td>
<td style="vertical-align:middle;padding:4px 22px 4px 4px;font-family:'trebuchet ms',sans-serif;font-size:20px;font-weight:bold;color:{TEAL};letter-spacing:1px">نسم<span style="color:#87a09a"> · </span>NASAM</td>
</tr></tbody></table>'''


def render(d):
    ind_rows = ""
    mx = max(v for _, v in d["top_industries"]) or 1
    for name, cnt in d["top_industries"]:
        pct = round(cnt * 100 / mx)
        ind_rows += f'''<div style="margin-bottom:9px"><table dir="rtl" width="100%" cellpadding="0" cellspacing="0"><tbody><tr><td style="font-size:12.5px;color:{TEAL};font-weight:700;font-family:{F}">{name}</td><td align="left" style="font-size:12.5px;color:{TEAL};font-weight:700;font-family:{F}">{cnt:,}</td></tr></tbody></table><table dir="rtl" width="100%" cellpadding="0" cellspacing="0" style="table-layout:fixed;margin-top:4px"><tbody><tr><td height="10" width="{pct}%" bgcolor="{TEAL}" style="font-size:1px;line-height:1px">&nbsp;</td><td height="10" width="{100-pct}%" bgcolor="{SAND}" style="font-size:1px;line-height:1px">&nbsp;</td></tr></tbody></table></div>'''

    return f'''<div dir="rtl" lang="ar"><table dir="rtl" width="100%" cellpadding="0" cellspacing="0" bgcolor="#e9e0d0" style="font-family:{F}"><tbody><tr><td align="center" style="padding:24px 12px">
<table dir="rtl" width="640" cellpadding="0" cellspacing="0" bgcolor="#fffdf9" style="width:100%;max-width:640px;border-radius:16px;overflow:hidden"><tbody>

<tr><td bgcolor="{GOLD}" align="center" style="padding:8px 20px;font-family:{F}">
  <span style="font-size:11.5px;font-weight:700;color:#ffffff">مقترح داخلي · بناء قاعدة بيانات التجّار وأتمتة الاستقطاب · 18 أغسطس 2026</span>
</td></tr>

<tr><td bgcolor="{TEAL}" style="padding:22px 30px;font-family:{F}">
  <div style="font-size:22px;font-weight:800;color:#f5efe6;line-height:1.4">نستقطب بذكاء لا بجهد — قاعدة {d['total']:,} تاجر جاهزة</div>
  <div style="font-size:12px;color:#e9dcc8;margin-top:8px;line-height:1.7">من دليل تابي وتمارا في السعودية · بيانات تواصل ومعيار أهلية وترتيب حسب الأولوية</div>
</td></tr>

<tr><td style="padding:20px 26px 6px;font-family:{F}">
  {section("١ · الفكرة")}
  {box("فريق المبيعات اليوم يبحث عن العملاء واحداً واحداً. المقترح أن نعكس المعادلة: بدل أن نبحث عن التاجر، نبني <b>قاعدة تجّار جاهزة ومصنّفة ومرتّبة حسب أولوية التواصل</b>، ويأتي دور الفريق في الإقناع والإغلاق فقط.<br><br>تابي وتمارا ينشران دليل متاجرهما للعموم. هذه المتاجر <b>أثبتت أصلاً أنها تبيع أونلاين وتقبل الدفع الآجل</b> — أي أنها تجاوزت أصعب مرحلة، وهي بالضبط الشريحة التي تنضم لنسم بسهولة.<br><br>سحبنا الدليلين بالكامل، ووحّدنا المكرر، واستخرجنا بيانات التواصل من مواقع التجّار أنفسهم، وصنّفنا كل تاجر: مؤهل لنسم أو غير مؤهل ولماذا.")}
</td></tr>

<tr><td style="padding:16px 26px 4px;font-family:{F}">
  {section("٢ · النتيجة", "الملف مرفق")}
  <table dir="rtl" width="100%" cellpadding="0" cellspacing="0"><tbody><tr>
    {card(f"{d['total']:,}", "تاجر بلا تكرار", "تابي + تمارا")}
    {card(f"{d['eligible']:,}", "مؤهل لنسم", f"{round(d['eligible']*100/d['total'])}% من الإجمالي", GREEN)}
    {card(f"{d['email']:,}", "بريد إلكتروني", "مستخرج من موقع التاجر")}
    {card(f"{d['phone']:,}", "جوال / واتساب", "قناة تواصل مباشرة")}
  </tr></tbody></table>
  <div style="font-size:11px;color:{MUTED};margin:9px 5px 0;line-height:1.7">غير المؤهلين ({d['not_eligible']:,}) في ورقة منفصلة مع سبب الاستبعاد لكل صف · {d['both']:,} تاجراً مسجّل في المنصتين معاً — إشارة نضج رقمي أعلى</div>
</td></tr>

<tr><td style="padding:16px 26px 4px;font-family:{F}">
  {section("٣ · الترتيب حسب الأولوية", "مقياس 0-100")}
  {box(f"كل تاجر حصل على <b>درجة أولوية</b> تُرتَّب بها القائمة تنازلياً: موقع يعمل +30 · بريد +25 · جوال أو واتساب +10 · حساب تواصل اجتماعي +10 · مسجّل في المنصتين +10 · متجر أونلاين +10 · أونلاين وفرع معاً +5.<br><br><b style='color:{GREEN}'>{d['high']:,} تاجراً في الفئة العالية</b> (65 فأكثر) — هؤلاء نبدأ بهم غداً، بياناتهم كاملة وقنوات التواصل معهم مفتوحة. و<b>{d['medium']:,}</b> في الفئة المتوسطة.<br><br>المعنى العملي: الفريق لا يفتح ملفاً من 25 ألف صف، بل يبدأ من الأعلى نزولاً — وكل مكالمة تبدأ ببيانات جاهزة لا ببحث.")}
</td></tr>

<tr><td style="padding:16px 26px 4px;font-family:{F}">
  {section("٤ · التوزيع القطاعي", "أكبر ٦ قطاعات بين المؤهلين")}
  {ind_rows}
</td></tr>

<tr><td style="padding:16px 26px 6px;font-family:{F}">
  {section("٥ · الأكبر من ذلك — أكثر من ٣٠ ألف عميل محتمل")}
  {box("لدينا أصلاً <b>أكثر من ٣٠ ألف عميل محتمل</b> من أمازون ونون وترينديول، والآن يُضاف إليها هذا الدليل. المشكلة لم تعد الكمّ — المشكلة أننا نتعامل مع كل اسم بنفس الطريقة اليدوية.<br><br>المقترح: <b>نظام فلترة موحّد</b> يمرّ عليه كل عميل محتمل من أي مصدر، ويرتّبه آلياً حسب القطاع وحجم النشاط ووجود بيانات التواصل ودرجة الجاهزية، ثم يوزّعه على الفريق مع رسالة أولى مناسبة للقطاع.<br><br>وبعدها نختصر مسار الانضمام نفسه: تسجيل أسرع، ربط أسرع، تفعيل أسرع — <b>نستقبل التاجر لا أن نطارده</b>.", "#faf3e4", "#ecd9ac")}
</td></tr>

<tr><td style="padding:16px 26px 6px;font-family:{F}">
  {section("٦ · المطلوب منكم", "قبل اجتماع الثلاثاء")}
  {box(f"""أرجو أن يفكّر كل واحد منكم في السؤال التالي، ونناقشه في الاجتماع:<br><br>
  <b style="color:{GOLD}">كيف نجعل الاستقطاب ذكياً لا شاقّاً؟</b><br><br>
  <div style="padding-right:14px">
  <b>١.</b> ما المعايير التي تجعل التاجر «مستحقاً للاتصال» فعلاً؟ نبني عليها الفلترة.<br>
  <b>٢.</b> ما الذي يمكن أتمتته بالكامل في التواصل الأول — بريد، واتساب، رسالة مخصصة لكل قطاع؟<br>
  <b>٣.</b> أين تضيع أطول مدة في رحلة الانضمام حالياً، وما الذي نحذفه منها؟<br>
  <b>٤.</b> ما القطاع الذي نبدأ به أولاً بحيث نبني قصة نجاح تفتح ما بعدها؟
  </div><br>
  تقرير الأسبوع الماضي يوضّح الحاجة بدقة: <b>١٢٠ عميلاً جديداً</b> قابلها <b>١١ فرصة مؤهلة فقط</b> (٩٪) وصفر عروض موثّقة. الخلل ليس في الكمّ — <b>الاختناق في التأهيل</b>، وهذا بالضبط ما يحلّه نظام الفلترة.""")}
</td></tr>

<tr><td style="padding:14px 26px 10px;border-top:1px solid {SAND};font-family:{F}">
  <div style="font-size:11px;color:{FAINT};line-height:1.8">المصدر: دليل متاجر تابي (tabby.sa/shop) ودليل متاجر تمارا (tamara.co/stores) — السعودية · تاريخ السحب 18 أغسطس 2026 · التكرار مُزال بمطابقة النطاق والاسم · بيانات التواصل مستخرجة من المواقع العامة للتجّار أنفسهم · الملف المرفق: ورقة ملخص + ورقة المؤهلين + ورقة غير المؤهلين</div>
</td></tr>

<tr><td style="padding:4px 26px 24px;font-family:{F}">{SIGNATURE}</td></tr>

</tbody></table>
</td></tr></tbody></table></div>'''


def plain(d):
    return f"""نستقطب بذكاء لا بجهد — قاعدة {d['total']:,} تاجر جاهزة

١ · الفكرة
بدل أن يبحث الفريق عن كل عميل يدوياً، نبني قاعدة تجّار جاهزة ومصنّفة ومرتّبة حسب أولوية التواصل. تابي وتمارا ينشران دليل متاجرهما للعموم، وهذه المتاجر أثبتت أصلاً أنها تبيع أونلاين وتقبل الدفع الآجل — وهي الشريحة التي تنضم لنسم بسهولة.

٢ · النتيجة (الملف مرفق)
- {d['total']:,} تاجر بلا تكرار من تابي وتمارا
- {d['eligible']:,} مؤهل لنسم ({round(d['eligible']*100/d['total'])}%)
- {d['email']:,} بريد إلكتروني مستخرج من مواقع التجّار
- {d['phone']:,} جوال أو واتساب
- {d['not_eligible']:,} غير مؤهل في ورقة منفصلة مع سبب الاستبعاد
- {d['both']:,} تاجراً مسجّل في المنصتين معاً

٣ · الترتيب حسب الأولوية
كل تاجر حصل على درجة أولوية من 100: موقع يعمل +30، بريد +25، جوال/واتساب +10، تواصل اجتماعي +10، المنصتين +10، متجر أونلاين +10، أونلاين وفرع +5.
{d['high']:,} تاجراً في الفئة العالية و{d['medium']:,} في المتوسطة.

٤ · أكثر من ٣٠ ألف عميل محتمل
لدينا أصلاً أكثر من ٣٠ ألف عميل محتمل من أمازون ونون وترينديول. المقترح نظام فلترة موحّد يرتّب كل عميل آلياً حسب القطاع والجاهزية وبيانات التواصل، ثم يوزّعه على الفريق مع رسالة أولى مناسبة — ونختصر مسار الانضمام نفسه.

٥ · المطلوب منكم قبل اجتماع الثلاثاء
كيف نجعل الاستقطاب ذكياً لا شاقّاً؟
١. ما المعايير التي تجعل التاجر مستحقاً للاتصال؟
٢. ما الذي يمكن أتمتته في التواصل الأول؟
٣. أين تضيع أطول مدة في رحلة الانضمام؟
٤. ما القطاع الذي نبدأ به أولاً؟

تقرير الأسبوع الماضي: ١٢٠ عميلاً جديداً قابلها ١١ فرصة مؤهلة (٩٪) وصفر عروض — الاختناق في التأهيل لا في الكمّ.

--
Tarik Alotay
[المسمّى الوظيفي]
MOBILE +966 5X XXX XXXX
OFFICE +966 53 289 4245
EMAIL tarik.alotay@nasam.co
WEB www.nasam.co
نسم · NASAM"""


if __name__ == "__main__":
    d = stats()
    open("email_body.html", "w", encoding="utf-8").write(render(d))
    open("email_body.txt", "w", encoding="utf-8").write(plain(d))
    json.dump(d, open("email_stats.json", "w", encoding="utf-8"), ensure_ascii=False)
    print(json.dumps(d, ensure_ascii=False, indent=1))

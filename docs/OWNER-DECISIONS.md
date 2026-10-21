# Owner decisions — قرارات المالك

These block the website-side work (Phase B) of Issues #21–#24. Agreed by Codex and Claude on 2026-10-21 (see the `CODEX REVIEW` and `AGREED PLAN` comments on each Issue). Record the answer, date and who decided; never record credentials here — this repository is public.

| ID | القرار | الخيارات | يوقف | القرار / التاريخ |
|---|---|---|---|---|
| D-01 | إضافة SEO واحدة متوافقة مع WPML | Yoast SEO + WPML SEO · Rank Math + WPML SEO + String Translation (WPML يذكر مشاكل مفتوحة مع Rank Math منها قيم schema غير مترجمة). التكلفة والتراخيص: يتأكد منها المالك من مواقع الشركات | #22 ثم #21 #23 #24 | PENDING — يُقرَّر بعد جرد #2 لما هو مثبّت فعلًا |
| D-02 | سياسة البيع لكل عائلة منتجات | «عرض سعر فقط» (لا Offer ولا سعر ولا مخزون في schema) · «قابل للشراء» (سعر حقيقي ظاهر بعملة صحيحة يعتمده المالك) | #24 | PENDING |
| D-03 | من يعتمد رموز الطلب (SKU) والصور | اسم مهندس/مسؤول مبيعات يطابق كل منتج ومتغيراته مع رمز `NSL-…` الحقيقي، ويؤكد صلة الصورة وحقوقها. لا نأخذ أول صف من الجدول كـ SKU | #24 | PENDING |
| D-04 | من يطبّق الإعدادات وكيف نصل لـ staging | المالك أو مطوّر الموقع يطبّق على نسخة staging مع نسخة احتياطية مُختبرة. Claude لا يُدخل كلمات سر؛ كود الموقع (إن لزم) في مستودع **خاص** منفصل | #2 وكل ما بعده | PENDING |
| D-05 | اعتماد جدول الترجمة وجدول خريطة الموقع | `tracking/translation-matrix.csv` و`tracking/sitemap-inventory.csv` — عمود `owner_approved` | #21 #23 | PENDING |

## لا يُفعَّل أثناء تركيب إضافة SEO (من مراجعة Codex لـ #22)
- التحويلات التلقائية (auto-redirects)، تغيير الروابط أو قاعدة التصنيفات (slug / category base).
- كتابة محتوى جماعي بالذكاء الاصطناعي، ربط حسابات خارجية، أو ميزات «الفهرسة الفورية».
- إخفاء أرقام إصدارات البرامج (generator) اختياري للحماية فقط — لا يصلح الفهرسة ولا يثبت الأمان.

## ترتيب التنفيذ المتفق عليه
`#2 (جرد + staging)` → `D-01` → `#22` → `#21` → `#23` → `#24`، كل خطوة على staging أولًا، ثم موافقة منفصلة للإنتاج.

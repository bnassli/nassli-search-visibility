# GitHub Setup — لصاحب المشروع (Windows / Claude / ChatGPT)

## ليش ما انرفع المشروع تلقائيًا؟
GitHub integration in the current session cannot create new repositories; it did not expose the website repo. The code can be handed over as a local repository. **Do not upload to an unrelated existing repository.**

## الخطوات
1. افتح https://github.com/new بالحساب الذي تريد أن يمتلك المشروع (حاليًا المستهدف `bnassli`).
2. Repository name: `nassli-search-visibility`. اختر **Private**، واترك خيارات Initialize README و`.gitignore` وLicense غير مفعلة.
3. فك الحزمة محليًا داخل مجلد. افتح PowerShell في هذا المجلد، وشغّل:

```powershell
# Note: ZIP may include an initialized .git directory. If absent, script initializes one.
.\scripts\push-to-github.ps1
```

أو عبر Git Bash:

```bash
bash scripts/push-to-github.sh
```

إن ظهر طلب دخول GitHub عبر المتصفح، أكمله يدويًا؛ **لا ترسل Token أو Password إلى الوكلاء.** إذا كان جهازك يستخدم Git Bash أو PowerShell، تأكد أن `git --version` يعمل قبل الخطوة.

4. راجع الرابط `https://github.com/bnassli/nassli-search-visibility` وأن جميع الملفات موجودة.
5. Settings → Branches / Rulesets: require pull requests, 1 human approval, passing `Quality gate`; prevent force push/direct push `main`.
6. Settings → Collaborators / app access: ensure Claude's GitHub integration and ChatGPT GitHub connection can access **this exact private repository** with appropriate read/write permissions. Some installed GitHub apps need repo-specific approval.
7. افتح Issues وأنشئ المهام من `tracking/ISSUE-BACKLOG.md` يدويًا، أو استخدم `scripts/create-issues.sh` بعد `gh auth login` لتوليدها دون تكرار titles إن لم تكن موجودة.
8. Confirm Actions enabled; manually run `Read-only public website audit` after owner approval for the public read requests.

## كيف يشتغل الوكيلان على نفس المشروع؟
- ChatGPT: راجع `STATUS.md`, Issue محدد، اطلب تعديل فرع وPR. تحقّق أولًا أن اتصال GitHub يسمح برؤية هذا المستودع.
- Claude: في Claude Code افتح/clone نفس المشروع، اقرأ `CLAUDE.md`، افتح issue على فرع وPR.
- كل واحد يراجع عمل الآخر مع موافقة بشرية نهائية. لن يتزامن الذكاء الاصطناعي تلقائيًا بين دردشات مستقلة: **GitHub هو الذاكرة المشتركة**.

## مهم
لا تربط هذا المشروع تلقائيًا بـVercel أو Namecheap أو الاستضافة الحيّة. لا تنشر حتى ننهي جرد بيئة الموقع وتدقيق الأمن والاختبارات.

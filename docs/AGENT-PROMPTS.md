# Ready prompts — انسخ والصق

ترتيب العمل لكل مهمة: **Codex يراجع أولًا ← Claude يراجع ثانيًا ← Claude وحده يعدّل الملفات ← Codex يؤكد ← المالك يدمج.**
علامة الـ Issue (`step-1` … `step-4`) تبيّن دور من.

## إلى Codex — المراجعة الأولى (step 1)

```text
Repository: https://github.com/bnassli/nassli-search-visibility
Read AGENTS.md, STATUS.md and docs/WORKFLOW.md first.
You are the FIRST REVIEWER. Do not edit files, push branches or open PRs.
Take Issue #<N> (label step-1:codex-review). Check its facts against the live site and
official docs, list risks and missing acceptance criteria, and propose an approach.
Post ONE comment on the Issue starting with "CODEX REVIEW", then change the label
from step-1:codex-review to step-2:claude-review.
```

لعدة مهام دفعة واحدة: استبدل السطر `Take Issue #<N>` بـ `Take every open Issue labeled step-1:codex-review, P0 first`.

## إلى Claude — المراجعة الثانية والتنفيذ (step 2 + 3)

```text
راجع تعليق CODEX REVIEW على Issue #<N>، اكتب AGREED PLAN، ثم نفّذ وافتح PR.
```

## إلى Codex — تأكيد الـ PR (step 4)

```text
Repository: https://github.com/bnassli/nassli-search-visibility
Read AGENTS.md. Do not edit files.
Review PR #<P> against the "AGREED PLAN" comment on its Issue. Check the diff, the
test output in the PR, and that no fact was invented. Comment on the PR starting with
"CODEX CONFIRMED" or "CODEX CHANGES REQUESTED" followed by numbered reasons.
```

إذا كان تطبيق Codex مثبتًا على GitHub يمكنك أيضًا كتابة `@codex review` كتعليق على الـ PR.

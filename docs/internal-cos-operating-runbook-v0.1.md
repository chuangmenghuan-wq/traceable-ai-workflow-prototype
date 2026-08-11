# RUNBOOK-001｜COS Operating Runbook v0.1

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal runbook / public-safe  
**Date:** 2026-07-08  
**Mode:** Docs-only / operating runbook  

> 中文定位：這份文件把目前的 Capability Operating System 變成一份可操作的內部手冊。目的不是新增更多概念，而是讓之後遇到研究、回饋、任務、工具、錯誤修正時，都能用同一套流程處理。

---

## 1. Runbook goal

```text
Turn scattered docs into an operating procedure.
```

中文目標：

```text
讓 Future Ability Universe 不只是有文件，而是有一套可以反覆執行的能力作業流程。
```

---

## 2. When to use this runbook

Use this runbook when there is:

```text
- a new user request
- a public feedback signal
- a research finding
- a tool research question
- a repeated workflow pattern
- an error correction lesson
- a validation result
- a possible capability idea
```

Do not use it to justify:

```text
- public posting without review
- main merge without review
- backend/API/storage/login work
- real customer data use
- paid tool/platform action
- production/compliance/security claims
```

---

## 3. Operating flow

```text
1. Capture signal.
2. Identify department owner.
3. Run boundary check.
4. Classify signal.
5. Run repeatability test.
6. Decide capability action.
7. Assign lifecycle state.
8. Validate safe boundary.
9. Choose next safe action.
10. Stop if user approval is required.
```

---

## 4. Step 1 — Capture signal

Signal capture fields:

```text
Signal source:
Signal type:
Summary:
Related project:
Sensitive data present: yes / no
Urgency:
Observed pattern:
```

If sensitive data is present:

```text
Do not store details.
Summarize only at a safe abstract level.
Route to blocked_boundary or user_review_required.
```

---

## 5. Step 2 — Identify department owner

Use this routing:

```text
Workflow safety / safe first test / validation / trace → DEPT-001
Public feedback / comments / reply drafts → DEPT-002
Tool evaluation / pricing / lock-in / vendor risk → DEPT-003
Capability extraction / repeatable pattern → DEPT-004
Demo kit / reviewer story / public-safe packaging → DEPT-005
Registry / lifecycle / gates → COS-Core
```

---

## 6. Step 3 — Boundary check

Ask:

```text
Does this require public action?
Does this require main merge?
Does this require backend/API/storage/login?
Does this require real customer data?
Does this require signup/payment/OAuth?
Does this imply production/compliance/security/legal/privacy claim?
```

If yes:

```text
Stop or route to user_review_required.
```

If no:

```text
Continue as internal docs/report-only.
```

---

## 7. Step 4 — Classify signal

Choose one:

```text
ignore
watch
draft_reply
report_only_summary
backlog_candidate
capability_candidate
registry_update
validation_update
blocked_boundary
user_review_required
```

---

## 8. Step 5 — Repeatability test

Repeatable if:

```text
- the same problem is likely to appear again
- input/process/output can be described
- it fits a department
- it can be validated safely
- allowed and blocked actions can be stated
```

Not repeatable if:

```text
- one-off preference
- platform-specific noise
- unsafe data dependency
- no validation path
- no department owner
```

---

## 9. Step 6 — Decide capability action

| Case | Action |
|---|---|
| Repeatable + safe + defined | registry_update |
| Repeatable but incomplete | backlog_candidate |
| Useful but needs evidence | paused |
| Unsafe now | blocked_boundary |
| Public-facing | user_review_required |
| One-off | ignore / watch |

---

## 10. Step 7 — Assign lifecycle state

Use one:

```text
idea
candidate
drafted
internal-spec
registered
public-safe-demo
validated-synthetic-only
paused
blocked
retired
```

Reminder:

```text
No lifecycle state means production-ready.
No lifecycle state means compliance-ready.
No lifecycle state means client-data-ready.
```

---

## 11. Step 8 — Validate boundary

Run the relevant validation:

```text
Public wording → Prototype Overclaim Risk Register
Department change → Department Draft Safety Validation
Capability change → Registry v0.2 mapping
Public reply → Reply Template Pack + User Review Boundary
Tool research → Tool Research Department boundary
Demo packaging → Demo Kit Department public-use gate
```

---

## 12. Step 9 — Choose next safe action

Allowed next actions:

```text
docs-only update
report-only summary
branch-only registry mapping
paused/backlog classification
internal validation pass
safe reply draft only
```

Blocked without review:

```text
public reply
public post
main merge
public demo change
README positioning change
new platform push
backend/API/storage/login
real customer data
signup/payment/OAuth
```

---

## 13. Step 10 — Stop condition

Stop and ask user approval when:

```text
next step affects public surface
next step merges into main
next step posts/replies publicly
next step requires external account/action
next step uses real/private data
next step changes product maturity claim
```

---

## 14. Example runbook execution

### Case: new research finding

```text
Signal: new research finding about workflow safety tools
Department owner: DEPT-003 Tool Research
Boundary: public-info only
Classification: report_only_summary
Repeatability: maybe
Capability action: backlog_candidate
Lifecycle state: candidate
Next safe action: report-only tool matrix
```

### Case: repeated user says “next step”

```text
Signal: repeated user request for continuous progress
Department owner: COS-Core / DEPT-004
Boundary: no public/main/backend/data actions
Classification: internal operating improvement
Repeatability: yes
Capability action: registry_update / runbook update
Lifecycle state: internal-spec
Next safe action: docs-only internal upgrade until approval boundary
```

### Case: public feedback appears

```text
Signal: public comment
Department owner: DEPT-002 Public Feedback
Boundary: public reply requires review
Classification: draft_reply or capability_candidate
Repeatability: depends
Capability action: candidate/backlog if repeatable
Next safe action: draft reply only; do not post
```

---

## 15. Current runbook result

```text
RUNBOOK-001 result: PASS
Operating flow defined: yes
Department routing defined: yes
Boundary checks defined: yes
Repeatability test defined: yes
Capability action rules defined: yes
Stop conditions defined: yes
No public demo code changed: yes
No backend / AI API added: yes
No real customer data added: yes
Recommended next: update PR summary and validate branch diff
```

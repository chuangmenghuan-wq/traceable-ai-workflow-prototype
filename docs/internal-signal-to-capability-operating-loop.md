# LOOP-001｜Signal-to-Capability Operating Loop

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal operating loop / public-safe  
**Date:** 2026-07-08  
**Mode:** Docs-only / operating model  

> 中文定位：這份文件定義 Future Ability Universe 的核心迴圈：任何公開回饋、研究結果、工具研究、錯誤修正、重複任務，都要先變成 signal，再判斷能否抽象成 Capability，而不是直接變成產品功能或外部承諾。

---

## 1. Core loop

```text
signal
→ intake
→ classify
→ boundary check
→ repeatability test
→ capability candidate extraction
→ validation idea
→ department owner
→ registry decision
→ next safe action
```

中文說明：這是內部升級的心臟。以後不是「看到一個東西就做」，而是先走這條迴圈。

---

## 2. Signal types

Use these signal types:

```text
public_feedback_signal
no_response_signal
research_finding
tool_research_finding
user_request_pattern
workflow_pattern
validation_result
error_correction_lesson
risk_boundary_lesson
copy_clarity_gap
public_demo_gap
internal_system_gap
```

---

## 3. Signal intake fields

Every signal should be summarized with:

```text
Signal ID:
Signal source:
Signal type:
Signal summary:
Observed from:
Sensitive data present: yes / no
Immediate risk: yes / no
Related department:
Related capability:
Timestamp / checkpoint:
```

Do not store:

```text
- private customer details
- credentials
- API keys
- screenshots containing sensitive data
- private company documents
- production exports
```

---

## 4. Classification

Classify each signal into one of these actions:

```text
ignore
watch
draft_reply
backlog_candidate
capability_candidate
registry_update
validation_update
blocked_boundary
user_review_required
```

---

## 5. Boundary check

Before any capability extraction, ask:

```text
Does this require real customer data?
Does this require backend / AI API / storage / login?
Does this require signup, payment, or OAuth?
Does this imply production readiness?
Does this imply legal / privacy / cybersecurity / compliance guarantee?
Does this require public posting or public reply?
Does this require main merge?
```

If yes to any of these:

```text
route = user_review_required or blocked_boundary
```

---

## 6. Repeatability test

A signal can become a capability candidate only when:

```text
- it can be reused across more than one workflow
- it can be described as input → process → output
- it can be validated safely
- it can be owned by a department
- its allowed mode can be stated
- its blocked actions can be stated
```

If unclear:

```text
route = backlog_candidate or watch
```

If unsafe:

```text
route = blocked_boundary
```

---

## 7. Capability candidate extraction

Capability candidate template:

```text
Capability candidate ID:
Candidate name:
Source signal:
Problem solved:
Input:
Process:
Output:
Owner department:
Lifecycle state:
Allowed mode:
Blocked actions:
Validation idea:
Fallback:
Public-safe status:
Registry action:
```

---

## 8. Registry decision rules

| Condition | Registry decision |
|---|---|
| Repeatable + safe + defined | register |
| Useful but incomplete | backlog_candidate |
| Needs public feedback first | paused |
| Requires user approval | user_review_required |
| Requires real data/backend/API now | blocked |
| One-off / irrelevant | ignore |
| Duplicates an existing capability | merge_with_existing |

---

## 9. Department routing

| Signal pattern | Department owner |
|---|---|
| Workflow risk / safe first test / validation / trace | DEPT-001 Workflow Safety |
| Public comments / replies / no-response | DEPT-002 Public Feedback |
| Tool evaluation / vendor / cost / lock-in | DEPT-003 Tool Research |
| Repeated pattern / capability extraction | DEPT-004 Research-to-Capability |
| Demo packaging / reviewer explanation | DEPT-005 Demo Kit |
| Cross-system gate / registry / lifecycle | COS-Core |

---

## 10. Output package

Each loop run should output:

```text
Signal summary:
Classification:
Boundary result:
Repeatability result:
Capability candidate: yes / no
Owner department:
Registry decision:
Validation needed:
User review needed: yes / no
Next safe action:
```

---

## 11. Example loop runs

### Example A — No-response on public post

```text
Signal type: no_response_signal
Classification: watch
Boundary result: safe
Repeatability result: unclear
Capability candidate: no
Owner department: DEPT-002 Public Feedback
Registry decision: no registry update
Next safe action: record in feedback checkpoint, do not rewrite demo yet
```

### Example B — Repeated question: why not ChatGPT?

```text
Signal type: public_feedback_signal
Classification: backlog_candidate
Boundary result: safe
Repeatability result: yes
Capability candidate: yes
Owner department: DEPT-002 / DEPT-004
Registry decision: backlog candidate
Next safe action: keep reply template; do not change demo unless repeated
```

### Example C — Tool looks useful but requires OAuth

```text
Signal type: tool_research_finding
Classification: user_review_required
Boundary result: OAuth required
Repeatability result: maybe
Capability candidate: possible but blocked for adoption
Owner department: DEPT-003 Tool Research
Registry decision: paused / blocked-current-phase
Next safe action: report-only note, no signup or connection
```

### Example D — Risk lesson: prototype may be overclaimed

```text
Signal type: risk_boundary_lesson
Classification: registry_update
Boundary result: safe as internal doc
Repeatability result: yes
Capability candidate: yes
Owner department: COS-Core / DEPT-004
Registry decision: register
Next safe action: maintain overclaim risk guard
```

---

## 12. What this loop prevents

```text
- panic rewriting the demo
- treating no-response as failure
- promising roadmap from one comment
- adding tools too early
- moving from feedback directly to product claims
- mixing internal capability maturity with public SaaS claims
- losing useful lessons as one-off notes
```

---

## 13. Operating boundary

Allowed:

```text
- internal signal classification
- report-only summaries
- docs-only capability candidates
- branch-only registry updates
- paused / blocked classifications
```

Blocked without user review:

```text
- public replies
- public posts
- main merge
- demo changes
- backend/API/storage/login
- real customer data
- signup/payment/OAuth
- production/compliance/security claims
```

---

## 14. Closeout

```text
LOOP-001 result: PASS
Signal-to-capability loop defined: yes
Department routing defined: yes
Boundary gates defined: yes
Registry decision rules defined: yes
No public demo code changed: yes
No backend / AI API added: yes
No real customer data added: yes
Recommended next: VALIDATION-002｜Department Draft Safety Validation Pass
```

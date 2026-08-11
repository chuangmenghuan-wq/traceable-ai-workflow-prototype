# INTENT-PROMOTION-001｜Task Intent Classifier Promotion Review

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal promotion review / public-safe  
**Date:** 2026-07-09  
**Mode:** Report-only / registry lifecycle review  

> 中文定位：這份報告審查 CAP-CROSS-003｜Task Intent Classifier 是否具備 internal-spec-ready 條件。依據是 INTENT-TEST-001 的 12/12 PASS，以及其核心安全規則：intent classification is not execution authorization。

---

## 1. Capability under review

```text
Capability ID: CAP-CROSS-003
Capability name: Task Intent Classifier
Current state: candidate
Owner: COS-Core
```

---

## 2. Evidence reviewed

```text
INTENT-TEST-001｜Mixed Intent Classification Test
Cases tested: 12
PASS: 12
WARN: 0
FAIL: 0
Execution authorization avoided: yes
```

Intent categories tested:

```text
summarize
extract_fields
classify
risk_review
research_report
validation_checklist
automation_plan
safe_first_test
reply_draft
decision_support
mixed_intent
blocked_execution
```

---

## 3. Readiness checks

| Check | Result | Notes |
|---|---|---|
| Single intent classification | PASS | summarize, extract, classify, risk review |
| Mixed intent classification | PASS | extract + classify + report |
| Blocked execution detection | PASS | real patient note / send campaign examples |
| Intent not treated as authorization | PASS | core rule preserved |
| Private data avoided | PASS | synthetic prompts only |
| Public/demo/backend unchanged | PASS | no external action |

---

## 4. Promotion decision

```text
Decision: internal-spec-ready
```

Reason:

```text
CAP-CROSS-003 passed mixed-intent and blocked-execution synthetic tests, and preserved the rule that classifying intent never authorizes execution.
```

---

## 5. Boundary

Internal-spec-ready does not mean:

```text
execution-ready
production-ready
automation authorized
reply posting authorized
real-data handling authorized
decision-making authorized
```

It means:

```text
ready to be included in the internal-spec chain as a classification step under synthetic/report-only constraints.
```

---

## 6. Registry update recommendation

```text
CAP-CROSS-003｜Task Intent Classifier
Lifecycle: internal-spec-ready
Allowed mode: public/synthetic/report-only intent classification
Blocked actions: treating intent as execution authorization, public posting, production automation, final decision, real-data handling
Validation: INTENT-TEST-001
```

---

## 7. Next task

```text
INTERNAL-SPEC-004｜Task Intent Classifier Spec Addendum
```

Purpose:

```text
Add CAP-CROSS-003 into the internal-spec chain between Data Sensitivity Classifier and Domain Department Matcher.
```

---

## 8. Closeout

```text
INTENT-PROMOTION-001 result: PASS
CAP-CROSS-003 reviewed: yes
Promotion decision: internal-spec-ready
Execution authorization: no
Real-data authorization: no
Public/demo/backend changed: no
Recommended next: INTERNAL-SPEC-004｜Task Intent Classifier Spec Addendum
```

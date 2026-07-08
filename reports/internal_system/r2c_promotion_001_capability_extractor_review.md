# R2C-PROMOTION-001｜Capability Candidate Extractor Promotion Review

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal promotion review / public-safe  
**Date:** 2026-07-09  
**Mode:** Report-only / registry lifecycle review  

> 中文定位：這份報告審查 CAP-R2C-001｜Capability Candidate Extractor 是否具備 internal-spec-ready 條件。依據是 EXTRACTOR-RECONCILE-001、REGISTRY-005、R2C-EXTRACTOR-TEST-001，以及 reject rules 測試。

---

## 1. Capability under review

```text
Capability ID: CAP-R2C-001
Capability name: Capability Candidate Extractor
Current state: candidate
Owner: Research-to-Capability Department
```

Historical aliases:

```text
CAP-FBK-005 → alias
CAP-CROSS-010 → alias
```

---

## 2. Evidence reviewed

```text
EXTRACTOR-RECONCILE-001: canonicalized duplicate extractor capabilities
REGISTRY-005: alias map created
R2C-EXTRACTOR-TEST-001: 8 source-type tests, 8 PASS, 0 FAIL
```

Source types tested:

```text
public feedback pattern
domain case pattern
validation warning
router gap
blocked claims audit finding
one-off vague idea
real-data-required idea
tool research pattern
```

---

## 3. Readiness checks

| Check | Result | Notes |
|---|---|---|
| Extracts from repeated public feedback | PASS | source-type tested |
| Extracts from domain case pattern | PASS | source-type tested |
| Extracts from validation warning | PASS | source-type tested |
| Extracts from router gap | PASS | source-type tested |
| Extracts from tool research pattern | PASS | source-type tested |
| Rejects one-off vague idea | PASS | backlog/watch fallback |
| Blocks real-data-required idea | PASS | blocked_current_phase / user_review_required |
| Alias/canonical mapping exists | PASS | REGISTRY-005 |
| No production implementation authorized | PASS | report-only |

---

## 4. Promotion decision

```text
Decision: internal-spec-ready
```

Reason:

```text
CAP-R2C-001 has canonical alias mapping, source-type evidence, reject rules, and safe fallbacks.
```

---

## 5. Boundary

Internal-spec-ready does not mean:

```text
automatic feature implementation
production deployment
public demo change
real data authorization
regulated/professional advice readiness
```

It means:

```text
ready to extract capability candidates in docs/report-only mode and route unsafe ideas to backlog, blocked_current_phase, or user_review_required.
```

---

## 6. Registry update recommendation

```text
CAP-R2C-001｜Capability Candidate Extractor
Lifecycle: internal-spec-ready
Allowed mode: docs/report-only registry extraction
Blocked actions: automatic implementation, production deployment, public claim update, real-data capability promotion without approval
Validation: R2C-EXTRACTOR-TEST-001 + alias map + reject rules
```

---

## 7. Next task

```text
INTERNAL-SPEC-005｜Capability Candidate Extractor Spec Addendum
```

Purpose:

```text
Add CAP-R2C-001 into the internal-spec chain after Domain Gap Detector for capability extraction and registry candidate creation.
```

---

## 8. Closeout

```text
R2C-PROMOTION-001 result: PASS
CAP-R2C-001 reviewed: yes
Promotion decision: internal-spec-ready
Reject rules preserved: yes
Real-data authorization: no
Production promotion: no
Public/demo/backend changed: no
Recommended next: INTERNAL-SPEC-005｜Capability Candidate Extractor Spec Addendum
```

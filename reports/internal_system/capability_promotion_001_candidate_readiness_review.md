# CAPABILITY-PROMOTION-001｜Candidate Promotion Readiness Review

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal promotion review / public-safe  
**Date:** 2026-07-09  
**Mode:** Report-only / registry lifecycle review  

> 中文定位：這份報告檢查 REGISTRY-003 / REGISTRY-004 裡的 CAP-CROSS 候選能力，哪些已經接近可以升到 internal-spec，哪些仍需更多測試。這不是 production promotion，也不代表可以處理真實客戶資料。

---

## 1. Review goal

```text
Decide which candidate capabilities are ready for internal-spec review and which must remain candidate.
```

中文目標：

```text
不是所有 candidate 都一起升級。只有通過足夠 synthetic/public-source 測試、邊界清楚、驗證方式清楚的能力，才可進 internal-spec review。
```

---

## 2. Promotion criteria

A candidate may be marked `internal-spec-ready` when:

```text
- 3+ synthetic/public-source examples exist
- owner department is clear
- input/process/output is clear
- allowed mode is clear
- blocked actions are clear
- validation method is clear
- fallback behavior is clear
- no real-data or production authorization is implied
```

If not:

```text
remain candidate
```

---

## 3. Capability readiness table

| Capability | Current state | Test result | Readiness | Decision |
|---|---|---|---|---|
| CAP-CROSS-001 Domain Intake Classifier | candidate | PASS | high | internal-spec-ready |
| CAP-CROSS-002 Data Sensitivity Classifier | candidate | PASS | high | internal-spec-ready |
| CAP-CROSS-003 Task Intent Classifier | candidate | PASS | medium | remain candidate |
| CAP-CROSS-004 Domain Department Matcher | candidate | PASS | high | internal-spec-ready |
| CAP-CROSS-005 Domain Validation Pack Selector | candidate | WARN | medium | remain candidate |
| CAP-CROSS-006 Human Review Gate Builder | candidate | PASS | high | internal-spec-ready |
| CAP-CROSS-007 Blocked Claims Detector | candidate | WARN | medium | remain candidate |
| CAP-CROSS-008 Multi-Department Routing Resolver | candidate | WARN | medium | remain candidate |
| CAP-CROSS-009 Safe First Test Generator | candidate | PASS | high | internal-spec-ready |
| CAP-R2C-001 Capability Candidate Extractor | candidate | WARN/merged | medium | remain candidate |
| CAP-CROSS-011 Domain Report Output Builder | candidate | PASS | high | internal-spec-ready |
| CAP-CROSS-012 Domain Gap Detector | candidate | PASS | high | internal-spec-ready |
| CAP-CROSS-013 Routing Coordinator | candidate | newly added | low-medium | remain candidate |

---

## 4. Internal-spec-ready list

Ready for internal-spec draft:

```text
CAP-CROSS-001｜Domain Intake Classifier
CAP-CROSS-002｜Data Sensitivity Classifier
CAP-CROSS-004｜Domain Department Matcher
CAP-CROSS-006｜Human Review Gate Builder
CAP-CROSS-009｜Safe First Test Generator
CAP-CROSS-011｜Domain Report Output Builder
CAP-CROSS-012｜Domain Gap Detector
```

Reason:

```text
These have clear input/process/output, useful synthetic/public-source evidence, clear owner, and safe fallback.
```

---

## 5. Remain candidate list

Remain candidate:

```text
CAP-CROSS-003｜Task Intent Classifier
CAP-CROSS-005｜Domain Validation Pack Selector
CAP-CROSS-007｜Blocked Claims Detector
CAP-CROSS-008｜Multi-Department Routing Resolver
CAP-R2C-001｜Capability Candidate Extractor
CAP-CROSS-013｜Routing Coordinator
```

Reason:

```text
They are useful but need more tests, stronger libraries, deduplication, or mixed-domain evidence before internal-spec promotion.
```

---

## 6. Promotion boundary

Internal-spec-ready does not mean:

```text
production-ready
customer-data-ready
compliance-ready
security-ready
public-demo-ready
```

It means only:

```text
ready to write a stronger internal spec after user-safe validation, still docs/report-only.
```

---

## 7. Next internal task

Recommended next:

```text
INTERNAL-SPEC-001｜Cross-Industry Core Capability Spec Draft
```

Purpose:

```text
Create internal-spec draft for the 7 ready CAP-CROSS capabilities while keeping all real-data/production/public actions blocked.
```

---

## 8. Closeout

```text
CAPABILITY-PROMOTION-001 result: PASS
Capabilities reviewed: 13
Internal-spec-ready: 7
Remain candidate: 6
Production promotion: no
Real-data authorization: no
Public/demo/backend changed: no
Recommended next: INTERNAL-SPEC-001｜Cross-Industry Core Capability Spec Draft
```

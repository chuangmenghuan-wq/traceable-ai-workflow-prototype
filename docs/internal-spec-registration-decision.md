# INTERNAL-SPEC-PROMOTION-002｜Internal Spec Registration Decision

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal registry decision / public-safe  
**Date:** 2026-07-09  
**Mode:** Docs-only / lifecycle registration  

> 中文定位：這份文件根據 CAPABILITY-CHAIN-AUDIT-001 的結果，將 7 個核心 CAP-CROSS 能力從 `internal-spec draft` 登記為 `internal-spec registered`。這不是 production promotion，不代表可以處理真實資料，也不代表可以公開宣稱產品成熟。

---

## 1. Registration basis

Evidence used:

```text
SPEC-TEST-001 Retail / marketing chain test
SPEC-TEST-002 Manufacturing operations chain test
SPEC-TEST-003 Insurance claims chain test
SPEC-TEST-004 Legal risk chain test
SPEC-TEST-005 Healthcare workflow chain test
SPEC-TEST-006 Education / student data chain test
SPEC-CHAIN-SUMMARY-001 Cross-domain summary
SPEC-CHAIN-SUMMARY-002 High-risk domain summary
CAPABILITY-CHAIN-AUDIT-001 Six-domain audit
```

Audit result:

```text
Domains audited: 6
Total chain steps audited: 42
PASS: 42
FAIL: 0
Boundary packs generated: 6
Critical safety issue: none
```

---

## 2. Registered capabilities

The following capabilities are now registered as internal-spec:

```text
CAP-CROSS-001｜Domain Intake Classifier
CAP-CROSS-002｜Data Sensitivity Classifier
CAP-CROSS-004｜Domain Department Matcher
CAP-CROSS-006｜Human Review Gate Builder
CAP-CROSS-009｜Safe First Test Generator
CAP-CROSS-011｜Domain Report Output Builder
CAP-CROSS-012｜Domain Gap Detector
```

Lifecycle state:

```text
internal-spec registered
```

Allowed mode:

```text
public-source / synthetic / report-only / docs-only
```

---

## 3. Not promoted yet

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
These need more targeted tests, stronger libraries, unknown/multi-pack stress tests, extractor tests, or mixed-domain coordinator evidence.
```

---

## 4. Strict boundary

Internal-spec registered does not mean:

```text
production-ready
real-data-ready
customer-data-ready
compliance-ready
security-ready
legal/medical/financial advice-ready
public-demo-ready
```

It only means:

```text
The capability is specified, repeatedly synthetic-tested, and allowed for internal public/synthetic/report-only workflows.
```

---

## 5. Required boundary packs

Current active internal boundary packs:

```text
RETAIL-DATA-BOUNDARY-001
MANUFACTURING-BOUNDARY-001
INSURANCE-BOUNDARY-001
LEGAL-BOUNDARY-001
HEALTHCARE-BOUNDARY-001
EDUCATION-BOUNDARY-001
```

These must be used whenever the corresponding domain appears.

---

## 6. Operating chain now registered

Registered chain:

```text
Input case
→ CAP-CROSS-001 Domain Intake Classifier
→ CAP-CROSS-002 Data Sensitivity Classifier
→ CAP-CROSS-004 Domain Department Matcher
→ CAP-CROSS-006 Human Review Gate Builder
→ CAP-CROSS-009 Safe First Test Generator
→ CAP-CROSS-011 Domain Report Output Builder
→ CAP-CROSS-012 Domain Gap Detector
```

---

## 7. Failure / fallback rule

If any chain step is uncertain:

```text
use UNKNOWN-DOMAIN-001
or route to user_review_required
or mark blocked_current_phase
```

Never:

```text
force a domain
skip sensitivity classification
skip human review for high-risk domains
recommend production execution
claim professional or compliance readiness
```

---

## 8. Registry decision

```text
REGISTRY DECISION: ACCEPTED FOR INTERNAL-SPEC REGISTRATION
Scope: synthetic / public-source / report-only only
Production scope: blocked
Real-data scope: blocked
Public-demo scope: unchanged
Main merge: user approval required
```

---

## 9. Next internal task

Recommended next:

```text
CAPABILITY-GAP-BACKLOG-001｜Remaining Candidate Capability Gap Backlog
```

Purpose:

```text
Prioritize the 6 remaining candidate capabilities and define the next tests needed for each.
```

---

## 10. Closeout

```text
INTERNAL-SPEC-PROMOTION-002 result: PASS
Capabilities registered internal-spec: 7
Capabilities remaining candidate: 6
Production promotion: no
Real-data authorization: no
Public/demo/backend changed: no
Recommended next: CAPABILITY-GAP-BACKLOG-001｜Remaining Candidate Capability Gap Backlog
```

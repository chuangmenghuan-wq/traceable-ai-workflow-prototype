# CAPABILITY-GAP-BACKLOG-001｜Remaining Candidate Capability Gap Backlog

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal backlog report / public-safe  
**Date:** 2026-07-09  
**Mode:** Report-only / planning backlog  

> 中文定位：這份報告整理 INTERNAL-SPEC-PROMOTION-002 後仍留在 candidate 狀態的 6 個能力。目的不是繼續泛用文件擴張，而是明確列出每個能力缺什麼測試、下一步該怎麼補。

---

## 1. Backlog scope

Remaining candidate capabilities:

```text
CAP-CROSS-003｜Task Intent Classifier
CAP-CROSS-005｜Domain Validation Pack Selector
CAP-CROSS-007｜Blocked Claims Detector
CAP-CROSS-008｜Multi-Department Routing Resolver
CAP-R2C-001｜Capability Candidate Extractor
CAP-CROSS-013｜Routing Coordinator
```

---

## 2. Gap table

| Capability | Gap | Next safe test | Priority |
|---|---|---|---:|
| CAP-CROSS-003 Task Intent Classifier | needs mixed-intent tests | INTENT-TEST-001 | P1 |
| CAP-CROSS-005 Domain Validation Pack Selector | needs unknown + multi-pack selector stress test | VALIDATION-SELECTOR-TEST-001 | P0 |
| CAP-CROSS-007 Blocked Claims Detector | needs phrase/pattern detection tests | CLAIMS-DETECTOR-TEST-001 | P0 |
| CAP-CROSS-008 Multi-Department Routing Resolver | needs more complex mixed-domain test cases | MIXED-ROUTING-TEST-002 | P1 |
| CAP-R2C-001 Capability Candidate Extractor | needs extractor-specific tests across source types | R2C-EXTRACTOR-TEST-001 | P1 |
| CAP-CROSS-013 Routing Coordinator | needs 3+ coordinator tests with conflict resolution | COORDINATOR-TEST-001 | P1 |

---

## 3. P0 tests

### VALIDATION-SELECTOR-TEST-001

Purpose:

```text
Test whether Domain Validation Pack Selector can choose the right pack, fallback pack, or multi-pack combination.
```

Required cases:

```text
- known single domain
- unknown domain
- mixed healthcare + insurance
- retail + education/minors
- legal + logistics/compliance
```

Expected result:

```text
select correct pack or safe fallback without forcing wrong domain
```

---

### CLAIMS-DETECTOR-TEST-001

Purpose:

```text
Test whether Blocked Claims Detector can flag unsafe maturity, compliance, legal, medical, financial, security, and automation claims.
```

Required cases:

```text
- production-ready overclaim
- compliance-ready overclaim
- safe for customer data overclaim
- medical advice claim
- legal advice claim
- fully automated / no human needed claim
```

Expected result:

```text
flag unsafe claim and propose safer framing
```

---

## 4. P1 tests

```text
INTENT-TEST-001｜Mixed Intent Classification Test
MIXED-ROUTING-TEST-002｜Complex Mixed-Domain Routing Test
R2C-EXTRACTOR-TEST-001｜Capability Extractor Source-Type Test
COORDINATOR-TEST-001｜Routing Coordinator Conflict Test
```

---

## 5. Safety boundary

All tests must remain:

```text
synthetic-only
report-only
docs-only
no real private data
no production action
no public/demo/backend change
```

---

## 6. Recommended execution order

```text
1. VALIDATION-SELECTOR-TEST-001
2. CLAIMS-DETECTOR-TEST-001
3. INTENT-TEST-001
4. MIXED-ROUTING-TEST-002
5. R2C-EXTRACTOR-TEST-001
6. COORDINATOR-TEST-001
```

Reason:

```text
Validation pack selection and blocked claims detection are safety-critical. They should be strengthened before broader promotion.
```

---

## 7. Closeout

```text
CAPABILITY-GAP-BACKLOG-001 result: PASS
Remaining candidate capabilities listed: 6
P0 tests identified: 2
P1 tests identified: 4
No private data used: yes
No public/demo/backend changed: yes
Recommended next: VALIDATION-SELECTOR-TEST-001｜Domain Validation Pack Selector Stress Test
```

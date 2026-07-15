# REGISTRY-004｜Routing Coordinator Capability Extension

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal registry extension / public-safe  
**Date:** 2026-07-09  
**Mode:** Docs-only / capability registry extension  

> 中文定位：這份文件把 ROUTING-COORDINATOR-001 發現的新能力登記為 CAP-CROSS-013。當一個任務涉及多個部門、風險、validation packs 時，Routing Coordinator 負責統一輸出與衝突處理。

---

## 1. New capability

```text
Capability ID: CAP-CROSS-013
Capability name: Routing Coordinator
Owner: COS-Core / Workflow Safety Department
Lifecycle state: candidate
Allowed mode: docs/report-only coordination
Blocked actions: production execution, real private data approval, overriding high-risk boundary
Registry decision: register candidate
```

---

## 2. Problem solved

```text
Multi-department routing can create conflicting outputs and unclear ownership.
```

CAP-CROSS-013 solves this by:

```text
- selecting coordinator
- merging department outputs
- applying highest-risk-boundary rule
- preserving human review gates
- producing one final safe output
```

---

## 3. Input / process / output

Input:

```text
case summary
detected domains
lead department
supporting departments
validation packs
risk boundaries
conflicts
```

Process:

```text
1. Confirm lead department.
2. Assign coordinator.
3. Apply highest-risk-boundary rule.
4. Resolve department conflicts.
5. Merge outputs into one report.
6. Mark blocked actions.
7. Produce next safe step.
```

Output:

```text
coordinated routing report
conflict resolution note
human review map
final safe output recommendation
```

---

## 4. Validation method

CAP-CROSS-013 should be validated by:

```text
- mixed-domain synthetic test cases
- conflict resolution examples
- human review gate preservation
- blocked action preservation
- no real-data or production authorization
```

---

## 5. Relation to existing capabilities

CAP-CROSS-013 supports:

```text
CAP-CROSS-004 Domain Department Matcher
CAP-CROSS-005 Domain Validation Pack Selector
CAP-CROSS-006 Human Review Gate Builder
CAP-CROSS-008 Multi-Department Routing Resolver
CAP-CROSS-011 Domain Report Output Builder
CAP-CROSS-012 Domain Gap Detector
```

---

## 6. Promotion rule

May move to internal-spec when:

```text
- 3+ mixed-domain synthetic tests PASS
- highest-risk-boundary is preserved
- coordinator output is complete
- no unsafe authorization appears
```

Remain candidate if:

```text
- conflict resolution is unclear
- validation packs disagree
- final owner cannot be selected
```

Blocked if:

```text
- it attempts to approve real sensitive data
- it bypasses human review
- it authorizes production execution
```

---

## 7. Closeout

```text
REGISTRY-004 result: PASS
CAP-CROSS-013 registered as candidate: yes
Owner mapped: yes
Allowed/blocked modes mapped: yes
Validation method mapped: yes
No public demo code changed: yes
No backend / AI API added: yes
No real customer data added: yes
Recommended next: update PR summary and validate branch diff
```

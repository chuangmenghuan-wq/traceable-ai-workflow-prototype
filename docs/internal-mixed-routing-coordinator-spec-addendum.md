# INTERNAL-SPEC-003｜Mixed Routing and Coordinator Spec Addendum

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal-spec addendum / public-safe  
**Date:** 2026-07-09  
**Mode:** Docs-only / internal capability spec addendum  

> 中文定位：這份文件把 CAP-CROSS-008｜Multi-Department Routing Resolver 與 CAP-CROSS-013｜Routing Coordinator 加入 internal-spec 能力鏈。這讓 COS 可以處理混合領域、多部門、多 boundary packs 的案例，並由 coordinator 套用最高風險邊界。

---

## 1. Capabilities added

```text
CAP-CROSS-008｜Multi-Department Routing Resolver
Lifecycle state: internal-spec-ready / internal-spec addendum
Owner: COS-Core / Workflow Safety Department
Allowed mode: public/synthetic/report-only mixed routing

CAP-CROSS-013｜Routing Coordinator
Lifecycle state: internal-spec-ready / internal-spec addendum
Owner: COS-Core / Workflow Safety Department
Allowed mode: public/synthetic/report-only coordination
```

---

## 2. Purpose

```text
Support mixed-domain cases where one task requires multiple departments, multiple boundary packs, and conflict resolution.
```

中文目的：

```text
真實任務常常不是單一產業。這兩個能力讓系統能處理跨領域、跨部門、跨風險的 synthetic/report-only 案例。
```

---

## 3. Multi-Department Routing Resolver

### Input

```text
detected domains
data sensitivity
task intent if available
possible boundary packs
required human review roles
```

### Process

```text
1. Identify whether the case is single-domain or mixed-domain.
2. Select lead department.
3. Select supporting departments.
4. Identify required boundary packs.
5. Identify highest-risk boundary.
6. Route to Routing Coordinator if 3+ departments or conflict exists.
```

### Output

```text
Lead department:
Supporting departments:
Mixed-domain: yes / no
Boundary packs required:
Highest-risk boundary:
Coordinator required: yes / no
```

---

## 4. Routing Coordinator

### Input

```text
lead department
supporting departments
boundary packs
conflicting recommendations
human review gates
blocked outputs
```

### Process

```text
1. Confirm coordinator owner.
2. Apply highest-risk-boundary wins rule.
3. Resolve department conflicts.
4. Preserve human review gates.
5. Remove unsafe or overclaiming recommendations.
6. Produce one coordinated final report route.
```

### Output

```text
Coordinator:
Conflict resolution:
Final boundary decision:
Human review map:
Blocked outputs:
Final safe output type:
```

---

## 5. Updated operating chain

Full internal-spec chain now:

```text
Input case
→ CAP-CROSS-001 Domain Intake Classifier
→ CAP-CROSS-002 Data Sensitivity Classifier
→ CAP-CROSS-003 Task Intent Classifier if needed
→ CAP-CROSS-004 Domain Department Matcher
→ CAP-CROSS-005 Domain Validation Pack Selector
→ CAP-CROSS-008 Multi-Department Routing Resolver if mixed-domain
→ CAP-CROSS-013 Routing Coordinator if conflict / 3+ departments
→ CAP-CROSS-006 Human Review Gate Builder
→ CAP-CROSS-009 Safe First Test Generator
→ CAP-CROSS-011 Domain Report Output Builder
→ CAP-CROSS-012 Domain Gap Detector
```

Note:

```text
CAP-CROSS-003 remains candidate unless separately promoted. It may be used cautiously but is not yet registered internal-spec.
```

---

## 6. Validation evidence

```text
MIXED-ROUTING-TEST-001
MIXED-ROUTING-TEST-002
COORDINATOR-TEST-001
COORDINATOR-PROMOTION-001
REPORT-TEMPLATE-001
```

---

## 7. Failure handling

If mixed routing or coordination is uncertain:

```text
Workflow Safety Department leads
highest-risk boundary wins
use unknown-domain fallback if needed
mark user_review_required if real/private data appears
mark blocked_current_phase if production/professional-advice risk appears
```

Never:

```text
override high-risk boundary for convenience
skip human review gate
allow public/demo/backend/production action
claim real-data readiness
claim regulated/professional advice readiness
```

---

## 8. Closeout

```text
INTERNAL-SPEC-003 result: PASS
CAP-CROSS-008 added to internal-spec chain: yes
CAP-CROSS-013 added to internal-spec chain: yes
Mixed-domain route defined: yes
Coordinator conflict rule defined: yes
Real-data authorization: no
Production promotion: no
Public/demo/backend changed: no
Recommended next: INTERNAL-SPEC-CHAIN-002｜Full Chain Registration Summary
```

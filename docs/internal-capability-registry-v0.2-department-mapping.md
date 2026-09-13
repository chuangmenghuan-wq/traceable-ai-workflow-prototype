# REGISTRY-002｜Capability Registry v0.2 Department Mapping

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal registry upgrade / public-safe  
**Date:** 2026-07-08  
**Mode:** Docs-only / registry mapping  

> 中文定位：這份文件把 Capability Registry v0.1 升級成 v0.2 的「部門映射版」。重點不是新增更多能力，而是讓每個能力知道：歸哪個 Department、目前 lifecycle state、允許模式、禁止行為、驗證方式與下一步。

---

## 1. Upgrade goal

```text
Capability Registry v0.1 = list of capabilities.
Capability Registry v0.2 = capabilities mapped to departments, states, validation, and boundaries.
```

中文說明：v0.2 的目標是讓能力庫從「清單」變成「可管理系統」。

---

## 2. Registry v0.2 schema

Each capability should include:

```text
Capability ID:
Capability name:
Owner department:
Lifecycle state:
Surface:
Problem solved:
Input:
Process:
Output:
Allowed mode:
Blocked actions:
Validation method:
Fallback / rollback:
Public-safe status:
Next action:
Registry decision:
```

---

## 3. Department owner model

Use these owner departments:

```text
DEPT-001 Workflow Safety Department
DEPT-002 Public Feedback Department
DEPT-003 Tool Research Department
DEPT-004 Research-to-Capability Department
DEPT-005 Demo Kit Department
COS-Core Capability Operating System Core
```

---

## 4. Registry v0.2 mapping table

| Capability ID | Capability | Owner department | Lifecycle state | Allowed mode | Public-safe | Registry decision |
|---|---|---|---|---|---:|---|
| CAP-PUB-001 | Workflow Risk Preview | DEPT-001 | public-safe-demo | browser-only / synthetic-only | yes | keep active |
| CAP-PUB-002 | Safe First Test Planner | DEPT-001 | public-safe-demo | browser-only / synthetic-only | yes | keep active |
| CAP-PUB-003 | Human Review Gate Planner | DEPT-001 | public-safe-demo | browser-only / synthetic-only | yes | keep active |
| CAP-PUB-004 | Validation Checklist Builder | DEPT-001 | public-safe-demo | browser-only / synthetic-only | yes | keep active |
| CAP-PUB-005 | Trace Note Generator | DEPT-001 | public-safe-demo | browser-only / synthetic-only | yes | keep active |
| CAP-FBK-001 | Public Feedback Intake | DEPT-002 | internal-spec | report-only | conditional | keep internal |
| CAP-FBK-002 | Feedback Classifier | DEPT-002 | internal-spec | report-only | conditional | keep internal |
| CAP-FBK-003 | Reply Strategy Generator | DEPT-002 | internal-spec | draft-only | conditional | keep internal |
| CAP-FBK-004 | Internal Action Router | DEPT-002 | internal-spec | report-only | conditional | keep internal |
| CAP-FBK-005 | Capability Candidate Extractor | DEPT-004 | internal-spec | report-only | conditional | keep internal |
| CAP-COS-001 | Capability Registry Maintainer | COS-Core / DEPT-004 | registered | docs-only | conditional | upgrade to v0.2 |
| CAP-COS-002 | User Review Boundary Gate | COS-Core | internal-spec | gate / docs-only | yes | keep active |
| CAP-COS-003 | Public-Safe Boundary Guard | COS-Core | internal-spec | gate / docs-only | yes | keep active |
| CAP-CAND-001 | Copy / Export Review Note | DEPT-005 / DEPT-001 | paused | none yet | possible | wait for feedback |
| CAP-CAND-002 | Synthetic Use Case Queue | DEPT-001 / DEPT-005 | paused | docs-only later | yes | wait for feedback |
| CAP-CAND-003 | AI Tool Candidate Evaluation | DEPT-003 | internal-spec | report-only | yes | ready for report-only task |
| CAP-CAND-004 | AI Department Template | COS-Core | internal-spec | docs-only | yes | implemented |
| CAP-CAND-005 | Public-Safe Demo Kit Outline | DEPT-005 | paused | internal outline only | yes | wait for feedback |
| CAP-CAND-006 | Controlled Client Pilot Boundary | COS-Core / DEPT-001 | blocked | none | no | block current phase |

---

## 5. Capability detail cards

### CAP-PUB-001｜Workflow Risk Preview

```text
Owner department: DEPT-001 Workflow Safety Department
Lifecycle state: public-safe-demo
Allowed mode: browser-only / synthetic-only
Blocked actions: real data, production scoring, compliance/security/legal claim
Validation method: public-safe boundary guard + docs safety checklist
Next action: keep active; improve only after feedback signal
```

### CAP-PUB-002｜Safe First Test Planner

```text
Owner department: DEPT-001 Workflow Safety Department
Lifecycle state: public-safe-demo
Allowed mode: browser-only / synthetic-only
Blocked actions: production pilot, API integration, real-data testing
Validation method: safe-first-test language check
Next action: keep active; collect clarity feedback
```

### CAP-PUB-003｜Human Review Gate Planner

```text
Owner department: DEPT-001 Workflow Safety Department
Lifecycle state: public-safe-demo
Allowed mode: browser-only / synthetic-only
Blocked actions: removing human review, auto-approval claims
Validation method: user review boundary gate
Next action: keep active
```

### CAP-PUB-004｜Validation Checklist Builder

```text
Owner department: DEPT-001 Workflow Safety Department
Lifecycle state: public-safe-demo
Allowed mode: starter checklist only
Blocked actions: certification, formal audit, compliance validation claim
Validation method: docs safety validation checklist
Next action: keep active; avoid overclaim
```

### CAP-PUB-005｜Trace Note Generator

```text
Owner department: DEPT-001 Workflow Safety Department
Lifecycle state: public-safe-demo
Allowed mode: explanatory trace note only
Blocked actions: legal/audit evidence claim
Validation method: prototype overclaim risk register
Next action: keep active
```

---

## 6. Internal capability routing

### Feedback capabilities

```text
CAP-FBK-001 to CAP-FBK-004 belong to DEPT-002 Public Feedback Department.
They are draft/report-only and cannot publish publicly without user review.
```

### Capability extraction capability

```text
CAP-FBK-005 is owned by DEPT-004 Research-to-Capability Department because its main value is converting repeated signals into reusable capabilities.
```

### COS core gates

```text
CAP-COS-001 to CAP-COS-003 belong to COS-Core, with DEPT-004 support for registry updates.
```

---

## 7. Blocked or paused capabilities

Paused:

```text
CAP-CAND-001 Copy / Export Review Note
CAP-CAND-002 Synthetic Use Case Queue
CAP-CAND-005 Public-Safe Demo Kit Outline
```

Reason:

```text
Useful, but should wait for feedback evidence before changing demo or public packaging.
```

Blocked:

```text
CAP-CAND-006 Controlled Client Pilot Boundary
```

Reason:

```text
Too early. Real client data, pilot boundary, privacy/security/legal review, and operational commitments are outside the current phase.
```

---

## 8. Registry update rules

Allowed without user review:

```text
- docs-only registry mapping
- branch-only capability classification
- lifecycle state correction
- internal owner department mapping
- blocked / paused classification
```

Requires user review:

```text
- public demo changes
- public positioning changes
- main merge
- client-data capability promotion
- backend/API/storage/login capability promotion
- production/compliance/security maturity claims
```

---

## 9. v0.2 result

```text
REGISTRY-002 result: PASS
Department ownership mapped: yes
Lifecycle states mapped: yes
Allowed modes mapped: yes
Blocked actions mapped: yes
Public-safe status mapped: yes
No public demo code changed: yes
No backend / AI API added: yes
No real customer data added: yes
Recommended next: LOOP-001｜Signal-to-Capability Operating Loop
```

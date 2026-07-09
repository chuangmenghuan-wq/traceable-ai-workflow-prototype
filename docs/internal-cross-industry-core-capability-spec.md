# INTERNAL-SPEC-001｜Cross-Industry Core Capability Spec Draft

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal-spec draft / public-safe  
**Date:** 2026-07-09  
**Mode:** Docs-only / internal capability spec  

> 中文定位：這份文件把 CAPABILITY-PROMOTION-001 判定為 internal-spec-ready 的 7 個 CAP-CROSS 能力寫成第一版內部規格。這些能力仍只限 public/synthetic/report-only，不代表可處理真實客戶資料或 production workflow。

---

## 1. Scope

Internal-spec draft covers:

```text
CAP-CROSS-001｜Domain Intake Classifier
CAP-CROSS-002｜Data Sensitivity Classifier
CAP-CROSS-004｜Domain Department Matcher
CAP-CROSS-006｜Human Review Gate Builder
CAP-CROSS-009｜Safe First Test Generator
CAP-CROSS-011｜Domain Report Output Builder
CAP-CROSS-012｜Domain Gap Detector
```

Not included yet:

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
These remain candidate until more tests or stronger libraries exist.
```

---

## 2. Common boundary

All included capabilities share this boundary:

```text
Allowed mode: public-source / synthetic / report-only / docs-only
Blocked: real customer data, private company data, regulated records, backend/API/storage/login, production execution, public posting, compliance/security/legal/medical/financial guarantee
```

---

## 3. CAP-CROSS-001｜Domain Intake Classifier

### Purpose

```text
Normalize incoming case/request into industry, subdomain, and business function.
```

### Input

```text
case summary
user request
public-source case note
synthetic test input
```

### Process

```text
1. Identify industry/domain.
2. Identify subdomain.
3. Identify business function.
4. Identify domain confidence: HIGH / MEDIUM / LOW / MIXED / UNKNOWN.
5. Trigger unknown fallback if needed.
```

### Output

```text
Domain:
Subdomain:
Business function:
Confidence:
Fallback needed: yes / no
```

### Validation

```text
3+ synthetic/public-source domain cases must route correctly.
Unknown or unclear cases must not be forced.
```

---

## 4. CAP-CROSS-002｜Data Sensitivity Classifier

### Purpose

```text
Classify data sensitivity before routing or output generation.
```

### Input

```text
data source description
domain
data type
user-provided context
```

### Process

```text
1. Identify whether data is public/synthetic/internal/private/regulated.
2. Assign S0-S4 sensitivity label.
3. Block or route high-risk data.
```

### Output

```text
Sensitivity level: S0 / S1 / S2 / S3 / S4
Allowed mode:
Blocked actions:
User review required: yes / no
```

### Validation

```text
S3/S4 real-data-like examples must be blocked or routed to user_review_required.
```

---

## 5. CAP-CROSS-004｜Domain Department Matcher

### Purpose

```text
Match a normalized case to the right department or candidate domain department.
```

### Input

```text
domain
subdomain
task intent if available
sensitivity level
known validation needs
```

### Process

```text
1. Check existing core departments.
2. Check existing domain candidates.
3. Select lead department.
4. Select supporting departments if needed.
5. Use unknown fallback if no confident match exists.
```

### Output

```text
Lead department:
Supporting departments:
Domain Department candidate:
Fallback route:
```

### Validation

```text
Known synthetic cases must route to sensible lead/support departments.
Unknown cases must not be forced.
```

---

## 6. CAP-CROSS-006｜Human Review Gate Builder

### Purpose

```text
Define who must review output before action in higher-risk workflows.
```

### Input

```text
domain
sensitivity
task intent
output type
risk boundary
```

### Process

```text
1. Identify risk type.
2. Identify reviewer role.
3. Define what reviewer must check.
4. Define what cannot be automated.
```

### Output

```text
Human reviewer role:
Review checklist:
Cannot automate:
Escalation condition:
```

### Validation

```text
Healthcare, legal, finance, insurance, logistics compliance, education/minors, and public-sector cases must include human review gate.
```

---

## 7. CAP-CROSS-009｜Safe First Test Generator

### Purpose

```text
Convert a risky workflow idea into a safe public/synthetic/report-only first test.
```

### Input

```text
workflow idea
domain
sensitivity
risk boundary
blocked actions
```

### Process

```text
1. Remove real/private data dependency.
2. Replace production action with public/synthetic dry-run.
3. Define report-only output.
4. Add human review requirement.
5. Mark blocked actions.
```

### Output

```text
Safe first test:
Data allowed:
Output allowed:
Human review:
Blocked actions:
```

### Validation

```text
No safe first test may recommend production execution, real-data processing, or public action without approval.
```

---

## 8. CAP-CROSS-011｜Domain Report Output Builder

### Purpose

```text
Produce consistent report structure after domain routing and safety validation.
```

### Input

```text
case summary
domain classification
data sensitivity
lead/support departments
validation pack or fallback
human review gate
capability candidates
```

### Process

```text
1. Build case summary.
2. Add domain/data/sensitivity classification.
3. Add workflow problem.
4. Add risk boundary.
5. Add department routing.
6. Add validation plan.
7. Add capability candidates.
8. Add next safe step.
```

### Output

```text
Domain report with required sections:
- Case summary
- Domain classification
- Data type and sensitivity
- Workflow problem
- AI workflow opportunity
- Risk boundary
- Human review gate
- Validation plan
- Department routing
- Capability candidates
- Next safe step
```

### Validation

```text
Report fails if it lacks risk boundary, human review gate, or blocked actions for high-risk cases.
```

---

## 9. CAP-CROSS-012｜Domain Gap Detector

### Purpose

```text
Identify missing department, validation pack, fallback rule, capability, or test after a report/test run.
```

### Input

```text
case report
test result
WARN / FAIL / BLOCKED notes
routing ambiguity
validation gap
```

### Process

```text
1. Identify unresolved issue.
2. Classify gap type.
3. Recommend next safe internal task.
4. Avoid unsafe/public/main/backend/data actions.
```

### Output

```text
Gap ID:
Gap type:
Why it matters:
Recommended safe next task:
Approval required: yes / no
```

### Validation

```text
Gaps must produce safe internal actions, not public/production actions unless user approval is explicitly required.
```

---

## 10. Combined operating flow

```text
Input case
→ CAP-CROSS-001 Domain Intake Classifier
→ CAP-CROSS-002 Data Sensitivity Classifier
→ CAP-CROSS-004 Domain Department Matcher
→ CAP-CROSS-006 Human Review Gate Builder if needed
→ CAP-CROSS-009 Safe First Test Generator
→ CAP-CROSS-011 Domain Report Output Builder
→ CAP-CROSS-012 Domain Gap Detector
```

---

## 11. Failure handling

If any step is uncertain:

```text
route to UNKNOWN-DOMAIN fallback
or mark user_review_required
or mark blocked_current_phase
```

Do not:

```text
force domain
skip sensitivity
skip human review
recommend production
claim compliance/security/legal/medical/financial readiness
```

---

## 12. Closeout

```text
INTERNAL-SPEC-001 result: PASS
Internal-spec draft created for ready capabilities: 7
Real data authorized: no
Production authorized: no
Public demo changed: no
Backend/API added: no
Recommended next: SPEC-TEST-001｜Internal Spec Chain Test
```

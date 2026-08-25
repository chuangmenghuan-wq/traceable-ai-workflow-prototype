# MIXED-ROUTING-TEST-001｜Mixed-Domain Routing Stress Test

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal stress test / public-safe  
**Date:** 2026-07-09  
**Mode:** Synthetic-only / report-only / no private data  

> 中文定位：這份報告測試 MIXED-ROUTING-001 的多部門路由規則。真實案例常常跨產業、跨資料型態、跨風險，因此不能只用單一部門處理。這份測試檢查 lead department、supporting departments、validation packs、highest-risk-boundary 是否能正確運作。

---

## 1. Test goal

```text
Stress-test multi-department routing with mixed-domain synthetic cases.
```

中文目標：

```text
測試複合型案例進來時，COS 能不能找出主責部門、支援部門、驗證包，並讓最高風險邊界優先。
```

---

## 2. Test boundary

```text
Synthetic cases only: yes
Private data used: no
Real customer data used: no
Production system touched: no
Public action: no
Backend/API/storage/login: no
```

---

## 3. Stress test cases

| Test ID | Mixed case | Domains | Lead department | Supporting departments | Validation packs | Result |
|---|---|---|---|---|---|---|
| M01 | Fake healthcare insurance claim review | healthcare + insurance + legal/privacy | Workflow Safety | Healthcare Workflow + Insurance Process Automation + Industry Case Research | Healthcare + Insurance + Legal boundary | PASS |
| M02 | Fake AI customs classification assistant | logistics + legal/compliance + customer data | Logistics Compliance candidate | Workflow Safety + Tool Research | Logistics + Legal boundary | PASS |
| M03 | Fake retail personalization workflow | retail + marketing + privacy/data governance | Retail Data Operations candidate | Workflow Safety + Public-Safe Boundary Guard | Retail + customer-data boundary | PASS |
| M04 | Fake manufacturing predictive maintenance vendor purchase | manufacturing + tool research + operations safety | Manufacturing Operations candidate | Tool Research + Workflow Safety | Manufacturing + Tool Research boundary | PASS |
| M05 | Fake city parking enforcement AI | public sector + legal/compliance + computer vision + citizen data | Workflow Safety | Industry Case Research + AI Governance candidate | Governance + privacy/legal boundary | WARN |
| M06 | Fake school student-risk prediction workflow | education + privacy + decision support + minors | Workflow Safety | Industry Case Research + Education candidate-needed | Generic sensitive-data fallback | WARN |

---

## 4. Detailed routing results

### M01 — Healthcare insurance claim review

```text
Detected domains: healthcare, insurance, legal/privacy
Lead department: Workflow Safety Department
Supporting departments: Healthcare Workflow candidate, Insurance Process Automation candidate, Industry Case Research Department
Validation packs: Healthcare Workflow, Insurance Process Automation, Legal boundary
Highest-risk boundary: S4 medical/claim data + legal/privacy implications
Result: PASS
Safe output: synthetic workflow risk report only
Blocked: real claim decision, medical advice, legal advice, payout decision
```

---

### M02 — AI customs classification assistant

```text
Detected domains: logistics, legal/compliance, customer data
Lead department: Logistics Compliance Department candidate
Supporting departments: Workflow Safety Department, Tool Research Department
Validation packs: Logistics Compliance, Legal boundary
Highest-risk boundary: compliance/legal decision risk
Result: PASS
Safe output: classification triage draft + exception escalation gate
Blocked: final customs/legal classification decision
```

---

### M03 — Retail personalization workflow

```text
Detected domains: retail, marketing, privacy/data governance
Lead department: Retail Data Operations Department candidate
Supporting departments: Workflow Safety Department, Public-Safe Boundary Guard
Validation packs: Retail Data Operations, customer-data boundary
Highest-risk boundary: real customer profile data
Result: PASS
Safe output: synthetic personalization workflow review
Blocked: real customer personalization without consent/governance review
```

---

### M04 — Manufacturing predictive maintenance vendor purchase

```text
Detected domains: manufacturing, tool research, operations safety
Lead department: Manufacturing Operations Department candidate
Supporting departments: Tool Research Department, Workflow Safety Department
Validation packs: Manufacturing Operations, Tool Research boundary
Highest-risk boundary: production system integration risk
Result: PASS
Safe output: public/vendor research + synthetic dry-run plan
Blocked: production integration, auto-control, purchase approval
```

---

### M05 — City parking enforcement AI

```text
Detected domains: public sector, legal/compliance, computer vision, citizen data
Lead department: Workflow Safety Department
Supporting departments: Industry Case Research Department, AI Governance Department candidate
Validation packs: Governance + privacy/legal boundary
Highest-risk boundary: citizen data / enforcement / legal decision risk
Result: WARN
Issue: Computer Vision / Public Sector Enforcement department candidate is not yet modeled
Safe output: risk preflight only
Blocked: enforcement decision automation
```

---

### M06 — School student-risk prediction workflow

```text
Detected domains: education, privacy, minors, decision support
Lead department: Workflow Safety Department
Supporting departments: Industry Case Research Department, Education Department candidate-needed
Validation packs: Generic sensitive-data fallback
Highest-risk boundary: minors + student data + eligibility/intervention risk
Result: WARN
Issue: Education / minors data validation pack missing
Safe output: synthetic risk review only
Blocked: real student-risk scoring or intervention decisions
```

---

## 5. Stress test summary

```text
Cases tested: 6
PASS: 4
WARN: 2
FAIL: 0
BLOCKED: 0
Critical safety issues: none
```

---

## 6. Findings

### Finding A — Highest-risk-boundary rule works

```text
In mixed cases, Workflow Safety takes lead when regulated/sensitive/rights-impacting data appears.
```

### Finding B — Domain gaps are now visible

New candidate gaps:

```text
Public Sector Enforcement Department candidate
Education / Student Data Department candidate
Computer Vision Validation Pack
Minors Data Boundary Pack
```

### Finding C — Multi-department routing is useful but needs a coordinator

Current gap:

```text
ROUTING-COORDINATOR-001｜Routing Coordinator Role
```

Reason:

```text
When 3+ departments are involved, the system needs one coordinating role to keep output coherent and avoid conflicting recommendations.
```

---

## 7. Next internal tasks

Recommended safe next tasks:

```text
1. ROUTING-COORDINATOR-001｜Routing Coordinator Role
2. EDUCATION-DOMAIN-SEED-001｜Education / Student Data Domain Seed
3. PUBLIC-SECTOR-SEED-001｜Public Sector Enforcement Domain Seed
4. VISION-VALIDATION-PACK-001｜Computer Vision Validation Pack Seed
```

---

## 8. Closeout

```text
MIXED-ROUTING-TEST-001 result: PASS
Mixed cases tested: 6
PASS: 4
WARN: 2
FAIL: 0
BLOCKED: 0
Highest-risk-boundary rule tested: yes
New gaps found: routing coordinator + education/public-sector/vision seeds
No private data used: yes
No public/demo/backend changed: yes
Recommended next: ROUTING-COORDINATOR-001｜Routing Coordinator Role
```

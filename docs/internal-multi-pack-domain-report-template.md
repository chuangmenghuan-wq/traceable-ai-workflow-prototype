# REPORT-TEMPLATE-001｜Multi-Pack Domain Report Template

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal report template / public-safe  
**Date:** 2026-07-09  
**Mode:** Docs-only / report template  

> 中文定位：這份文件補上 SPEC-TEST-007 發現的缺口：混合領域報告不能只寫一個 domain 或一個 boundary pack。它需要明確列出 primary packs、secondary packs、最高風險邊界、人審角色與被禁止的輸出。

---

## 1. Purpose

```text
Create a standard report template for mixed-domain cases using multiple boundary packs.
```

中文目的：

```text
當一個案例同時涉及多個產業或多種敏感資料時，報告要清楚說明用了哪些安全邊界包，以及哪個邊界優先。
```

---

## 2. Template structure

```text
# [CASE-ID]｜Mixed-Domain Report

## 1. Case summary
## 2. Detected domains
## 3. Data types and sensitivity
## 4. Lead and supporting departments
## 5. Boundary packs selected
## 6. Highest-risk boundary
## 7. Human review gates
## 8. Allowed outputs
## 9. Blocked outputs
## 10. Safe first test
## 11. Validation checklist
## 12. Capability candidates
## 13. Gaps found
## 14. Next safe step
```

---

## 3. Boundary packs selected section

Required fields:

```text
Primary boundary packs:
Secondary boundary packs:
Fallback used: yes / no
Missing pack: yes / no
Pack confidence: high / medium / low / mixed
Reason for each pack:
```

---

## 4. Highest-risk boundary section

Required rule:

```text
highest-risk boundary wins
```

Required fields:

```text
Highest-risk domain:
Highest-risk data type:
Highest-risk blocked action:
Human reviewer required:
Reason this boundary overrides lower-risk routes:
```

---

## 5. Human review gates section

Required fields:

```text
Reviewer role 1:
Reviewer role 2:
Reviewer role 3 if needed:
What each reviewer must check:
What cannot be automated:
```

---

## 6. Blocked outputs section

Must include all relevant blocked outputs from each selected pack.

Example:

```text
Healthcare + Insurance case blocked outputs:
- medical advice
- diagnosis
- treatment recommendation
- final clinical note approval
- claim approval/denial
- coverage decision
- payout recommendation
- customer-facing decision message
```

---

## 7. Safe first test section

Must specify:

```text
Synthetic data only: yes
Public-source only if applicable: yes / no
No real private data: yes
No production action: yes
No professional advice or decision: yes
Human review required before any next step: yes
```

---

## 8. Template validation checklist

```text
Detected domains listed: yes / no
All relevant boundary packs listed: yes / no
Highest-risk boundary stated: yes / no
Human review gates present: yes / no
Blocked outputs listed: yes / no
Safe first test uses synthetic/public data only: yes / no
No real-data/production/professional-advice claim: yes / no
Next safe step is internal/docs/report-only: yes / no
```

Fail if:

```text
- boundary packs are missing
- highest-risk boundary is unclear
- human review gate is missing
- blocked outputs are incomplete
- report implies real-data or production readiness
```

---

## 9. Relationship to capabilities

This template strengthens:

```text
CAP-CROSS-005 Domain Validation Pack Selector
CAP-CROSS-008 Multi-Department Routing Resolver
CAP-CROSS-011 Domain Report Output Builder
CAP-CROSS-012 Domain Gap Detector
CAP-CROSS-013 Routing Coordinator
```

---

## 10. Closeout

```text
REPORT-TEMPLATE-001 result: PASS
Multi-pack report template created: yes
Boundary packs selected section defined: yes
Highest-risk boundary section defined: yes
Human review gate section defined: yes
Validation checklist defined: yes
No private data used: yes
No public/demo/backend changed: yes
Recommended next: update PR summary and validate branch diff
```

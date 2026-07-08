# MARKETING-CLAIMS-BOUNDARY-001｜Marketing Claims Boundary Pack

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal domain boundary pack / public-safe  
**Date:** 2026-07-09  
**Mode:** Docs-only / boundary pack  

> 中文定位：這份文件補上 MIXED-ROUTING-TEST-002 發現的缺口：行銷內容可能涉及產品功效、保險保障、金融利益、醫療/健康效果、合規、安全或性能承諾。AI 只能產出 synthetic/report-only 草稿與風險檢查，不能產生未審核的正式廣告主張或合規保證。

---

## 1. Purpose

```text
Define safe boundaries for marketing claim drafting, product copy review, campaign risk review, and claims-sensitive content workflows.
```

中文目的：

```text
行銷文案不是只要寫得漂亮；只要牽涉保險、金融、醫療、健康、安全、合規、性能、價格或保證，就需要 claim boundary。
```

---

## 2. Common inputs

Allowed in current phase:

```text
- synthetic campaign brief
- fake product feature list
- public product description
- synthetic claim-risk examples
- fake insurance/finance/health product copy examples
```

Blocked without explicit later review:

```text
- real customer targeting data
- real regulated product marketing copy
- unverified product claims
- medical/health outcome claims
- insurance coverage claims
- financial return claims
- compliance/security guarantee claims
- customer-facing campaign ready-to-send copy
```

---

## 3. Sensitivity classification

```text
Public generic product copy → S0
Synthetic campaign brief → S0/S1
Internal non-sensitive marketing draft → S1
Real campaign performance/customer targeting data → S2-S3
Regulated product claims or customer-identifiable targeting → S4
```

---

## 4. Allowed outputs now

```text
- synthetic campaign risk review
- claim-risk checklist
- safer wording suggestions
- brand-safety review draft
- human review map
- safe first test plan
```

Blocked outputs now:

```text
- ready-to-publish regulated marketing claim
- insurance coverage guarantee
- financial return guarantee
- medical/health effect claim
- compliance/security guarantee
- performance guarantee
- customer-facing final campaign approval
```

---

## 5. Human review gate

Reviewer roles:

```text
marketing owner
product owner
legal/compliance reviewer if regulated claims appear
medical/financial/insurance reviewer if domain-specific claims appear
```

Must review:

```text
- whether claims are supported by source facts
- whether regulated claims appear
- whether disclaimers or qualifications are needed
- whether copy implies guarantees
- whether customer targeting data is involved
- whether output is draft/report-only
```

Cannot automate in current phase:

```text
- final campaign approval
- regulated claim approval
- product performance guarantee
- compliance/legal approval
- customer targeting execution
```

---

## 6. Validation checklist

```text
Data is synthetic/public: yes / no
Claims match source facts: yes / no
No regulated claim is treated as final: yes / no
No guarantee is implied: yes / no
Human review gate is present: yes / no
Output is marked draft/report-only: yes / no
Customer targeting data is not used: yes / no
```

Fail if:

```text
- unverified claim is presented as fact
- insurance/financial/medical/compliance/security guarantee is made
- campaign is marked ready to publish without review
- real targeting data is used without approval
- human review is omitted for regulated claims
```

---

## 7. Safe first test pattern

```text
Use a synthetic campaign brief and fake product feature list.
Generate a claim-risk checklist and safer wording suggestions.
Route all regulated or guarantee-like claims to human review.
Do not publish, target, send, approve, or guarantee.
```

---

## 8. Relationship to capabilities

This boundary pack strengthens:

```text
CAP-CROSS-005 Domain Validation Pack Selector
CAP-CROSS-006 Human Review Gate Builder
CAP-CROSS-007 Blocked Claims Detector
CAP-CROSS-008 Multi-Department Routing Resolver
CAP-CROSS-009 Safe First Test Generator
CAP-CROSS-011 Domain Report Output Builder
CAP-CROSS-013 Routing Coordinator
```

---

## 9. Closeout

```text
MARKETING-CLAIMS-BOUNDARY-001 result: PASS
Marketing claims boundary pack created: yes
Allowed/blocked data defined: yes
Human review gate defined: yes
Validation checklist defined: yes
No real customer/regulated marketing data used: yes
No final marketing claim approved: yes
No public/demo/backend changed: yes
Recommended next: COORDINATOR-TEST-001｜Routing Coordinator Conflict Test
```

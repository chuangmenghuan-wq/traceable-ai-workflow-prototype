# RETAIL-DATA-BOUNDARY-001｜Retail Customer Data Boundary Pack

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal domain boundary pack / public-safe  
**Date:** 2026-07-09  
**Mode:** Docs-only / boundary pack  

> 中文定位：這份文件補上 SPEC-TEST-001 發現的缺口：零售/行銷工作流常會碰到 customer profiles、purchase history、segmentation、personalization、product copy、brand claims，因此即使只是做報告，也需要一個 Retail Customer Data Boundary Pack，避免系統把 synthetic 測試誤推到真實客戶資料。

---

## 1. Purpose

```text
Define the data, consent, segmentation, personalization, and brand-safety boundaries for retail/marketing AI workflows.
```

中文目的：

```text
零售/行銷看起來風險比醫療法律低，但只要碰到顧客資料、購買紀錄、分眾、個人化，就會變成敏感資料工作流。
```

---

## 2. Common inputs

Allowed in current phase:

```text
- synthetic customer profiles
- fake purchase history
- public/fake product catalog
- synthetic campaign brief
- public product descriptions
```

Blocked without approval:

```text
- real customer profiles
- real purchase history
- real email/phone/customer IDs
- loyalty program data
- sensitive demographic attributes
- ad platform exports
- CRM exports
- private campaign performance logs
```

---

## 3. Sensitivity classification

```text
Public/fake product data → S0
Synthetic customer profiles → S0/S1
Internal non-sensitive campaign notes → S1
Real product performance data → S2
Real customer profiles / purchase history → S3
Sensitive demographics / minors / regulated attributes → S4
```

---

## 4. Allowed outputs now

```text
- synthetic segmentation draft
- product description draft from fake/public catalog
- brand-safety checklist
- customer-data boundary note
- safe first test plan
- validation checklist
```

Blocked outputs now:

```text
- real customer targeting decision
- automated email sending
- real personalization deployment
- consent/compliance guarantee
- sensitive attribute segmentation
- customer scoring without approval
```

---

## 5. Human review gate

Reviewer role:

```text
marketing/data owner
```

Must review:

```text
- product claim accuracy
- brand voice
- customer data boundary
- consent/governance requirement
- segmentation fairness/sensitivity
- whether output is draft-only or action-ready
```

Cannot automate in current phase:

```text
- final real customer targeting
- consent determination
- sensitive segmentation
- campaign send/deployment
```

---

## 6. Validation checklist

```text
Product facts match source catalog: yes / no
Claims are not exaggerated: yes / no
Customer data is synthetic/public: yes / no
Segmentation avoids sensitive attributes: yes / no
Consent/governance boundary stated: yes / no
Human review gate present: yes / no
Output marked as draft/report-only: yes / no
```

Fail if:

```text
- real customer data is used without approval
- consent/compliance is claimed as guaranteed
- sensitive attributes are used for segmentation
- system suggests sending campaign automatically
- product claims are unsupported
```

---

## 7. Safe first test pattern

```text
Use 10 synthetic customer profiles + fake product catalog fields.
Generate draft product descriptions and broad segment labels.
Run brand-safety and customer-data boundary checklist.
Do not send, target, upload, or connect to any real system.
```

---

## 8. Relationship to capabilities

This boundary pack strengthens:

```text
CAP-CROSS-002 Data Sensitivity Classifier
CAP-CROSS-005 Domain Validation Pack Selector
CAP-CROSS-006 Human Review Gate Builder
CAP-CROSS-009 Safe First Test Generator
CAP-CROSS-011 Domain Report Output Builder
CAP-CROSS-012 Domain Gap Detector
```

---

## 9. Closeout

```text
RETAIL-DATA-BOUNDARY-001 result: PASS
Retail/customer-data boundary pack created: yes
Allowed/blocked data defined: yes
Human review gate defined: yes
Validation checklist defined: yes
No real customer data used: yes
No public/demo/backend changed: yes
Recommended next: update PR summary and validate branch diff
```

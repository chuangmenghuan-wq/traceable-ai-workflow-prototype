# LEGAL-BOUNDARY-001｜Legal AI Risk Boundary Pack

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal domain boundary pack / public-safe  
**Date:** 2026-07-09  
**Mode:** Docs-only / boundary pack  

> 中文定位：這份文件補上 SPEC-TEST-004 發現的缺口：法律相關工作流很容易從「資訊整理 / 草稿審查 / 風險提示」跨到「法律建議 / 合規保證 / 合約核准」。目前只能做 synthetic/report-only 的 legal-risk preflight，不能處理真實案件或提供法律建議。

---

## 1. Purpose

```text
Define safe boundaries for legal-risk preflight, synthetic contract draft review, and legal workflow research.
```

中文目的：

```text
法律領域不能把 AI 報告誤當成律師意見、合約核准或合規保證，所以必須有明確邊界。
```

---

## 2. Common inputs

Allowed in current phase:

```text
- synthetic contract drafts
- fake clause examples
- public legal workflow examples
- synthetic mediation scenario
- generic business-risk examples
```

Blocked without explicit later review:

```text
- real legal case files
- real client facts
- real contract drafts tied to a transaction
- privileged or confidential communications
- court documents needing legal interpretation
- jurisdiction-specific legal advice requests
- compliance certification requests
```

---

## 3. Sensitivity classification

```text
Public legal article → S0
Synthetic contract draft → S0/S1
Internal non-sensitive legal workflow note → S1
Real contract / business transaction context → S3
Privileged legal communication / litigation / rights-impacting facts → S4
```

---

## 4. Allowed outputs now

```text
- synthetic legal-risk preflight report
- missing-clause checklist draft
- issue-spotting draft
- business-risk summary draft
- human legal review map
- safe first test plan
```

Blocked outputs now:

```text
- legal advice
- final legal conclusion
- contract approval
- ready-to-sign recommendation
- compliance guarantee
- jurisdiction-specific legal interpretation
- lawyer replacement claim
```

---

## 5. Human review gate

Reviewer role:

```text
legal professional / authorized legal reviewer
```

Must review:

```text
- facts and assumptions
- jurisdiction applicability
- whether the output is only issue spotting
- whether any language sounds like legal advice
- whether compliance or approval is implied
- whether client rights or obligations are affected
```

Cannot automate in current phase:

```text
- final legal interpretation
- contract approval
- compliance conclusion
- legal strategy
- rights-impacting recommendation
```

---

## 6. Validation checklist

```text
Data is synthetic/public: yes / no
No real client facts are present: yes / no
Jurisdiction assumptions are marked: yes / no
Output is labeled draft/report-only: yes / no
No legal advice is provided: yes / no
No contract approval is implied: yes / no
Human legal review gate is present: yes / no
```

Fail if:

```text
- real legal facts are used without approval
- output gives legal advice
- output says contract is legally approved
- compliance is guaranteed
- jurisdiction-specific interpretation is final
- ready-to-sign recommendation is made
```

---

## 7. Safe first test pattern

```text
Use a synthetic vendor agreement draft.
Generate a missing-clause checklist and issue-spotting draft.
Add business-risk summary and human legal review map.
Do not approve, interpret, guarantee, or recommend signing.
```

---

## 8. Relationship to capabilities

This boundary pack strengthens:

```text
CAP-CROSS-002 Data Sensitivity Classifier
CAP-CROSS-005 Domain Validation Pack Selector
CAP-CROSS-006 Human Review Gate Builder
CAP-CROSS-007 Blocked Claims Detector
CAP-CROSS-009 Safe First Test Generator
CAP-CROSS-011 Domain Report Output Builder
CAP-CROSS-012 Domain Gap Detector
```

---

## 9. Closeout

```text
LEGAL-BOUNDARY-001 result: PASS
Legal AI risk boundary pack created: yes
Allowed/blocked data defined: yes
Human legal review gate defined: yes
Validation checklist defined: yes
No real legal case used: yes
No legal advice given: yes
No public/demo/backend changed: yes
Recommended next: SPEC-TEST-005｜Healthcare Internal Spec Chain Test
```

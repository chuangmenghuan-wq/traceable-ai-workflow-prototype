# EDUCATION-BOUNDARY-001｜Student Data Boundary Pack

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal domain boundary pack / public-safe  
**Date:** 2026-07-09  
**Mode:** Docs-only / boundary pack  

> 中文定位：這份文件補上 SPEC-TEST-006 發現的缺口：教育/學生資料工作流可能涉及未成年人、學生紀錄、學習或行為標籤、支援需求、介入決策與家庭溝通。目前只能做 synthetic/report-only 測試，不可處理真實學生資料或產生學生決策。

---

## 1. Purpose

```text
Define safe boundaries for synthetic student-support workflow review and education data research.
```

中文目的：

```text
學生資料與未成年人資料高度敏感，AI 只能協助做合成案例下的流程檢查，不能替學生貼標籤、評分、決定介入或產生正式通知。
```

---

## 2. Common inputs

Allowed in current phase:

```text
- synthetic attendance notes
- fake assignment completion patterns
- fake teacher observations
- synthetic support workflow notes
- public education workflow examples
```

Blocked without explicit later review:

```text
- real student records
- real attendance records
- real grades or assessment data
- behavioral or disciplinary records
- student health or counseling notes
- parent/student communications
- special education or eligibility records
- identifiable minors data
```

---

## 3. Sensitivity classification

```text
Public education article → S0
Synthetic student-support example → S0/S1
Internal non-sensitive workflow note → S1
Real student academic/support data → S3
Identifiable minors data / health / discipline / eligibility data → S4
```

---

## 4. Allowed outputs now

```text
- synthetic missing-information checklist
- educator review map
- workflow risk report
- draft support-process checklist
- safe first test plan
```

Blocked outputs now:

```text
- student risk score
- student label
- eligibility/intervention decision
- disciplinary recommendation
- special education placement suggestion
- parent/student message ready to send
- automated student support action
```

---

## 5. Human review gate

Reviewer roles:

```text
educator
school counselor
authorized student-support reviewer
```

Must review:

```text
- whether data is synthetic or real
- whether student identity is present
- whether labels or scores are implied
- whether output affects eligibility, discipline, intervention, or support placement
- whether family communication is draft-only
- whether human educator judgment remains central
```

Cannot automate in current phase:

```text
- student risk scoring
- eligibility decision
- intervention action
- disciplinary action
- family communication as final
- support placement decision
```

---

## 6. Validation checklist

```text
Data is synthetic/public: yes / no
No identifiable student/minor data is present: yes / no
No student score or label is produced: yes / no
No eligibility/intervention decision is made: yes / no
No ready-to-send family message is generated: yes / no
Human educator review gate is present: yes / no
Output is marked draft/report-only: yes / no
```

Fail if:

```text
- real student data is used without approval
- student risk score or label is produced
- eligibility/intervention/displine action is suggested as final
- family message is generated as ready to send
- minors data is treated as low sensitivity
```

---

## 7. Safe first test pattern

```text
Use synthetic attendance notes, fake assignment patterns, and fake teacher observations.
Generate a missing-information checklist and educator review map.
Do not score, label, decide, discipline, place, intervene, or message families.
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
EDUCATION-BOUNDARY-001 result: PASS
Student data boundary pack created: yes
Allowed/blocked data defined: yes
Human educator review gate defined: yes
Validation checklist defined: yes
No real student data used: yes
No student decision made: yes
No public/demo/backend changed: yes
Recommended next: SPEC-CHAIN-SUMMARY-002｜High-Risk Domain Chain Summary
```

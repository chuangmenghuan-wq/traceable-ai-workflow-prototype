# INDUSTRY-CASE-002｜Cross-Domain Router Test

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal research report / public-safe  
**Date:** 2026-07-09  
**Mode:** Public-source / report-only / no private data  

> 中文定位：這份報告延續 INDUSTRY-CASE-001，用更多不同行業案例測試 Universal Domain Intake Router 與 Domain Department Factory。目的不是證明系統已經完美，而是找出哪些產業需要自己的 Domain Department，哪些能力可以先抽象成 reusable Capability。

---

## 1. Research question

```text
Can the Universal Domain Intake Router handle additional industries with different data types, risks, and validation needs?
```

中文問題：

```text
如果農業、保險、法律、物流、零售/行銷等案例進來，COS 能不能分對領域、辨識資料型態、抓出風險、找到部門，並提出可重複能力？
```

---

## 2. Source boundary

Only public-source patterns were used.

```text
Private customer data: no
Confidential company documents: no
Credentials/API keys: no
Production logs: no
Regulated records: no
```

---

## 3. Case set v0.2

This test adds five more domain patterns:

```text
1. Agriculture — precision agriculture / data infrastructure / crop decision support
2. Insurance — claim process automation / object-centric process mining
3. Legal — legal AI risk management / legal consultation / mediation
4. Logistics / trade compliance — AI classification assistant / compliance workflow
5. Retail / marketing — customer data identity resolution / product data automation
```

---

## 4. Cross-domain routing table

| Case | Domain | Data type | Sensitivity | Primary department | Domain Department candidate | Capability candidates |
|---|---|---|---|---|---|---|
| Precision agriculture | Agriculture | soil, weather, yield, satellite/drone/sensor data | S1-S3 | Industry Case Research + Workflow Safety | Agriculture Decision Support Department | Data readiness check, sensor-risk mapper, farmer decision support gate |
| Insurance claim automation | Insurance | claim files, object/process logs, claim parts | S3-S4 if real | Industry Case Research + Workflow Safety | Insurance Process Automation Department | Claim part extraction validation, process mining impact review, human claim review gate |
| Legal AI risk management | Legal | legal questions, legal drafts, mediation context | S3-S4 if real | Workflow Safety + Industry Case Research | Legal AI Risk Department | Legal-use risk preflight, affected-user concern checklist, human legal review gate |
| Logistics / trade compliance | Logistics | shipment classification, compliance records, customs data | S2-S4 | Industry Case Research + Tool Research | Logistics Compliance Department | AI classification assistant validation, compliance trace note, exception escalation gate |
| Retail / marketing data | Retail / ecommerce / marketing | customer profiles, product data, campaigns | S2-S3 | Industry Case Research + Public-Safe Boundary Guard | Retail Data Operations Department | Identity resolution boundary check, customer-data consent gate, brand-safe content validation |

---

## 5. Case A — Agriculture: precision agriculture / data infrastructure

### Public signal

Public research on AI in agriculture highlights that farming AI depends heavily on data readiness: soil, weather, yield, crop insurance, satellite, sensor, and platform data must align in timing, geography, and machine-readable structure before automated decision support can scale.

### COS routing

```text
Domain: agriculture
Subdomain: precision agriculture / decision support
Data type: soil / weather / yield / satellite / sensor / crop insurance data
Sensitivity level: S1-S3 depending on farm and platform data
Task intent: decision support / prediction / resource planning
Primary department: Industry Case Research Department + Workflow Safety Department
Domain Department candidate: Agriculture Decision Support Department
```

### Risk boundary

```text
Public or synthetic agricultural data can be used for report-only tests.
Real farm financial, insurance, or location-specific operational data requires user review.
```

### Validation method

```text
- data readiness check
- time/geography alignment check
- baseline comparison against existing farm decision process
- human agronomist/farmer review gate
```

### Capability candidates

```text
CAP-AGRI-CAND-001｜Agriculture Data Readiness Checker
CAP-AGRI-CAND-002｜Farm Decision Support Human Review Gate
CAP-AGRI-CAND-003｜Sensor-to-Decision Validation Checklist
```

---

## 6. Case B — Insurance: claim process automation

### Public signal

A public insurance-domain case study describes using LLMs to automate identification of claim parts, with object-centric process mining used to evaluate how AI changes operational capacity and process dynamics.

### COS routing

```text
Domain: insurance
Subdomain: claims automation / process mining
Data type: claim files / claim parts / process logs
Sensitivity level: S3-S4 if real customer claim data
Task intent: extract fields / classify claim parts / process impact analysis
Primary department: Industry Case Research Department + Workflow Safety Department
Domain Department candidate: Insurance Process Automation Department
```

### Risk boundary

```text
Real claim data is blocked in current public/prototype phase.
Report-only public case research is allowed.
No automated claim decision or coverage decision is authorized.
```

### Validation method

```text
- extraction accuracy
- human claim handler review
- process mining before/after comparison
- exception escalation gate
```

### Capability candidates

```text
CAP-INS-CAND-001｜Claim Part Extraction Validation
CAP-INS-CAND-002｜Insurance Process Mining Impact Review
CAP-INS-CAND-003｜Claim Automation Human Escalation Gate
```

---

## 7. Case C — Legal: legal AI risk management

### Public signal

Public research on legal AI emphasizes that generative AI in legal consultation, drafting, mediation, and legal decision-support introduces risk-management problems beyond expert evaluation, including affected-user perceptions, acceptability, legitimacy, and rights-related risks.

### COS routing

```text
Domain: legal
Subdomain: legal consultation / drafting / mediation / legal AI risk
Data type: legal questions / drafts / mediation context / case-like facts
Sensitivity level: S3-S4 if real
Task intent: draft / summarize / risk review / decision support
Primary department: Workflow Safety Department + Industry Case Research Department
Domain Department candidate: Legal AI Risk Department
```

### Risk boundary

```text
No legal advice claim.
No automated legal decision-making.
Real legal files are blocked in current phase.
Any legal output must be framed as draft/research, not advice.
```

### Validation method

```text
- human legal professional review
- affected-user concern checklist
- risk/benefit tradeoff map
- jurisdiction-specific limitation note
```

### Capability candidates

```text
CAP-LEGAL-CAND-001｜Legal AI Risk Preflight
CAP-LEGAL-CAND-002｜Affected-User Concern Checklist
CAP-LEGAL-CAND-003｜Legal Draft Human Review Gate
```

---

## 8. Case D — Logistics / trade compliance

### Public signal

Public reporting on logistics AI adoption describes AI tools that assist classification, trade compliance, automation of complex logistics functions, and redeployment of staff to higher-value tasks.

### COS routing

```text
Domain: logistics / trade compliance
Subdomain: classification / compliance workflow / supply chain software
Data type: shipment records / product classifications / compliance documents
Sensitivity level: S2-S4 depending customer and customs data
Task intent: classify / compliance review / workflow automation
Primary department: Industry Case Research Department + Tool Research Department
Domain Department candidate: Logistics Compliance Department
```

### Risk boundary

```text
No automated customs/legal compliance decision.
No private shipment data in current phase.
Any trade-compliance use requires human specialist review and audit trail.
```

### Validation method

```text
- classification accuracy
- exception queue
- human compliance review
- trace note for decision basis
```

### Capability candidates

```text
CAP-LOG-CAND-001｜AI Classification Assistant Validation
CAP-LOG-CAND-002｜Trade Compliance Exception Escalation Gate
CAP-LOG-CAND-003｜Shipment Classification Trace Note
```

---

## 9. Case E — Retail / marketing data operations

### Public signal

Public retail and marketing AI examples show two common patterns: fragmented customer data identity resolution and product/campaign content automation. Both require clear data boundaries, brand safety, consent, and performance measurement.

### COS routing

```text
Domain: retail / ecommerce / marketing
Subdomain: customer data / personalization / product content
Data type: customer profiles / product data / campaign records
Sensitivity level: S2-S3 depending customer data
Task intent: identity resolution / personalization / content automation
Primary department: Industry Case Research Department + Public-Safe Boundary Guard
Domain Department candidate: Retail Data Operations Department
```

### Risk boundary

```text
No private customer data in current phase.
No personalization workflow without consent/data governance review.
Brand and accuracy validation are required for generated content.
```

### Validation method

```text
- data consent/governance checklist
- identity resolution quality metrics
- brand voice validation
- campaign performance review
```

### Capability candidates

```text
CAP-RET-CAND-001｜Customer Data Boundary Checker
CAP-RET-CAND-002｜Brand-Safe Product Content Validation
CAP-RET-CAND-003｜Identity Resolution Quality Review
```

---

## 10. What changed from INDUSTRY-CASE-001

INDUSTRY-CASE-001 showed COS can begin routing across domains.

INDUSTRY-CASE-002 adds a stronger pattern:

```text
Different industries require not only different departments, but different validation logic.
```

Examples:

```text
Agriculture → data readiness and sensor/geography/time alignment
Insurance → claim extraction validation and process mining impact review
Legal → no-advice boundary and affected-user concern checklist
Logistics → classification accuracy and compliance escalation gate
Retail → consent/data boundary and brand-safety validation
```

---

## 11. Domain Department Factory result

Candidate departments now supported by repeated public-case patterns:

```text
Healthcare Workflow Department
Finance Risk Review Department
Manufacturing Operations Department
Operations Forecasting Department
AI Governance Department
Taiwan Applied AI Department
Agriculture Decision Support Department
Insurance Process Automation Department
Legal AI Risk Department
Logistics Compliance Department
Retail Data Operations Department
```

Priority candidates for next internal test:

```text
1. Manufacturing Operations Department
2. Insurance Process Automation Department
3. Retail Data Operations Department
4. Legal AI Risk Department
5. Agriculture Decision Support Department
```

Reason:

```text
These have clearer report-only test paths without needing real private data first.
```

---

## 12. System maturity assessment

Current COS maturity for cross-domain routing:

```text
Domain detection: improving
Data type detection: improving
Risk boundary detection: improving
Department routing: improving
Validation routing: early but now visible
Perfect all-domain output: no
Production real-data readiness: no
```

Overall:

```text
COS is ready for public/synthetic multi-industry report-only testing.
COS is not ready for real private data or production automation.
```

---

## 13. Next capability gap

New gap discovered:

```text
VALIDATION-PACK-001｜Domain Validation Pack Template
```

Reason:

```text
Each Domain Department candidate needs its own validation pack:
- accuracy metrics
- human review gate
- risk checklist
- blocked actions
- safe first test
- output quality criteria
```

---

## 14. Closeout

```text
INDUSTRY-CASE-002 result: PASS
Additional industries tested: 5
Private data used: no
Domain Department Factory tested: yes
New domain candidates identified: yes
Perfect all-domain output proven: no
New gap found: Domain Validation Pack Template needed
Recommended next: VALIDATION-PACK-001｜Domain Validation Pack Template
```

---

## 15. Public source notes

Public-source patterns reviewed include:

```text
- AI agriculture data readiness and precision agriculture research
- insurance claim automation and object-centric process mining case study
- legal AI risk management and public opinion / affected-user risk research
- logistics / trade compliance AI adoption reporting
- retail / marketing AI case examples involving customer data identity resolution and product content automation
```

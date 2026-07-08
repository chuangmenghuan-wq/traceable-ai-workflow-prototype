# BLOCKED-CLAIMS-LIB-001｜Blocked Claims Pattern Library

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal safety library / public-safe  
**Date:** 2026-07-09  
**Mode:** Docs-only / claim safety guard  

> 中文定位：這份文件補上 CAPABILITY-TEST-002 發現的第二個 gap：Blocked Claims Detector 可以抓到明顯過度承諾，但需要更完整的 prohibited phrase / risky framing pattern library，避免系統把 prototype、report-only、synthetic-only 的能力講成產品成熟、合規、安全、醫療、法律或財務保證。

---

## 1. Purpose

```text
Detect and rewrite unsafe maturity, compliance, security, legal, medical, financial, and production-readiness claims.
```

中文目的：

```text
避免把還在內部測試的能力講成已經能正式商用、合規、資安安全、醫療/法律/金融可用。
```

---

## 2. Blocked claim families

### A. Product maturity overclaims

Blocked patterns:

```text
production-ready
enterprise-ready
customer-ready
ready for deployment
finished SaaS product
full automation platform
complete operating system
fully autonomous
```

Safer framing:

```text
internal prototype
public-safe demo
report-only workflow
synthetic-only test
internal architecture draft
candidate capability
```

---

### B. Compliance / legal guarantee overclaims

Blocked patterns:

```text
compliance-ready
legally compliant
guaranteed compliant
passes legal review
replaces legal review
approved for regulated use
```

Safer framing:

```text
compliance-risk preflight draft
legal review required
policy boundary checklist
not a compliance guarantee
```

---

### C. Security / privacy guarantee overclaims

Blocked patterns:

```text
secure by default
privacy-safe for all data
security-certified
enterprise security ready
safe for customer data
can process sensitive data now
```

Safer framing:

```text
public/synthetic data only
privacy/security review required
sensitive data blocked in current phase
no security certification claim
```

---

### D. Medical overclaims

Blocked patterns:

```text
medical advice
diagnosis
treatment recommendation
clinically approved
safe for patient records
replaces clinician review
```

Safer framing:

```text
draft clinical workflow note
clinician review required
synthetic/public medical example only
not medical advice
```

---

### E. Legal overclaims

Blocked patterns:

```text
legal advice
legal decision
court-ready
lawyer replacement
contract legally validated
legal compliance guaranteed
```

Safer framing:

```text
legal-risk draft
legal professional review required
jurisdiction-specific review needed
not legal advice
```

---

### F. Financial overclaims

Blocked patterns:

```text
financial advice
investment advice
fraud decision automation
loan approval automation
payout decision
risk score is final
```

Safer framing:

```text
financial-risk review draft
human analyst review required
not financial advice
not final eligibility or payout decision
```

---

### G. Automation overclaims

Blocked patterns:

```text
fully automated
no human needed
hands-off workflow
replaces staff
auto-approve
auto-deploy
auto-integrate
```

Safer framing:

```text
human-in-the-loop
safe first test
draft automation plan
manual review required
report-only recommendation
```

---

## 3. Risky framing patterns

Even without exact blocked words, these patterns are risky:

```text
- saying a prototype solves a regulated problem
- saying a checklist equals certification
- saying a report equals expert review
- saying synthetic test success proves real-world readiness
- saying public-source research proves private-data readiness
- saying a candidate department is an active production department
```

---

## 4. Detection output format

```text
Original phrase:
Claim family:
Risk level: low / medium / high / blocked
Why risky:
Safer replacement:
User review required: yes / no
```

---

## 5. Rewrite examples

### Example 1

Original:

```text
This system is ready for enterprise customer data.
```

Safer:

```text
This system is currently limited to public/synthetic internal testing. Customer data requires separate privacy, security, and user approval review.
```

### Example 2

Original:

```text
The legal workflow is compliant.
```

Safer:

```text
The workflow includes a legal-risk preflight draft, but it is not a compliance guarantee and requires legal professional review.
```

### Example 3

Original:

```text
The healthcare department can generate clinical notes for patient records.
```

Safer:

```text
The healthcare workflow candidate can be tested only with public/synthetic examples in the current phase. Any real clinical note workflow requires clinician, privacy, security, and governance review.
```

---

## 6. Relationship to CAP-CROSS

This library strengthens:

```text
CAP-CROSS-007 Blocked Claims Detector
CAP-CROSS-006 Human Review Gate Builder
CAP-CROSS-009 Safe First Test Generator
CAP-CROSS-011 Domain Report Output Builder
```

---

## 7. Validation rule

A public-facing or merge-ready document should fail claim validation if it contains:

```text
- production-ready claim without approval
- customer-data-ready claim without review
- compliance/security/legal/privacy guarantee
- professional advice claim
- automation without human review for high-risk workflows
```

---

## 8. Closeout

```text
BLOCKED-CLAIMS-LIB-001 result: PASS
Blocked claim families defined: yes
Safer framing examples defined: yes
Detection output format defined: yes
No public demo code changed: yes
No backend / AI API added: yes
No real customer data added: yes
Recommended next: MIXED-ROUTING-TEST-001｜Mixed-Domain Routing Stress Test
```

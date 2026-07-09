# INTERNAL-SPEC-006｜Blocked Claims Detector Spec Addendum

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal-spec addendum / public-safe  
**Date:** 2026-07-09  
**Mode:** Docs-only / internal capability spec addendum  

> 中文定位：這份文件把 CAP-CROSS-007｜Blocked Claims Detector 加入 internal-spec chain。它負責在 report output、PR-facing summary、public-facing-like wording 產出後，檢查是否出現 production-ready、real-data-ready、合規/安全/法律/醫療/金融保證、全自動等過度承諾。

---

## 1. Capability added

```text
CAP-CROSS-007｜Blocked Claims Detector
Lifecycle state: internal-spec-ready / internal-spec addendum
Owner: Public-Safe Boundary Guard / Workflow Safety Department
Allowed mode: docs/report-only wording safety review
```

---

## 2. Purpose

```text
Detect and rewrite unsafe overclaims before summaries, reports, or public-facing-like text are used.
```

中文目的：

```text
避免內部 prototype 被講成正式產品、可用真實資料、合規保證、資安保證、專業建議或全自動系統。
```

---

## 3. Input

```text
report draft
PR summary
user review guide
public reply draft
boundary pack summary
capability card
spec summary
```

---

## 4. Process

```text
1. Scan for blocked claim families.
2. Identify risky phrase or framing.
3. Classify risk level.
4. Suggest safer framing.
5. Require user review if public action is involved.
6. Block if wording implies production/real-data/professional readiness.
```

---

## 5. Blocked claim families

```text
product maturity overclaims
real-data readiness overclaims
compliance/security/privacy guarantee overclaims
legal advice overclaims
medical advice overclaims
financial/insurance decision overclaims
automation/no-human-needed overclaims
public/demo readiness overclaims
```

---

## 6. Output

```text
Original phrase:
Claim family:
Risk level:
Why risky:
Safer replacement:
User review required:
Result: PASS / WARN / FAIL / BLOCKED
```

---

## 7. Updated operating chain

```text
Input case
→ Domain Intake Classifier
→ Data Sensitivity Classifier
→ Task Intent Classifier
→ Domain Department Matcher
→ Domain Validation Pack Selector
→ Multi-Department Routing Resolver if mixed-domain
→ Routing Coordinator if conflict / 3+ departments
→ Human Review Gate Builder
→ Safe First Test Generator
→ Domain Report Output Builder
→ Blocked Claims Detector
→ Domain Gap Detector
→ Capability Candidate Extractor
→ Registry decision
```

---

## 8. Validation evidence

```text
BLOCKED-CLAIMS-LIB-001
CLAIMS-DETECTOR-TEST-001: 10/10 PASS
CLAIMS-AUDIT-001: PASS
CLAIMS-AUDIT-002: PASS
FINAL-CANDIDATE-PROMOTION-001: internal-spec-ready decision
```

---

## 9. Safety boundary

CAP-CROSS-007 does not authorize:

```text
- public posting
- public copy approval
- compliance/security/privacy certification
- legal/medical/financial advice
- production marketing approval
- real-data use
```

It only detects unsafe wording and suggests safer framing.

---

## 10. Closeout

```text
INTERNAL-SPEC-006 result: PASS
CAP-CROSS-007 added to internal-spec chain: yes
Blocked claim families defined: yes
Safer framing output defined: yes
Real-data authorization: no
Production promotion: no
Public/demo/backend changed: no
Recommended next: INTERNAL-SPEC-CHAIN-004｜Final Full Chain Closeout
```

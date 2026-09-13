# SPEC-TEST-004｜Legal Internal Spec Chain Test

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal chain test / public-safe  
**Date:** 2026-07-09  
**Mode:** Synthetic-only / report-only / no private data  

> 中文定位：這份報告用法律風險合成案例測試 INTERNAL-SPEC-001 的 7 個核心能力是否能處理 legal / legal-risk / draft-review 領域。這不是法律建議，不處理真實案件，也不產生可直接使用的法律文件。

---

## 1. Test goal

```text
Verify whether the 7-step internal-spec chain works for a synthetic legal-risk review case.
```

中文目標：

```text
確認 COS 能不能在法律高風險領域中，保持 no legal advice、human legal review、report-only 的安全邊界。
```

---

## 2. Test boundary

```text
Synthetic input only: yes
Real legal case file used: no
Legal advice given: no
Final legal decision made: no
Customer/private data used: no
Backend/API/storage/login added: no
Public demo changed: no
```

---

## 3. Synthetic test input

```text
A small business wants to use AI to review a synthetic vendor agreement draft, identify missing clauses, summarize possible business risks, and prepare a report for a human legal professional to review later.
```

---

## 4. Chain execution

### Step 1 — CAP-CROSS-001 Domain Intake Classifier

```text
Detected domain: legal
Subdomain: contract draft review / legal-risk preflight
Business function: vendor agreement review / business risk awareness
Confidence: HIGH
Fallback needed: no
Result: PASS
```

---

### Step 2 — CAP-CROSS-002 Data Sensitivity Classifier

```text
Data types: synthetic contract draft, clause list, business-risk notes
Sensitivity: S3-S4 if real contract/client/legal facts are used
Allowed mode now: synthetic contract examples only
Blocked: real legal files, client facts, final legal interpretation, legal advice
User review required: yes if real legal context is involved
Result: PASS
```

---

### Step 3 — CAP-CROSS-004 Domain Department Matcher

```text
Lead department: Legal AI Risk Department candidate
Supporting departments: Workflow Safety Department, Industry Case Research Department
Fallback route: not needed
Result: PASS
```

---

### Step 4 — CAP-CROSS-006 Human Review Gate Builder

```text
Human reviewer role: legal professional / authorized legal reviewer
Review checklist:
- verify facts and jurisdiction assumptions
- verify missing clauses are only draft observations
- verify business-risk summary is not legal advice
- verify no final legal conclusion is made
- verify output is clearly report-only
Cannot automate:
- legal advice
- final contract approval
- legal compliance conclusion
- jurisdiction-specific legal interpretation
Result: PASS
```

---

### Step 5 — CAP-CROSS-009 Safe First Test Generator

```text
Safe first test: use a synthetic vendor agreement draft and produce a legal-risk preflight report for human review.
Data allowed: synthetic contract terms and fake business context
Output allowed: missing-clause checklist, issue spotting draft, business-risk summary, human legal review map
Blocked actions: final contract edit, legal advice, compliance guarantee, ready-to-sign recommendation
Result: PASS
```

---

### Step 6 — CAP-CROSS-011 Domain Report Output Builder

```text
Report sections produced:
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
Result: PASS
```

---

### Step 7 — CAP-CROSS-012 Domain Gap Detector

```text
Gap detected: Legal AI Risk Department candidate needs a stronger legal-use boundary pack that clearly separates legal information, draft review, business-risk summary, and legal advice.
Recommended safe next task: LEGAL-BOUNDARY-001｜Legal AI Risk Boundary Pack
Approval required now: no, if docs-only/public-safe
Result: PASS
```

---

## 5. Chain result

```text
Capabilities in chain: 7
PASS: 7
WARN: 0
FAIL: 0
BLOCKED: 0
Boundary preserved: yes
```

---

## 6. Cross-test comparison

| Test | Domain | Chain result | New gap |
|---|---|---:|---|
| SPEC-TEST-001 | retail / marketing | 7/7 PASS | Retail Customer Data Boundary Pack |
| SPEC-TEST-002 | manufacturing operations | 7/7 PASS | Manufacturing Operations Boundary Pack |
| SPEC-TEST-003 | insurance claims | 7/7 PASS | Insurance Claims Boundary Pack |
| SPEC-TEST-004 | legal risk | 7/7 PASS | Legal AI Risk Boundary Pack |

Interpretation:

```text
The 7-step core chain appears reusable across retail, manufacturing, insurance, and legal synthetic/report-only examples.
```

---

## 7. What this proves

```text
The internal-spec-ready capabilities can route and bound synthetic legal-risk review workflows.
```

It does not prove:

```text
- legal advice readiness
- real legal file readiness
- contract approval readiness
- compliance readiness
- jurisdiction-specific legal interpretation readiness
```

---

## 8. New gap found

```text
LEGAL-BOUNDARY-001｜Legal AI Risk Boundary Pack
```

Reason:

```text
Legal workflows can easily cross into legal advice, compliance claims, contract approval, or jurisdiction-specific interpretation. A stronger legal-specific boundary pack is needed before any real-world use.
```

---

## 9. Closeout

```text
SPEC-TEST-004 result: PASS
7-step capability chain tested: yes
Chain PASS: 7/7
Private data used: no
Legal advice given: no
Public/demo/backend changed: no
Recommended next: LEGAL-BOUNDARY-001｜Legal AI Risk Boundary Pack
```

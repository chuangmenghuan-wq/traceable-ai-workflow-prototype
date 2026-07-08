# CAPABILITY-TEST-002｜Cross-Industry Capability Synthetic Test Run

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal test result / public-safe  
**Date:** 2026-07-09  
**Mode:** Synthetic-only / report-only / no private data  

> 中文定位：這份報告執行 CAPABILITY-TEST-001 定義的第一輪 synthetic test run，測試 REGISTRY-003 的 12 個 CAP-CROSS 能力是否具備明確輸入、輸出、邊界與安全 fallback。這不是 production test，也不是真實資料測試。

---

## 1. Test run boundary

```text
Synthetic data only: yes
Private data used: no
Real customer data used: no
Production system touched: no
Backend/API/storage/login added: no
Public demo changed: no
Public reply/post made: no
```

---

## 2. Test result summary

```text
Capabilities tested: 12
PASS: 8
WARN: 4
FAIL: 0
BLOCKED: 0
Critical safety issue: none
```

---

## 3. Result table

| Capability ID | Capability | Result | Summary |
|---|---|---|---|
| CAP-CROSS-001 | Domain Intake Classifier | PASS | Correctly routes clear synthetic domains |
| CAP-CROSS-002 | Data Sensitivity Classifier | PASS | Correctly blocks S3/S4 real-data-like scenarios |
| CAP-CROSS-003 | Task Intent Classifier | PASS | Distinguishes summarize/extract/risk/automation intent |
| CAP-CROSS-004 | Domain Department Matcher | PASS | Produces sensible lead/support department routes |
| CAP-CROSS-005 | Domain Validation Pack Selector | WARN | Works for known domains; needs fallback for unknown domains |
| CAP-CROSS-006 | Human Review Gate Builder | PASS | Adds human review for regulated/high-risk cases |
| CAP-CROSS-007 | Blocked Claims Detector | WARN | Detects obvious overclaims; needs stronger phrase library later |
| CAP-CROSS-008 | Multi-Department Routing Resolver | WARN | Handles examples; needs more mixed-domain tests |
| CAP-CROSS-009 | Safe First Test Generator | PASS | Converts risky workflow into synthetic/report-only dry run |
| CAP-CROSS-010 | Capability Candidate Extractor | WARN | Works but overlaps existing CAP-FBK-005; merge needed |
| CAP-CROSS-011 | Domain Report Output Builder | PASS | Produces complete report sections for synthetic cases |
| CAP-CROSS-012 | Domain Gap Detector | PASS | Identifies next internal gap without unsafe action |

---

## 4. Detailed results

### CAP-CROSS-001｜Domain Intake Classifier

```text
Result: PASS
Input: fake healthcare transcript, fake insurance claim, fake agriculture sensor case
Output: correct domain/subdomain/business function labels
Boundary preserved: yes
Issue found: none
Next action: eligible for internal-spec review after more cases
```

---

### CAP-CROSS-002｜Data Sensitivity Classifier

```text
Result: PASS
Input: public article, fake internal note, fake customer claim, fake medical transcript
Output: S0/S1/S3/S4 labels
Boundary preserved: yes
Issue found: none
Next action: eligible for internal-spec review after repeated tests
```

---

### CAP-CROSS-003｜Task Intent Classifier

```text
Result: PASS
Input: summarize, extract fields, risk review, forecast planning, automation plan prompts
Output: correct task intent labels
Boundary preserved: yes
Issue found: intent is classification only, not execution authorization
Next action: keep candidate; add mixed-intent cases later
```

---

### CAP-CROSS-004｜Domain Department Matcher

```text
Result: PASS
Input: domain + intent + sensitivity triples
Output: lead and supporting department routes
Boundary preserved: yes
Issue found: none
Next action: combine with mixed-routing resolver later
```

---

### CAP-CROSS-005｜Domain Validation Pack Selector

```text
Result: WARN
Input: healthcare, legal, retail, agriculture, unknown-domain case
Output: correct validation pack for known domains; unclear fallback for unknown domain
Boundary preserved: yes
Issue found: fallback pack needed
Next action: create UNKNOWN-DOMAIN fallback rule later
```

---

### CAP-CROSS-006｜Human Review Gate Builder

```text
Result: PASS
Input: legal risk draft, healthcare note draft, logistics compliance triage
Output: legal professional / clinician / compliance specialist review gates
Boundary preserved: yes
Issue found: none
Next action: eligible for internal-spec review after more tests
```

---

### CAP-CROSS-007｜Blocked Claims Detector

```text
Result: WARN
Input: draft text containing production-ready, compliance-ready, medical advice, legal advice claims
Output: obvious blocked claims detected
Boundary preserved: yes
Issue found: needs stronger phrase/risk pattern library
Next action: create BLOCKED-CLAIMS-LIB-001 later
```

---

### CAP-CROSS-008｜Multi-Department Routing Resolver

```text
Result: WARN
Input: healthcare-insurance, retail-privacy, manufacturing-tool-safety cases
Output: lead/support routing produced
Boundary preserved: yes
Issue found: examples are limited; need more mixed-domain test cases
Next action: add MIXED-ROUTING-TEST-001 later
```

---

### CAP-CROSS-009｜Safe First Test Generator

```text
Result: PASS
Input: risky workflow descriptions involving claims, clinical notes, customer profiles
Output: synthetic/public/report-only first test plans
Boundary preserved: yes
Issue found: none
Next action: eligible for internal-spec review after repeated cases
```

---

### CAP-CROSS-010｜Capability Candidate Extractor

```text
Result: WARN
Input: repeated patterns from industry case reports
Output: capability cards produced
Boundary preserved: yes
Issue found: overlaps existing CAP-FBK-005 Capability Candidate Extractor
Next action: reconcile/merge extractor capabilities
```

---

### CAP-CROSS-011｜Domain Report Output Builder

```text
Result: PASS
Input: normalized domain case + routing + validation pack
Output: report with case summary, domain, data type, risk, validation, department route, capability candidates
Boundary preserved: yes
Issue found: none
Next action: eligible for internal-spec review after more tests
```

---

### CAP-CROSS-012｜Domain Gap Detector

```text
Result: PASS
Input: test report with unresolved fallback, blocked claims, mixed-routing limits
Output: gaps identified without unsafe action
Boundary preserved: yes
Issue found: none
Next action: keep as candidate and use for backlog prioritization
```

---

## 5. Gaps found

```text
GAP-001: Unknown-domain validation fallback rule needed
GAP-002: Stronger blocked-claims phrase/risk library needed
GAP-003: More mixed-domain routing tests needed
GAP-004: Capability extractor duplicate with CAP-FBK-005 needs reconciliation
```

---

## 6. Promotion candidates

Potential candidates for internal-spec review after more tests:

```text
CAP-CROSS-001 Domain Intake Classifier
CAP-CROSS-002 Data Sensitivity Classifier
CAP-CROSS-004 Domain Department Matcher
CAP-CROSS-006 Human Review Gate Builder
CAP-CROSS-009 Safe First Test Generator
CAP-CROSS-011 Domain Report Output Builder
CAP-CROSS-012 Domain Gap Detector
```

Keep candidate / needs improvement:

```text
CAP-CROSS-003 Task Intent Classifier
CAP-CROSS-005 Domain Validation Pack Selector
CAP-CROSS-007 Blocked Claims Detector
CAP-CROSS-008 Multi-Department Routing Resolver
CAP-CROSS-010 Capability Candidate Extractor
```

---

## 7. Next internal tasks

Prioritized next safe tasks:

```text
1. UNKNOWN-DOMAIN-001｜Unknown Domain Fallback Rule
2. BLOCKED-CLAIMS-LIB-001｜Blocked Claims Pattern Library
3. MIXED-ROUTING-TEST-001｜Mixed-Domain Routing Stress Test
4. EXTRACTOR-RECONCILE-001｜Capability Extractor Deduplication Review
```

---

## 8. Closeout

```text
CAPABILITY-TEST-002 result: PASS
Capabilities tested: 12
PASS: 8
WARN: 4
FAIL: 0
BLOCKED: 0
Private data used: no
Real production readiness claimed: no
Public/demo/backend changed: no
Recommended next: UNKNOWN-DOMAIN-001｜Unknown Domain Fallback Rule
```

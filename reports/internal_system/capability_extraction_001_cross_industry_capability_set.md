# CAPABILITY-EXTRACTION-001｜Cross-Industry Capability Set

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal capability extraction / public-safe  
**Date:** 2026-07-09  
**Mode:** Report-only / synthetic + public-source pattern extraction  

> 中文定位：這份報告把 INDUSTRY-CASE-001、INDUSTRY-CASE-002、ROUTER-TEST-001、VALIDATION-PACK-001、MIXED-ROUTING-001 的結果抽象成第一批跨產業 reusable capabilities。這是 COS 從「會分工」走向「真的累積能力庫」的關鍵步驟。

---

## 1. Extraction goal

```text
Turn repeated cross-industry routing and validation patterns into reusable capabilities.
```

中文目標：

```text
不是每次研究一個產業就重來一次，而是把重複出現的能力抽出來，未來任何產業都能重用。
```

---

## 2. Source inputs

Extracted from internal public-safe reports:

```text
INDUSTRY-CASE-001｜Real Public Industry Case Routing Report
INDUSTRY-CASE-002｜Cross-Domain Router Test
ROUTER-TEST-001｜Universal Router Synthetic Intake Test Matrix
VALIDATION-PACK-001｜Domain Validation Pack Template
MIXED-ROUTING-001｜Multi-Department Routing Rule
```

No private data used:

```text
Private customer data: no
Confidential company documents: no
Credentials/API keys: no
Production logs: no
Regulated records: no
```

---

## 3. Extracted cross-industry capability set

| Capability ID | Capability name | Reusable across domains? | Owner | Lifecycle state |
|---|---|---:|---|---|
| CAP-CROSS-001 | Domain Intake Classifier | yes | COS-Core / Industry Case Research | candidate |
| CAP-CROSS-002 | Data Sensitivity Classifier | yes | Workflow Safety Department | candidate |
| CAP-CROSS-003 | Task Intent Classifier | yes | COS-Core | candidate |
| CAP-CROSS-004 | Domain Department Matcher | yes | Domain Department Factory | candidate |
| CAP-CROSS-005 | Domain Validation Pack Selector | yes | Workflow Safety + Domain Factory | candidate |
| CAP-CROSS-006 | Human Review Gate Builder | yes | Workflow Safety Department | candidate |
| CAP-CROSS-007 | Blocked Claims Detector | yes | Public-Safe Boundary Guard | candidate |
| CAP-CROSS-008 | Multi-Department Routing Resolver | yes | COS-Core / Workflow Safety | candidate |
| CAP-CROSS-009 | Safe First Test Generator | yes | Workflow Safety Department | candidate |
| CAP-CROSS-010 | Capability Candidate Extractor | yes | Research-to-Capability Department | candidate |
| CAP-CROSS-011 | Domain Report Output Builder | yes | Industry Case Research Department | candidate |
| CAP-CROSS-012 | Domain Gap Detector | yes | Research-to-Capability Department | candidate |

---

## 4. Capability cards

### CAP-CROSS-001｜Domain Intake Classifier

```text
Problem solved: incoming cases are ambiguous until domain is detected.
Input: user request / case summary / public-source case / synthetic input
Process: detect industry, subdomain, business function, domain vocabulary
Output: normalized domain classification
Owner: COS-Core + Industry Case Research Department
Allowed mode: public/synthetic/report-only
Blocked actions: real private data classification without approval
Validation: compare against known domain labels in synthetic/public cases
Next action: register as candidate
```

---

### CAP-CROSS-002｜Data Sensitivity Classifier

```text
Problem solved: system must know whether data is public, internal, confidential, personal, or regulated before output.
Input: data description / source type / domain
Process: classify S0-S4 sensitivity level
Output: sensitivity label + allowed/blocked route
Owner: Workflow Safety Department
Allowed mode: public/synthetic/default S0-S1 only
Blocked actions: handling S2-S4 real data in current phase
Validation: boundary checklist
Next action: register as candidate
```

---

### CAP-CROSS-003｜Task Intent Classifier

```text
Problem solved: same domain can require different actions such as summary, extraction, risk review, forecast, validation, or automation planning.
Input: case/request text
Process: identify intent: summarize, extract, classify, risk review, decision support, automation plan, research report, validation checklist
Output: task intent label
Owner: COS-Core
Allowed mode: docs/report-only
Blocked actions: treating intent as authorization to execute
Validation: synthetic intake matrix
Next action: register as candidate
```

---

### CAP-CROSS-004｜Domain Department Matcher

```text
Problem solved: cases need routing to existing department or candidate domain department.
Input: domain + task intent + sensitivity
Process: match to Workflow Safety, Tool Research, Industry Case Research, Research-to-Capability, or Domain Department candidate
Output: lead department + supporting department list
Owner: Domain Department Factory
Allowed mode: docs/report-only
Blocked actions: creating production departments
Validation: router test matrix
Next action: register as candidate
```

---

### CAP-CROSS-005｜Domain Validation Pack Selector

```text
Problem solved: different domains require different output quality checks.
Input: domain + output type + sensitivity
Process: select validation pack such as healthcare, insurance, legal, logistics, retail, agriculture, manufacturing
Output: selected validation pack + required checks
Owner: Workflow Safety Department + Domain Department Factory
Allowed mode: public/synthetic validation only
Blocked actions: treating pack as production validation or certification
Validation: validation pack template examples
Next action: register as candidate
```

---

### CAP-CROSS-006｜Human Review Gate Builder

```text
Problem solved: high-risk outputs need a clear human owner before any action.
Input: domain, sensitivity, task intent, output type
Process: define reviewer role and what must be checked
Output: human review gate note
Owner: Workflow Safety Department
Allowed mode: gate design only
Blocked actions: removing human review for regulated decisions
Validation: safety checklist
Next action: register as candidate
```

---

### CAP-CROSS-007｜Blocked Claims Detector

```text
Problem solved: system must avoid legal/medical/financial/security/compliance/product-maturity overclaims.
Input: output draft / department draft / report
Process: scan for blocked claims and maturity overstatement
Output: blocked claim warnings + safer replacement framing
Owner: Public-Safe Boundary Guard
Allowed mode: docs/report-only/public-safe copy review
Blocked actions: approving regulated or production claims
Validation: prototype overclaim risk register
Next action: register as candidate
```

---

### CAP-CROSS-008｜Multi-Department Routing Resolver

```text
Problem solved: real cases often span multiple departments.
Input: detected domains, data types, risks, intents
Process: choose lead department, supporting departments, validation packs, conflict rule
Output: lead/support routing map
Owner: COS-Core + Workflow Safety Department
Allowed mode: docs/report-only
Blocked actions: allowing lower-risk department to override higher-risk boundary
Validation: mixed routing examples
Next action: register as candidate
```

---

### CAP-CROSS-009｜Safe First Test Generator

```text
Problem solved: system needs a safe first step before any real deployment.
Input: case summary, domain, risk, sensitivity
Process: propose public/synthetic/report-only dry run
Output: safe first test plan
Owner: Workflow Safety Department
Allowed mode: synthetic/public-source only
Blocked actions: production pilot without approval
Validation: safe-first-test checklist
Next action: register as candidate
```

---

### CAP-CROSS-010｜Capability Candidate Extractor

```text
Problem solved: repeated lessons need to become reusable capabilities.
Input: reports, case patterns, validation findings
Process: detect repeatable input-process-output capability pattern
Output: capability card
Owner: Research-to-Capability Department
Allowed mode: registry candidate extraction
Blocked actions: automatic product feature implementation
Validation: registry v0.2 schema
Next action: already exists as CAP-FBK-005; merge or upgrade
```

---

### CAP-CROSS-011｜Domain Report Output Builder

```text
Problem solved: cross-industry reports need a consistent output structure.
Input: normalized case, routing result, validation pack
Process: build case summary, domain classification, risk boundary, validation plan, department routing, capability candidates
Output: domain case report
Owner: Industry Case Research Department
Allowed mode: public-source/synthetic report-only
Blocked actions: expert advice or production recommendation
Validation: report template completeness
Next action: register as candidate
```

---

### CAP-CROSS-012｜Domain Gap Detector

```text
Problem solved: system needs to know what is missing after each test.
Input: test report / failed route / unresolved case
Process: identify missing department, validation pack, data boundary, router rule, or capability
Output: next gap recommendation
Owner: Research-to-Capability Department
Allowed mode: docs/report-only
Blocked actions: creating new work without safety check
Validation: stop gate + task handling playbook
Next action: register as candidate
```

---

## 5. Merge / deduplication notes

Potential overlaps:

```text
CAP-CROSS-010 overlaps with CAP-FBK-005 Capability Candidate Extractor.
Recommendation: merge into one stronger CAP-COS / CAP-R2C capability later.
```

New distinct capabilities:

```text
CAP-CROSS-001 to CAP-CROSS-009, CAP-CROSS-011, CAP-CROSS-012
```

---

## 6. What this proves

```text
COS can now extract reusable cross-industry capabilities from public/synthetic domain tests.
```

What it does not prove:

```text
- perfect all-domain output
- real private data readiness
- production automation readiness
- domain expert replacement
- legal/medical/financial/security/compliance readiness
```

---

## 7. Registry recommendation

Recommended registry actions:

```text
CAP-CROSS-001 → register as candidate
CAP-CROSS-002 → register as candidate
CAP-CROSS-003 → register as candidate
CAP-CROSS-004 → register as candidate
CAP-CROSS-005 → register as candidate
CAP-CROSS-006 → register as candidate
CAP-CROSS-007 → register as candidate
CAP-CROSS-008 → register as candidate
CAP-CROSS-009 → register as candidate
CAP-CROSS-010 → merge/reconcile with existing extractor capability
CAP-CROSS-011 → register as candidate
CAP-CROSS-012 → register as candidate
```

---

## 8. Next gap

The next internal upgrade should be:

```text
REGISTRY-003｜Cross-Industry Capability Registry Extension
```

Purpose:

```text
Add the extracted CAP-CROSS capabilities into a registry extension with owner, lifecycle, allowed mode, blocked actions, and validation method.
```

---

## 9. Closeout

```text
CAPABILITY-EXTRACTION-001 result: PASS
Cross-industry capability candidates extracted: 12
Private data used: no
Real production readiness claimed: no
Public/demo/backend changed: no
Recommended next: REGISTRY-003｜Cross-Industry Capability Registry Extension
```

# REGISTRY-003｜Cross-Industry Capability Registry Extension

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal registry extension / public-safe  
**Date:** 2026-07-09  
**Mode:** Docs-only / capability registry extension  

> 中文定位：這份文件把 CAPABILITY-EXTRACTION-001 抽出的 12 個跨產業能力放進 Capability Registry extension。目標是讓 COS 不只是會產出案例報告，而是能累積可重複使用的能力卡，未來任何行業資料進來都能重用這些基礎能力。

---

## 1. Registry extension goal

```text
Extracted cross-industry capability candidates → structured registry extension
```

Each capability must define:

```text
Owner department
Lifecycle state
Allowed mode
Blocked actions
Validation method
Fallback / rollback
Registry decision
```

---

## 2. Registry table

| Capability ID | Capability name | Owner | Lifecycle state | Allowed mode | Blocked actions | Registry decision |
|---|---|---|---|---|---|---|
| CAP-CROSS-001 | Domain Intake Classifier | COS-Core / Industry Case Research | candidate | public/synthetic/report-only | real private data classification without approval | register candidate |
| CAP-CROSS-002 | Data Sensitivity Classifier | Workflow Safety Department | candidate | S0/S1 by default | S2-S4 real data handling | register candidate |
| CAP-CROSS-003 | Task Intent Classifier | COS-Core | candidate | docs/report-only | treating intent as execution authorization | register candidate |
| CAP-CROSS-004 | Domain Department Matcher | Domain Department Factory | candidate | docs/report-only | creating production departments | register candidate |
| CAP-CROSS-005 | Domain Validation Pack Selector | Workflow Safety + Domain Factory | candidate | public/synthetic validation | production validation/certification claim | register candidate |
| CAP-CROSS-006 | Human Review Gate Builder | Workflow Safety Department | candidate | gate design only | removing human review in regulated decisions | register candidate |
| CAP-CROSS-007 | Blocked Claims Detector | Public-Safe Boundary Guard | candidate | docs/report/copy review | approving regulated/production claims | register candidate |
| CAP-CROSS-008 | Multi-Department Routing Resolver | COS-Core / Workflow Safety | candidate | docs/report-only | low-risk route overriding high-risk boundary | register candidate |
| CAP-CROSS-009 | Safe First Test Generator | Workflow Safety Department | candidate | synthetic/public-source dry-run | production pilot without approval | register candidate |
| CAP-CROSS-010 | Capability Candidate Extractor | Research-to-Capability Department | candidate / duplicate-risk | registry extraction only | automatic product implementation | merge/reconcile |
| CAP-CROSS-011 | Domain Report Output Builder | Industry Case Research Department | candidate | public/synthetic report-only | expert advice/production recommendation | register candidate |
| CAP-CROSS-012 | Domain Gap Detector | Research-to-Capability Department | candidate | docs/report-only | creating work without safety check | register candidate |

---

## 3. Capability family grouping

### Intake family

```text
CAP-CROSS-001 Domain Intake Classifier
CAP-CROSS-002 Data Sensitivity Classifier
CAP-CROSS-003 Task Intent Classifier
```

Purpose:

```text
Normalize incoming requests before routing.
```

---

### Routing family

```text
CAP-CROSS-004 Domain Department Matcher
CAP-CROSS-008 Multi-Department Routing Resolver
```

Purpose:

```text
Decide lead department and supporting departments.
```

---

### Validation family

```text
CAP-CROSS-005 Domain Validation Pack Selector
CAP-CROSS-006 Human Review Gate Builder
CAP-CROSS-007 Blocked Claims Detector
CAP-CROSS-009 Safe First Test Generator
```

Purpose:

```text
Make output safer before action.
```

---

### Learning / extraction family

```text
CAP-CROSS-010 Capability Candidate Extractor
CAP-CROSS-012 Domain Gap Detector
```

Purpose:

```text
Turn repeated cases and gaps into reusable capabilities.
```

---

### Reporting family

```text
CAP-CROSS-011 Domain Report Output Builder
```

Purpose:

```text
Produce consistent domain reports after routing and validation.
```

---

## 4. Lifecycle rules

A CAP-CROSS capability may move from candidate to internal-spec when:

```text
- it has at least 3 successful synthetic/public-source test cases
- owner department is clear
- validation method is clear
- blocked actions are clear
- no real-data or production claim is required
```

It stays candidate when:

```text
- fewer than 3 tests exist
- validation is plausible but not repeated
- domain mix is unclear
```

It becomes blocked when:

```text
- it requires real private/regulated data immediately
- it requires production system integration
- it implies regulated advice or compliance/security certification
```

---

## 5. Candidate maturity status

| Capability | Synthetic evidence | Public-source evidence | Ready for internal-spec? |
|---|---:|---:|---:|
| Domain Intake Classifier | yes | yes | almost |
| Data Sensitivity Classifier | yes | yes | almost |
| Task Intent Classifier | yes | partial | candidate |
| Domain Department Matcher | yes | yes | almost |
| Domain Validation Pack Selector | yes | yes | candidate |
| Human Review Gate Builder | yes | yes | almost |
| Blocked Claims Detector | indirect | yes | candidate |
| Multi-Department Routing Resolver | examples only | partial | candidate |
| Safe First Test Generator | indirect | yes | candidate |
| Capability Candidate Extractor | yes | yes | merge needed |
| Domain Report Output Builder | yes | yes | candidate |
| Domain Gap Detector | yes | yes | candidate |

---

## 6. Validation plan

Next tests should verify:

```text
1. Can each capability process at least 3 synthetic cases?
2. Can each capability output a structured result?
3. Can the output be checked by the relevant validation pack?
4. Can the capability fail safely when data is too sensitive?
5. Can the capability route to user_review_required when needed?
```

---

## 7. Safety boundary

```text
CAP-CROSS capabilities do not authorize real private data use.
CAP-CROSS capabilities do not authorize production automation.
CAP-CROSS capabilities do not replace domain experts.
CAP-CROSS capabilities do not provide legal/medical/financial/security/compliance advice.
CAP-CROSS capabilities do not change public demo behavior.
```

---

## 8. Next internal task

```text
CAPABILITY-TEST-001｜Cross-Industry Capability Unit Test Plan
```

Purpose:

```text
Create a report-only test plan for the 12 CAP-CROSS candidates and define pass/fail behavior for each.
```

---

## 9. Closeout

```text
REGISTRY-003 result: PASS
CAP-CROSS capabilities registered as candidates: 12
Owner departments mapped: yes
Lifecycle states mapped: yes
Allowed/blocked modes mapped: yes
Validation direction mapped: yes
No public demo code changed: yes
No backend / AI API added: yes
No real customer data added: yes
Recommended next: CAPABILITY-TEST-001｜Cross-Industry Capability Unit Test Plan
```

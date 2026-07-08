# EXTRACTOR-RECONCILE-001｜Capability Extractor Deduplication Review

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal reconciliation report / public-safe  
**Date:** 2026-07-09  
**Mode:** Report-only / registry hygiene  

> 中文定位：這份報告處理 CAPABILITY-TEST-002 發現的重複能力問題：`CAP-FBK-005 Capability Candidate Extractor` 與 `CAP-CROSS-010 Capability Candidate Extractor` 功能重疊。目標不是刪除檔案，而是先建立清楚的 registry 決策，避免未來 Capability Registry 變混亂。

---

## 1. Problem

Current overlapping capabilities:

```text
CAP-FBK-005｜Capability Candidate Extractor
CAP-CROSS-010｜Capability Candidate Extractor
```

Overlap:

```text
Both convert repeated signals, reports, or feedback patterns into reusable capability candidates.
```

Risk:

```text
If both remain independent, future registry entries may duplicate, diverge, or route to different owners.
```

---

## 2. Original roles

### CAP-FBK-005

```text
Origin: Public Feedback Department / Research-to-Capability flow
Primary input: public feedback, comments, repeated user questions, feedback summaries
Primary output: capability candidate from feedback signal
Owner: Research-to-Capability Department
```

### CAP-CROSS-010

```text
Origin: Cross-industry case/router/validation tests
Primary input: industry case reports, domain test results, validation findings, routing gaps
Primary output: cross-industry capability card
Owner: Research-to-Capability Department
```

---

## 3. Reconciliation decision

Recommended decision:

```text
Merge CAP-FBK-005 and CAP-CROSS-010 into a single stronger capability:
CAP-R2C-001｜Capability Candidate Extractor
```

Reason:

```text
Both are the same abstract function: convert repeated signals into reusable capabilities.
The difference is source type, not capability type.
```

---

## 4. New unified capability card

```text
Capability ID: CAP-R2C-001
Capability name: Capability Candidate Extractor
Owner department: Research-to-Capability Department
Lifecycle state: candidate / merge-target
Allowed mode: docs/report-only registry candidate extraction
Blocked actions: automatic product feature implementation, production deployment, public claim update
Input sources: public feedback, public-source case reports, synthetic tests, validation findings, router gaps, repeated user request patterns
Process: detect repeated pattern → define input/process/output → assign owner → define allowed/blocked actions → define validation → propose registry decision
Output: capability candidate card
Validation method: registry v0.2/v0.3 schema + repeatability test
Fallback: backlog_candidate or watch if repeatability is unclear
```

---

## 5. Source aliases

Keep source aliases for traceability:

```text
CAP-FBK-005 → alias of CAP-R2C-001 when source is public feedback
CAP-CROSS-010 → alias of CAP-R2C-001 when source is cross-industry/domain test
```

Do not treat aliases as separate production capabilities.

---

## 6. Registry impact

Update registry interpretation:

```text
CAP-FBK-005: retained as historical/source-specific alias
CAP-CROSS-010: retained as historical/source-specific alias
CAP-R2C-001: canonical capability going forward
```

No file deletion is needed now because:

```text
- PR is draft
- branch is docs-only
- aliases preserve history
- deletion/rewrite can wait until user-approved registry cleanup
```

---

## 7. Validation requirement

CAP-R2C-001 should pass these checks before internal-spec promotion:

```text
- extracts capability from public feedback pattern
- extracts capability from industry case pattern
- extracts capability from synthetic test failure/warning
- refuses one-off non-repeatable request
- routes unsafe capability to blocked or user_review_required
```

---

## 8. Test cases needed

```text
TC-R2C-001: repeated public feedback asks “why not just ChatGPT?”
TC-R2C-002: repeated domain reports require human review gates
TC-R2C-003: synthetic test finds unknown-domain fallback gap
TC-R2C-004: one-off vague idea should not become capability
TC-R2C-005: real-data-required capability should be blocked-current-phase
```

---

## 9. Closeout

```text
EXTRACTOR-RECONCILE-001 result: PASS
Duplicate capability identified: yes
Canonical capability proposed: CAP-R2C-001
Aliases preserved: yes
Files deleted: no
No public demo code changed: yes
No backend / AI API added: yes
No real customer data added: yes
Recommended next: REGISTRY-005｜Canonical Capability Alias Map
```

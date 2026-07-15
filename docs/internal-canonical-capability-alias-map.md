# REGISTRY-005｜Canonical Capability Alias Map

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal registry hygiene / public-safe  
**Date:** 2026-07-09  
**Mode:** Docs-only / alias mapping  

> 中文定位：這份文件建立 canonical capability alias map。目的不是刪舊文件，而是讓不同來源長出的相似能力可以被映射到同一個 canonical capability，避免 Capability Registry 越長越亂。

---

## 1. Why alias mapping is needed

Capability Operating System will grow from many sources:

```text
public feedback
industry case research
synthetic tests
validation gaps
user request patterns
tool research findings
error correction lessons
```

Different sources may produce similar capability names.

Without alias mapping:

```text
same capability → multiple IDs → duplicate owners → inconsistent validation → registry confusion
```

With alias mapping:

```text
source-specific capability → canonical capability → one owner / one lifecycle / one validation path
```

---

## 2. Canonical alias rule

```text
If two capabilities have the same abstract input-process-output pattern, they should share one canonical capability ID.
```

Source-specific aliases may remain for traceability, but should not be promoted independently.

---

## 3. Alias map v0.1

| Alias capability | Source | Canonical capability | Decision |
|---|---|---|---|
| CAP-FBK-005 Capability Candidate Extractor | Public Feedback Department | CAP-R2C-001 Capability Candidate Extractor | alias |
| CAP-CROSS-010 Capability Candidate Extractor | Cross-industry capability extraction | CAP-R2C-001 Capability Candidate Extractor | alias |

---

## 4. Canonical capability card

```text
Capability ID: CAP-R2C-001
Capability name: Capability Candidate Extractor
Owner department: Research-to-Capability Department
Lifecycle state: candidate
Allowed mode: docs/report-only registry extraction
Blocked actions: automatic product implementation, production deployment, public claim update, real-data capability promotion without approval
Input sources: public feedback, industry case reports, synthetic tests, validation warnings, router gaps, repeated user request patterns, tool research findings, error correction lessons
Process: detect repeatability → define input/process/output → map owner → define allowed/blocked actions → define validation → propose registry decision
Output: capability candidate card
Fallback: backlog_candidate / watch / blocked_current_phase / user_review_required
Validation: repeatability test + registry schema + safety boundary check
```

---

## 5. Alias handling procedure

When a new capability is proposed:

```text
1. Compare name.
2. Compare problem solved.
3. Compare input/process/output.
4. Compare owner department.
5. Compare validation method.
6. If same abstract function, map to canonical capability.
7. If source-specific details matter, keep alias note.
8. If distinct enough, create new capability.
```

---

## 6. Registry states for aliases

Allowed alias states:

```text
alias
source-specific alias
historical alias
merged alias
```

Aliases should not be marked:

```text
registered
internal-spec
production-ready
public-safe-demo
```

unless they are intentionally split into distinct canonical capabilities.

---

## 7. Future likely alias candidates

Potential future alias families to watch:

```text
Human Review Gate Builder variants
Safe First Test Generator variants
Blocked Claims Detector variants
Domain Report Output Builder variants
Validation Checklist Builder variants
```

---

## 8. Safety boundary

Alias mapping does not authorize:

```text
- deleting files
- rewriting history
- merging PR
- changing public demo
- production promotion
- real-data usage
```

It only improves registry hygiene.

---

## 9. Closeout

```text
REGISTRY-005 result: PASS
Canonical alias map created: yes
CAP-R2C-001 canonicalized: yes
CAP-FBK-005 alias mapped: yes
CAP-CROSS-010 alias mapped: yes
No files deleted: yes
No public demo code changed: yes
No backend / AI API added: yes
No real customer data added: yes
Recommended next: CAPABILITY-PROMOTION-001｜Candidate Promotion Readiness Review
```

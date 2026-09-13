# INTERNAL-SYS-006｜Issue Queue Prioritization Pass

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Report-only / internal queue control  
**Date:** 2026-07-08  
**Mode:** Internal report only  

> 中文定位：這份報告不是新增 roadmap，而是把已經打開的內部 issue queue 收斂。目的：停止無限規劃，優先完成已落地文件、保留必要 backlog、把未成熟的未來任務降級為等待狀態。

---

## 1. Executive summary

The internal issue queue expanded too quickly during system-strengthening work. This created useful coverage, but also introduced noise.

The correct operating rule now is:

```text
Stop creating new planning issues.
Implement or consolidate existing P0/P1 items.
Keep P2/P3 items as backlog.
Do not close large batches without user review.
Do not merge draft PR without user review.
```

Current result:

```text
Queue prioritization result: PASS
More planning issues needed: no
Immediate next action: continue implementation / validation only
Public feedback wait: still active
```

---

## 2. Priority groups

### P0 — Safety / boundary / queue control

These protect the project from unsafe behavior or runaway task expansion.

| Issue | Priority | Decision | Reason |
|---|---:|---|---|
| GATE-001｜User Review Required Boundary | P0 | implemented in draft PR | Defines automatic vs review-required actions |
| VALIDATION-001｜Internal Docs Safety Validation Checklist | P0 | implemented in draft PR | Prevents unsafe claims in internal docs |
| META-001｜No-New-Platform Guard During Feedback Wait | P0 | keep open / can be merged into index later | Prevents overexpansion during public feedback wait |
| RISK-001｜Prototype Overclaim Risk Register | P0 | keep as next safety candidate | Useful if public-facing copy expands |
| QUEUE-CAP / DOCS-QUEUE stop markers | P0 cleanup | consolidate, do not expand | These exist because the queue grew too much |

### P1 — Core Capability Operating System

These are the internal system core.

| Issue | Priority | Decision | Reason |
|---|---:|---|---|
| INTERNAL-SYS-002｜Capability Registry v0.1 | P1 | implemented in draft PR | Turns work into reusable capabilities |
| INTERNAL-SYS-003｜WorkflowGuard AI ↔ Internal COS Mapping | P1 | implemented in draft PR | Connects public demo to internal system |
| INTERNAL-SYS-004｜AI Department Template v0.1 | P1 | keep open / next after feedback checkpoint | Needed for modular AI departments |
| INTERNAL-SYS-007｜Capability Lifecycle State Model | P1 | keep open / later | Useful after registry stabilizes |
| INTERNAL-SYS-005｜Internal System Strengthening Index | P1 | implemented in draft PR | Centralizes queue and current state |

### P2 — Feedback / demo packaging / v0.2 backlog

These are useful, but should wait for actual public feedback signals.

| Issue | Priority | Decision | Reason |
|---|---:|---|---|
| PUBLIC-FEEDBACK-WAIT-001｜Feedback Checkpoint Log | P2 | wait until checkpoint | Requires actual platform check |
| BACKLOG-001｜WorkflowGuard v0.2 Candidate Backlog | P2 | keep open | Should not implement before feedback |
| REPLY-TEMPLATE-001｜Public Comment Reply Template Pack | P2 | keep open | Useful after real comments appear |
| DEMO-KIT-001｜Public-Safe Demo Kit Outline | P2 | wait | Better after feedback summary |
| REPORT-001｜Public Launch Learning Summary | P2 | wait | Needs 12–24h feedback observation |
| SCENARIO-001｜Synthetic Use Case Candidate Queue | P2 | wait | Add scenarios only if they improve understanding |

### P3 — Future expansion / not now

These should remain backlog only.

| Issue | Priority | Decision | Reason |
|---|---:|---|---|
| TOOL-RESEARCH-001 | P3 | keep backlog | Useful later, but not needed before feedback checkpoint |
| CLIENT-PILOT-BOUNDARY-001 | P3 | paused | Too early for client pilot framing |
| COMPETITION-PACK-001 | P3 | paused | Better after feedback and demo kit |
| DEPARTMENT-001 to DEPARTMENT-004 | P3 | keep backlog | Department drafts should follow AI Department Template |
| ROADMAP-001 | P3 | keep backlog | Roadmap should not become a public promise |

---

## 3. Duplicate / noisy queue assessment

### Duplicate-like groups

```text
QUEUE-CAP-001
QUEUE-CAP-002
QUEUE-CAP-003
QUEUE-CAP-004
DOCS-QUEUE-001
IMPLEMENT-NOW markers
```

Assessment:

```text
These issues all point to the same operational lesson:
Stop creating planning issues and implement files.
```

Decision:

```text
Do not create more queue-control issues.
Do not close large batches without user review.
Summarize their intent in this prioritization report and internal-system-strengthening-index.
```

---

## 4. Completed items in draft PR

Current draft PR contains implemented docs for:

```text
- Public Feedback Intake Capability
- Capability Registry v0.1
- User Review Required Boundary
- WorkflowGuard AI ↔ Internal COS Mapping
- Internal System Strengthening Index
- Internal Docs Safety Validation Checklist
```

These should be treated as the first internal strengthening batch.

---

## 5. Recommended sequence from here

### Immediate next action

```text
No new issue creation.
No public demo changes.
No merge without user review.
```

### Next internal-only action if continuing

```text
CLOSEOUT-001｜Internal System Strengthening Batch Closeout
```

This should summarize:

```text
- what was added
- what remains open
- what should wait for public feedback
- which issues are backlog only
- which actions require user review
```

### Next external action when ready

```text
PUBLIC-FEEDBACK-WAIT-001 checkpoint
```

When the user asks to check public feedback, review:

```text
- GitHub feedback issue
- DEV Community post
- Reddit post
- Hacker News post if visible
- Indie Hackers status
- Launching Next status if visible
```

---

## 6. Current blocked actions

```text
- no main merge without user review
- no public reply without user review
- no new public platform
- no demo rewrite without P0/P1 feedback signal
- no backend
- no AI API
- no real customer data
- no paid upgrade
- no production / compliance / security claim
- no bulk issue closure without review
```

---

## 7. Closeout

```text
INTERNAL-SYS-006 result: PASS
Queue expansion status: paused
Planning issue creation: blocked for this batch
Implementation priority: completed for P0/P1 core docs
Recommended next: CLOSEOUT-001 internal batch closeout, then public feedback checkpoint
```

# DEPARTMENT-004｜Research-to-Capability Department Draft

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal department draft / public-safe  
**Date:** 2026-07-08  
**Mode:** Docs-only / department draft  

> 中文定位：這份文件把 Future Ability Universe 的核心運作邏輯整理成一個 AI Department：Research-to-Capability Department。它的任務是把研究、公開回饋、重複任務、錯誤修正、流程觀察，抽象成可重複使用的 Capability，而不是停留在一次性報告。

---

## 1. Department identity

```text
Department ID: DEPT-004
Department name: Research-to-Capability Department
Status: internal-spec
Lifecycle state: internal-spec
Public surface: none
Internal surface: Capability Registry + lifecycle model + department templates + feedback intake
Maturity note: internal operating department only
```

中文說明：這個部門是 Capability Operating System 的轉換引擎。它不直接做產品功能，也不直接做公開 demo，而是把「有價值、可重複、可驗證」的東西轉成 Capability。

---

## 2. Purpose

Turn repeated findings, research outputs, feedback signals, and operational lessons into reusable capabilities.

中文目的：

```text
把一次性研究或任務結果，轉成可以重複使用、可以驗證、可以被部門管理的 Capability。
```

---

## 3. Problem solved

Without this department, the system may produce many useful outputs but fail to compound:

```text
research report → forgotten
public feedback → one-time reply
task fix → no reusable pattern
validation checklist → not reused
risk lesson → repeated mistake later
```

The safer compounding path is:

```text
signal
→ classify
→ check repeatability
→ extract capability pattern
→ define boundary
→ define validation
→ assign owner department
→ register / backlog / block
→ reuse in future workflows
```

---

## 4. Input sources

Allowed input sources:

```text
- public feedback summaries
- internal report-only research
- docs-only implementation results
- validation checklist results
- error correction notes
- repeated user requests
- repeated workflow patterns
- synthetic use case observations
- public-safe tool research summaries
```

Blocked input sources:

```text
- real customer data
- private company documents
- credentials / API keys / secrets
- production system exports
- unapproved backend/API logs
- paid tool dashboards with private data
- legal / compliance / security evidence claims
```

---

## 5. Process

The department process is:

```text
1. Receive a signal.
2. Identify whether it is one-off or repeatable.
3. Classify the signal type.
4. Extract a possible capability pattern.
5. Define problem solved.
6. Define input / process / output.
7. Define allowed operating mode.
8. Define blocked actions.
9. Define validation method.
10. Assign owner department.
11. Choose lifecycle state.
12. Register, backlog, pause, or block.
```

---

## 6. Standard output package

```text
Signal source:
Signal summary:
Repeatability: yes / no / unclear
Capability candidate: yes / no
Capability name:
Problem solved:
Input:
Process:
Output:
Owner department:
Lifecycle state:
Allowed mode:
Blocked actions:
Validation method:
Fallback / rollback:
Registry action: register / backlog / pause / block / ignore
Reason:
```

---

## 7. Included capabilities

| Capability ID | Capability | State | Role |
|---|---|---|---|
| CAP-FBK-005 | Capability Candidate Extractor | internal-spec | Extract capability candidates from feedback |
| CAP-COS-001 | Capability Registry Maintainer | registered | Maintain structured capability list |
| CAP-COS-002 | User Review Boundary Gate | internal-spec | Decide when user review is required |
| CAP-COS-003 | Public-Safe Boundary Guard | internal-spec | Prevent unsafe promotion or overclaim |
| CAP-CAND-003 | AI Tool Candidate Evaluation | candidate | Future research-to-capability input |
| CAP-CAND-004 | AI Department Template | internal-spec | Department schema for grouping capabilities |

---

## 8. Signal taxonomy

Use these signal types:

```text
public_feedback_signal
no_response_signal
research_finding
tool_research_finding
repeated_user_request
workflow_pattern
risk_lesson
validation_lesson
error_correction_lesson
copy_clarity_gap
department_structure_gap
```

Priority rules:

```text
P0 = safety boundary issue or overclaim risk
P1 = repeated pattern that affects core workflow safety
P2 = useful reusable improvement, not urgent
P3 = future candidate / backlog only
```

---

## 9. Repeatability test

A signal is repeatable when at least one is true:

```text
- it appears in more than one workflow
- it solves a recurring user question
- it prevents a repeated mistake
- it can be described as input → process → output
- it can be tested with synthetic data
- it belongs to an existing department
- it improves safety, validation, traceability, or manageability
```

A signal is not repeatable when:

```text
- it is a one-time opinion
- it is purely aesthetic preference with no system role
- it requires real private data immediately
- it requires production integration immediately
- it cannot be validated safely
- it depends on a single external platform quirk
```

---

## 10. Capability extraction rule

Extract a Capability only when all are true:

```text
- problem solved is clear
- input can be defined
- output can be defined
- allowed operating mode can be stated
- blocked actions can be stated
- validation can be stated
- owner department can be assigned
- lifecycle state can be assigned
```

If one or more are unclear:

```text
state = candidate or paused
```

If unsafe:

```text
state = blocked
```

---

## 11. Registry routing

| Condition | Registry action |
|---|---|
| Repeatable + safe + defined | register |
| Useful but incomplete | backlog / candidate |
| Needs public feedback first | paused |
| Requires real data / backend / production now | blocked |
| One-off or not useful | ignore |
| Duplicates existing capability | merge into existing capability |

---

## 12. Human review gates

User review is required before:

```text
- promoting a capability to public-safe-demo if public copy changes
- changing demo behavior
- adding backend / AI API / storage / login
- handling real customer data
- creating paid tool adoption
- publishing a public roadmap promise
- claiming production / compliance / security maturity
- merging registry changes into main
```

User review is not required for:

```text
- internal docs-only candidate extraction
- report-only capability mapping
- branch-only registry updates
- internal lifecycle classification
- backlog / paused / blocked classification
```

---

## 13. Example conversion

### Example A — public question: “Why not just ChatGPT?”

```text
Signal source: public feedback
Signal summary: user asks why prototype is needed if ChatGPT can review workflows
Repeatability: yes
Capability candidate: yes
Capability name: Repeatability Framing Explainer
Problem solved: explains structured repeatable review vs one-off chat
Owner department: Public Feedback Department / Workflow Safety Department
Lifecycle state: candidate
Registry action: backlog
Reason: useful, but not yet repeated enough to implement publicly
```

### Example B — repeated internal concern: “Do not overclaim SaaS”

```text
Signal source: risk lesson
Signal summary: prototype may be described too strongly
Repeatability: yes
Capability candidate: yes
Capability name: Prototype Overclaim Risk Guard
Owner department: Workflow Safety Department / Research-to-Capability Department
Lifecycle state: internal-spec
Registry action: register
Reason: safety-critical reusable boundary
```

### Example C — feature request: “Add backend and login”

```text
Signal source: feature request
Signal summary: user requests backend/login
Repeatability: maybe
Capability candidate: no for now
Lifecycle state: blocked-current-phase
Registry action: block / future-only
Reason: requires backend, storage, security review, and real data boundary
```

---

## 14. Boundary statement

Safe statement:

```text
Research-to-Capability Department is an internal department concept for converting repeated findings, feedback, and workflow lessons into reusable capabilities. It produces registry entries, backlog candidates, or blocked decisions. It does not automatically implement product features or claim maturity.
```

Unsafe statements to avoid:

```text
Research-to-Capability Department automatically builds product features.
Research-to-Capability Department guarantees best practice extraction.
Research-to-Capability Department validates compliance/security readiness.
Research-to-Capability Department can use private customer workflows now.
```

---

## 15. Current operating state

```text
Department status: internal-spec
Allowed mode: docs-only / report-only
Public-facing behavior: none
Backend/API: not allowed
Real customer data: not allowed
Production claim: not allowed
Main merge: user review required
```

---

## 16. Closeout

```text
DEPARTMENT-004 result: PASS
Research-to-Capability Department draft created: yes
Capability extraction loop defined: yes
Public-safe boundary preserved: yes
No public demo code changed: yes
No backend / AI API added: yes
No real customer data added: yes
No production / compliance / security claim added: yes
Recommended next: DEPARTMENT-003｜Tool Research Department Draft or public feedback checkpoint
```

# INTERNAL-SYS-002｜Capability Registry v0.1

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal registry draft / public-safe  
**Date:** 2026-07-08  
**Mode:** Docs-only / report-only  
**Related issue:** INTERNAL-SYS-002｜Capability Registry v0.1

> 中文定位：這份文件是 Future Ability Universe / Capability Operating System 的第一版能力庫。目的不是宣稱產品成熟，而是把目前已經出現的能力，用可管理、可驗證、可擴充的格式登記起來，避免每次都把工作當成一次性任務處理。

---

## 1. Registry purpose

The Capability Registry tracks reusable workflow abilities.

It answers:

```text
What capability exists?
What problem does it solve?
What input does it accept?
What output does it produce?
What boundary must it keep?
How can it be validated?
Which AI department owns it?
Is it public-facing, internal, or only a future candidate?
```

中文說明：能力庫不是功能清單，也不是產品 roadmap。它是用來管理「可重複使用的工作流能力」。

---

## 2. Capability schema

Each capability should use this structure:

```text
Capability ID:
Capability name:
Status:
Owner department:
Surface: public demo / internal spec / future candidate
Problem solved:
Input:
Process:
Output:
Allowed mode:
Risk level:
Validation:
Rollback / fallback:
Boundary:
Reusable scenarios:
Public-safe: yes / no / conditional
Next improvement:
```

---

## 3. Status model v0.1

```text
registered = defined enough to reference internally
active-public-demo = visible in the public prototype
internal-spec = internal operating rule only
candidate = useful idea, not implemented
backlog = parked for later
blocked = should not proceed under current boundary
paused = waiting for feedback or review
```

Important: none of these statuses mean production-ready.

中文提醒：這裡所有狀態都不代表正式 SaaS、不代表 production-ready、不代表合規或資安保證。

---

## 4. First registered capabilities

### CAP-PUB-001｜Workflow Risk Preview

```text
Capability ID: CAP-PUB-001
Capability name: Workflow Risk Preview
Status: active-public-demo
Owner department: Workflow Safety Department
Surface: public demo
Problem solved: A vague AI workflow idea needs an early risk snapshot before real data or production tools are used.
Input: synthetic or user-described workflow idea
Process: identify risk indicators and summarize a first risk level
Output: risk level / reason codes / risk snapshot
Allowed mode: browser-only public-safe preview
Risk level: low when synthetic-only; higher if user enters real private data
Validation: confirm no storage, no backend, no AI API, no production claim
Rollback / fallback: remove or rewrite risky wording
Boundary: not a security, legal, privacy, compliance, or production-readiness assessment
Reusable scenarios: customer support, internal knowledge, reporting, operations notes, quality review
Public-safe: yes, if synthetic or non-sensitive input only
Next improvement: use public feedback to improve clarity of risk language
```

---

### CAP-PUB-002｜Safe First Test Planner

```text
Capability ID: CAP-PUB-002
Capability name: Safe First Test Planner
Status: active-public-demo
Owner department: Workflow Safety Department
Surface: public demo
Problem solved: Teams often jump from AI idea to real integration too quickly.
Input: workflow idea and risk signals
Process: suggest a small first test that avoids production systems and sensitive data
Output: safe first test note
Allowed mode: browser-only static recommendation
Risk level: low
Validation: the first test must avoid real customer data, auto-send, production writes, or irreversible action
Rollback / fallback: downgrade to report-only / synthetic-only test
Boundary: does not create or run the test automatically
Reusable scenarios: draft-only replies, fake-ticket review, synthetic report summary, checklist review
Public-safe: yes
Next improvement: add more synthetic examples only if feedback supports it
```

---

### CAP-PUB-003｜Human Review Gate Planner

```text
Capability ID: CAP-PUB-003
Capability name: Human Review Gate Planner
Status: active-public-demo
Owner department: Workflow Safety Department
Surface: public demo
Problem solved: AI output may reach people or systems before a human review point is defined.
Input: workflow idea and output path
Process: identify where a human should approve, reject, or edit output
Output: human review gate suggestion
Allowed mode: advisory / preview only
Risk level: low
Validation: output must not imply autonomous approval or production execution
Rollback / fallback: mark workflow as not ready for automation
Boundary: does not replace professional review or operational governance
Reusable scenarios: customer-facing drafts, internal reports, operational summaries, quality checks
Public-safe: yes
Next improvement: improve wording based on external confusion patterns
```

---

### CAP-PUB-004｜Validation Checklist Builder

```text
Capability ID: CAP-PUB-004
Capability name: Validation Checklist Builder
Status: active-public-demo
Owner department: Workflow Safety Department
Surface: public demo
Problem solved: Early AI workflow ideas often lack a concrete validation checklist.
Input: workflow idea, risk snapshot, first test, review gate
Process: convert risk signals into basic validation questions
Output: starter validation checklist
Allowed mode: static checklist generation / browser-only preview
Risk level: low
Validation: checklist must remain starter-level and not claim formal compliance
Rollback / fallback: remove overclaiming checklist items
Boundary: not an audit, not certification, not legal/security/compliance validation
Reusable scenarios: workflow review, demo review, capability quality gate
Public-safe: yes
Next improvement: add traceable checklist categories if feedback asks for more structure
```

---

### CAP-PUB-005｜Trace Note Generator

```text
Capability ID: CAP-PUB-005
Capability name: Trace Note Generator
Status: active-public-demo
Owner department: Workflow Safety Department
Surface: public demo
Problem solved: Teams need a simple note explaining why a workflow is or is not ready for the next step.
Input: risk level, first test, review gate, validation checklist
Process: summarize the decision boundary in a traceable note
Output: trace note
Allowed mode: explanatory note only
Risk level: low
Validation: note must not imply production approval
Rollback / fallback: mark as prototype preview only
Boundary: not a formal audit trail or legal record
Reusable scenarios: demo output, internal review, feedback discussion
Public-safe: yes
Next improvement: make notes easier to copy only if feedback requests it
```

---

## 5. Internal feedback capabilities

### CAP-FBK-001｜Public Feedback Intake

```text
Capability ID: CAP-FBK-001
Capability name: Public Feedback Intake
Status: internal-spec
Owner department: Public Feedback Department
Surface: internal spec
Problem solved: Public comments need to be handled consistently instead of reactively.
Input: public comments, reactions, no-response signals, listing status
Process: summarize, classify, and remove unnecessary private details
Output: structured feedback entry
Allowed mode: report-only / manual review
Risk level: low to medium depending on content
Validation: no private data retained, no defensive reply, no product overclaim
Rollback / fallback: summarize less; do not reply if unclear
Boundary: no automatic posting, no scraping beyond normal visible checks, no sensitive data collection
Reusable scenarios: GitHub issue, DEV, Reddit, Hacker News, Indie Hackers, Launching Next
Public-safe: conditional; internal output should avoid identities and private details
Next improvement: test on first feedback checkpoint
```

---

### CAP-FBK-002｜Feedback Classifier

```text
Capability ID: CAP-FBK-002
Capability name: Feedback Classifier
Status: internal-spec
Owner department: Public Feedback Department
Surface: internal spec
Problem solved: Different feedback types require different responses and internal actions.
Input: structured feedback entry
Process: classify into clarity, misunderstanding, feature request, use case, security question, no-response, or spam/offtopic
Output: feedback type and priority
Allowed mode: report-only
Risk level: low
Validation: classification must be explainable and not overreact to one signal
Rollback / fallback: mark as unclear and wait
Boundary: classification is not user sentiment analysis for manipulation or sales targeting
Reusable scenarios: feedback synthesis, v0.2 backlog, capability extraction
Public-safe: no; internal operating capability
Next improvement: compare multiple platform signals after the first wait period
```

---

### CAP-FBK-003｜Reply Strategy Generator

```text
Capability ID: CAP-FBK-003
Capability name: Reply Strategy Generator
Status: internal-spec
Owner department: Public Feedback Department
Surface: internal spec
Problem solved: Public replies must stay non-defensive, non-salesy, and prototype-first.
Input: feedback type, user intent, product signal
Process: generate short safe reply drafts
Output: suggested reply text
Allowed mode: draft-only; user review required before posting
Risk level: medium because public posting affects positioning
Validation: no production claim, no compliance claim, no roadmap promise, no private-data request
Rollback / fallback: do not reply
Boundary: does not auto-post; does not impersonate; does not hard-sell
Reusable scenarios: why no backend, why not ChatGPT, feature request, security question
Public-safe: conditional; output requires review before posting
Next improvement: maintain a small reply template pack
```

---

### CAP-FBK-004｜Internal Action Router

```text
Capability ID: CAP-FBK-004
Capability name: Internal Action Router
Status: internal-spec
Owner department: Public Feedback Department
Surface: internal spec
Problem solved: Feedback should not automatically become product changes.
Input: classified feedback and priority
Process: route to no action, reply only, backlog, copy improvement, synthetic scenario candidate, or blocked
Output: internal action recommendation
Allowed mode: report-only / docs-only
Risk level: low
Validation: action must be based on actual signal, not anxiety
Rollback / fallback: leave in wait state
Boundary: no demo changes unless P0/P1 clarity or boundary issue exists
Reusable scenarios: v0.2 planning, roadmap, issue queue prioritization
Public-safe: no; internal operating capability
Next improvement: connect to Capability Registry updates
```

---

### CAP-FBK-005｜Capability Candidate Extractor

```text
Capability ID: CAP-FBK-005
Capability name: Capability Candidate Extractor
Status: internal-spec
Owner department: Research-to-Capability Department
Surface: internal spec
Problem solved: Useful public feedback may reveal repeatable workflow patterns.
Input: use case signal or repeated feature request
Process: check whether the pattern is reusable and public-safe
Output: capability candidate entry
Allowed mode: report-only / registry candidate
Risk level: low
Validation: candidate must not require real data, backend, or production integration at this stage
Rollback / fallback: classify as backlog idea only
Boundary: does not implement feature automatically
Reusable scenarios: customer support, internal knowledge, reporting, operations, tool research
Public-safe: no; internal operating capability
Next improvement: use first real public use case if one appears
```

---

## 6. Internal COS capabilities

### CAP-COS-001｜Capability Registry Maintainer

```text
Capability ID: CAP-COS-001
Capability name: Capability Registry Maintainer
Status: registered
Owner department: Research-to-Capability Department
Surface: internal spec
Problem solved: Capabilities need a single registry so the system does not become scattered.
Input: capability specs, feedback-derived candidates, internal tasks
Process: register, update, pause, or block capabilities
Output: maintained capability list
Allowed mode: docs-only / report-only
Risk level: low
Validation: each capability must have purpose, input, output, boundary, validation, and owner department
Rollback / fallback: mark incomplete entries as candidate instead of registered
Boundary: registry does not imply production maturity
Reusable scenarios: all Future Ability Universe capability work
Public-safe: no; internal operating capability
Next improvement: add lifecycle state model
```

---

### CAP-COS-002｜User Review Boundary Gate

```text
Capability ID: CAP-COS-002
Capability name: User Review Boundary Gate
Status: candidate
Owner department: Capability Operating System
Surface: internal spec
Problem solved: The system needs a clear rule for what can continue automatically and what requires user review.
Input: proposed action
Process: check action risk and public/private impact
Output: continue automatically / user review required / blocked
Allowed mode: internal decision support
Risk level: low
Validation: gate must block public posting, main merge, demo changes, backend/API, real data, payments, and product claims unless reviewed
Rollback / fallback: pause and ask user
Boundary: does not bypass user control for high-impact actions
Reusable scenarios: GitHub work, public replies, demo changes, tool adoption, client pilot planning
Public-safe: no; internal operating capability
Next improvement: implement GATE-001 doc
```

---

### CAP-COS-003｜Public-Safe Boundary Guard

```text
Capability ID: CAP-COS-003
Capability name: Public-Safe Boundary Guard
Status: registered
Owner department: Capability Operating System
Surface: internal spec / public repo wording
Problem solved: The prototype must avoid unsafe claims and data assumptions.
Input: proposed wording, task, feature, or public reply
Process: check against public-safe boundary rules
Output: pass / needs review / blocked
Allowed mode: docs-only / review gate
Risk level: low
Validation: no real data, no secrets, no production claim, no compliance/security/legal guarantee
Rollback / fallback: downgrade wording or block action
Boundary: not a compliance system; only an internal safety guard
Reusable scenarios: README, docs, public replies, demo kit, roadmap
Public-safe: conditional
Next improvement: add internal docs safety validation checklist
```

---

## 7. Future candidate capabilities

| ID | Candidate | Why it matters | Status | Current decision |
|---|---|---|---|---|
| CAP-CAND-001 | Copy / Export Review Note | Users may want to copy outputs | backlog | wait for feedback |
| CAP-CAND-002 | Synthetic Use Case Queue | More examples may improve understanding | backlog | wait for feedback |
| CAP-CAND-003 | AI Tool Candidate Evaluation | Tool Research Department needs first report-only task | candidate | research later |
| CAP-CAND-004 | AI Department Template | Needed for modular AI department system | candidate | after registry / mapping |
| CAP-CAND-005 | Public-Safe Demo Kit Outline | Useful for future competition / portfolio | candidate | after feedback summary |
| CAP-CAND-006 | Controlled Client Pilot Boundary | Future boundary only | paused | not now |

---

## 8. Department ownership map

| Department | Registered capabilities | Purpose |
|---|---|---|
| Workflow Safety Department | CAP-PUB-001 to CAP-PUB-005 | Turns vague AI workflow ideas into public-safe review previews |
| Public Feedback Department | CAP-FBK-001 to CAP-FBK-004 | Turns public feedback into safe replies and internal actions |
| Research-to-Capability Department | CAP-FBK-005, CAP-COS-001 | Converts repeated signals into reusable capabilities |
| Capability Operating System | CAP-COS-002, CAP-COS-003 | Maintains gates, boundaries, and safe operating rules |
| Tool Research Department | CAP-CAND-003 | Future report-only research on tools |
| Demo Kit Department | CAP-CAND-005 | Future public-safe explanation package |

---

## 9. Registry update rules

A capability can be added or promoted only when:

```text
- it solves a repeatable workflow problem
- it has clear input and output
- it has a public-safe boundary
- it has validation criteria
- it has an owner department
- it does not imply production readiness
- it does not require real customer data at this stage
- it does not require backend / AI API unless explicitly approved later
```

A capability must remain candidate / backlog / blocked when:

```text
- it depends on real customer data
- it requires production integration
- it requires legal/security/compliance claims
- it requires paid tools or platform upgrades
- it would change public positioning without feedback
- it cannot be validated safely
```

---

## 10. Current registry state

```text
PUBLIC-FEEDBACK-WAIT-001: active
INTERNAL-SYS-001 Public Feedback Intake: prepared in draft PR
INTERNAL-SYS-002 Capability Registry v0.1: this file
WorkflowGuard public demo: unchanged
New platform push: paused
Backend / AI API: blocked
Real customer data: blocked
Production readiness claim: blocked
Main merge: user review required
Public replies: user review required before posting
```

---

## 11. Closeout

```text
INTERNAL-SYS-002 result: PASS
Registry version: v0.1
Registered public-facing capabilities: 5
Registered internal feedback capabilities: 5
Registered COS capabilities: 3
Future candidate capabilities: 6
Recommended next implementation: GATE-001｜User Review Required Boundary
```

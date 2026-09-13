# INTERNAL-SYS-004｜AI Department Template v0.1

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal template / public-safe  
**Date:** 2026-07-08  
**Mode:** Docs-only / department governance  

> 中文定位：這份文件定義 Future Ability Universe 的「AI 部門模板」。目的不是立刻建立完整 AI 公司系統，而是讓每一個 AI Department 都能用同一種格式描述：解決什麼問題、吃什麼輸入、產出什麼、有哪些 Capability、邊界在哪裡、什麼要人審、怎麼驗證。

---

## 1. Why AI Department templates matter

A department is not a single feature.

A department is a repeatable operating unit that groups related capabilities.

```text
Capability = reusable ability
Department = managed group of related capabilities
Capability Operating System = registry + gates + departments + validation + feedback loop
```

中文說明：未來不是每次重新做一個工具，而是把能力歸類到部門。每個部門都有固定規格，方便擴充、驗證、展示與管理。

---

## 2. Department schema

Each AI Department should use this format:

```text
Department ID:
Department name:
Status:
Lifecycle state:
Purpose:
Problem solved:
Target user:
Input:
Process:
Output:
Included capabilities:
Allowed operating mode:
Human review gate:
Validation method:
Boundary / blocked actions:
Public demo surface:
Internal execution surface:
Data policy:
Risk level:
Maturity note:
Owner / maintainer:
Next improvement:
```

---

## 3. Status model

| Status | Meaning | Public claim allowed? |
|---|---|---:|
| `draft` | Template exists, not operational | no |
| `internal-spec` | Internal department structure exists | no |
| `public-safe-demo-linked` | Has a public-safe demo surface | prototype-only |
| `report-only` | Produces reports only | limited |
| `paused` | Waiting for feedback or dependencies | no |
| `blocked` | Out of current boundary | no |

Important:

```text
No department is production-ready in the current phase.
No department is client-data-ready in the current phase.
No department provides legal / privacy / cybersecurity / compliance guarantees.
```

---

## 4. Standard department template

```text
Department ID:
Department name:
Status:
Lifecycle state:

Purpose:

Problem solved:

Target user:

Input:

Process:
1.
2.
3.

Output:

Included capabilities:
- CAP-...

Allowed operating mode:

Human review gate:

Validation method:

Boundary / blocked actions:
- no real customer data unless separately approved
- no production integration
- no backend / AI API unless separately approved
- no legal / privacy / cybersecurity / compliance guarantee

Public demo surface:

Internal execution surface:

Data policy:

Risk level:

Maturity note:

Owner / maintainer:

Next improvement:
```

---

## 5. Candidate departments v0.1

### DEPT-001｜Workflow Safety Department

```text
Department ID: DEPT-001
Department name: Workflow Safety Department
Status: public-safe-demo-linked
Lifecycle state: internal-spec / public-safe-demo-linked

Purpose:
Help review AI workflow ideas before real data or production systems are involved.

Problem solved:
Teams may want to connect AI to workflows too quickly without defining risk, safe first test, human review, validation, or trace notes.

Target user:
Builders, founders, teams, reviewers, or internal operators evaluating early AI workflow ideas.

Input:
Synthetic or non-sensitive AI workflow description.

Process:
1. Intake workflow idea.
2. Preview risk level.
3. Suggest safe first test.
4. Identify human review gate.
5. Build starter validation checklist.
6. Generate trace note.

Output:
Risk level, safe first test, human review gate, validation checklist, trace note.

Included capabilities:
- CAP-PUB-001 Workflow Risk Preview
- CAP-PUB-002 Safe First Test Planner
- CAP-PUB-003 Human Review Gate Planner
- CAP-PUB-004 Validation Checklist Builder
- CAP-PUB-005 Trace Note Generator

Allowed operating mode:
Browser-only / public-safe / prototype preview.

Human review gate:
Required before any public copy change, production claim, or real-data workflow.

Validation method:
Internal docs safety checklist and public-safe boundary review.

Boundary / blocked actions:
- no real customer data
- no backend / AI API
- no production automation
- no compliance/security/legal guarantee

Public demo surface:
WorkflowGuard AI public demo.

Internal execution surface:
Capability Registry + COS mapping + feedback intake loop.

Data policy:
Synthetic or non-sensitive input only.

Risk level:
Low when synthetic-only; higher if users paste sensitive data.

Maturity note:
Public-safe prototype only.

Owner / maintainer:
Future Ability Universe / Capability Operating System.

Next improvement:
Use public feedback to decide whether examples, copy/export, or scenario templates are justified.
```

---

### DEPT-002｜Public Feedback Department

```text
Department ID: DEPT-002
Department name: Public Feedback Department
Status: internal-spec
Lifecycle state: internal-spec

Purpose:
Convert public comments, reactions, and no-response signals into safe replies, internal actions, backlog candidates, or capability candidates.

Problem solved:
Public feedback can cause random reactions unless it is classified and routed.

Target user:
Internal operator / AI General Manager.

Input:
Public comments, visible reactions, no-response signals, platform listing status.

Process:
1. Intake feedback.
2. Remove unnecessary private details.
3. Classify feedback type.
4. Draft reply if needed.
5. Route internal action.
6. Extract capability candidate if repeatable.

Output:
Feedback entry, feedback type, suggested reply, internal action, capability candidate.

Included capabilities:
- CAP-FBK-001 Public Feedback Intake
- CAP-FBK-002 Feedback Classifier
- CAP-FBK-003 Reply Strategy Generator
- CAP-FBK-004 Internal Action Router
- CAP-FBK-005 Capability Candidate Extractor

Allowed operating mode:
Report-only / draft-only.

Human review gate:
Required before posting any public reply.

Validation method:
Reply template pack + docs safety validation checklist.

Boundary / blocked actions:
- no auto-posting
- no spam-like engagement
- no asking for private data
- no hard-selling
- no roadmap promise

Public demo surface:
None.

Internal execution surface:
Internal feedback intake docs and reply template pack.

Data policy:
Public signals only; avoid retaining private details.

Risk level:
Medium if public replies are involved; low if report-only.

Maturity note:
Internal spec only.

Owner / maintainer:
Future Ability Universe / Public Feedback Department.

Next improvement:
Use first feedback checkpoint to validate taxonomy.
```

---

### DEPT-003｜Research-to-Capability Department

```text
Department ID: DEPT-003
Department name: Research-to-Capability Department
Status: internal-spec
Lifecycle state: candidate / internal-spec

Purpose:
Turn repeated findings, feedback, or tasks into reusable capabilities.

Problem solved:
Research and feedback often remain one-off notes instead of becoming reusable operating abilities.

Target user:
Internal system designer / AI General Manager.

Input:
Research findings, feedback signals, repeated workflow patterns, internal task results.

Process:
1. Identify repeatable pattern.
2. Check public-safe boundary.
3. Draft capability candidate.
4. Assign owner department.
5. Define validation and boundary.
6. Register or backlog capability.

Output:
Capability candidate or registry update.

Included capabilities:
- CAP-FBK-005 Capability Candidate Extractor
- CAP-COS-001 Capability Registry Maintainer

Allowed operating mode:
Docs-only / report-only.

Human review gate:
Required if capability changes public positioning or requires real data / backend / AI API.

Validation method:
Capability Registry schema + lifecycle state model.

Boundary / blocked actions:
- no automatic feature implementation
- no production maturity claim
- no client-data assumption

Public demo surface:
None directly.

Internal execution surface:
Capability Registry.

Data policy:
Use public-safe summaries only.

Risk level:
Low.

Maturity note:
Internal operating capability.

Owner / maintainer:
Future Ability Universe / Capability Operating System.

Next improvement:
Create a dedicated department draft after registry stabilizes.
```

---

### DEPT-004｜Tool Research Department

```text
Department ID: DEPT-004
Department name: Tool Research Department
Status: candidate
Lifecycle state: candidate / paused

Purpose:
Evaluate AI tools before adoption using public-safe, local-first, traceability, validation, cost, and lock-in criteria.

Problem solved:
Tools can be adopted too early without checking data risk, cost risk, vendor lock-in, or capability fit.

Target user:
Internal operator evaluating tools for Future Ability Universe.

Input:
Research question and tool category.

Process:
1. Define tool category.
2. Gather candidate tools.
3. Score public-safe fit.
4. Score data boundary risk.
5. Score cost / lock-in risk.
6. Produce report-only recommendation.

Output:
Tool candidate list and evaluation matrix.

Included capabilities:
- CAP-CAND-003 AI Tool Candidate Evaluation

Allowed operating mode:
Report-only.

Human review gate:
Required before signup, purchase, API key usage, or integration.

Validation method:
Tool research report criteria.

Boundary / blocked actions:
- no signup
- no paid tools
- no API key usage
- no integration
- no real customer data

Public demo surface:
None.

Internal execution surface:
Future reports/tool_research outputs.

Data policy:
Public information only.

Risk level:
Low if report-only; higher if tool adoption begins.

Maturity note:
Candidate only.

Owner / maintainer:
Future Ability Universe / Tool Research Department.

Next improvement:
Run TOOL-RESEARCH-001 only after current public feedback batch stabilizes.
```

---

### DEPT-005｜Demo Kit Department

```text
Department ID: DEPT-005
Department name: Demo Kit Department
Status: candidate
Lifecycle state: paused

Purpose:
Package public-safe capabilities into reviewer-friendly demo explanations without exposing internal systems or overclaiming maturity.

Problem solved:
A prototype may be technically understandable internally but unclear to reviewers, competition judges, or collaborators.

Target user:
Reviewer, competition judge, collaborator, public-safe feedback giver.

Input:
Capability Registry, COS mapping, feedback summary, public demo.

Process:
1. Define one-sentence positioning.
2. Explain problem.
3. Show demo path.
4. Clarify what it does not claim.
5. Connect to Capability Operating System.
6. Prepare reviewer questions.

Output:
Public-safe demo kit outline.

Included capabilities:
- CAP-CAND-005 Public-Safe Demo Kit Outline

Allowed operating mode:
Docs-only / outline-only.

Human review gate:
Required before public pitch, competition submission, or deck creation.

Validation method:
Prototype overclaim risk register.

Boundary / blocked actions:
- no investor claims
- no sales promises
- no production claims
- no compliance/security guarantee

Public demo surface:
Future demo explanation, not current demo behavior.

Internal execution surface:
Demo kit docs.

Data policy:
Synthetic / public-safe examples only.

Risk level:
Medium because public positioning can change.

Maturity note:
Paused until public feedback summary.

Owner / maintainer:
Future Ability Universe / Demo Kit Department.

Next improvement:
Wait for first public launch learning summary.
```

---

## 6. Department promotion rules

A department may move from `candidate` to `internal-spec` only when:

```text
- its purpose is clear
- it has at least one capability
- allowed operating mode is defined
- blocked actions are defined
- validation method is defined
- owner / maintainer is defined
```

A department may become `public-safe-demo-linked` only when:

```text
- public surface uses synthetic or non-sensitive examples
- public wording avoids production / compliance / security claims
- user review approves public-facing positioning changes
- no backend / AI API / real data is required
```

---

## 7. Current department map

| Department | Status | Current action |
|---|---|---|
| Workflow Safety Department | public-safe-demo-linked | active through WorkflowGuard AI public demo |
| Public Feedback Department | internal-spec | active during feedback wait |
| Research-to-Capability Department | internal-spec | active through Capability Registry |
| Tool Research Department | candidate / paused | wait |
| Demo Kit Department | candidate / paused | wait for feedback summary |
| Client Pilot Department | blocked / future-only | not now |

---

## 8. Closeout

```text
INTERNAL-SYS-004 result: PASS
AI Department Template created: yes
Core departments defined: yes
Production maturity claim avoided: yes
Public-safe boundary preserved: yes
No public demo code changed: yes
No backend / AI API added: yes
Recommended next: public feedback checkpoint or department-specific drafts only if needed
```

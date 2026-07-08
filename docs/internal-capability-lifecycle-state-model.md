# INTERNAL-SYS-007｜Capability Lifecycle State Model

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal lifecycle model / public-safe  
**Date:** 2026-07-08  
**Mode:** Docs-only / capability governance  

> 中文定位：這份文件定義 Capability 從「想法」到「候選」、「內部規格」、「公開安全 demo」、「合成資料驗證」、「暫停」、「封鎖」、「退役」的生命週期。目的不是宣稱成熟度，而是避免能力狀態混亂，讓 Future Ability Universe 可以安全管理可重複能力。

---

## 1. Why lifecycle states matter

A capability should not jump directly from an idea to a public product claim.

Lifecycle states help the system decide:

```text
- what exists only as an idea
- what is safe to register
- what can be shown publicly
- what is internal-only
- what requires user review
- what must remain blocked
- what can be retired later
```

中文說明：Capability 狀態不是成熟度吹噓，而是風險管理。每一個能力都要知道自己現在在哪一階段、允許做什麼、不允許做什麼。

---

## 2. Lifecycle states v0.1

| State | 中文 | Meaning | Allowed mode | Public claim allowed? |
|---|---|---|---|---:|
| `idea` | 想法 | Raw concept, not yet structured | notes only | no |
| `candidate` | 候選 | Has repeatable pattern, but not defined enough | report-only | no |
| `drafted` | 初稿 | Has a written spec or template | docs-only | no |
| `internal-spec` | 內部規格 | Safe internal operating rule exists | internal use only | no |
| `registered` | 已登記 | In Capability Registry with owner, input/output, boundary, validation | docs/report-only | no |
| `public-safe-demo` | 公開安全展示 | Can be shown publicly with synthetic/non-sensitive input | browser-only/demo | yes, but prototype-only |
| `validated-synthetic-only` | 合成資料驗證 | Tested only with fake/synthetic scenarios | report-only/demo | limited |
| `paused` | 暫停 | Waiting for feedback, review, or better evidence | no action except review | no |
| `blocked` | 封鎖 | Unsafe or out of current boundary | no action | no |
| `retired` | 退役 | No longer useful or superseded | archived reference | no |

Important:

```text
No state in v0.1 means production-ready.
No state in v0.1 means compliance-ready.
No state in v0.1 means client-data-ready.
```

---

## 3. Promotion rules

### idea → candidate

Allowed when:

```text
- the idea solves a repeated workflow problem
- it can be described without real customer data
- it may become reusable
```

Blocked when:

```text
- it is a one-off reaction
- it depends on private data
- it requires production integration immediately
```

---

### candidate → drafted

Allowed when:

```text
- input and output can be described
- boundary can be described
- owner department can be guessed
- first validation idea exists
```

---

### drafted → internal-spec

Allowed when:

```text
- allowed mode is stated
- blocked actions are stated
- public-safe boundary is clear
- user-review-required points are clear
```

---

### internal-spec → registered

Allowed when:

```text
- capability ID exists
- owner department exists
- problem / input / process / output are defined
- validation exists
- rollback or fallback exists
- boundary exists
```

---

### registered → public-safe-demo

Allowed only when:

```text
- no real customer data is needed
- no backend / AI API is needed
- no storage / login is needed
- output can be explained as prototype preview
- public wording avoids production / compliance / security claims
- user review approves public exposure if public copy changes
```

---

### registered → validated-synthetic-only

Allowed when:

```text
- synthetic scenarios have been tested
- expected output is understandable
- validation checklist passes
- no real data or production workflow was used
```

---

## 4. Demotion rules

A capability should be demoted to `paused` when:

```text
- public feedback is inconclusive
- the problem framing is unclear
- it may be useful but timing is wrong
- it requires another capability first
```

A capability should be demoted to `blocked` when:

```text
- it requires real customer data now
- it requires backend / AI API now
- it implies legal / privacy / cybersecurity / compliance guarantee
- it implies production readiness
- it requires payment / upgrade / external subscription
- it cannot be validated safely
```

A capability should become `retired` when:

```text
- it is replaced by a clearer capability
- it duplicates another capability
- it no longer supports the project direction
- keeping it creates confusion
```

---

## 5. Current capability state map

| Capability | Current state | Reason |
|---|---|---|
| CAP-PUB-001 Workflow Risk Preview | public-safe-demo | Visible in public prototype, browser-only |
| CAP-PUB-002 Safe First Test Planner | public-safe-demo | Visible in public prototype, advisory only |
| CAP-PUB-003 Human Review Gate Planner | public-safe-demo | Visible in public prototype, preview only |
| CAP-PUB-004 Validation Checklist Builder | public-safe-demo | Visible in public prototype, starter checklist only |
| CAP-PUB-005 Trace Note Generator | public-safe-demo | Visible in public prototype, explanatory only |
| CAP-FBK-001 Public Feedback Intake | internal-spec | Defined as internal operating rule |
| CAP-FBK-002 Feedback Classifier | internal-spec | Defined as internal operating rule |
| CAP-FBK-003 Reply Strategy Generator | internal-spec | Draft-only, user review required |
| CAP-FBK-004 Internal Action Router | internal-spec | Routes feedback to backlog / no action / capability candidate |
| CAP-FBK-005 Capability Candidate Extractor | internal-spec | Internal extraction rule only |
| CAP-COS-001 Capability Registry Maintainer | registered | Registry file exists |
| CAP-COS-002 User Review Boundary Gate | internal-spec | Boundary doc exists |
| CAP-COS-003 Public-Safe Boundary Guard | internal-spec | Safety validation and risk register exist |
| CAP-CAND-001 Copy / Export Review Note | paused | Wait for feedback signal |
| CAP-CAND-002 Synthetic Use Case Queue | paused | Wait for feedback signal |
| CAP-CAND-003 AI Tool Candidate Evaluation | candidate | Future Tool Research task only |
| CAP-CAND-004 AI Department Template | candidate | Next internal structure task, not urgent |
| CAP-CAND-005 Public-Safe Demo Kit Outline | paused | Wait for feedback summary |
| CAP-CAND-006 Controlled Client Pilot Boundary | blocked | Too early; no client-data work now |

---

## 6. User review gates by lifecycle state

| State | User review required? | Why |
|---|---:|---|
| idea | no | Internal notes only |
| candidate | no | Internal report-only |
| drafted | no | Docs-only if internal |
| internal-spec | no | Internal docs-only |
| registered | no | Registry-only if no public claim changes |
| public-safe-demo | yes if public copy or behavior changes | Public surface |
| validated-synthetic-only | maybe | If used publicly, review needed |
| paused | no | No action |
| blocked | yes to unblock | Requires explicit decision |
| retired | yes if deleting public or main content | Cleanup risk |

---

## 7. Status labels for registry

Use these labels in future registry updates:

```text
state: idea
state: candidate
state: drafted
state: internal-spec
state: registered
state: public-safe-demo
state: validated-synthetic-only
state: paused
state: blocked
state: retired
```

Optional maturity note:

```text
maturity_note: prototype-only / synthetic-only / internal-only / feedback-wait / blocked-current-phase
```

---

## 8. Current blocked promotions

Do not promote any capability to production, client-ready, or compliance-ready.

Blocked states for current phase:

```text
production-ready
client-ready
enterprise-ready
compliance-ready
security-certified
data-connected
backend-enabled
auto-executing
```

---

## 9. Closeout

```text
INTERNAL-SYS-007 result: PASS
Lifecycle state model created: yes
Production maturity claim avoided: yes
Public-safe boundary preserved: yes
No public demo code changed: yes
No backend / AI API added: yes
Recommended next: INTERNAL-SYS-004｜AI Department Template v0.1 or public feedback checkpoint
```

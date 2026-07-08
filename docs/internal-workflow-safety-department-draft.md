# DEPARTMENT-001｜Workflow Safety Department Draft

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal department draft / public-safe  
**Date:** 2026-07-08  
**Mode:** Docs-only / department draft  

> 中文定位：這份文件把 WorkflowGuard AI 背後的第一個 AI Department 正式整理出來：Workflow Safety Department。它不是完整 SaaS、不是正式治理產品、不是合規或資安工具，而是 Future Ability Universe / Capability Operating System 裡第一個可公開安全展示的部門雛形。

---

## 1. Department identity

```text
Department ID: DEPT-001
Department name: Workflow Safety Department
Status: public-safe-demo-linked
Lifecycle state: internal-spec / public-safe-demo
Public surface: WorkflowGuard AI public demo
Internal surface: Capability Registry + COS Mapping + Safety Gates
Maturity note: public-safe prototype only
```

中文說明：這個部門目前只在 public-safe prototype 層級成立，不能被描述成 production-ready、enterprise-ready、client-ready 或 compliance-ready。

---

## 2. Purpose

Help review AI workflow ideas before sensitive data, real customers, internal tools, or production systems are involved.

中文目的：

```text
在公司或團隊把 AI 接進真實流程前，先檢查：
風險在哪裡、第一步怎麼安全測、哪裡要人審、怎麼驗證、怎麼留下 trace note。
```

---

## 3. Problem solved

Many AI workflow ideas jump too quickly from:

```text
idea → integration → real data → production automation
```

The safer path is:

```text
idea
→ public-safe / synthetic review
→ risk preview
→ safe first test
→ human review gate
→ validation checklist
→ trace note
→ only then consider whether a deeper pilot is justified
```

This department exists to protect that safer path.

---

## 4. Target users

Current stage:

```text
- builders exploring AI workflows
- founders testing internal AI ideas
- reviewers giving public-safe feedback
- internal Future Ability Universe operator
- competition / demo reviewers in the future
```

Not current stage:

```text
- enterprise production deployment users
- regulated compliance teams relying on formal assurance
- customers submitting real private data
- teams expecting direct backend integration
```

---

## 5. Inputs

Allowed inputs:

```text
- synthetic workflow descriptions
- non-sensitive workflow ideas
- public-safe examples
- general use case categories
- fake tickets / fake reports / fake process notes
```

Blocked inputs:

```text
- real customer data
- private company workflows
- credentials
- API keys
- internal documents
- screenshots containing private information
- production system exports
```

---

## 6. Process

The department process is:

```text
1. Intake workflow idea.
2. Identify public-safe boundary.
3. Preview risk level.
4. Suggest safe first test.
5. Identify human review gate.
6. Build starter validation checklist.
7. Generate trace note.
8. Route repeated pattern into Capability Registry or backlog.
```

---

## 7. Outputs

Standard output package:

```text
Risk level:
Risk reasons:
Safe first test:
Human review gate:
Validation checklist:
Trace note:
Boundary note:
Capability candidate: yes / no
Recommended next action: wait / revise / backlog / synthetic test / blocked
```

Current public demo output:

```text
- risk level
- safe first test
- human review gate
- validation checklist
- trace note
```

---

## 8. Included capabilities

| Capability ID | Capability | State | Role |
|---|---|---|---|
| CAP-PUB-001 | Workflow Risk Preview | public-safe-demo | Risk snapshot |
| CAP-PUB-002 | Safe First Test Planner | public-safe-demo | Low-risk first test |
| CAP-PUB-003 | Human Review Gate Planner | public-safe-demo | Human approval point |
| CAP-PUB-004 | Validation Checklist Builder | public-safe-demo | Starter validation checklist |
| CAP-PUB-005 | Trace Note Generator | public-safe-demo | Decision trace note |
| CAP-COS-003 | Public-Safe Boundary Guard | internal-spec | Prevents overclaim and data-risk drift |

---

## 9. Allowed operating modes

Current allowed modes:

```text
browser-only public-safe preview
synthetic-only scenario review
non-sensitive workflow framing
report-only internal analysis
docs-only capability registration
```

Not allowed in current phase:

```text
production automation
backend integration
AI API execution
real customer data processing
compliance/security/legal audit
client-data pilot
paid deployment
```

---

## 10. Human review gates

User review is required before:

```text
- changing public demo behavior
- changing public positioning copy
- replying publicly under the user's account
- submitting to a new external platform
- claiming production readiness
- claiming security / compliance / legal / privacy assurance
- using real customer data
- adding backend / AI API / storage / login
- merging draft PR into main
```

---

## 11. Validation method

Use these validation documents:

```text
- internal-docs-safety-validation-checklist.md
- internal-prototype-overclaim-risk-register.md
- internal-user-review-required-boundary.md
- internal-capability-lifecycle-state-model.md
```

Validation questions:

```text
- Does the output avoid real data?
- Does it avoid production claims?
- Does it avoid compliance/security/legal guarantees?
- Is the first test actually safe and small?
- Is there a human review gate?
- Is the validation checklist starter-level, not certification-level?
- Is the trace note clear but not formal audit evidence?
```

---

## 12. Public demo relationship

WorkflowGuard AI is the public-safe demo surface of this department.

It shows:

```text
- how a vague AI workflow idea can be reviewed safely
- how to avoid jumping directly into production
- how risk, first test, human review, validation, and trace note fit together
```

It does not show:

```text
- the full internal Capability Operating System
- backend integrations
- AI API calls
- real data processing
- production deployment
- formal governance / compliance workflows
```

---

## 13. Boundary statement

Safe statement:

```text
Workflow Safety Department is an internal department concept behind WorkflowGuard AI. At this stage, it exists as a public-safe prototype and docs-only operating model for reviewing AI workflow ideas before real data or production systems are involved.
```

Unsafe statements to avoid:

```text
Workflow Safety Department is an enterprise AI governance system.
Workflow Safety Department guarantees safe AI deployment.
Workflow Safety Department is production-ready.
Workflow Safety Department provides compliance or cybersecurity review.
Workflow Safety Department can process client data now.
```

---

## 14. Future expansion candidates

Only after public feedback and user review:

```text
- synthetic scenario library
- copy/export output
- before/after workflow explanation
- team review mode concept
- local-only private version concept
- controlled client pilot boundary
```

Current decision:

```text
Do not build these now.
Wait for public feedback signals.
```

---

## 15. Closeout

```text
DEPARTMENT-001 result: PASS
Workflow Safety Department draft created: yes
Public-safe boundary preserved: yes
No public demo code changed: yes
No backend / AI API added: yes
No real customer data added: yes
No production / compliance / security claim added: yes
Recommended next: DEPARTMENT-002｜Public Feedback Department Draft or public feedback checkpoint
```

# INTERNAL-SYS-003｜WorkflowGuard AI ↔ Internal COS Mapping

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal mapping draft / public-safe  
**Date:** 2026-07-08  
**Mode:** Docs-only / architecture mapping  

> 中文定位：這份文件把 WorkflowGuard AI 的公開 demo 語言，對應到 Future Ability Universe / Capability Operating System 的內部概念。目的不是把 demo 說成正式產品，而是說明它如何作為 Capability Operating System 的 public-safe 展示層。

---

## 1. Why this mapping exists

WorkflowGuard AI is the public-safe prototype surface.

Future Ability Universe / Capability Operating System is the internal operating logic.

The mapping is:

```text
Internal COS concept
→ simplified public-safe demo term
→ reviewer-facing output
→ public feedback signal
→ capability improvement
```

中文說明：外面的人看到的是簡化後的 demo；內部管理的是任務分類、風險邊界、人審、驗證、留痕、能力化。

---

## 2. Public demo to internal COS map

| WorkflowGuard AI public term | Internal COS concept | Meaning | Boundary |
|---|---|---|---|
| Task intake | Task intake / task framing | Turn a vague AI idea into a structured review input | Does not collect private data |
| Risk level | Selector / risk classification | Estimate whether the workflow should stay small, reviewed, or blocked | Not a formal risk audit |
| Reason codes | Decision trace / explainable classification | Explain why a risk level was assigned | Not a compliance record |
| Safe first test | Report-only / controlled dry-run first step | Start with the smallest safe test before real data or production use | Does not execute the test |
| Human review gate | Human approval gate | Identify where a person must approve, reject, or edit | Does not replace governance |
| Validation checklist | Validation gate | Create starter checks before expanding the workflow | Not certification |
| Trace note | Audit-style decision note | Summarize the boundary and next safe step | Not legal evidence |
| Capability routing | Capability abstraction | Identify reusable workflow patterns | Not automatic implementation |
| Browser-only | Public-safe sandbox surface | Avoid backend, storage, and API exposure | Not production architecture |
| No backend / no AI API | Data and secret boundary | Keep early review safe and simple | Not a permanent product promise |
| Prototype seeking feedback | Public validation stage | Learn whether people understand the workflow framing | Not launch / SaaS claim |

---

## 3. Internal COS operating loop

```text
1. Receive workflow idea
2. Classify risk boundary
3. Recommend safe first test
4. Add human review gate
5. Build validation checklist
6. Produce trace note
7. Detect reusable capability pattern
8. Route to registry / backlog / blocked
9. Wait for public feedback before changing public demo
```

中文版本：

```text
接收工作流想法
→ 判斷風險邊界
→ 找出安全第一步測試
→ 放入人工審核關卡
→ 產生驗證清單
→ 留下 trace note
→ 判斷是否可重複能力化
→ 進入能力庫 / backlog / blocked
→ 等公開回饋再決定是否改 demo
```

---

## 4. How WorkflowGuard AI represents COS safely

### Public-safe simplification

WorkflowGuard AI intentionally shows a simplified version of the internal system.

It does not expose:

```text
- private runner logic
- production automation
- API keys
- internal customer workflows
- backend architecture
- sensitive validation ledgers
- real client data
```

It does show:

```text
- a safe workflow review path
- risk boundary thinking
- human-review-first structure
- validation-before-automation thinking
- traceable notes
- reusable capability language
```

---

## 5. Capability mapping

| Public output | Capability Registry entry | Owner department |
|---|---|---|
| Risk level | CAP-PUB-001 Workflow Risk Preview | Workflow Safety Department |
| Safe first test | CAP-PUB-002 Safe First Test Planner | Workflow Safety Department |
| Human review gate | CAP-PUB-003 Human Review Gate Planner | Workflow Safety Department |
| Validation checklist | CAP-PUB-004 Validation Checklist Builder | Workflow Safety Department |
| Trace note | CAP-PUB-005 Trace Note Generator | Workflow Safety Department |
| Public feedback entry | CAP-FBK-001 Public Feedback Intake | Public Feedback Department |
| Feedback type | CAP-FBK-002 Feedback Classifier | Public Feedback Department |
| Suggested reply | CAP-FBK-003 Reply Strategy Generator | Public Feedback Department |
| Internal action | CAP-FBK-004 Internal Action Router | Public Feedback Department |
| Capability candidate | CAP-FBK-005 Capability Candidate Extractor | Research-to-Capability Department |

---

## 6. What this mapping does not claim

This mapping does not claim:

```text
- WorkflowGuard AI is a finished SaaS
- the prototype is production-ready
- the prototype is a compliance solution
- the prototype is a cybersecurity tool
- the prototype can safely handle real customer data
- the prototype replaces professional review
- the public demo exposes the full internal COS
```

中文提醒：這張對應表是架構說明，不是成熟度聲明。

---

## 7. Use in future explanation

Safe explanation:

```text
WorkflowGuard AI is a public-safe demo layer for a broader Capability Operating System idea. It shows how an AI workflow can be reviewed through risk level, safe first test, human review gate, validation checklist, and trace note before using real data or production tools.
```

Unsafe explanation to avoid:

```text
WorkflowGuard AI is an enterprise-ready AI governance platform.
WorkflowGuard AI guarantees safe AI deployment.
WorkflowGuard AI provides compliance / cybersecurity review.
WorkflowGuard AI can connect directly to customer production workflows.
```

---

## 8. Feedback loop

Public feedback should be routed as follows:

```text
public comment
→ CAP-FBK-001 Public Feedback Intake
→ CAP-FBK-002 Feedback Classifier
→ CAP-FBK-003 Reply Strategy Generator if reply needed
→ CAP-FBK-004 Internal Action Router
→ CAP-FBK-005 Capability Candidate Extractor if repeatable pattern exists
→ CAP-COS-001 Capability Registry Maintainer
```

This prevents one-off comments from directly forcing product changes.

---

## 9. Current mapping state

```text
WorkflowGuard AI public demo: unchanged
Internal COS mapping: documented
Capability Registry v0.1: available on branch
User Review Boundary Gate: available on branch
Public Feedback Wait: active
Next internal task: Internal System Strengthening Index
```

---

## 10. Closeout

```text
INTERNAL-SYS-003 result: PASS
Mapping completed: yes
Public-safe boundary preserved: yes
No demo code changed: yes
No backend / AI API added: yes
No production or compliance claim added: yes
Recommended next implementation: INTERNAL-SYS-005｜Internal System Strengthening Index
```

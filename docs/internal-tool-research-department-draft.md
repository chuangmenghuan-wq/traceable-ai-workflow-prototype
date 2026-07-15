# DEPARTMENT-003｜Tool Research Department Draft

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal department draft / public-safe  
**Date:** 2026-07-08  
**Mode:** Docs-only / report-only department draft  

> 中文定位：這份文件把 AI 工具研究正式整理成第三個 AI Department：Tool Research Department。它的任務是用公開資訊、可驗證標準與安全邊界，評估 AI 工具是否值得後續研究或納入 Capability Operating System。它不負責註冊帳號、不負責購買、不負責接 API、不負責整合工具。

---

## 1. Department identity

```text
Department ID: DEPT-003
Department name: Tool Research Department
Status: internal-spec / candidate-operating
Lifecycle state: internal-spec
Public surface: none
Internal surface: report-only tool research outputs + capability candidate routing
Maturity note: report-only department; no tool adoption authority
```

中文說明：Tool Research Department 只做研究與評估，不做採購、不做整合、不拿 API key、不處理真實資料。

---

## 2. Purpose

Evaluate AI tools before adoption using safe, repeatable, report-only criteria.

中文目的：

```text
先研究工具是否值得看，不是立刻使用工具。
```

---

## 3. Problem solved

AI tools are easy to adopt too early:

```text
interesting tool → sign up → paste data → pay → integrate → lock-in / data risk
```

The safer path is:

```text
tool category need
→ public information research
→ candidate list
→ scoring matrix
→ data boundary check
→ cost / lock-in check
→ capability fit check
→ report-only recommendation
→ user review before any adoption
```

---

## 4. Input sources

Allowed input sources:

```text
- public websites
- public documentation
- pricing pages
- public changelogs
- public GitHub repositories
- public comparison articles
- public product pages
- user-provided non-sensitive tool questions
- internal capability gaps
```

Blocked input sources:

```text
- private dashboards
- paid account-only data
- customer data
- private company documents
- credentials / API keys / secrets
- production logs
- unapproved internal exports
```

---

## 5. Process

The department process is:

```text
1. Define tool category or tool question.
2. Define why the tool is being researched.
3. Gather public candidate tools.
4. Filter out tools that require unsafe access for evaluation.
5. Score public-safe fit.
6. Score data boundary risk.
7. Score cost / pricing risk.
8. Score vendor lock-in risk.
9. Score local-first or exportability if relevant.
10. Score traceability / auditability.
11. Map tool to possible capability gap.
12. Produce report-only recommendation.
13. Route to Research-to-Capability Department if reusable.
```

---

## 6. Standard output package

```text
Tool research question:
Tool category:
Why now:
Candidate tools:
Public-safe fit:
Data boundary risk:
Cost risk:
Vendor lock-in risk:
Traceability:
Local-first / exportability:
Capability fit:
Adoption recommendation: no / wait / research deeper / user-review-required
Blocked actions:
Next safe step:
Capability candidate:
```

---

## 7. Evaluation criteria

| Criterion | Question |
|---|---|
| Public-safe fit | Can it be evaluated without private data? |
| Data boundary | Does it require uploading sensitive data? |
| Cost risk | Is pricing clear? Is there a hidden upgrade trap? |
| Lock-in risk | Can data or outputs be exported? |
| Local-first | Can it run locally or stay browser-only if needed? |
| Traceability | Does it support logs, history, or reviewable outputs? |
| Capability fit | Does it solve a reusable capability gap? |
| Integration risk | Does it require backend/API/storage/login? |
| Review need | Does adoption require user approval? |

---

## 8. Scoring model v0.1

Use simple scores:

```text
0 = unknown / not enough information
1 = weak / risky
2 = acceptable with caution
3 = strong fit
```

Never use the score as final adoption permission.

```text
Score supports recommendation.
Score does not authorize signup, purchase, API use, or integration.
```

---

## 9. Included capabilities

| Capability ID | Capability | State | Role |
|---|---|---|---|
| CAP-CAND-003 | AI Tool Candidate Evaluation | candidate / internal-spec | Evaluate tool candidates safely |
| CAP-COS-002 | User Review Boundary Gate | internal-spec | Require approval before adoption |
| CAP-COS-003 | Public-Safe Boundary Guard | internal-spec | Prevent data / claim overreach |
| CAP-COS-001 | Capability Registry Maintainer | registered | Route reusable findings into registry/backlog |

---

## 10. Allowed operating modes

Allowed now:

```text
public-info research
report-only comparison
candidate scoring matrix
risk note
cost note
capability fit mapping
recommendation draft
```

Not allowed now:

```text
signing up for tools
starting free trials
paying for tools
entering credit card details
using API keys
connecting GitHub / Gmail / Drive / Slack / customer systems
uploading real data
building production integrations
```

---

## 11. Human review gates

User review is required before:

```text
- signup
- free trial activation
- paid upgrade
- API key usage
- OAuth connection
- installing browser extension
- connecting repository / email / drive / calendar / Slack
- uploading private files
- using customer data
- changing production workflow
- publicly recommending a tool as adopted
```

User review is not required for:

```text
- public website research
- report-only candidate list
- internal scoring matrix
- docs-only recommendation draft
- capability gap mapping
```

---

## 12. Tool recommendation levels

Use these recommendation levels:

```text
REJECT_NOW = too risky or irrelevant
WAIT = interesting but not needed yet
WATCHLIST = track later
RESEARCH_DEEPER = needs more public-source review
PILOT_BOUNDARY_REQUIRED = only after explicit user review
ADOPTION_BLOCKED = current boundary does not allow adoption
```

Do not use:

```text
APPROVED
ADOPT_NOW
READY_FOR_PRODUCTION
SAFE_FOR_CUSTOMER_DATA
COMPLIANCE_READY
```

---

## 13. Report template

```text
# TOOL-RESEARCH-[ID]｜[Tool Category] Candidate Research

## 1. Research question

## 2. Why this matters

## 3. Candidate tools

| Tool | Use case | Public-safe fit | Data risk | Cost risk | Lock-in risk | Traceability | Notes |
|---|---|---:|---:|---:|---:|---:|---|

## 4. Boundary notes

## 5. Capability fit

## 6. Recommendation

## 7. Blocked actions

## 8. Next safe step
```

---

## 14. Example routing

### Example A — tool requires uploading customer data

```text
Recommendation: ADOPTION_BLOCKED
Reason: requires private data before value can be tested
Next safe step: search for synthetic-data or local-first alternative
```

### Example B — tool has useful concept but no current need

```text
Recommendation: WAIT
Reason: useful but not needed during public feedback wait
Next safe step: add to watchlist, no action
```

### Example C — tool fits a capability gap but needs API key

```text
Recommendation: PILOT_BOUNDARY_REQUIRED
Reason: may solve capability gap, but API key/integration requires user review
Next safe step: draft controlled pilot boundary, do not connect yet
```

---

## 15. Boundary statement

Safe statement:

```text
Tool Research Department is an internal report-only department for evaluating AI tools using public information, safety boundaries, cost risk, lock-in risk, traceability, and capability fit. It does not sign up, pay, connect APIs, or process private data.
```

Unsafe statements to avoid:

```text
Tool Research Department can automatically adopt tools.
Tool Research Department approves vendor integrations.
Tool Research Department validates tool security or compliance.
Tool Research Department can test tools with customer data.
Tool Research Department manages procurement.
```

---

## 16. Current operating state

```text
Department status: internal-spec
Allowed mode: report-only / public-info only
Signup/payment/API usage: blocked
Private data: blocked
Production integration: blocked
Main merge: user review required
```

---

## 17. Closeout

```text
DEPARTMENT-003 result: PASS
Tool Research Department draft created: yes
Report-only boundary defined: yes
Public-safe boundary preserved: yes
No signup / payment / API usage authorized: yes
No public demo code changed: yes
No backend / AI API added: yes
No real customer data added: yes
Recommended next: TOOL-RESEARCH-001 candidate list only after public feedback checkpoint or explicit user direction
```

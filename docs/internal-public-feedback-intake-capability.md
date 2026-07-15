# INTERNAL-SYS-001｜Public Feedback Intake Capability

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal operating spec / public-safe  
**Date:** 2026-07-08  
**Mode:** Report-only / feedback-routing only  
**Do not use for:** sales automation, production support, legal / security / compliance claims, paid outreach, or handling private customer data.

> 中文定位：這份文件不是對外行銷文，也不是正式客服 SOP。它是 Future Ability Universe 內部用來處理公開回饋的低風險能力規格：當 GitHub / DEV / Reddit / Hacker News / Indie Hackers 等公開平台出現留言或反應時，先分類、判斷、回覆，再決定是否轉成內部改善任務或 Capability 候選。

---

## 1. Purpose

Public feedback should not be treated as random comments only. Each public response is a signal that can help the system decide whether the prototype is understandable, whether the public-safe boundary is clear, and whether a repeated concern should become a reusable capability.

```text
public feedback
→ classify
→ decide whether to reply
→ generate safe reply
→ route internal action
→ extract capability candidate
→ update future improvement backlog
```

中文說明：

```text
公開留言 / 點讚 / 質疑 / 沒反應
→ 分類
→ 判斷是否需要回覆
→ 產生安全回覆方向
→ 判斷是否轉內部任務
→ 判斷是否可抽象成 Capability
→ 累積成下一版改善依據
```

---

## 2. Scope

### In scope

```text
- GitHub feedback issue comments
- DEV Community comments / reactions
- Reddit comments / upvotes / downvotes when visible
- Hacker News comments / points when visible
- Indie Hackers replies / account unlock status
- Launching Next public listing status if available
- direct public-safe feedback copied manually without private identity
```

### Out of scope

```text
- collecting real customer data
- collecting private company workflows
- asking for credentials, API keys, screenshots, or internal documents
- making production-readiness claims
- making legal / privacy / cybersecurity / compliance guarantees
- promising a SaaS roadmap
- paid outreach or paid platform upgrades
- automatic posting, voting, scraping, or spam-like engagement
```

中文邊界：只處理公開、低風險、可摘要的訊號；不碰真實客戶資料、不要求對方提供內部文件、不承諾產品化、不把 prototype 說成正式 SaaS。

---

## 3. Feedback entry schema

Use this structure for every meaningful public signal.

```text
Feedback ID:
Date observed:
Source platform:
Source URL:
Signal type: comment / reaction / no-response / listing-status / account-status
Raw public summary:
Private data removed: yes / no / not applicable
Feedback type:
User intent:
Misunderstanding present: yes / no / unclear
Product signal:
Reply needed: yes / no / wait
Suggested reply:
Internal action:
Capability candidate:
Priority: P0 / P1 / P2 / P3
Owner mode: manual reply / backlog / v0.2 candidate / no action
Boundary check: pass / needs review / blocked
```

中文說明：這不是要複製大量原文，而是把公開訊號整理成可判斷的結構。若留言包含個人資訊、公司資訊或不必要細節，先摘要，不要原樣納入。

---

## 4. Feedback type taxonomy

| Type | Meaning | System interpretation | Default action |
|---|---|---|---|
| `clarity_question` | Reader does not understand what it is | Positioning may be unclear | Reply + consider copy improvement |
| `misunderstanding_saas` | Reader treats it as finished SaaS | Boundary needs reinforcement | Reply with prototype boundary |
| `why_not_chatgpt` | Reader sees it as generic chatbot output | Workflow/process differentiation unclear | Reply with repeatable-process explanation |
| `why_no_backend_or_ai_api` | Reader expects backend or AI API | Public-safe design needs explanation | Reply with intentional boundary explanation |
| `feature_request` | Reader asks for export, login, API, team mode, etc. | Potential backlog signal | Thank + backlog; do not promise |
| `use_case_signal` | Reader gives a concrete workflow scenario | High-value learning signal | Ask safe follow-up; extract use case |
| `security_or_compliance_question` | Reader asks about security, privacy, compliance | High overclaim risk | De-escalate; clarify prototype only |
| `negative_reaction` | Reader dismisses or criticizes | Could reveal positioning gap | Do not defend; clarify only if useful |
| `supportive_reaction` | Reader likes, saves, upvotes, or says useful | Positive signal, may not need reply | Acknowledge if comment exists |
| `no_response_signal` | No comments after waiting window | Distribution or clarity may be weak | Wait / adjust framing later, not immediate rewrite |
| `spam_or_offtopic` | Irrelevant or hostile noise | No product signal | Ignore or moderate per platform rules |

Priority rules:

```text
P0 = creates unsafe overclaim, asks for sensitive data, or could make prototype look production-ready
P1 = blocks first-reader understanding or repeats across platforms
P2 = useful improvement candidate but not blocking
P3 = future idea / backlog only
```

---

## 5. Reply strategy matrix

### 5.1 General reply style

Always follow this tone:

```text
- appreciative
- non-defensive
- prototype-first
- no hard selling
- no production claim
- no compliance claim
- no roadmap promise
- no request for sensitive data
```

中文原則：先感謝、再澄清、最後只邀請 public-safe feedback。不要辯論、不要硬賣、不要把它講成正式產品。

---

### 5.2 If asked: “Why no backend / AI API?”

Safe reply pattern:

```text
Thanks for checking it out. The no-backend / no-AI-API design is intentional for this stage.

This prototype is trying to validate the workflow framing and public-safe boundary first: can someone understand the risk level, safe first test, human review gate, validation checklist, and trace note before any real data or production system is involved?

If that framing is understandable, more complex features can be explored later. For now, keeping it browser-only helps avoid collecting sensitive data too early.
```

中文判斷：這類問題通常不是攻擊，而是對方期待更完整產品。回覆重點不是說「我還沒做」，而是說「這階段刻意先驗證 public-safe workflow framing」。

---

### 5.3 If asked: “Why not just ChatGPT?”

Safe reply pattern:

```text
That is a fair question. ChatGPT can absolutely help brainstorm a workflow.

The difference I am exploring here is repeatability: this prototype tries to turn the same review pattern into a structured flow — risk level, safe first test, human review gate, validation checklist, and trace note — so a team can discuss the workflow boundary before connecting AI to real data or production tools.

So it is not meant to replace ChatGPT. It is a small prototype for making the first AI workflow review more traceable and repeatable.
```

中文判斷：這是核心定位問題。不要說 ChatGPT 不好，要說 WorkflowGuard AI 的重點是「可重複檢查流程」而不是一次性回答。

---

### 5.4 If asked about security / compliance

Safe reply pattern:

```text
Good point. I would not describe this as a security, privacy, legal, or compliance solution.

It is only an early public-safe prototype for reviewing workflow boundaries before sensitive data or production systems are involved. The current version does not store input, does not use real customer data, does not connect to a backend, and does not call an AI API.

Any real deployment would still need proper security, privacy, legal, and operational review.
```

中文判斷：這類問題要降調，不能順勢說自己符合安全或合規。只說 prototype 可以幫助前期討論邊界。

---

### 5.5 If receiving a feature request

Safe reply pattern:

```text
Thanks, that is useful feedback. I am collecting feature ideas carefully because the current version is intentionally public-safe and small.

I will treat this as a backlog candidate rather than a promise. The first thing I want to validate is whether the workflow review structure itself is clear and useful.
```

Internal routing:

```text
feature_request
→ backlog candidate
→ do not implement immediately
→ check whether the request preserves public-safe boundary
→ consider for v0.2 only if repeated or strongly connected to clarity
```

---

### 5.6 If receiving a concrete use case

Safe reply pattern:

```text
That use case is helpful. I am trying to understand which early AI workflow reviews are easiest to make safe and understandable.

Without sharing any private data, would you frame this as more of a customer-support, internal-knowledge, reporting, sales, or operations workflow?
```

Internal routing:

```text
use_case_signal
→ high-value signal
→ summarize without private data
→ convert into synthetic scenario candidate
→ consider capability candidate
```

中文提醒：可以追問類型，但不要請對方貼公司內部資料。

---

### 5.7 If no one responds after 12–24 hours

Do not treat silence as failure immediately.

Possible interpretations:

```text
- audience mismatch
- title / hook not clear enough
- prototype value requires stronger use case framing
- post timing issue
- platform account trust is low
- call-to-action is too broad
```

Default action:

```text
wait → record no_response_signal → do not rewrite product immediately → prepare alternate framing later
```

中文判斷：沒留言不代表東西錯，可能只是切角、平台、時間、帳號新舊問題。先記錄，不要馬上大改。

---

## 6. Internal action router

| Condition | Internal action | Allowed now? | Notes |
|---|---|---:|---|
| One person asks what this is | Improve reply only | yes | Do not change repo yet |
| Multiple people say they do not understand | Create copy-improvement task | yes | v0.2 candidate |
| One person asks for backend / AI API | Reply with boundary | yes | No implementation |
| Multiple people ask for export / copy output | Add backlog candidate | yes | Low-risk if browser-only |
| Someone provides a concrete use case | Create synthetic scenario candidate | yes | Remove all private details |
| Someone asks for compliance/security guarantee | Add boundary clarification candidate | yes | Avoid overclaim |
| Someone asks for real deployment | Reply: not production-ready | yes | Do not invite sensitive data |
| Spam / hostile / irrelevant comment | Ignore or moderate | yes | No product signal |
| No response in first window | Record signal only | yes | Wait before repositioning |

---

## 7. Capability extraction rule

A public comment can become a Capability candidate only if it describes a repeatable workflow pattern.

Capability candidate template:

```text
Capability candidate name:
Source signal:
Problem:
Input:
Safe first test:
Human review gate:
Validation checklist:
Trace note:
Boundary:
Reusable department:
Priority:
```

Example:

```text
Capability candidate name: Customer Support AI Workflow Safety Preview
Source signal: public user mentions AI customer support use case
Problem: team wants to use AI for customer replies but should not auto-send too early
Input: synthetic or anonymized support-ticket examples
Safe first test: generate draft-only reply suggestions from fake tickets
Human review gate: human must approve every reply before customer-facing use
Validation checklist: tone, factuality, privacy, escalation, unsupported claims
Trace note: prototype preview only; not autonomous customer support
Boundary: no real customer data, no auto-send, no production integration
Reusable department: Workflow Safety Department
Priority: P1 if repeated, P2 if single signal
```

---

## 8. Validation gate before any reply

Before replying publicly, confirm:

```text
- reply does not sound defensive
- reply does not hard-sell
- reply does not claim this is finished SaaS
- reply does not claim production readiness
- reply does not claim legal / privacy / cybersecurity / compliance guarantee
- reply does not ask for private data
- reply does not promise a roadmap
- reply keeps the prototype seeking feedback
- reply is short enough for the platform
```

Result:

```text
PASS = safe to reply
NEEDS_REVIEW = user should review before posting
BLOCKED = do not reply in current form
```

---

## 9. Validation gate before any internal task

Before creating a repo improvement task from public feedback, confirm:

```text
- task is based on an actual signal, not anxiety
- task does not require backend, storage, login, or AI API unless explicitly approved later
- task does not add sensitive data or private examples
- task does not create production / compliance claims
- task is small enough for v0.2 or clearly marked backlog
- task can be validated by reading or browser-only demo behavior
```

Allowed task modes:

```text
report-only
copy-only
docs-only
browser-only static demo improvement
synthetic scenario addition
backlog entry
```

Blocked task modes for this stage:

```text
backend integration
AI API integration
real customer data handling
login / account system
payment / pricing
automated public posting
security or compliance certification claims
production automation
```

---

## 10. Current operating state

```text
PUBLIC-FEEDBACK-WAIT-001: active
INTERNAL-SYS-001: prepared
External platforms: waiting for natural feedback
New platform push: paused
Indie Hackers: warm-up only, no paid upgrade, no spam
Repo demo changes: paused unless feedback shows P0/P1 clarity issue
Backend / AI API: not allowed at this stage
Production claim: not allowed
Real customer data: not allowed
```

---

## 11. Minimal use procedure

When the user says: “check public feedback”

```text
1. Review public feedback sources.
2. Summarize visible comments / reactions.
3. Classify each signal using this taxonomy.
4. Decide whether reply is needed.
5. Draft short safe replies.
6. Decide whether any internal action is needed.
7. Extract capability candidates only from repeatable workflow patterns.
8. Do not change demo unless feedback creates a P0/P1 reason.
```

Expected response to user:

```text
Platform:
Signal:
Feedback type:
Meaning:
Reply needed:
Suggested reply:
Internal action:
Capability candidate:
Risk / boundary note:
```

---

## 12. Closeout criteria

INTERNAL-SYS-001 is complete when:

```text
- public feedback types are defined
- reply strategies are defined
- internal routing rules are defined
- capability extraction rule is defined
- safety gates are defined
- current operating state is documented
- no public demo code is changed
- no backend / AI API / data storage is introduced
```

Result:

```text
INTERNAL-SYS-001 result: PASS
Recommended next internal task: INTERNAL-SYS-002｜Capability Registry v0.1
```

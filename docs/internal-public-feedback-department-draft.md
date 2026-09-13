# DEPARTMENT-002｜Public Feedback Department Draft

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal department draft / public-safe  
**Date:** 2026-07-08  
**Mode:** Docs-only / department draft  

> 中文定位：這份文件把公開回饋處理正式整理成第二個 AI Department：Public Feedback Department。它的任務不是行銷自動化，也不是自動公開發文，而是把 GitHub / DEV / Reddit / Hacker News / Indie Hackers / Launching Next 等公開訊號，用安全、可追蹤、可轉成 Capability 的方式處理。

---

## 1. Department identity

```text
Department ID: DEPT-002
Department name: Public Feedback Department
Status: internal-spec
Lifecycle state: internal-spec
Public surface: none
Internal surface: feedback intake docs + reply templates + action router + capability registry
Maturity note: internal operating department only
```

中文說明：這個部門不負責「推廣更多平台」，也不負責「自動回留言」。它只負責把已經出現的公開回饋轉成可管理的系統訊號。

---

## 2. Purpose

Convert public comments, reactions, no-response signals, and listing statuses into:

```text
- structured feedback entries
- feedback type classifications
- safe reply drafts
- internal action recommendations
- backlog candidates
- capability candidates
- public launch learning summaries
```

---

## 3. Problem solved

Without a Public Feedback Department, public signals may cause random reactions:

```text
one comment → panic rewrite
no response → assume failure
feature request → promise roadmap
security question → overclaim maturity
criticism → defensive reply
```

The safer path is:

```text
public signal
→ intake
→ classify
→ check boundary
→ draft reply if needed
→ route internal action
→ extract capability candidate only if repeatable
→ wait / backlog / implement docs-only if justified
```

---

## 4. Input sources

Allowed input sources:

```text
- GitHub feedback issue comments
- DEV Community comments / reactions
- Reddit comments / visible votes when available
- Hacker News comments / points when visible
- Indie Hackers account / comment status
- Launching Next listing status if visible
- public-safe feedback copied manually without private identity
```

Blocked input sources:

```text
- private customer documents
- internal company screenshots
- credentials / API keys / secrets
- private messages containing sensitive details
- production workflow exports
- paid lead lists
- scraped private data
```

---

## 5. Process

The department process is:

```text
1. Observe existing public surfaces only.
2. Summarize visible public signal.
3. Remove unnecessary identity or private details.
4. Classify feedback type.
5. Determine reply needed: yes / no / wait.
6. Draft safe reply if needed.
7. Run reply boundary validation.
8. Route internal action.
9. Extract capability candidate if the pattern is repeatable.
10. Record no-response as weak signal, not failure.
```

---

## 6. Standard output package

```text
Platform:
Signal:
Feedback type:
User intent:
Misunderstanding present:
Product signal:
Reply needed:
Suggested reply:
Internal action:
Capability candidate:
Priority:
Boundary check:
Recommended next action:
```

---

## 7. Included capabilities

| Capability ID | Capability | State | Role |
|---|---|---|---|
| CAP-FBK-001 | Public Feedback Intake | internal-spec | Convert public signals into structured feedback entries |
| CAP-FBK-002 | Feedback Classifier | internal-spec | Identify feedback type and priority |
| CAP-FBK-003 | Reply Strategy Generator | internal-spec | Draft safe public replies for user review |
| CAP-FBK-004 | Internal Action Router | internal-spec | Route to no action / reply / backlog / docs-only improvement |
| CAP-FBK-005 | Capability Candidate Extractor | internal-spec | Extract reusable workflow patterns |
| CAP-COS-003 | Public-Safe Boundary Guard | internal-spec | Prevent overclaims and unsafe replies |

---

## 8. Feedback taxonomy

Use these feedback types:

```text
clarity_question
misunderstanding_saas
why_not_chatgpt
why_no_backend_or_ai_api
feature_request
use_case_signal
security_or_compliance_question
negative_reaction
supportive_reaction
no_response_signal
spam_or_offtopic
```

Priority rules:

```text
P0 = unsafe overclaim, sensitive-data risk, or prototype looks production-ready
P1 = repeated first-reader confusion or boundary confusion
P2 = useful improvement candidate but not blocking
P3 = future idea / backlog only
```

---

## 9. Allowed operating modes

Allowed now:

```text
report-only feedback summary
draft-only reply generation
internal backlog routing
capability candidate extraction
public launch learning summary
no-response signal recording
```

Not allowed now:

```text
automatic public posting
automatic public replies
new platform submissions
paid promotion
spam-like engagement
asking for private data
turning one comment into immediate demo rewrite
making production / compliance / security claims
```

---

## 10. Human review gates

User review is required before:

```text
- posting any public reply
- changing public demo behavior
- changing public positioning copy
- submitting to a new external platform
- paying for listing / promotion / upgrade
- turning feedback into public roadmap promise
- requesting private data from someone
- merging branch into main
```

---

## 11. Reply safety rules

All reply drafts must pass:

```text
- appreciative
- non-defensive
- not hard-selling
- prototype-first
- no production-readiness claim
- no compliance/security/legal/privacy guarantee
- no roadmap promise
- no private-data request
- short enough for platform context
```

Use:

```text
internal-public-reply-template-pack.md
internal-prototype-overclaim-risk-register.md
internal-user-review-required-boundary.md
```

---

## 12. No-response handling

No-response is a weak signal, not a failure.

Possible interpretations:

```text
- title/hook not strong enough
- platform mismatch
- account trust too low
- timing issue
- audience did not understand the use case
- call-to-action unclear
- topic is niche
```

Default action:

```text
record → wait → summarize → do not panic rewrite → do not add platforms immediately
```

---

## 13. Internal action router

| Condition | Action | Allowed now? |
|---|---|---:|
| One clarity question | draft reply / maybe copy backlog | yes |
| Repeated clarity question | create copy-improvement candidate | yes, docs-only |
| Why no backend/API | reply with boundary | yes, draft-only |
| Why not ChatGPT | reply with repeatability framing | yes, draft-only |
| Security/compliance question | reply with non-guarantee boundary | yes, draft-only |
| Feature request | backlog candidate | yes |
| Concrete use case | capability candidate if repeatable | yes |
| Hostile/offtopic | ignore / no action | yes |
| No response | record weak signal | yes |
| Request for real data handling | block / boundary reply | yes, draft-only |

---

## 14. Capability extraction rule

A public feedback signal becomes a capability candidate only when:

```text
- it describes a repeatable workflow pattern
- it can be tested with synthetic or non-sensitive examples
- it does not require backend / AI API now
- it does not require real customer data now
- it can be assigned to an owner department
- it has a safe first test and validation idea
```

Do not extract a capability when:

```text
- it is a one-off opinion
- it is spam/offtopic
- it requires production integration immediately
- it requires legal/security/compliance assurance
- it cannot be validated safely
```

---

## 15. Public feedback checkpoint procedure

When checking public feedback:

```text
1. Check only existing public surfaces.
2. Summarize visible signals.
3. Classify each signal.
4. Draft replies only if needed.
5. Do not post replies automatically.
6. Route internal action.
7. Extract capability candidates if repeatable.
8. Summarize no-response without overreacting.
```

Expected user-facing summary:

```text
Platform:
Signal:
Meaning:
Reply needed:
Suggested reply:
Internal action:
Capability candidate:
Boundary note:
```

---

## 16. Boundary statement

Safe statement:

```text
Public Feedback Department is an internal department concept for processing public feedback about WorkflowGuard AI. It creates structured summaries, safe reply drafts, internal action recommendations, and capability candidates. It does not automatically post, scrape private data, or change the public demo.
```

Unsafe statements to avoid:

```text
Public Feedback Department automates community management.
Public Feedback Department handles customer support.
Public Feedback Department collects leads.
Public Feedback Department automatically replies to users.
Public Feedback Department turns comments into product roadmap promises.
```

---

## 17. Closeout

```text
DEPARTMENT-002 result: PASS
Public Feedback Department draft created: yes
Auto-posting allowed: no
User review before public reply: required
Public-safe boundary preserved: yes
No public demo code changed: yes
No backend / AI API added: yes
No real customer data added: yes
Recommended next: DEPARTMENT-003｜Research-to-Capability Department Draft or public feedback checkpoint
```

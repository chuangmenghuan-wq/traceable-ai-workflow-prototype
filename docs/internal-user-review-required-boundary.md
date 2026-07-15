# GATE-001｜User Review Required Boundary

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal safety gate / public-safe  
**Date:** 2026-07-08  
**Mode:** Docs-only / operating boundary  

> 中文定位：這份文件定義「哪些事情 AI General Manager 可以直接往下做」與「哪些事情一定要停下來讓使用者審核」。目的不是降低使用者控制權，而是減少低風險任務反覆詢問，同時保護公開定位、資料安全與產品邊界。

---

## 1. Core rule

```text
Low-risk internal work can continue automatically.
Public-facing, production-impacting, data-impacting, paid, or claim-changing work requires user review.
```

中文原則：

```text
內部、低風險、文件/報告/規格類任務，可以自動往下做。
只要牽涉公開發文、公開回覆、主線合併、demo 改動、API/backend、真實資料、付款、正式產品承諾，就必須停下來給使用者審核。
```

---

## 2. Continue automatically

The assistant / system may continue without asking the user when all conditions below are true:

```text
- docs-only
- report-only
- internal spec only
- public-safe wording
- no public posting
- no public reply
- no merge to main
- no live demo behavior change
- no backend / API / storage / login
- no real customer data
- no private company data
- no payment / subscription / upgrade
- no legal / privacy / cybersecurity / compliance guarantee
- no production-readiness claim
- reversible by leaving a branch, draft PR, or open issue
```

Examples:

```text
- create an internal docs-only spec
- create a draft PR for review
- add a report-only issue
- classify internal capabilities
- draft a safe reply for user review
- summarize public feedback without posting
- create a backlog entry
- write a public-safe boundary checklist
```

---

## 3. User review required

User review is required before any of the following:

```text
- merging a PR into main
- changing the live GitHub Pages demo behavior
- editing public-facing positioning copy in a way that changes product claims
- posting publicly under the user's account
- replying publicly to comments under the user's account
- submitting to a new external platform
- paying for any upgrade, listing, promotion, subscription, or tool
- adding backend, database, storage, login, authentication, or user accounts
- adding AI API calls or API keys
- handling real customer data or private company data
- accepting screenshots, documents, credentials, or internal workflow exports
- making legal, privacy, cybersecurity, compliance, financial, medical, or professional guarantee claims
- presenting the prototype as production-ready SaaS
- starting client outreach or paid pilot conversation
```

---

## 4. Blocked unless explicitly approved later

These actions are blocked in the current public-safe prototype phase:

```text
- backend integration
- AI API integration
- data storage
- user login system
- payment / pricing page
- automated public posting
- scraping beyond normal visible manual checks
- production workflow automation
- real customer data processing
- client-data pilot
- compliance / security certification language
- enterprise-ready claim
```

If one of these becomes necessary later, it must become a separate reviewed task with scope, validation, rollback, and safety boundary.

---

## 5. Public reply gate

A public reply can be drafted automatically, but posting requires user review.

Before the user posts a suggested reply, the draft must pass:

```text
- not defensive
- not hard-selling
- not claiming finished SaaS
- not claiming production readiness
- not claiming legal / privacy / cybersecurity / compliance guarantee
- not asking for private data
- not promising roadmap
- keeps prototype seeking feedback
- short enough for the platform
```

Result options:

```text
PASS = safe to show user as a suggested reply
NEEDS_REVIEW = user must review carefully before posting
BLOCKED = do not post
```

---

## 6. GitHub work gate

### Automatically allowed

```text
- create internal docs-only branch
- create draft PR
- create internal docs-only file on a branch
- create report-only issue
- add safety / boundary / registry docs
- compare branch changes
- fetch files for validation
```

### User review required

```text
- merge PR into main
- mark draft PR ready if it changes public positioning
- close many issues at once
- delete files
- edit README public positioning significantly
- change GitHub Pages live demo behavior
- change repository description / topics / release status
```

### Cleanup note

If the issue queue grows too much, the correct action is:

```text
pause new issue creation
prioritize implementation docs
close or consolidate obvious duplicates only after review, unless they are clearly accidental placeholder issues
```

---

## 7. Public feedback wait gate

During `PUBLIC-FEEDBACK-WAIT-001`:

Allowed:

```text
- check existing public pages when asked
- summarize comments / reactions
- draft safe replies for user review
- classify feedback
- update internal registry or backlog
- prepare report-only learning summary
```

Blocked:

```text
- add new public platforms
- post new launch messages
- pay for promotion
- spam warm-up comments
- rewrite demo without P0/P1 feedback reason
- overreact to no-response signal
```

---

## 8. Capability Registry gate

A capability may be added to the registry automatically if:

```text
- it is internal or public-safe
- it is docs-only / report-only
- it has clear input and output
- it has a boundary
- it has validation criteria
- it does not imply production maturity
```

User review is required if:

```text
- capability requires production integration
- capability requires backend / AI API
- capability touches real customer data
- capability changes public positioning
- capability could be interpreted as compliance/security guarantee
```

---

## 9. Decision table

| Action | Auto-continue? | User review? | Notes |
|---|---:|---:|---|
| Internal docs-only spec | yes | no | Low risk |
| Draft PR | yes | no | No merge |
| Main merge | no | yes | Always review |
| Public reply draft | yes | yes before posting | Draft only |
| Public reply posting | no | yes | User controls account |
| New external platform | no | yes | Avoid spam / overexpansion |
| Demo copy typo fix | conditional | maybe | If public positioning changes, review |
| Demo behavior change | no | yes | Live public surface |
| Backend / AI API | no | yes | Currently blocked |
| Real data handling | no | yes | Currently blocked |
| Payment / upgrade | no | yes | Always review |
| Capability registry update | yes | no | If internal and public-safe |
| Closing accidental placeholder issue | conditional | maybe | Single obvious accident can be cleaned; batch cleanup needs review |

---

## 10. Current operating policy

```text
PUBLIC-FEEDBACK-WAIT-001: active
Internal docs-only strengthening: allowed
Public demo changes: paused
New platform push: paused
Public replies: draft-only until user review
Main merge: user review required
Backend / AI API: blocked
Real customer data: blocked
Payment / upgrade: blocked
Production claim: blocked
```

---

## 11. Closeout

```text
GATE-001 result: PASS
Automatic continuation boundary: defined
User review boundary: defined
Current phase: internal strengthening + public feedback wait
Recommended next implementation: INTERNAL-SYS-003｜WorkflowGuard AI ↔ Internal COS Mapping
```

# META-001｜No-New-Platform Guard During Feedback Wait

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal guard / public-safe  
**Date:** 2026-07-08  
**Mode:** Docs-only / external-expansion control  

> 中文定位：這份文件定義在 `PUBLIC-FEEDBACK-WAIT-001` 期間，不再新增外部平台、不再付費曝光、不再洗版暖帳號。目的不是放棄推廣，而是先讓已經投放的平台自然產生訊號，再用系統化方式判斷下一步。

---

## 1. Core rule

```text
During PUBLIC-FEEDBACK-WAIT-001, do not add new public platforms.
```

中文規則：

```text
公開回饋等待期內，不新增平台、不追加曝光、不付費加速、不洗版留言。
```

Reason:

```text
The current goal is learning quality, not exposure quantity.
```

---

## 2. Current allowed public surfaces

Existing public surfaces already used or prepared:

```text
- GitHub repository
- GitHub Pages demo
- GitHub feedback issue
- DEV Community post
- Reddit r/SideProject post
- Hacker News post
- Launching Next free queue submission
- Indie Hackers warm-up status only
```

These can be checked for feedback when needed.

---

## 3. Allowed during wait mode

```text
- check existing public pages when the user asks
- summarize visible comments / reactions
- classify feedback using Public Feedback Intake
- draft safe replies for user review
- record no-response signals
- update internal docs-only registry / backlog
- prepare report-only learning summary
```

---

## 4. Blocked during wait mode

```text
- new launch-directory submissions
- new social posts
- new community posts
- paid fast-track listings
- paid platform upgrades
- Indie Hackers Plus upgrade
- spam-like warm-up comments
- repeating the same post across platforms
- changing public positioning without feedback reason
- rewriting the demo because of anxiety rather than signal
```

---

## 5. When platform expansion can resume

Platform expansion may be reconsidered only after:

```text
- first public feedback checkpoint is completed
- no-response signals are summarized
- reply-needed items are handled or drafted
- v0.2 changes are either rejected or clearly justified
- a new audience hypothesis is written
- user review approves another public push
```

---

## 6. No-response interpretation

No-response does not automatically mean failure.

Possible meanings:

```text
- audience mismatch
- weak title / hook
- platform timing issue
- low account trust
- unclear call-to-action
- prototype needs stronger use case framing
- topic is niche and requires repeated exposure later
```

Default action:

```text
record → wait → summarize → do not immediately rewrite demo or add platforms
```

---

## 7. Guard decision table

| Proposed action | Allowed now? | Reason |
|---|---:|---|
| Check GitHub issue comments | yes | Existing public surface |
| Check DEV / Reddit / HN reactions | yes | Existing public surfaces |
| Draft reply for user review | yes | No auto-posting |
| Post reply publicly | no | User review required |
| Submit to another directory | no | New platform expansion |
| Pay for fast-track listing | no | Payment / promotion risk |
| Warm up with more comments | no | Spam / reputation risk |
| Update internal backlog | yes | Docs-only |
| Change demo because no one replied | no | Needs feedback evidence |
| Add synthetic scenario from repeated feedback | conditional | Requires feedback signal |

---

## 8. Current operating state

```text
PUBLIC-FEEDBACK-WAIT-001: active
New platform push: blocked
Paid promotion: blocked
Public reply: user review required
Existing platform check: allowed
Internal docs-only strengthening: allowed
Demo change: paused unless P0/P1 feedback reason appears
```

---

## 9. Closeout

```text
META-001 result: PASS
No-new-platform guard created: yes
Public-safe boundary preserved: yes
No public demo code changed: yes
No backend / AI API added: yes
Recommended next: REPLY-TEMPLATE-001 or wait for public feedback checkpoint
```

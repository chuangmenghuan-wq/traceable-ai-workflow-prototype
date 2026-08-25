# PLAYBOOK-001｜Internal Task Handling Playbook

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal playbook / public-safe  
**Date:** 2026-07-08  
**Mode:** Docs-only / operating playbook  

> 中文定位：這份 playbook 定義當使用者連續要求「下一步」、「繼續」、「直到需要我批准」時，系統應如何安全、自動、可驗證地推進。它的目的不是讓系統無限產生文件，而是讓自動推進有邊界、有節奏、有停損點。

---

## 1. Core rule

```text
Continue automatically only while the next step is internal, reversible, docs/report-only, branch-only, and does not affect public surfaces or real data.
```

中文規則：

```text
只要還是內部、可回退、文件/報告型、分支內、不碰公開/真實資料，就可以自動往下做。
```

---

## 2. Allowed automatic actions

The assistant/system may continue automatically with:

```text
- internal docs-only files
- report-only validation
- capability mapping
- department routing
- lifecycle classification
- synthetic-only planning
- internal runbook refinement
- branch-only PR body update
- compare/diff validation
- safety closeout report
```

---

## 3. Actions requiring user approval

Stop and ask for approval before:

```text
- merging into main
- marking draft PR as ready if public-facing impact exists
- changing public demo behavior
- editing public README / public positioning copy
- replying publicly
- posting to public platforms
- submitting to competitions
- creating public slides or pitch material
- closing many issues at once
- adding backend / API / storage / login
- using real customer data or private documents
- signup / payment / OAuth / API key usage
- making production / compliance / legal / privacy / cybersecurity claims
```

---

## 4. Task selection order

When user says “next step,” choose the first safe applicable action:

```text
1. Validate current branch or batch.
2. Close out completed internal batch.
3. Convert scattered docs into runbook/playbook.
4. Map capabilities to departments and lifecycle states.
5. Add validation/checklist only if it prevents real risk.
6. Add short queue only if it reduces sprawl.
7. Stop if next action is public/main/backend/data/payment/claim-impacting.
```

---

## 5. Anti-sprawl rule

Do not create documents just because another document can exist.

A new internal file is allowed only if it does at least one of these:

```text
- reduces ambiguity
- connects existing components
- defines a reusable operating procedure
- validates safety or boundaries
- closes a batch
- prevents accidental public/production overreach
- creates a limited task queue
```

If it does not:

```text
stop and summarize instead of creating another file
```

---

## 6. Internal task classification

Use this classification:

```text
AUTO_CONTINUE = safe internal docs/report-only branch work
AUTO_VALIDATE = safe validation or diff check
AUTO_CLOSEOUT = safe batch closeout
ASK_USER = user approval required
BLOCKED = unsafe or outside current phase
```

Examples:

| Proposed task | Classification | Reason |
|---|---|---|
| Add internal runbook | AUTO_CONTINUE | docs-only, improves operation |
| Compare branch with main | AUTO_VALIDATE | read-only validation |
| Update PR body | AUTO_CONTINUE | branch/PR metadata only |
| Merge PR | ASK_USER | main branch change |
| Public reply | ASK_USER | public action |
| Add backend | ASK_USER / BLOCKED | architecture + data risk |
| New platform launch | ASK_USER | external expansion |
| Tool signup | ASK_USER | account/action risk |

---

## 7. Continuous progress loop

```text
receive next-step request
→ check approval boundary
→ choose safe internal task
→ create/update docs/report if useful
→ validate safety
→ update PR summary
→ decide whether another safe internal task exists
→ stop if next task requires approval or creates sprawl
```

---

## 8. Required validation after multi-step run

After several automatic internal actions, run:

```text
- PR summary update
- branch compare against main
- safety boundary summary
- stop condition check
```

---

## 9. Stop condition checklist

Stop when any is true:

```text
- next useful action is main merge
- next useful action is public feedback checkpoint
- next useful action changes public demo / README / public copy
- next useful action is public reply/post/submission
- next useful action needs backend/API/storage/login
- next useful action uses real data
- next useful action needs payment/signup/OAuth
- next useful action would be low-value document sprawl
```

---

## 10. Current application

Current project state:

```text
External expansion: paused
Internal upgrade: active
Branch-only docs/report work: allowed
Main merge: approval required
Public feedback checkpoint: approval preferred
Demo/README change: approval required
```

---

## 11. Closeout

```text
PLAYBOOK-001 result: PASS
Continuous next-step behavior defined: yes
Automatic safe-action boundary defined: yes
Approval boundary defined: yes
Anti-sprawl rule defined: yes
No public demo code changed: yes
No backend / AI API added: yes
No real customer data added: yes
Recommended next: STOP-GATE-001｜Internal Work Stop Gate
```

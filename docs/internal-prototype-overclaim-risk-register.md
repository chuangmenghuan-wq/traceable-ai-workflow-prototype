# RISK-001｜Prototype Overclaim Risk Register

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal risk register / public-safe  
**Date:** 2026-07-08  
**Mode:** Docs-only / risk control  

> 中文定位：這份文件列出 WorkflowGuard AI 在 public-safe prototype 階段最容易不小心講太滿的風險。目的不是對外防禦，而是讓所有文件、回覆、demo kit、比賽草稿、未來客戶試點草稿，都先避開過度承諾。

---

## 1. Core risk

WorkflowGuard AI is currently:

```text
public-safe prototype
browser-only demo
workflow review preview
synthetic / non-sensitive input only
feedback-seeking project
```

It is not currently:

```text
finished SaaS
production automation system
enterprise governance platform
security product
privacy product
legal / compliance solution
client-ready deployment
paid pilot offer
```

---

## 2. Risk categories

| Risk ID | Overclaim risk | Unsafe implication | Safe replacement |
|---|---|---|---|
| RISK-SaaS-001 | Calling it a SaaS product | Suggests launch, support, accounts, uptime, pricing | public-safe prototype / browser-only demo |
| RISK-Prod-001 | Saying production-ready | Suggests real workflow deployment is safe | early workflow review preview |
| RISK-Sec-001 | Saying security solution | Suggests cybersecurity assurance | data-boundary awareness / public-safe boundary |
| RISK-Privacy-001 | Saying privacy solution | Suggests privacy compliance | avoids collecting data in this prototype |
| RISK-Compliance-001 | Saying compliance-ready | Suggests formal compliance review | not a compliance guarantee |
| RISK-Legal-001 | Saying legal review | Suggests legal assurance | requires professional review for real deployment |
| RISK-Auto-001 | Saying AI automation system | Suggests the tool executes workflows | review preview only, no automation |
| RISK-Client-001 | Saying client-ready | Suggests real clients can plug in data | future controlled pilot only after review |
| RISK-ROI-001 | Claiming business ROI | Suggests measured economic proof | not yet measured; learning stage |
| RISK-Roadmap-001 | Promising future features | Creates commitment before validation | backlog candidate / future idea |

---

## 3. Safe positioning language

Allowed:

```text
WorkflowGuard AI is a public-safe prototype for reviewing AI workflow ideas before sensitive data or production systems are involved.
```

Allowed:

```text
It helps preview risk level, safe first test, human review gate, validation checklist, and trace note.
```

Allowed:

```text
The current version is browser-only, does not store input, does not call an AI API, and does not connect to a backend.
```

Allowed:

```text
The goal is to validate whether this workflow-safety framing is understandable and useful.
```

---

## 4. Unsafe wording to avoid

Avoid:

```text
WorkflowGuard AI is production-ready.
WorkflowGuard AI guarantees safe AI deployment.
WorkflowGuard AI is an enterprise AI governance platform.
WorkflowGuard AI ensures compliance.
WorkflowGuard AI provides cybersecurity review.
WorkflowGuard AI protects customer data.
WorkflowGuard AI can connect to your internal systems now.
WorkflowGuard AI is ready for paid pilots.
WorkflowGuard AI replaces professional security / legal / compliance review.
WorkflowGuard AI automates your workflows.
```

---

## 5. Reply-specific risk notes

### If someone asks “Is this a SaaS?”

Safe reply:

```text
Not yet. I would describe it as a public-safe prototype rather than a finished SaaS. The current version is intentionally browser-only and does not store input, call an AI API, or connect to a backend. I am using it to test whether the workflow-review structure is understandable before adding more complexity.
```

### If someone asks “Can I use this with real company data?”

Safe reply:

```text
I would not use real company or customer data with this prototype. The current version is meant for synthetic or non-sensitive workflow ideas only. Any real deployment would need separate security, privacy, legal, and operational review.
```

### If someone asks “Is this compliant / secure?”

Safe reply:

```text
No, I would not describe it as compliant or security-certified. It is only a public-safe workflow review prototype. It can help frame early questions, but it does not replace formal security, privacy, legal, or compliance review.
```

### If someone asks “Can it automate my workflow?”

Safe reply:

```text
No. The current prototype does not automate workflows. It helps preview the first safe test, human review gate, validation checklist, and trace note before any automation is considered.
```

---

## 6. Document review checklist

Before publishing or merging any public-facing wording, check:

```text
- Does it accidentally sound like a finished product?
- Does it imply production readiness?
- Does it imply compliance, legal, privacy, or security assurance?
- Does it imply real customer data can be used?
- Does it promise future features?
- Does it imply paid pilot readiness?
- Does it claim measured ROI?
- Does it stay prototype-first and feedback-seeking?
```

If any answer is unclear:

```text
rewrite / downgrade / ask user review
```

---

## 7. Allowed maturity statement

Safe maturity statement:

```text
Current maturity: public-safe prototype / feedback-seeking / browser-only demo.
```

Do not use:

```text
production-ready
enterprise-ready
client-ready
compliance-ready
security-ready
```

---

## 8. Current risk status

```text
SaaS overclaim risk: controlled
Production overclaim risk: controlled
Security / compliance overclaim risk: controlled
Client-data overclaim risk: controlled
Automation overclaim risk: controlled
Roadmap promise risk: controlled
```

Status remains controlled only if future copy follows this register.

---

## 9. Closeout

```text
RISK-001 result: PASS
Risk register created: yes
Public-safe positioning preserved: yes
No public demo code changed: yes
No backend / AI API added: yes
No production / compliance / security claim added: yes
Recommended next: public feedback checkpoint or META-001 no-new-platform guard if continuing internal-only work
```

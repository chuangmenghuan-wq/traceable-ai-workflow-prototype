# WorkflowGuard AI — Traceable AI Workflow Prototype

**Repository:** `traceable-ai-workflow-prototype`  
**Status:** Independent prototype / pre-company project  
**Release state:** Public-safe draft, not launched yet  
**Version:** Public-safe v0.6

> **Public prototype notice:** This is an early public prototype for reviewing AI workflow ideas before using sensitive or production data. It is not a finished SaaS product, production automation system, or legal / privacy / cybersecurity / compliance guarantee.

---

## Live demo

Open the static GitHub Pages demo:

```text
https://chuangmenghuan-wq.github.io/traceable-ai-workflow-prototype/
```

The live demo is a static public prototype page. It does not require login, does not store input, does not call an AI API, and does not connect to a backend.

---

## One-page overview

### What this is

WorkflowGuard AI helps answer one early question:

```text
Before we use AI in a real workflow, where can we start safely?
```

It turns a vague AI adoption idea into a small, reviewable workflow preview with:

```text
task intake → risk snapshot → safe first test → human review gate → validation checklist → trace note
```

The goal is not to replace professional review or build a full workflow automatically. The goal is to make the first AI step easier to understand, check, and discuss.

### Who this is for

This prototype is mainly for first-time reviewers, small teams, operators, and non-technical decision makers who want to understand where AI might fit without exposing sensitive data too early.

### What you can review in 3 minutes

1. [Live demo](https://chuangmenghuan-wq.github.io/traceable-ai-workflow-prototype/)
2. [Traditional Chinese plain-language overview](docs/chinese-plain-language-overview.md)
3. [Demo index](web/demo-index.html)
4. [5 synthetic workflow scenarios](examples/5-synthetic-workflow-scenarios.md)
5. [Mini audit preview](web/ai-workflow-planner.html)
6. [Public repo final check](docs/public-repo-final-check.md)

### What this repository proves

```text
- A vague AI workflow idea can be turned into a structured first-step review.
- A public demo can use synthetic examples instead of real customer data.
- Repeated workflow patterns can become reusable capability packs.
- Human review and validation can be shown before production use.
```

### What this repository does not prove

```text
- It is not a production-ready product.
- It is not a full consulting report.
- It is not a legal, privacy, cybersecurity, compliance, financial, or medical guarantee.
- It does not prove ROI, deployment readiness, or enterprise security.
```

### Data and secret boundary

This repository uses synthetic examples only. It does not require login, file upload, backend storage, production systems, API keys, real customer data, private company data, or secrets.

For the explicit checklist, see [Secret / API Key Safety Checklist](docs/secret-api-key-safety-checklist.md).

---

## Simple value statement

Most AI workflow problems do not start because the model is not smart enough. They start because the workflow boundary is unclear:

```text
What data can AI see?
Can output reach customers?
Can AI affect production systems?
Who reviews the result?
What happens when AI is wrong or uncertain?
```

WorkflowGuard AI focuses on this early boundary layer before production use.

---

## Why not just ask a chatbot?

| Asking a generic chatbot | WorkflowGuard Mini Audit Preview |
|---|---|
| One-off answer | Repeatable workflow preview |
| May jump straight to solution | Checks the risk boundary first |
| May ignore data exposure | Forces a data-boundary review |
| May skip human review | Requires review-gate thinking |
| Hard to trace why it said something | Produces reason codes and a trace note |
| May sound complete too early | Keeps the first step small and reviewable |

---

## Demo flow

```text
Vague AI adoption task
  → Task Intake
  → Safety Risk Snapshot
  → Safe First Test
  → Capability Routing
  → Demo Output
  → Human Review Gate
  → Validation Checklist
  → Trace Note
```

Example task:

> Our company wants to use AI in customer service. Which workflow should we start with, what data should we avoid, and what is the safest first step?

---

## Main files

| File | Why it matters |
|---|---|
| [docs/chinese-plain-language-overview.md](docs/chinese-plain-language-overview.md) | Fast Traditional Chinese explanation for first-time readers. |
| [web/demo-index.html](web/demo-index.html) | Static demo index and reading path. |
| [web/ai-workflow-planner.html](web/ai-workflow-planner.html) | Browser-only mini audit preview. |
| [examples/5-synthetic-workflow-scenarios.md](examples/5-synthetic-workflow-scenarios.md) | Five synthetic examples showing reusable workflow patterns. |
| [examples/mini-audit-preview-sample.md](examples/mini-audit-preview-sample.md) | Sample output from a synthetic AI workflow idea. |
| [docs/capability-pack-overview.md](docs/capability-pack-overview.md) | How repeated patterns become capability packs. |
| [docs/capability-pack-quality-gate.md](docs/capability-pack-quality-gate.md) | Quality gate for keeping capability packs reviewable. |
| [docs/secret-api-key-safety-checklist.md](docs/secret-api-key-safety-checklist.md) | Explicit checklist for API key / secret boundaries. |
| [docs/external-review-synthesis-001.md](docs/external-review-synthesis-001.md) | External review synthesis and next improvement plan. |
| [docs/github-pages-readiness-note.md](docs/github-pages-readiness-note.md) | GitHub Pages readiness and owner approval record. |
| [release/public-safe-launch-readiness-checklist.md](release/public-safe-launch-readiness-checklist.md) | Checklist before wider sharing or public demo positioning. |

---

## Mini audit preview

The mini audit preview is a static browser-only tool. It helps a reviewer turn one AI workflow idea into a public-safe preview with:

```text
risk level
safety snapshot
reason codes
workflow map preview
AI touchpoint preview
data boundary preview
human review gate
starter validation checklist
trace note
```

The tool does not require login, does not store input, does not send data to a backend, does not call an AI API, does not allow file uploads, and does not use real customer data.

---

## 5 synthetic workflow scenarios

The scenario pack shows the same pattern across five work types:

```text
FAQ grouping
Appointment notes
Daily work notes
Small-test value check
Quality gate review
```

Each scenario now includes a before state, synthetic input, safe first test, example output, human check, and capability shown.

---

## Capability language

In this repository, a **capability** means a reusable workflow ability, not a finished product feature.

Examples:

```text
FAQ Topic Capability
Appointment-Service Capability
Daily Note Capability
Small-Test Value Capability
Capability Pack Quality Gate
```

This keeps the prototype focused on repeatable workflow patterns instead of one-off prompts.

---

## Public-safe boundaries

This repository intentionally does not include:

```text
real customer data
private company data
customer lists
customer scoring
sales scripts
private outreach strategy
production runner details
API keys
secrets
private file paths
confidential business materials
unrelated production systems
```

---

## Current stage

WorkflowGuard AI is currently an early independent prototype. It is public as a repository and available as a static GitHub Pages demo, but it is not publicly launched as a finished product.

Short-term improvements:

```text
- keep reducing first-reader confusion
- improve synthetic scenario examples
- periodically check the GitHub Pages demo link
- collect trusted reviewer feedback
- decide license with owner approval
```

Long-term direction:

```text
Turn repeated workflow patterns into reusable capabilities.
```

# WorkflowGuard AI — Traceable AI Workflow Prototype

**Repository:** `traceable-ai-workflow-prototype`  
**Status:** Independent prototype / pre-company project  
**Release state:** Public-safe draft, not launched yet  
**Version:** Public-safe v0.4

WorkflowGuard AI is a public-safe prototype for traceable AI workflow evaluation before using sensitive production data.

In simple terms, this prototype helps a team decide where AI should start, what data should be avoided, and what should be checked before trying AI in a real workflow.

It demonstrates how a vague AI adoption request can be turned into a structured workflow with task intake, classification, execution planning, capability routing, validation checks, reporting, trace logs, and safety boundaries.

This repository uses synthetic examples only. It does not use real customer data, private company data, production systems, secrets, or internal business development materials.

## Chinese overview

For a Traditional Chinese plain-language introduction, see `docs/chinese-plain-language-overview.md`.

This overview is designed for Taiwanese small business owners, operations leads, non-technical reviewers, and first-time readers. It explains the concept without turning it into a sales page, pricing document, or launch announcement.

## 30-second plain-language overview

WorkflowGuard AI helps answer one early question:

```text
Before we use AI in a real workflow, where can we start safely?
```

It is not trying to be a smarter chatbot. It is a repeatable safety preview for AI workflow ideas. It checks whether the idea may touch sensitive data, customer-facing output, automatic actions, production systems, missing human review, or weak traceability.

The free preview gives a safe starting direction. It does not design the full workflow, choose tools, estimate ROI, or build the implementation roadmap.

## Why not just ask GPT?

You can ask GPT for ideas. WorkflowGuard AI is designed for a different job: making the first AI workflow step safer and more traceable.

| Asking a generic chatbot | WorkflowGuard Mini Audit Preview |
|---|---|
| One-off answer | Repeatable safety preview |
| May jump straight to solution | Checks risk boundary first |
| May skip data exposure | Forces data-boundary review |
| May ignore human review | Requires review-gate thinking |
| Hard to trace why it said something | Gives reason codes and trace preview |
| May give a full-sounding plan too early | Blocks unsafe first steps |

## Why the free preview is limited

The free preview is limited because a full AI workflow plan needs real workflow context: data access, people, tools, review owner, failure cases, customer impact, and business goal.

Those details should not be guessed from a public free form, and users should not paste real customer data into a public-safe browser preview.

```text
Free preview = safe direction.
Paid review = actual workflow design.
Paid pilot = implementation path.
```

The limitation is not only a paid wall. It is also a safety boundary.

## The problem

Many teams want to use AI, but they do not know where to start safely.

Most AI workflow problems do not start because the AI model is not smart enough. They usually start because the workflow boundary is unclear: what data AI can see, whether output can reach customers, whether AI can affect production systems, who reviews the result, and what happens when AI is uncertain or wrong.

## Safety analysis focus

WorkflowGuard AI focuses on the early safety layer before production use:

- choosing a safer first workflow
- identifying data that should be avoided
- checking whether AI output may reach customers
- checking whether AI may affect production systems
- keeping humans in the review loop
- creating validation checks and traceable decision records

This is a public-safe workflow safety preview. It is not a legal, privacy, cybersecurity, compliance, financial, medical, or professional guarantee.

## Demo flow

```text
Vague AI adoption task
  → Task Intake
  → Task Classification
  → Safety Risk Snapshot
  → Execution Plan
  → Capability Routing
  → Demo Execution
  → Validation
  → Report
  → Trace Log
```

Example task:

> Our company wants to use AI in customer service. Which workflow should we start with, what data should we avoid, and what is the safest first step?

## Package index

For a single map of the public-safe package, use `release/public-safe-package-index.md`.

The index explains the recommended reading path, core package files, reviewer flow files, launch and safety files, supporting examples, what the package currently proves, and what it does not prove yet.

## Quick reviewer path

For a 3 to 5 minute review, start with `demo/reviewer-walkthrough.md`.

The walkthrough guides a reviewer through the README, sample output, browser-only mini audit tool, synthetic test case, free / paid boundary, public-safe boundary, and suggested feedback questions.

## Mini audit preview

A first static browser-only tool is available at `web/ai-workflow-planner.html`.

The tool is positioned as a **WorkflowGuard Mini Audit Preview**, not a full consulting report. It helps a user turn one AI workflow idea into a public-safe preview with an initial Green / Yellow / Red risk level, safety risk snapshot, reason codes, workflow map preview, AI touchpoint preview, data boundary preview, human review gate preview, starter validation checklist, trace log preview, and a public-safe next step.

The free preview is intentionally limited. It shows the method and direction, but it does not include full safety control design, full workflow redesign, implementation planning, ROI analysis, tool selection, production integration, client-specific risk review, or a paid pilot roadmap.

The tool does not require login, does not store user input, does not send data to a backend, does not call an AI API, does not allow file uploads, and does not use real customer data.

## What happens after the preview

A public-safe deliverable preview is available at `docs/public-safe-review-deliverable-preview.md`.

It explains what a public-safe workflow review may produce after the free mini audit preview, such as a workflow idea summary, manual workflow sketch, AI touchpoint candidates, data boundary notes, human review gate notes, blocked first-step list, starter validation checklist, safe first experiment, questions before paid pilot, and recommended next decision.

A synthetic example review note is available at `examples/public-safe-review-note-sample.md`.

This remains high-level and does not include pricing, sales scripts, customer scoring, payability qualification, production architecture, or full implementation methodology.

## Free user objection response

Common skeptical questions from free users are handled by `docs/free-user-objection-response-department.md`.

This public-safe department answers questions such as why the free preview is limited, why it is different from asking GPT, why real customer data should not be pasted, what is free, what remains locked, and why this is not a safety guarantee.

## Sample output

A public-safe sample output is available at `examples/mini-audit-preview-sample.md`.

The sample shows how one synthetic customer-service AI idea becomes a mini audit preview with safety risk snapshot, reason codes, workflow map preview, AI touchpoint preview, data boundary preview, validation checklist, locked advanced sections, and trace log preview.

## Launch readiness

Before enabling GitHub Pages, changing repository visibility, sharing with wider reviewers, or presenting this as a controlled public-safe demo, use `release/public-safe-launch-readiness-checklist.md`.

The checklist verifies product maturity wording, legal/privacy/cybersecurity/compliance disclaimers, data safety, technical boundaries, internal strategy exposure, private system exposure, free / paid boundary, and reviewer flow readiness.

## Reviewer feedback

For controlled trusted-reviewer preview, use `release/controlled-reviewer-outreach-message.md` to invite reviewers without turning the request into a sales message or public launch announcement.

Then use `release/trusted-reviewer-feedback-form.md` after the reviewer has followed `demo/reviewer-walkthrough.md`.

After collecting 3 to 5 reviewer responses, use `release/reviewer-feedback-summary-template.md` to create an anonymized public-safe summary and convert feedback into the next patch decision.

The feedback form focuses on problem clarity, safety-analysis positioning, difference from a generic chatbot, free / paid boundary, trust, business usefulness, next-step clarity, overclaim risk, and public-safe boundary checks.

## Architecture

See `docs/architecture.md` and `assets/workflowguard_architecture.svg`.

## Public-safe examples

See the `examples/` folder for sample task intake, execution plan, validation checklist, report, trace log, mini audit preview sample output, and public-safe review note sample.

## What this is not

This prototype is not a finished AI operating system, mature commercial SaaS product, production automation system, legal/privacy/cybersecurity/compliance guarantee, replacement for professional review, or repository for internal customer discovery strategy.

## Public-safe boundaries

This repository intentionally does not include real customer data, internal customer lists, customer scoring, sales scripts, private outreach strategy, production runner details, API keys, secrets, private file paths, confidential business materials, or unrelated production systems.

## Current stage

WorkflowGuard AI is currently an early independent prototype. It is not publicly launched yet.

## Roadmap

Short term: improve the mini audit preview, add demo video, collect feedback from 3–5 reviewers, and refine public-safe wording.  
Medium term: create controlled pilot templates, improve validation rules, and add optional UI mockup.  
Long term: turn repeated workflow patterns into reusable capabilities.

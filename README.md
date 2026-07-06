# WorkflowGuard AI — Traceable AI Workflow Prototype

**Repository:** `traceable-ai-workflow-prototype`  
**Status:** Independent prototype / pre-company project  
**Release state:** Public-safe draft, not launched yet  
**Version:** Public-safe v0.3

WorkflowGuard AI is a public-safe prototype for traceable AI workflow evaluation before using sensitive production data.

In simple terms, this prototype helps a team decide where AI should start, what data should be avoided, and what should be checked before trying AI in a real workflow.

It demonstrates how a vague AI adoption request can be turned into a structured workflow with task intake, classification, execution planning, capability routing, validation checks, reporting, trace logs, and safety boundaries.

This repository uses synthetic examples only. It does not use real customer data, private company data, production systems, secrets, or internal business development materials.

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

## Quick reviewer path

For a 3 to 5 minute review, start with `demo/reviewer-walkthrough.md`.

The walkthrough guides a reviewer through the README, sample output, browser-only mini audit tool, synthetic test case, free / paid boundary, public-safe boundary, and suggested feedback questions.

## Mini audit preview

A first static browser-only tool is available at `web/ai-workflow-planner.html`.

The tool is positioned as a **WorkflowGuard Mini Audit Preview**, not a full consulting report. It helps a user turn one AI workflow idea into a public-safe preview with an initial Green / Yellow / Red risk level, safety risk snapshot, reason codes, workflow map preview, AI touchpoint preview, data boundary preview, human review gate preview, starter validation checklist, trace log preview, and a public-safe next step.

The free preview is intentionally limited. It shows the method and direction, but it does not include full safety control design, full workflow redesign, implementation planning, ROI analysis, tool selection, production integration, client-specific risk review, or a paid pilot roadmap.

The tool does not require login, does not store user input, does not send data to a backend, does not call an AI API, does not allow file uploads, and does not use real customer data.

## Sample output

A public-safe sample output is available at `examples/mini-audit-preview-sample.md`.

The sample shows how one synthetic customer-service AI idea becomes a mini audit preview with safety risk snapshot, reason codes, workflow map preview, AI touchpoint preview, data boundary preview, validation checklist, locked advanced sections, and trace log preview.

## Architecture

See `docs/architecture.md` and `assets/workflowguard_architecture.svg`.

## Public-safe examples

See the `examples/` folder for sample task intake, execution plan, validation checklist, report, trace log, and mini audit preview sample output.

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

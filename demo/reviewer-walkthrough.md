# WorkflowGuard AI — Reviewer Walkthrough

**Status:** Public-safe reviewer guide  
**Estimated review time:** 3 to 5 minutes  
**Audience:** trusted reviewer, potential collaborator, competition reviewer, technical reviewer, or early business reviewer  
**Data requirement:** synthetic examples only

This walkthrough explains how to review the repository quickly without using real customer data, private company data, secrets, production systems, or internal customer discovery materials.

---

## What this reviewer should understand

After a short review, the reviewer should understand that WorkflowGuard AI is not trying to be a generic chatbot. It is a public-safe prototype for evaluating AI workflow ideas before production use.

The key idea is:

```text
Before using AI in a real workflow, first check the workflow boundary:
what data AI may see, whether output may reach customers, whether AI may affect production systems,
who reviews the result, what should be blocked, and how the decision is traceable.
```

---

## 1. Start with the README

Open:

```text
README.md
```

Look for these points:

- the project is an independent prototype / pre-company project
- it uses synthetic examples only
- it does not use real customer data, secrets, production systems, or private business development materials
- the core focus is AI workflow safety analysis before production use
- the free preview is intentionally limited and is not a full consulting report

The reviewer should be able to answer:

```text
What problem is this prototype trying to solve?
Why does safety analysis matter before using AI in production workflows?
What is intentionally not included?
```

---

## 2. Review the sample output first

Open:

```text
examples/mini-audit-preview-sample.md
```

This file shows a synthetic customer-service example and the mini audit preview output.

Focus on these sections:

- initial Green / Yellow / Red risk level
- Safety Risk Snapshot
- reason codes
- workflow map preview
- AI touchpoint preview
- data boundary preview
- human review gate preview
- starter validation checklist
- locked advanced sections
- trace log preview

The reviewer should notice that the output is not just a short answer. It is a structured preview that shows how a vague AI idea can be turned into a safer first experiment.

---

## 3. Open the static browser tool

Open the local file or GitHub Pages version when available:

```text
web/ai-workflow-planner.html
```

The tool should run in the browser only.

Expected boundaries:

```text
No login
No backend
No storage
No API call
No file upload
No real customer data
```

Use one synthetic workflow idea only. Do not paste real company or customer information.

---

## 4. Try one synthetic test case

Suggested test input:

```text
We want AI to help our support team summarize repeated customer questions and create reply drafts, but a human should approve before sending.
```

Suggested selections:

```text
Workflow type: Customer service
Main AI use: Create a draft for a human to review
Output audience: Human review before external use
Data boundaries: Customer records or customer conversations; Personal data
Human review: A human reviews before any real use
```

Expected result:

```text
Risk level: Yellow
Reason: possible customer/personal data and external use after review
Safe first role: internal draft or summary only
Blocked first role: direct customer reply or automatic execution
Recommended experiment: fake or anonymized examples with human review
```

---

## 5. Check the free / paid boundary

The free preview should show enough value to prove the method, but it should not provide a complete implementation plan.

Unlocked in the free preview:

- initial risk level
- Safety Risk Snapshot
- reason codes
- workflow map preview
- AI touchpoint preview
- data boundary preview
- human review gate preview
- starter validation checklist
- trace log preview

Locked for review / paid pilot:

- full safety control design
- full workflow redesign
- client-specific data policy
- production integration architecture
- tool selection or vendor comparison
- ROI and cost estimation
- paid pilot roadmap
- stakeholder decision map
- internal customer discovery or payability scoring

The reviewer should understand that the free tool is a preview, not the final deliverable.

---

## 6. Check the public-safe boundary

This repository should not expose:

- real customer data
- internal customer lists
- customer scoring
- sales scripts
- outreach strategy
- production runner details
- API keys or secrets
- private file paths
- confidential business materials
- unrelated production systems

This repository also intentionally does not include internal lead scoring, internal payability qualification logic, Hermes_sport, WorldCup_AI, production bridge/runner details, or private operating-system internals.

---

## 7. Suggested reviewer feedback

Useful reviewer feedback should focus on:

```text
Is the problem clear?
Is the safety-analysis positioning understandable?
Does the sample output feel different from a generic chatbot answer?
Are the locked paid sections clear enough?
Is the public-safe boundary credible?
Would a non-technical business owner understand what to do next?
```

Less useful feedback:

```text
Add real customer data
Connect to a CRM immediately
Make it auto-send emails
Add login and lead capture first
Expose the internal sales or scoring logic
Turn it into a full SaaS before validating the concept
```

---

## 8. What success looks like

A successful 3 to 5 minute review should leave the reviewer with this understanding:

```text
WorkflowGuard AI helps a team evaluate where AI should start safely,
what data should be avoided,
what should stay human-reviewed,
what should be blocked from automation,
and how the decision can be traced before production use.
```

The reviewer does not need to understand every internal capability or implementation detail. The public-safe package should communicate the direction, method, safety boundary, and next step without exposing internal strategy.

---

## Public-safe note

Use only synthetic examples when reviewing this prototype. Do not paste real customer records, private company data, production credentials, confidential documents, internal sales strategy, customer scoring, or unrelated production-system details.

# Public-Safe Launch Readiness Checklist

**Status:** Public-safe release checklist  
**Scope:** trusted reviewer sharing, GitHub Pages preview, competition preview, or controlled public-safe demo  
**Current release state:** draft / not publicly launched  
**Data requirement:** synthetic examples only

This checklist is used before sharing WorkflowGuard AI outside the private working context. It is designed to reduce three launch risks:

```text
1. Someone thinks this is a finished product.
2. Someone thinks this is legal, privacy, cybersecurity, or compliance assurance.
3. Internal strategy, customer discovery logic, private systems, or unrelated production projects are exposed.
```

---

## 1. Repository visibility gate

Before changing repository visibility or sharing links:

- [ ] Repository is still private unless explicitly approved for public release.
- [ ] GitHub Pages is not enabled unless explicitly approved.
- [ ] No public social post or announcement has been made.
- [ ] Reviewer access is limited to trusted reviewers or controlled preview users.
- [ ] The repo is not presented as a finished SaaS product.

Decision:

```text
PASS only if sharing remains controlled, or public release has been explicitly approved.
```

---

## 2. Product maturity wording gate

Check public-facing wording in:

```text
README.md
web/ai-workflow-planner.html
demo/reviewer-walkthrough.md
examples/mini-audit-preview-sample.md
release/*
```

Required wording:

- [ ] It says this is an independent prototype / pre-company project.
- [ ] It says the release state is draft / not publicly launched yet where relevant.
- [ ] It says this is a mini audit preview, not a full consulting report.
- [ ] It says the free preview is intentionally limited.
- [ ] It does not claim to be a mature commercial SaaS product.
- [ ] It does not claim to be a complete AI operating system.
- [ ] It does not imply production readiness.

Blocked wording:

- [ ] No claim that the product is complete.
- [ ] No claim that it is enterprise-ready.
- [ ] No claim that it is safe for production use.
- [ ] No claim that it replaces professional review.

Decision:

```text
PASS only if the public-facing package clearly says prototype / preview / not production-ready.
```

---

## 3. Legal / privacy / cybersecurity / compliance wording gate

Required disclaimers:

- [ ] The project does not provide legal advice.
- [ ] The project does not provide privacy advice.
- [ ] The project does not provide cybersecurity assurance.
- [ ] The project does not provide compliance assurance.
- [ ] The project does not provide financial, medical, or professional advice.
- [ ] The project does not guarantee safety.
- [ ] The project is a public-safe workflow safety preview only.

Blocked wording:

- [ ] No claim of legal compliance.
- [ ] No claim of privacy compliance.
- [ ] No claim of cybersecurity certification.
- [ ] No claim of formal risk certification.
- [ ] No claim that a workflow is guaranteed safe.

Decision:

```text
PASS only if the wording remains safety-preview focused, not assurance/certification focused.
```

---

## 4. Data safety gate

The public-safe package must not include:

- [ ] real customer data
- [ ] private company data
- [ ] production data
- [ ] personal data from real people
- [ ] customer conversations from real systems
- [ ] support tickets from real systems
- [ ] CRM exports
- [ ] payment, billing, order, or transaction records
- [ ] private files or documents
- [ ] secrets, tokens, API keys, passwords, or credentials
- [ ] private file paths

Required:

- [ ] All examples are synthetic.
- [ ] All sample workflows are public-safe.
- [ ] The tool warns users not to paste real customer or private data.
- [ ] The sample output states it uses synthetic examples only.

Decision:

```text
PASS only if no real or sensitive data is present.
```

---

## 5. Technical boundary gate

The first public-safe tool should remain static and browser-only.

Required:

- [ ] No login.
- [ ] No backend.
- [ ] No database.
- [ ] No file upload.
- [ ] No AI API call.
- [ ] No CRM / Gmail / Drive / Slack / database connection.
- [ ] No analytics or tracking unless explicitly approved later.
- [ ] No collection of email or lead forms in this version.
- [ ] No automatic email sending.
- [ ] No production system write access.

Search terms to check before launch:

```text
fetch
XMLHttpRequest
sendBeacon
localStorage
sessionStorage
indexedDB
apiKey
secret
token
password
openai
crm
gmail
drive
slack
```

Decision:

```text
PASS only if the tool remains static, local, and non-collecting.
```

---

## 6. Internal strategy exposure gate

The repository must not include internal business-development or customer-discovery materials.

Do not expose:

- [ ] internal customer lists
- [ ] target company lists
- [ ] customer scoring
- [ ] payability qualification formulas
- [ ] sales scripts
- [ ] outreach strategy
- [ ] pricing strategy
- [ ] negotiation notes
- [ ] private reviewer names
- [ ] private partner names
- [ ] internal lead pipeline
- [ ] internal business prioritization logic

Allowed:

- [ ] high-level public-safe positioning
- [ ] generic free / paid boundary
- [ ] public-safe reviewer guide
- [ ] synthetic examples only

Decision:

```text
PASS only if the repo shows the public-safe method without exposing internal go-to-market logic.
```

---

## 7. Internal system exposure gate

The repository must not expose private operating-system internals or unrelated production systems.

Do not expose:

- [ ] production bridge or runner details
- [ ] internal automation runner implementation
- [ ] private Capability Operating System internals
- [ ] internal AI Dispatch operating rules beyond public-safe positioning
- [ ] Hermes_sport
- [ ] WorldCup_AI
- [ ] private local paths
- [ ] database schema from private projects
- [ ] API usage ledgers from private projects
- [ ] model provider credentials or routing rules

Allowed:

- [ ] public-safe architecture overview
- [ ] synthetic trace log example
- [ ] generic capability-oriented wording
- [ ] high-level validation-first positioning

Decision:

```text
PASS only if the public package does not reveal private system mechanics.
```

---

## 8. Free / paid boundary gate

The free preview should demonstrate the method without giving away a full implementation plan.

Free preview may include:

- [ ] initial risk level
- [ ] Safety Risk Snapshot
- [ ] reason codes
- [ ] workflow map preview
- [ ] AI touchpoint preview
- [ ] data boundary preview
- [ ] human review gate preview
- [ ] first safe experiment
- [ ] starter validation checklist
- [ ] trace log preview

Free preview should not include:

- [ ] full safety control design
- [ ] full workflow redesign
- [ ] detailed client-specific data policy
- [ ] production integration architecture
- [ ] tool selection or vendor comparison
- [ ] ROI and cost estimation
- [ ] paid pilot roadmap
- [ ] stakeholder decision map
- [ ] internal customer discovery or payability scoring

Decision:

```text
PASS only if the tool proves value but keeps the full solution behind review / pilot.
```

---

## 9. Reviewer flow gate

Before sharing with a reviewer:

- [ ] README has a quick reviewer path.
- [ ] `demo/reviewer-walkthrough.md` exists.
- [ ] `examples/mini-audit-preview-sample.md` exists.
- [ ] The static tool path is clear: `web/ai-workflow-planner.html`.
- [ ] The reviewer guide says to use synthetic examples only.
- [ ] The reviewer guide asks for useful feedback, not premature SaaS expansion.
- [ ] The reviewer can understand the project in 3 to 5 minutes.

Decision:

```text
PASS only if a reviewer can understand what to inspect without asking for internal context.
```

---

## 10. Launch readiness decision

Use this decision table:

| Result | Meaning | Action |
|---|---|---|
| PASS | Safe for controlled trusted-reviewer sharing | Share with selected reviewers only |
| PASS WITH NOTES | Minor wording or clarity issues remain | Fix notes before wider sharing |
| BLOCKED | Sensitive data, misleading claims, or internal strategy exposure found | Do not share until fixed |

Recommended current default:

```text
PASS for private trusted-reviewer preview only.
BLOCKED for full public launch until explicitly approved.
```

---

## Current recommended status

```text
Release state: Public-safe draft
GitHub visibility: private
GitHub Pages: not enabled unless explicitly approved
Recommended sharing: controlled trusted reviewers only
Recommended next action: collect 3 to 5 reviewer feedback notes using synthetic examples
```

---

## Final pre-share checklist

Before sending the repo or demo link to anyone:

- [ ] I know who the reviewer is.
- [ ] I know why they are reviewing it.
- [ ] I will tell them to use synthetic examples only.
- [ ] I will not ask them to upload files.
- [ ] I will not ask them to paste customer data.
- [ ] I will not describe it as a finished product.
- [ ] I will not describe it as legal, privacy, cybersecurity, or compliance assurance.
- [ ] I will ask for feedback on clarity, safety positioning, free / paid boundary, and whether it feels different from a generic chatbot.

---

## Public-safe note

This checklist is itself public-safe. It does not include internal customer discovery logic, customer scoring, sales scripts, production runner details, Hermes_sport, WorldCup_AI, secrets, credentials, or private system paths.

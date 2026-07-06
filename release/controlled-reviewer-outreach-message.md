# Controlled Reviewer Outreach Message

**Status:** Public-safe outreach template  
**Use case:** invite 3 to 5 trusted reviewers to review the prototype  
**Audience:** trusted reviewer, collaborator, technical reviewer, business reviewer, or competition/program reviewer  
**Data requirement:** synthetic examples only

This is not a sales script. It is a controlled reviewer invitation message for collecting feedback on a public-safe prototype.

Do not use this message for mass outreach, cold sales, public launch, social media announcement, or lead generation without a separate public-safe launch review.

---

## When to use this message

Use this message only when:

- [ ] The reviewer is known and trusted.
- [ ] The reviewer understands this is a prototype preview.
- [ ] The reviewer will not paste real customer data or private company data.
- [ ] The goal is feedback, not selling.
- [ ] The repo remains private unless public release is explicitly approved.
- [ ] You are collecting 3 to 5 controlled feedback responses.

Do not use it when:

- [ ] You are announcing a public launch.
- [ ] You are selling a paid service directly.
- [ ] You want to collect leads at scale.
- [ ] You want reviewers to test with real customer data.
- [ ] You have not checked the public-safe launch readiness checklist.

---

## Short message

```text
Hi [Name], I’m building a small public-safe prototype called WorkflowGuard AI.

It is not a chatbot and not a finished product. The idea is to help teams check an AI workflow idea before production use: what data AI may touch, whether output may reach customers, what should stay human-reviewed, what should be blocked from automation, and how the decision can be traced.

Could you spend 3 to 5 minutes reviewing it with synthetic examples only? Please do not use real customer data or private company information.

What I want feedback on:
- Is the problem clear?
- Does the safety-analysis positioning make sense?
- Does it feel different from simply asking a generic chatbot?
- Is the free / paid boundary clear?
- Does anything sound overclaimed or risky?

Suggested review path:
1. README
2. Reviewer walkthrough
3. Sample output
4. Static browser-only mini audit tool
5. Feedback form

Thank you — short, honest feedback is enough.
```

---

## Slightly more detailed message

```text
Hi [Name], I’d like to ask for a short trusted-reviewer check on a prototype I’m building.

The project is called WorkflowGuard AI. It is a public-safe prototype for reviewing AI workflow ideas before production use. The main idea is that many AI adoption problems are not caused by the model being unintelligent, but by unclear workflow boundaries: what data AI may see, whether output may reach customers, whether AI may affect production systems, who reviews the result, and what should happen when AI is uncertain or wrong.

This is not a finished product, not a SaaS launch, and not legal/privacy/cybersecurity/compliance advice. It is only a safety-analysis preview.

Please review it with synthetic examples only. Do not paste real customer data, private company data, production credentials, confidential documents, or internal business information.

The review should take about 3 to 5 minutes. I’m mainly trying to learn:

1. Is the problem easy to understand?
2. Is the safety-analysis positioning clear?
3. Does the sample output feel different from a generic chatbot answer?
4. Does the tool show enough value without giving away the full implementation plan?
5. Is the free / paid boundary clear?
6. Does anything sound like an overclaim?
7. Would a non-technical business owner understand what to do next?

Suggested review path:

- Start with `README.md`
- Follow `demo/reviewer-walkthrough.md`
- Review `examples/mini-audit-preview-sample.md`
- Try `web/ai-workflow-planner.html` with one synthetic workflow idea
- Fill out `release/trusted-reviewer-feedback-form.md`

Short feedback is fine. I’m looking for clarity, trust, and positioning feedback — not private customer examples.
```

---

## Very short chat version

```text
Can I ask you to spend 3 to 5 minutes reviewing a small AI workflow safety prototype?

It is called WorkflowGuard AI. It helps check an AI workflow idea before production use: data boundary, customer-facing output, automation risk, human review, and traceability.

Please use synthetic examples only — no real customer or company data.

I mainly want to know:
- Is it clear?
- Does it feel different from asking GPT?
- Is the safety angle useful?
- Does anything sound overclaimed?
- Is the free / paid boundary clear?
```

---

## Message for a technical reviewer

```text
Hi [Name], I’m looking for a quick technical/product sanity check on a static prototype called WorkflowGuard AI.

The first version is intentionally simple: browser-only HTML, no login, no backend, no storage, no API calls, and synthetic examples only.

The goal is not model intelligence. The goal is workflow safety analysis before production use: data boundary, external output risk, automation risk, production system risk, human review gap, validation checks, and trace log preview.

Could you review whether the repo communicates this clearly and whether the public-safe boundary looks credible?

Please do not test with real customer data, private company data, credentials, or production system details.

I’m especially interested in:
- Does the output feel meaningfully structured, or still too much like a chatbot answer?
- Is the safety risk snapshot useful?
- Are the locked paid sections clear?
- Are there any overclaim or public-safe risks?
- Does the static/no-backend approach feel trustworthy for a first demo?
```

---

## Message for a business reviewer

```text
Hi [Name], I’m testing a small prototype called WorkflowGuard AI and would value your business perspective.

It is for teams that want to use AI but are not sure where to start safely. Instead of jumping straight into automation, it helps preview the risk boundary: what data AI might touch, whether the result may reach customers, whether a human should review it, and what should not be automated first.

It is not a finished product and not legal/privacy/cybersecurity advice. Please review it using fake examples only, not real customer or company data.

I’d love your honest feedback on:
- Is the problem understandable?
- Would this be useful before a company starts using AI in a workflow?
- Does it feel different from asking a chatbot?
- Is it clear what the free preview gives and what should require a paid review or pilot?
- What would make it more credible to a business owner?
```

---

## What not to say

Avoid wording like:

```text
We launched a finished AI safety product.
This guarantees your workflow is safe.
This provides legal, privacy, cybersecurity, or compliance assurance.
Paste your real customer data to test it.
Connect your CRM or email to try it.
This is enterprise-ready.
This is a complete AI operating system.
```

---

## Reviewer instruction block

Add this block when sending the prototype:

```text
Important review boundary:
Please use synthetic examples only. Do not paste real customer data, private company data, production credentials, confidential documents, internal sales strategy, customer scoring, or unrelated production-system details.

This is a prototype preview, not a finished product or professional assurance.
```

---

## Follow-up after receiving feedback

```text
Thank you for reviewing it. I’ll anonymize your feedback and summarize it into product-improvement themes only. I will not store private names, company details, customer situations, or sensitive business context in the public-safe repo.
```

---

## Internal handling note

After collecting feedback, use:

```text
release/reviewer-feedback-summary-template.md
```

to summarize responses into anonymized product feedback and next patch decisions.

Do not paste raw private feedback into the public-safe repository.

---

## Public-safe note

This outreach template is public-safe. It does not include internal customer discovery logic, customer scoring, sales scripts, production runner details, Hermes_sport, WorldCup_AI, secrets, credentials, or private system paths.

# WorkflowGuard Mini Audit Preview — Sample Output

**Status:** Public-safe sample  
**Version:** v0.4 sample  
**Data type:** Synthetic example only  
**Purpose:** Show what the free mini audit preview can produce without using real customer data.

This sample is intentionally limited. It demonstrates the preview structure and safety-preview style, but it is not a full consulting report, implementation plan, legal review, cybersecurity review, privacy review, compliance guarantee, or production integration plan.

A short visual summary card example is available at `examples/mini-audit-visual-summary-card.md`.

---

## 30-second plain-language overview

WorkflowGuard AI helps answer one early question:

```text
Before we use AI in a real workflow, where can we start safely?
```

It is not trying to be a smarter chatbot. It is a repeatable safety preview for AI workflow ideas. It checks whether the idea may touch sensitive data, customer-facing output, automatic actions, production systems, missing human review, or weak traceability.

The free preview gives a safe starting direction. It does not design the full workflow, choose tools, estimate ROI, or build the implementation roadmap.

---

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

---

## Why this preview is limited

The free preview is limited because a full AI workflow plan needs real workflow context: data access, people, tools, review owner, failure cases, customer impact, and business goal.

Those details should not be guessed from a public free form, and users should not paste real customer data into a public-safe browser preview.

```text
Free preview = safe direction.
Paid review = actual workflow design.
Paid pilot = implementation path.
```

The limitation is not only a paid wall. It is also a safety boundary.

---

## Sample input

**Workflow idea**

> We want AI to help our support team turn repeated customer questions into draft replies, but a human should approve before sending.

**Selected workflow type**

```text
Customer service
```

**Selected AI use**

```text
Create a draft for a human to review
```

**Selected output audience**

```text
Human review before external use
```

**Selected data and system boundary checks**

```text
Customer messages or customer records
Personal data
```

**Human review setting**

```text
Yes, every AI output is reviewed by a human
```

---

## Sample generated preview

```text
WorkflowGuard Mini Audit Preview
Public-safe preview generated in browser · Not a full consulting report

0. What this preview is for

This preview helps decide where an AI workflow idea can start safely before using sensitive production data.

It is a triage preview, not a full workflow design.

1. Original AI idea

We want AI to help our support team turn repeated customer questions into draft replies, but a human should approve before sending.

2. Initial risk level

Yellow — Needs human review and clearer boundary before use.

3. Safety risk snapshot

- Data exposure risk: High — Customer or personal data may be involved. Use synthetic or anonymized examples first.
- External output risk: Medium — Output may eventually affect customer-facing communication. Keep AI output internal until approved.
- Automation risk: Low — AI is drafting for human review, not executing automatically.
- Production system risk: Low — No production system access should be used in the first experiment.
- Human review gap: Low — Human review is required.
- Traceability gap: Medium — Keep a simple record of why the workflow was classified this way.

4. Why this is not just a generic chatbot answer

This preview checks risk boundary before giving a solution. It looks at data exposure, output audience, automation, production-system involvement, human review, and traceability.

5. Reason codes

- draft_requires_review
- external_use_after_review
- customer_data_possible
- personal_data_possible

6. Why this was classified this way

This idea can be a reasonable first AI workflow, but it may touch customer messages and personal data. It should not start with real customer records or direct customer output.

7. Workflow map preview

Intake customer question → AI groups repeated themes and drafts internal reply suggestion → Human checks accuracy, tone, and missing context → Approved response may be used by staff.

8. AI touchpoint preview

AI should help with internal draft suggestions only. It should not directly send a reply or update customer records.

9. Data boundary preview

Start with synthetic or anonymized examples. Do not paste real customer names, emails, phone numbers, addresses, order numbers, payment details, or private conversations into the preview.

10. Human review gate preview

Every AI draft should be reviewed by a human before it is used externally. The human reviewer should check correctness, tone, privacy exposure, and whether escalation is needed.

11. First safe experiment

Use 10 fake or anonymized customer questions. Ask AI to group repeated question types and draft internal reply suggestions. A human records what needed correction.

12. Starter validation checklist preview

[ ] Synthetic or anonymized examples only
[ ] AI output stays internal
[ ] Human reviews every draft
[ ] Reviewer can reject unsafe or uncertain output
[ ] Corrections are recorded

13. Why this preview is limited

A full workflow plan would need real workflow context, allowed data, reviewer ownership, tools, failure cases, customer impact, and business goals.

This public-safe preview intentionally avoids guessing those details.

14. Locked advanced sections

- Full workflow redesign
- Client-specific data policy
- Production integration design
- Tool selection
- ROI or cost estimate
- Paid pilot roadmap

15. Suggested next step

Run a public-safe experiment with synthetic or anonymized examples. Do not connect this to CRM, email, ticketing, database, or customer-facing output yet.

16. Trace log preview

{
  "preview_type": "mini_audit_preview_v0_4",
  "risk_level": "Yellow",
  "risk_score_band": "5_to_9",
  "recommended_start": "internal_human_reviewed_experiment",
  "blocked_start": [
    "direct_external_output",
    "production_write_access",
    "sensitive_data_processing",
    "automatic_execution"
  ]
}
```

---

## Public-safe note

This sample does not include real customer data, private company data, production credentials, pricing, sales scripts, internal customer scoring, payability qualification, production runner details, Hermes_sport internals, WorldCup_AI internals, secrets, credentials, or private system paths.

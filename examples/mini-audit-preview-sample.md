# WorkflowGuard Mini Audit Preview — Sample Output

**Status:** Public-safe sample  
**Version:** v0.3 sample  
**Data type:** Synthetic example only  
**Purpose:** Show what the free mini audit preview can produce without using real customer data.

This sample is intentionally limited. It demonstrates the preview structure and safety-analysis style, but it is not a full consulting report, implementation plan, legal review, cybersecurity review, privacy review, compliance guarantee, or production integration plan.

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

**Selected data / system boundaries**

```text
- Customer records or customer conversations
- Personal data such as names, phones, emails, IDs, or addresses
```

**Selected human review**

```text
A human reviews before any real use
```

---

## Sample generated preview

```text
WorkflowGuard Mini Audit Preview
Public-safe safety analysis preview generated in browser · Not a full consulting report

1. Original AI idea
We want AI to help our support team turn repeated customer questions into draft replies, but a human should approve before sending.

2. Initial risk level
Yellow: can start, but not with direct automation

3. Safety risk snapshot
- Data exposure risk: High — Sensitive data may be involved. Use synthetic examples only in the first version.
- External output risk: Medium — External use may be possible only after human review.
- Automation risk: Low — Drafting or organizing is safer than automatic execution.
- Production system risk: Low — No production system boundary was selected. Keep it disconnected first.
- Human review gap: Low — Human review is planned before real use.
- Traceability gap: Medium — The free preview includes a trace log preview, but a real pilot needs stronger decision logs and validation records.

4. Reason codes
- draft_requires_review
- external_use_after_review
- customer_data_possible
- personal_data_possible

5. Why this was classified this way
- AI would create drafts, so human review should stay in the loop.
- AI output may be used externally after review.
- The workflow may touch sensitive data or systems, so the first version should use synthetic or anonymized examples only.

6. Workflow map preview
1. User or customer request arrives
2. Human identifies the request type
3. AI assists with a narrow internal step
4. Human reviews AI output
5. Reviewed output may be used externally

7. AI touchpoint preview
Safe first AI role: Use AI to create internal drafts that a human reviews before any real use.
Blocked first AI role: Do not let AI directly send the draft or decide whether the draft is correct.

8. Data boundary preview
Selected boundary: customer records or customer conversations; personal data such as names, phones, emails, IDs, or addresses
Avoid for now:
- customer names, phone numbers, emails, addresses, IDs, or full conversations
- order numbers, billing records, payment details, refunds, or transaction history
- API keys, passwords, tokens, private file paths, and production credentials
- confidential strategy, HR, legal, finance, or security documents

9. Human review gate preview
A human must check accuracy, tone, missing context, privacy exposure, and whether the output should be rejected.

10. First safe experiment
Use 10 fake or anonymized examples and record what a human had to correct.

11. Starter validation checklist preview
[ ] Is the output based only on public-safe or synthetic examples?
[ ] Can a human quickly verify the output before use?
[ ] Does the output avoid personal data, secrets, and production credentials?
[ ] Is there a clear rule for rejecting unsafe or uncertain output?
[ ] Is external use blocked until a human approves the final version?
[ ] Is the first experiment limited to draft-only, summary-only, or checklist-only use?

12. Locked advanced sections
These are intentionally not included in the free preview:
- Full safety control design and review workflow
- Full workflow redesign and step-by-step operating procedure
- Detailed AI touchpoint design and capability routing
- Production data policy and integration plan
- Tool selection, build-vs-buy comparison, and implementation architecture
- ROI, cost, effort, timeline, and paid pilot roadmap
- Client-specific risk review and stakeholder decision map

13. Suggested next step
Use a 20-minute public-safe workflow review to turn this preview into a more specific workflow map and paid pilot decision. Do not use real customer data for the review.

14. Trace log preview
{
  "preview_type": "mini_audit_preview_v0_3",
  "risk_level": "Yellow",
  "risk_score_band": "5_to_9",
  "reason_codes": [
    "draft_requires_review",
    "external_use_after_review",
    "customer_data_possible",
    "personal_data_possible"
  ],
  "safety_snapshot": [
    {
      "risk": "Data exposure risk",
      "level": "High"
    },
    {
      "risk": "External output risk",
      "level": "Medium"
    },
    {
      "risk": "Automation risk",
      "level": "Low"
    },
    {
      "risk": "Production system risk",
      "level": "Low"
    },
    {
      "risk": "Human review gap",
      "level": "Low"
    },
    {
      "risk": "Traceability gap",
      "level": "Medium"
    }
  ],
  "recommended_start": "internal_human_reviewed_experiment",
  "blocked_start": [
    "direct_external_output",
    "production_write_access",
    "sensitive_data_processing",
    "automatic_execution"
  ]
}

Disclaimer
This is a limited rule-based safety analysis preview. It is not legal, privacy, cybersecurity, compliance, financial, medical, or professional advice. It does not include full safety control design, full workflow redesign, implementation planning, ROI analysis, tool selection, production integration, or a formal consulting report.
```

---

## What this sample is meant to show

This sample shows the value of the free preview:

- It does not only return a short answer.
- It turns one vague AI idea into a structured safety-analysis preview.
- It identifies data exposure, external output, automation, production system, human review, and traceability risks.
- It shows what should be blocked in the first version.
- It gives a safe first experiment without giving away a complete consulting plan.

---

## What remains locked for a paid review or pilot

The free preview does not include:

- full safety control design
- detailed workflow redesign
- client-specific data policy
- production integration architecture
- tool selection or vendor comparison
- ROI and cost estimation
- paid pilot roadmap
- stakeholder decision map
- internal customer discovery or payability scoring

---

## Public-safe note

This file uses a synthetic customer-service example only. It does not include real customer records, private company data, secrets, production credentials, internal sales strategy, customer scoring, or unrelated production systems.

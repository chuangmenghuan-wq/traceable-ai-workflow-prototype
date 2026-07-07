# 5 Synthetic Workflow Scenarios

**Status:** Public-safe synthetic examples  
**Task ID:** REVIEW-001D  
**Date:** 2026-07-08

This file shows five synthetic workflow scenarios. They are not real customer cases.

The goal is to make the prototype easier to understand by showing the same pattern repeatedly:

```text
messy input → safe small test → visible output → human check → reusable capability
```

---

## How to read these scenarios

Each scenario uses only synthetic or public-style sample content. The examples are intentionally small so a reviewer can see what the workflow is trying to prove without needing private data, production access, or a real customer case.

---

## Scenario 1: FAQ grouping

### Before

A team has repeated simple questions, but the questions are mixed together and nobody knows which topics should be turned into FAQ entries first.

### Synthetic input

```text
Can I change my appointment time?
Where can I find the refund policy?
Do you support weekend pickup?
Can I update my phone number?
```

### Safe first test

Group similar questions into simple topic labels without answering customers directly.

### Example output

```text
Appointment changes:
- Can I change my appointment time?

Policy questions:
- Where can I find the refund policy?

Pickup availability:
- Do you support weekend pickup?

Account/contact updates:
- Can I update my phone number?
```

### Human check

A human reviewer confirms whether the topic labels are understandable and whether any question is placed in the wrong group.

### Capability shown

```text
FAQ Topic Capability
```

---

## Scenario 2: Appointment notes

### Before

Short appointment messages contain useful details, but date, time, person, and follow-up notes are mixed inside free text.

### Synthetic input

```text
Alex wants to move the Tuesday 3pm visit to Friday morning. Please call back before noon.
```

### Safe first test

Extract appointment fields for human review. Do not update the real schedule automatically.

### Example output

```text
Person: Alex
Original time: Tuesday 3pm
Requested change: Friday morning
Follow-up: Call back before noon
Automation allowed: No
Human review required: Yes
```

### Human check

A human reviewer checks whether the extracted fields match the original message before any real schedule is changed.

### Capability shown

```text
Appointment-Service Capability
```

---

## Scenario 3: Daily work notes

### Before

A small team keeps daily notes, but delays, material issues, follow-ups, and review items are mixed together.

### Synthetic input

```text
Paint delivery was late. Front desk checklist done. Need to call supplier tomorrow. Review photos before closing.
```

### Safe first test

Group notes into simple operational categories.

### Example output

```text
Delay:
- Paint delivery was late.

Checklist:
- Front desk checklist done.

Follow-up:
- Need to call supplier tomorrow.

Review:
- Review photos before closing.
```

### Human check

A human reviewer checks whether the grouping is useful and whether any item needs a responsible owner.

### Capability shown

```text
Daily Note Capability
```

---

## Scenario 4: Small-test value check

### Before

A team has a vague AI idea, but the first step is too broad and may touch sensitive data too early.

### Synthetic input

```text
We want to use AI to improve customer service.
```

### Safe first test

Turn the vague idea into one small, reviewable, non-production experiment.

### Example output

```text
Unsafe first step:
- Let AI answer real customers automatically.

Safer first test:
- Use 20 synthetic customer-service questions.
- Ask AI to group the questions by topic.
- Do not send answers to customers.
- Have a human review the topic groups.

Reason:
- This tests usefulness without exposing real customer data or customer-facing output.
```

### Human check

A human reviewer confirms whether the test avoids sensitive data, avoids customer-facing automation, and produces a result that can be checked manually.

### Capability shown

```text
Small-Test Value Capability
```

---

## Scenario 5: Quality gate review

### Before

A drafted capability pack may sound useful, but it is not clear whether it is reusable, explainable, and reviewable.

### Synthetic input

```text
Capability draft: Customer Message Sorting Capability
Purpose: Sort customer messages into topics.
Example layer: missing
Traditional Chinese explanation: missing
English explanation: present
Human review rule: unclear
```

### Safe first test

Check whether the capability draft has enough structure to be reused safely.

### Example output

```text
Value card: Present
Example layer: Missing
Traditional Chinese version: Missing
English version: Present
Human review rule: Unclear

Gate result: Needs revision
Next safe patch:
- Add a small synthetic example.
- Add Traditional Chinese explanation.
- Define what a human must review before use.
```

### Human check

A human reviewer confirms whether the capability is simple enough, has a visible example, and does not imply production automation.

### Capability shown

```text
Capability Pack Quality Gate
```

---

## Boundary

```text
Synthetic examples only.
No real client data.
No private company data.
No production workflow.
No live automation.
No claim that these are real case studies.
```

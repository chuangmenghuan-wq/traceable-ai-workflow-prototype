# Friendly Question Boundary Copy

**Status:** Public-safe communication copy  
**Task ID:** LEAD-FLOW-001W  
**Purpose:** explain answer boundaries in a friendly, useful way

This document helps explain what people can ask during a public-safe review without making the boundary feel like a wall.

It should be used together with:

```text
release/review-response-scope.md
release/controlled-reviewer-operator-checklist.md
release/public-safe-package-index.md
```

---

## 1. Core message

Use this framing:

```text
You can ask many questions about the prototype, the sample outputs, the free preview, the safety boundary, and what a safe first experiment looks like.

For deeper implementation questions, I will keep the answer high-level because a full plan needs real workflow context and should not be guessed from a public-safe review.
```

This should feel like guidance, not refusal.

---

## 2. What you can ask

Useful public-safe questions include:

```text
What is this prototype for?
How is it different from asking GPT?
What does the free preview show?
Why are synthetic examples used?
Why should real customer data not be pasted?
What is a safe first experiment?
What does the sample output demonstrate?
What does a public-safe review note look like?
What does the package currently prove?
What does the package not prove yet?
```

---

## 3. How deeper questions will be handled

For deeper questions, use this tone:

```text
I can explain the direction and the public-safe structure, but I will keep the answer high-level here. A real plan depends on actual workflow context, allowed data, review ownership, tools, failure cases, and business goals.
```

Then redirect to:

```text
release/public-safe-package-index.md
examples/mini-audit-preview-sample.md
examples/public-safe-review-note-sample.md
docs/chinese-plain-language-overview.md
```

---

## 4. Friendly short version

For quick replies:

```text
You can ask about the concept, sample outputs, safety boundary, free preview, and what a safe first experiment looks like. If the question moves toward a full implementation plan, I will keep the answer high-level so we do not turn an early public-safe review into a guessed production plan.
```

---

## 5. Traditional Chinese version

```text
你可以問概念、範例、免費 preview、資料邊界、為什麼需要人工審查，以及第一步怎麼安全開始。

如果問題已經進到完整導入方案、真實公司流程、工具選型、正式系統設計或商業細節，我會先停在高層級。原因不是不能問，而是那些內容需要真實流程脈絡，不應該在 public-safe preview 裡用猜的。
```

---

## 6. Bad tone to avoid

Avoid wording that feels like:

```text
You cannot ask that.
That is confidential.
We will not answer.
That is locked.
```

Prefer wording that feels like:

```text
I can answer the public-safe part.
I can explain the high-level structure.
I will avoid guessing a full plan without real workflow context.
Here is the safest useful answer at this stage.
```

---

## 7. Decision

```text
Friendly question boundary copy added.
```

Use this copy when preparing reviewer instructions, Chinese explanations, or controlled preview responses.

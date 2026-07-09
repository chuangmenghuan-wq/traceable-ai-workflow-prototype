# CAP-AGENT-GOV-001｜Agent Governance Preflight Spec

**Status:** internal-spec / repo-docs-candidate  
**Mode:** internal governance / report-first / public-safe  
**Production status:** not production-ready, not SaaS, not compliance platform

## 1. Purpose

CAP-AGENT-GOV-001 defines the preflight gate that runs before a request enters the Capability Operating System chain.

Its job is to answer a different question from domain routing:

```text
Before asking what the task is, ask whether the agent is allowed to do it.
```

This capability protects the system from unauthorized tool writes, public output, private data handling, production changes, professional overclaims, hidden write effects, and approval scope creep.

## 2. Position

CAP-AGENT-GOV-001 is a Step 0 governance gate.

It is not a product feature, not a compliance guarantee, and not a replacement for legal, privacy, security, medical, financial, or human review.

It only classifies action permission:

- PASS
- USER_REVIEW_REQUIRED
- BLOCKED

## 3. Preflight Card

Each preflight produces a card with at least these fields:

| Field | Meaning |
|---|---|
| `task` | User-visible task summary |
| `data_type` | public / synthetic / private / unknown |
| `data_sensitivity` | low / medium / high / unknown |
| `tools_requested` | requested tools or write actions |
| `memory_needed` | none / temporary / persistent / sensitive |
| `output_type` | report / draft / public output / code / tool action |
| `risk_level` | low / medium / high / blocked |
| `human_approval_needed` | yes / no |
| `allowed_mode` | report-only / draft-only / read-only / write-with-approval / blocked |
| `blocked_actions` | actions that must not be executed |
| `audit_note_required` | yes / no |
| `stop_condition` | condition that stops the task |
| `decision` | PASS / USER_REVIEW_REQUIRED / BLOCKED |

## 4. Input Signals

Preflight may consume signals from later COS classifiers when available, but it does not replace them.

Important signals include:

- data sensitivity
- requested tool action
- public output risk
- repository governance risk
- production or deployment impact
- professional advice risk
- memory persistence risk
- external API / quota / cost risk
- approval scope match

## 5. Output Schema

```json
{
  "capability_id": "CAP-AGENT-GOV-001",
  "decision": "PASS | USER_REVIEW_REQUIRED | BLOCKED",
  "allowed_mode": "report-only | draft-only | read-only | write-with-approval | blocked",
  "blocked_actions": [],
  "human_approval_needed": true,
  "stop_condition": "string",
  "audit_note_required": true,
  "reason": "string"
}
```

## 6. Core Guarantees

1. Unknown does not PASS.
2. Tool write does not PASS silently.
3. Public output requires review.
4. GitHub write requires explicit approval.
5. Approval scope must match the exact action.
6. BLOCKED actions cannot be made valid by vague approval.
7. Fallback must be lower-risk than the original action.
8. The capability judges actual effects, not labels.

## 7. Non-goals

This capability does not:

- write GitHub files by itself
- merge pull requests
- publish public content
- handle real customer data automatically
- call external APIs automatically
- make legal, medical, financial, privacy, security, or compliance guarantees
- claim production-readiness

## 8. Status

This spec is part of the Agent Governance Mini repo-docs candidate batch. It remains internal and non-production until separately promoted and validated.

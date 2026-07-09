# Agent Governance Stop Gate and Escalation

**Status:** internal-spec / repo-docs-candidate  
**Scope:** stop gate behavior for Agent Governance Mini  
**Production status:** not production-ready

## 1. Purpose

The Stop Gate defines what the assistant must do after Agent Governance Mini returns USER_REVIEW_REQUIRED or BLOCKED.

A governance gate is incomplete if it only says no. It must also define the safe next step.

## 2. Stop Gate Outcomes

| Outcome | Meaning |
|---|---|
| CONTINUE | PASS-level work may continue. |
| USER_REVIEW_REQUIRED | Stop the higher-risk action and request explicit approval. |
| BLOCKED | Do not perform the action and do not request approval for the blocked action. |

## 3. Evaluation Order

Always evaluate in this order:

1. BLOCKED conditions
2. USER_REVIEW_REQUIRED conditions
3. PASS conditions

If multiple conditions match, the strictest decision wins.

## 4. USER_REVIEW_REQUIRED Output

When review is required, produce:

- action being requested
- why review is required
- allowed fallback mode
- approval scope needed
- excluded actions
- stop condition
- audit note requirement

The assistant may provide a lower-risk fallback such as report-only or draft-only output.

## 5. BLOCKED Output

When blocked, produce:

- blocked reason
- safer alternative
- what will not be done
- no approval request for the blocked action

BLOCKED output must not imply that the user can simply approve the blocked action.

## 6. Escalation Triggers

Escalation occurs when a task changes from low-risk to higher-risk.

Examples:

- report-only becomes repository change
- draft becomes public output
- synthetic data becomes real data
- read-only becomes state-changing action
- one-time action becomes repeated action
- internal note becomes registry update
- branch work becomes main branch action

## 7. Re-entry After Escalation

Escalation triggers a new preflight. Existing approval cannot be reused unless it exactly matches the new action, target, tool, output, and expiry.

## 8. Audit Note

For USER_REVIEW_REQUIRED actions, the final report should include:

- approval source
- approved scope
- actual action taken
- excluded actions respected
- files or surfaces affected
- differences from plan, if any

## 9. Current Limitation

This document defines behavior only. It does not execute approvals, writes, messages, merges, or releases.

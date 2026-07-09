# Agent Governance Approval Lifecycle

**Status:** internal-spec / repo-docs-candidate  
**Scope:** approval object lifecycle for Agent Governance Mini  
**Production status:** not production-ready

## 1. Purpose

Approval Lifecycle defines how an approval is represented, checked, expired, and revoked.

Core rule:

```text
No approval object, no approval.
```

## 2. Approval Object

A higher-risk action should be represented as:

```json
{
  "approval_id": "APR-YYYYMMDD-NNN",
  "approved_action": "string",
  "approved_scope": "string",
  "target_resource": "string",
  "allowed_tools": [],
  "allowed_output": "string",
  "expiry": "string",
  "session_boundary": "string",
  "excluded_actions": [],
  "rollback_or_stop_condition": "string",
  "approval_source": "user quote",
  "audit_note": "filled after action"
}
```

## 3. Scope Rules

1. One approval object covers one bounded action set.
2. `excluded_actions` should not be empty for higher-risk actions.
3. Approval does not automatically transfer across tools, resources, branches, data types, or sessions.
4. BLOCKED actions cannot be approved by an approval object.

## 4. Expiry Rules

Default expiry:

- one-time action completion
- task completion
- same session boundary
- explicit user revocation

A vague approval must not be stored as persistent authorization.

## 5. Revocation Rules

The following user signals pause or revoke active approval:

- stop
- wait
- hold on
- pause
- do not do it
- withdraw

After revocation:

1. stop pending action
2. report completed and incomplete parts
3. do not roll back unless rollback is separately approved
4. do not reuse the revoked approval object

## 6. Preflight Approval Check

```text
Step 0: Is the requested action BLOCKED?
  yes → BLOCKED. Do not check approval.
Step 1: Is there an active approval object?
  no → USER_REVIEW_REQUIRED.
Step 2: Does action, target, tool, output, and excluded scope match?
  no → USER_REVIEW_REQUIRED.
Step 3: Has approval expired or been revoked?
  yes → USER_REVIEW_REQUIRED.
Step 4: If all checks pass, action may proceed within scope.
```

## 7. Scope Creep Detection

The following require a new approval:

- draft PR to merge
- branch write to main write
- report-only to public output
- synthetic data to real data
- one-time action to repeated action
- local validation to production-impacting action
- read-only to state-changing action

## 8. Ambiguous Approval Handling

Vague phrases can only approve the immediately described PASS-level continuation. They cannot approve repository changes, public-facing output, private data handling, production-impacting action, deletion, payment, or persistent memory.

## 9. Audit Note

After any approved action, record:

- approval source
- branch or resource used
- files or surfaces affected
- excluded actions respected
- differences from approved scope
- stop condition status

## 10. Current Limitation

This document defines approval handling. It does not create, store, or execute approvals by itself.

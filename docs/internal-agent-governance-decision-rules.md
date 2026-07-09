# Agent Governance Decision Rules

**Status:** internal-spec / repo-docs-candidate  
**Scope:** decision source of truth for Agent Governance Mini  
**Production status:** not production-ready

## 1. Purpose

This document defines the current decision rules for Agent Governance Mini.

It supersedes the earlier GATE-001 decision pattern as the active decision source. The legacy file still requires a separate superseded annotation after its branch situation is resolved.

## 2. Decision Values

| Decision | Meaning |
|---|---|
| PASS | The task may continue in a low-risk mode. |
| USER_REVIEW_REQUIRED | The task must stop and request explicit approval before the higher-risk action. |
| BLOCKED | The requested action is not allowed in the current scope. |

## 3. PASS Conditions

PASS may be used only when all are true:

- internal-only or report-only
- public-safe wording
- no repository state change
- no public-facing release or response
- no real private data processing
- no production impact
- no payment, deletion, merge, or irreversible action
- no professional final decision or guarantee
- no persistent sensitive memory
- no unknown tool behavior

Allowed examples:

- report-only draft
- internal spec design
- synthetic test design
- safe checklist
- public-source research summary with citations when needed

## 4. USER_REVIEW_REQUIRED Conditions

USER_REVIEW_REQUIRED is used when the action may be valid, but needs explicit approval.

Examples:

- repository branch, commit, pull request, or registry update
- public-facing output
- external message sending
- private data access or processing
- real customer data handling
- API call, quota use, or paid tool use
- production-impacting action
- long-term memory write
- approval scope mismatch

## 5. BLOCKED Conditions

BLOCKED is used when the request is outside allowed scope even with vague approval.

Examples:

- secret exposure
- bypassing review gates
- destructive or irreversible action without a safe approval process
- unauthorized private data handling
- unsupported legal, medical, financial, privacy, security, or compliance guarantee
- production-ready claim without evidence
- using a superseded rule as the active source of truth

## 6. Fail-Closed Rules

1. Unknown data sensitivity does not PASS.
2. Unknown tool effect does not PASS.
3. Unclear approval scope does not authorize a write action.
4. Vague phrases such as continue, next step, OK, or you decide only apply to PASS-level work.
5. BLOCKED actions must not include an approval prompt.

## 7. Legacy GATE-001 Absorption

GATE-001 is treated as a legacy predecessor. Current governance decisions use CAP-AGENT-GOV-001 Decision Rules, Stop Gate, Approval Lifecycle, and Safe Fallback.

If GATE-001 conflicts with this document, this document wins.

## 8. Non-production Statement

These rules are internal governance rules. They are not a legal, privacy, security, compliance, or production-readiness guarantee.

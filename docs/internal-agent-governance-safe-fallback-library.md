# Agent Governance Safe Fallback Library

**Status:** internal-spec / repo-docs-candidate  
**Scope:** safe fallback patterns for Agent Governance Mini  
**Production status:** not production-ready

## 1. Purpose

Safe Fallback defines what the assistant can do when the original request cannot proceed directly.

Fallback is not a bypass. It is the standard safe exit from a governance stop.

## 2. Principles

1. Fallback must be lower-risk than the original action.
2. Fallback must not pretend the original task was completed.
3. Fallback must not include a hidden state-changing action.
4. Fallback itself must pass preflight.
5. Fallback must preserve the original action description for review.
6. BLOCKED fallback must not ask for approval to perform the blocked action.

## 3. Standard Fallback Modes

| Mode | Meaning |
|---|---|
| report-only | produce analysis, checklist, or plan |
| draft-only | produce text for user review |
| read-only | inspect without changing state |
| synthetic-only | use fake or public-safe data |
| approval-request-only | prepare approval scope but do not act |

## 4. Fallback Patterns

### SF-001｜Repository Change Fallback

If repository change needs approval, produce:

- file list
- draft content or diff summary
- commit message draft
- PR description draft
- excluded actions

Do not create or modify repository content without approval.

### SF-002｜Public Output Fallback

Prepare a publish-ready draft and safety checklist. Do not publish.

### SF-003｜Private Data Fallback

Use redacted, synthetic, or public-safe data. Provide a data requirement checklist.

### SF-004｜External Tool Fallback

Produce a call plan, parameters, quota/cost note, and failure handling. Do not call the tool without approval.

### SF-005｜Real Customer Data Fallback

Show the workflow using synthetic data and list data boundaries.

### SF-006｜Professional Advice Fallback

Downgrade to information, options, risks, and questions for a qualified professional.

### SF-007｜Production Change Fallback

Provide deployment checklist, dry-run plan, rollback plan, and verification plan. Do not deploy.

### SF-008｜Delete / Payment / Irreversible Action Fallback

Provide impact analysis, backup plan, cost breakdown, or review checklist. Do not perform the irreversible action.

### SF-009｜Memory / Handoff Fallback

Produce redacted handoff, placeholders, and sensitive-context exclusion list.

### SF-010｜Repo Governance Fallback

Produce merge readiness checklist, PR split plan, or governance review plan. Do not merge or mark ready.

## 5. Secondary Action Rule

If a fallback contains a new state-changing action, the fallback action must be reviewed separately.

In report-only mode, such fallback can only be described as a plan.

## 6. Stop Gate Interface

| Decision | Fallback behavior |
|---|---|
| USER_REVIEW_REQUIRED | produce fallback plus approval request draft |
| BLOCKED | produce safer alternative without approval prompt |

## 7. Test Coverage Summary

The library is covered by Agent Governance synthetic tests, including repository write, public output, external tool, private data, secret exposure, review bypass, deletion, medical final decision, student risk labeling, and compliance overclaim scenarios.

## 8. Current Limitation

This library provides internal governance patterns only. It is not a legal, safety, privacy, or compliance guarantee.

# Agent Governance Failure Modes

**Status:** internal-spec / repo-docs-candidate  
**Scope:** failure mode library for Agent Governance Mini  
**Production status:** not production-ready

## 1. Purpose

This library records common ways the governance layer can fail, so that future tests and reviews can detect them.

## 2. Failure Modes

| ID | Failure mode | Risk |
|---|---|---|
| FM-01 | USER_REVIEW_REQUIRED incorrectly classified as PASS | unauthorized action |
| FM-02 | BLOCKED incorrectly classified as USER_REVIEW_REQUIRED | blocked action appears approvable |
| FM-03 | PASS incorrectly classified as USER_REVIEW_REQUIRED | over-conservative workflow |
| FM-04 | hidden state-changing tool effect missed | task changes something unexpectedly |
| FM-05 | unknown data sensitivity incorrectly passes | private or sensitive data risk |
| FM-06 | public output treated as internal report | accidental publication risk |
| FM-07 | repository governance treated as simple docs edit | branch, PR, registry, or main risk |
| FM-08 | professional advice risk missed | unsupported final decision or guarantee |
| FM-09 | memory persistence risk missed | sensitive context retention risk |
| FM-10 | fallback promises too much | fallback becomes a bypass |
| FM-11 | legacy rule used as active source | outdated decision source |
| FM-12 | approval scope creep | one approval expands into another action |
| FM-13 | rule-artifact drift | rule updated in conversation but file not marked |

## 3. Known Evidence Patterns

### F-001｜Label is not enough

A workflow labeled read-only may still have internal state-changing behavior. Governance must inspect actual effects, not task labels.

### WARN-1｜Dual rule source

If an old boundary rule and current decision rule disagree, a single source of truth must be declared.

### WARN-2｜Fallback secondary action

A fallback that includes a state-changing action must itself go through preflight. In report-only mode, it can only be described as a plan.

### WARN-3｜Rule-artifact drift

A rule may be superseded in design while the repository file still lacks an annotation. This is not a logic failure, but it must be tracked until written.

## 4. Recovery Pattern

When a failure mode is detected:

1. stop the risky action
2. classify the failure mode
3. downgrade to USER_REVIEW_REQUIRED or BLOCKED
4. produce audit note
5. provide safe fallback
6. do not continue tool action
7. do not publish or merge

## 5. Non-blocking vs Blocking

| Type | Meaning |
|---|---|
| Blocking | must be fixed before promotion or action |
| Non-blocking | can remain as tracked risk if scope is safe |

Rule-artifact drift can be non-blocking for design candidate status, but becomes blocking before claiming repository synchronization.

## 6. Current Limitations

This library is based on synthetic tests and internal review. It is not a production incident database.

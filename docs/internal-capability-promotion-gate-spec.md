# CAP-SYS-003｜Capability Promotion Gate Spec

**Status:** internal-spec v0.2 / repo-docs-candidate  
**Mode:** report-only governance capability  
**Release status:** internal draft only

## 1. Purpose

CAP-SYS-003 decides whether a capability has enough evidence to move from one maturity level to the next.

It answers:

```text
Can this capability be promoted, held, fixed first, blocked, or deprecated?
```

It does not perform the promotion. It only produces a decision report.

## 2. Scope

CAP-SYS-003 is report-only. It does not change repository content, registry content, README, demo, main branch, PR state, or external systems.

## 3. Promotion Levels

| Level | Meaning |
|---|---|
| L0 | idea |
| L1 | written spec |
| L2 | test cases exist |
| L3 | synthetic tests passed |
| L4 | repo-docs-candidate / draft PR candidate |
| L5 | committed to repo docs or registry and verified |
| L6 | usable for real tasks with human review |
| L7 | semi-automated controlled execution |
| L8 | stable repeated execution |
| L9 | production-ready |

Promotion should normally move one level at a time. Current governance capabilities do not claim L9.

## 4. Gate Types

| Gate | Transition | Required evidence |
|---|---|---|
| Gate A | L1 to L2 | clear purpose, input/output, boundaries, test cases |
| Gate B | L2 to L3 | synthetic tests executed, pass/fail/warn recorded, fix loop if needed |
| Gate C | L3 to L4 | closeout, candidate file list, risk closure, approval draft, non-production statement |
| Gate D | L4 to L5 | explicit user approval, write completed, post-write check, no unapproved merge |
| Gate E | L5 to L6 | controlled dry-run, stop condition, rollback plan, human review |
| Gate F | L6 to L7+ | project-level review and stronger evidence |

## 5. Decision Values

| Decision | Meaning |
|---|---|
| PROMOTE | evidence is sufficient for requested next level |
| PROMOTE_AFTER_FIX | limited report-only fix is needed first |
| HOLD | cannot move yet; waits for external event or missing evidence |
| BLOCKED_FOR_PROMOTION | serious blocker prevents promotion |
| DEPRECATE_OR_SUPERSEDE | asset should be replaced or marked legacy |

## 6. PROMOTE_AFTER_FIX vs HOLD

PROMOTE_AFTER_FIX applies only when all are true:

1. missing items can be listed completely now
2. missing items can be produced report-only
3. checking the fix does not require rerunning the entire gate

Otherwise use HOLD.

## 7. Promotion Input Card

A promotion request should include:

- capability_id / capability_name
- current_level / target_level
- current_status
- evidence
- test_result
- warn_status
- health_status
- dependencies / downstream_users
- repo_docs_status / registry_status
- approval_status
- known_risks
- requested_promotion_reason

## 8. Promotion Output Report

The report should include:

- decision
- current_level / target_level / allowed_level
- blocking_issues
- non_blocking_warnings
- required_fixes
- required_approval
- excluded_actions
- evidence_summary
- health_check_summary
- next_step
- audit_note

## 9. Blocking Rules

Promotion is blocked or held when:

- FAIL remains unresolved
- test evidence is missing for L3+
- closeout is missing for L4
- blocking warning remains open
- health status is CONFLICT or unresolved high drift
- registry and actual state disagree outside the current promotion plan
- repo write is required but not approved
- L5 is claimed without write and verification evidence
- L9 is claimed without project-level evidence

## 10. Middle-state Rule

If registry or repo-doc mismatch is caused by the current promotion workflow itself and is already listed as a next step, use HOLD instead of BLOCKED_FOR_PROMOTION.

If the mismatch is unrelated or unmanaged, use BLOCKED_FOR_PROMOTION.

## 11. Synthetic Test Cases

The v0.2 test set includes PG-T01 through PG-T15, covering missing test cases, unexecuted tests, missing closeout, unapproved write, registry middle-state, unresolved FAIL, unclassified WARN, health conflict, superseded asset, department without output contract, boundary pack without test, overclaim, clear L3 to L4 promotion, L5 to L6 missing dry-run, and L6 to L7 project review.

## 12. Relation to Other Governance Capabilities

- CAP-SYS-001 supplies health status.
- CAP-SYS-002 supplies dependency impact.
- Agent Governance Mini controls any actual write, registry update, PR action, public output, or merge.

## 13. Non-claims

This specification is internal governance documentation only. It is not a launched product or production-ready system.

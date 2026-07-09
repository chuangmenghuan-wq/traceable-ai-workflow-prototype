# CAP-SYS-003-TEST-001｜Capability Promotion Gate Synthetic Test

**Status:** report-only synthetic test record  
**Result:** PASS after v0.2 fix loop  
**Release status:** internal draft only

## 1. Purpose

This test checks whether CAP-SYS-003 can classify promotion requests into PROMOTE, PROMOTE_AFTER_FIX, HOLD, BLOCKED_FOR_PROMOTION, or DEPRECATE_OR_SUPERSEDE.

## 2. Initial Result

Initial desk-check result:

```text
10 PASS / 0 FAIL / 2 WARN + 1 coverage gap
```

Warnings:

- W1: PROMOTE_AFTER_FIX vs HOLD boundary was unclear
- W2: registry drift middle-state created an apparent contradiction
- W3: PROMOTE decision had no dedicated coverage case

## 3. Fix Loop

### FIX-1｜PROMOTE_AFTER_FIX vs HOLD

PROMOTE_AFTER_FIX now requires three conditions:

1. missing items are finite and listable now
2. missing items can be produced report-only
3. checking the fix does not require rerunning the whole gate

Otherwise use HOLD.

### FIX-2｜Middle-state Rule

Registry or repo-doc mismatch caused by the current workflow and listed in next steps is HOLD. Unmanaged mismatch is BLOCKED_FOR_PROMOTION.

### FIX-3｜PG-T13

A clear L3 to L4 candidate with closeout, file list, risk closure, approval draft, and non-production statement is PROMOTE.

## 4. Final Test Cases

| Case | Scenario | Expected decision | Result |
|---|---|---|---|
| PG-T01 | spec exists but test cases missing | PROMOTE_AFTER_FIX | PASS |
| PG-T02 | test cases exist but not executed | HOLD | PASS |
| PG-T03 | tests pass but closeout missing | HOLD | PASS |
| PG-T04 | L4 to L5 without write approval | HOLD | PASS |
| PG-T05 | write done but registry sync pending in current plan | HOLD | PASS |
| PG-T06 | unresolved FAIL | BLOCKED_FOR_PROMOTION | PASS |
| PG-T07 | WARN not classified | PROMOTE_AFTER_FIX | PASS |
| PG-T08 | health conflict | BLOCKED_FOR_PROMOTION | PASS |
| PG-T09 | superseded document asks for promotion | DEPRECATE_OR_SUPERSEDE | PASS |
| PG-T10 | department draft lacks output contract | HOLD | PASS |
| PG-T11 | boundary pack lacks independent test | HOLD | PASS |
| PG-T12 | production-ready overclaim | BLOCKED_FOR_PROMOTION | PASS |
| PG-T13 | L3 to L4 conditions all satisfied | PROMOTE | PASS |
| PG-T14 | L5 to L6 missing controlled dry-run | HOLD | PASS |
| PG-T15 | L6 to L7 without project-level review | HOLD | PASS |

## 5. Final Result

| Metric | Value |
|---|---|
| total_cases | 15 |
| pass_count | 15 |
| fail_count | 0 |
| residual_warn_count | 0 |
| promote_detected | true |
| promote_after_fix_detected | true |
| hold_detected | true |
| blocked_for_promotion_detected | true |
| deprecate_or_supersede_detected | true |
| l5_requires_write_audit_health_check | true |
| l9_overclaim_blocked | true |
| no_tool_action_executed | true |
| no_repo_write_in_test | true |
| no_public_output | true |

## 6. Conclusion

CAP-SYS-003-TEST-001 passes for v0.2. The capability can be treated as L3 internal-spec evidence, not as a production-ready system.

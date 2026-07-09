# CAP-SYS-001-TEST-001｜Capability Health Checker Synthetic Test

**Status:** report-only synthetic test record  
**Result:** PASS after v0.2 fix loop  
**Release status:** internal draft only

## 1. Purpose

This test checks whether CAP-SYS-001 can classify capability assets using the health status values and action tiers defined in the spec.

## 2. Initial Result

Initial desk-check result:

```text
10 PASS / 0 FAIL / 2 WARN
```

Warnings:

- W1: multiple statuses were possible but severity order was missing
- W2: recommended_action needed a clearer three-tier model
- W3: BLOCKED_FOR_PROMOTION lacked a dedicated test case

## 3. Fix Loop

### FIX-1｜Severity Order

The v0.2 spec adds a status severity order:

```text
CONFLICT > DRIFT_RISK > SUPERSEDED unannotated > BLOCKED_FOR_PROMOTION > NEEDS_TEST > NEEDS_INTEGRATION > WATCH > SUPERSEDED annotated > HEALTHY
```

### FIX-2｜Action Tiers

Recommended action now has three tiers:

1. report-only may proceed
2. user approval required
3. do not do / do not promote

### FIX-3｜HC-T13

A new case covers blocked promotion when the capability requests repo-doc promotion but required governance write has not been approved.

## 4. Final Test Cases

| Case | Scenario | Expected status | Result |
|---|---|---|---|
| HC-T01 | complete healthy capability | HEALTHY | PASS |
| HC-T02 | spec but no test | NEEDS_TEST | PASS |
| HC-T03 | test pass but registry stale | DRIFT_RISK | PASS |
| HC-T04 | superseded document lacks annotation | DRIFT_RISK / SUPERSEDED | PASS |
| HC-T05 | two capabilities conflict | CONFLICT | PASS |
| HC-T06 | department lacks output contract | WATCH / NEEDS_INTEGRATION | PASS |
| HC-T07 | boundary pack referenced but untested | NEEDS_TEST | PASS |
| HC-T08 | production-ready overclaim | BLOCKED_FOR_PROMOTION | PASS |
| HC-T09 | legacy rule still referenced | DRIFT_RISK | PASS |
| HC-T10 | missing dependency | CONFLICT | PASS |
| HC-T11 | test targets old version | DRIFT_RISK | PASS |
| HC-T12 | spec/test exist but no chain or registry integration | NEEDS_INTEGRATION | PASS |
| HC-T13 | promotion blocked by missing approved governance write | BLOCKED_FOR_PROMOTION | PASS |
| HC-T14 | Step 0 chain graph stale | DRIFT_RISK | PASS |

## 5. Final Result

| Metric | Value |
|---|---|
| total_cases | 14 |
| pass_count | 14 |
| fail_count | 0 |
| residual_warn_count | 0 |
| severity_order_defined | true |
| action_tiers_defined | true |
| blocked_for_promotion_covered | true |
| no_tool_action_executed | true |
| no_repo_write_in_test | true |
| no_public_output | true |

## 6. Conclusion

CAP-SYS-001-TEST-001 passes for v0.2. The capability can be treated as L3 internal-spec evidence, not as a production-ready system.

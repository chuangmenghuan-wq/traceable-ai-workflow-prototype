# CAP-SYS-002-TEST-001｜Capability Dependency Mapper Synthetic Test

**Status:** report-only synthetic test record  
**Result:** PASS after v0.2 fix loop  
**Release status:** internal draft only

## 1. Purpose

This test checks whether CAP-SYS-002 can classify dependency relationships, detect drift and conflicts, and produce impact maps.

## 2. Initial Result

Initial desk-check result:

```text
13 PASS / 0 FAIL / 1 WARN
```

Warnings:

- W1: multiple status ordering was not defined
- W2: BLOCKED_FOR_MAPPING had no dedicated test case

## 3. Fix Loop

### FIX-1｜Multi-status Order

The v0.2 spec adds a multi-status order:

```text
BLOCKED_FOR_MAPPING > CYCLE_RISK > CONFLICTING_EDGE > SUPERSEDED_REFERENCE > MISSING_UPSTREAM > STALE_REFERENCE > MISSING_DOWNSTREAM > UNKNOWN_OWNER > WEAK_EVIDENCE > CLEAR
```

### FIX-2｜DM-T15

A new test case covers a department with no output contract, no owner, and no usage evidence. The expected result is BLOCKED_FOR_MAPPING.

## 4. Final Test Cases

| Case | Scenario | Expected status | Result |
|---|---|---|---|
| DM-T01 | clear hard dependency | CLEAR | PASS |
| DM-T02 | clear soft dependency | CLEAR | PASS |
| DM-T03 | informational reference | CLEAR | PASS |
| DM-T04 | missing upstream | MISSING_UPSTREAM | PASS |
| DM-T05 | missing downstream | MISSING_DOWNSTREAM | PASS |
| DM-T06 | superseded reference | SUPERSEDED_REFERENCE | PASS |
| DM-T07 | stale reference | STALE_REFERENCE | PASS |
| DM-T08 | conflicting edge | CONFLICTING_EDGE | PASS |
| DM-T09 | overlap with separation draft | CLEAR with overlaps_with | PASS |
| DM-T10 | hard dependency cycle | CYCLE_RISK | PASS |
| DM-T11 | weak evidence plus unknown owner | WEAK_EVIDENCE / UNKNOWN_OWNER | PASS |
| DM-T12 | CAP-CROSS-002 change impact | Impact Map produced | PASS |
| DM-T13 | registry drift impact | STALE_REFERENCE | PASS |
| DM-T14 | chain graph stale impact | STALE_REFERENCE | PASS |
| DM-T15 | insufficient evidence to map | BLOCKED_FOR_MAPPING | PASS |
| DM-T16 | retire item with hard downstream | HOLD / do not retire until downstream is handled | PASS |

## 5. Impact Coverage

The test includes:

- upstream impact
- downstream impact
- test impact
- registry impact
- documentation impact
- governance impact
- fallback / approval impact

Deep checks were performed for CAP-CROSS-002 change, registry drift, chain graph stale state, and retirement impact.

## 6. Final Result

| Metric | Value |
|---|---|
| total_cases | 16 |
| pass_count | 16 |
| fail_count | 0 |
| residual_warn_count | 0 |
| clear_detected | true |
| weak_evidence_detected | true |
| missing_upstream_detected | true |
| missing_downstream_detected | true |
| cycle_risk_detected | true |
| conflicting_edge_detected | true |
| stale_reference_detected | true |
| superseded_reference_detected | true |
| unknown_owner_detected | true |
| blocked_for_mapping_detected | true |
| impact_analysis_completed | true |
| no_tool_action_executed | true |
| no_repo_write_in_test | true |
| no_public_output | true |

## 7. Conclusion

CAP-SYS-002-TEST-001 passes for v0.2. The capability can be treated as L3 internal-spec evidence, not as a production-ready system.

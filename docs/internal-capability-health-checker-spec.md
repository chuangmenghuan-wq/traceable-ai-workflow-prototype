# CAP-SYS-001｜Capability Health Checker Spec

**Status:** internal-spec v0.2 / repo-docs-candidate  
**Mode:** report-only governance capability  
**Release status:** internal draft only

## 1. Purpose

CAP-SYS-001 checks the health of capability assets in the Capability Operating System.

It answers:

```text
Is this capability asset healthy, stale, conflicted, untested, disconnected, or blocked from promotion?
```

## 2. Scope

This capability may classify:

- Capability
- Department
- Boundary Pack
- Template
- Test
- Governance Rule
- Registry Entry
- Legacy or superseded document

It is report-only. It does not change repository content, registry content, public demo, README, main branch, PR state, or external systems.

## 3. Health Record Fields

Each checked item should include:

| Field | Meaning |
|---|---|
| item_id | stable identifier |
| item_name | human-readable name |
| item_type | capability, department, test, registry entry, etc. |
| current_status | current known status |
| maturity_level | L0-L9 maturity level |
| evidence | spec, test, closeout, PR, or report evidence |
| test_coverage | none / cases / synthetic pass / dry-run / real-use |
| dependencies | upstream items |
| downstream_users | items consuming this item |
| known_gaps | known missing pieces |
| conflict_or_overlap | conflict, overlap, or none |
| drift_risk | low / medium / high |
| superseded_status | current / superseded / supersedes other |
| recommended_action | report-only / needs approval / do not promote |
| next_review_needed | yes / no / condition |

## 4. Maturity Levels

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

This spec does not claim L9.

## 5. Health Status Values

| Status | Meaning |
|---|---|
| HEALTHY | evidence, tests, and references are consistent |
| WATCH | minor risk, no immediate block |
| NEEDS_TEST | spec exists but test evidence is missing |
| NEEDS_INTEGRATION | asset exists but is not connected to chain or registry |
| DRIFT_RISK | repo artifact, registry, chain, or status may be stale |
| CONFLICT | rules or artifacts contradict each other |
| SUPERSEDED | asset has been replaced or should be deprecated |
| BLOCKED_FOR_PROMOTION | cannot be promoted until blocking issue is resolved |

## 6. Severity Order

When multiple statuses apply, report them in this order:

```text
CONFLICT > DRIFT_RISK > SUPERSEDED unannotated > BLOCKED_FOR_PROMOTION > NEEDS_TEST > NEEDS_INTEGRATION > WATCH > SUPERSEDED annotated > HEALTHY
```

## 7. Recommended Action Tiers

1. report-only may proceed: analysis, draft, checklist, gap report
2. user approval required: repo write, registry update, chain update, annotation, PR action
3. do not do / do not promote: promotion while conflict remains or using superseded rule as current

## 8. Drift Detection

| Drift | Meaning |
|---|---|
| D1 | superseded document lacks annotation |
| D2 | test passed but registry not updated |
| D3 | capability upgraded but chain diagram remains old |
| D4 | legacy document still used as active rule source |
| D5 | report-only spec mislabeled as production-ready |

## 9. Output Format

A Health Checker report should include Summary, Inventory Table, Risk List, Promotion Candidates, Deprecation List, Recommended Next Actions, and a report-only statement.

## 10. Synthetic Test Cases

The v0.2 test set includes HC-T01 through HC-T14, covering healthy asset, missing test, registry drift, superseded document, conflicts, missing output contract, untested boundary pack, overclaim, legacy reference, missing dependency, stale test, disconnected asset, blocked promotion, and stale chain graph.

## 11. Relation to Other Governance Capabilities

- CAP-SYS-002 supplies dependency and downstream impact data.
- CAP-SYS-003 consumes health status for promotion decisions.
- Agent Governance Mini controls any actual corrective action.

## 12. Non-claims

This specification is internal governance documentation only. It is not a launched product or production-ready system.

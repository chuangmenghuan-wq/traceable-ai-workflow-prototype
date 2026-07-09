# CAP-SYS-002｜Capability Dependency Mapper Spec

**Status:** internal-spec v0.2 / repo-docs-candidate  
**Mode:** report-only governance capability  
**Release status:** internal draft only

## 1. Purpose

CAP-SYS-002 maps dependency relationships between capability assets.

It answers:

```text
Who depends on whom, and what changes if one item is modified, promoted, or retired?
```

This prevents dependency knowledge from living only in memory or scattered prose.

## 2. Scope

CAP-SYS-002 is report-only. It builds dependency maps and impact reports. It does not change repository content, registry content, README, demo, main branch, PR state, or external systems.

## 3. Node Types

| Node type | Meaning |
|---|---|
| Capability | reusable capability with a spec |
| Department | internal department or department draft |
| Boundary Pack | domain or safety boundary package |
| Template | reusable output or review template |
| Test | test case set or test report |
| Governance Rule | rule document |
| Registry Entry | registry record |
| Chain Step | position in a chain diagram |
| Legacy Document | superseded or old document |
| Evidence Document | closeout, audit, or promotion report |

## 4. Edge Types

| Edge | Meaning |
|---|---|
| consumes_output_of | source uses target output |
| validates | source validates target |
| gated_by | source action is governed by target |
| registered_in | source is recorded in target registry |
| supersedes | source replaces target |
| references | source text references target |
| routes_to | source routes work to target |
| produces_candidate_for | source produces candidates for target |
| conflicts_with | source conflicts with target |
| overlaps_with | source overlaps but can be separated |
| requires_approval_from | source action requires approval from target |

## 5. Dependency Record Fields

Each dependency record should include:

- source_id / source_name / source_type
- edge_type
- target_id / target_name / target_type
- dependency_direction
- strength: hard / soft / informational
- evidence
- risk_if_target_changes
- downstream_impact
- conflict_risk
- drift_risk
- recommended_action

## 6. Impact Analysis

For a requested modification, promotion, or retirement, the report should consider:

- upstream impact
- downstream impact
- test impact
- registry impact
- documentation impact
- governance impact
- fallback / approval impact

Example: if CAP-CROSS-002 changes, downstream human review and governance preflight inputs may require review, and related tests or registry entries may become stale.

## 7. Dependency Health Status

| Status | Meaning |
|---|---|
| CLEAR | dependency is well supported |
| WEAK_EVIDENCE | dependency exists but evidence is thin |
| MISSING_UPSTREAM | source depends on a missing target |
| MISSING_DOWNSTREAM | item has no known consumers |
| CYCLE_RISK | hard dependency loop exists |
| CONFLICTING_EDGE | incompatible edges exist between items |
| STALE_REFERENCE | reference points to old version |
| SUPERSEDED_REFERENCE | reference points to replaced item |
| UNKNOWN_OWNER | owner is not defined |
| BLOCKED_FOR_MAPPING | evidence is too incomplete to map safely |

## 8. Multi-status Order

A node or edge may have more than one status. Report them in this order:

```text
BLOCKED_FOR_MAPPING > CYCLE_RISK > CONFLICTING_EDGE > SUPERSEDED_REFERENCE > MISSING_UPSTREAM > STALE_REFERENCE > MISSING_DOWNSTREAM > UNKNOWN_OWNER > WEAK_EVIDENCE > CLEAR
```

Statuses from CYCLE_RISK through MISSING_UPSTREAM block related promotion until resolved.

## 9. Output Format

Dependency Mapper output should include:

- Summary
- Node Inventory
- Dependency Edge Table
- Impact Map
- Risk List
- Recommended Next Actions
- report-only statement

## 10. Known Initial Edges

The initial map includes relationships among CAP-CROSS chain capabilities, boundary packs, Agent Governance Mini, CAP-SYS-001, CAP-SYS-003, test reports, registry entries, department drafts, and legacy GATE-001 references.

## 11. Synthetic Test Cases

The v0.2 test set includes DM-T01 through DM-T16, covering hard, soft, informational, missing upstream, missing downstream, superseded reference, stale reference, conflicting edge, overlap, cycle risk, unknown owner, CAP-CROSS-002 impact, registry drift, chain graph stale, blocked mapping, and retirement impact.

## 12. Relation to Other Governance Capabilities

- CAP-SYS-001 uses dependency and downstream data to judge health.
- CAP-SYS-003 uses dependency impact when deciding promotion.
- Agent Governance Mini governs any actual corrective action.

## 13. Non-claims

This specification is internal governance documentation only. It is not a launched product or production-ready system.

# SUPERSEDE-REC-001｜GATE-001 Supersede Decision Record

**Status:** internal governance decision record / repo-docs-candidate  
**Scope:** legacy GATE-001 supersede record  
**Mode:** docs-only / report-only governance documentation  
**Production status:** not production-ready

## 1. Decision Statement

GATE-001 is a legacy / superseded source-archive artifact.

It must not be used as the active rule source for repository write actions, approval handling, stop-gate escalation, fail-closed behavior, or agent governance decisions.

Current governance decisions use the Agent Governance Mini documents on `main` as the active rule source.

## 2. Superseded Artifact Identification

| Field | Value |
|---|---|
| legacy_artifact_id | GATE-001 |
| legacy_artifact_name | Internal User Review Required Boundary |
| legacy_file_path | `docs/internal-user-review-required-boundary.md` |
| legacy_location | PR #2 source archive branch: `internal-sys-001-public-feedback-intake` |
| main_presence | not present on `main` at the time of this record |
| superseded_status | superseded / legacy archive artifact |

This record does not copy the legacy GATE-001 content into `main`.

## 3. Current Rule Sources

The current active rule sources are:

| Governance area | Current source |
|---|---|
| approval lifecycle | `docs/internal-agent-governance-approval-lifecycle.md` |
| stop-gate escalation | `docs/internal-agent-governance-stop-gate-escalation.md` |
| decision rules and fail-closed behavior | `docs/internal-agent-governance-decision-rules.md` |
| approval grammar | `docs/internal-agent-governance-approval-grammar.md` |
| safe fallback | `docs/internal-agent-governance-safe-fallback-library.md` |
| registry context | `docs/internal-capability-registry-v0.3-agent-governance.md` |

## 4. Prior Evidence Chain

`docs/internal-agent-governance-decision-rules.md` states that the current decision rules supersede the earlier GATE-001 decision pattern as the active decision source, and that the legacy file still requires a separate superseded annotation after its branch situation is resolved.

The same document treats GATE-001 as a legacy predecessor and states that current governance decisions use CAP-AGENT-GOV-001 Decision Rules, Stop Gate, Approval Lifecycle, and Safe Fallback. If GATE-001 conflicts with the current decision rules, the current decision rules win.

`docs/internal-capability-registry-v0.3-agent-governance.md` records the known artifact drift: the legacy GATE-001 file requires a superseded annotation, but the annotation was not performed in that batch because the legacy file was not present on `main` and modifying the PR #2 branch would have exceeded that batch scope.

This record completes that deferred documentation item on `main` without modifying the PR #2 source archive branch.

## 5. Archive Handling Rules

1. The original GATE-001 file remains in the PR #2 source archive branch.
2. The PR #2 source archive branch is not modified by this record.
3. GATE-001 must not be moved into `main` in its original form.
4. Future mini-PR splits from PR #2 must exclude the original GATE-001 artifact unless a later explicitly approved migration has a specific reason to transport it.
5. If GATE-001 is ever transported, it must carry a clear `SUPERSEDED` banner at the top, name its replacement sources, and state that it must not be used as an active rule source.
6. No chain, registry, runbook, or governance decision may cite GATE-001 as the active rule source.

## 6. Conflict Rule

If GATE-001 conflicts with current Agent Governance Mini documents, the current Agent Governance Mini documents win.

Current active governance decisions must use:

- `docs/internal-agent-governance-decision-rules.md`
- `docs/internal-agent-governance-approval-lifecycle.md`
- `docs/internal-agent-governance-stop-gate-escalation.md`
- `docs/internal-agent-governance-safe-fallback-library.md`

## 7. Drift Closure Note

This record closes the `main`-level D1 drift for GATE-001 under CAP-SYS-001:

```text
D1: superseded document lacks annotation
```

For dependency mapping, this record provides evidence for the edge:

```text
CAP-AGENT-GOV-001 supersedes GATE-001
```

This record does not clear unrelated registry drift, CAP-SYS registry sync drift, or future source archive split risks.

## 8. Boundary / Non-claims

This record is internal governance documentation only.

It does not:

- change README
- change the public demo
- change GitHub Pages behavior
- modify PR #2 or its branch
- modify any registry document
- add code, backend, storage, login, payment, or API behavior
- authorize production execution
- authorize real customer data handling
- create a SaaS launch claim
- create a legal, privacy, security, cybersecurity, or compliance guarantee
- claim production readiness

## 9. Reuse Pattern

This record defines a reusable pattern for future legacy artifact supersede records:

```text
legacy artifact identified
→ current rule source named
→ prior evidence chain recorded
→ archive handling rule defined
→ conflict rule stated
→ drift closure note added
→ non-claims boundary preserved
```

Future supersede records should use a new record ID, such as `SUPERSEDE-REC-002`, and should remain one artifact per record.

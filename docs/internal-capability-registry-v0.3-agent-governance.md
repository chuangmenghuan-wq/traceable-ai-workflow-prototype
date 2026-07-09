# Internal Capability Registry v0.3｜Agent Governance Mini

**Status:** internal registry draft / repo-docs-candidate  
**Scope:** CAP-AGENT-GOV-001 registry entry and v0.3 chain note  
**Production status:** not production-ready

## 1. Purpose

This document records CAP-AGENT-GOV-001 as a registry-ready internal capability candidate.

It does not mark the capability as production-ready and does not modify any live registry automatically.

## 2. Capability Entry

| Field | Value |
|---|---|
| capability_id | CAP-AGENT-GOV-001 |
| capability_name | Agent Governance Preflight |
| capability_family | Agent Governance Mini |
| capability_type | governance / preflight / approval boundary |
| current_status | repo-docs-candidate |
| maturity_level | L4 candidate, not L5 until committed and verified |
| owner_layer | System Governance / Action Governance |
| primary_decision_values | PASS / USER_REVIEW_REQUIRED / BLOCKED |
| primary_outputs | Preflight Card, allowed mode, blocked actions, stop condition, audit note requirement |
| tests | AGENT-GOV-TEST-001, AGENT-GOV-TEST-002 |
| production_ready | false |

## 3. Component Set

CAP-AGENT-GOV-001 is supported by these documents:

1. Preflight Spec
2. Chain Integration
3. Decision Rules
4. Approval Grammar
5. Stop Gate and Escalation
6. Review Templates
7. Failure Modes
8. Safe Fallback Library
9. Approval Lifecycle
10. TEST-001 Preflight Synthetic Test
11. TEST-002 Approval Lifecycle Regression Test

## 4. v0.3 Chain Note

The intended v0.3 chain inserts CAP-AGENT-GOV-001 before the existing CAP-CROSS chain:

```text
Input request
→ CAP-AGENT-GOV-001 Agent Governance Preflight
→ CAP-CROSS-001 Domain Intake Classifier
→ CAP-CROSS-002 Data Sensitivity Classifier
→ CAP-CROSS-003 Task Intent Classifier
→ CAP-CROSS-004 Domain Department Matcher
→ CAP-CROSS-005 Domain Validation Pack Selector
→ CAP-CROSS-008 Multi-Department Routing Resolver
→ CAP-CROSS-013 Routing Coordinator
→ CAP-CROSS-006 Human Review Gate Builder
→ CAP-CROSS-009 Safe First Test Generator
→ CAP-CROSS-011 Domain Report Output Builder
→ CAP-CROSS-007 Blocked Claims Detector
→ CAP-CROSS-012 Domain Gap Detector
→ CAP-R2C-001 Capability Candidate Extractor
→ Registry decision
```

## 5. Re-entry Points

CAP-AGENT-GOV-001 should also re-enter before:

1. state-changing tool action
2. public-facing output
3. registry decision or registry update
4. escalation
5. approval scope mismatch
6. fallback-created new action

## 6. Promotion Status

| Level | Status |
|---|---|
| L1 | complete: text spec exists |
| L2 | complete: synthetic test cases exist |
| L3 | complete: synthetic tests passed |
| L4 | complete: repo-docs-candidate closeout exists |
| L5 | not complete: not yet committed and post-write verified |
| L6+ | not in scope |

## 7. Known Artifact Drift

The legacy GATE-001 file requires a superseded annotation. In this branch, that annotation is not performed because the legacy file is not present on `main` and modifying the PR #2 branch would exceed this batch scope.

## 8. Non-claims

This registry draft does not claim:

- production readiness
- legal, privacy, security, or compliance assurance
- SaaS launch
- public product release
- autonomous execution permission

## 9. Recommended Verification After Write

After this batch is written, verify:

- all listed files exist
- tests are present
- v0.3 chain note includes Step 0
- no README or demo files were changed
- no merge or ready-for-review action occurred

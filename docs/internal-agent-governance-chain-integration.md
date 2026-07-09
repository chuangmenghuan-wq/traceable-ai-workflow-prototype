# Agent Governance Chain Integration

**Status:** internal-spec / repo-docs-candidate  
**Scope:** COS chain integration note for CAP-AGENT-GOV-001  
**Production status:** not production-ready

## 1. Purpose

This document defines where Agent Governance Mini sits in the Capability Operating System chain.

Core rule:

```text
Agent Governance Mini controls whether the agent may act.
CAP-CROSS chain controls how the case should be processed.
```

## 2. v0.3 Chain Draft

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

## 3. Step 0 Rule

CAP-AGENT-GOV-001 runs before CAP-CROSS-001 because permission risk can exist before the domain is known.

Typical risk signals:

- repository change
- external communication
- private or sensitive data handling
- production-impacting action
- unknown tool behavior
- persistent memory request

## 4. Re-entry Rules

CAP-AGENT-GOV-001 is not only a one-time front door. It must re-enter at these action boundaries:

1. before any tool changes state
2. before any public-facing output
3. before registry decision or registry update
4. when escalation occurs
5. when approval scope does not match the requested action
6. when fallback creates a new action

## 5. Responsibility Split

| Component | Owns |
|---|---|
| CAP-AGENT-GOV-001 | agent permission, allowed mode, approval scope, blocked actions |
| CAP-CROSS-001 | domain intake |
| CAP-CROSS-002 | data sensitivity classification |
| CAP-CROSS-006 | case-level human review gate |
| CAP-CROSS-007 | output claim safety |
| CAP-R2C-001 | capability candidate extraction |

CAP-CROSS-002 can provide data sensitivity as an input signal to Agent Governance Mini. Agent Governance Mini does not replace CAP-CROSS-002.

## 6. Effect-Based Rule

The chain judges actual effects, not labels.

If a task is labeled low risk but the actual result changes repository content, registry content, public-facing content, or persistent records, the action boundary triggers preflight re-entry.

## 7. Public Repository Rule

Public repository branches, pull requests, issues, and comments are public surface. Creating a draft PR is a repository change and requires explicit approval.

## 8. Current Limitation

This document describes integration design only. It does not modify the public demo, README, main branch, or PR #2.

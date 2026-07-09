# Agent Governance Approval Grammar

**Status:** internal-spec / repo-docs-candidate  
**Scope:** approval scope grammar for Agent Governance Mini  
**Production status:** not production-ready

## 1. Purpose

Approval grammar prevents vague approval from expanding into unintended actions.

Core rule:

```text
Approval is not a mood. Approval is a bounded object.
```

## 2. Valid Approval Shape

A valid approval for a higher-risk action must include enough information to identify:

- approved action
- target resource
- allowed tools or surfaces
- expected output
- excluded actions
- expiry or session boundary
- stop condition

## 3. Vague Phrases

The following phrases do not authorize repository changes, public output, external messages, production-impacting actions, deletion, payment, private data access, or persistent memory:

- continue
- next step
- OK
- yes
- you decide
- do what you think
- no need to ask me

They may only allow low-risk report-only continuation.

## 4. Scope Boundaries

Approval does not cross these boundaries unless explicitly stated:

| Boundary | Example |
|---|---|
| action | draft does not authorize publish |
| resource | one repo does not authorize another repo |
| branch | one branch does not authorize main |
| output | report does not authorize public reply |
| data | synthetic data does not authorize real data |
| tool | read does not authorize write |
| session | prior session approval does not automatically persist |

## 5. Negative Scope Required

Higher-risk approval should include excluded actions.

Typical exclusions:

- do not merge main
- do not mark ready for review
- do not change public demo
- do not change README unless separately approved
- do not publish public posts
- do not process real customer data
- do not delete files
- do not force push

## 6. Multi-Action Requests

If a request contains multiple higher-risk actions, each action needs either:

1. a separate approval object, or
2. a single approval object listing every action and every exclusion.

If unclear, the system must split and hold.

## 7. Revocation Language

The following pauses or revokes current execution:

- stop
- wait
- hold on
- do not do it
- withdraw
- pause

After revocation, a new approval is required.

## 8. Output

Approval grammar should produce either:

- approval object draft
- missing approval fields
- decision that existing approval is insufficient

It must not silently infer authorization for a repository change or public-facing action.

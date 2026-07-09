# Agent Governance Review Templates

**Status:** internal-spec / repo-docs-candidate  
**Scope:** human review request templates for Agent Governance Mini  
**Production status:** not production-ready

## 1. Purpose

This document provides standard wording for USER_REVIEW_REQUIRED actions.

The goal is to ask for precise approval without hiding scope or bundling unsafe actions.

## 2. Review Request Levels

| Level | Use |
|---|---|
| Level 1 Soft Review | User should review wording or direction. No action is executed. |
| Level 2 Action Review | A bounded repository, tool, or external action needs approval. |
| Level 3 Governance Review | The action changes governance, registry, public positioning, or escalation rules. |

## 3. Generic Review Template

```text
Review required before continuing.

Requested action:
- <action>

Why review is required:
- <reason>

Allowed scope if approved:
- <scope>

Excluded actions:
- <excluded actions>

Fallback available now:
- <report-only or draft-only fallback>

Stop condition:
- <stop condition>
```

## 4. Repository Change Template

```text
Repository write requires approval.

Approved action needed:
- create branch / commit listed files / open draft PR

Target:
- repo: <owner/repo>
- branch: <branch>

Allowed output:
- one draft PR

Excluded:
- no merge
- no mark ready
- no README or demo change unless separately approved
- no deletion
- no force push
- no unrelated PR changes
```

## 5. Public Output Template

```text
Public-facing output requires review.

I can prepare a draft now, but I will not publish or reply publicly without explicit approval.
```

## 6. Private Data Template

```text
Private or sensitive data handling requires review.

Fallback:
- use synthetic data
- ask for a redacted sample
- produce a data requirement checklist
```

## 7. API or External Tool Template

```text
External call or quota-impacting action requires review.

Fallback:
- produce a call plan
- simulate with synthetic input
- list endpoint, parameters, cost, quota, and failure handling
```

## 8. Registry or Governance Template

```text
Registry or governance change requires review.

Fallback:
- produce a registry diff draft
- list affected capabilities
- provide rollback and verification plan
```

## 9. BLOCKED Fallback Template

```text
I cannot perform the requested action because: <reason>.

Safer alternative:
- <educational explanation / checklist / synthetic demo / draft-only output>

I will not ask for approval to perform the blocked action.
```

## 10. Boundary with CAP-CROSS-006

CAP-CROSS-006 handles case-level review. This document handles agent-action approval.

If both apply, action approval must be resolved before any action is executed.

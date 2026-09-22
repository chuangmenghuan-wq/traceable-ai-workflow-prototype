# Architecture

## Product boundary

Future Ability is an assurance/control plane above interchangeable AI executors.

```text
Goal / Service Contract
        ↓
Capability Registry
        ↓
Source Qualification
        ↓
Authority Gate
        ↓
Planner / Executor
        ↓
Independent Verifier
        ↓
Completion Truth
        ↓
Recovery / Replan / Escalate
        ↓
Evidence Ledger
```

## Three planes

### Control plane
- goal / root state
- capability registry
- qualification registry
- authority policy
- planner / dispatcher
- completion truth
- recovery / successor logic
- evidence ledger

### Execution plane
- local or remote model executor
- tool adapters
- code/configuration repair
- test runner
- deployment target

### Verification plane
- independent health probes
- business transaction probes
- evidence freshness checks
- contradiction detection
- deterministic completion gates

## Capability Source

A Capability Source is the deployable trust object:

```text
model + runtime + hardware + tools + authority profile
```

Task-family qualification belongs to the source, not merely to the model name.

A material source change can invalidate prior trust and trigger requalification.

## Core invariant

**Execution Receipt cannot prove its own completion.**

The executor may provide execution evidence, but the required outcome is decided from independently observed evidence against the goal/service contract.

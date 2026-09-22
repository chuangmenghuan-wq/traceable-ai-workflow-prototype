# Authority and Qualification

## Qualification

A candidate capability source must earn eligibility for a task family through deterministic and adversarial checks.

Qualification is operational: it is connected to what the source is allowed to execute.

## Authority

Every proposed action is resolved to one of three outcomes:

- **AUTO** — bounded low-risk action may proceed.
- **HUMAN APPROVAL** — explicit approval is required.
- **DENY** — action is outside the allowed policy/scope.

The model cannot promote its own authority.

## Fail-closed behavior

If capability existence, authority, required evidence, or legal execution path is missing, the correct state is BLOCKED / ESCALATE rather than inventing a new privileged action.

## Requalification

A material change to any of the following can require requalification:

- model,
- quantisation/runtime,
- hardware,
- tool adapters,
- authority policy/profile.

This is how Future Ability turns model benchmarking into an operational trust gate.

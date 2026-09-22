# Completion Truth

Future Ability separates four states that are often collapsed into one:

| State | Question |
|---|---|
| Execution PASS | Did the command/action run? |
| Task PASS | Did the local repair meet its immediate condition? |
| Business Restored | Do required external probes prove the service outcome? |
| Root Cause Resolved | Is the causal contract closed with no unresolved required frontier? |

## False-completion example

```json
{
  "execution_ok": true,
  "local_tests": "PASS",
  "business_probes": {
    "health": "PASS",
    "authentication": "FAIL",
    "transaction": "FAIL"
  },
  "business_restored": false,
  "completion_allowed": false,
  "next_state": "RECOVER_OR_REPLAN"
}
```

The point is not that an agent can never be wrong. The point is that a local success signal cannot silently become mission completion.

## Evidence rules

Required evidence should carry:
- source,
- timestamp,
- observed value,
- freshness status,
- goal/contract mapping.

Missing, stale, conflicting, or failing required evidence blocks automatic completion.

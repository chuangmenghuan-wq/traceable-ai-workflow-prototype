# Architecture

```text
User Task
  ↓
Task Intake
  ↓
Task Classification
  ↓
Execution Plan
  ↓
Capability Router
  ↓
Demo Execution
  ↓
Validation Layer
  ↓
Report Layer
  ↓
Traceability Layer
```

## Mermaid diagram

```mermaid
flowchart TD
    A[User Task] --> B[Task Intake]
    B --> C[Task Classification]
    C --> D[Execution Plan]
    D --> E[Capability Router]
    E --> F[Demo Execution]
    F --> G[Validation Layer]
    G --> H[Report Layer]
    H --> I[Traceability Layer]
    G --> J[Safety Boundary Check]
    J --> K{Pass?}
    K -->|Yes| H
    K -->|No| L[Stop / Revise / Block]
```

## Design principle

Make AI workflow decisions visible, reviewable, and safer before production use.

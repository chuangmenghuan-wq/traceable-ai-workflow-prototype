# ROUTER-TEST-001｜Universal Router Synthetic Intake Test Matrix

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal test report / public-safe  
**Date:** 2026-07-09  
**Mode:** Synthetic-only / report-only / no private data  

> 中文定位：這份報告用 synthetic cases 測試 Universal Domain Intake Router。目的不是證明系統已經完美，而是檢查「不同資料進來 → 是否能判斷產業、資料型態、敏感度、任務意圖、部門、validation pack、下一步輸出」。

---

## 1. Test goal

```text
Test whether COS can route diverse synthetic inputs into the correct domain department and validation pack.
```

中文目標：

```text
測試不同產業任務進來時，系統能不能先分對，而不是直接亂產報告。
```

---

## 2. Test boundary

```text
Synthetic cases only: yes
Private data used: no
Real customer data used: no
Production systems touched: no
Backend/API/storage/login added: no
Public demo changed: no
```

---

## 3. Synthetic intake matrix

| Test ID | Synthetic input summary | Detected domain | Data type | Sensitivity | Intent | Routed department | Validation pack | Result |
|---|---|---|---|---|---|---|---|---|
| T01 | Draft a note from fake doctor-patient transcript | Healthcare | transcript / note | S4 if real | summarize / draft | Healthcare Workflow candidate + Workflow Safety | Healthcare Workflow Validation Pack | PASS |
| T02 | Extract claim parts from fake insurance claim text | Insurance | claim document | S3-S4 if real | extract fields | Insurance Process Automation candidate | Insurance Process Automation Validation Pack | PASS |
| T03 | Review fake legal mediation draft risks | Legal | legal draft | S3-S4 if real | risk review / draft | Legal AI Risk candidate + Workflow Safety | Legal AI Risk Validation Pack | PASS |
| T04 | Classify fake shipment item for trade compliance triage | Logistics | shipment/classification text | S2-S4 if real | classify / compliance triage | Logistics Compliance candidate | Logistics Compliance Validation Pack | PASS |
| T05 | Generate product description from fake catalog fields | Retail / marketing | product data | S1-S3 | content draft | Retail Data Operations candidate | Retail Data Operations Validation Pack | PASS |
| T06 | Check fake farm sensor/weather/yield data readiness | Agriculture | sensor/weather/yield table | S1-S3 | data readiness / decision support | Agriculture Decision Support candidate | Agriculture Decision Support Validation Pack | PASS |
| T07 | Create dry-run plan from fake machine failure logs | Manufacturing | machine logs | S2-S3 | predictive maintenance / dry-run | Manufacturing Operations candidate | Manufacturing Operations Validation Pack | PASS |
| T08 | Summarize fake public feedback comment | Public feedback | public comment | S0 | classify feedback | Public Feedback Department | Public Feedback boundary | PASS |
| T09 | Evaluate fake AI vendor pricing and lock-in | Tool research | public pricing/tool notes | S0 | vendor evaluation | Tool Research Department | Tool Research boundary | PASS |
| T10 | Convert repeated fake workflow lesson into capability | Research-to-capability | internal summary | S0-S1 | capability extraction | Research-to-Capability Department | Registry v0.2 mapping | PASS |

---

## 4. Routing observations

### Observation A — Domain detection works for clear cases

```text
Healthcare, insurance, legal, logistics, retail, agriculture, and manufacturing cases routed correctly when the synthetic input clearly included domain-specific vocabulary.
```

### Observation B — Sensitivity detection is necessary before output

```text
Healthcare, insurance, legal, logistics, agriculture, and manufacturing all become higher-risk if real data is used.
```

### Observation C — Validation pack selection is now visible

```text
The router can now route not only to a department, but also to a domain-specific validation pack.
```

### Observation D — Public/internal generic signals still route to existing departments

```text
Public feedback, tool research, and capability extraction do not need new Domain Departments.
```

---

## 5. Failures / limitations

No blocking routing failures were found in this synthetic test.

But limitations remain:

```text
- synthetic tests are easier than messy real inputs
- mixed-domain cases may require multi-department routing
- ambiguous cases need clarification or watch/backlog route
- real sensitive data remains blocked
- production execution is not authorized
```

---

## 6. New gap discovered

```text
MIXED-ROUTING-001｜Multi-Department Routing Rule
```

Reason:

```text
Some real cases will span multiple domains.
Example: AI for healthcare insurance claim review touches healthcare, insurance, legal/compliance, and privacy.
A single department route may be insufficient.
```

---

## 7. Maturity assessment after this test

```text
Universal domain intake: draft-tested on synthetic cases
Domain Department Factory: draft-tested on public/synthetic patterns
Domain Validation Packs: template-level ready
Multi-department routing: missing / next gap
Real private data readiness: no
Production readiness: no
```

---

## 8. Closeout

```text
ROUTER-TEST-001 result: PASS
Synthetic cases tested: 10
Routing success: 10/10 synthetic cases
Private data used: no
Domain validation pack selection tested: yes
New gap found: Multi-Department Routing Rule needed
Recommended next: MIXED-ROUTING-001｜Multi-Department Routing Rule
```

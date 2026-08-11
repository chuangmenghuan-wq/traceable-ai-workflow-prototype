# MIXED-ROUTING-001｜Multi-Department Routing Rule

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal architecture upgrade / public-safe  
**Date:** 2026-07-09  
**Mode:** Docs-only / routing rule  

> 中文定位：這份文件補上 ROUTER-TEST-001 發現的缺口：真實任務常常不是單一領域，而是跨部門、跨產業、跨風險。例如醫療保險理賠、金融法遵、物流海關、零售個資行銷，都不能只交給一個部門。系統需要 Multi-Department Routing Rule。

---

## 1. Why this is needed

Single-department routing is not enough when a case crosses:

```text
- multiple domains
- multiple data types
- regulated + business workflows
- customer impact + operational automation
- professional advice + decision support
```

中文說明：

```text
真實世界不是單選題。
一個任務可能同時需要醫療、保險、法律、隱私、流程設計、人審 gate。
```

---

## 2. Core rule

```text
If a case touches more than one domain, route to a lead department plus supporting departments.
```

---

## 3. Routing structure

```text
Lead Department:
Supporting Departments:
Domain Departments:
Safety Gate Owner:
Validation Pack Owner:
Final Output Owner:
User Review Required: yes / no
```

---

## 4. Lead department selection

Choose lead department by primary task intent:

| Primary intent | Lead department |
|---|---|
| workflow risk / safe first test | Workflow Safety Department |
| public feedback | Public Feedback Department |
| tool/vendor evaluation | Tool Research Department |
| capability extraction | Research-to-Capability Department |
| demo packaging | Demo Kit Department |
| public-source industry case research | Industry Case Research Department |
| domain-specific operation | relevant Domain Department candidate |
| regulated/high-sensitive decision support | Workflow Safety Department leads |

---

## 5. Supporting department rules

Add supporting departments when:

```text
- tool/vendor/cost questions appear → Tool Research Department
- repeated reusable pattern appears → Research-to-Capability Department
- public/synthetic industry evidence needed → Industry Case Research Department
- public/demo explanation needed → Demo Kit Department
- safety, human review, validation needed → Workflow Safety Department
- public response needed → Public Feedback Department
```

---

## 6. Mixed-case examples

### Example A — Healthcare insurance claim review

```text
Domains: healthcare + insurance + legal/privacy
Lead: Workflow Safety Department
Supporting: Industry Case Research Department, Insurance Process Automation candidate, Healthcare Workflow candidate
Validation packs: Healthcare Workflow + Insurance Process Automation + Legal boundary
User review required: yes if real data
```

### Example B — AI trade compliance assistant

```text
Domains: logistics + legal/compliance + customer data
Lead: Logistics Compliance Department candidate
Supporting: Workflow Safety Department, Tool Research Department
Validation packs: Logistics Compliance + Legal boundary
User review required: yes if real shipment/customs data
```

### Example C — Retail personalization with customer profiles

```text
Domains: retail + marketing + privacy/data governance
Lead: Retail Data Operations Department candidate
Supporting: Workflow Safety Department, Public-Safe Boundary Guard
Validation packs: Retail Data Operations + customer data boundary
User review required: yes if real customer data
```

### Example D — Manufacturing predictive maintenance tool purchase

```text
Domains: manufacturing + tool research + operations safety
Lead: Manufacturing Operations Department candidate
Supporting: Tool Research Department, Workflow Safety Department
Validation packs: Manufacturing Operations + Tool Research boundary
User review required: yes if production system integration
```

---

## 7. Output template

```text
Case summary:
Detected domains:
Lead department:
Supporting departments:
Data sensitivity:
Primary validation pack:
Secondary validation packs:
Human review owner:
Blocked actions:
Safe first output:
Capability candidates:
Registry decision:
```

---

## 8. Conflict rule

If departments disagree:

```text
highest-risk boundary wins
```

Priority order:

```text
1. User Review Boundary / blocked-current-phase
2. Workflow Safety Department
3. Domain-specific validation pack
4. Research-to-Capability Department
5. Tool Research / Demo / Public Feedback support
```

---

## 9. What this improves

Before:

```text
case → one department → one report
```

After:

```text
case → lead department + supporting departments → multiple validation packs → safer report → capability extraction
```

---

## 10. What this does not authorize

```text
- real private data use
- backend/API integration
- production automation
- legal/medical/financial/compliance/security advice
- public demo changes
- public replies
```

---

## 11. Closeout

```text
MIXED-ROUTING-001 result: PASS
Lead/support department model defined: yes
Conflict rule defined: yes
Mixed-domain examples defined: yes
No public demo code changed: yes
No backend / AI API added: yes
No real customer data added: yes
Recommended next: update PR summary and validate branch diff
```

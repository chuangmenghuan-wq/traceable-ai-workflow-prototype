# ROUTING-COORDINATOR-001｜Routing Coordinator Role

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal architecture upgrade / public-safe  
**Date:** 2026-07-09  
**Mode:** Docs-only / coordination role  

> 中文定位：這份文件補上 MIXED-ROUTING-TEST-001 發現的缺口：當一個任務同時牽涉 3 個以上部門時，需要 Routing Coordinator 統一輸出、管理衝突、套用最高風險邊界，避免多部門各講各話。

---

## 1. Why this role is needed

Multi-department routing can produce better safety, but it can also create:

```text
- conflicting department recommendations
- duplicated output sections
- unclear final owner
- weak priority between business value and risk boundary
- missing final summary
```

Routing Coordinator solves:

```text
lead/support routing → coherent final output → highest-risk boundary preserved
```

---

## 2. Coordinator responsibility

```text
1. Confirm lead department.
2. Confirm supporting departments.
3. Apply highest-risk-boundary rule.
4. Select primary and secondary validation packs.
5. Merge department outputs into one report.
6. Remove conflicting or unsafe recommendations.
7. Ensure human review gates are clear.
8. Ensure blocked actions are explicit.
9. Produce final next safe step.
```

---

## 3. When coordinator is required

Required when:

```text
- 3+ departments are involved
- regulated/sensitive data appears
- multiple validation packs apply
- business workflow + legal/privacy/security risk coexist
- case spans domain + tool research + workflow safety
- there are conflicting department recommendations
```

Not required when:

```text
- single domain and low risk
- existing department owner is clear
- validation pack is obvious
- output is only a short internal note
```

---

## 4. Coordinator assignment rule

Default coordinator:

```text
COS-Core
```

Workflow Safety Department coordinates when:

```text
- regulated/high-sensitive data appears
- human review gate is central
- legal/medical/financial/security/compliance risk appears
- highest-risk-boundary rule is triggered
```

Industry Case Research coordinates when:

```text
- task is public-source case research
- no real data is used
- output is a domain research report
```

Research-to-Capability coordinates when:

```text
- task is extracting reusable capabilities from repeated cases
```

---

## 5. Coordinator output template

```text
Case summary:
Lead department:
Supporting departments:
Coordinator:
Primary risk boundary:
Primary validation pack:
Secondary validation packs:
Conflicts detected:
Conflict resolution:
Human review gate:
Blocked actions:
Final safe output:
Capability candidates:
Next safe step:
```

---

## 6. Conflict resolution rules

```text
1. Highest-risk boundary wins.
2. No department may authorize real private data without approval.
3. No department may override human review for high-risk cases.
4. Tool Research may recommend report-only evaluation, not adoption.
5. Demo Kit may explain, not sell or publish without approval.
6. Research-to-Capability may extract capability candidates, not implement production features.
```

---

## 7. Example

### Healthcare insurance claim review

```text
Lead department: Workflow Safety Department
Supporting departments: Healthcare Workflow candidate, Insurance Process Automation candidate, Industry Case Research Department
Coordinator: Workflow Safety Department
Primary risk boundary: medical + claim + privacy/legal sensitivity
Conflict resolution: no payout/coverage/clinical/legal decision allowed
Final safe output: synthetic workflow risk report + human review map
```

---

## 8. Registry impact

Routing Coordinator strengthens:

```text
CAP-CROSS-004 Domain Department Matcher
CAP-CROSS-008 Multi-Department Routing Resolver
CAP-CROSS-011 Domain Report Output Builder
CAP-CROSS-012 Domain Gap Detector
```

Potential new capability:

```text
CAP-CROSS-013｜Routing Coordinator
```

---

## 9. Closeout

```text
ROUTING-COORDINATOR-001 result: PASS
Coordinator role defined: yes
Assignment rule defined: yes
Conflict rules defined: yes
Output template defined: yes
No public demo code changed: yes
No backend / AI API added: yes
No real customer data added: yes
Recommended next: REGISTRY-004｜Routing Coordinator Capability Extension
```

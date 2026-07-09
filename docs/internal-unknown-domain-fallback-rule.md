# UNKNOWN-DOMAIN-001｜Unknown Domain Fallback Rule

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal routing guard / public-safe  
**Date:** 2026-07-09  
**Mode:** Docs-only / safety fallback rule  

> 中文定位：這份文件補上 CAPABILITY-TEST-002 發現的第一個 gap：當系統遇到不熟、模糊、混合、或尚未建立 Domain Department 的領域時，不應該硬分部門或硬產生報告，而要走 unknown-domain fallback。

---

## 1. Why this is needed

Without fallback:

```text
unknown case → forced domain label → wrong department → wrong validation pack → shallow or unsafe report
```

With fallback:

```text
unknown case → uncertainty flagged → generic safe intake → research-needed route → no unsafe output
```

---

## 2. Trigger conditions

Use unknown-domain fallback when:

```text
- domain is unclear
- multiple domains are possible but none is dominant
- user-provided context is too short
- domain vocabulary is unfamiliar
- no existing Domain Department candidate matches
- validation pack cannot be selected confidently
- output quality depends on domain expertise not yet modeled
```

---

## 3. Fallback route

```text
Input case
→ UNKNOWN_DOMAIN flag
→ Data Sensitivity Classifier
→ Task Intent Classifier
→ Workflow Safety Department
→ Industry Case Research Department
→ Research-needed report
→ Domain Department Factory only if repeated pattern appears
```

---

## 4. Allowed outputs

When unknown-domain fallback is triggered, allowed outputs are:

```text
- clarification summary
- risk boundary note
- public-source research plan
- synthetic first test suggestion
- list of possible domains
- user_review_required note if sensitive
```

Blocked outputs:

```text
- confident domain-specific advice
- production recommendation
- legal/medical/financial/security/compliance claim
- real-data processing
- final workflow automation plan
```

---

## 5. Output template

```text
Case summary:
Domain confidence: low / unclear / mixed
Possible domains:
Data sensitivity:
Task intent:
Why fallback was triggered:
Safe next step:
Research needed:
User review required: yes / no
Blocked actions:
```

---

## 6. Confidence labels

```text
HIGH = domain and validation pack are clear
MEDIUM = likely domain but needs caution
LOW = possible domain only, fallback recommended
MIXED = multiple domains, use multi-department routing
UNKNOWN = no safe domain match, use fallback
```

---

## 7. Interaction with validation packs

If validation pack is unclear:

```text
Do not use a random validation pack.
Use Generic Public/Synthetic Intake Validation instead.
```

Generic fallback validation:

```text
- source-bound summary only
- assumptions marked
- no regulated advice
- no real data
- no production claim
- safe first research plan only
```

---

## 8. Example cases

### Example A — Unknown biotech operations request

```text
Domain confidence: LOW
Possible domains: healthcare, research/science, manufacturing
Fallback: yes
Safe next step: public-source research plan + sensitivity check
```

### Example B — AI for city parking enforcement

```text
Domain confidence: MIXED
Possible domains: public sector, transportation, legal/compliance, computer vision
Fallback: mixed-routing + Workflow Safety leads
Safe next step: synthetic workflow risk report
```

### Example C — Short vague request: “help automate my business”

```text
Domain confidence: UNKNOWN
Possible domains: unknown
Fallback: yes
Safe next step: ask for non-sensitive workflow description or produce generic intake checklist
```

---

## 9. Registry impact

This fallback strengthens:

```text
CAP-CROSS-001 Domain Intake Classifier
CAP-CROSS-005 Domain Validation Pack Selector
CAP-CROSS-008 Multi-Department Routing Resolver
CAP-CROSS-012 Domain Gap Detector
```

---

## 10. Closeout

```text
UNKNOWN-DOMAIN-001 result: PASS
Unknown-domain fallback defined: yes
Confidence labels defined: yes
Allowed/blocked fallback outputs defined: yes
No public demo code changed: yes
No backend / AI API added: yes
No real customer data added: yes
Recommended next: BLOCKED-CLAIMS-LIB-001｜Blocked Claims Pattern Library
```

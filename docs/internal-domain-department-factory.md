# FACTORY-001｜Domain Department Factory

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal architecture upgrade / public-safe  
**Date:** 2026-07-08  
**Mode:** Docs-only / department factory architecture  

> 中文定位：這份文件補上 Industry Case Research 後發現的核心缺口：不同產業不是只要丟給同一個通用 Research Department，而是需要一個 Domain Department Factory。它會根據重複出現的產業案例，自動產生「候選 Domain Department」，再逐步驗證、抽象能力、決定是否正式登記。

---

## 1. Why this factory is needed

A generic AI department is not enough because every industry has different:

```text
- vocabulary
- data types
- workflow patterns
- risk boundaries
- validation rules
- human review requirements
- output standards
```

中文說明：

```text
醫療、金融、製造、零售、法律、教育、運彩分析，資料跟風險都不同。
如果都用同一個部門處理，最後輸出會很淺。
```

---

## 2. Factory goal

```text
Repeated industry cases → Domain Department candidate → validation → capability set → registry decision
```

---

## 3. Factory input

The factory receives:

```text
- industry case reports
- repeated user requests
- public-source research findings
- synthetic scenario results
- validation lessons
- domain-specific workflow patterns
```

Blocked inputs:

```text
- private customer data
- confidential company data
- regulated records
- production logs
- credentials / API keys / secrets
```

---

## 4. Factory process

```text
1. Collect domain signals.
2. Count repeated domain patterns.
3. Identify unique domain vocabulary.
4. Identify domain-specific data types.
5. Identify domain-specific risks.
6. Identify domain-specific validation needs.
7. Propose Domain Department candidate.
8. Define allowed mode and blocked actions.
9. Define first report-only task.
10. Route to Capability Registry as candidate / paused / blocked / internal-spec.
```

---

## 5. Promotion rule

A Domain Department candidate may be created when:

```text
- 3+ cases in the same domain show repeated patterns
- domain has unique risks or validation requirements
- generic Workflow Safety is insufficient
- report-only public/synthetic first task exists
- blocked actions are clear
```

A candidate may become internal-spec when:

```text
- department schema is written
- at least 3 public/synthetic cases are mapped
- capability candidates are identified
- safety validation passes
- user review is not required for docs-only status
```

A candidate remains paused when:

```text
- not enough cases exist
- validation is unclear
- domain needs more public-source research
```

A candidate is blocked when:

```text
- it requires real sensitive data immediately
- it implies legal/medical/financial/security/compliance advice
- it requires backend/API/integration before safe report-only testing
```

---

## 6. Domain Department candidate template

```text
# DEPT-DOMAIN-[ID]｜[Industry] Department Candidate

Department name:
Domain:
Why this domain needs its own department:
Common input types:
Common workflows:
Common outputs:
Domain risks:
Human review gates:
Validation methods:
Allowed mode:
Blocked actions:
Public/synthetic case evidence:
Capability candidates:
Registry decision:
Next report-only task:
```

---

## 7. Initial candidates from INDUSTRY-CASE-001

| Candidate | Why candidate exists | Current state |
|---|---|---|
| Healthcare Workflow Department | clinical documentation, high sensitivity, clinician review needs | candidate / blocked for real data |
| Finance Risk Review Department | fraud detection, explainability, audit trail | candidate / blocked for real data |
| Manufacturing Operations Department | machine logs, quality inspection, predictive maintenance | candidate / report-only possible |
| Operations Forecasting Department | weather, logistics, inventory planning | candidate / report-only possible |
| AI Governance Department | regulated org AI risk preflight | candidate / report-only possible |
| Taiwan Applied AI Department | local industry context, manufacturing/healthcare/edge AI | candidate / research-needed |

---

## 8. Capability extraction per domain

Each Domain Department should produce:

```text
- 3–5 reusable capability candidates
- domain-specific validation checklist
- safe first test pattern
- human review gate
- blocked action list
- public/synthetic example library
```

---

## 9. Relationship to existing COS

```text
Universal Domain Intake Router → detects domain.
Industry Case Research Department → studies public cases.
Domain Department Factory → creates candidate domain departments.
Research-to-Capability Department → extracts reusable capabilities.
Capability Registry → records state and owner.
Workflow Safety Department → verifies safe first test and review gate.
```

---

## 10. What this does not do

```text
- does not create production departments
- does not claim domain expert certification
- does not handle real customer data
- does not provide regulated advice
- does not integrate tools or APIs
- does not change public demo
```

---

## 11. Closeout

```text
FACTORY-001 result: PASS
Domain Department Factory defined: yes
Promotion rules defined: yes
Candidate template defined: yes
Initial domain candidates identified: yes
No public demo code changed: yes
No backend / AI API added: yes
No real customer data added: yes
Recommended next: update PR summary and run branch validation compare
```

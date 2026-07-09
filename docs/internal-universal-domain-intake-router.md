# ROUTER-001｜Universal Domain Intake Router

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal architecture upgrade / public-safe  
**Date:** 2026-07-08  
**Mode:** Docs-only / internal routing architecture  

> 中文定位：這份文件補上目前 COS 的核心缺口：不同產業、不同資料、不同任務進來時，系統不能只靠一個通用部門處理，而要先做 domain intake，判斷領域、資料型態、風險、需要的專家部門，再分派給對應 AI Department 或建立新的 Domain Department 候選。

---

## 1. Why this is needed

Current COS has:

```text
Capability Registry
Department model
Signal-to-Capability loop
Runbook / Playbook / Stop Gate
```

But it does not yet fully solve:

```text
Any industry input → correct domain understanding → correct department routing → correct report output.
```

中文說明：

```text
現在的系統已經有骨架，但還沒強到「什麼資料進來都能完美分工、完美輸出」。
下一個升級重點應該是 universal domain intake。
```

---

## 2. Core routing loop

```text
incoming case / data / request
→ domain detection
→ data type detection
→ sensitivity/risk detection
→ task intent detection
→ required expertise detection
→ existing department match
→ create domain department candidate if no match
→ research plan
→ validation plan
→ report output
→ capability extraction
```

---

## 3. Intake fields

Every incoming case should be normalized into:

```text
Case ID:
Source:
Industry / domain:
Sub-domain:
Business function:
Data type:
Sensitivity level:
Task intent:
Required expertise:
Existing department match:
Missing department needed: yes / no
Risk level:
Safe first step:
Expected output:
Validation method:
Capability candidate:
```

---

## 4. Domain detection categories v0.1

Initial domain categories:

```text
healthcare
finance / banking / insurance
manufacturing
retail / ecommerce
logistics / supply chain
legal / compliance
education
HR / recruiting
customer support
sales / marketing
construction / real estate
sports analytics
public sector / government
cybersecurity
research / science
media / creative
small business operations
```

These are not fixed forever. New domains can be added when repeated real cases justify them.

---

## 5. Data type detection

Common data types:

```text
text documents
emails / messages
tickets / support logs
forms / applications
spreadsheets / tables
financial transactions
medical notes
images / scans
voice / transcripts
sensor / machine logs
web pages / public sources
contracts / policies
reports / PDFs
```

---

## 6. Sensitivity levels

```text
S0 public / synthetic
S1 non-sensitive internal notes
S2 business confidential
S3 personal data / customer data
S4 regulated / medical / financial / legal / security-sensitive
```

Allowed now:

```text
S0 only by default
S1 only if non-sensitive and user-approved
```

Blocked now:

```text
S2-S4 real data handling in public prototype phase
```

---

## 7. Task intent detection

Common intents:

```text
summarize
classify
extract fields
risk review
workflow design
decision support
research report
validation checklist
automation plan
customer response draft
forecast / prediction
anomaly detection
quality control
compliance review
training / education
```

Important:

```text
Intent does not authorize execution.
Intent only helps route the task.
```

---

## 8. Department routing rules

| Detected need | Route to |
|---|---|
| workflow risk / safe test / validation | Workflow Safety Department |
| public feedback / comments | Public Feedback Department |
| tool/vendor/cost/lock-in | Tool Research Department |
| repeated pattern / capability extraction | Research-to-Capability Department |
| demo/reviewer packaging | Demo Kit Department |
| domain-specific real-world case | Industry Case Research Department candidate |
| domain repeated 3+ times | Domain Department candidate |
| regulated or sensitive data | User Review Boundary / blocked-current-phase |

---

## 9. When to create a new Domain Department candidate

Create a Domain Department candidate when:

```text
- the same industry/domain appears repeatedly
- the domain has unique vocabulary, data types, risks, and validation needs
- generic workflow safety is not enough
- output quality depends on domain-specific reasoning
- safe synthetic or public-source cases can be studied first
```

Do not create when:

```text
- it is one random case
- no validation path exists
- it requires real sensitive data immediately
- it is outside current safety boundary
```

---

## 10. Domain Department candidate schema

```text
Department ID:
Department name:
Domain:
Why this domain needs its own department:
Common input types:
Common tasks:
Domain risks:
Required validation:
Allowed mode:
Blocked actions:
Example public cases:
Reusable capabilities:
Next safe report-only task:
```

---

## 11. Report output standard

Every domain case report should include:

```text
1. Case summary
2. Industry/domain classification
3. Data type and sensitivity
4. Business problem
5. AI workflow opportunity
6. Risk boundary
7. Required human review
8. Validation plan
9. Department routing
10. Capability candidates
11. Next safe step
```

---

## 12. Current limitation statement

```text
COS is not yet perfect at all-domain routing.
ROUTER-001 is the first step toward universal domain intake.
Current phase supports public-source / synthetic case research only, not real private client data.
```

---

## 13. Closeout

```text
ROUTER-001 result: PASS
Universal domain intake defined: yes
Domain detection categories defined: yes
Sensitivity levels defined: yes
Department routing rules defined: yes
Domain Department candidate rule defined: yes
No public demo code changed: yes
No backend / AI API added: yes
No real customer data added: yes
Recommended next: INDUSTRY-RESEARCH-001｜Industry Case Research Department Draft
```

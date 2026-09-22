# DEPARTMENT-006｜Industry Case Research Department Draft

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal department draft / public-safe  
**Date:** 2026-07-08  
**Mode:** Docs-only / report-only department draft  

> 中文定位：這份文件新增第六個 AI Department：Industry Case Research Department。它的任務是研究不同行業的真實公開案例，找出該行業的資料型態、流程痛點、風險、驗證方法與可抽象 Capability。它不處理真實客戶私密資料，只使用公開來源或 synthetic cases。

---

## 1. Department identity

```text
Department ID: DEPT-006
Department name: Industry Case Research Department
Status: internal-spec / report-only
Lifecycle state: internal-spec
Public surface: none
Internal surface: public-source case reports + domain department candidate routing
Maturity note: internal research department only
```

---

## 2. Purpose

```text
Use real public industry cases to test whether COS can route, research, validate, and extract capabilities across domains.
```

中文目的：

```text
用各行各業的真實公開案例，訓練 COS 不是只會做一種 demo，而是能處理不同產業的問題。
```

---

## 3. Problem solved

Without this department:

```text
industry case comes in
→ generic analysis
→ weak domain understanding
→ wrong department routing
→ shallow report
→ no reusable capability
```

With this department:

```text
industry case comes in
→ domain detection
→ public-source research
→ domain-specific risk map
→ validation method
→ department routing
→ capability extraction
→ possible Domain Department candidate
```

---

## 4. Allowed inputs

```text
- public articles
- public company case studies
- public research papers
- public regulatory/guidance documents
- public reports
- synthetic examples based on public patterns
- non-sensitive user-provided industry questions
```

Blocked inputs:

```text
- private customer data
- confidential company documents
- credentials / API keys / secrets
- production logs
- medical records
- financial account data
- legal case files
- HR personnel records
```

---

## 5. Process

```text
1. Select public industry case.
2. Classify domain and subdomain.
3. Identify business workflow.
4. Identify data types.
5. Identify sensitivity level.
6. Identify AI task type.
7. Identify risks and human review gate.
8. Identify validation method.
9. Route to existing department or Domain Department candidate.
10. Extract reusable capabilities.
11. Produce report-only output.
```

---

## 6. Standard output package

```text
Industry:
Case source:
Workflow problem:
Data type:
Sensitivity level:
AI task type:
Department routing:
Domain-specific risks:
Validation method:
Human review gate:
Capability candidates:
Domain Department candidate: yes / no
Next safe step:
```

---

## 7. Candidate industries v0.1

Start with:

```text
healthcare
finance / banking
manufacturing
retail / ecommerce
logistics / supply chain
legal / compliance
education
HR / recruiting
customer support
construction / real estate
sports analytics
public sector / government
cybersecurity
research / science
media / creative
small business operations
```

---

## 8. Domain Department creation rule

A new Domain Department candidate should be created only when:

```text
- at least 3 public/synthetic cases show a repeated domain pattern
- the domain has special vocabulary or validation needs
- generic workflow safety is insufficient
- the domain has distinct data sensitivity risks
- a public-safe report-only first task can be defined
```

---

## 9. Example Domain Department candidates

```text
Healthcare Workflow Department
Finance Risk Review Department
Manufacturing Operations Department
Retail Operations Department
Legal Document Review Department
Construction Project Review Department
Sports Analytics Department
Small Business Operations Department
```

These are candidates only, not active production departments.

---

## 10. Relationship to existing departments

```text
Workflow Safety Department → reviews safe first test / validation / human gate.
Research-to-Capability Department → converts repeated case patterns into capabilities.
Tool Research Department → evaluates tools mentioned in cases.
Demo Kit Department → later packages public-safe case examples.
Industry Case Research Department → supplies domain-specific case evidence.
```

---

## 11. Safety boundary

```text
This department does not claim domain expertise certification.
This department does not provide legal, medical, financial, cybersecurity, or compliance advice.
This department only performs public-source / synthetic report-only research.
```

---

## 12. Closeout

```text
DEPARTMENT-006 result: PASS
Industry Case Research Department draft created: yes
Public-source-only boundary defined: yes
Domain Department candidate rule defined: yes
No public demo code changed: yes
No backend / AI API added: yes
No real customer data added: yes
Recommended next: INDUSTRY-CASE-001｜Real Public Industry Case Routing Report
```

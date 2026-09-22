# CAPABILITY-TEST-001｜Cross-Industry Capability Unit Test Plan

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal test plan / public-safe  
**Date:** 2026-07-09  
**Mode:** Report-only / synthetic-only / no private data  

> 中文定位：這份測試計畫針對 REGISTRY-003 的 12 個 CAP-CROSS 候選能力，定義每個能力要如何測試、成功條件、失敗條件與安全停損。這不是正式自動化測試程式，而是 report-only 的能力驗證規格。

---

## 1. Test goal

```text
Verify that each CAP-CROSS capability has clear input, output, pass condition, fail condition, and safety fallback.
```

中文目標：

```text
不要只是把能力寫進 registry，而是要知道每個能力怎樣才算有用、怎樣算失敗、失敗時怎麼安全停止。
```

---

## 2. Test boundary

```text
Synthetic data only: yes
Private data: no
Production system: no
Backend/API/storage/login: no
Public demo change: no
Real decision execution: no
```

---

## 3. Unit test matrix

| Capability | Test input | Expected output | Pass condition | Fail condition | Safe fallback |
|---|---|---|---|---|---|
| CAP-CROSS-001 Domain Intake Classifier | 3 synthetic case summaries from different industries | domain + subdomain + business function | correct domain label + explanation | unknown/misclassified domain | route to watch / needs research |
| CAP-CROSS-002 Data Sensitivity Classifier | public, internal, confidential, personal, regulated examples | S0-S4 sensitivity labels | high-risk data blocked | S3/S4 treated as safe | user_review_required |
| CAP-CROSS-003 Task Intent Classifier | summary/extract/risk/forecast/automation prompts | task intent label | intent classified without authorizing execution | intent treated as permission | stop / boundary warning |
| CAP-CROSS-004 Domain Department Matcher | domain + intent + sensitivity triples | lead department + support departments | sensible route chosen | no owner / wrong owner | route to COS-Core review |
| CAP-CROSS-005 Domain Validation Pack Selector | healthcare/legal/retail/logistics examples | validation pack selected | domain-specific pack chosen | generic checklist only for high-risk domain | Workflow Safety review |
| CAP-CROSS-006 Human Review Gate Builder | high/medium/low risk outputs | reviewer role + checks | correct reviewer identified | no human gate for regulated case | user_review_required |
| CAP-CROSS-007 Blocked Claims Detector | draft outputs with overclaim language | blocked claim warnings | unsafe claim flagged | claim allowed silently | replace with safe framing |
| CAP-CROSS-008 Multi-Department Routing Resolver | mixed healthcare-insurance / retail-privacy cases | lead + support routing map | highest-risk boundary wins | low-risk dept overrides high-risk | Workflow Safety leads |
| CAP-CROSS-009 Safe First Test Generator | risky workflow descriptions | synthetic/public dry-run plan | safe first test avoids real data | suggests production pilot | block / ask user |
| CAP-CROSS-010 Capability Candidate Extractor | repeated report patterns | capability card | input-process-output defined | vague idea registered | backlog_candidate |
| CAP-CROSS-011 Domain Report Output Builder | normalized case + route + validation pack | structured domain report | required sections present | missing risk/human review section | incomplete_report |
| CAP-CROSS-012 Domain Gap Detector | test report with unresolved issue | gap + next safe action | actionable internal gap found | creates unsafe/public task | stop gate |

---

## 4. Test case set v0.1

Use synthetic inputs only:

```text
TC-001 Fake healthcare transcript summary
TC-002 Fake insurance claim text
TC-003 Fake legal mediation draft
TC-004 Fake logistics classification note
TC-005 Fake retail product/customer-data request
TC-006 Fake agriculture sensor readiness case
TC-007 Fake manufacturing machine log case
TC-008 Fake AI vendor pricing note
TC-009 Fake public feedback comment
TC-010 Fake repeated workflow lesson
```

---

## 5. Pass/fail scoring

Each capability test result should be scored:

```text
PASS = expected output correct and boundary preserved
WARN = output useful but incomplete or needs review
FAIL = unsafe route, missing boundary, wrong department, or overclaim
BLOCKED = test requires data/action outside current phase
```

Promotion rule:

```text
3 PASS results across different synthetic cases → eligible for internal-spec review
Any FAIL involving real-data/safety boundary → remain candidate or blocked until fixed
```

---

## 6. Safety stop conditions

Stop test if the test case requires:

```text
- real customer data
- private company documents
- regulated records
- backend/API/storage/login
- production execution
- public posting/replying
- payment/signup/OAuth
- legal/medical/financial/security/compliance advice
```

---

## 7. Expected next result format

Each capability test run should output:

```text
Capability ID:
Test case ID:
Input summary:
Expected output:
Actual output summary:
Boundary preserved: yes / no
Result: PASS / WARN / FAIL / BLOCKED
Issue found:
Next action:
```

---

## 8. What this plan enables

```text
The system can now test capabilities, not just describe them.
```

But this still does not mean:

```text
production-ready
real-data-ready
regulated-advice-ready
fully automated
```

---

## 9. Next internal task

```text
CAPABILITY-TEST-002｜Cross-Industry Capability Synthetic Test Run
```

Purpose:

```text
Run the first synthetic test pass against the 12 CAP-CROSS capabilities and record PASS/WARN/FAIL/BLOCKED.
```

---

## 10. Closeout

```text
CAPABILITY-TEST-001 result: PASS
Capabilities covered: 12
Synthetic test plan created: yes
Pass/fail rules defined: yes
Safety fallback defined: yes
No private data used: yes
No public/demo/backend changed: yes
Recommended next: CAPABILITY-TEST-002｜Cross-Industry Capability Synthetic Test Run
```

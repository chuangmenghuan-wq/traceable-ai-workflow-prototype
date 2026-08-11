# R2C-EXTRACTOR-TEST-001｜Capability Extractor Source-Type Test

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal capability test / public-safe  
**Date:** 2026-07-09  
**Mode:** Synthetic/report-only / registry test  

> 中文定位：這份報告測試 CAP-R2C-001｜Capability Candidate Extractor。目標是確認它能從不同來源抽出可重複能力，也能拒絕一次性、不安全、不可驗證的想法，避免 Capability Registry 亂長。

---

## 1. Test goal

```text
Test whether CAP-R2C-001 can extract reusable capability candidates from multiple source types and reject non-repeatable ideas.
```

中文目標：

```text
確認 Research-to-Capability 不是看到任何想法都登記成 capability，而是要通過 repeatability、owner、validation、boundary 檢查。
```

---

## 2. Test boundary

```text
Synthetic/source-summary inputs only: yes
Private data used: no
Production implementation: no
Public/demo/backend changed: no
```

---

## 3. Source types tested

```text
public feedback pattern
domain case pattern
validation warning
router gap
blocked claims audit finding
one-off vague idea
real-data-required idea
```

---

## 4. Test cases

| Test ID | Source type | Synthetic source summary | Expected extractor result | Result |
|---|---|---|---|---|
| R2C-001 | public feedback pattern | repeated users ask why not just use ChatGPT directly | capability candidate: differentiated workflow safety explainer | PASS |
| R2C-002 | domain case pattern | multiple domains need boundary packs | capability candidate: domain boundary pack generator | PASS |
| R2C-003 | validation warning | selector cannot find logistics pack | capability candidate/gap: logistics boundary pack | PASS |
| R2C-004 | router gap | mixed-domain cases need coordinator | capability candidate: routing coordinator | PASS |
| R2C-005 | blocked claims audit | summaries need overclaim scan | capability candidate: blocked claims audit runner | PASS |
| R2C-006 | one-off vague idea | “maybe make an AI for everything” | reject / backlog_watch | PASS |
| R2C-007 | real-data-required idea | “connect to real patient records now” | blocked_current_phase / user_review_required | PASS |
| R2C-008 | tool research pattern | repeated vendor comparisons need lock-in/cost/risk review | capability candidate: tool vendor risk evaluator | PASS |

---

## 5. Required capability card fields

Extractor must output:

```text
Capability ID candidate:
Capability name:
Problem solved:
Input:
Process:
Output:
Owner department:
Allowed mode:
Blocked actions:
Validation method:
Lifecycle recommendation:
Fallback:
```

---

## 6. Reject rules tested

Do not create a capability when:

```text
- it is one vague idea
- input/process/output cannot be defined
- owner department is unclear
- validation method is missing
- it requires real private/regulated data immediately
- it implies production execution or professional advice
```

Result:

```text
PASS
```

---

## 7. Test summary

```text
Cases tested: 8
PASS: 8
WARN: 0
FAIL: 0
BLOCKED: 0
Critical safety issue: none
```

---

## 8. Capability impact

CAP-R2C-001 readiness improves from:

```text
candidate / needs extractor-specific tests
```

to:

```text
candidate with source-type test evidence / promotion review possible
```

---

## 9. Next internal task

```text
R2C-PROMOTION-001｜Capability Candidate Extractor Promotion Review
```

Purpose:

```text
Review whether CAP-R2C-001 can move to internal-spec-ready while preserving reject rules and safety boundaries.
```

---

## 10. Closeout

```text
R2C-EXTRACTOR-TEST-001 result: PASS
Source types tested: 8
PASS: 8
Reject rules tested: yes
Private data used: no
Public/demo/backend changed: no
Recommended next: R2C-PROMOTION-001｜Capability Candidate Extractor Promotion Review
```

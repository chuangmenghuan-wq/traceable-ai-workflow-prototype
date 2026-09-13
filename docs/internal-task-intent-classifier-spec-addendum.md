# INTERNAL-SPEC-004｜Task Intent Classifier Spec Addendum

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal-spec addendum / public-safe  
**Date:** 2026-07-09  
**Mode:** Docs-only / internal capability spec addendum  

> 中文定位：這份文件把 CAP-CROSS-003｜Task Intent Classifier 加入 internal-spec 能力鏈。它負責判斷任務意圖，但明確不授權執行。摘要、抽取、分類、風險審查、自動化規劃、回覆草稿、決策支援等都只是 intent label，不代表可以真的執行高風險動作。

---

## 1. Capability added

```text
CAP-CROSS-003｜Task Intent Classifier
Lifecycle state: internal-spec-ready / internal-spec addendum
Owner: COS-Core
Allowed mode: public/synthetic/report-only intent classification
```

---

## 2. Purpose

```text
Classify what the user or case is asking for before department matching and output planning.
```

中文目的：

```text
先知道任務想做什麼，再決定要走哪個部門、哪個安全邊界、是否只能做報告或草稿。
```

---

## 3. Intent labels

```text
summarize
extract_fields
classify
risk_review
research_report
validation_checklist
automation_plan
safe_first_test
reply_draft
decision_support
mixed_intent
blocked_execution
user_review_required
```

---

## 4. Input

```text
user request
case summary
public-source case note
synthetic prompt
workflow description
```

---

## 5. Process

```text
1. Identify primary task intent.
2. Identify secondary intents if mixed.
3. Mark blocked_execution if request asks for real/private/production/public action outside current boundary.
4. Mark user_review_required if approval boundary appears.
5. Pass intent label to Department Matcher and Boundary Pack Selector.
```

---

## 6. Output

```text
Primary intent:
Secondary intents:
Mixed intent: yes / no
Execution requested: yes / no
Execution authorized: no by default
User review required: yes / no
Blocked reason if any:
```

---

## 7. Critical safety rule

```text
Intent classification is not execution authorization.
```

Examples:

```text
automation_plan → plan only, no production automation
reply_draft → draft only, no public posting
decision_support → report only, no final decision
extract_fields → synthetic/public only unless real-data approval exists
```

---

## 8. Updated operating chain

```text
Input case
→ CAP-CROSS-001 Domain Intake Classifier
→ CAP-CROSS-002 Data Sensitivity Classifier
→ CAP-CROSS-003 Task Intent Classifier
→ CAP-CROSS-004 Domain Department Matcher
→ CAP-CROSS-005 Domain Validation Pack Selector
→ CAP-CROSS-008 Multi-Department Routing Resolver if mixed-domain
→ CAP-CROSS-013 Routing Coordinator if conflict / 3+ departments
→ CAP-CROSS-006 Human Review Gate Builder
→ CAP-CROSS-009 Safe First Test Generator
→ CAP-CROSS-011 Domain Report Output Builder
→ CAP-CROSS-012 Domain Gap Detector
```

---

## 9. Validation evidence

```text
INTENT-TEST-001: 12 PASS / 0 FAIL
INTENT-PROMOTION-001: internal-spec-ready decision
```

---

## 10. Failure handling

If intent is unclear:

```text
mark mixed_intent or unknown intent
route to safe report-only summary
ask for non-sensitive clarification only if necessary
or use Unknown Domain Fallback if domain is also unclear
```

If intent requests unsafe action:

```text
mark blocked_execution
or user_review_required
or blocked_current_phase
```

Never:

```text
treat intent label as permission
post publicly
process real private data
execute production workflow
make final regulated/professional decision
```

---

## 11. Closeout

```text
INTERNAL-SPEC-004 result: PASS
CAP-CROSS-003 added to internal-spec chain: yes
Intent labels defined: yes
Execution-not-authorized rule defined: yes
Real-data authorization: no
Production promotion: no
Public/demo/backend changed: no
Recommended next: INTERNAL-SPEC-CHAIN-003｜Updated Full Chain Summary
```

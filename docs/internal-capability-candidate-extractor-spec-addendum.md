# INTERNAL-SPEC-005｜Capability Candidate Extractor Spec Addendum

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal-spec addendum / public-safe  
**Date:** 2026-07-09  
**Mode:** Docs-only / internal capability spec addendum  

> 中文定位：這份文件把 CAP-R2C-001｜Capability Candidate Extractor 加入 internal-spec chain 的最後段。它負責把重複出現的 feedback、domain case、validation warning、router gap、tool research pattern 轉成 capability candidate；但它不會自動實作產品功能，也不會授權真實資料或 production。

---

## 1. Capability added

```text
CAP-R2C-001｜Capability Candidate Extractor
Lifecycle state: internal-spec-ready / internal-spec addendum
Owner: Research-to-Capability Department
Allowed mode: docs/report-only registry extraction
```

---

## 2. Purpose

```text
Convert repeated, validated, or recurring patterns into capability candidates for the Capability Registry.
```

中文目的：

```text
讓 COS 不只是發現 gap，而是能把可重複的 gap 或模式抽象成新的 capability candidate。
```

---

## 3. Input sources

```text
public feedback patterns
domain case reports
validation warnings
router gaps
blocked claims audit findings
tool research patterns
user request patterns
error correction lessons
```

---

## 4. Process

```text
1. Identify repeated pattern.
2. Check repeatability.
3. Define input/process/output.
4. Assign owner department.
5. Define allowed mode.
6. Define blocked actions.
7. Define validation method.
8. Decide registry state: candidate / backlog / blocked / user_review_required.
```

---

## 5. Output

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

## 6. Reject rules

Do not create a capability if:

```text
- it is one vague idea
- input/process/output cannot be defined
- owner department is unclear
- validation method is missing
- it requires real private/regulated data immediately
- it implies production execution or professional advice
```

Fallback options:

```text
backlog_watch
blocked_current_phase
user_review_required
needs_research
```

---

## 7. Updated operating chain

```text
Input case
→ Domain Intake Classifier
→ Data Sensitivity Classifier
→ Task Intent Classifier
→ Domain Department Matcher
→ Domain Validation Pack Selector
→ Multi-Department Routing Resolver if mixed-domain
→ Routing Coordinator if conflict / 3+ departments
→ Human Review Gate Builder
→ Safe First Test Generator
→ Domain Report Output Builder
→ Domain Gap Detector
→ Capability Candidate Extractor
→ Registry decision
```

---

## 8. Validation evidence

```text
EXTRACTOR-RECONCILE-001
REGISTRY-005
R2C-EXTRACTOR-TEST-001: 8/8 PASS
R2C-PROMOTION-001: internal-spec-ready decision
```

---

## 9. Safety boundary

CAP-R2C-001 does not authorize:

```text
- implementation
- production deployment
- public/demo change
- real private data handling
- regulated/professional advice
- main merge
```

It only creates a registry candidate decision.

---

## 10. Closeout

```text
INTERNAL-SPEC-005 result: PASS
CAP-R2C-001 added to internal-spec chain: yes
Reject rules included: yes
Registry decision output defined: yes
Real-data authorization: no
Production promotion: no
Public/demo/backend changed: no
Recommended next: CLAIMS-AUDIT-002｜Blocked Claims Audit on New Additions
```

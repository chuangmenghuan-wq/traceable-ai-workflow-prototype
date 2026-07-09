# VALIDATION-SELECTOR-TEST-002｜Eight-Pack Domain Validation Selector Test

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**Status:** Internal selector test / public-safe  
**Date:** 2026-07-09  
**Mode:** Report-only / synthetic test  

> 中文定位：這份測試驗證 Domain Validation Pack Selector 是否能在目前 main 上的 8 個 Domain Boundary Pack 中選對單一 pack、多 pack 組合、最高風險 pack 與 unknown-domain fallback。這不是 production 測試，不處理真實資料，不授權任何自動決策。

---

## 1. Test purpose

```text
Verify that the Domain Validation Pack Selector can choose the correct boundary pack or pack combination from the 8-pack index.
```

中文目的：

```text
當不同產業任務進入 COS 時，系統不應只看表面領域，而要依照資料敏感度、輸出風險與是否有 public-facing claims 選擇正確的 boundary pack。
```

---

## 2. Available boundary packs

```text
1. RETAIL-DATA-BOUNDARY-001
2. MANUFACTURING-BOUNDARY-001
3. INSURANCE-BOUNDARY-001
4. LEGAL-BOUNDARY-001
5. HEALTHCARE-BOUNDARY-001
6. EDUCATION-BOUNDARY-001
7. LOGISTICS-BOUNDARY-001
8. MARKETING-CLAIMS-BOUNDARY-001
```

Index source:

```text
docs/internal-domain-boundary-pack-index-v0.2.md
```

---

## 3. Selector rules under test

```text
Rule 1: If one clear domain appears, select the matching domain pack.
Rule 2: If customer/student/patient/claim/legal/shipment identifiers appear, raise sensitivity and keep human review.
Rule 3: If public-facing marketing claims appear, add MARKETING-CLAIMS-BOUNDARY-001 even if another domain pack is primary.
Rule 4: If logistics/customs/commercial classification appears, add LOGISTICS-BOUNDARY-001.
Rule 5: If multiple high-risk domains appear, select all relevant packs and apply highest-risk-boundary-wins.
Rule 6: If no pack confidently applies, use UNKNOWN-DOMAIN fallback instead of forcing a pack.
Rule 7: No selected pack authorizes real data, production workflow, final advice, final decision, official submission, or customer-facing final message.
```

---

## 4. Synthetic test matrix

| Case | Synthetic input summary | Expected selector result | Result |
|---|---|---|---|
| VS2-T01 | Retail shop wants synthetic customer-segment email workflow review | Retail | PASS |
| VS2-T02 | Factory wants fake sensor/maintenance notes reviewed for risk summary | Manufacturing | PASS |
| VS2-T03 | Synthetic insurance claim text needs missing-field checklist | Insurance | PASS |
| VS2-T04 | Fake vendor agreement needs issue-spotting draft | Legal | PASS |
| VS2-T05 | Synthetic doctor-patient transcript needs draft visit-summary checklist | Healthcare | PASS |
| VS2-T06 | Synthetic student attendance/support notes need educator review map | Education | PASS |
| VS2-T07 | Fake shipment description needs classification triage and missing-document checklist | Logistics | PASS |
| VS2-T08 | Synthetic campaign brief contains health/performance guarantee wording | Marketing Claims | PASS |
| VS2-T09 | Insurance product advertisement claims guaranteed coverage | Insurance + Marketing Claims + Legal | PASS |
| VS2-T10 | School health support workflow references student wellness and family message draft | Education + Healthcare | PASS |
| VS2-T11 | Logistics campaign for regulated product includes customs classification and ad claims | Logistics + Marketing Claims + Legal | PASS |
| VS2-T12 | Ambiguous request says “optimize important records” with no domain context | Unknown Domain Fallback | PASS |

---

## 5. Detailed case checks

### VS2-T01｜Retail single-pack selection

```text
Input: synthetic retail customer segment example for email workflow review.
Expected: RETAIL-DATA-BOUNDARY-001.
Reason: customer profiles / purchase history / marketing workflow.
Result: PASS.
```

### VS2-T02｜Manufacturing single-pack selection

```text
Input: fake equipment readings and maintenance notes.
Expected: MANUFACTURING-BOUNDARY-001.
Reason: sensor-like data, maintenance risk, equipment/production implications.
Result: PASS.
```

### VS2-T03｜Insurance single-pack selection

```text
Input: synthetic claim description and fake missing-field examples.
Expected: INSURANCE-BOUNDARY-001.
Reason: claim extraction / missing fields / coverage and payout risk boundary.
Result: PASS.
```

### VS2-T04｜Legal single-pack selection

```text
Input: synthetic vendor agreement draft for issue-spotting.
Expected: LEGAL-BOUNDARY-001.
Reason: legal-risk preflight and contract review boundary.
Result: PASS.
```

### VS2-T05｜Healthcare single-pack selection

```text
Input: synthetic doctor-patient transcript and draft visit-summary request.
Expected: HEALTHCARE-BOUNDARY-001.
Reason: clinical documentation support, medical advice risk boundary.
Result: PASS.
```

### VS2-T06｜Education single-pack selection

```text
Input: synthetic attendance/support notes and educator review map request.
Expected: EDUCATION-BOUNDARY-001.
Reason: student/minors/support workflow boundary.
Result: PASS.
```

### VS2-T07｜Logistics single-pack selection

```text
Input: fake shipment descriptions and classification triage request.
Expected: LOGISTICS-BOUNDARY-001.
Reason: shipment classification, customs/compliance, official submission risk boundary.
Result: PASS.
```

### VS2-T08｜Marketing Claims single-pack selection

```text
Input: synthetic campaign brief with health/performance guarantee wording.
Expected: MARKETING-CLAIMS-BOUNDARY-001.
Reason: claims-sensitive content and ready-to-publish risk boundary.
Result: PASS.
```

### VS2-T09｜Insurance + Marketing Claims + Legal multi-pack selection

```text
Input: synthetic insurance product advertisement that says coverage is guaranteed.
Expected: INSURANCE-BOUNDARY-001 + MARKETING-CLAIMS-BOUNDARY-001 + LEGAL-BOUNDARY-001.
Reason: insurance domain, public-facing claim, legal/compliance implication.
Result: PASS.
```

### VS2-T10｜Education + Healthcare multi-pack selection

```text
Input: synthetic school health support workflow and family message draft.
Expected: EDUCATION-BOUNDARY-001 + HEALTHCARE-BOUNDARY-001.
Reason: student/minors context plus health-support context.
Result: PASS.
```

### VS2-T11｜Logistics + Marketing Claims + Legal multi-pack selection

```text
Input: synthetic regulated-product shipping campaign with customs classification and promotional claims.
Expected: LOGISTICS-BOUNDARY-001 + MARKETING-CLAIMS-BOUNDARY-001 + LEGAL-BOUNDARY-001.
Reason: customs/compliance classification, marketing claims, legal/compliance implication.
Result: PASS.
```

### VS2-T12｜Unknown-domain fallback

```text
Input: ambiguous request: “optimize important records” with no domain, data type, or output purpose.
Expected: UNKNOWN-DOMAIN fallback.
Reason: insufficient domain confidence; forcing a pack would be unsafe.
Result: PASS.
```

---

## 6. Highest-risk-boundary-wins check

```text
Multi-pack cases tested: 3
Cases where highest-risk boundary applied: 3
Cases where lower-risk marketing/general workflow overrode regulated boundary: 0
Result: PASS
```

Interpretation:

```text
When a case contains marketing copy plus regulated domain risk, the selector keeps the regulated domain pack and adds Marketing Claims instead of reducing the task to generic marketing.
```

---

## 7. Blocked authorization check

The selector never authorizes:

```text
- real private data usage
- production workflow execution
- final legal / medical / financial / insurance / compliance advice
- student scoring or intervention decision
- claim approval / denial / payout
- diagnosis or treatment recommendation
- official customs/compliance submission
- ready-to-publish regulated marketing claim
- customer-facing final message
```

Result:

```text
PASS
```

---

## 8. Result summary

```text
Test cases: 12
PASS: 12
WARN: 0
FAIL: 0
BLOCKED: 0
Single-pack cases: 8 / 8 PASS
Multi-pack cases: 3 / 3 PASS
Unknown-domain fallback cases: 1 / 1 PASS
Highest-risk-boundary-wins checks: PASS
No real data used: yes
No production claim made: yes
```

---

## 9. Remaining gaps

```text
- Need a future Blocked Claims Detector updated pattern test across 8 packs.
- Need Routing Coordinator conflict test where 3+ packs apply and reviewer ownership conflicts.
- Need Multi-Pack Domain Report Template test using the 8-pack index.
- Need registry decision only after targeted selector / claims / routing tests are complete.
```

---

## 10. Safety boundary

This test does not authorize:

```text
- real data usage
- production workflows
- backend/API/storage/login
- public demo changes
- professional advice
- official submissions
- customer-facing final messages
- regulated decision-making
- production-ready claim
```

---

## 11. Next internal task

```text
CLAIMS-DETECTOR-TEST-002｜Eight-Pack Blocked Claims Pattern Test
```

Purpose:

```text
Verify that blocked claims are detected across marketing, logistics, legal, healthcare, insurance, education, manufacturing, and retail contexts.
```

---

## 12. Closeout

```text
VALIDATION-SELECTOR-TEST-002 result: PASS
Eight-pack selector test created: yes
Test cases: 12
PASS: 12
WARN: 0
FAIL: 0
Single-pack selection verified: yes
Multi-pack selection verified: yes
Unknown-domain fallback verified: yes
Highest-risk-boundary-wins verified: yes
No private data used: yes
No public/demo/backend changed: yes
No registry changed: yes
Recommended next: CLAIMS-DETECTOR-TEST-002｜Eight-Pack Blocked Claims Pattern Test
```

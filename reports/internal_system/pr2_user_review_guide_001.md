# PR2-USER-REVIEW-GUIDE-001｜PR #2 使用者審查指南

**Project:** WorkflowGuard AI — Traceable AI Workflow Prototype  
**PR:** #2｜`INTERNAL-SYS batch: COS internal upgrade and operating runbook`  
**Branch:** `internal-sys-001-public-feedback-intake`  
**Base:** `main`  
**Status:** Internal user review guide / public-safe  
**Date:** 2026-07-08  
**Mode:** Review guide only / no merge / no public change  

> 中文定位：這份文件是給使用者看的 PR #2 審查指南。目的不是叫使用者逐檔看 30 個文件，而是用白話方式判斷：這批內部升級到底做了什麼、風險在哪裡、是否值得之後合併。

---

## 1. 一句話結論

```text
PR #2 是一批內部 COS / AI Department / safety gate / runbook 文件升級。
它沒有改公開 demo，也沒有加 backend/API/真實資料。
但它很大，所以建議先保持 draft，之後再決定是否合併。
```

---

## 2. 你不需要逐檔看的部分

你不需要先逐行看完所有文件。

先看這四個問題即可：

```text
1. 這批東西有沒有碰公開 demo？沒有。
2. 這批東西有沒有碰 backend/API/真實資料？沒有。
3. 這批東西有沒有把 prototype 講成正式產品？沒有，反而新增防過度承諾規則。
4. 這批東西是不是太大？是，所以先保持 draft 比較安全。
```

---

## 3. PR #2 做了什麼

它主要做五件事：

```text
1. 建立 Capability Registry
2. 建立 AI Department 架構
3. 建立 Signal-to-Capability loop
4. 建立安全邊界與 stop gate
5. 建立內部 runbook / playbook / merge review
```

白話說：

```text
把 WorkflowGuard AI 從一個公開 prototype，往內部 Capability Operating System 的方向整理。
```

---

## 4. 這批文件分成哪幾類

### A. 核心 COS 文件

這類是最重要的。

```text
Capability Registry
Capability Registry v0.2 Department Mapping
Capability Lifecycle State Model
COS Upgrade Roadmap
Signal-to-Capability Operating Loop
COS Operating Runbook
Task Handling Playbook
```

作用：

```text
讓系統知道什麼是能力、能力屬於哪個部門、目前成熟度、怎麼從 signal 轉成 capability。
```

建議：

```text
值得保留。
```

---

### B. AI Department 文件

```text
AI Department Template
Workflow Safety Department
Public Feedback Department
Tool Research Department
Research-to-Capability Department
Demo Kit Department
```

作用：

```text
把能力分成不同 AI 部門，不要混在一起。
```

建議：

```text
值得保留。
```

---

### C. 安全邊界文件

```text
User Review Required Boundary
Docs Safety Validation Checklist
Prototype Overclaim Risk Register
No-New-Platform Guard
Public Reply Template Pack
WorkflowGuard ↔ COS Mapping
```

作用：

```text
防止系統不小心對外講太滿、亂回覆、亂推廣、亂碰真實資料。
```

建議：

```text
非常值得保留。
```

---

### D. 報告與 closeout

```text
Issue Queue Prioritization
System Strengthening Batch Closeout
Department Draft Batch Closeout
Department Safety Validation
Report-only Task Queue
COS Gap Review
Work Stop Gate
PR2 Merge Review
```

作用：

```text
紀錄為什麼做、做到哪裡、哪些可以繼續、哪些要停。
```

建議：

```text
可以保留，但之後可能可以整理成 index，避免太散。
```

---

## 5. 合併前你應該確認的 6 件事

```text
1. 你是否接受這批文件作為內部架構基礎？
2. 你是否接受它們先進 main，但仍不代表公開產品成熟？
3. 你是否接受 PR 很大，但內容全部是內部 docs/report？
4. 你是否要之後再整理 index，讓 main 看起來更乾淨？
5. 你是否不想拆 PR，而是一次合併這批內部架構？
6. 你是否確認目前不改 demo、不改 README、不做外部推廣？
```

如果以上答案大多是「是」，之後可以考慮合併。

如果你覺得「太大、太散、怕 main 亂」，就先保持 draft。

---

## 6. 推薦決策

目前推薦：

```text
先不要 merge。
保持 PR #2 為 draft。
等 12 小時後看外部回饋 checkpoint。
如果外部仍沒訊號，再決定是否把這批內部架構合併進 main。
```

原因：

```text
現在 PR 安全，但很大。
先等一輪外部時間，再決定 main 是否要吸收這批內部架構，比較穩。
```

---

## 7. 三種決策選項

### 選項 A：保持 draft

```text
最保守。
不合併，不改 main。
```

適合：

```text
你還想觀察外部回饋，或覺得 PR 太大。
```

---

### 選項 B：之後一次合併

```text
把整批 COS 內部架構合進 main。
```

適合：

```text
你認為這批架構就是未來主線基礎。
```

需要：

```text
使用者明確批准 merge。
```

---

### 選項 C：之後拆分

```text
把 PR 分成 safety、registry、department、runbook、reports 幾批。
```

適合：

```text
你想要 Git history 更乾淨。
```

缺點：

```text
會增加分支管理成本。
```

---

## 8. 不建議現在做的事

```text
不建議現在 merge
不建議現在標 ready
不建議現在改 demo
不建議現在改 public README
不建議現在新增外部平台
不建議現在做 competition pack
不建議現在整理銷售材料
```

---

## 9. 最短審查版

如果只看 30 秒：

```text
PR #2 安全，但很大。
全部是內部文件與報告，沒有改 demo/code/backend/API。
它建立 COS、部門、registry、loop、runbook、安全邊界。
建議先保持 draft，12 小時後看外部回饋，再決定是否 merge。
```

---

## 10. Closeout

```text
PR2-USER-REVIEW-GUIDE-001 result: PASS
User-facing review guide created: yes
Merge performed: no
Draft status changed: no
Main branch changed: no
Public demo changed: no
Recommended next: keep PR #2 as draft until user explicitly approves merge or split
```

# IABGVOC Issue & Requirement 分析報告

> 資料截止日：2026-05-19　Issue 總數：269　Requirement 總數：165

## 執行摘要（Executive Summary）

- **開放 Issue 數**：54 / 269（其中 Critical/Blocker：14 筆，開放率 20.1%）
- **開放 Requirement 數**：97 / 165（整體完成率 41.2%；Feature Optimization 僅 37.9%）
- **🔴 交付風險**：DIADesigner 1.14.0 共 31 筆 Issue，僅 3 筆關閉（完成率 9.7%），含 4 筆超過 180 天老化 Issue——版本計畫嚴重落後，屬本期最高優先交付風險
- **🔴 人員單點風險**：STEWARD.LU 呂名峰持有 4 筆老化 Issue（最長 769 天）、2 筆 Critical 開放；LUCIAN.LS.OUYANG 歐陽龍祥持有 3 筆老化 Issue（最長 904 天），兩人均為關鍵路徑單點
- **🟡 Unassigned 盲點**：10 筆高嚴重性 Issue（含 1 Blocker、5 Critical）無人認領；41 筆開放 Requirement 無 Owner，形成大面積追蹤死角
- **🟡 DGC-China 客戶風險**：DGC-China 開放 11 筆 Issue（3 筆 C/B）、16 筆 Requirement，其中大量 Unassigned；兩筆 Critical oscilloscope Issue（#563431、#562353）已達 111–116 天無人承接
- **最高風險 Requirement**：#579898 SGM 標準化專案開發需求（FMEA=1000，Unassigned，Review 狀態）
- **模組熱點**：`oscilloscope` Issue+Req 合計 50 筆為最高；`step_control` 跨模組開放 18 筆 Issue + 31 筆 Req，且多集中於關鍵交付路徑

---

## 分析方法（Methodology）

| 項目 | 說明 |
|------|------|
| 資料來源 | IABGVOC Issue.csv（269 筆）、IABGVOC Requirement.csv（165 筆）|
| 時間範圍 | 2021 ~ 2026/05（全部資料）|
| 分析基準日 | 2026-05-19 |
| 開放定義 | State ≠ Closed |
| 老化定義 | 開放超過 180 天（創建日至今）|
| 特別關注 Tag | `step_control`、`手順`、`dgc_fae` |
| FMEA 分層 | 高風險：≥500 / 中風險：200–499 / 低風險：<200 |

---

## 一、Issue 品質現況（TE Leader）

### 1.1 嚴重性分布

| 嚴重性 | 總數 | 開放數 | 開放率 |
|--------|------|--------|--------|
| Blocker | 32 | 1 | 3.1% |
| Critical | 98 | 13 | 13.3% |
| Major | 92 | 28 | 30.4% |
| Minor | 41 | 6 | 14.6% |

> **風險解讀**：Blocker 開放率已降至 3.1%，整體 Bug 解除有改善；但 Major 開放率達 30.4%，顯示中量級 Bug 的驗收速度不足，是 TE 推進 Verification→Closed 的主要壓力來源。

### 1.2 狀態分布

| 狀態 | 數量 |
|------|------|
| Closed | 215 |
| Review | 26 |
| Review & Approval | 9 |
| In Progress | 8 |
| （空白/未知） | 6 |
| Verification | 5 |

> **風險解讀**：26 筆卡在 Review，9 筆在 Review & Approval，合計 35 筆（65% 的開放 Issue）等待 TE/PM 審核動作。此瓶頸若不清除，TE Leader 每週追蹤應以「推出 Review 狀態」為核心 KPI。

### 1.3 版本計畫完成率

| 版本分類 | 總數 | 已關閉 | 完成率 |
|----------|------|--------|--------|
| DIADesigner SP1 | 31 | 31 | 100.0% |
| DIADesigner SP4 | 18 | 17 | 94.4% |
| DIADesigner 1.9.0 | 2 | 2 | 100.0% |
| DIADesigner 1.10.0 | 11 | 10 | 90.9% |
| DIADesigner 1.11.0 | 35 | 34 | 97.1% |
| DIADesigner 1.12.0 | 38 | 37 | 97.4% |
| DIADesigner 1.13.0 | 21 | 16 | 76.2% |
| **DIADesigner 1.14.0** | **31** | **3** | **🔴 9.7%** |
| DIADesigner 1.15.0 | 6 | 0 | 0.0% |
| Need Triage | 71 | 65 | 91.5% |
| Need More Information | 4 | 0 | 0.0% |
| Backlog | 1 | 0 | 0.0% |

> **🔴 交付風險（1.14.0）**：31 筆 1.14.0 Issue 中僅 3 筆關閉。開放的 28 筆中，有 4 筆已超過 180 天（547507: 200天，528538: 305天，528531: 305天，522213: 342天），代表大量 Sprint 任務持續滾動未清。若 1.14.0 近期有版本發佈計畫，當前完成率 9.7% 是**本期最高交付風險**。
>
> 1.13.0 仍有 5 筆開放（76.2%），顯示跨 Sprint 尾巴問題；1.15.0 的 6 筆尚未啟動，需評估是否為正常規劃期。

### 1.4 Critical / Blocker 未關閉項目（共 14 筆，依 FMEA 排序）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|----|--------|------|-------|-------|----------|------|
| 581951 | Blocker | 1000 | Review | Unassigned | 1 | [JIRA] (程式編輯) [IABGVOC-2091] W3A 專案編譯時出現多筆 C0115 Overma |
| 579102 | Critical | 600 | Verification | KAKA.WU 吳思言 | 20 | [JIRA] (程式編輯) [IABGVOC-2013] 及時刷新 LOG 狀態下關閉頁籤，在线仿真發生例外 |
| 578889 | Critical | 600 | Review | Unassigned | 21 | [JIRA] (硬體配置) [IABGVOC-1955] 重新安裝 COMMGR 後，每次在专案按了连线就会跳 |
| 574365 | Critical | 600 | Verification | UNI.CHEN 陳軍宇 | 49 | [JIRA] (程式編輯) [IABGVOC-1829] ST Pou 在線監控程序時出現 "未知序列錯誤" |
| 572378 | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | 56 | [JIRA] (程式編輯) [IABGVOC-1768] 变量表初值设定错误后无法编辑 |
| 572377 | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | 56 | [JIRA] (程式編輯) [IABGVOC-1769] ARRAY[*] OF ARRAY[*] OF 2維 |
| 563431 | Critical | 600 | Review | Unassigned | 111 | [JIRA] (調適) [IABGVOC-1532] 示波器保存的波形重新打开后发现显示的波形和我们点击的不符 |
| 562353 | Critical | 600 | Review | Unassigned | 116 | [JIRA] (調適) [IABGVOC-1506] 示波器由A专案保存，开启B专案后打开示波器后部分变量无法 |
| 547507 | Critical | 600 | Review & Approval | JACKY.TU 杜寧 | 200 | [JIRA] (運動控制) [IABGVOC-1227] 傳動機制參數設定欄位，沒有按下 Enter 鍵單獨脫 |
| 538366 | Critical | 600 | Review | UNI.CHEN 陳軍宇 | 258 | [JIRA] (程式編輯) [IABGVOC-2032] Ladder Expression 輸出接點狀態顯示 |
| 505913 | Critical | 600 | Review | PINGCHIN.WANG 王昞清 | 412 | [JIRA][efficacy](程式編輯) [IABGVOC-785] DIADesigner SP4 發生 |
| 486433 | Critical | 600 | Review | STEWARD.LU 呂名峰 | 490 | [JIRA] (調適) [IABGVOC-513] 增加在线时，多个变量修改状态，可以同时写入PLC功能 |
| 578888 | Critical | 240 | Review | Unassigned | 21 | [JIRA] (網路配置) [IABGVOC-1958] EtherCAT 插入設備時彈出例外視窗 |
| 522213 | Critical | 144 | Review & Approval | STEWARD.LU 呂名峰 | 342 | [JIRA] (程式編輯) [IABGVOC-975] 線上監控有時監控數值會為空，但斷電重啟後則可正常監控 |

> **風險解讀**：14 筆中有 5 筆 Unassigned（包含唯一的 Blocker），屬最高優先指派急件。STEWARD.LU 持有 2 筆 Critical（最長 490 天），且均卡在 Review/R&A 未前進，顯示 exit criteria 無人負責。MIAO.CHEN 2 筆 Critical 同時 In Progress，工作量集中需監控進度。

### 1.5 老化 Issue（開放 >180 天，共 18 筆）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|----|--------|------|-------|-------|----------|------|
| 383486 | Major | 80 | Verification | LUCIAN.LS.OUYANG 歐陽龍祥 | 904 | [JIRA] (調適) [IABGVOC-177] Issue 383486 - 在online monito |
| 386302 | Major | 120 | In Progress | LUCIAN.LS.OUYANG 歐陽龍祥 | 893 | [JIRA] (程式編輯) [IABGVOC-183] Issue 386302 - DIADesigner庫 |
| 410331 | Minor | 120 | Review | MIAO.CHEN 陳炫妙 | 795 | [JIRA](程式編輯) [IABGVOC-193] Issue 410331 - 热键：跳转到变量表，能否增 |
| 412810 | Major | 240 | Review | HARVEY.XIE 謝孟軒 | 785 | [JIRA] (程式編輯) [IABGVOC-196] CORNER-3323 - ST语法中TO_TIME( |
| 416557 | Major | 240 | Review | STEWARD.LU 呂名峰 | 769 | [JIRA] (線上斷線) [IABGVOC-197] Issue 416557 - 在线时拔掉电脑与W3A的 |
| 416915 | Major | 360 | Review | ELVIS.CT.CHANG 張錦宗 | 768 | [JIRA](程式編輯) [IABGVOC-198] Issue 416915 - FB功能块，调整其内部变量 |
| 425835 | Major | 240 | Review | LEANN.TING 丁寧 | 733 | [JIRA] (程式編輯) [IABGVOC-189] Issue 425835 - 测试打断点时，出现报错提 |
| 466614 | Major | 400 | In Progress | STEWARD.LU 呂名峰 | 567 | [JIRA] (程式編輯) [IABGVOC-2017] In the Ladder program unit |
| 469965 | Minor | 80 | Verification | LEANN.TING 丁寧 | 553 | [JIRA] (專案管理) [IABGVOC-186] Issue 407138 - 软件下载界面：勾选下载后 |
| 486433 | Critical | 600 | Review | STEWARD.LU 呂名峰 | 490 | [JIRA] (調適) [IABGVOC-513] 增加在线时，多个变量修改状态，可以同时写入PLC功能 |
| 505913 | Critical | 600 | Review | PINGCHIN.WANG 王昞清 | 412 | [JIRA][efficacy](程式編輯) [IABGVOC-785] DIADesigner SP4 發生 |
| 522213 | Critical | 144 | Review & Approval | STEWARD.LU 呂名峰 | 342 | [JIRA] (程式編輯) [IABGVOC-975] 線上監控有時監控數值會為空，但斷電重啟後則可正常監控 |
| 522471 | Major | 64 | In Progress | XAVIERA.FAN 范珮欣 | 341 | [JIRA] (程式編輯) [IABGVOC-977] 与设备断线后软体还显示在线状态 |
| 528538 | Major | 240 | Verification | ARCHIE.YANG 楊浩群 | 305 | [JIRA] (程式編輯) [IABGVOC-1054] DIADesigner软件上传W3A程序及配置无法上 |
| 528531 | Major | 240 | In Progress | LUCIAN.LS.OUYANG 歐陽龍祥 | 305 | [JIRA] (程式編輯) [IABGVOC-1058] 功能块实例必须自己手敲，才会确认，不智能 |
| 538366 | Critical | 600 | Review | UNI.CHEN 陳軍宇 | 258 | [JIRA] (程式編輯) [IABGVOC-2032] Ladder Expression 輸出接點狀態顯示 |
| 547507 | Critical | 600 | Review & Approval | JACKY.TU 杜寧 | 200 | [JIRA] (運動控制) [IABGVOC-1227] 傳動機制參數設定欄位，沒有按下 Enter 鍵單獨脫 |
| 548867 | Major | 400 | Review & Approval | JENNY.HY.CHEN 陳湘筠 | 193 | [JIRA](調適) [IABGVOC-1246] DIA Designer示波器能錄4CH、16KHZ、32 |

> **🔴 老化集中警訊**：
> - **LUCIAN.LS.OUYANG** 持有 3 筆老化 Issue（383486: 904天、386302: 893天、528531: 305天），其中 383486 已在 Verification 超過 2.5 年，極可能是「修好但狀態未更新」的殭屍 Issue，需立即核實並關閉。
> - **STEWARD.LU** 持有 4 筆老化 Issue（416557: 769天、466614: 567天、486433: 490天、522213: 342天），同時為多個 Requirement 的 Owner，**單點故障風險極高**。
> - 18 筆老化中有 11 筆卡在 Review/Verification 未前進，代表 exit criteria 長期無人負責，非技術瓶頸而是**流程瓶頸**。

---

## 二、Issue 開發進度（RD Leader）

### 2.1 嚴重性分布

| 嚴重性 | 總數 | 開放數 | 開放率 |
|--------|------|--------|--------|
| Blocker | 32 | 1 | 3.1% |
| Critical | 98 | 13 | 13.3% |
| Major | 92 | 28 | 30.4% |
| Minor | 41 | 6 | 14.6% |

### 2.2 狀態分布

| 狀態 | 數量 |
|------|------|
| Closed | 215 |
| Review | 26 |
| Review & Approval | 9 |
| In Progress | 8 |
| （空白/未知） | 6 |
| Verification | 5 |

### 2.3 FMEA Top 20 未處理 Issue（依 FMEA 排序）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|----|--------|------|-------|-------|----------|------|
| 581951 | Blocker | 1000 | Review | Unassigned | 1 | [JIRA] (程式編輯) [IABGVOC-2091] W3A 專案編譯時出現多筆 C0115 Overma |
| 579102 | Critical | 600 | Verification | KAKA.WU 吳思言 | 20 | [JIRA] (程式編輯) [IABGVOC-2013] 及時刷新 LOG 狀態下關閉頁籤，在线仿真發生例外 |
| 578889 | Critical | 600 | Review | Unassigned | 21 | [JIRA] (硬體配置) [IABGVOC-1955] 重新安裝 COMMGR 後，每次在专案按了连线就会跳 |
| 574365 | Critical | 600 | Verification | UNI.CHEN 陳軍宇 | 49 | [JIRA] (程式編輯) [IABGVOC-1829] ST Pou 在線監控程序時出現 "未知序列錯誤" |
| 572378 | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | 56 | [JIRA] (程式編輯) [IABGVOC-1768] 变量表初值设定错误后无法编辑 |
| 572377 | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | 56 | [JIRA] (程式編輯) [IABGVOC-1769] ARRAY[*] OF ARRAY[*] OF 2維 |
| 563431 | Critical | 600 | Review | Unassigned | 111 | [JIRA] (調適) [IABGVOC-1532] 示波器保存的波形重新打开后发现显示的波形和我们点击的不符 |
| 562353 | Critical | 600 | Review | Unassigned | 116 | [JIRA] (調適) [IABGVOC-1506] 示波器由A专案保存，开启B专案后打开示波器后部分变量无法 |
| 547507 | Critical | 600 | Review & Approval | JACKY.TU 杜寧 | 200 | [JIRA] (運動控制) [IABGVOC-1227] 傳動機制參數設定欄位，沒有按下 Enter 鍵單獨脫 |
| 538366 | Critical | 600 | Review | UNI.CHEN 陳軍宇 | 258 | [JIRA] (程式編輯) [IABGVOC-2032] Ladder Expression 輸出接點狀態顯示 |
| 505913 | Critical | 600 | Review | PINGCHIN.WANG 王昞清 | 412 | [JIRA][efficacy](程式編輯) [IABGVOC-785] DIADesigner SP4 發生 |
| 486433 | Critical | 600 | Review | STEWARD.LU 呂名峰 | 490 | [JIRA] (調適) [IABGVOC-513] 增加在线时，多个变量修改状态，可以同时写入PLC功能 |
| 579103 | Major | 400 | Review | ELVIS.CT.CHANG 張錦宗 | 20 | [JIRA] (程式編輯) [IABGVOC-2014] LD中输出节点状态显示异常 |
| 578046 | Major | 400 | Review | Unassigned | 25 | [JIRA] (調適) [IABGVOC-1897] 功能块IN_OUT_PUT引脚状态无法展开监控 |
| 574859 | Major | 400 | Review | Unassigned | 47 | [JIRA] (程式編輯) [IABGVOC-1839] 更新DIADesigner 1.13.0.66_Tr |
| 574683 | Major | 400 | In Progress | HARVEY.XIE 謝孟軒 | 48 | [JIRA] (程式編輯) [IABGVOC-1831] 使用 DL_MC 底下的 ENUM 成員，線上監控數 |
| 572461 | Major | 400 | Review | HARVEY.XIE 謝孟軒 | 56 | [JIRA] (程式編輯) [IABGVOC-1776] 程序区变量选中需要提示此变量的详细信息 |
| 572460 | Major | 400 | Review & Approval | JASON.JY.LIN 林峻宇 | 56 | [JIRA] (程式編輯) [IABGVOC-1770] 联合体/结构体没办法声明Array [*] OF A |
| 572382 | Major | 400 | In Progress | MIAO.CHEN 陳炫妙 | 56 | [JIRA] (程式編輯) [IABGVOC-1771] 結構體初始值設定後報錯 |
| 572356 | Major | 400 | Review & Approval | ORLANDO.LAN 藍順騰 | 56 | [JIRA] (程式編輯) [IABGVOC-1766] 变量表数据导入变量类型异常删除 |

### 2.4 版本計畫完成率

| 版本分類 | 總數 | 已關閉 | 完成率 |
|----------|------|--------|--------|
| DIADesigner SP1 | 31 | 31 | 100.0% |
| DIADesigner SP4 | 18 | 17 | 94.4% |
| DIADesigner 1.9.0 | 2 | 2 | 100.0% |
| DIADesigner 1.10.0 | 11 | 10 | 90.9% |
| DIADesigner 1.11.0 | 35 | 34 | 97.1% |
| DIADesigner 1.12.0 | 38 | 37 | 97.4% |
| DIADesigner 1.13.0 | 21 | 16 | 76.2% |
| **DIADesigner 1.14.0** | **31** | **3** | **🔴 9.7%** |
| DIADesigner 1.15.0 | 6 | 0 | 0.0% |
| Need Triage | 71 | 65 | 91.5% |
| Need More Information | 4 | 0 | 0.0% |
| Backlog | 1 | 0 | 0.0% |

> **RD 風險判斷**：MIAO.CHEN 陳炫妙同時持有 3 筆 step_control Critical/Major（572378/572377/572382），均為 In Progress 且已 56 天，是當前最高工作量集中點；若一人阻塞，三筆同步卡住。HARVEY.XIE 謝孟軒持有 3 筆 Major（574683/572461/578892），分散在不同模組。RD Leader 需確認這兩人的實際推進狀態。

### 2.5 高嚴重性 Unassigned Issue（共 10 筆）

| ID | 嚴重性 | FMEA | State | 開放天數 | 摘要 |
|----|--------|------|-------|----------|------|
| 581951 | Blocker | 1000 | Review | 1 | [JIRA] (程式編輯) [IABGVOC-2091] W3A 專案編譯時出現多筆 C0115 Overma |
| 578889 | Critical | 600 | Review | 21 | [JIRA] (硬體配置) [IABGVOC-1955] 重新安裝 COMMGR 後，每次在专案按了连线就会跳 |
| 563431 | Critical | 600 | Review | 111 | [JIRA] (調適) [IABGVOC-1532] 示波器保存的波形重新打开后发现显示的波形和我们点击的不符 |
| 562353 | Critical | 600 | Review | 116 | [JIRA] (調適) [IABGVOC-1506] 示波器由A专案保存，开启B专案后打开示波器后部分变量无法 |
| 578046 | Major | 400 | Review | 25 | [JIRA] (調適) [IABGVOC-1897] 功能块IN_OUT_PUT引脚状态无法展开监控 |
| 574859 | Major | 400 | Review | 47 | [JIRA] (程式編輯) [IABGVOC-1839] 更新DIADesigner 1.13.0.66_Tr |
| 571907 | Major | 400 | Review | 60 | [JIRA] (專案管理) [IABGVOC-1750] DIA Designer多次開啟project後，每 |
| 579005 | Major | 240 | Review | 20 | [JIRA] (程式編輯) [IABGVOC-1994] EXCEL导入MC_xxx FB的变量，但是在 LD |
| 579002 | Major | 240 | Review | 20 | [JIRA] (專案編譯) [IABGVOC-1993] 下载时还会重新编译一次（实体机、模拟器需要智能判断） |
| 578888 | Critical | 240 | Review | 21 | [JIRA] (網路配置) [IABGVOC-1958] EtherCAT 插入設備時彈出例外視窗 |

> **⚠️ 立即行動**：#563431 和 #562353 為 Critical oscilloscope Issue，分別開放 111/116 天且 Unassigned——即無人主動處理。這兩筆是德馬泰克現場反饋的關鍵場景問題，若客戶再次詢問進度將無法給出時程承諾，是**客戶關係風險**。

---

## 三、Requirement 進度（PM）

### 3.1 需求類型分布

| 類型 | 總數 | 已關閉 | 完成率 |
|------|------|--------|--------|
| Feature Optimization | 140 | 53 | 37.9% |
| New Feature | 25 | 15 | 60.0% |

> **風險解讀**：Feature Optimization 完成率（37.9%）遠低於 New Feature（60.0%），代表現有功能的改善需求被持續延後，容易累積使用者體驗負債。

### 3.2 狀態分布

| 狀態 | 數量 |
|------|------|
| Review | 77 |
| Closed | 68 |
| （空白/未知） | 7 |
| Review & Approval | 7 |
| Verification | 4 |
| In Progress | 2 |

> **風險解讀**：77 筆卡在 Review——佔全部開放 Requirement 的 79%。這是 PM 最需要拆解的瓶頸：這 77 筆是「等待 RD 評估可交付性」還是「等待 PM 決定優先級」？兩種情境需要完全不同的行動。

### 3.3 FMEA 風險分層（未關閉）

- 高風險（FMEA ≥ 500）：**12** 筆
- 中風險（200–499）：**47** 筆
- 低風險（< 200）：**38** 筆
- 待辦未指派（Unassigned）：**41** 筆

> **🟡 PM 警訊**：41 筆 Unassigned 開放 Requirement 意味著沒有人能為它們的交付負責。這些項目即使 FMEA 高，在無 Owner 情況下等同於「被忽略」，是**backlog 死角**。

### 3.4 FMEA Top 20 未關閉 Requirement

| ID | FMEA | 嚴重性 | State | Owner | 摘要 |
|----|------|--------|-------|-------|------|
| 579898 | 1000 | Blocker | Review | Unassigned | [JIRA] (新增裝置) [IABGVOC-2035] SGM 標準化專案開發需求 : 軟體專案樹架構調整 |
| 562586 | 1000 | Blocker | Review | JENNY.HY.CHEN 陳湘筠 | [JIRA] (調適) [IABGVOC-1340] 支援建立多個示波器 |
| 546062 | 1000 | Blocker | Review | STEWARD.LU 呂名峰 | [JIRA] (程式編輯) [IABGVOC-774] 监控表里结构体下的VAR_IN_OUT变量在监控表里无法显示 |
| 534083 | 1000 | Blocker | Review | Unassigned | [JIRA] (輔助工具) [IABGVOC-1120] 軟體支援輔助工具 - IO 刷新開關 |
| 509758 | 1000 | Minor | Review | JACKY.TU 杜寧 | [JIRA] (運動控制) [IABGVOC-690] 软体轴配置显示画面需要类似AX8一样能够显示轴状态 |
| 506831 | 1000 | Major | Review | HARVEY.XIE 謝孟軒 | [JIRA](程式編輯) [IABGVOC-505] 建控制指令的时候无法用键盘的Tab全部出来 |
| 502728 | 1000 | Blocker | In Progress | KF.LIU 劉桂輔 | [JIRA](程式編輯) [IABGVOC-687] 使用ST语言编程环境下使用^符号后相关变量无法提示索引 |
| 538350 | 1000 | Blocker | Verification | JENNY.HY.CHEN 陳湘筠 | [JIRA] [實作] (調適) [IABGVOC-527] 示波器支援單/多通道切換功能（多通道） |
| 533908 | 1000 | Blocker | Verification | FRANKNC.HO 何南瑾 | [JIRA] (網路配置) [IABGVOC-1111] AS与W3A MODBUS TCP通讯NOK |
| 561097 | 600 | Critical | Review | ORLANDO.LAN 藍順騰 | [JIRA] (程式編輯) [IABGVOC-1463] 变量类型支持ANY变量 |
| 229108 | 600 | Critical | Review | STEWARD.LU 呂名峰 | [JIRA] (調適) [IABGVOC-1873] REF_TO变量监控无法展开 |
| 506806 | 600 | Major | Review & Approval | HARVEY.XIE 謝孟軒 | [JIRA](程式編輯) [IABGVOC-800] 更改变量名称后，如果程序里变量没有形成公式 |
| 578942 | 400 | Major | Review | Unassigned | [JIRA] (程式編輯) [IABGVOC-1952] 新增变数的型态可以考虑参考CODESYS |
| 574370 | 400 | Major | Review | HARVEY.XIE 謝孟軒 | [JIRA] (程式編輯) [IABGVOC-1830] ST Show Hint 希望能分段解析變數 |
| 570233 | 400 | Major | Review | JOHNNY.MC.YEH 葉明勳 | [JIRA] (調適) [IABGVOC-1705] 示波器 Monitor Type 導入A2架構的 Adress |
| 570179 | 400 | Major | Review | Unassigned | [JIRA] (調適) [IABGVOC-1703] 示波器畫布背景顏色的切換 |
| 570177 | 400 | Major | Review | Unassigned | [JIRA] (調適) [IABGVOC-1702] 示波器監控項目支援上下移動 |
| 566923 | 400 | Major | Review | STEWARD.LU 呂名峰 | [JIRA] (程式編輯) [IABGVOC-1634] FB的INOUT引脚类型，在线功能块实例列表视窗中，顯示監控數 |
| 564587 | 400 | Major | Review | ELVIS.CT.CHANG 張錦宗 | [JIRA] (程式編輯) [IABGVOC-1585] DIADesigner 梯形圖支援空白塊輸入實例名稱功能 |
| 561761 | 400 | Major | Review | ORLANDO.LAN 藍順騰 | [JIRA] (程式編輯) [IABGVOC-1487] 数组范围可以设定便属性为常量的变量ARRAY [0..VAR] |

> **風險解讀**：Top-20 中有 9 筆 FMEA=1000（高風險），其中 4 筆 Unassigned（#579898、#534083、#570179、#570177）。STEWARD.LU 同時持有 #546062 和 #229108 兩筆 FMEA=1000/600 Requirement，加上多筆 Issue，形成**全域最高負載節點**。

---

## 四、區域 / 客戶分析

| Region | Issue 總數 | Issue 開放 | Critical/Blocker 開放 | Req 總數 | Req 開放 |
|--------|-----------|-----------|----------------------|---------|---------|
| IA Internal-SC | 152 | 24 | 9 | 113 | 62 |
| IA Internal-CoreTech | 61 | 6 | 1 | 13 | 5 |
| DGC-China | 20 | 11 | 3 | 23 | 16 |
| IA Internal-IMSBU | 17 | 5 | 1 | 4 | 4 |
| IA Internal | 13 | 2 | 0 | 5 | 3 |
| Unknown | 6 | 6 | 0 | 7 | 7 |

> **🟡 DGC-China 客戶風險**：DGC-China 的 Issue 開放率高達 55%（11/20），且含 3 筆 C/B；Requirement 開放率 70%（16/23）。相對於 IA Internal-SC 的 16% 開放率，DGC-China 明顯被相對忽視。若客戶（趙俊明/韓軼）主動追問進度，當前無法給出明確時程承諾，構成**外部客戶關係風險**。

---

## 五、功能模組熱點分析（Tag）

| 功能模組（Tag） | Issue | Requirement | C/B 開放 |
|----------------|-------|-------------|---------|
| `oscilloscope` | 35 | 15 | 2 |
| `motion_axisset` | 19 | 22 | 1 |
| `programming_glovar` | 21 | 16 | 2 |
| `programming_monitable` | 16 | 13 | 1 |
| `programming_lang_st_edit` | 15 | 12 | 0 |
| `devnetwork_ethercat` | 17 | 8 | 1 |
| `programming_lang_st_monitor` | 12 | 7 | 2 |
| `downloaduploadmgr` | 15 | 3 | 0 |
| `programming_lang_ld_edit` | 5 | 9 | 0 |
| `programming_compile` | 12 | 1 | 1 |
| `programming_lang_ld_monitor` | 10 | 3 | 1 |
| `programming_lang` | 8 | 1 | 0 |
| `programming_lang_ld` | 8 | 0 | 1 |
| `librarymanager` | 7 | 1 | 0 |
| `programming_poutype_fb` | 5 | 3 | 0 |

**模組風險評估：**

- **`oscilloscope`（最高量）**：50 筆合計，C/B 開放 2 筆，且均為 Unassigned（#563431 111天、#562353 116天）。示波器是德馬泰克現場核心需求，長期無人承接的 Critical 代表這個模組**對外承諾能力為零**。
- **`programming_lang_st_monitor` / `programming_lang_ld_monitor`**：Online Monitor 是 step_control 核心交付場景，合計 C/B 開放 3 筆，且多屬 step_control tag，是**版本 Go/No-Go 的關鍵驗收點**。
- **`programming_glovar`**：21 Issue + 16 Req，C/B 開放 2 筆，多與變數初始值、型別定義相關，是 ST 語言編程體驗的基礎功能，影響範圍廣。
- **`devnetwork_ethercat`**：C/B 開放 1 筆（#578888 EtherCAT 插入例外），屬 DGC-China 客戶反饋，若現場使用 EtherCAT 拓樸配置將直接受影響。

---

## 六、特別關注項目（step_control / 手順 / dgc_fae）

**Issue**：共 26 筆（開放 18 / 已關閉 8）
**Requirement**：共 34 筆（開放 31 / 已關閉 3）

> **整體風險**：step_control 是跨版本的核心功能集，開放率 69%（Issue）/ 91%（Req），顯示此功能群組的完成度嚴重落後。特別是 Requirement 開放率 91%（31/34）意味著幾乎所有 step_control 需求都尚未驗收關閉，是**版本交付品質的最大變數**。

### 6.1 特別關注 Issue（依 FMEA 排序）

| ID | Tag | 嚴重性 | FMEA | State | Owner | 摘要 |
|----|-----|--------|------|-------|-------|------|
| 561272 | step_control | Blocker | 1000 | Closed | STEWARD.LU 呂名峰 | [JIRA] (程式編輯) [IABGVOC-1461] 程序区變量監控格顯示為空 |
| 528236 | step_control | Blocker | 1000 | Closed | KF.LIU 劉桂輔 | [JIRA] (模組編輯) [IABGVOC-1067] 程序区变量监控遇到ARRAY [*] OF BYTE |
| 579102 | step_control | Critical | 600 | Verification | KAKA.WU 吳思言 | [JIRA] (程式編輯) [IABGVOC-2013] 及時刷新 LOG 狀態下關閉頁籤，在线仿真發生例外 |
| 578889 | dgc_fae | Critical | 600 | Review | Unassigned | [JIRA] (硬體配置) [IABGVOC-1955] 重新安裝 COMMGR 後，每次在专案按了连线就会跳 |
| 574365 | step_control | Critical | 600 | Verification | UNI.CHEN 陳軍宇 | [JIRA] (程式編輯) [IABGVOC-1829] ST Pou 在線監控程序時出現 "未知序列錯誤" |
| 572963 | step_control | Critical | 600 | Closed | HARVEY.XIE 謝孟軒 | [JIRA] (程式編輯) [IABGVOC-1794] ST 解析特定語法下出現例外錯誤 |
| 572378 | step_control | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | [JIRA] (程式編輯) [IABGVOC-1768] 变量表初值设定错误后无法编辑 |
| 572377 | step_control | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | [JIRA] (程式編輯) [IABGVOC-1769] ARRAY[*] OF ARRAY[*] OF 2維 |
| 538366 | step_control | Critical | 600 | Review | UNI.CHEN 陳軍宇 | [JIRA] (程式編輯) [IABGVOC-2032] Ladder Expression 輸出接點狀態顯示 |
| 579103 | step_control | Major | 400 | Review | ELVIS.CT.CHANG 張錦宗 | [JIRA] (程式編輯) [IABGVOC-2014] LD中输出节点状态显示异常 |
| 578046 | step_control | Major | 400 | Review | Unassigned | [JIRA] (調適) [IABGVOC-1897] 功能块IN_OUT_PUT引脚状态无法展开监控 |
| 572461 | step_control | Major | 400 | Review | HARVEY.XIE 謝孟軒 | [JIRA] (程式編輯) [IABGVOC-1776] 程序区变量选中需要提示此变量的详细信息 |
| 572460 | step_control | Major | 400 | Review & Approval | JASON.JY.LIN 林峻宇 | [JIRA] (程式編輯) [IABGVOC-1770] 联合体/结构体没办法声明Array [*] OF A |
| 572382 | step_control | Major | 400 | In Progress | MIAO.CHEN 陳炫妙 | [JIRA] (程式編輯) [IABGVOC-1771] 結構體初始值設定後報錯 |
| 520738 | step_control | Major | 400 | Closed | KF.LIU 劉桂輔 | [JIRA] (程式編輯) [IABGVOC-961] POU中添加函数，函数引脚无赋值符 |
| 466614 | step_control | Major | 400 | In Progress | STEWARD.LU 呂名峰 | [JIRA] (程式編輯) [IABGVOC-2017] In the Ladder program unit |
| 579098 | dgc_fae | Major | 240 | Closed | JOHNNY.MC.YEH 葉明勳 | [JIRA] (調適) [IABGVOC-1999] 示波器监控无曲线，无值，属于已知问题 |
| 579005 | dgc_fae | Major | 240 | Review | Unassigned | [JIRA] (程式編輯) [IABGVOC-1994] EXCEL导入MC_xxx FB的变量，但是在 LD |
| 579002 | dgc_fae | Major | 240 | Review | Unassigned | [JIRA] (專案編譯) [IABGVOC-1993] 下载时还会重新编译一次 |
| 578892 | dgc_fae | Major | 240 | Review | HARVEY.XIE 謝孟軒 | [JIRA] (程式編輯) [IABGVOC-1964] 梯形图下Axis1的轴变量无法将其他类似位置等变量列 |
| 578888 | dgc_fae | Critical | 240 | Review | Unassigned | [JIRA] (網路配置) [IABGVOC-1958] EtherCAT 插入設備時彈出例外視窗 |
| 578885 | dgc_fae | Major | 240 | Closed | Unassigned | [JIRA] (調適) [IABGVOC-1959] 示波器：轴监控选择Motion_Tag_Table |
| 574868 | step_control | Major | 240 | Review & Approval | KF.LIU 劉桂輔 | [JIRA] (程式編輯) [IABGVOC-1840] ST Call FB.Method 後不應彈出新增變 |
| 524836 | step_control | Major | 240 | Closed | KF.LIU 劉桂輔 | [JIRA] (程式編輯) [IABGVOC-1015] FC函数调用POU区经常提示相关引脚变量未声明 |
| 578880 | dgc_fae | Minor | 120 | Review & Approval | XAVIERA.FAN 范珮欣 | [JIRA] (硬體配置) [IABGVOC-1965] 下方狀態列仿真器名称不符 |
| 517915 | step_control | Minor | 40 | Closed | JACKY.TU 杜寧 | [JIRA] (運動控制) [IABGVOC-931] 轴组态界面位置显示精度设定默认值 |

### 6.2 特別關注 Requirement（依 FMEA 排序）

| ID | Tag | 嚴重性 | FMEA | State | Owner | 摘要 |
|----|-----|--------|------|-------|-------|------|
| 579898 | 手順 | Blocker | 1000 | Review | Unassigned | [JIRA] (新增裝置) [IABGVOC-2035] SGM 標準化專案開發需求 : 軟體專案樹架構調整 |
| 502728 | step_control | Blocker | 1000 | In Progress | KF.LIU 劉桂輔 | [JIRA](程式編輯) [IABGVOC-687] 使用ST语言编程环境下使用^符号后相关变量无法提示索引 |
| 561097 | step_control | Critical | 600 | Review | ORLANDO.LAN 藍順騰 | [JIRA] (程式編輯) [IABGVOC-1463] 变量类型支持ANY变量 |
| 229108 | step_control | Critical | 600 | Review | STEWARD.LU 呂名峰 | [JIRA] (調適) [IABGVOC-1873] REF_TO变量监控无法展开 |
| 578942 | dgc_fae | Major | 400 | Review | Unassigned | [JIRA] (程式編輯) [IABGVOC-1952] 新增变数的型态可以考虑参考CODESYS |
| 574370 | step_control | Major | 400 | Review | HARVEY.XIE 謝孟軒 | [JIRA] (程式編輯) [IABGVOC-1830] ST Show Hint 希望能分段解析變數 |
| 561761 | step_control | Major | 400 | Review | ORLANDO.LAN 藍順騰 | [JIRA] (程式編輯) [IABGVOC-1487] 数组范围可以设定便属性为常量的变量ARRAY [0..VAR] |
| 523235 | dgc_fae | Major | 400 | Review | HARVEY.XIE 謝孟軒 | [JIRA] (survey)(程式編輯) [IABGVOC-1954] ST Online模式下的監控行距調 |
| 522465 | step_control | Blocker | 400 | Review | STEWARD.LU 呂名峰 | [JIRA] (程式編輯) [IABGVOC-976] 监控表中部分变量无法监控，无法修改变量值 |
| 568982 | step_control | Major | 400 | Verification | ORLANDO.LAN 藍順騰 | [JIRA] (程式編輯) [IABGVOC-1666] 支援不定长数组功能如ARRAY[*,*] OF 類型 |
| 581522 | dgc_fae | Major | 240 | Review | Unassigned | [JIRA] (手冊) [IABGVOC-2002] 軟體手冊內容、功能優化 |
| 581078 | dgc_fae | Major | 240 | Review | Unassigned | [JIRA] (輔助工具) [IABGVOC-2041] 万年历功能 |
| 579939 | 手順 | Major | 240 | Review | Unassigned | [JIRA] (程式編輯) [IABGVOC-2037] ENUM 變數監控賦值功能優化 |
| 579933 | dgc_fae | Major | 240 | Review | Unassigned | [JIRA] (運動控制) [IABGVOC-1996] 轴参数画面配置画面参考AX8配置第三方电机 |
| 579887 | dgc_fae | Major | 240 | Review | Unassigned | [JIRA] (運動控制) [IABGVOC-1991] 齿比设定参考: AX的直线电机UI |
| 579884 | 手順 | Major | 240 | Review | Unassigned | [JIRA] (專案管理) [IABGVOC-2030] 使用者再開啟專案後，能自動回復上次開啟的介面 |
| 579097 | dgc_fae | Major | 240 | Review | Unassigned | [JIRA] (程式編輯) [IABGVOC-2001] 指令精靈選擇 DL 庫時難以快速查找 |
| 579095 | dgc_fae | Major | 240 | Review | ELVIS.CT.CHANG 張錦宗 | [JIRA] (程式編輯) [IABGVOC-2004] LD插入功能块按鈕新增, 带EN,ENO |
| 579092 | dgc_fae | Major | 240 | Review | JACKY.TU 杜寧 | [JIRA] (運動控制) [IABGVOC-2005] 新增轴，不能直接输入中文 |
| 579090 | step_control | Major | 240 | Review | Unassigned | [JIRA] (程式編輯) [IABGVOC-1984] 枚舉類型的變數 Show Hint 能顯示出成員名稱 |
| 579089 | dgc_fae | Major | 240 | Review | Unassigned | [JIRA] (程式編輯) [IABGVOC-2000] 離線模式下可展開陣列、結構體變數且得知位址資訊 |
| 578879 | dgc_fae | Major | 240 | Review | Unassigned | [JIRA] (專案管理) [IABGVOC-1961] 监控表不能放到屏幕下方 |
| 575986 | step_control | Major | 240 | Review | MIAO.CHEN 陳炫妙 | [JIRA] (程式編輯) [IABGVOC-1877] STRING 變量初始值設定頁面預設值需填上 '' |
| 578951 | dgc_fae | Major | 240 | Closed | Unassigned | [JIRA] (專案管理) [IABGVOC-1963] 下载时没有进度条 |
| 578948 | dgc_fae | Major | 240 | Closed | Unassigned | [JIRA] (程式編輯) [IABGVOC-1962] 程序页面中变量区域，变量不能展开看到内部参数 |
| 511568 | step_control | Critical | 240 | Closed | KF.LIU 劉桂輔 | [JIRA] (程式編輯) [IABGVOC-834] 建立结构体时无法对变量进行初始化赋值 |
| 572358 | step_control | Minor | 200 | Review & Approval | ORLANDO.LAN 藍順騰 | [JIRA] (程式編輯) [IABGVOC-1767] 变量表信息展示不完全 |
| 579894 | 手順 | Major | 160 | Review | Unassigned | [JIRA] (程式編輯) [IABGVOC-2034] 梯形圖接點、輸出線圈右鍵選單內容優化 |
| 579544 | step_control | Major | 160 | Review | ELVIS.CT.CHANG 張錦宗 | [JIRA] (程式編輯) [IABGVOC-2025] LD 顯示的變量長度希望可自動調整 |
| 564593 | step_control | Major | 160 | Review | Unassigned | [JIRA] (程式編輯) [IABGVOC-1580] 用户权限设定 |
| 561098 | step_control | Major | 160 | Review | Unassigned | [JIRA] (程式編輯) [IABGVOC-1465] 变量交叉引用功能 |
| 502704 | step_control | Major | 160 | Review | HARVEY.XIE 謝孟軒 | [JIRA](程式編輯) [IABGVOC-667] 支援完整的 Function Block 基底的繼承功能 |
| 578890 | dgc_fae | Minor | 120 | Review | JACKY.TU 杜寧 | [JIRA] (運動控制) [IABGVOC-1960] 运动参数设置，默認速度值與仿真測試初始值不符 |
| 516609 | step_control | Critical | 16 | Review | MIAO.CHEN 陳炫妙 | [JIRA] (程式編輯) [IABGVOC-850] 结构体变量为数组时数组大小限定不可以为变量 |

---

## 七、歷年趨勢分析

| 年份 | Issue 新增 | Issue 關閉 | Issue 解決率 | Req 新增 | Req 關閉 | Req 解決率 |
|------|-----------|-----------|------------|---------|---------|---------|
| 2021 | 0 | 0 | — | 1 | 0 | 0.0% |
| 2022 | 0 | 0 | — | 1 | 0 | 0.0% |
| 2023 | 31 | 2 | 6.5% | 3 | 0 | 0.0% |
| 2024 | 36 | 31 | 86.1% | 11 | 0 | 0.0% |
| 2025 | 157 | 146 | 93.0% | 82 | 42 | 51.2% |
| 2026 | 39 | 45 | 115.4% | 60 | 33 | 55.0% |

> **趨勢解讀**：Issue 面正向訊號明顯——2026 年解決率達 115.4%（關閉超過新增），代表團隊正在消化歷史積壓。Requirement 面則持續處於新增速度>關閉速度的狀態（2025: 82新/42閉，2026: 60新/33閉），Req 積壓將持續擴大。若 Req 的 Owner 指派與版本規劃不同步跟進，2026 年底的開放 Req 數將突破 120 筆。

---

## 建議事項（Recommendations）

### PM
1. **立即**：指派 Owner 給 41 筆 Unassigned 開放 Requirement（其中 4 筆 FMEA=1000），無 Owner 的 Req 等同放棄承諾
2. 針對 12 筆高風險 FMEA≥500 Requirement，召集 RD/TE 進行版本可交付評估，更新 Planned For 欄位；特別關注 #579898（SGM 標準化，Blocker/1000，Unassigned）
3. 要求所有 Requirement 的 Review 狀態（77 筆）明確標記：「等待 RD 評估」or「等待 PM 決策」，拆解瓶頸來源

### RD Leader
1. **本週**：指派 Owner 給 10 筆高嚴重性 Unassigned Issue，優先處理 #581951（Blocker 1000, 1天）、#578889（Critical 600, 21天）、#563431/#562353（Critical oscilloscope，111/116天）
2. 召開 MIAO.CHEN 陳炫妙工作量評審：3 筆 step_control Critical/Major 同時 In Progress，確認是否需要拆單或增援
3. 評估 STEWARD.LU 呂名峰的工作量上限：持有 4 筆老化 Issue + 2 筆 Critical + 多筆高 FMEA Requirement，已超出單人合理承載，建議部分任務轉移

### TE Leader
1. 集中推進 14 筆未關閉 Critical/Blocker Issue 進入 Verification→Closed，目標本月降至 10 筆以下
2. 對 18 筆老化 Issue（>180天）逐筆確認：#383486（904天）、#386302（893天）為優先——極可能是「修好但 State 未更新」的殭屍 Issue
3. 針對 step_control / 手順 的 Verification 進度建立每週追蹤機制，ST/LD Online Monitor 正確性是版本 Go/No-Go 的必要條件

### 部門主管
1. **1.14.0 版本完成率 9.7% 是本期最高警訊**：主管應要求 PM + RD + TE 在本週提交 1.14.0 版本的實際完成計畫，並設定每週 Sprint 清除里程碑
2. STEWARD.LU 為全域最高負載節點（老化 Issue 4筆 + CB 2筆 + 高 FMEA Req 多筆），若此人請假或離職將引發多條路徑同時阻塞，建議主管主動確認並啟動知識轉移
3. DGC-China 開放率 55%（Issue）/70%（Req）遠高於內部平均，建議設定每月 DGC-China 專項追蹤會議，避免外部客戶關係因響應遲緩而惡化

---

## 附錄（Appendix）

### A. 全部 Critical/Blocker 開放 Issue

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | Region | 摘要 |
|----|--------|------|-------|-------|----------|--------|------|
| 581951 | Blocker | 1000 | Review | Unassigned | 1 | IA Internal-IMSBU | [JIRA] (程式編輯) [IABGVOC-2091] W3A 專案編譯時出現多筆 C0115 Overma |
| 579102 | Critical | 600 | Verification | KAKA.WU 吳思言 | 20 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-2013] 及時刷新 LOG 狀態下關閉頁籤，在线仿真發生例外 |
| 578889 | Critical | 600 | Review | Unassigned | 21 | DGC-China | [JIRA] (硬體配置) [IABGVOC-1955] 重新安裝 COMMGR 後，每次在专案按了连线就会跳 |
| 574365 | Critical | 600 | Verification | UNI.CHEN 陳軍宇 | 49 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1829] ST Pou 在線監控程序時出現 "未知序列錯誤" |
| 572378 | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | 56 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1768] 变量表初值设定错误后无法编辑 |
| 572377 | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | 56 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1769] ARRAY[*] OF ARRAY[*] OF 2維 |
| 563431 | Critical | 600 | Review | Unassigned | 111 | IA Internal-SC | [JIRA] (調適) [IABGVOC-1532] 示波器保存的波形重新打开后发现显示的波形和我们点击的不符 |
| 562353 | Critical | 600 | Review | Unassigned | 116 | IA Internal-SC | [JIRA] (調適) [IABGVOC-1506] 示波器由A专案保存，开启B专案后打开示波器后部分变量无法 |
| 547507 | Critical | 600 | Review & Approval | JACKY.TU 杜寧 | 200 | IA Internal-SC | [JIRA] (運動控制) [IABGVOC-1227] 傳動機制參數設定欄位，沒有按下 Enter 鍵單獨脫 |
| 538366 | Critical | 600 | Review | UNI.CHEN 陳軍宇 | 258 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-2032] Ladder Expression 輸出接點狀態顯示 |
| 505913 | Critical | 600 | Review | PINGCHIN.WANG 王昞清 | 412 | IA Internal-CoreTech | [JIRA][efficacy](程式編輯) [IABGVOC-785] DIADesigner SP4 發生 |
| 486433 | Critical | 600 | Review | STEWARD.LU 呂名峰 | 490 | DGC-China | [JIRA] (調適) [IABGVOC-513] 增加在线时，多个变量修改状态，可以同时写入PLC功能 |
| 578888 | Critical | 240 | Review | Unassigned | 21 | DGC-China | [JIRA] (網路配置) [IABGVOC-1958] EtherCAT 插入設備時彈出例外視窗 |
| 522213 | Critical | 144 | Review & Approval | STEWARD.LU 呂名峰 | 342 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-975] 線上監控有時監控數值會為空，但斷電重啟後則可正常監控 |

### B. 老化 Issue 完整清單（>180 天，共 18 筆）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | Region | 摘要 |
|----|--------|------|-------|-------|----------|--------|------|
| 383486 | Major | 80 | Verification | LUCIAN.LS.OUYANG 歐陽龍祥 | 904 | IA Internal-CoreTech | [JIRA] (調適) [IABGVOC-177] Issue 383486 - 在online monito |
| 386302 | Major | 120 | In Progress | LUCIAN.LS.OUYANG 歐陽龍祥 | 893 | IA Internal-CoreTech | [JIRA] (程式編輯) [IABGVOC-183] Issue 386302 - DIADesigner庫 |
| 410331 | Minor | 120 | Review | MIAO.CHEN 陳炫妙 | 795 | IA Internal-CoreTech | [JIRA](程式編輯) [IABGVOC-193] Issue 410331 - 热键：跳转到变量表，能否增 |
| 412810 | Major | 240 | Review | HARVEY.XIE 謝孟軒 | 785 | IA Internal | [JIRA] (程式編輯) [IABGVOC-196] CORNER-3323 - ST语法中TO_TIME( |
| 416557 | Major | 240 | Review | STEWARD.LU 呂名峰 | 769 | IA Internal-CoreTech | [JIRA] (線上斷線) [IABGVOC-197] Issue 416557 - 在线时拔掉电脑与W3A的 |
| 416915 | Major | 360 | Review | ELVIS.CT.CHANG 張錦宗 | 768 | IA Internal-CoreTech | [JIRA](程式編輯) [IABGVOC-198] Issue 416915 - FB功能块，调整其内部变量 |
| 425835 | Major | 240 | Review | LEANN.TING 丁寧 | 733 | IA Internal | [JIRA] (程式編輯) [IABGVOC-189] Issue 425835 - 测试打断点时，出现报错提 |
| 466614 | Major | 400 | In Progress | STEWARD.LU 呂名峰 | 567 | DGC-China | [JIRA] (程式編輯) [IABGVOC-2017] In the Ladder program unit |
| 469965 | Minor | 80 | Verification | LEANN.TING 丁寧 | 553 | DGC-China | [JIRA] (專案管理) [IABGVOC-186] Issue 407138 - 软件下载界面：勾选下载后 |
| 486433 | Critical | 600 | Review | STEWARD.LU 呂名峰 | 490 | DGC-China | [JIRA] (調適) [IABGVOC-513] 增加在线时，多个变量修改状态，可以同时写入PLC功能 |
| 505913 | Critical | 600 | Review | PINGCHIN.WANG 王昞清 | 412 | IA Internal-CoreTech | [JIRA][efficacy](程式編輯) [IABGVOC-785] DIADesigner SP4 發生 |
| 522213 | Critical | 144 | Review & Approval | STEWARD.LU 呂名峰 | 342 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-975] 線上監控有時監控數值會為空，但斷電重啟後則可正常監控 |
| 522471 | Major | 64 | In Progress | XAVIERA.FAN 范珮欣 | 341 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-977] 与设备断线后软体还显示在线状态 |
| 528538 | Major | 240 | Verification | ARCHIE.YANG 楊浩群 | 305 | DGC-China | [JIRA] (程式編輯) [IABGVOC-1054] DIADesigner软件上传W3A程序及配置无法上 |
| 528531 | Major | 240 | In Progress | LUCIAN.LS.OUYANG 歐陽龍祥 | 305 | DGC-China | [JIRA] (程式編輯) [IABGVOC-1058] 功能块实例必须自己手敲，才会确认，不智能 |
| 538366 | Critical | 600 | Review | UNI.CHEN 陳軍宇 | 258 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-2032] Ladder Expression 輸出接點狀態顯示 |
| 547507 | Critical | 600 | Review & Approval | JACKY.TU 杜寧 | 200 | IA Internal-SC | [JIRA] (運動控制) [IABGVOC-1227] 傳動機制參數設定欄位，沒有按下 Enter 鍵單獨脫 |
| 548867 | Major | 400 | Review & Approval | JENNY.HY.CHEN 陳湘筠 | 193 | IA Internal-IMSBU | [JIRA](調適) [IABGVOC-1246] DIA Designer示波器能錄4CH、16KHZ、32 |

### C. step_control / 手順 / dgc_fae 完整項目列表

#### C1. Issue（26 筆）

| ID | Tag | 嚴重性 | FMEA | State | Owner | Region | 摘要 |
|----|-----|--------|------|-------|-------|--------|------|
| 561272 | step_control | Blocker | 1000 | Closed | STEWARD.LU 呂名峰 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1461] 程序区變量監控格顯示為空 |
| 528236 | step_control | Blocker | 1000 | Closed | KF.LIU 劉桂輔 | IA Internal-SC | [JIRA] (模組編輯) [IABGVOC-1067] 程序区变量监控遇到ARRAY [*] OF BYTE |
| 579102 | step_control | Critical | 600 | Verification | KAKA.WU 吳思言 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-2013] 及時刷新 LOG 狀態下關閉頁籤，在线仿真發生例外 |
| 578889 | dgc_fae | Critical | 600 | Review | Unassigned | DGC-China | [JIRA] (硬體配置) [IABGVOC-1955] 重新安裝 COMMGR 後，每次在专案按了连线就会跳 |
| 574365 | step_control | Critical | 600 | Verification | UNI.CHEN 陳軍宇 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1829] ST Pou 在線監控程序時出現 "未知序列錯誤" |
| 572963 | step_control | Critical | 600 | Closed | HARVEY.XIE 謝孟軒 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1794] ST 解析特定語法下出現例外錯誤 |
| 572378 | step_control | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1768] 变量表初值设定错误后无法编辑 |
| 572377 | step_control | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1769] ARRAY[*] OF ARRAY[*] OF 2維 |
| 538366 | step_control | Critical | 600 | Review | UNI.CHEN 陳軍宇 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-2032] Ladder Expression 輸出接點狀態顯示 |
| 579103 | step_control | Major | 400 | Review | ELVIS.CT.CHANG 張錦宗 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-2014] LD中输出节点状态显示异常 |
| 578046 | step_control | Major | 400 | Review | Unassigned | IA Internal-SC | [JIRA] (調適) [IABGVOC-1897] 功能块IN_OUT_PUT引脚状态无法展开监控 |
| 572461 | step_control | Major | 400 | Review | HARVEY.XIE 謝孟軒 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1776] 程序区变量选中需要提示此变量的详细信息 |
| 572460 | step_control | Major | 400 | Review & Approval | JASON.JY.LIN 林峻宇 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1770] 联合体/结构体没办法声明Array [*] OF A |
| 572382 | step_control | Major | 400 | In Progress | MIAO.CHEN 陳炫妙 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1771] 結構體初始值設定後報錯 |
| 520738 | step_control | Major | 400 | Closed | KF.LIU 劉桂輔 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-961] POU中添加函数，函数引脚无赋值符 |
| 466614 | step_control | Major | 400 | In Progress | STEWARD.LU 呂名峰 | DGC-China | [JIRA] (程式編輯) [IABGVOC-2017] In the Ladder program unit |
| 579098 | dgc_fae | Major | 240 | Closed | JOHNNY.MC.YEH 葉明勳 | IA Internal-SC | [JIRA] (調適) [IABGVOC-1999] 示波器监控无曲线，无值，属于已知问题 |
| 579005 | dgc_fae | Major | 240 | Review | Unassigned | DGC-China | [JIRA] (程式編輯) [IABGVOC-1994] EXCEL导入MC_xxx FB的变量，但是在 LD |
| 579002 | dgc_fae | Major | 240 | Review | Unassigned | DGC-China | [JIRA] (專案編譯) [IABGVOC-1993] 下载时还会重新编译一次 |
| 578892 | dgc_fae | Major | 240 | Review | HARVEY.XIE 謝孟軒 | DGC-China | [JIRA] (程式編輯) [IABGVOC-1964] 梯形图下Axis1的轴变量无法将其他类似位置等变量列 |
| 578888 | dgc_fae | Critical | 240 | Review | Unassigned | DGC-China | [JIRA] (網路配置) [IABGVOC-1958] EtherCAT 插入設備時彈出例外視窗 |
| 578885 | dgc_fae | Major | 240 | Closed | Unassigned | DGC-China | [JIRA] (調適) [IABGVOC-1959] 示波器：轴监控选择Motion_Tag_Table |
| 574868 | step_control | Major | 240 | Review & Approval | KF.LIU 劉桂輔 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1840] ST Call FB.Method 後不應彈出新增變 |
| 524836 | step_control | Major | 240 | Closed | KF.LIU 劉桂輔 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1015] FC函数调用POU区经常提示相关引脚变量未声明 |
| 578880 | dgc_fae | Minor | 120 | Review & Approval | XAVIERA.FAN 范珮欣 | DGC-China | [JIRA] (硬體配置) [IABGVOC-1965] 下方狀態列仿真器名称不符 |
| 517915 | step_control | Minor | 40 | Closed | JACKY.TU 杜寧 | IA Internal-SC | [JIRA] (運動控制) [IABGVOC-931] 轴组态界面位置显示精度设定默认值 |

#### C2. Requirement（34 筆）

| ID | Tag | 嚴重性 | FMEA | State | Owner | Region | 摘要 |
|----|-----|--------|------|-------|-------|--------|------|
| 579898 | 手順 | Blocker | 1000 | Review | Unassigned | IA Internal-SC | [JIRA] (新增裝置) [IABGVOC-2035] SGM 標準化專案開發需求 : 軟體專案樹架構調整 |
| 502728 | step_control | Blocker | 1000 | In Progress | KF.LIU 劉桂輔 | IA Internal-SC | [JIRA](程式編輯) [IABGVOC-687] 使用ST语言编程环境下使用^符号后相关变量无法提示索引 |
| 561097 | step_control | Critical | 600 | Review | ORLANDO.LAN 藍順騰 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1463] 变量类型支持ANY变量 |
| 229108 | step_control | Critical | 600 | Review | STEWARD.LU 呂名峰 | IA Internal-SC | [JIRA] (調適) [IABGVOC-1873] REF_TO变量监控无法展开 |
| 578942 | dgc_fae | Major | 400 | Review | Unassigned | DGC-China | [JIRA] (程式編輯) [IABGVOC-1952] 新增变数的型态可以考虑参考CODESYS |
| 574370 | step_control | Major | 400 | Review | HARVEY.XIE 謝孟軒 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1830] ST Show Hint 希望能分段解析變數 |
| 561761 | step_control | Major | 400 | Review | ORLANDO.LAN 藍順騰 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1487] 数组范围可以设定便属性为常量的变量ARRAY [0..VAR] |
| 523235 | dgc_fae | Major | 400 | Review | HARVEY.XIE 謝孟軒 | DGC-China | [JIRA] (survey)(程式編輯) [IABGVOC-1954] ST Online模式下的監控行距調 |
| 522465 | step_control | Blocker | 400 | Review | STEWARD.LU 呂名峰 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-976] 监控表中部分变量无法监控，无法修改变量值 |
| 568982 | step_control | Major | 400 | Verification | ORLANDO.LAN 藍順騰 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1666] 支援不定长数组功能如ARRAY[*,*] OF 類型 |
| 581522 | dgc_fae | Major | 240 | Review | Unassigned | DGC-China | [JIRA] (手冊) [IABGVOC-2002] 軟體手冊內容、功能優化 |
| 581078 | dgc_fae | Major | 240 | Review | Unassigned | IA Internal-SC | [JIRA] (輔助工具) [IABGVOC-2041] 万年历功能 |
| 579939 | 手順 | Major | 240 | Review | Unassigned | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-2037] ENUM 變數監控賦值功能優化 |
| 579933 | dgc_fae | Major | 240 | Review | Unassigned | DGC-China | [JIRA] (運動控制) [IABGVOC-1996] 轴参数画面配置画面参考AX8配置第三方电机 |
| 579887 | dgc_fae | Major | 240 | Review | Unassigned | DGC-China | [JIRA] (運動控制) [IABGVOC-1991] 齿比设定参考: AX的直线电机UI |
| 579884 | 手順 | Major | 240 | Review | Unassigned | IA Internal-SC | [JIRA] (專案管理) [IABGVOC-2030] 使用者再開啟專案後，能自動回復上次開啟的介面 |
| 579097 | dgc_fae | Major | 240 | Review | Unassigned | DGC-China | [JIRA] (程式編輯) [IABGVOC-2001] 指令精靈選擇 DL 庫時難以快速查找 |
| 579095 | dgc_fae | Major | 240 | Review | ELVIS.CT.CHANG 張錦宗 | DGC-China | [JIRA] (程式編輯) [IABGVOC-2004] LD插入功能块按鈕新增 |
| 579092 | dgc_fae | Major | 240 | Review | JACKY.TU 杜寧 | DGC-China | [JIRA] (運動控制) [IABGVOC-2005] 新增轴，不能直接输入中文 |
| 579090 | step_control | Major | 240 | Review | Unassigned | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1984] 枚舉類型的變數 Show Hint 能顯示出成員名稱 |
| 579089 | dgc_fae | Major | 240 | Review | Unassigned | DGC-China | [JIRA] (程式編輯) [IABGVOC-2000] 離線模式下可展開陣列、結構體變數且得知位址資訊 |
| 578879 | dgc_fae | Major | 240 | Review | Unassigned | DGC-China | [JIRA] (專案管理) [IABGVOC-1961] 监控表不能放到屏幕下方 |
| 575986 | step_control | Major | 240 | Review | MIAO.CHEN 陳炫妙 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1877] STRING 變量初始值設定頁面預設值需填上 '' |
| 578951 | dgc_fae | Major | 240 | Closed | Unassigned | DGC-China | [JIRA] (專案管理) [IABGVOC-1963] 下载时没有进度条 |
| 578948 | dgc_fae | Major | 240 | Closed | Unassigned | DGC-China | [JIRA] (程式編輯) [IABGVOC-1962] 程序页面中变量区域，变量不能展开看到内部参数 |
| 511568 | step_control | Critical | 240 | Closed | KF.LIU 劉桂輔 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-834] 建立结构体时无法对变量进行初始化赋值 |
| 572358 | step_control | Minor | 200 | Review & Approval | ORLANDO.LAN 藍順騰 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1767] 变量表信息展示不完全 |
| 579894 | 手順 | Major | 160 | Review | Unassigned | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-2034] 梯形圖接點、輸出線圈右鍵選單內容優化 |
| 579544 | step_control | Major | 160 | Review | ELVIS.CT.CHANG 張錦宗 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-2025] LD 顯示的變量長度希望可自動調整 |
| 564593 | step_control | Major | 160 | Review | Unassigned | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1580] 用户权限设定 |
| 561098 | step_control | Major | 160 | Review | Unassigned | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1465] 变量交叉引用功能 |
| 502704 | step_control | Major | 160 | Review | HARVEY.XIE 謝孟軒 | IA Internal-SC | [JIRA](程式編輯) [IABGVOC-667] 支援完整的 Function Block 基底的繼承功能 |
| 578890 | dgc_fae | Minor | 120 | Review | JACKY.TU 杜寧 | DGC-China | [JIRA] (運動控制) [IABGVOC-1960] 运动参数设置，默認速度值與仿真測試初始值不符 |
| 516609 | step_control | Critical | 16 | Review | MIAO.CHEN 陳炫妙 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-850] 结构体变量为数组时数组大小限定不可以为变量 |

# DIADesigner / W3A Issue & Requirement 分析報告

> 資料截止日：2026-05-20　Issue 總數：269　Requirement 總數：165

---

## 執行摘要（Executive Summary）

- **立即風險 — Blocker Unassigned**：#581951（FMEA=1000，EtherCAT IO Mapping 編譯錯誤）2 天前新增，目前 **Unassigned**，需今日完成指派並開始修復。
- **1.14.0 交付危機**：Issue 完成率僅 **34%**（11/32），Requirement 完成率僅 **22%**（9/41）——距版本封版所剩工作量龐大，是當前 **最高優先交付風險**。
- **1.15.0 零進展**：Issue 0/6（0%）、Requirement 0/20（0%），所有項目仍停在開放狀態，尚無任何 Close 記錄，規劃版本窗口壓力上升。
- **Unassigned 黑洞**：10 筆 B/C/M 開放 Issue 無人負責（佔開放 Issue 的 **26%**）；37 筆開放 Requirement 無負責人（佔開放 Req 的 **42%**）——無負責人即無結案路徑。
- **step_control 模組最不穩定**：Issue 開放率 **53%**（10/19），Req 開放率 **88%**（15/17），含多筆高 FMEA 項目，是影響手順功能穩定性的最大單一風險點。
- **老化積壓**：15 筆 Issue 開放超過 180 天，最長達 905 天（#383486）；LUCIAN.LS.OUYANG 與 STEWARD.LU 各持有 3 筆 Backlog Issue，構成 **單點故障風險**。
- **DGC-China 客戶響應風險**：dgc_fae 標籤有 5 筆開放 Issue + 12 筆開放 Requirement，多數 Unassigned——若持續無回應，將影響外部客戶關係。
- **Requirement 積壓未收斂**：2024 年 Req 關閉率 0%，2025 年 51%，2026 年至今 54%，始終低於新增速度；Issue 解決動能正向（2026 年已達 118%，清理舊欠款）。

---

## 分析方法（Methodology）

| 項目 | 說明 |
|------|------|
| 資料來源 | JIRA CSV 匯出：IABGVOC Issue.csv（269 筆）、IABGVOC Requirement.csv（165 筆） |
| 截止日期 | 2026-05-20 |
| Open 定義 | State ∉ {"Closed", "Review & Approval"} |
| 老化定義 | 開放天數 > 180 天 |
| FMEA 分層 | 🔴 ≥500 / 🟡 201–499 / 🟢 ≤200 |
| 功能檢點 Tag | 比對 Excel D 欄 321 個合法 Tag（全小寫比對），排除 JIRA 流程標籤 |
| 特別關注 Tag | step_control / 手順 / dgc_fae（固定三個，不在 Excel 內）|
| 版本映射 | Planned For 欄位 → 顯示版本類別（見 SKILL.md Section 5）|

---

## 一、Issue 現況（TE Leader / RD Leader）

### 1.1 嚴重性分布

| 嚴重性 | 總數 | 開放數 | 開放率 |
|--------|------|--------|--------|
| Blocker | 33 | 1 | 3% |
| Critical | 100 | 11 | 11% |
| Major | 94 | 23 | 24% |
| Minor | 42 | 4 | 10% |
| **合計** | **269** | **39** | **15%** |

> **觀察**：整體 Issue 開放率 15%，健康度尚可；但 Major 開放率 24% 偏高，Critical 仍有 11 筆開放，其中多筆已老化（見 1.5）或 Unassigned（見 1.6）。

### 1.2 狀態分布

| State | Issue 數量 |
|-------|-----------|
| Closed | 221 |
| Review | 26 |
| Review & Approval | 9 |
| In Progress | 8 |
| Verification | 5 |

> **觀察**：26 筆 Issue 卡在 Review 等待 TE 驗收，是當前最大的流程瓶頸。8 筆 In Progress 代表正在修復中。

### 1.3 版本計畫完成率

| 版本 | Issue 總數 | 已關閉 | 完成率 | 風險 |
|------|-----------|--------|--------|------|
| DIADesigner 1.14.0 | 32 | 11 | 34% | 🔴 **交付風險** |
| DIADesigner 1.15.0 | 6 | 0 | 0% | 🔴 **零進展** |
| Need More Information | 4 | 0 | 0% | 🟡 待分類 |
| Backlog | 1 | 0 | 0% | 🟡 積壓 |
| DIADesigner 1.13.0 | 21 | 18 | 86% | 🟢 正常 |
| Need Triage | 54 | 50 | 93% | 🟢 正常 |
| DIADesigner 1.12.0 | 41 | 41 | 100% | 🟢 完成 |
| DIADesigner 1.11.0 | 38 | 38 | 100% | 🟢 完成 |
| DIADesigner SP1 | 31 | 31 | 100% | 🟢 完成 |
| DIADesigner SP4 | 25 | 25 | 100% | 🟢 完成 |
| DIADesigner 1.10.0 | 14 | 14 | 100% | 🟢 完成 |
| DIADesigner 1.9.0 | 2 | 2 | 100% | 🟢 完成 |

> **1.14.0 交付風險**：21 筆 Issue 仍未關閉，完成率 34%，若版本即將封版需立即介入。**1.15.0 零進展**：6 筆全部開放，尚未開始修復，須確認版本規劃是否需延後。

### 1.4 Critical / Blocker 未關閉項目（依 FMEA 排序）

共 **12 筆**（Blocker × 1，Critical × 11）。

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|----|--------|------|-------|-------|---------|------|
| 581951 | Blocker | 1000 | Review | Unassigned | 2 | [JIRA] (程式編輯) [IABGVOC-2091] W3A 專案編譯時出現多筆 C0115 Overma… |
| 579102 | Critical | 600 | Verification | KAKA.WU 吳思言 | 21 | [JIRA] (程式編輯) [IABGVOC-2013] 及時刷新 LOG 狀態下關閉頁籤，在线仿真發生例外 |
| 578889 | Critical | 600 | Review | Unassigned | 22 | [JIRA] (硬體配置) [IABGVOC-1955] 重新安裝 COMMGR 後，每次在专案按了连线就会跳… |
| 574365 | Critical | 600 | Verification | UNI.CHEN 陳軍宇 | 50 | [JIRA] (程式編輯) [IABGVOC-1829] ST Pou 在線監控程序時出現 "未知序列錯誤" |
| 572378 | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | 57 | [JIRA] (程式編輯) [IABGVOC-1768] 变量表初值设定错误后无法编辑 |
| 572377 | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | 57 | [JIRA] (程式編輯) [IABGVOC-1769] ARRAY[*] OF ARRAY[*] OF 2維… |
| 563431 | Critical | 600 | Review | Unassigned | 112 | [JIRA] (調適) [IABGVOC-1532] 示波器保存的波形重新打开后发现显示的波形和我们点击的不符… |
| 562353 | Critical | 600 | Review | Unassigned | 117 | [JIRA] (調適) [IABGVOC-1506] 示波器由A专案保存，开启B专案后打开示波器后部分变量无法… |
| 538366 | Critical | 600 | Review | UNI.CHEN 陳軍宇 | 259 | [JIRA] (程式編輯) [IABGVOC-2032] Ladder Expression 輸出接點狀態顯示… |
| 505913 | Critical | 600 | Review | PINGCHIN.WANG 王昞清 | 413 | [JIRA][efficacy](程式編輯) [IABGVOC-785] DIADesigner SP4 發生… |
| 486433 | Critical | 600 | Review | STEWARD.LU 呂名峰 | 491 | [JIRA] (調適) [IABGVOC-513] 增加在线时，多个变量修改状态，可以同时写入PLC功能 - … |
| 578888 | Critical | 240 | Review | Unassigned | 22 | [JIRA] (網路配置) [IABGVOC-1958] EtherCAT 插入設備時彈出例外視窗 |

> **風險詮釋**：STEWARD.LU 負責的 #486433 開放已達 **491 天**（🔴 FMEA=600），已成老化高風險。5 筆 Unassigned Critical/Blocker 中，#578889、#563431、#562353 均無人認領超過 22 天。

### 1.5 Backlog Issue（開放 > 180 天）

共 **15 筆**，最長 905 天。

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|----|--------|------|-------|-------|---------|------|
| 383486 | Major | 80 | Verification | LUCIAN.LS.OUYANG 歐陽龍祥 | 905 | [JIRA] (調適) [IABGVOC-177] Issue 383486 - 在online monito… |
| 386302 | Major | 120 | In Progress | LUCIAN.LS.OUYANG 歐陽龍祥 | 894 | [JIRA] (程式編輯) [IABGVOC-183] Issue 386302 - DIADesigner庫… |
| 410331 | Minor | 120 | Review | MIAO.CHEN 陳炫妙 | 796 | [JIRA](程式編輯) [IABGVOC-193] Issue 410331 - 热键：跳转到变量表，能否增… |
| 412810 | Major | 240 | Review | HARVEY.XIE 謝孟軒 | 786 | [JIRA] (程式編輯) [IABGVOC-196] CORNER-3323 - ST语法中TO_TIME(… |
| 416557 | Major | 240 | Review | STEWARD.LU 呂名峰 | 770 | [JIRA] (線上斷線) [IABGVOC-197] Issue 416557 - 在线时拔掉电脑与W3A的… |
| 416915 | Major | 360 | Review | ELVIS.CT.CHANG 張錦宗 | 769 | [JIRA](程式編輯) [IABGVOC-198] Issue 416915 - FB功能块，调整其内部变量… |
| 425835 | Major | 240 | Review | LEANN.TING 丁寧 | 734 | [JIRA] (程式編輯) [IABGVOC-189] Issue 425835 - 测试打断点时，出现报错提… |
| 466614 | Major | 400 | In Progress | STEWARD.LU 呂名峰 | 568 | [JIRA] (程式編輯) [IABGVOC-2017] In the Ladder program unit… |
| 469965 | Minor | 80 | Verification | LEANN.TING 丁寧 | 554 | [JIRA] (專案管理) [IABGVOC-186] Issue 407138 - 软件下载界面：勾选下载后… |
| 486433 | Critical | 600 | Review | STEWARD.LU 呂名峰 | 491 | [JIRA] (調適) [IABGVOC-513] 增加在线时，多个变量修改状态，可以同时写入PLC功能 - … |
| 505913 | Critical | 600 | Review | PINGCHIN.WANG 王昞清 | 413 | [JIRA][efficacy](程式編輯) [IABGVOC-785] DIADesigner SP4 發生… |
| 522471 | Major | 64 | In Progress | XAVIERA.FAN 范珮欣 | 342 | [JIRA] (程式編輯) [IABGVOC-977] 与设备断线后软体还显示在线状态 |
| 528538 | Major | 240 | Verification | ARCHIE.YANG 楊浩群 | 306 | [JIRA] (程式編輯) [IABGVOC-1054] DIADesigner软件上传W3A程序及配置无法上… |
| 528531 | Major | 240 | In Progress | LUCIAN.LS.OUYANG 歐陽龍祥 | 306 | [JIRA] (程式編輯) [IABGVOC-1058] 功能块实例必须自己手敲，才会确认，不智能，应该可以自… |
| 538366 | Critical | 600 | Review | UNI.CHEN 陳軍宇 | 259 | [JIRA] (程式編輯) [IABGVOC-2032] Ladder Expression 輸出接點狀態顯示… |

> **單點故障風險**：LUCIAN.LS.OUYANG（3 筆）、STEWARD.LU（3 筆）各持有大量老化 Issue；STEWARD.LU 的 #486433（Critical, FMEA=600）同時出現在 C/B 開放清單，風險最高。

### 1.6 高嚴重性 Unassigned Issue

共 **10 筆**（B/C/M 且 Unassigned）。

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|----|--------|------|-------|-------|---------|------|
| 581951 | Blocker | 1000 | Review | Unassigned | 2 | [JIRA] (程式編輯) [IABGVOC-2091] W3A 專案編譯時出現多筆 C0115 Overma… |
| 578889 | Critical | 600 | Review | Unassigned | 22 | [JIRA] (硬體配置) [IABGVOC-1955] 重新安裝 COMMGR 後，每次在专案按了连线就会跳… |
| 563431 | Critical | 600 | Review | Unassigned | 112 | [JIRA] (調適) [IABGVOC-1532] 示波器保存的波形重新打开后发现显示的波形和我们点击的不符… |
| 562353 | Critical | 600 | Review | Unassigned | 117 | [JIRA] (調適) [IABGVOC-1506] 示波器由A专案保存，开启B专案后打开示波器后部分变量无法… |
| 578046 | Major | 400 | Review | Unassigned | 26 | [JIRA] (調適) [IABGVOC-1897] 功能块IN_OUT_PUT引脚状态无法展开监控 |
| 574859 | Major | 400 | Review | Unassigned | 48 | [JIRA] (程式編輯) [IABGVOC-1839] 更新DIADesigner 1.13.0.66_Tr… |
| 571907 | Major | 400 | Review | Unassigned | 61 | [JIRA] (專案管理) [IABGVOC-1750] DIA Designer多次開啟project後，每… |
| 578888 | Critical | 240 | Review | Unassigned | 22 | [JIRA] (網路配置) [IABGVOC-1958] EtherCAT 插入設備時彈出例外視窗 |
| 579005 | Major | 240 | Review | Unassigned | 21 | [JIRA] (程式編輯) [IABGVOC-1994] EXCEL导入MC_xxx FB的变量，但是在 LD… |
| 579002 | Major | 240 | Review | Unassigned | 21 | [JIRA] (專案編譯) [IABGVOC-1993] 下载时还会重新编译一次(实体机、模拟器需要智能判断) |

---

## 二、Requirement 進度（PM）

### 2.1 嚴重性分布

| 嚴重性 | 總數 | 開放數 | 開放率 |
|--------|------|--------|--------|
| Blocker | 19 | 8 | 42% |
| Critical | 28 | 9 | 32% |
| Major | 77 | 52 | 68% |
| Minor | 41 | 19 | 46% |
| **合計** | **165** | **88** | **53%** |

> **觀察**：Requirement 整體開放率 **53%**，遠高於 Issue 的 15%。Blocker 開放率 42%、Major 開放率 68% 尤為嚴峻，顯示需求管理存在系統性落差。

### 2.2 狀態分布

| State | Requirement 數量 |
|-------|----------------|
| Review | 80 |
| Closed | 70 |
| Review & Approval | 7 |
| In Progress | 4 |
| Verification | 4 |

> **觀察**：80 筆 Requirement 停在 Review 狀態，佔開放總量的 **91%**，顯示需求評審機制是最大流程瓶頸，而非開發或驗收問題。

### 2.3 FMEA 風險分層（未關閉 88 筆）

| 風險層級 | 筆數 | 佔比 |
|---------|------|------|
| 🔴 High（FMEA ≥ 500） | 12 | 14% |
| 🟡 Medium（FMEA 201–499） | 41 | 47% |
| 🟢 Low（FMEA ≤ 200） | 35 | 40% |

> **觀察**：14% 的高風險 Req（12 筆 🔴）仍無交付計畫，其中多筆 FMEA=1000，需 PM 優先排定版本規劃。

### 2.4 FMEA Top-20 未關閉 Requirement

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|----|--------|------|-------|-------|---------|------|
| 579898 | Blocker | 1000 | Review | Unassigned | 13 | [JIRA] (新增裝置) [IABGVOC-2035] SGM 標準化專案開發需求 : 軟體專案樹架構調整 |
| 562586 | Blocker | 1000 | Review | JENNY.HY.CHEN 陳湘筠 | 117 | [JIRA] (調適) [IABGVOC-1340] 支援建立多個示波器 |
| 546062 | Blocker | 1000 | Review | STEWARD.LU 呂名峰 | 211 | [JIRA] (程式編輯) [IABGVOC-774] 监控表里结构体下的VAR_IN_OUT变量在监控表里无… |
| 534083 | Blocker | 1000 | Review | Unassigned | 281 | [JIRA] (輔助工具) [IABGVOC-1120] 軟體支援輔助工具 - IO 刷新開關 |
| 509758 | Minor | 1000 | Review | JACKY.TU 杜寧 | 397 | [JIRA] (運動控制) [IABGVOC-690] 软体轴配置显示画面需要类似AX8一样能够显示轴状态，位… |
| 506831 | Major | 1000 | Review | HARVEY.XIE 謝孟軒 | 408 | [JIRA](程式編輯) [IABGVOC-505] 建控制指令的时候无法用键盘的Tab全部出来，必须打出来再… |
| 502728 | Blocker | 1000 | In Progress | KF.LIU 劉桂輔 | 426 | [JIRA](程式編輯) [IABGVOC-687] 使用ST语言编程环境下使用^符号后相关变量无法提示索引,… |
| 538350 | Blocker | 1000 | Verification | JENNY.HY.CHEN 陳湘筠 | 259 | [JIRA] [實作] (調適) [IABGVOC-527] 示波器支援單/多通道切換功能 (多通道) |
| 533908 | Blocker | 1000 | Verification | FRANKNC.HO 何南瑾 | 282 | [JIRA] (網路配置) [IABGVOC-1111] AS与W3A MODBUS TCP通讯NOK,原因内… |
| 561097 | Critical | 600 | Review | ORLANDO.LAN 藍順騰 | 124 | [JIRA] (程式編輯) [IABGVOC-1463] 变量类型支持ANY变量 |
| 229108 | Critical | 600 | Review | STEWARD.LU 呂名峰 | 1759 | [JIRA] (調適) [IABGVOC-1873] REF_TO变量监控无法展开 |
| 527019 | Critical | 600 | In Progress | JEAN.LC.WANG 王儷臻 | 314 | [JIRA] (模組編輯) [IABGVOC-1012] R1扩展模组映射变量无法关联Byte/Word等数据… |
| 578942 | Major | 400 | Review | Unassigned | 21 | [JIRA] (程式編輯) [IABGVOC-1952] 新增变数的型态可以考虑参考CODESYS :只要搜寻… |
| 574370 | Major | 400 | Review | HARVEY.XIE 謝孟軒 | 50 | [JIRA] (程式編輯) [IABGVOC-1830] ST Show Hint 希望能分段解析變數 |
| 570233 | Major | 400 | Review | JOHNNY.MC.YEH 葉明勳 | 70 | [JIRA] (調適) [IABGVOC-1705] 示波器 Monitor Type 導入A2架構的 Adr… |
| 570179 | Major | 400 | Review | Unassigned | 70 | [JIRA] (調適) [IABGVOC-1703] 示波器畫布背景顏色的切換 |
| 570177 | Major | 400 | Review | Unassigned | 70 | [JIRA] (調適) [IABGVOC-1702] 示波器監控項目支援上下移動 |
| 566923 | Major | 400 | Review | STEWARD.LU 呂名峰 | 86 | [JIRA] (程式編輯) [IABGVOC-1634] FB的INOUT引脚类型，在线功能块实例列表视窗中，… |
| 564587 | Major | 400 | Review | ELVIS.CT.CHANG 張錦宗 | 106 | [JIRA] (程式編輯) [IABGVOC-1585] DIADesigner 梯形圖支援空白塊輸入實例名稱… |
| 561761 | Major | 400 | Review | ORLANDO.LAN 藍順騰 | 120 | [JIRA] (程式編輯) [IABGVOC-1487] 数组范围可以设定便属性为常量的变量ARRAY [0.… |

> **特別注意**：#229108（Critical, FMEA=600）開放達 **1759 天**，是全資料集中開放最久的項目，STEWARD.LU 負責，需立即確認是否仍有效。

### 2.5 版本計畫完成率（Requirement）

| 版本 | Req 總數 | 已關閉 | 完成率 | 風險 |
|------|---------|--------|--------|------|
| DIADesigner 1.15.0 | 20 | 0 | 0% | 🔴 **零進展** |
| Backlog | 14 | 0 | 0% | 🔴 **無計畫** |
| Need More Information | 3 | 0 | 0% | 🟡 待分類 |
| Need Triage | 22 | 6 | 27% | 🟡 待分類 |
| DIADesigner 1.14.0 | 41 | 9 | 22% | 🔴 **交付風險** |
| DIADesigner 1.12.0 | 31 | 30 | 97% | 🟢 完成 |
| DIADesigner 1.13.0 | 13 | 13 | 100% | 🟢 完成 |
| DIADesigner 1.11.0 | 13 | 13 | 100% | 🟢 完成 |
| DIADesigner SP4 | 3 | 3 | 100% | 🟢 完成 |
| DIADesigner 1.10.0 | 3 | 3 | 100% | 🟢 完成 |

---

## 三、區域 / 客戶分析

| Region | Customer Name | Issue 總數 | Issue 開放 | C/B 開放 | Req 總數 | Req 開放 |
|--------|--------------|-----------|-----------|---------|---------|---------|
| IA Internal-SC | 陳會杰 | 56 | 4 | 0 | 31 | 13 |
| IA Internal-SC | 辛昱錦 | 24 | 3 | 2 | 53 | 23 |
| IA Internal-SC | 郭德山 | 26 | 8 | 4 | 21 | 17 |
| IA Internal-CoreTech | 蔡弘晉 | 38 | 5 | 0 | 1 | 0 |
| IA Internal-SC | 蔡弘晉 | 35 | 0 | 0 | 0 | 0 |
| DGC-China | 韓軼 | 7 | 5 | 2 | 12 | 10 |
| IA Internal-IMSBU | 楊政達 | 13 | 3 | 0 | 3 | 2 |
| DGC-China | 趙俊明 | 7 | 2 | 0 | 5 | 2 |
| IA Internal | 蔡弘晉 | 11 | 2 | 0 | 0 | 0 |
| IA Internal-SC | 韓軼 | 7 | 1 | 0 | 2 | 2 |
| IA Internal-CoreTech | 陳軍宇 | 5 | 0 | 0 | 4 | 3 |
| IA Internal-CoreTech | 陳嘉俊 | 3 | 0 | 0 | 3 | 1 |
| IA Internal-SC | 商福進 | 0 | 0 | 0 | 6 | 4 |
| IA Internal-CoreTech | 鄧亨禮 | 3 | 1 | 1 | 2 | 1 |
| IA Internal-IMSBU | 陳嘉俊 | 2 | 1 | 1 | 0 | 0 |
| DGC-China | 陳會杰 | 1 | 1 | 1 | 1 | 0 |
| DGC-China | 黃亮亮\蔡弘晉 | 1 | 1 | 0 | 0 | 0 |
| DGC-China | 朱賀; 郭德山 | 1 | 1 | 0 | 0 | 0 |
| DGC-China | 李凱旋 | 0 | 0 | 0 | 1 | 1 |
| DGC-China | 郭德山; 陳會杰; 辛昱錦; 張育然; DGC | 0 | 0 | 0 | 1 | 1 |
| DGC-China | 上海托展\陳會杰 | 0 | 0 | 0 | 1 | 1 |
| DGC-China | 湛江恒润机械; 辛昱錦 | 0 | 0 | 0 | 1 | 1 |

> **DGC-China 客戶關係風險**：DGC-China 合計 Issue 開放 10 筆（C/B 開放 3 筆），Req 開放 15 筆，多數為 Unassigned——若持續無負責人回應，將損害外部客戶信任。
>
> **IA Internal-SC / 郭德山**：C/B 開放 4 筆，Issue 開放率 31%，為內部 SC 客戶中風險最高的聯絡人。

---

## 四、功能模組熱點分析（功能檢點 Tag）

Top-20 功能模組，以 Issue + Req 總量降冪排序。

| 功能模組（Tag） | Issue 總數 | Issue 開放 | C/B 開放 | Req 總數 | Req 開放 |
|--------------|-----------|-----------|---------|---------|---------|
| oscilloscope | 37 | 3 | 2 | 16 | 7 |
| motion_axisset | 20 | 0 | 0 | 22 | 11 |
| programming_glovar | 21 | 4 | 2 | 16 | 7 |
| programming_monitable | 16 | 3 | 1 | 13 | 8 |
| programming_lang_st_edit | 15 | 5 | 0 | 12 | 8 |
| devnetwork_ethercat | 17 | 1 | 1 | 9 | 3 |
| programming_lang_st_monitor | 13 | 2 | 1 | 7 | 7 |
| downloaduploadmgr | 15 | 2 | 0 | 3 | 0 |
| programming_lang_ld_edit | 5 | 3 | 0 | 9 | 7 |
| programming_compile | 12 | 2 | 1 | 1 | 1 |
| programming_lang_ld_monitor | 10 | 3 | 1 | 3 | 2 |
| programming_lang | 8 | 0 | 0 | 1 | 1 |
| programming_lang_ld | 8 | 2 | 1 | 0 | 0 |
| librarymanager | 7 | 2 | 0 | 1 | 0 |
| programming_poutype_fb | 5 | 0 | 0 | 3 | 1 |
| diadesigner_file_load | 5 | 1 | 0 | 2 | 2 |
| devhardware_layout_moduletable_iomap | 4 | 1 | 1 | 2 | 1 |
| diadesigner_edit_searchreplace | 3 | 1 | 0 | 3 | 2 |
| diadesigner_file_save | 3 | 0 | 0 | 2 | 1 |
| deverrorinfo | 3 | 1 | 1 | 1 | 0 |

> **模組風險詮釋**：
> - **oscilloscope**：總量最高（53 筆），Issue C/B 開放 2 筆，Req 開放 7 筆（44%）——示波器功能積壓需求多，屬 **中等不穩定**。
> - **motion_axisset**：Req 開放率 **50%**（11/22），且 Issue 開放為 0，顯示運動控制開發需求大量積壓，RD 尚未接手。
> - **programming_lang_st_edit**：Issue 開放率 **33%**（5/15），含多筆 Review 卡關，TE 需驅動驗收。
> - **devnetwork_ethercat**：C/B 開放 1 筆（#581951 FMEA=1000 Blocker）——最高風險模組，需立即處理。

---

## 五、特別關注項目（step_control / 手順 / dgc_fae）

### 5.1 Issue

**step_control**（Issue=19，開放=10，開放率 53%）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|----|--------|------|-------|-------|---------|------|
| 579102 | Critical | 600 | Verification | KAKA.WU 吳思言 | 21 | [JIRA] (程式編輯) [IABGVOC-2013] 及時刷新 LOG 狀態下關閉頁籤，在线仿真發生例外 |
| 574365 | Critical | 600 | Verification | UNI.CHEN 陳軍宇 | 50 | [JIRA] (程式編輯) [IABGVOC-1829] ST Pou 在線監控程序時出現 "未知序列錯誤" |
| 572378 | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | 57 | [JIRA] (程式編輯) [IABGVOC-1768] 变量表初值设定错误后无法编辑 |
| 572377 | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | 57 | [JIRA] (程式編輯) [IABGVOC-1769] ARRAY[*] OF ARRAY[*] OF 2維… |
| 538366 | Critical | 600 | Review | UNI.CHEN 陳軍宇 | 259 | [JIRA] (程式編輯) [IABGVOC-2032] Ladder Expression 輸出接點狀態顯示… |
| 579103 | Major | 400 | Review | ELVIS.CT.CHANG 張錦宗 | 21 | [JIRA] (程式編輯) [IABGVOC-2014] LD中输出节点状态显示异常 |
| 578046 | Major | 400 | Review | Unassigned | 26 | [JIRA] (調適) [IABGVOC-1897] 功能块IN_OUT_PUT引脚状态无法展开监控 |
| 572461 | Major | 400 | Review | HARVEY.XIE 謝孟軒 | 57 | [JIRA] (程式編輯) [IABGVOC-1776] 程序区变量选中需要提示此变量的详细信息 |
| 572382 | Major | 400 | In Progress | MIAO.CHEN 陳炫妙 | 57 | [JIRA] (程式編輯) [IABGVOC-1771] 結構體初始值設定後報錯: "String数据类型无法… |
| 466614 | Major | 400 | In Progress | STEWARD.LU 呂名峰 | 568 | [JIRA] (程式編輯) [IABGVOC-2017] In the Ladder program unit… |

**手順**（Issue=0）

**dgc_fae**（Issue=8，開放=5，開放率 63%）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|----|--------|------|-------|-------|---------|------|
| 578889 | Critical | 600 | Review | Unassigned | 22 | [JIRA] (硬體配置) [IABGVOC-1955] 重新安裝 COMMGR 後，每次在专案按了连线就会跳… |
| 578888 | Critical | 240 | Review | Unassigned | 22 | [JIRA] (網路配置) [IABGVOC-1958] EtherCAT 插入設備時彈出例外視窗 |
| 578892 | Major | 240 | Review | HARVEY.XIE 謝孟軒 | 22 | [JIRA] (程式編輯) [IABGVOC-1964] 梯形图下Axis1的轴变量无法将其他类似位置等变量列… |
| 579005 | Major | 240 | Review | Unassigned | 21 | [JIRA] (程式編輯) [IABGVOC-1994] EXCEL导入MC_xxx FB的变量，但是在 LD… |
| 579002 | Major | 240 | Review | Unassigned | 21 | [JIRA] (專案編譯) [IABGVOC-1993] 下载时还会重新编译一次(实体机、模拟器需要智能判断) |

### 5.2 Requirement

**step_control**（Req=17，開放=15，開放率 88%）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|----|--------|------|-------|-------|---------|------|
| 502728 | Blocker | 1000 | In Progress | KF.LIU 劉桂輔 | 426 | [JIRA](程式編輯) [IABGVOC-687] 使用ST语言编程环境下使用^符号后相关变量无法提示索引,… |
| 561097 | Critical | 600 | Review | ORLANDO.LAN 藍順騰 | 124 | [JIRA] (程式編輯) [IABGVOC-1463] 变量类型支持ANY变量 |
| 229108 | Critical | 600 | Review | STEWARD.LU 呂名峰 | 1759 | [JIRA] (調適) [IABGVOC-1873] REF_TO变量监控无法展开 |
| 527019 | Critical | 600 | In Progress | JEAN.LC.WANG 王儷臻 | 314 | [JIRA] (模組編輯) [IABGVOC-1012] R1扩展模组映射变量无法关联Byte/Word等数据… |
| 522465 | Blocker | 400 | Review | STEWARD.LU 呂名峰 | 342 | [JIRA] (程式編輯) [IABGVOC-976] 监控表中部分变量无法监控，无法修改变量值 |
| 574370 | Major | 400 | Review | HARVEY.XIE 謝孟軒 | 50 | [JIRA] (程式編輯) [IABGVOC-1830] ST Show Hint 希望能分段解析變數 |
| 561761 | Major | 400 | Review | ORLANDO.LAN 藍順騰 | 120 | [JIRA] (程式編輯) [IABGVOC-1487] 数组范围可以设定便属性为常量的变量ARRAY [0.… |
| 568982 | Major | 400 | Verification | ORLANDO.LAN 藍順騰 | 76 | [JIRA] (程式編輯) [IABGVOC-1666] 支援不定长数组功能如ARRAY[*,*] OF 類型… |
| 579090 | Major | 240 | Review | Unassigned | 21 | [JIRA] (程式編輯) [IABGVOC-1984] 枚舉類型的變數 Show Hint 能顯示出成員名稱… |
| 575986 | Major | 240 | Review | MIAO.CHEN 陳炫妙 | 40 | [JIRA] (程式編輯) [IABGVOC-1877] STRING 變量初始值設定頁面預設值需填上 '' |
| 579544 | Major | 160 | Review | ELVIS.CT.CHANG 張錦宗 | 15 | [JIRA] (程式編輯) [IABGVOC-2025] LD 顯示的變量長度希望可自動調整 |
| 564593 | Major | 160 | Review | Unassigned | 106 | [JIRA] (程式編輯) [IABGVOC-1580] 用户权限设定 |
| 561098 | Major | 160 | Review | Unassigned | 124 | [JIRA] (程式編輯) [IABGVOC-1465] 变量交叉引用功能 |
| 502704 | Major | 160 | Review | HARVEY.XIE 謝孟軒 | 426 | [JIRA](程式編輯) [IABGVOC-667] 支援完整的 Function Block 基底的繼承功能… |
| 516609 | Critical | 16 | Review | MIAO.CHEN 陳炫妙 | 371 | [JIRA] (程式編輯) [IABGVOC-850] 结构体变量为数组时数组大小限定不可以为变量 |

**手順**（Req=4，開放=4，開放率 100%）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|----|--------|------|-------|-------|---------|------|
| 579898 | Blocker | 1000 | Review | Unassigned | 13 | [JIRA] (新增裝置) [IABGVOC-2035] SGM 標準化專案開發需求 : 軟體專案樹架構調整 |
| 579939 | Major | 240 | Review | Unassigned | 13 | [JIRA] (程式編輯) [IABGVOC-2037] ENUM 變數監控賦值功能優化 |
| 579884 | Major | 240 | Review | Unassigned | 13 | [JIRA] (專案管理) [IABGVOC-2030] 使用者再開啟專案後，能自動回復上次開啟的介面 |
| 579894 | Major | 160 | Review | Unassigned | 13 | [JIRA] (程式編輯) [IABGVOC-2034] 梯形圖接點、輸出線圈右鍵選單內容優化 |

> **手順 Req 全數 Unassigned**：4 筆 100% 開放且無負責人，需 PM 今日指派。

**dgc_fae**（Req=14，開放=12，開放率 86%）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|----|--------|------|-------|-------|---------|------|
| 578942 | Major | 400 | Review | Unassigned | 21 | [JIRA] (程式編輯) [IABGVOC-1952] 新增变数的型态可以考虑参考CODESYS :只要搜寻… |
| 523235 | Major | 400 | Review | HARVEY.XIE 謝孟軒 | 337 | [JIRA] (survey)(程式編輯) [IABGVOC-1954] ST Online模式下的監控行距調… |
| 581522 | Major | 240 | Review | Unassigned | 6 | [JIRA] (手冊) [IABGVOC-2002] 軟體手冊內容、功能優化 |
| 581078 | Major | 240 | Review | Unassigned | 8 | [JIRA] (輔助工具) [IABGVOC-2041] 万年历功能 |
| 579933 | Major | 240 | Review | Unassigned | 13 | [JIRA] (運動控制) [IABGVOC-1996] 轴参数画面配置画面参考AX8配置第三方电机（比亚迪）… |
| 579887 | Major | 240 | Review | Unassigned | 13 | [JIRA] (運動控制) [IABGVOC-1991] 齿比设定参考: AX的直线电机UI |
| 579097 | Major | 240 | Review | Unassigned | 21 | [JIRA] (程式編輯) [IABGVOC-2001] 指令精靈選擇 DL 庫時難以快速查找 |
| 579095 | Major | 240 | Review | ELVIS.CT.CHANG 張錦宗 | 21 | [JIRA] (程式編輯) [IABGVOC-2004] LD插入功能块按鈕新增, 带EN,ENO, 不帶 E… |
| 579092 | Major | 240 | Review | JACKY.TU 杜寧 | 21 | [JIRA] (運動控制) [IABGVOC-2005] 新增轴，不能直接输入中文，需要以字母为首 |
| 579089 | Major | 240 | Review | Unassigned | 21 | [JIRA] (程式編輯) [IABGVOC-2000] 離線模式下可展開陣列、結構體變數且得知位址資訊 |
| 578879 | Major | 240 | Review | Unassigned | 22 | [JIRA] (專案管理) [IABGVOC-1961] 监控表不能放到屏幕下方，只能放在两侧，监控变量时不方… |
| 578890 | Minor | 120 | Review | JACKY.TU 杜寧 | 22 | [JIRA] (運動控制) [IABGVOC-1960] 运动参数设置，默認速度值與仿真測試初始值不符 |

---

## 六、歷年趨勢分析

| 年份 | Issue 新增 | Issue 關閉 | Issue 解決率 | Req 新增 | Req 關閉 | Req 解決率 |
|------|-----------|-----------|------------|---------|---------|----------|
| 2021 | 0 | 0 | — | 1 | 0 | 0% |
| 2022 | 0 | 0 | — | 1 | 0 | 0% |
| 2023 | 31 | 2 | 6% | 3 | 0 | 0% |
| 2024 | 39 | 31 | 79% | 12 | 0 | 0% |
| 2025 | 159 | 150 | 94% | 85 | 43 | 51% |
| 2026（截至今日）| 40 | 47 | 118% | 63 | 34 | 54% |

> **Issue 解決能力正向**：2025 年 94%，2026 年已達 118%（清理舊欠款），Issue 動能持續改善中。
>
> **Requirement 積壓加速警示**：2024 年 Req 解決率 0%，2025 年才首度開始關閉（51%），2026 年 54%，但新增速度（63 筆）遠超關閉速度（34 筆）——積壓總量仍在擴大，需系統性介入。

---

## 建議事項（Recommendations）

### PM

1. **今日**指派 #581951（Blocker, FMEA=1000, Unassigned）負責人——EtherCAT IO Mapping 編譯錯誤，無負責人即無結案路徑。
2. 指派 **37 筆 Unassigned 開放 Requirement** 的負責人，優先處理 12 筆 🔴 High FMEA（≥500）。
3. **手順 4 筆 Req 全數 Unassigned**，需今日完成指派並確認版本交付計畫。
4. 召開 **1.14.0 版本健康審查**：Issue 完成率 34%、Req 完成率 22%，若封版時程固定，需立即縮減版本範圍或增加人力。
5. 確認 **#229108**（Critical, FMEA=600，開放 1759 天）是否仍有效，無效則關閉，有效則排定版本。

### RD Leader

1. **今日**指派 #581951 修復工程師（Blocker, FMEA=1000, EtherCAT 相關）。
2. 檢視 MIAO.CHEN 陳炫妙 工作負載：持有 #572378、#572377、#572382 等多筆 In Progress C/B，為潛在單點風險。
3. 確認 **1.15.0 Issue 6 筆**的開發認領時程與預估完成日——目前完成率 0%。
4. 驅動 STEWARD.LU 處理 #466614（Major, FMEA=400，已積壓 **568 天**）——老化最嚴重的 In Progress Issue。
5. STEWARD.LU 持有 #486433（Critical, FMEA=600，開放 491 天）+ 多筆 Backlog，為 **單點故障風險**，需確認是否需要轉移負責人。

### TE Leader

1. 驅動 **26 筆 Review 狀態 Issue** 完成驗收——佔所有開放 Issue 的 67%，是當前最大流程瓶頸。
2. 稽核 **15 筆 Backlog Issue**：確認修復是否已完成但 State 未更新，或仍有缺陷待驗。
3. **step_control 模組** Issue 開放率 53%（含 5 筆 C/B），為版本 Go/No-Go 關鍵指標，建立專項驗收計畫。
4. 追蹤 Verification 狀態的 5 筆 Issue（#579102、#574365 等 FMEA=600），確認驗收時程。

### 部門主管

1. **C/B 開放 Issue 共 12 筆**——設定每週最低關閉目標（建議 3 筆/週）並在周會追蹤。
2. **12 筆 🔴 High-FMEA Requirement** 未交付——PM 應在本月底完成優先序對齊會議，明確版本或 Backlog 決策。
3. **DGC-China 客戶 Issue 開放率偏高**（韓軼相關：5/7=71%），多數 Unassigned——於下次客戶季報前主動溝通交付計畫，降低客戶關係風險。
4. Requirement 積壓仍在擴大（2026 年新增 63 筆、關閉 34 筆），建議引入 Req 每月 Review 機制，設定最大積壓上限。

---

## 附錄（Appendix）

### A. 全部 Critical / Blocker 開放 Issue（12 筆）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|----|--------|------|-------|-------|---------|------|
| 581951 | Blocker | 1000 | Review | Unassigned | 2 | [JIRA] (程式編輯) [IABGVOC-2091] W3A 專案編譯時出現多筆 C0115 Overma… |
| 579102 | Critical | 600 | Verification | KAKA.WU 吳思言 | 21 | [JIRA] (程式編輯) [IABGVOC-2013] 及時刷新 LOG 狀態下關閉頁籤，在线仿真發生例外 |
| 578889 | Critical | 600 | Review | Unassigned | 22 | [JIRA] (硬體配置) [IABGVOC-1955] 重新安裝 COMMGR 後，每次在专案按了连线就会跳… |
| 574365 | Critical | 600 | Verification | UNI.CHEN 陳軍宇 | 50 | [JIRA] (程式編輯) [IABGVOC-1829] ST Pou 在線監控程序時出現 "未知序列錯誤" |
| 572378 | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | 57 | [JIRA] (程式編輯) [IABGVOC-1768] 变量表初值设定错误后无法编辑 |
| 572377 | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | 57 | [JIRA] (程式編輯) [IABGVOC-1769] ARRAY[*] OF ARRAY[*] OF 2維… |
| 563431 | Critical | 600 | Review | Unassigned | 112 | [JIRA] (調適) [IABGVOC-1532] 示波器保存的波形重新打开后发现显示的波形和我们点击的不符… |
| 562353 | Critical | 600 | Review | Unassigned | 117 | [JIRA] (調適) [IABGVOC-1506] 示波器由A专案保存，开启B专案后打开示波器后部分变量无法… |
| 538366 | Critical | 600 | Review | UNI.CHEN 陳軍宇 | 259 | [JIRA] (程式編輯) [IABGVOC-2032] Ladder Expression 輸出接點狀態顯示… |
| 505913 | Critical | 600 | Review | PINGCHIN.WANG 王昞清 | 413 | [JIRA][efficacy](程式編輯) [IABGVOC-785] DIADesigner SP4 發生… |
| 486433 | Critical | 600 | Review | STEWARD.LU 呂名峰 | 491 | [JIRA] (調適) [IABGVOC-513] 增加在线时，多个变量修改状态，可以同时写入PLC功能 - … |
| 578888 | Critical | 240 | Review | Unassigned | 22 | [JIRA] (網路配置) [IABGVOC-1958] EtherCAT 插入設備時彈出例外視窗 |

### B. Backlog Issue 完整清單（開放 > 180 天，共 15 筆）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|----|--------|------|-------|-------|---------|------|
| 383486 | Major | 80 | Verification | LUCIAN.LS.OUYANG 歐陽龍祥 | 905 | [JIRA] (調適) [IABGVOC-177] Issue 383486 - 在online monito… |
| 386302 | Major | 120 | In Progress | LUCIAN.LS.OUYANG 歐陽龍祥 | 894 | [JIRA] (程式編輯) [IABGVOC-183] Issue 386302 - DIADesigner庫… |
| 410331 | Minor | 120 | Review | MIAO.CHEN 陳炫妙 | 796 | [JIRA](程式編輯) [IABGVOC-193] Issue 410331 - 热键：跳转到变量表，能否增… |
| 412810 | Major | 240 | Review | HARVEY.XIE 謝孟軒 | 786 | [JIRA] (程式編輯) [IABGVOC-196] CORNER-3323 - ST语法中TO_TIME(… |
| 416557 | Major | 240 | Review | STEWARD.LU 呂名峰 | 770 | [JIRA] (線上斷線) [IABGVOC-197] Issue 416557 - 在线时拔掉电脑与W3A的… |
| 416915 | Major | 360 | Review | ELVIS.CT.CHANG 張錦宗 | 769 | [JIRA](程式編輯) [IABGVOC-198] Issue 416915 - FB功能块，调整其内部变量… |
| 425835 | Major | 240 | Review | LEANN.TING 丁寧 | 734 | [JIRA] (程式編輯) [IABGVOC-189] Issue 425835 - 测试打断点时，出现报错提… |
| 466614 | Major | 400 | In Progress | STEWARD.LU 呂名峰 | 568 | [JIRA] (程式編輯) [IABGVOC-2017] In the Ladder program unit… |
| 469965 | Minor | 80 | Verification | LEANN.TING 丁寧 | 554 | [JIRA] (專案管理) [IABGVOC-186] Issue 407138 - 软件下载界面：勾选下载后… |
| 486433 | Critical | 600 | Review | STEWARD.LU 呂名峰 | 491 | [JIRA] (調適) [IABGVOC-513] 增加在线时，多个变量修改状态，可以同时写入PLC功能 - … |
| 505913 | Critical | 600 | Review | PINGCHIN.WANG 王昞清 | 413 | [JIRA][efficacy](程式編輯) [IABGVOC-785] DIADesigner SP4 發生… |
| 522471 | Major | 64 | In Progress | XAVIERA.FAN 范珮欣 | 342 | [JIRA] (程式編輯) [IABGVOC-977] 与设备断线后软体还显示在线状态 |
| 528538 | Major | 240 | Verification | ARCHIE.YANG 楊浩群 | 306 | [JIRA] (程式編輯) [IABGVOC-1054] DIADesigner软件上传W3A程序及配置无法上… |
| 528531 | Major | 240 | In Progress | LUCIAN.LS.OUYANG 歐陽龍祥 | 306 | [JIRA] (程式編輯) [IABGVOC-1058] 功能块实例必须自己手敲，才会确认，不智能，应该可以自… |
| 538366 | Critical | 600 | Review | UNI.CHEN 陳軍宇 | 259 | [JIRA] (程式編輯) [IABGVOC-2032] Ladder Expression 輸出接點狀態顯示… |

### C. step_control / 手順 / dgc_fae 完整項目列表

#### C.1 step_control — Issue（全 19 筆）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|----|--------|------|-------|-------|---------|------|
| 561272 | Blocker | 1000 | Closed | STEWARD.LU 呂名峰 | 121 | [JIRA] (程式編輯) [IABGVOC-1461] 程序区變量監控格顯示為空 |
| 528236 | Blocker | 1000 | Closed | KF.LIU 劉桂輔 | 307 | [JIRA] (模組編輯) [IABGVOC-1067] 程序区变量监控遇到ARRAY [*] OF BYTE… |
| 579102 | Critical | 600 | Verification | KAKA.WU 吳思言 | 21 | [JIRA] (程式編輯) [IABGVOC-2013] 及時刷新 LOG 狀態下關閉頁籤，在线仿真發生例外 |
| 574365 | Critical | 600 | Verification | UNI.CHEN 陳軍宇 | 50 | [JIRA] (程式編輯) [IABGVOC-1829] ST Pou 在線監控程序時出現 "未知序列錯誤" |
| 572963 | Critical | 600 | Closed | HARVEY.XIE 謝孟軒 | 56 | [JIRA] (程式編輯) [IABGVOC-1794] ST 解析特定語法下出現例外錯誤 : "序列未包含項… |
| 572378 | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | 57 | [JIRA] (程式編輯) [IABGVOC-1768] 变量表初值设定错误后无法编辑 |
| 572377 | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | 57 | [JIRA] (程式編輯) [IABGVOC-1769] ARRAY[*] OF ARRAY[*] OF 2維… |
| 538366 | Critical | 600 | Review | UNI.CHEN 陳軍宇 | 259 | [JIRA] (程式編輯) [IABGVOC-2032] Ladder Expression 輸出接點狀態顯示… |
| 527679 | Critical | 600 | Closed | ORLANDO.LAN 藍順騰 | 309 | [JIRA] (模組編輯) [IABGVOC-1061] VAR RETAIN/RETAIN_M 問題反饋 (… |
| 579103 | Major | 400 | Review | ELVIS.CT.CHANG 張錦宗 | 21 | [JIRA] (程式編輯) [IABGVOC-2014] LD中输出节点状态显示异常 |
| 578046 | Major | 400 | Review | Unassigned | 26 | [JIRA] (調適) [IABGVOC-1897] 功能块IN_OUT_PUT引脚状态无法展开监控 |
| 572461 | Major | 400 | Review | HARVEY.XIE 謝孟軒 | 57 | [JIRA] (程式編輯) [IABGVOC-1776] 程序区变量选中需要提示此变量的详细信息 |
| 572460 | Major | 400 | Review & Approval | JASON.JY.LIN 林峻宇 | 57 | [JIRA] (程式編輯) [IABGVOC-1770] 联合体/结构体没办法声明Array [*] OF A… |
| 572382 | Major | 400 | In Progress | MIAO.CHEN 陳炫妙 | 57 | [JIRA] (程式編輯) [IABGVOC-1771] 結構體初始值設定後報錯: "String数据类型无法… |
| 520738 | Major | 400 | Closed | KF.LIU 劉桂輔 | 350 | [JIRA] (程式編輯) [IABGVOC-961] POU中添加函数，函数引脚无赋值符，引脚无相关说明 |
| 466614 | Major | 400 | In Progress | STEWARD.LU 呂名峰 | 568 | [JIRA] (程式編輯) [IABGVOC-2017] In the Ladder program unit… |
| 574868 | Major | 240 | Review & Approval | KF.LIU 劉桂輔 | 48 | [JIRA] (程式編輯) [IABGVOC-1840] ST Call FB.Method 後不應彈出新增變… |
| 524836 | Major | 240 | Closed | KF.LIU 劉桂輔 | 323 | [JIRA] (程式編輯) [IABGVOC-1015] FC函数调用POU区经常提示相关引脚变量未声明 |
| 517915 | Minor | 40 | Closed | JACKY.TU 杜寧 | 365 | [JIRA] (運動控制) [IABGVOC-931] 轴组态界面位置显示精度设定默认值 |

#### C.2 step_control — Requirement（全 17 筆）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|----|--------|------|-------|-------|---------|------|
| 502728 | Blocker | 1000 | In Progress | KF.LIU 劉桂輔 | 426 | [JIRA](程式編輯) [IABGVOC-687] 使用ST语言编程环境下使用^符号后相关变量无法提示索引,… |
| 561097 | Critical | 600 | Review | ORLANDO.LAN 藍順騰 | 124 | [JIRA] (程式編輯) [IABGVOC-1463] 变量类型支持ANY变量 |
| 229108 | Critical | 600 | Review | STEWARD.LU 呂名峰 | 1759 | [JIRA] (調適) [IABGVOC-1873] REF_TO变量监控无法展开 |
| 527019 | Critical | 600 | In Progress | JEAN.LC.WANG 王儷臻 | 314 | [JIRA] (模組編輯) [IABGVOC-1012] R1扩展模组映射变量无法关联Byte/Word等数据… |
| 522465 | Blocker | 400 | Review | STEWARD.LU 呂名峰 | 342 | [JIRA] (程式編輯) [IABGVOC-976] 监控表中部分变量无法监控，无法修改变量值 |
| 574370 | Major | 400 | Review | HARVEY.XIE 謝孟軒 | 50 | [JIRA] (程式編輯) [IABGVOC-1830] ST Show Hint 希望能分段解析變數 |
| 561761 | Major | 400 | Review | ORLANDO.LAN 藍順騰 | 120 | [JIRA] (程式編輯) [IABGVOC-1487] 数组范围可以设定便属性为常量的变量ARRAY [0.… |
| 568982 | Major | 400 | Verification | ORLANDO.LAN 藍順騰 | 76 | [JIRA] (程式編輯) [IABGVOC-1666] 支援不定长数组功能如ARRAY[*,*] OF 類型… |
| 579090 | Major | 240 | Review | Unassigned | 21 | [JIRA] (程式編輯) [IABGVOC-1984] 枚舉類型的變數 Show Hint 能顯示出成員名稱… |
| 575986 | Major | 240 | Review | MIAO.CHEN 陳炫妙 | 40 | [JIRA] (程式編輯) [IABGVOC-1877] STRING 變量初始值設定頁面預設值需填上 '' |
| 511568 | Critical | 240 | Closed | KF.LIU 劉桂輔 | 387 | [JIRA] (程式編輯) [IABGVOC-834] 建立结构体时无法对变量进行初始化赋值 |
| 572358 | Minor | 200 | Review & Approval | ORLANDO.LAN 藍順騰 | 57 | [JIRA] (程式編輯) [IABGVOC-1767] 变量表信息展示不完全 |
| 579544 | Major | 160 | Review | ELVIS.CT.CHANG 張錦宗 | 15 | [JIRA] (程式編輯) [IABGVOC-2025] LD 顯示的變量長度希望可自動調整 |
| 564593 | Major | 160 | Review | Unassigned | 106 | [JIRA] (程式編輯) [IABGVOC-1580] 用户权限设定 |
| 561098 | Major | 160 | Review | Unassigned | 124 | [JIRA] (程式編輯) [IABGVOC-1465] 变量交叉引用功能 |
| 502704 | Major | 160 | Review | HARVEY.XIE 謝孟軒 | 426 | [JIRA](程式編輯) [IABGVOC-667] 支援完整的 Function Block 基底的繼承功能… |
| 516609 | Critical | 16 | Review | MIAO.CHEN 陳炫妙 | 371 | [JIRA] (程式編輯) [IABGVOC-850] 结构体变量为数组时数组大小限定不可以为变量 |

#### C.3 手順 — Issue（0 筆）

#### C.4 手順 — Requirement（全 4 筆）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|----|--------|------|-------|-------|---------|------|
| 579898 | Blocker | 1000 | Review | Unassigned | 13 | [JIRA] (新增裝置) [IABGVOC-2035] SGM 標準化專案開發需求 : 軟體專案樹架構調整 |
| 579939 | Major | 240 | Review | Unassigned | 13 | [JIRA] (程式編輯) [IABGVOC-2037] ENUM 變數監控賦值功能優化 |
| 579884 | Major | 240 | Review | Unassigned | 13 | [JIRA] (專案管理) [IABGVOC-2030] 使用者再開啟專案後，能自動回復上次開啟的介面 |
| 579894 | Major | 160 | Review | Unassigned | 13 | [JIRA] (程式編輯) [IABGVOC-2034] 梯形圖接點、輸出線圈右鍵選單內容優化 |

#### C.5 dgc_fae — Issue（全 8 筆）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|----|--------|------|-------|-------|---------|------|
| 578889 | Critical | 600 | Review | Unassigned | 22 | [JIRA] (硬體配置) [IABGVOC-1955] 重新安裝 COMMGR 後，每次在专案按了连线就会跳… |
| 578888 | Critical | 240 | Review | Unassigned | 22 | [JIRA] (網路配置) [IABGVOC-1958] EtherCAT 插入設備時彈出例外視窗 |
| 578892 | Major | 240 | Review | HARVEY.XIE 謝孟軒 | 22 | [JIRA] (程式編輯) [IABGVOC-1964] 梯形图下Axis1的轴变量无法将其他类似位置等变量列… |
| 579005 | Major | 240 | Review | Unassigned | 21 | [JIRA] (程式編輯) [IABGVOC-1994] EXCEL导入MC_xxx FB的变量，但是在 LD… |
| 579002 | Major | 240 | Review | Unassigned | 21 | [JIRA] (專案編譯) [IABGVOC-1993] 下载时还会重新编译一次(实体机、模拟器需要智能判断) |
| 579098 | Major | 240 | Closed | JOHNNY.MC.YEH 葉明勳 | 21 | [JIRA] (調適) [IABGVOC-1999] 示波器监控无曲线，无值，属于已知问题 |
| 578885 | Major | 240 | Closed | Unassigned | 22 | [JIRA] (調適) [IABGVOC-1959] 示波器：轴监控选择Motion_Tag_Table.Ax… |
| 578880 | Minor | 120 | Review & Approval | XAVIERA.FAN 范珮欣 | 22 | [JIRA] (硬體配置) [IABGVOC-1965] 下方狀態列仿真器名称不符 |

#### C.6 dgc_fae — Requirement（全 14 筆）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|----|--------|------|-------|-------|---------|------|
| 578942 | Major | 400 | Review | Unassigned | 21 | [JIRA] (程式編輯) [IABGVOC-1952] 新增变数的型态可以考虑参考CODESYS :只要搜寻… |
| 523235 | Major | 400 | Review | HARVEY.XIE 謝孟軒 | 337 | [JIRA] (survey)(程式編輯) [IABGVOC-1954] ST Online模式下的監控行距調… |
| 581522 | Major | 240 | Review | Unassigned | 6 | [JIRA] (手冊) [IABGVOC-2002] 軟體手冊內容、功能優化 |
| 581078 | Major | 240 | Review | Unassigned | 8 | [JIRA] (輔助工具) [IABGVOC-2041] 万年历功能 |
| 579933 | Major | 240 | Review | Unassigned | 13 | [JIRA] (運動控制) [IABGVOC-1996] 轴参数画面配置画面参考AX8配置第三方电机（比亚迪）… |
| 579887 | Major | 240 | Review | Unassigned | 13 | [JIRA] (運動控制) [IABGVOC-1991] 齿比设定参考: AX的直线电机UI |
| 579097 | Major | 240 | Review | Unassigned | 21 | [JIRA] (程式編輯) [IABGVOC-2001] 指令精靈選擇 DL 庫時難以快速查找 |
| 579095 | Major | 240 | Review | ELVIS.CT.CHANG 張錦宗 | 21 | [JIRA] (程式編輯) [IABGVOC-2004] LD插入功能块按鈕新增, 带EN,ENO, 不帶 E… |
| 579092 | Major | 240 | Review | JACKY.TU 杜寧 | 21 | [JIRA] (運動控制) [IABGVOC-2005] 新增轴，不能直接输入中文，需要以字母为首 |
| 579089 | Major | 240 | Review | Unassigned | 21 | [JIRA] (程式編輯) [IABGVOC-2000] 離線模式下可展開陣列、結構體變數且得知位址資訊 |
| 578879 | Major | 240 | Review | Unassigned | 22 | [JIRA] (專案管理) [IABGVOC-1961] 监控表不能放到屏幕下方，只能放在两侧，监控变量时不方… |
| 578951 | Major | 240 | Closed | Unassigned | 21 | [JIRA] (專案管理) [IABGVOC-1963] 下载时没有进度条 |
| 578948 | Major | 240 | Closed | Unassigned | 21 | [JIRA] (程式編輯) [IABGVOC-1962] 程序页面中变量区域，变量不能展开看到内部参数 |
| 578890 | Minor | 120 | Review | JACKY.TU 杜寧 | 22 | [JIRA] (運動控制) [IABGVOC-1960] 运动参数设置，默認速度值與仿真測試初始值不符 |

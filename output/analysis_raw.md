# IABGVOC Issue & Requirement 分析報告

> 資料截止日：2026-05-21　Issue 總數：269　Requirement 總數：165

## 執行摘要（Executive Summary）

- **開放 Issue 數**：39 / 269（其中 Critical/Blocker：12 筆）
- **開放 Requirement 數**：88 / 165（整體完成率：46.7%）
- **最高風險 Requirement**：[579898] [JIRA] (新增裝置) [IABGVOC-2035] SGM 標準化專案開發需求 : 軟體專案樹架構調整… (FMEA=1000)
- **最熱點功能模組（Tag）**：`oscilloscope`（Issue+Req 合計 53 筆）
- **老化 Issue（>180天未關閉）**：15 筆

## 分析方法（Methodology）

| 項目 | 說明 |
|------|------|
| 資料來源 | IABGVOC Issue.csv（269 筆）、IABGVOC Requirement.csv（165 筆）|
| 時間範圍 | 2021 ~ 2026/05（全部資料）|
| 分析基準日 | 2026-05-21 |
| 開放定義 | State ∉ {Closed, Review & Approval} |
| 老化定義 | 開放超過 180 天（創建日至今）|
| 特別關注 Tag | `step_control`、`手順`、`dgc_fae` |
| FMEA 分層 | 高風險：>=500 / 中風險：200-499 / 低風險：<200 |

## 一、Issue 現況（TE Leader / RD Leader）

### 1.1 嚴重性分布

| 嚴重性 | 總數 | 開放數 | 開放率 |
|--------|------|--------|--------|
| Blocker | 33 | 1 | 3.0% |
| Critical | 100 | 11 | 11.0% |
| Major | 94 | 23 | 24.5% |
| Minor | 42 | 4 | 9.5% |

### 1.2 狀態分布

| 狀態 | 數量 |
|------|------|
| Closed | 221 |
| Review | 24 |
| Review & Approval | 9 |
| In Progress | 8 |
| Verification | 7 |

### 1.3 版本計畫完成率（分類規則）

| 版本分類 | 總數 | 已關閉 | 完成率 |
|----------|------|--------|--------|
| DIADesigner SP1 | 31 | 31 | 100.0% |
| DIADesigner SP4 | 25 | 25 | 100.0% |
| DIADesigner 1.9.0 | 2 | 2 | 100.0% |
| DIADesigner 1.10.0 | 14 | 14 | 100.0% |
| DIADesigner 1.11.0 | 38 | 38 | 100.0% |
| DIADesigner 1.12.0 | 41 | 41 | 100.0% |
| DIADesigner 1.13.0 | 21 | 18 | 85.7% |
| DIADesigner 1.14.0 | 32 | 11 | 34.4% |
| DIADesigner 1.15.0 | 6 | 0 | 0.0% |
| Need Triage | 54 | 50 | 92.6% |
| Need More Information | 4 | 0 | 0.0% |
| Backlog | 1 | 0 | 0.0% |

### 1.4 Critical / Blocker 未關閉項目（共 12 筆，依 FMEA 排序）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|---|---|----|-----|-----|----|---|
| 581951 | Blocker | 1000 | Verification | JEAN.LC.WANG 王儷臻 | 3 | [JIRA] (程式編輯) [IABGVOC-2091] W3A 專案編譯時出現多筆 C0115 Overma |
| 579102 | Critical | 600 | Verification | KAKA.WU 吳思言 | 22 | [JIRA] (程式編輯) [IABGVOC-2013] 及時刷新 LOG 狀態下關閉頁籤，在线仿真發生例外 |
| 578889 | Critical | 600 | Review | Unassigned | 23 | [JIRA] (硬體配置) [IABGVOC-1955] 重新安裝 COMMGR 後，每次在专案按了连线就会跳 |
| 574365 | Critical | 600 | Verification | UNI.CHEN 陳軍宇 | 51 | [JIRA] (程式編輯) [IABGVOC-1829] ST Pou 在線監控程序時出現 "未知序列錯誤" |
| 572378 | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | 58 | [JIRA] (程式編輯) [IABGVOC-1768] 变量表初值设定错误后无法编辑 |
| 572377 | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | 58 | [JIRA] (程式編輯) [IABGVOC-1769] ARRAY[*] OF ARRAY[*] OF 2維 |
| 563431 | Critical | 600 | Review | Unassigned | 113 | [JIRA] (調適) [IABGVOC-1532] 示波器保存的波形重新打开后发现显示的波形和我们点击的不符 |
| 562353 | Critical | 600 | Review | Unassigned | 118 | [JIRA] (調適) [IABGVOC-1506] 示波器由A专案保存，开启B专案后打开示波器后部分变量无法 |
| 538366 | Critical | 600 | Review | UNI.CHEN 陳軍宇 | 260 | [JIRA] (程式編輯) [IABGVOC-2032] Ladder Expression 輸出接點狀態顯示 |
| 505913 | Critical | 600 | Review | PINGCHIN.WANG 王昞清 | 414 | [JIRA][efficacy](程式編輯) [IABGVOC-785] DIADesigner SP4 發生 |
| 486433 | Critical | 600 | Review | STEWARD.LU 呂名峰 | 492 | [JIRA] (調適) [IABGVOC-513] 增加在线时，多个变量修改状态，可以同时写入PLC功能 -  |
| 578888 | Critical | 240 | Review | Unassigned | 23 | [JIRA] (網路配置) [IABGVOC-1958] EtherCAT 插入設備時彈出例外視窗 |

### 1.5 Backlog Issue（開放 >180 天，共 15 筆）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|---|---|----|-----|-----|----|---|
| 383486 | Major | 80 | Verification | LUCIAN.LS.OUYANG 歐陽龍祥 | 906 | [JIRA] (調適) [IABGVOC-177] Issue 383486 - 在online monito |
| 386302 | Major | 120 | In Progress | LUCIAN.LS.OUYANG 歐陽龍祥 | 895 | [JIRA] (程式編輯) [IABGVOC-183] Issue 386302 - DIADesigner庫 |
| 410331 | Minor | 120 | Review | MIAO.CHEN 陳炫妙 | 797 | [JIRA](程式編輯) [IABGVOC-193] Issue 410331 - 热键：跳转到变量表，能否增 |
| 412810 | Major | 240 | Review | HARVEY.XIE 謝孟軒 | 787 | [JIRA] (程式編輯) [IABGVOC-196] CORNER-3323 - ST语法中TO_TIME( |
| 416557 | Major | 240 | Review | STEWARD.LU 呂名峰 | 771 | [JIRA] (線上斷線) [IABGVOC-197] Issue 416557 - 在线时拔掉电脑与W3A的 |
| 416915 | Major | 360 | Review | ELVIS.CT.CHANG 張錦宗 | 770 | [JIRA](程式編輯) [IABGVOC-198] Issue 416915 - FB功能块，调整其内部变量 |
| 425835 | Major | 240 | Review | LEANN.TING 丁寧 | 735 | [JIRA] (程式編輯) [IABGVOC-189] Issue 425835 - 测试打断点时，出现报错提 |
| 466614 | Major | 400 | In Progress | STEWARD.LU 呂名峰 | 569 | [JIRA] (程式編輯) [IABGVOC-2017] In the Ladder program unit |
| 469965 | Minor | 80 | Verification | LEANN.TING 丁寧 | 555 | [JIRA] (專案管理) [IABGVOC-186] Issue 407138 - 软件下载界面：勾选下载后 |
| 486433 | Critical | 600 | Review | STEWARD.LU 呂名峰 | 492 | [JIRA] (調適) [IABGVOC-513] 增加在线时，多个变量修改状态，可以同时写入PLC功能 -  |
| 505913 | Critical | 600 | Review | PINGCHIN.WANG 王昞清 | 414 | [JIRA][efficacy](程式編輯) [IABGVOC-785] DIADesigner SP4 發生 |
| 522471 | Major | 64 | In Progress | XAVIERA.FAN 范珮欣 | 343 | [JIRA] (程式編輯) [IABGVOC-977] 与设备断线后软体还显示在线状态 |
| 528538 | Major | 240 | Verification | ARCHIE.YANG 楊浩群 | 307 | [JIRA] (程式編輯) [IABGVOC-1054] DIADesigner软件上传W3A程序及配置无法上 |
| 528531 | Major | 240 | In Progress | LUCIAN.LS.OUYANG 歐陽龍祥 | 307 | [JIRA] (程式編輯) [IABGVOC-1058] 功能块实例必须自己手敲，才会确认，不智能，应该可以自 |
| 538366 | Critical | 600 | Review | UNI.CHEN 陳軍宇 | 260 | [JIRA] (程式編輯) [IABGVOC-2032] Ladder Expression 輸出接點狀態顯示 |

### 1.6 高嚴重性 Unassigned Issue（共 9 筆）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|---|---|----|-----|-----|----|---|
| 578889 | Critical | 600 | Review | Unassigned | 23 | [JIRA] (硬體配置) [IABGVOC-1955] 重新安裝 COMMGR 後，每次在专案按了连线就会跳 |
| 563431 | Critical | 600 | Review | Unassigned | 113 | [JIRA] (調適) [IABGVOC-1532] 示波器保存的波形重新打开后发现显示的波形和我们点击的不符 |
| 562353 | Critical | 600 | Review | Unassigned | 118 | [JIRA] (調適) [IABGVOC-1506] 示波器由A专案保存，开启B专案后打开示波器后部分变量无法 |
| 578046 | Major | 400 | Review | Unassigned | 27 | [JIRA] (調適) [IABGVOC-1897] 功能块IN_OUT_PUT引脚状态无法展开监控 |
| 574859 | Major | 400 | Review | Unassigned | 49 | [JIRA] (程式編輯) [IABGVOC-1839] 更新DIADesigner 1.13.0.66_Tr |
| 571907 | Major | 400 | Review | Unassigned | 62 | [JIRA] (專案管理) [IABGVOC-1750] DIA Designer多次開啟project後，每 |
| 579005 | Major | 240 | Review | Unassigned | 22 | [JIRA] (程式編輯) [IABGVOC-1994] EXCEL导入MC_xxx FB的变量，但是在 LD |
| 579002 | Major | 240 | Review | Unassigned | 22 | [JIRA] (專案編譯) [IABGVOC-1993] 下载时还会重新编译一次(实体机、模拟器需要智能判断) |
| 578888 | Critical | 240 | Review | Unassigned | 23 | [JIRA] (網路配置) [IABGVOC-1958] EtherCAT 插入設備時彈出例外視窗 |

## 二、Requirement 進度（PM）

### 2.1 嚴重性分布

| 嚴重性 | 總數 | 開放數 | 開放率 |
|--------|------|--------|--------|
| Blocker | 19 | 8 | 42.1% |
| Critical | 28 | 9 | 32.1% |
| Major | 77 | 52 | 67.5% |
| Minor | 41 | 19 | 46.3% |

### 2.2 狀態分布

| 狀態 | 數量 |
|------|------|
| Review | 78 |
| Closed | 70 |
| Review & Approval | 7 |
| In Progress | 5 |
| Verification | 5 |

### 2.3 FMEA 風險分層（未關閉）

- 高風險（FMEA ≥ 500）：**12** 筆
- 中風險（201–499）：**41** 筆
- 低風險（0–200）：**35** 筆
- 待辦未指派（Unassigned）：**31** 筆

### 2.4 FMEA Top 20 未關閉 Requirement（PM 優先關注）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | 摘要 |
|---|---|----|-----|-----|----|---|
| 579898 | Blocker | 1000 | Review | Unassigned | 14 | [JIRA] (新增裝置) [IABGVOC-2035] SGM 標準化專案開發需求 : 軟體專案樹架構調整 |
| 562586 | Blocker | 1000 | Review | JENNY.HY.CHEN 陳湘筠 | 118 | [JIRA] (調適) [IABGVOC-1340] 支援建立多個示波器 |
| 546062 | Blocker | 1000 | Review | STEWARD.LU 呂名峰 | 212 | [JIRA] (程式編輯) [IABGVOC-774] 监控表里结构体下的VAR_IN_OUT变量在监控表里无 |
| 534083 | Blocker | 1000 | Review | Unassigned | 282 | [JIRA] (輔助工具) [IABGVOC-1120] 軟體支援輔助工具 - IO 刷新開關 |
| 509758 | Minor | 1000 | Review | JACKY.TU 杜寧 | 398 | [JIRA] (運動控制) [IABGVOC-690] 软体轴配置显示画面需要类似AX8一样能够显示轴状态，位 |
| 506831 | Major | 1000 | Review | HARVEY.XIE 謝孟軒 | 409 | [JIRA](程式編輯) [IABGVOC-505] 建控制指令的时候无法用键盘的Tab全部出来，必须打出来再 |
| 502728 | Blocker | 1000 | In Progress | KF.LIU 劉桂輔 | 427 | [JIRA](程式編輯) [IABGVOC-687] 使用ST语言编程环境下使用^符号后相关变量无法提示索引, |
| 538350 | Blocker | 1000 | Verification | JENNY.HY.CHEN 陳湘筠 | 260 | [JIRA] [實作] (調適) [IABGVOC-527] 示波器支援單/多通道切換功能 (多通道) |
| 533908 | Blocker | 1000 | Verification | FRANKNC.HO 何南瑾 | 283 | [JIRA] (網路配置) [IABGVOC-1111] AS与W3A MODBUS TCP通讯NOK,原因内 |
| 229108 | Critical | 600 | Review | STEWARD.LU 呂名峰 | 1760 | [JIRA] (調適) [IABGVOC-1873] REF_TO变量监控无法展开 |
| 527019 | Critical | 600 | In Progress | JEAN.LC.WANG 王儷臻 | 315 | [JIRA] (模組編輯) [IABGVOC-1012] R1扩展模组映射变量无法关联Byte/Word等数据 |
| 561097 | Critical | 600 | Verification | ORLANDO.LAN 藍順騰 | 125 | [JIRA] (程式編輯) [IABGVOC-1463] 变量类型支持ANY变量 |
| 578942 | Major | 400 | Review | ORLANDO.LAN 藍順騰 | 22 | [JIRA] (程式編輯) [IABGVOC-1952] 新增变数的型态可以考虑参考CODESYS :只要搜寻 |
| 574370 | Major | 400 | Review | HARVEY.XIE 謝孟軒 | 51 | [JIRA] (程式編輯) [IABGVOC-1830] ST Show Hint 希望能分段解析變數 |
| 570233 | Major | 400 | Review | JOHNNY.MC.YEH 葉明勳 | 71 | [JIRA] (調適) [IABGVOC-1705] 示波器 Monitor Type 導入A2架構的 Adr |
| 570179 | Major | 400 | Review | Unassigned | 71 | [JIRA] (調適) [IABGVOC-1703] 示波器畫布背景顏色的切換 |
| 570177 | Major | 400 | Review | Unassigned | 71 | [JIRA] (調適) [IABGVOC-1702] 示波器監控項目支援上下移動 |
| 566923 | Major | 400 | Review | STEWARD.LU 呂名峰 | 87 | [JIRA] (程式編輯) [IABGVOC-1634] FB的INOUT引脚类型，在线功能块实例列表视窗中， |
| 564587 | Major | 400 | Review | ELVIS.CT.CHANG 張錦宗 | 107 | [JIRA] (程式編輯) [IABGVOC-1585] DIADesigner 梯形圖支援空白塊輸入實例名稱 |
| 561259 | Major | 400 | Review | MICHAEL.JN.TSAI 蔡秉昌 | 122 | [JIRA] (運動控制) [IABGVOC-1476] DIADesigner软件评估能否增加：当修改轴设置 |

## 三、區域分析

| Region | Issue 總數 | Issue 開放 | Critical/Blocker Opened | Req 總數 | Req 開放 |
|------|--------|--------|-----------------------|------|------|
| IA Internal-SC | 157 | 17 | 7 | 123 | 64 |
| IA Internal-CoreTech | 75 | 8 | 1 | 15 | 5 |
| DGC-China | 20 | 10 | 3 | 23 | 16 |
| IA Internal-IMSBU | 17 | 4 | 1 | 4 | 3 |

## 四、功能模組熱點分析（功能檢點 Tag）

| 功能模組（Tag） | Issue 總數 | Issue 開放 | Req 總數 | Req 開放 | Critical/Blocker Opened |
|---------|--------|--------|------|------|-----------------------|
| `oscilloscope` | 37 | 3 | 16 | 7 | 2 |
| `motion_axisset` | 20 | 0 | 22 | 11 | 0 |
| `programming_glovar` | 21 | 4 | 16 | 7 | 2 |
| `programming_monitable` | 16 | 3 | 13 | 8 | 1 |
| `programming_lang_st_edit` | 15 | 5 | 12 | 8 | 0 |
| `devnetwork_ethercat` | 17 | 1 | 9 | 3 | 1 |
| `programming_lang_st_monitor` | 13 | 2 | 7 | 7 | 1 |
| `downloaduploadmgr` | 15 | 2 | 3 | 0 | 0 |
| `programming_lang_ld_edit` | 5 | 3 | 9 | 7 | 0 |
| `programming_compile` | 12 | 2 | 1 | 1 | 1 |
| `programming_lang_ld_monitor` | 10 | 3 | 3 | 2 | 1 |
| `programming_lang` | 8 | 0 | 1 | 1 | 0 |
| `programming_lang_ld` | 8 | 2 | 0 | 0 | 1 |
| `librarymanager` | 7 | 2 | 1 | 0 | 0 |
| `programming_poutype_fb` | 5 | 0 | 3 | 1 | 0 |
| `diadesigner_file_load` | 5 | 1 | 2 | 2 | 0 |
| `devhardware_layout_moduletable_iomap` | 4 | 1 | 2 | 1 | 1 |
| `diadesigner_edit_searchreplace` | 3 | 1 | 3 | 2 | 0 |
| `diadesigner_file_save` | 3 | 0 | 2 | 1 | 0 |
| `deverrorinfo` | 3 | 1 | 1 | 0 | 1 |

## 五、特別關注項目（step_control / 手順 / dgc_fae）

> 僅列出開放項目（State 不含 Closed / Review & Approval）

| Tag | Issue（開放）| Req（開放）| 開放合計 |
|-----|------------:|----------:|---------:|
| step_control | 10 | 15 | 25 |
| 手順 | 0 | 4 | 4 |
| dgc_fae | 5 | 12 | 17 |
| **合計** | **15** | **31** | **46** |

### 5.1 step_control（Issue + Requirement，依 FMEA 排序）

**Issue**：開放 10 筆　**Requirement**：開放 15 筆

| ID | 類型 | 嚴重性 | FMEA | State | Owner | 摘要 |
|---|---|---|----|-----|-----|---|
| 502728 | Req | Blocker | 1000 | In Progress | KF.LIU 劉桂輔 | [JIRA](程式編輯) [IABGVOC-687] 使用ST语言编程环境下使用^符号后相关变量无法提示索引, |
| 579102 | Issue | Critical | 600 | Verification | KAKA.WU 吳思言 | [JIRA] (程式編輯) [IABGVOC-2013] 及時刷新 LOG 狀態下關閉頁籤，在线仿真發生例外 |
| 574365 | Issue | Critical | 600 | Verification | UNI.CHEN 陳軍宇 | [JIRA] (程式編輯) [IABGVOC-1829] ST Pou 在線監控程序時出現 "未知序列錯誤" |
| 572378 | Issue | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | [JIRA] (程式編輯) [IABGVOC-1768] 变量表初值设定错误后无法编辑 |
| 572377 | Issue | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | [JIRA] (程式編輯) [IABGVOC-1769] ARRAY[*] OF ARRAY[*] OF 2維 |
| 538366 | Issue | Critical | 600 | Review | UNI.CHEN 陳軍宇 | [JIRA] (程式編輯) [IABGVOC-2032] Ladder Expression 輸出接點狀態顯示 |
| 229108 | Req | Critical | 600 | Review | STEWARD.LU 呂名峰 | [JIRA] (調適) [IABGVOC-1873] REF_TO变量监控无法展开 |
| 527019 | Req | Critical | 600 | In Progress | JEAN.LC.WANG 王儷臻 | [JIRA] (模組編輯) [IABGVOC-1012] R1扩展模组映射变量无法关联Byte/Word等数据 |
| 561097 | Req | Critical | 600 | Verification | ORLANDO.LAN 藍順騰 | [JIRA] (程式編輯) [IABGVOC-1463] 变量类型支持ANY变量 |
| 579103 | Issue | Major | 400 | Review | ELVIS.CT.CHANG 張錦宗 | [JIRA] (程式編輯) [IABGVOC-2014] LD中输出节点状态显示异常 |
| 578046 | Issue | Major | 400 | Review | Unassigned | [JIRA] (調適) [IABGVOC-1897] 功能块IN_OUT_PUT引脚状态无法展开监控 |
| 572461 | Issue | Major | 400 | Review | HARVEY.XIE 謝孟軒 | [JIRA] (程式編輯) [IABGVOC-1776] 程序区变量选中需要提示此变量的详细信息 |
| 572382 | Issue | Major | 400 | In Progress | MIAO.CHEN 陳炫妙 | [JIRA] (程式編輯) [IABGVOC-1771] 結構體初始值設定後報錯: "String数据类型无法 |
| 466614 | Issue | Major | 400 | In Progress | STEWARD.LU 呂名峰 | [JIRA] (程式編輯) [IABGVOC-2017] In the Ladder program unit |
| 574370 | Req | Major | 400 | Review | HARVEY.XIE 謝孟軒 | [JIRA] (程式編輯) [IABGVOC-1830] ST Show Hint 希望能分段解析變數 |
| 522465 | Req | Blocker | 400 | Review | STEWARD.LU 呂名峰 | [JIRA] (程式編輯) [IABGVOC-976] 监控表中部分变量无法监控，无法修改变量值 |
| 561761 | Req | Major | 400 | In Progress | ORLANDO.LAN 藍順騰 | [JIRA] (程式編輯) [IABGVOC-1487] 数组范围可以设定便属性为常量的变量ARRAY [0. |
| 568982 | Req | Major | 400 | Verification | ORLANDO.LAN 藍順騰 | [JIRA] (程式編輯) [IABGVOC-1666] 支援不定长数组功能如ARRAY[*,*] OF 類型 |
| 579090 | Req | Major | 240 | Review | HARVEY.XIE 謝孟軒 | [JIRA] (程式編輯) [IABGVOC-1984] 枚舉類型的變數 Show Hint 能顯示出成員名稱 |
| 575986 | Req | Major | 240 | Review | MIAO.CHEN 陳炫妙 | [JIRA] (程式編輯) [IABGVOC-1877] STRING 變量初始值設定頁面預設值需填上 '' |
| 579544 | Req | Major | 160 | Review | ELVIS.CT.CHANG 張錦宗 | [JIRA] (程式編輯) [IABGVOC-2025] LD 顯示的變量長度希望可自動調整 |
| 564593 | Req | Major | 160 | Review | Unassigned | [JIRA] (程式編輯) [IABGVOC-1580] 用户权限设定 |
| 561098 | Req | Major | 160 | Review | Unassigned | [JIRA] (程式編輯) [IABGVOC-1465] 变量交叉引用功能 |
| 502704 | Req | Major | 160 | Review | HARVEY.XIE 謝孟軒 | [JIRA](程式編輯) [IABGVOC-667] 支援完整的 Function Block 基底的繼承功能 |
| 516609 | Req | Critical | 16 | Review | MIAO.CHEN 陳炫妙 | [JIRA] (程式編輯) [IABGVOC-850] 结构体变量为数组时数组大小限定不可以为变量 |

### 5.2 手順（Issue + Requirement，依 FMEA 排序）

**Issue**：開放 0 筆　**Requirement**：開放 4 筆

| ID | 類型 | 嚴重性 | FMEA | State | Owner | 摘要 |
|---|---|---|----|-----|-----|---|
| 579898 | Req | Blocker | 1000 | Review | Unassigned | [JIRA] (新增裝置) [IABGVOC-2035] SGM 標準化專案開發需求 : 軟體專案樹架構調整 |
| 579939 | Req | Major | 240 | Review | STEWARD.LU 呂名峰 | [JIRA] (程式編輯) [IABGVOC-2037] ENUM 變數監控賦值功能優化 |
| 579884 | Req | Major | 240 | Review | Unassigned | [JIRA] (專案管理) [IABGVOC-2030] 使用者再開啟專案後，能自動回復上次開啟的介面 |
| 579894 | Req | Major | 160 | Review | ELVIS.CT.CHANG 張錦宗 | [JIRA] (程式編輯) [IABGVOC-2034] 梯形圖接點、輸出線圈右鍵選單內容優化 |

### 5.3 dgc_fae（Issue + Requirement，依 FMEA 排序）

**Issue**：開放 5 筆　**Requirement**：開放 12 筆

| ID | 類型 | 嚴重性 | FMEA | State | Owner | 摘要 |
|---|---|---|----|-----|-----|---|
| 578889 | Issue | Critical | 600 | Review | Unassigned | [JIRA] (硬體配置) [IABGVOC-1955] 重新安裝 COMMGR 後，每次在专案按了连线就会跳 |
| 578942 | Req | Major | 400 | Review | ORLANDO.LAN 藍順騰 | [JIRA] (程式編輯) [IABGVOC-1952] 新增变数的型态可以考虑参考CODESYS :只要搜寻 |
| 523235 | Req | Major | 400 | Review | HARVEY.XIE 謝孟軒 | [JIRA] (survey)(程式編輯) [IABGVOC-1954] ST Online模式下的監控行距調 |
| 579005 | Issue | Major | 240 | Review | Unassigned | [JIRA] (程式編輯) [IABGVOC-1994] EXCEL导入MC_xxx FB的变量，但是在 LD |
| 579002 | Issue | Major | 240 | Review | Unassigned | [JIRA] (專案編譯) [IABGVOC-1993] 下载时还会重新编译一次(实体机、模拟器需要智能判断) |
| 578892 | Issue | Major | 240 | Review | HARVEY.XIE 謝孟軒 | [JIRA] (程式編輯) [IABGVOC-1964] 梯形图下Axis1的轴变量无法将其他类似位置等变量列 |
| 578888 | Issue | Critical | 240 | Review | Unassigned | [JIRA] (網路配置) [IABGVOC-1958] EtherCAT 插入設備時彈出例外視窗 |
| 581522 | Req | Major | 240 | Review | Unassigned | [JIRA] (手冊) [IABGVOC-2002] 軟體手冊內容、功能優化 |
| 581078 | Req | Major | 240 | Review | LEANN.TING 丁寧 | [JIRA] (輔助工具) [IABGVOC-2041] 万年历功能 |
| 579933 | Req | Major | 240 | Review | JACKY.TU 杜寧 | [JIRA] (運動控制) [IABGVOC-1996] 轴参数画面配置画面参考AX8配置第三方电机（比亚迪） |
| 579887 | Req | Major | 240 | Review | Unassigned | [JIRA] (運動控制) [IABGVOC-1991] 齿比设定参考: AX的直线电机UI |
| 579097 | Req | Major | 240 | Review | Unassigned | [JIRA] (程式編輯) [IABGVOC-2001] 指令精靈選擇 DL 庫時難以快速查找 |
| 579095 | Req | Major | 240 | Review | ELVIS.CT.CHANG 張錦宗 | [JIRA] (程式編輯) [IABGVOC-2004] LD插入功能块按鈕新增, 带EN,ENO, 不帶 E |
| 579092 | Req | Major | 240 | Review | JACKY.TU 杜寧 | [JIRA] (運動控制) [IABGVOC-2005] 新增轴，不能直接输入中文，需要以字母为首 |
| 579089 | Req | Major | 240 | Review | Unassigned | [JIRA] (程式編輯) [IABGVOC-2000] 離線模式下可展開陣列、結構體變數且得知位址資訊 |
| 578879 | Req | Major | 240 | Review | Unassigned | [JIRA] (專案管理) [IABGVOC-1961] 监控表不能放到屏幕下方，只能放在两侧，监控变量时不方 |
| 578890 | Req | Minor | 120 | Review | JACKY.TU 杜寧 | [JIRA] (運動控制) [IABGVOC-1960] 运动参数设置，默認速度值與仿真測試初始值不符 |

## 六、歷年趨勢分析

| 年份 | Issue 新增 | Issue 關閉 | Issue 解決率 | Req 新增 | Req 關閉 | Req 解決率 |
|---|--------|--------|---------|------|------|-------|
| 2021 | 0 | 0 | -% | 1 | 0 | 0.0% |
| 2022 | 0 | 0 | -% | 1 | 0 | 0.0% |
| 2023 | 31 | 2 | 6.5% | 3 | 0 | 0.0% |
| 2024 | 39 | 31 | 79.5% | 12 | 0 | 0.0% |
| 2025 | 159 | 150 | 94.3% | 85 | 43 | 50.6% |
| 2026 | 40 | 47 | 117.5% | 63 | 34 | 54.0% |

## 建議事項（Recommendations）

### PM
1. 優先推動 FMEA ≥ 500 的 12 筆高風險 Requirement 排入近期版本規劃，避免持續積壓。
2. 對 Unassigned 的 31 筆開放 Requirement 進行責任指派，降低 Backlog 盲點。
3. 針對 Top 20 FMEA Requirement，召集 RD/TE 評估可交付版本，並更新 Planned For 欄位。

### RD Leader
1. 解決 9 筆高嚴重性 Unassigned Issue，明確指派負責人。
2. 檢視 Owner 分布，避免少數人員過度集中，規劃工作分擔。
3. 確認各版本（Planned For）的 Issue 完成率，對接近截止的版本提前介入。

### TE Leader
1. 集中測試驗證 12 筆未關閉的 Critical/Blocker Issue，確保 State 推進至 Verification→Closed。
2. 對 15 筆老化 Issue（>180天）逐一確認是否已完成但未更新 State，或需要重新排程。
3. 追蹤 `step_control` / `手順` 相關 Issue 的驗證進度，確保手順邏輯正確性。

### 部門主管
1. 目前 Critical/Blocker 開放數為 12，建議設定每週清零目標並追蹤。
2. FMEA 高風險 Requirement 有 12 筆待處理，建議 PM 召開優先級對齊會議。
3. 關注 DGC-China 區域需求（dgc_fae）的回應速度，確保客戶關係維繫。

## 附錄（Appendix）

### A. 全部 Critical/Blocker 開放 Issue

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | Region | 摘要 |
|---|---|----|-----|-----|----|------|---|
| 581951 | Blocker | 1000 | Verification | JEAN.LC.WANG 王儷臻 | 3 | IA Internal-IMSBU | [JIRA] (程式編輯) [IABGVOC-2091] W3A 專案編譯時出現多筆 C0115 Overma |
| 579102 | Critical | 600 | Verification | KAKA.WU 吳思言 | 22 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-2013] 及時刷新 LOG 狀態下關閉頁籤，在线仿真發生例外 |
| 578889 | Critical | 600 | Review | Unassigned | 23 | DGC-China | [JIRA] (硬體配置) [IABGVOC-1955] 重新安裝 COMMGR 後，每次在专案按了连线就会跳 |
| 574365 | Critical | 600 | Verification | UNI.CHEN 陳軍宇 | 51 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1829] ST Pou 在線監控程序時出現 "未知序列錯誤" |
| 572378 | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | 58 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1768] 变量表初值设定错误后无法编辑 |
| 572377 | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | 58 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1769] ARRAY[*] OF ARRAY[*] OF 2維 |
| 563431 | Critical | 600 | Review | Unassigned | 113 | IA Internal-SC | [JIRA] (調適) [IABGVOC-1532] 示波器保存的波形重新打开后发现显示的波形和我们点击的不符 |
| 562353 | Critical | 600 | Review | Unassigned | 118 | IA Internal-SC | [JIRA] (調適) [IABGVOC-1506] 示波器由A专案保存，开启B专案后打开示波器后部分变量无法 |
| 538366 | Critical | 600 | Review | UNI.CHEN 陳軍宇 | 260 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-2032] Ladder Expression 輸出接點狀態顯示 |
| 505913 | Critical | 600 | Review | PINGCHIN.WANG 王昞清 | 414 | IA Internal-CoreTech | [JIRA][efficacy](程式編輯) [IABGVOC-785] DIADesigner SP4 發生 |
| 486433 | Critical | 600 | Review | STEWARD.LU 呂名峰 | 492 | DGC-China | [JIRA] (調適) [IABGVOC-513] 增加在线时，多个变量修改状态，可以同时写入PLC功能 -  |
| 578888 | Critical | 240 | Review | Unassigned | 23 | DGC-China | [JIRA] (網路配置) [IABGVOC-1958] EtherCAT 插入設備時彈出例外視窗 |

### B. 老化 Issue 完整清單（>180 天，共 15 筆）

| ID | 嚴重性 | FMEA | State | Owner | 開放天數 | Region | 摘要 |
|---|---|----|-----|-----|----|------|---|
| 383486 | Major | 80 | Verification | LUCIAN.LS.OUYANG 歐陽龍祥 | 906 | IA Internal-CoreTech | [JIRA] (調適) [IABGVOC-177] Issue 383486 - 在online monito |
| 386302 | Major | 120 | In Progress | LUCIAN.LS.OUYANG 歐陽龍祥 | 895 | IA Internal-CoreTech | [JIRA] (程式編輯) [IABGVOC-183] Issue 386302 - DIADesigner庫 |
| 410331 | Minor | 120 | Review | MIAO.CHEN 陳炫妙 | 797 | IA Internal-CoreTech | [JIRA](程式編輯) [IABGVOC-193] Issue 410331 - 热键：跳转到变量表，能否增 |
| 412810 | Major | 240 | Review | HARVEY.XIE 謝孟軒 | 787 | IA Internal-CoreTech | [JIRA] (程式編輯) [IABGVOC-196] CORNER-3323 - ST语法中TO_TIME( |
| 416557 | Major | 240 | Review | STEWARD.LU 呂名峰 | 771 | IA Internal-CoreTech | [JIRA] (線上斷線) [IABGVOC-197] Issue 416557 - 在线时拔掉电脑与W3A的 |
| 416915 | Major | 360 | Review | ELVIS.CT.CHANG 張錦宗 | 770 | IA Internal-CoreTech | [JIRA](程式編輯) [IABGVOC-198] Issue 416915 - FB功能块，调整其内部变量 |
| 425835 | Major | 240 | Review | LEANN.TING 丁寧 | 735 | IA Internal-CoreTech | [JIRA] (程式編輯) [IABGVOC-189] Issue 425835 - 测试打断点时，出现报错提 |
| 466614 | Major | 400 | In Progress | STEWARD.LU 呂名峰 | 569 | DGC-China | [JIRA] (程式編輯) [IABGVOC-2017] In the Ladder program unit |
| 469965 | Minor | 80 | Verification | LEANN.TING 丁寧 | 555 | DGC-China | [JIRA] (專案管理) [IABGVOC-186] Issue 407138 - 软件下载界面：勾选下载后 |
| 486433 | Critical | 600 | Review | STEWARD.LU 呂名峰 | 492 | DGC-China | [JIRA] (調適) [IABGVOC-513] 增加在线时，多个变量修改状态，可以同时写入PLC功能 -  |
| 505913 | Critical | 600 | Review | PINGCHIN.WANG 王昞清 | 414 | IA Internal-CoreTech | [JIRA][efficacy](程式編輯) [IABGVOC-785] DIADesigner SP4 發生 |
| 522471 | Major | 64 | In Progress | XAVIERA.FAN 范珮欣 | 343 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-977] 与设备断线后软体还显示在线状态 |
| 528538 | Major | 240 | Verification | ARCHIE.YANG 楊浩群 | 307 | DGC-China | [JIRA] (程式編輯) [IABGVOC-1054] DIADesigner软件上传W3A程序及配置无法上 |
| 528531 | Major | 240 | In Progress | LUCIAN.LS.OUYANG 歐陽龍祥 | 307 | DGC-China | [JIRA] (程式編輯) [IABGVOC-1058] 功能块实例必须自己手敲，才会确认，不智能，应该可以自 |
| 538366 | Critical | 600 | Review | UNI.CHEN 陳軍宇 | 260 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-2032] Ladder Expression 輸出接點狀態顯示 |

### C. step_control / 手順 / dgc_fae 完整項目列表

#### C1. Issue

| ID | Tag | 嚴重性 | FMEA | State | Owner | Region | 摘要 |
|---|---|---|----|-----|-----|------|---|
| 561272 | step_control | Blocker | 1000 | Closed | STEWARD.LU 呂名峰 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1461] 程序区變量監控格顯示為空 |
| 528236 | step_control | Blocker | 1000 | Closed | KF.LIU 劉桂輔 | IA Internal-SC | [JIRA] (模組編輯) [IABGVOC-1067] 程序区变量监控遇到ARRAY [*] OF BYTE |
| 579102 | step_control | Critical | 600 | Verification | KAKA.WU 吳思言 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-2013] 及時刷新 LOG 狀態下關閉頁籤，在线仿真發生例外 |
| 578889 | dgc_fae | Critical | 600 | Review | Unassigned | DGC-China | [JIRA] (硬體配置) [IABGVOC-1955] 重新安裝 COMMGR 後，每次在专案按了连线就会跳 |
| 574365 | step_control | Critical | 600 | Verification | UNI.CHEN 陳軍宇 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1829] ST Pou 在線監控程序時出現 "未知序列錯誤" |
| 572963 | step_control | Critical | 600 | Closed | HARVEY.XIE 謝孟軒 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1794] ST 解析特定語法下出現例外錯誤 : "序列未包含項 |
| 572378 | step_control | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1768] 变量表初值设定错误后无法编辑 |
| 572377 | step_control | Critical | 600 | In Progress | MIAO.CHEN 陳炫妙 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1769] ARRAY[*] OF ARRAY[*] OF 2維 |
| 538366 | step_control | Critical | 600 | Review | UNI.CHEN 陳軍宇 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-2032] Ladder Expression 輸出接點狀態顯示 |
| 527679 | step_control | Critical | 600 | Closed | ORLANDO.LAN 藍順騰 | IA Internal-SC | [JIRA] (模組編輯) [IABGVOC-1061] VAR RETAIN/RETAIN_M 問題反饋 ( |
| 579103 | step_control | Major | 400 | Review | ELVIS.CT.CHANG 張錦宗 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-2014] LD中输出节点状态显示异常 |
| 578046 | step_control | Major | 400 | Review | Unassigned | IA Internal-SC | [JIRA] (調適) [IABGVOC-1897] 功能块IN_OUT_PUT引脚状态无法展开监控 |
| 572461 | step_control | Major | 400 | Review | HARVEY.XIE 謝孟軒 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1776] 程序区变量选中需要提示此变量的详细信息 |
| 572460 | step_control | Major | 400 | Review & Approval | JASON.JY.LIN 林峻宇 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1770] 联合体/结构体没办法声明Array [*] OF A |
| 572382 | step_control | Major | 400 | In Progress | MIAO.CHEN 陳炫妙 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1771] 結構體初始值設定後報錯: "String数据类型无法 |
| 520738 | step_control | Major | 400 | Closed | KF.LIU 劉桂輔 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-961] POU中添加函数，函数引脚无赋值符，引脚无相关说明 |
| 466614 | step_control | Major | 400 | In Progress | STEWARD.LU 呂名峰 | DGC-China | [JIRA] (程式編輯) [IABGVOC-2017] In the Ladder program unit |
| 579098 | dgc_fae | Major | 240 | Closed | JOHNNY.MC.YEH 葉明勳 | IA Internal-SC | [JIRA] (調適) [IABGVOC-1999] 示波器监控无曲线，无值，属于已知问题 |
| 579005 | dgc_fae | Major | 240 | Review | Unassigned | DGC-China | [JIRA] (程式編輯) [IABGVOC-1994] EXCEL导入MC_xxx FB的变量，但是在 LD |
| 579002 | dgc_fae | Major | 240 | Review | Unassigned | DGC-China | [JIRA] (專案編譯) [IABGVOC-1993] 下载时还会重新编译一次(实体机、模拟器需要智能判断) |
| 578892 | dgc_fae | Major | 240 | Review | HARVEY.XIE 謝孟軒 | DGC-China | [JIRA] (程式編輯) [IABGVOC-1964] 梯形图下Axis1的轴变量无法将其他类似位置等变量列 |
| 578888 | dgc_fae | Critical | 240 | Review | Unassigned | DGC-China | [JIRA] (網路配置) [IABGVOC-1958] EtherCAT 插入設備時彈出例外視窗 |
| 578885 | dgc_fae | Major | 240 | Closed | Unassigned | DGC-China | [JIRA] (調適) [IABGVOC-1959] 示波器：轴监控选择Motion_Tag_Table.Ax |
| 574868 | step_control | Major | 240 | Review & Approval | KF.LIU 劉桂輔 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1840] ST Call FB.Method 後不應彈出新增變 |
| 524836 | step_control | Major | 240 | Closed | KF.LIU 劉桂輔 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1015] FC函数调用POU区经常提示相关引脚变量未声明 |
| 578880 | dgc_fae | Minor | 120 | Review & Approval | XAVIERA.FAN 范珮欣 | DGC-China | [JIRA] (硬體配置) [IABGVOC-1965] 下方狀態列仿真器名称不符 |
| 517915 | step_control | Minor | 40 | Closed | JACKY.TU 杜寧 | IA Internal-SC | [JIRA] (運動控制) [IABGVOC-931] 轴组态界面位置显示精度设定默认值 |

#### C2. Requirement

| ID | Tag | 嚴重性 | FMEA | State | Owner | Region | 摘要 |
|---|---|---|----|-----|-----|------|---|
| 579898 | 手順 | Blocker | 1000 | Review | Unassigned | IA Internal-SC | [JIRA] (新增裝置) [IABGVOC-2035] SGM 標準化專案開發需求 : 軟體專案樹架構調整 |
| 502728 | step_control | Blocker | 1000 | In Progress | KF.LIU 劉桂輔 | IA Internal-SC | [JIRA](程式編輯) [IABGVOC-687] 使用ST语言编程环境下使用^符号后相关变量无法提示索引, |
| 229108 | step_control | Critical | 600 | Review | STEWARD.LU 呂名峰 | IA Internal-SC | [JIRA] (調適) [IABGVOC-1873] REF_TO变量监控无法展开 |
| 527019 | step_control | Critical | 600 | In Progress | JEAN.LC.WANG 王儷臻 | IA Internal-SC | [JIRA] (模組編輯) [IABGVOC-1012] R1扩展模组映射变量无法关联Byte/Word等数据 |
| 561097 | step_control | Critical | 600 | Verification | ORLANDO.LAN 藍順騰 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1463] 变量类型支持ANY变量 |
| 578942 | dgc_fae | Major | 400 | Review | ORLANDO.LAN 藍順騰 | DGC-China | [JIRA] (程式編輯) [IABGVOC-1952] 新增变数的型态可以考虑参考CODESYS :只要搜寻 |
| 574370 | step_control | Major | 400 | Review | HARVEY.XIE 謝孟軒 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1830] ST Show Hint 希望能分段解析變數 |
| 523235 | dgc_fae | Major | 400 | Review | HARVEY.XIE 謝孟軒 | DGC-China | [JIRA] (survey)(程式編輯) [IABGVOC-1954] ST Online模式下的監控行距調 |
| 522465 | step_control | Blocker | 400 | Review | STEWARD.LU 呂名峰 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-976] 监控表中部分变量无法监控，无法修改变量值 |
| 561761 | step_control | Major | 400 | In Progress | ORLANDO.LAN 藍順騰 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1487] 数组范围可以设定便属性为常量的变量ARRAY [0. |
| 568982 | step_control | Major | 400 | Verification | ORLANDO.LAN 藍順騰 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1666] 支援不定长数组功能如ARRAY[*,*] OF 類型 |
| 581522 | dgc_fae | Major | 240 | Review | Unassigned | DGC-China | [JIRA] (手冊) [IABGVOC-2002] 軟體手冊內容、功能優化 |
| 581078 | dgc_fae | Major | 240 | Review | LEANN.TING 丁寧 | IA Internal-SC | [JIRA] (輔助工具) [IABGVOC-2041] 万年历功能 |
| 579939 | 手順 | Major | 240 | Review | STEWARD.LU 呂名峰 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-2037] ENUM 變數監控賦值功能優化 |
| 579933 | dgc_fae | Major | 240 | Review | JACKY.TU 杜寧 | DGC-China | [JIRA] (運動控制) [IABGVOC-1996] 轴参数画面配置画面参考AX8配置第三方电机（比亚迪） |
| 579887 | dgc_fae | Major | 240 | Review | Unassigned | DGC-China | [JIRA] (運動控制) [IABGVOC-1991] 齿比设定参考: AX的直线电机UI |
| 579884 | 手順 | Major | 240 | Review | Unassigned | IA Internal-SC | [JIRA] (專案管理) [IABGVOC-2030] 使用者再開啟專案後，能自動回復上次開啟的介面 |
| 579097 | dgc_fae | Major | 240 | Review | Unassigned | DGC-China | [JIRA] (程式編輯) [IABGVOC-2001] 指令精靈選擇 DL 庫時難以快速查找 |
| 579095 | dgc_fae | Major | 240 | Review | ELVIS.CT.CHANG 張錦宗 | DGC-China | [JIRA] (程式編輯) [IABGVOC-2004] LD插入功能块按鈕新增, 带EN,ENO, 不帶 E |
| 579092 | dgc_fae | Major | 240 | Review | JACKY.TU 杜寧 | DGC-China | [JIRA] (運動控制) [IABGVOC-2005] 新增轴，不能直接输入中文，需要以字母为首 |
| 579090 | step_control | Major | 240 | Review | HARVEY.XIE 謝孟軒 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1984] 枚舉類型的變數 Show Hint 能顯示出成員名稱 |
| 579089 | dgc_fae | Major | 240 | Review | Unassigned | DGC-China | [JIRA] (程式編輯) [IABGVOC-2000] 離線模式下可展開陣列、結構體變數且得知位址資訊 |
| 578879 | dgc_fae | Major | 240 | Review | Unassigned | DGC-China | [JIRA] (專案管理) [IABGVOC-1961] 监控表不能放到屏幕下方，只能放在两侧，监控变量时不方 |
| 575986 | step_control | Major | 240 | Review | MIAO.CHEN 陳炫妙 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1877] STRING 變量初始值設定頁面預設值需填上 '' |
| 578951 | dgc_fae | Major | 240 | Closed | Unassigned | DGC-China | [JIRA] (專案管理) [IABGVOC-1963] 下载时没有进度条 |
| 578948 | dgc_fae | Major | 240 | Closed | Unassigned | DGC-China | [JIRA] (程式編輯) [IABGVOC-1962] 程序页面中变量区域，变量不能展开看到内部参数 |
| 511568 | step_control | Critical | 240 | Closed | KF.LIU 劉桂輔 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-834] 建立结构体时无法对变量进行初始化赋值 |
| 572358 | step_control | Minor | 200 | Review & Approval | ORLANDO.LAN 藍順騰 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1767] 变量表信息展示不完全 |
| 579894 | 手順 | Major | 160 | Review | ELVIS.CT.CHANG 張錦宗 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-2034] 梯形圖接點、輸出線圈右鍵選單內容優化 |
| 579544 | step_control | Major | 160 | Review | ELVIS.CT.CHANG 張錦宗 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-2025] LD 顯示的變量長度希望可自動調整 |
| 564593 | step_control | Major | 160 | Review | Unassigned | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1580] 用户权限设定 |
| 561098 | step_control | Major | 160 | Review | Unassigned | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-1465] 变量交叉引用功能 |
| 502704 | step_control | Major | 160 | Review | HARVEY.XIE 謝孟軒 | IA Internal-SC | [JIRA](程式編輯) [IABGVOC-667] 支援完整的 Function Block 基底的繼承功能 |
| 578890 | dgc_fae | Minor | 120 | Review | JACKY.TU 杜寧 | DGC-China | [JIRA] (運動控制) [IABGVOC-1960] 运动参数设置，默認速度值與仿真測試初始值不符 |
| 516609 | step_control | Critical | 16 | Review | MIAO.CHEN 陳炫妙 | IA Internal-SC | [JIRA] (程式編輯) [IABGVOC-850] 结构体变量为数组时数组大小限定不可以为变量 |

## 附錄 D — 稽核資料（Audit）

> 此區段由腳本自動產生，用於驗證報告數字的正確性。請在閱讀報告前確認下方數值與 JIRA 一致。

| 項目 | 數值 |
|------|------|
| Issue CSV 載入筆數 | 269 |
| Requirement CSV 載入筆數 | 165 |
| 基準日期（TODAY） | 2026-05-21 |
| is_open 排除的 State | Closed, Review & Approval |
| Issue State 分布 | Closed:221、Review:24、Review & Approval:9、In Progress:8、Verification:7 |
| Req State 分布 | Review:78、Closed:70、Review & Approval:7、In Progress:5、Verification:5 |
| 日期解析失敗（Issue） | 0 |
| 日期解析失敗（Req） | 0 |
| FMEA 解析失敗（Issue） | 0 |
| FMEA 解析失敗（Req） | 0 |
| 開放 Issue 數（計算結果） | 39 |
| 開放 Req 數（計算結果） | 88 |
| 開放數一致性自檢 | ✅ 通過 |

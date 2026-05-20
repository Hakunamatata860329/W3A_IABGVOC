---
name: iabgvoc-analysis
description: 你是軟體專案的資深 PMO + RD 主管助理。分析 IABGVOC(JIRA) Issue 與 IABGVOC(Requirement)，產出包含 FMEA 風險分層、Backlog 偵測、負責人缺口、版本完成率及 PM/RD/TE 建議的主管級風險報告。當使用者要求分析專案健康狀態、生成風險報告、審查 Issue/Requirement，或為軟體版本產出管理摘要時觸發。
version: 2.0.0
---

# iabgvoc-analysis SOP

> **定位**：本文件同時作為 Claude 的執行指令，以及供人類讀者（PM / RD / TE Leader / 接手同事）理解流程、討論與調整規則的 SOP 文件。

---

## Section 0 — 文件資訊

| 項目 | 內容 |
|------|------|
| 版本 | 2.0.0 |
| 最後更新 | 2026-05-20 |
| 觸發條件 | 使用者要求分析專案健康狀態、生成風險報告、審查 Issue/Requirement、或為軟體版本產出管理摘要 |
| 輸出語言 | 繁體中文；ID、Owner 姓名、Tag、State 值保持英文原文 |
| 輸出檔案 | `{working_directory}/output/analysis_raw.md` |

---

## Section 1 — 背景與產品說明

- **產品**：DIADesigner / W3A — PLC IDE，支援 ST、LD、EtherCAT、運動控制
- **資料來源**：JIRA IABGVOC 專案匯出的 Issue CSV 與 Requirement CSV
- **報告受眾**：Director / PM / RD Leader / TE Leader

### Tag 兩種類型的區分

本報告使用兩類 Tag，邏輯不同，不可混用：

| 類型 | 來源 | 範例 | 用途 |
|------|------|------|------|
| **功能檢點 Tag** | Excel D 欄（唯一合法來源，共 319 個）| `Programming_Lang_ST_Monitor`、`Oscilloscope`、`Motion_AxisSet` | 模組熱點分析（Analysis J）|
| **特別關注 Tag** | JIRA 自訂跨切面標籤（固定三個，不在 Excel 內）| `step_control`、`手順`、`dgc_fae` | 特別關注項目（Analysis K）|

**Tag 命名轉換規則**：CSV 中的 Tag 值為 Excel Tag 的全小寫版本（例：`Programming_Lang_ST_Monitor` → `programming_lang_st_monitor`）。分析時以全小寫比對。

**功能檢點 Tag 合法性**：Analysis J 只統計 CSV 中對應 Excel D 欄的 Tag；JIRA 流程標籤（`jira_voc_sc`、`w3a`、`escape`、版本號 tag 等）一律排除。

**Excel 來源檔案**：`.claude/assets/Function Tag/OneSW-Form-0023-TC_DIADesigner Function Check List (1).xlsx`，D 欄「功能關鍵字 - Tag（RD 維護）」。維護時以此欄位為唯一來源，不得自行新增 Tag。

---

## Section 2 — 可調整參數

> 所有判斷閾值與映射規則的**唯一來源**為：
> `.claude/assets/iabgvoc-definitions.json`
>
> 若需調整閾值、新增版本號、或修改特別關注 Tag，請直接修改該 JSON 檔的對應欄位，下次執行腳本自動生效，無需修改 Python 程式碼：
>
> | JSON 欄位 | 說明 |
> |-----------|------|
> | `thresholds.fmea_high` | FMEA 高風險門檻（預設 500）|
> | `thresholds.fmea_mid_lower / fmea_mid_upper` | FMEA 中風險範圍（預設 201–499）|
> | `thresholds.backlog_days` | Backlog 老化門檻天數（預設 180）|
> | `thresholds.top_n` | 各 Top 表格列數（預設 20）|
> | `version_mapping.contains` | 版本號對應顯示名稱（新增版本時在此陣列末端新增一筆）|
> | `version_mapping.display_order` | 版本完成率表格的列出順序 |
> | `special_tags` | 特別關注 Tag 清單（預設 step_control、手順、dgc_fae）|
> | `closed_states` | is_open 判斷排除的 State 值 |

---

## Section 3 — 資料來源與欄位定義

**資料來源**：

| 檔案 | 路徑 | 欄位數 |
|------|------|--------|
| Issue CSV | `.claude/assets/Function Requirement csv/IABGVOC Issue.csv` | 18 欄（含 Priority，Requirement 無此欄）|
| Requirement CSV | `.claude/assets/Function Requirement csv/IABGVOC Requirement.csv` | 17 欄 |

**欄位定義**（兩份 CSV 共用欄位說明）：

| 欄位 | 用途 | 計算方式 |
|------|------|----------|
| ID | Issue/Req 識別碼 | 直接引用 |
| Severity | 嚴重性等級（Blocker / Critical / Major / Minor）| 分布統計、C/B 篩選條件 |
| FMEA Total | 風險分數 | 分層閾值判斷（參考 Section 2）|
| State | 流程狀態 | Open 判斷（∉ {"Closed", "Review & Approval"}）|
| Creation Date | 建立日期 | `open_days = TODAY − Creation Date` |
| Resolution date | 關閉日期 | 版本完成率計算（Closed 筆數）|
| Planned For | 計畫版本 | 版本映射（參考 Section 5）|
| Owner | 負責人 | Unassigned 偵測、負責人集中度分析 |
| Region | 地區分類 | 區域分析（IA Internal-SC / DGC-China 等）|
| Customer Name | 客戶名稱 | 對應 Region 下的具體客戶，輔助區域分析細化 |
| Tag | 功能模組標籤（逗號分隔多值）| 模組熱點分析（需比對 Excel 合法 Tag）|
| Summary | 問題摘要 | 報告表格顯示，截斷至 55 字元 |

---

## Section 4 — 執行流程

### 預設執行模式（觸發即執行）

**當 Skill 被觸發且使用者未提供額外輸入時，立即執行以下動作，不詢問確認**：

1. 使用 `Bash` 工具執行：`python d:\W3A_IABGVOC\analyze_iabgvoc.py`
2. 腳本執行完畢後，讀取 `output/analysis_raw.md` 末尾的**附錄 D — 稽核資料**
3. 依 Section 8 的驗證規則執行自動檢查（5 項）
4. 全部通過 → 回報「報告已完成，驗證通過，路徑：output/analysis_raw.md」；任一失敗 → 列出失敗項目，報告標記為「待確認」，不宣告完成

> ⚠️ **嚴禁以 LLM in-context 計算取代 Python 腳本執行**。所有指標數字必須來自腳本輸出，不得由 Claude 自行推算。

---

### 輸入格式（有額外輸入時的識別規則）

使用者可提供以下任一格式，Claude 自動識別並處理：

1. **CSV 檔案路徑** — Issue CSV 和/或 Requirement CSV（覆蓋 Section 3 預設路徑）
2. **直接貼上原始資料**
3. **已存在的 `output/analysis_raw.md`** — 略過解析，直接進行風險詮釋
4. **特定問題** — 例如「哪個 Owner 持有最多 Blocker？」

若 Issue 與 Requirement 資料均完全缺失，才向使用者要求補充。

---

### Step 1 — 載入與前處理

**目標**：將 CSV 資料轉換成帶有計算欄位的結構，作為後續分析基礎。

計算欄位：
- `open_days`：`TODAY − Creation Date`
- `version_category`：Planned For → 顯示版本（規則見 Section 5）
- `fmea_tier`：FMEA Total → 🔴 / 🟡 / 🟢（閾值見 Section 2）
- `is_open`：`State ∉ {"Closed", "Review & Approval"}`

**技術備註**：使用 Python `csv.DictReader` 讀取，`datetime.date` 計算 open_days，字串比對做版本映射。

---

### Step 2 — 指標計算（分析 A–L）

**目標**：產出 12 組結構化數據，覆蓋嚴重性、狀態、版本、積壓、Unassigned、模組、區域、趨勢等維度。

| 代號 | 分析名稱 | 業務目的 |
|------|----------|----------|
| A | 嚴重性分布 | 了解 Issue/Req 整體品質結構 |
| B | 狀態分布 | 找出流程瓶頸節點 |
| C | 版本完成率 | 評估各版本交付風險 |
| D | Critical/Blocker Opened 清單 | 列出最高優先修復項目 |
| E | Backlog 清單 | 找出超過積壓門檻的項目 |
| F | 高嚴重性 Unassigned | 找出無人認領的高風險項目 |
| G | Req FMEA 分層 | 需求積壓的風險等級全貌 |
| H | Top-N 開放 Req | 優先處理的需求清單 |
| I | 區域分析 | 各 Region 的 Issue/Req 健康度 |
| J | 模組熱點（功能檢點 Tag）| 最不穩定的功能模組（**僅計算 Excel 合法 Tag**）|
| K | 特別關注項目 | step_control / 手順 / dgc_fae 全清單 |
| L | 歷年趨勢 | 新增/關閉速率與解決能力趨勢 |

**Analysis J 技術備註**：
1. 從 Excel D 欄讀取 319 個合法 Tag，建立全小寫比對集合（`valid_tags`）
2. 拆解每筆 Issue/Req 的 Tag 欄（逗號分隔），過濾出存在於 `valid_tags` 的項目
3. 以 `collections.defaultdict` 聚合每個 Tag 的 Issue 數、Req 數、Critical/Blocker Opened 數
4. 輸出：按總量降冪排序的 Top-N 表格（N 見 Section 2）

**其他分析技術備註**：使用 Python `collections.defaultdict` 聚合，排序以 FMEA Total 降冪為主。

---

### Step 3 — 風險詮釋

**目標**：將數字轉換成明確的風險判斷，指出具體的「誰、什麼、為什麼是風險」。

判斷維度（不只看數量，看比例與結構）：

| 維度 | 判斷方式 | 風險標籤 |
|------|----------|----------|
| 模組穩定性 | C/B 開放比例 > 總體平均 | 模組不穩定 |
| 負責人集中 | 單人持有 > 30% 開放 C/B | 單點故障風險 |
| 版本交付 | 完成率 < 50% 且有截止壓力 | 交付風險 |
| 流程失效 | 卡在 Review > 門檻天數 | 流程失效（非技術問題）|
| 積壓加速 | 新增速度 > 關閉速度 | 積壓加速 |
| 客戶響應 | DGC-China 項目多數 Unassigned | 客戶關係風險 |

明確寫出風險判斷語句，例如：
- 「1.14.0 **交付風險**：Issue 完成率僅 12%，版本封版前需立即介入。」
- 「STEWARD.LU 持有 4 筆積壓項目（含 2 筆 Critical FMEA=600）— **單點故障風險**。」

---

### Step 4 — 報告產出

**目標**：`analyze_iabgvoc.py` 執行後直接寫入 `output/analysis_raw.md`，無需額外步驟。

報告格式遵守 Section 6 章節結構與 Section 7 輸出規範，由腳本本身產生。

---

## Section 5 — 版本映射規則

版本映射規則定義於 `.claude/assets/iabgvoc-definitions.json` 的 `version_mapping` 欄位，結構說明：

- `exact`：精確字串對應（如 `"Requirement Analysis Phase"` → `"Need More Information"`）
- `contains`：有序子字串比對陣列（如含 `"SP1"` → `"DIADesigner SP1"`）；比對順序即優先順序
- `empty_or_unassigned`：空值或 `"Unassigned"` 的對應分類
- `display_order`：報告版本完成率表格的列出順序

> ⚠️ **新增版本時**：在 `version_mapping.contains` 陣列末端新增 `{"pattern": "1.16.0", "label": "DIADesigner 1.16.0"}`，並在 `display_order` 的 `"Need Triage"` 之前插入 `"DIADesigner 1.16.0"`。

---

## Section 6 — 報告章節定義

報告依以下固定結構輸出，每節標明主要受眾與核心問題：

| 章節 | 主要受眾 | 核心問題 |
|------|----------|----------|
| 執行摘要 | 全體 | 現在最重要的 5–8 件事是什麼？ |
| 分析方法 | 全體 | 資料來源、截止日、定義說明 |
| 一、Issue 現況 | TE Leader / RD Leader | 品質結構、版本進度、積壓、Unassigned 全貌 |
| 二、Requirement 進度 | PM | 需求積壓多嚴重？高風險需求有計畫嗎？ |
| 三、區域分析 | PM / 主管 | DGC-China 等外部客戶風險？ |
| 四、功能模組熱點 | RD / TE | 哪個模組最不穩定？ |
| 五、特別關注項目 | PM / RD / TE | step_control / 手順 / dgc_fae 即時狀態 |
| 六、歷年趨勢分析 | 主管 | 解決能力在改善還是惡化？ |

**完整報告結構**：

```
# {Project} Issue & Requirement 分析報告

> 資料截止日：{TODAY}　Issue 總數：{N}　Requirement 總數：{N}

## 執行摘要（Executive Summary）
[5–8 bullet points：最關鍵事實 + 明確風險判斷]

## 分析方法（Methodology）
[資料來源、截止日、定義對照表]

## 一、Issue 現況（TE Leader / RD Leader）
### 1.1 嚴重性分布
### 1.2 狀態分布
### 1.3 版本計畫完成率
### 1.4 Critical / Blocker 未關閉項目（依 FMEA 排序）
### 1.5 Backlog Issue（>{門檻}天）
### 1.6 高嚴重性 Unassigned Issue

## 二、Requirement 進度（PM）
### 2.1 嚴重性分布
### 2.2 狀態分布
### 2.3 FMEA 風險分層（未關閉）
### 2.4 FMEA Top-N 未關閉 Requirement

## 三、區域分析
[Region × Issue/Req 總數 + Critical/Blocker Opened]

## 四、功能模組熱點分析（功能檢點 Tag）
[Top-N 表格；加入風險詮釋]

## 五、特別關注項目（step_control / 手順 / dgc_fae）
### 5.1 Issue
### 5.2 Requirement

## 六、歷年趨勢分析
[表格 + 1–2 句趨勢詮釋]

## 建議事項（Recommendations）
### PM
### RD Leader
### TE Leader
### 部門主管

## 附錄（Appendix）
### A. 全部 Critical/Blocker 開放 Issue
### B. Backlog Issue 完整清單
### C. step_control / 手順 / dgc_fae 完整項目列表
```

---

## Section 7 — 輸出與儲存規範

- **格式**：Markdown，使用 GitHub Flavored Markdown 表格
- **語言**：繁體中文，ID / Owner / Tag / State 原文保留英文
- **表格排序**：FMEA Total 降冪
- **摘要截斷**：每列 Summary 最多 `thresholds.summary_max_chars` 字元（預設 55），`|` 符號轉為 `｜`
- **輸出路徑**：`{working_directory}/output/analysis_raw.md`（由 `Write` 工具寫入）
- 報告產出後，告知使用者檔案已儲存

**各表格欄位定義**：各表格的欄位名稱定義於 `.claude/assets/iabgvoc-definitions.json` 的 `table_headers` 欄位（`item`、`item_with_region`、`special_item`、`tag_module`、`region`、`trend`）。腳本啟動時讀取後賦值給 `HDR_*` 常數，輸出行格式由這些常數驅動。

---

## Section 8 — 資料準確性驗證（Audit SOP）

> 本節定義每次產出報告後的自動驗證規則。**報告只有在自動驗證通過後才視為有效。**

### 8.1 自動驗證規則（Claude 執行 Step 2–3）

每次腳本執行完畢，Claude 讀取附錄 D 後需確認以下 5 項：

| 檢查項目 | 通過條件 | 失敗時動作 |
|----------|----------|-----------|
| 載入筆數 | Issue + Req 總數 > 0 | 回報「CSV 可能未正確讀取」，停止 |
| State 分布完整 | 附錄 D 的 Issue State 分布包含 `Closed` 與 `Review & Approval` | 回報「State 分布異常，請確認 CSV 欄位名稱」|
| 日期解析失敗數 | Issue + Req 日期失敗均為 0 | 回報「X 筆日期解析失敗，open_days 計算可能有誤」|
| FMEA 解析失敗數 | Issue + Req FMEA 失敗均為 0 | 回報「X 筆 FMEA 解析失敗，風險分層可能有誤」|
| 開放數一致性 | 附錄 D 標示「✅ 通過」 | 回報「開放數計算與 State 分布不一致，請重新執行」|

### 8.2 人工抽查方法（可選，用於進一步確認）

| 驗證目標 | JIRA 篩選條件 | 對照位置 |
|----------|---------------|---------|
| 開放 Issue 數 | `State 不在 {Closed, Review & Approval}` | 附錄 D「開放 Issue 數」 |
| 開放 Req 數 | `State 不在 {Closed, Review & Approval}` | 附錄 D「開放 Req 數」 |
| 高風險 Req | `FMEA ≥ 500 AND State 不在 {Closed, Review & Approval}` | 報告 3.3 FMEA 分層高風險計數 |
| 特定 ID open_days | 手動計算 `Creation Date 至 TODAY` | 報告清單中的「開放天數」欄 |

### 8.3 `is_open` 定義（唯一合法定義）

```
is_open = State ∉ {"Closed", "Review & Approval"}
```

凡報告中涉及開放/老化判斷及表格欄位名稱，均以 `.claude/assets/iabgvoc-definitions.json` 為準：
- 開放/老化行標籤：`labels.open_definition`、`labels.aging_definition`
- 嚴重性分布欄位：`table_headers.severity_dist`
- 排除的 State 值：`closed_states` 陣列

---

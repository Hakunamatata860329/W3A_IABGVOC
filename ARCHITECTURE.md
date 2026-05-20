# IABGVOC 分析系統 — 程式架構文件

> 本文件描述 `analyze_iabgvoc.py` 的架構、資料流、設定系統與報告結構，  
> 作為後續需求討論的共同基礎。

---

## 1. 目錄結構

```
d:\W3A_IABGVOC\
├── analyze_iabgvoc.py          # 主分析腳本（唯一執行入口）
├── iabgvoc-definitions.json    # 設定檔（唯一規則來源）
├── ARCHITECTURE.md             # 本文件
├── CLAUDE.md                   # Claude Code 行為指南
├── .gitignore
│
├── data\                       # 輸入資料（手動從 JIRA 匯出更新）
│   ├── IABGVOC Issue.csv
│   ├── IABGVOC Requirement.csv
│   └── OneSW-Form-0023-TC_DIADesigner Function Check List (1).xlsx
│
├── output\                     # 腳本自動寫入，不納入版控
│   └── analysis_raw.md         # 報告輸出
│
└── .claude\
    └── skills\
        └── iabgvoc-analysis\
            └── SKILL.md        # Claude Skill 執行 SOP
```

---

## 2. 資料流

```
[JIRA 匯出]
    │
    ▼
data/IABGVOC Issue.csv
data/IABGVOC Requirement.csv          ──┐
data/...Function Check List.xlsx      ──┤
iabgvoc-definitions.json              ──┤
                                        │
                                        ▼
                            analyze_iabgvoc.py
                                        │
                         ┌──────────────┼──────────────┐
                         ▼              ▼               ▼
                    計算區段 1–6    建議事項        附錄 A–D
                                        │
                                        ▼
                            output/analysis_raw.md
```

---

## 3. 設定系統（iabgvoc-definitions.json）

所有可調整的規則集中於此檔，腳本啟動時讀入，不需改程式碼即可調整行為。

| 欄位 | 型態 | 用途 |
|------|------|------|
| `closed_states` | `string[]` | 判定 Issue/Req 為「已關閉」的 State 值 |
| `severity_order` | `string[]` | 嚴重性排序（Blocker → Minor），控制表格列順序 |
| `special_tags` | `string[]` | 特別關注的 Tag（step_control、手順、dgc_fae） |
| `thresholds.fmea_high` | `int` | FMEA 高風險門檻（≥此值） |
| `thresholds.fmea_mid_lower/upper` | `int` | FMEA 中風險區間 |
| `thresholds.backlog_days` | `int` | 老化定義：開放超過幾天 |
| `thresholds.top_n` | `int` | Top N 清單筆數（FMEA Top N） |
| `thresholds.summary_max_chars` | `int` | 報告摘要欄截斷字元數 |
| `version_mapping.exact` | `object` | Planned For 精確對應版本名稱 |
| `version_mapping.empty_or_unassigned` | `string` | 空白/Unassigned 的顯示名稱 |
| `version_mapping.contains` | `array` | 以 pattern 模糊對應版本名稱 |
| `version_mapping.display_order` | `string[]` | 版本表格的顯示順序 |
| `labels.open_definition` | `string` | 報告中「開放定義」行標籤 |
| `labels.aging_definition` | `string` | 報告中「老化定義」行標籤 |
| `table_headers.*` | `string` | 各表格欄位標題（8 種） |

**修改原則**：只改 JSON，重跑腳本即生效，無需動 Python 程式碼。

---

## 4. 腳本架構（analyze_iabgvoc.py）

### 4.1 啟動階段（全域）

| 常數 | 來源 | 說明 |
|------|------|------|
| `_ROOT` | `os.path` | 腳本所在目錄，所有路徑基準 |
| `ISSUE_PATH` / `REQ_PATH` / `XLSX_PATH` | `_ROOT + data/` | 輸入資料路徑 |
| `DEFS_PATH` | `_ROOT` | definitions JSON 路徑 |
| `CLOSED_STATES` | JSON `closed_states` | frozenset，用於 `is_open()` |
| `SEV_ORDER` | JSON `severity_order` | 嚴重性排序 |
| `SPECIAL_TAGS` | JSON `special_tags` | 特別關注 Tag |
| `FMEA_HIGH/MID_*` | JSON `thresholds` | FMEA 分層門檻 |
| `BACKLOG_DAYS` | JSON `thresholds` | 老化天數 |
| `TOP_N` | JSON `thresholds` | Top N 筆數 |
| `SUMMARY_MAX_CHARS` | JSON `thresholds` | 摘要截斷 |
| `HDR_*` | JSON `table_headers` | 8 種表格標題常數 |
| `LABEL_OPEN_DEF` / `LABEL_AGING_DEF` | JSON `labels` | 顯示名詞 |
| `VERSION_CATEGORIES` | JSON `version_mapping.display_order` | 版本顯示順序 |
| `VALID_TAGS` | Excel D 欄 | 合法 Tag 集合（小寫） |

### 4.2 工具函式

| 函式 | 說明 |
|------|------|
| `_load_definitions()` | 讀入 JSON，驗證必要欄位，缺欄位直接拋錯 |
| `make_sep(header)` | 依 Markdown 表頭自動產生分隔列 |
| `load_valid_tags()` | 讀 Excel，取 D 欄合法 Tag（小寫，排除 n/a） |
| `parse_date(s)` | 解析 JIRA 日期格式（`yyyy/m/d 上下午 h:mm`），失敗回傳 `None` |
| `load_csv(path)` | 讀 CSV，回傳 `list[dict]`，支援 UTF-8-BOM |
| `tags(row)` | 解析 row 的 `Tag` 欄，回傳 `list[str]`（小寫，去空白） |
| `is_open(row)` | `State` 不在 `CLOSED_STATES` → True |
| `fmea(row)` | 解析 `FMEA Total` 欄，解析失敗回傳 0 |
| `open_days(row)` | `TODAY - Creation Date`，解析失敗回傳 0 |

### 4.3 計算區段

腳本按以下 6 大區段依序計算，結果存入 Python 變數供輸出使用：

| 區段 | 對應報告章節 | 主要產出變數 |
|------|------------|-------------|
| **區段 1** Issue 品質（TE） | §1.1–1.5 | `sev_counts`, `state_counts`, `cb_open`, `aged` |
| **區段 1b** Issue 開發進度（RD） | §1.3, §1.6 | `cat_counts`, `all_open_issues`, `unassigned_high` |
| **區段 2** Requirement 進度（PM） | §2.1–2.4 | `req_sev_counts`, `req_open`, `req_top20`, `fmea_high/mid/low` |
| **區段 3** 區域分析 | §三 | `region_issue`, `region_req` |
| **區段 4** 功能模組（Tag） | §四 | `tag_stats`, `tag_top20` |
| **區段 5** 特別關注 | §五 | `special_issues`, `special_reqs` |
| **區段 6** 歷年趨勢 | §六 | `year_issue`, `year_req` |

### 4.4 輸出階段

計算完成後，以 `out: list[str]` 組裝 Markdown，依序輸出：
執行摘要 → Methodology → §一～六 → 建議事項 → 附錄 A/B/C → 附錄 D（稽核）  
最後寫入 `output/analysis_raw.md`。

---

## 5. 報告結構（output/analysis_raw.md）

| 章節 | 標題 | 主要受眾 |
|------|------|---------|
| Executive Summary | 執行摘要 | 主管 |
| Methodology | 分析方法 | 所有人 |
| §一 | Issue 現況（TE Leader / RD Leader）| TE / RD |
| §一.1 | 嚴重性分布 | — |
| §一.2 | 狀態分布 | — |
| §一.3 | 版本計畫完成率 | — |
| §一.4 | Critical/Blocker 未關閉（Top by FMEA） | — |
| §一.5 | Backlog Issue（開放 >N 天） | — |
| §一.6 | 高嚴重性 Unassigned Issue | — |
| §二 | Requirement 進度（PM） | PM |
| §二.1 | 嚴重性分布 | — |
| §二.2 | 狀態分布 | — |
| §二.3 | FMEA 風險分層 | — |
| §二.4 | FMEA Top 20 未關閉 Requirement | — |
| §三 | 區域分析 | PM / 主管 |
| §四 | 功能模組熱點（Tag Top 20） | RD / TE |
| §五 | 特別關注（step_control / 手順 / dgc_fae） | RD / TE / PM |
| §六 | 歷年趨勢 | 主管 |
| 建議事項 | PM / RD / TE / 主管四組建議 | 各角色 |
| 附錄 A | 全部 Critical/Blocker 開放 Issue | TE |
| 附錄 B | 老化 Issue 完整清單 | RD / TE |
| 附錄 C | 特別關注項目完整清單 | — |
| 附錄 D | 稽核資料（自動驗證） | — |

---

## 6. 擴充指引

### 新增報告章節
1. 在計算區段（4.3）末尾新增變數計算邏輯
2. 在輸出階段（4.4）的 `out.append(...)` 序列中插入對應位置

### 新增可調整的名詞或閾值
1. 在 `iabgvoc-definitions.json` 新增欄位
2. 在腳本 `_load_definitions()` 的 `required` set 加入新欄位名
3. 在全域常數區提取並使用

### 新增版本
在 `version_mapping.contains` 加入 `{ "pattern": "x.x.x", "label": "DIADesigner x.x.x" }`，  
並在 `display_order` 加入對應標籤。

### 新增 special_tags
只需在 `special_tags` 陣列加入 Tag 名稱，無需改 Python。

### 更換輸入資料
將新的 JIRA 匯出覆蓋 `data/` 目錄下的 CSV 檔，重跑腳本即可。

---

## 7. 執行方式

```powershell
cd D:\W3A_IABGVOC
python analyze_iabgvoc.py
```

成功輸出範例：
```
Loaded: 269 issues, 165 requirements

=== DONE: output/analysis_raw.md saved ===
Audit: Issues=269, Reqs=165, Open Issues=39, Open Reqs=88, Consistency=OK
```

`Consistency=OK` 表示開放數自檢通過；若為 `FAIL` 需檢查 CSV 資料或 `closed_states` 設定。

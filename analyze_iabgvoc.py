import csv
import json
import os
import re
from datetime import datetime, date
from collections import defaultdict
import openpyxl

_ROOT      = os.path.dirname(os.path.abspath(__file__))
ISSUE_PATH = os.path.join(_ROOT, 'data', 'IABGVOC Issue.csv')
REQ_PATH   = os.path.join(_ROOT, 'data', 'IABGVOC Requirement.csv')
XLSX_PATH  = os.path.join(_ROOT, 'data', 'OneSW-Form-0023-TC_DIADesigner Function Check List (1).xlsx')
TODAY = date.today()

# ── Load external definitions (single source of truth for all thresholds/mappings) ──
DEFS_PATH = os.path.join(_ROOT, 'iabgvoc-definitions.json')

def _load_definitions():
    with open(DEFS_PATH, encoding='utf-8') as f:
        d = json.load(f)
    required = {'closed_states', 'severity_order', 'special_tags',
                'thresholds', 'version_mapping', 'table_headers', 'labels'}
    missing = required - d.keys()
    if missing:
        raise KeyError(f"iabgvoc-definitions.json 缺少必要欄位：{missing}")
    return d

DEFS = _load_definitions()

CLOSED_STATES  = frozenset(DEFS['closed_states'])
SEV_ORDER      = DEFS['severity_order']
SPECIAL_TAGS   = set(DEFS['special_tags'])

_thr = DEFS['thresholds']
FMEA_HIGH         = _thr['fmea_high']
FMEA_MID_LOWER    = _thr['fmea_mid_lower']
FMEA_MID_UPPER    = _thr['fmea_mid_upper']
BACKLOG_DAYS      = _thr['backlog_days']
TOP_N             = _thr['top_n']
SUMMARY_MAX_CHARS = _thr['summary_max_chars']

_hdr = DEFS['table_headers']
HDR_SEVERITY_DIST    = _hdr['severity_dist']
HDR_ITEM             = _hdr['item']
HDR_ITEM_WITH_REGION = _hdr['item_with_region']
HDR_SPECIAL_ITEM     = _hdr['special_item']
HDR_SPECIAL_APPENDIX = _hdr['special_appendix']
HDR_TAG_MODULE       = _hdr['tag_module']
HDR_REGION           = _hdr['region']
HDR_TREND            = _hdr['trend']

_lbl = DEFS['labels']
LABEL_OPEN_DEF   = _lbl['open_definition']
LABEL_AGING_DEF  = _lbl['aging_definition']

VERSION_CATEGORIES = DEFS['version_mapping']['display_order']

def make_sep(header):
    """Auto-generate a markdown separator row that matches the given header."""
    cols = [c.strip() for c in header.split('|')[1:-1]]
    return '|' + '|'.join('-' * max(3, len(c)) for c in cols) + '|'

def load_valid_tags():
    wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)
    ws = wb['DIADesigner Function List']
    valid = set()
    for row in ws.iter_rows(min_row=2, values_only=True):
        val = row[3] if len(row) > 3 else None
        if val and isinstance(val, str) and val.strip():
            t = val.strip().lower()
            # skip header-like or n/a entries
            if t not in ('n/a', 'download/upload mgr') and not t.startswith('\x5c'):
                valid.add(t)
    return valid

VALID_TAGS = load_valid_tags()

def parse_date(s):
    if not s:
        return None
    s = s.strip()
    # "2026/5/18 下午 3:02" or "2026/5/18 上午 9:00"
    m = re.match(r'(\d{4})/(\d{1,2})/(\d{1,2})', s)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    return None

def load_csv(path):
    rows = []
    with open(path, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def tags(row):
    return [t.strip().lower() for t in row.get('Tag', '').split(',') if t.strip()]

def is_open(row):
    return row.get('State', '').strip() not in CLOSED_STATES

def fmea(row):
    try:
        return int(row.get('FMEA Total', '0') or 0)
    except ValueError:
        return 0

def open_days(row):
    d = parse_date(row.get('Creation Date', ''))
    if d:
        return (TODAY - d).days
    return 0

# ── Load data ──────────────────────────────────────────────────────────────
issues = load_csv(ISSUE_PATH)
reqs   = load_csv(REQ_PATH)

print(f"Loaded: {len(issues)} issues, {len(reqs)} requirements")

# ═══════════════════════════════════════════════════════════════════════════
# 1. ISSUE 品質現況（TE Leader）
# ═══════════════════════════════════════════════════════════════════════════

sev_counts = defaultdict(lambda: {'total': 0, 'open': 0})
for r in issues:
    sv = r.get('Severity', 'Unknown').strip()
    sev_counts[sv]['total'] += 1
    if is_open(r):
        sev_counts[sv]['open'] += 1

state_counts = defaultdict(int)
for r in issues:
    state_counts[r.get('State', '').strip()] += 1

# Critical/Blocker open list
cb_open = [r for r in issues if r.get('Severity','').strip() in ('Blocker','Critical') and is_open(r)]
cb_open.sort(key=lambda r: fmea(r), reverse=True)

# Aging: open > 180 days
aged = [r for r in issues if is_open(r) and open_days(r) > BACKLOG_DAYS]
aged.sort(key=lambda r: open_days(r), reverse=True)

# ═══════════════════════════════════════════════════════════════════════════
# 1b. ISSUE 開發進度（RD Leader）
# ═══════════════════════════════════════════════════════════════════════════

# Planned For version breakdown
planned_counts = defaultdict(lambda: {'total': 0, 'closed': 0})
for r in issues:
    pf = r.get('Planned For', 'Unassigned').strip() or 'Unassigned'
    planned_counts[pf]['total'] += 1
    if not is_open(r):
        planned_counts[pf]['closed'] += 1

def categorize_version(pf):
    vm = DEFS['version_mapping']
    if pf in ('', 'Unassigned'):
        return vm['empty_or_unassigned']
    if pf in vm['exact']:
        return vm['exact'][pf]
    for entry in vm['contains']:
        if entry['pattern'] in pf:
            return entry['label']
    return pf

cat_counts = defaultdict(lambda: {'total': 0, 'closed': 0})
cat_versions = defaultdict(list)
for pf, d in planned_counts.items():
    cat = categorize_version(pf)
    cat_counts[cat]['total'] += d['total']
    cat_counts[cat]['closed'] += d['closed']
    cat_versions[cat].append((pf, d))
for cat in cat_versions:
    cat_versions[cat].sort(key=lambda x: -x[1]['total'])

# All open issues sorted by FMEA for 2.3
all_open_issues = sorted([r for r in issues if is_open(r)], key=lambda r: fmea(r), reverse=True)

# Unassigned high-severity open issues
unassigned_high = [r for r in issues
                   if is_open(r)
                   and r.get('Owner','').strip() in ('', 'Unassigned')
                   and r.get('Severity','').strip() in ('Blocker','Critical','Major')]
unassigned_high.sort(key=lambda r: fmea(r), reverse=True)

# ═══════════════════════════════════════════════════════════════════════════
# 2. REQUIREMENT 進度（PM）
# ═══════════════════════════════════════════════════════════════════════════

req_type_counts = defaultdict(lambda: {'total': 0, 'closed': 0})
for r in reqs:
    rt = r.get('Requirement Type', 'Unknown').strip()
    req_type_counts[rt]['total'] += 1
    if not is_open(r):
        req_type_counts[rt]['closed'] += 1

req_state_counts = defaultdict(int)
for r in reqs:
    req_state_counts[r.get('State', '').strip()] += 1

# FMEA top 20 open requirements
req_open = [r for r in reqs if is_open(r)]
req_open.sort(key=lambda r: fmea(r), reverse=True)
req_top20 = req_open[:TOP_N]

# FMEA tier breakdown for open reqs
fmea_high = [r for r in req_open if fmea(r) >= FMEA_HIGH]
fmea_mid  = [r for r in req_open if FMEA_MID_LOWER <= fmea(r) <= FMEA_MID_UPPER]
fmea_low  = [r for r in req_open if fmea(r) < FMEA_MID_LOWER]

# Unassigned ratio
req_unassigned = sum(1 for r in reqs if r.get('Owner','').strip() in ('', 'Unassigned') and is_open(r))

# Requirement version breakdown (same categorize_version logic as Issues)
req_planned_counts = defaultdict(lambda: {'total': 0, 'closed': 0})
for r in reqs:
    pf = r.get('Planned For', 'Unassigned').strip() or 'Unassigned'
    req_planned_counts[pf]['total'] += 1
    if not is_open(r):
        req_planned_counts[pf]['closed'] += 1

req_cat_counts = defaultdict(lambda: {'total': 0, 'closed': 0})
for pf, d in req_planned_counts.items():
    cat = categorize_version(pf)
    req_cat_counts[cat]['total'] += d['total']
    req_cat_counts[cat]['closed'] += d['closed']

req_sev_counts = defaultdict(lambda: {'total': 0, 'open': 0})
for r in reqs:
    sv = r.get('Severity', 'Unknown').strip()
    req_sev_counts[sv]['total'] += 1
    if is_open(r):
        req_sev_counts[sv]['open'] += 1

# ═══════════════════════════════════════════════════════════════════════════
# 3. 區域 / 客戶分析
# ═══════════════════════════════════════════════════════════════════════════

region_issue = defaultdict(lambda: {'total': 0, 'open': 0, 'cb_open': 0})
for r in issues:
    rg = r.get('Region', 'Unknown').strip() or 'Unknown'
    region_issue[rg]['total'] += 1
    if is_open(r):
        region_issue[rg]['open'] += 1
        if r.get('Severity','').strip() in ('Blocker','Critical'):
            region_issue[rg]['cb_open'] += 1

region_req = defaultdict(lambda: {'total': 0, 'open': 0})
for r in reqs:
    rg = r.get('Region', 'Unknown').strip() or 'Unknown'
    region_req[rg]['total'] += 1
    if is_open(r):
        region_req[rg]['open'] += 1

# ═══════════════════════════════════════════════════════════════════════════
# 4. 功能模組分析（Tag）
# ═══════════════════════════════════════════════════════════════════════════

# Collect tag stats: only tags defined in the Function Check List xlsx (column D)
tag_stats = defaultdict(lambda: {'issue': 0, 'issue_open': 0, 'req': 0, 'req_open': 0, 'cb_open': 0})

for r in issues:
    for t in tags(r):
        if t in VALID_TAGS:
            tag_stats[t]['issue'] += 1
            if is_open(r):
                tag_stats[t]['issue_open'] += 1
                if r.get('Severity','').strip() in ('Blocker','Critical'):
                    tag_stats[t]['cb_open'] += 1

for r in reqs:
    for t in tags(r):
        if t in VALID_TAGS:
            tag_stats[t]['req'] += 1
            if is_open(r):
                tag_stats[t]['req_open'] += 1

# Sort by total volume
tag_sorted = sorted(tag_stats.items(), key=lambda x: x[1]['issue'] + x[1]['req'], reverse=True)
tag_top20 = tag_sorted[:TOP_N]

# ═══════════════════════════════════════════════════════════════════════════
# 5. 特別關注：step_control / 手順 / dgc_fae
# ═══════════════════════════════════════════════════════════════════════════

special_issues = [r for r in issues if any(t in SPECIAL_TAGS for t in tags(r))]
special_reqs   = [r for r in reqs   if any(t in SPECIAL_TAGS for t in tags(r))]

def special_tag_label(row):
    matched = [t for t in tags(row) if t in SPECIAL_TAGS]
    return ', '.join(matched)

special_issues.sort(key=lambda r: fmea(r), reverse=True)
special_reqs.sort(key=lambda r: fmea(r), reverse=True)

# ═══════════════════════════════════════════════════════════════════════════
# 6. 歷年趨勢
# ═══════════════════════════════════════════════════════════════════════════

year_issue = defaultdict(lambda: {'created': 0, 'closed': 0})
for r in issues:
    d = parse_date(r.get('Creation Date', ''))
    if d:
        year_issue[d.year]['created'] += 1
    d2 = parse_date(r.get('Resolution date', ''))
    if d2:
        year_issue[d2.year]['closed'] += 1

year_req = defaultdict(lambda: {'created': 0, 'closed': 0})
for r in reqs:
    d = parse_date(r.get('Creation Date', ''))
    if d:
        year_req[d.year]['created'] += 1
    d2 = parse_date(r.get('Resolution date', ''))
    if d2:
        year_req[d2.year]['closed'] += 1

# ═══════════════════════════════════════════════════════════════════════════
# OUTPUT
# ═══════════════════════════════════════════════════════════════════════════

out = []

out.append("# IABGVOC Issue & Requirement 分析報告\n")
out.append(f"> 資料截止日：{TODAY}　Issue 總數：{len(issues)}　Requirement 總數：{len(reqs)}\n")

# ─── Executive Summary ───────────────────────────────────────────────────
total_open_issues = sum(1 for r in issues if is_open(r))
total_open_reqs   = sum(1 for r in reqs if is_open(r))
cb_total = len(cb_open)
req_closed_pct = round(sum(v['closed'] for v in req_type_counts.values()) / len(reqs) * 100, 1)

out.append("## 執行摘要（Executive Summary）\n")
out.append(f"- **開放 Issue 數**：{total_open_issues} / {len(issues)}（其中 Critical/Blocker：{cb_total} 筆）")
out.append(f"- **開放 Requirement 數**：{total_open_reqs} / {len(reqs)}（整體完成率：{req_closed_pct}%）")

max_fmea_req = req_top20[0] if req_top20 else None
if max_fmea_req:
    out.append(f"- **最高風險 Requirement**：[{max_fmea_req['ID']}] {max_fmea_req['Summary'][:60]}… (FMEA={fmea(max_fmea_req)})")

top_tag = tag_top20[0][0] if tag_top20 else '-'
out.append(f"- **最熱點功能模組（Tag）**：`{top_tag}`（Issue+Req 合計 {tag_top20[0][1]['issue']+tag_top20[0][1]['req']} 筆）")
out.append(f"- **老化 Issue（>{BACKLOG_DAYS}天未關閉）**：{len(aged)} 筆\n")

# ─── Methodology ─────────────────────────────────────────────────────────
out.append("## 分析方法（Methodology）\n")
out.append("| 項目 | 說明 |")
out.append("|------|------|")
out.append(f"| 資料來源 | IABGVOC Issue.csv（{len(issues)} 筆）、IABGVOC Requirement.csv（{len(reqs)} 筆）|")
out.append("| 時間範圍 | 2021 ~ 2026/05（全部資料）|")
out.append(f"| 分析基準日 | {TODAY} |")
out.append(f"| {LABEL_OPEN_DEF} | State ∉ {{{', '.join(DEFS['closed_states'])}}} |")
out.append(f"| {LABEL_AGING_DEF} | 開放超過 {BACKLOG_DAYS} 天（創建日至今）|")
out.append("| 特別關注 Tag | `step_control`、`手順`、`dgc_fae` |")
out.append("| FMEA 分層 | 高風險：>=500 / 中風險：200-499 / 低風險：<200 |\n")

# ─── 1. Issue 現況（TE Leader / RD Leader）──────────────────────────────
out.append("## 一、Issue 現況（TE Leader / RD Leader）\n")

out.append("### 1.1 嚴重性分布\n")
out.append(HDR_SEVERITY_DIST)
out.append("|--------|------|--------|--------|")
for sv in SEV_ORDER:
    d = sev_counts.get(sv, {'total': 0, 'open': 0})
    pct = round(d['open']/d['total']*100, 1) if d['total'] else 0
    out.append(f"| {sv} | {d['total']} | {d['open']} | {pct}% |")
out.append("")

out.append("### 1.2 狀態分布\n")
out.append("| 狀態 | 數量 |")
out.append("|------|------|")
for st, cnt in sorted(state_counts.items(), key=lambda x: -x[1]):
    out.append(f"| {st} | {cnt} |")
out.append("")

out.append("### 1.3 版本計畫完成率（分類規則）\n")
out.append("| 版本分類 | 總數 | 已關閉 | 完成率 |")
out.append("|----------|------|--------|--------|")
for cat in VERSION_CATEGORIES:
    if cat in cat_counts:
        d = cat_counts[cat]
        pct = round(d['closed']/d['total']*100, 1) if d['total'] else 0
        out.append(f"| {cat} | {d['total']} | {d['closed']} | {pct}% |")
out.append("")

out.append(f"### 1.4 Critical / Blocker 未關閉項目（共 {len(cb_open)} 筆，依 FMEA 排序）\n")
out.append(HDR_ITEM)
out.append(make_sep(HDR_ITEM))
for r in cb_open:
    summ = r.get('Summary','').strip()[:SUMMARY_MAX_CHARS].replace('|','｜')
    out.append(f"| {r['ID']} | {r.get('Severity','')} | {fmea(r)} | {r.get('State','')} | {r.get('Owner','')} | {open_days(r)} | {summ} |")
out.append("")

out.append(f"### 1.5 Backlog Issue（開放 >{BACKLOG_DAYS} 天，共 {len(aged)} 筆）\n")
if aged:
    out.append(HDR_ITEM)
    out.append(make_sep(HDR_ITEM))
    for r in aged[:30]:
        summ = r.get('Summary','').strip()[:SUMMARY_MAX_CHARS].replace('|','｜')
        out.append(f"| {r['ID']} | {r.get('Severity','')} | {fmea(r)} | {r.get('State','')} | {r.get('Owner','')} | {open_days(r)} | {summ} |")
    if len(aged) > 30:
        out.append(f"\n> 僅列出前 30 筆，完整清單見附錄。")
out.append("")

out.append(f"### 1.6 高嚴重性 Unassigned Issue（共 {len(unassigned_high)} 筆）\n")
if unassigned_high:
    out.append(HDR_ITEM)
    out.append(make_sep(HDR_ITEM))
    for r in unassigned_high[:20]:
        summ = r.get('Summary','').strip()[:SUMMARY_MAX_CHARS].replace('|','｜')
        out.append(f"| {r['ID']} | {r.get('Severity','')} | {fmea(r)} | {r.get('State','')} | {r.get('Owner','')} | {open_days(r)} | {summ} |")
out.append("")

# ─── 2. Requirement 進度（PM）──────────────────────────────────────────
out.append("## 二、Requirement 進度（PM）\n")

out.append("### 2.1 嚴重性分布\n")
out.append(HDR_SEVERITY_DIST)
out.append("|--------|------|--------|--------|")
for sv in SEV_ORDER:
    d = req_sev_counts.get(sv, {'total': 0, 'open': 0})
    pct = round(d['open']/d['total']*100, 1) if d['total'] else 0
    out.append(f"| {sv} | {d['total']} | {d['open']} | {pct}% |")
out.append("")

out.append("### 2.2 狀態分布\n")
out.append("| 狀態 | 數量 |")
out.append("|------|------|")
for st, cnt in sorted(req_state_counts.items(), key=lambda x: -x[1]):
    out.append(f"| {st} | {cnt} |")
out.append("")

out.append("### 2.3 版本計畫完成率（分類規則）\n")
out.append("| 版本分類 | 總數 | 已關閉 | 完成率 |")
out.append("|----------|------|--------|--------|")
for cat in VERSION_CATEGORIES:
    if cat in req_cat_counts:
        d = req_cat_counts[cat]
        pct = round(d['closed']/d['total']*100, 1) if d['total'] else 0
        out.append(f"| {cat} | {d['total']} | {d['closed']} | {pct}% |")
out.append("")

out.append("### 2.4 FMEA 風險分層（未關閉）\n")
out.append(f"- 高風險（FMEA ≥ 500）：**{len(fmea_high)}** 筆")
out.append(f"- 中風險（201–499）：**{len(fmea_mid)}** 筆")
out.append(f"- 低風險（0–200）：**{len(fmea_low)}** 筆")
out.append(f"- 待辦未指派（Unassigned）：**{req_unassigned}** 筆\n")

out.append(f"### 2.5 FMEA Top 20 未關閉 Requirement（PM 優先關注）\n")
out.append(HDR_ITEM)
out.append(make_sep(HDR_ITEM))
for r in req_top20:
    summ = r.get('Summary','').strip()[:SUMMARY_MAX_CHARS].replace('|','｜')
    out.append(f"| {r['ID']} | {r.get('Severity','')} | {fmea(r)} | {r.get('State','')} | {r.get('Owner','')} | {open_days(r)} | {summ} |")
out.append("")

# ─── 3. 區域分析 ────────────────────────────────────────────────────────
out.append("## 三、區域分析\n")
out.append(HDR_REGION)
out.append(make_sep(HDR_REGION))
all_regions = sorted(set(list(region_issue.keys()) + list(region_req.keys())),
                     key=lambda r: region_issue[r]['total'] + region_req[r]['total'], reverse=True)
for rg in all_regions:
    ri = region_issue[rg]
    rr = region_req[rg]
    out.append(f"| {rg} | {ri['total']} | {ri['open']} | {ri['cb_open']} | {rr['total']} | {rr['open']} |")
out.append("")

# ─── 4. 功能模組分析（Tag）──────────────────────────────────────────────
out.append("## 四、功能模組熱點分析（功能檢點 Tag）\n")
out.append(HDR_TAG_MODULE)
out.append(make_sep(HDR_TAG_MODULE))
for t, d in tag_top20:
    out.append(f"| `{t}` | {d['issue']} | {d['issue_open']} | {d['req']} | {d['req_open']} | {d['cb_open']} |")
out.append("")

# ─── 5. 特別關注 ──────────────────────────────────────────────────────────
out.append("## 五、特別關注項目（step_control / 手順 / dgc_fae）\n")
out.append("> 僅列出開放項目（State 不含 Closed / Review & Approval）\n")

def open_items_for_tag(tag):
    ti = [r for r in special_issues if tag in tags(r) and is_open(r)]
    tr = [r for r in special_reqs   if tag in tags(r) and is_open(r)]
    return ti, tr

# 總覽表
out.append("| Tag | Issue（開放）| Req（開放）| 開放合計 |")
out.append("|-----|------------:|----------:|---------:|")
total_i, total_r = 0, 0
for tag in DEFS['special_tags']:
    ti, tr = open_items_for_tag(tag)
    total_i += len(ti); total_r += len(tr)
    out.append(f"| {tag} | {len(ti)} | {len(tr)} | {len(ti)+len(tr)} |")
out.append(f"| **合計** | **{total_i}** | **{total_r}** | **{total_i+total_r}** |\n")

# 各 tag 小節
for idx, tag in enumerate(DEFS['special_tags'], 1):
    ti, tr = open_items_for_tag(tag)
    combined = sorted(
        [(r, 'Issue') for r in ti] + [(r, 'Req') for r in tr],
        key=lambda x: fmea(x[0]), reverse=True
    )
    out.append(f"### 5.{idx} {tag}（Issue + Requirement，依 FMEA 排序）\n")
    out.append(f"**Issue**：開放 {len(ti)} 筆　**Requirement**：開放 {len(tr)} 筆\n")
    out.append(HDR_SPECIAL_ITEM)
    out.append(make_sep(HDR_SPECIAL_ITEM))
    for r, kind in combined:
        summ = r.get('Summary','').strip()[:SUMMARY_MAX_CHARS].replace('|','｜')
        out.append(f"| {r['ID']} | {kind} | {r.get('Severity','')} | {fmea(r)} | {r.get('State','')} | {r.get('Owner','')} | {summ} |")
    out.append("")

# ─── 6. 歷年趨勢 ──────────────────────────────────────────────────────────
out.append("## 六、歷年趨勢分析\n")
out.append(HDR_TREND)
out.append(make_sep(HDR_TREND))
all_years = sorted(set(list(year_issue.keys()) + list(year_req.keys())))
for yr in all_years:
    yi = year_issue[yr]
    yr2 = year_req[yr]
    i_pct = round(yi['closed']/yi['created']*100, 1) if yi['created'] else '-'
    r_pct = round(yr2['closed']/yr2['created']*100, 1) if yr2['created'] else '-'
    out.append(f"| {yr} | {yi['created']} | {yi['closed']} | {i_pct}% | {yr2['created']} | {yr2['closed']} | {r_pct}% |")
out.append("")

# ─── Recommendations ────────────────────────────────────────────────────
out.append("## 建議事項（Recommendations）\n")

out.append("### PM")
out.append(f"1. 優先推動 FMEA ≥ 500 的 {len(fmea_high)} 筆高風險 Requirement 排入近期版本規劃，避免持續積壓。")
out.append(f"2. 對 Unassigned 的 {req_unassigned} 筆開放 Requirement 進行責任指派，降低 Backlog 盲點。")
out.append("3. 針對 Top 20 FMEA Requirement，召集 RD/TE 評估可交付版本，並更新 Planned For 欄位。\n")

out.append("### RD Leader")
out.append(f"1. 解決 {len(unassigned_high)} 筆高嚴重性 Unassigned Issue，明確指派負責人。")
out.append("2. 檢視 Owner 分布，避免少數人員過度集中，規劃工作分擔。")
out.append(f"3. 確認各版本（Planned For）的 Issue 完成率，對接近截止的版本提前介入。\n")

out.append("### TE Leader")
out.append(f"1. 集中測試驗證 {len(cb_open)} 筆未關閉的 Critical/Blocker Issue，確保 State 推進至 Verification→Closed。")
out.append(f"2. 對 {len(aged)} 筆老化 Issue（>180天）逐一確認是否已完成但未更新 State，或需要重新排程。")
out.append("3. 追蹤 `step_control` / `手順` 相關 Issue 的驗證進度，確保手順邏輯正確性。\n")

out.append("### 部門主管")
out.append(f"1. 目前 Critical/Blocker 開放數為 {cb_total}，建議設定每週清零目標並追蹤。")
out.append(f"2. FMEA 高風險 Requirement 有 {len(fmea_high)} 筆待處理，建議 PM 召開優先級對齊會議。")
out.append("3. 關注 DGC-China 區域需求（dgc_fae）的回應速度，確保客戶關係維繫。\n")

# ─── Appendix ────────────────────────────────────────────────────────────
out.append("## 附錄（Appendix）\n")

out.append("### A. 全部 Critical/Blocker 開放 Issue\n")
out.append(HDR_ITEM_WITH_REGION)
out.append(make_sep(HDR_ITEM_WITH_REGION))
for r in cb_open:
    summ = r.get('Summary','').strip()[:SUMMARY_MAX_CHARS].replace('|','｜')
    out.append(f"| {r['ID']} | {r.get('Severity','')} | {fmea(r)} | {r.get('State','')} | {r.get('Owner','')} | {open_days(r)} | {r.get('Region','')} | {summ} |")
out.append("")

out.append(f"### B. 老化 Issue 完整清單（>180 天，共 {len(aged)} 筆）\n")
out.append(HDR_ITEM_WITH_REGION)
out.append(make_sep(HDR_ITEM_WITH_REGION))
for r in aged:
    summ = r.get('Summary','').strip()[:SUMMARY_MAX_CHARS].replace('|','｜')
    out.append(f"| {r['ID']} | {r.get('Severity','')} | {fmea(r)} | {r.get('State','')} | {r.get('Owner','')} | {open_days(r)} | {r.get('Region','')} | {summ} |")
out.append("")

out.append("### C. step_control / 手順 / dgc_fae 完整項目列表\n")
out.append("#### C1. Issue\n")
out.append(HDR_SPECIAL_APPENDIX)
out.append(make_sep(HDR_SPECIAL_APPENDIX))
for r in special_issues:
    summ = r.get('Summary','').strip()[:SUMMARY_MAX_CHARS].replace('|','｜')
    out.append(f"| {r['ID']} | {special_tag_label(r)} | {r.get('Severity','')} | {fmea(r)} | {r.get('State','')} | {r.get('Owner','')} | {r.get('Region','')} | {summ} |")
out.append("")
out.append("#### C2. Requirement\n")
out.append(HDR_SPECIAL_APPENDIX)
out.append(make_sep(HDR_SPECIAL_APPENDIX))
for r in special_reqs:
    summ = r.get('Summary','').strip()[:SUMMARY_MAX_CHARS].replace('|','｜')
    out.append(f"| {r['ID']} | {special_tag_label(r)} | {r.get('Severity','')} | {fmea(r)} | {r.get('State','')} | {r.get('Owner','')} | {r.get('Region','')} | {summ} |")
out.append("")

# ─── Appendix D — Audit Data ─────────────────────────────────────────────
# Count date/fmea parse failures for audit
date_fail_issues = sum(1 for r in issues if not parse_date(r.get('Creation Date', '')))
date_fail_reqs   = sum(1 for r in reqs   if not parse_date(r.get('Creation Date', '')))
fmea_fail_issues = sum(1 for r in issues if r.get('FMEA Total', '').strip() not in ('', '0') and fmea(r) == 0)
fmea_fail_reqs   = sum(1 for r in reqs   if r.get('FMEA Total', '').strip() not in ('', '0') and fmea(r) == 0)

issue_state_dist = defaultdict(int)
for r in issues:
    issue_state_dist[r.get('State', '').strip()] += 1
req_state_dist = defaultdict(int)
for r in reqs:
    req_state_dist[r.get('State', '').strip()] += 1

open_issues_count = sum(1 for r in issues if is_open(r))
open_reqs_count   = sum(1 for r in reqs   if is_open(r))
# Cross-check: open = total - closed_states
closed_issue_check = sum(v for k, v in issue_state_dist.items() if k in CLOSED_STATES)
closed_req_check   = sum(v for k, v in req_state_dist.items()   if k in CLOSED_STATES)
open_issue_check   = len(issues) - closed_issue_check
open_req_check     = len(reqs)   - closed_req_check
audit_ok = (open_issues_count == open_issue_check) and (open_reqs_count == open_req_check)

issue_state_str = '、'.join(f"{k}:{v}" for k, v in sorted(issue_state_dist.items(), key=lambda x: -x[1]))
req_state_str   = '、'.join(f"{k}:{v}" for k, v in sorted(req_state_dist.items(),   key=lambda x: -x[1]))

out.append("## 附錄 D — 稽核資料（Audit）\n")
out.append("> 此區段由腳本自動產生，用於驗證報告數字的正確性。請在閱讀報告前確認下方數值與 JIRA 一致。\n")
out.append("| 項目 | 數值 |")
out.append("|------|------|")
out.append(f"| Issue CSV 載入筆數 | {len(issues)} |")
out.append(f"| Requirement CSV 載入筆數 | {len(reqs)} |")
out.append(f"| 基準日期（TODAY） | {TODAY} |")
out.append(f"| is_open 排除的 State | {', '.join(sorted(CLOSED_STATES))} |")
out.append(f"| Issue State 分布 | {issue_state_str} |")
out.append(f"| Req State 分布 | {req_state_str} |")
out.append(f"| 日期解析失敗（Issue） | {date_fail_issues} |")
out.append(f"| 日期解析失敗（Req） | {date_fail_reqs} |")
out.append(f"| FMEA 解析失敗（Issue） | {fmea_fail_issues} |")
out.append(f"| FMEA 解析失敗（Req） | {fmea_fail_reqs} |")
out.append(f"| 開放 Issue 數（計算結果） | {open_issues_count} |")
out.append(f"| 開放 Req 數（計算結果） | {open_reqs_count} |")
out.append(f"| 開放數一致性自檢 | {'✅ 通過' if audit_ok else '❌ 失敗：開放數計算與 State 分布不一致，請檢查資料'} |")
out.append("")

result = '\n'.join(out)

# Save raw analysis for report-writer
with open(os.path.join(_ROOT, 'output', 'analysis_raw.md'), 'w', encoding='utf-8') as f:
    f.write(result)

print("\n\n=== DONE: output/analysis_raw.md saved ===")
print(f"Audit: Issues={len(issues)}, Reqs={len(reqs)}, Open Issues={open_issues_count}, Open Reqs={open_reqs_count}, Consistency={'OK' if audit_ok else 'FAIL'}")

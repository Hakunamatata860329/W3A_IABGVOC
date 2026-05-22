import csv
import json
import os
import re
from datetime import date
from collections import defaultdict
import openpyxl

_ROOT     = os.path.dirname(os.path.abspath(__file__))
ISSUE_PATH = os.path.join(_ROOT, 'data', 'IABGVOC Issue.csv')
REQ_PATH   = os.path.join(_ROOT, 'data', 'IABGVOC Requirement.csv')
XLSX_PATH  = os.path.join(_ROOT, 'data', 'OneSW-Form-0023-TC_DIADesigner Function Check List (1).xlsx')
DEFS_PATH  = os.path.join(_ROOT, 'iabgvoc-definitions.json')
OUT_PATH   = os.path.join(_ROOT, 'output', 'dashboard.html')
TODAY      = date.today()

with open(DEFS_PATH, encoding='utf-8') as f:
    DEFS = json.load(f)

CLOSED_STATES  = frozenset(DEFS['closed_states'])
SEV_ORDER      = DEFS['severity_order']
_thr           = DEFS['thresholds']
FMEA_HIGH      = _thr['fmea_high']
FMEA_MID_LOWER = _thr['fmea_mid_lower']
FMEA_MID_UPPER = _thr['fmea_mid_upper']

def load_valid_tags():
    wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)
    ws = wb['DIADesigner Function List']
    valid = set()
    for row in ws.iter_rows(min_row=2, values_only=True):
        val = row[3] if len(row) > 3 else None
        if val and isinstance(val, str) and val.strip():
            t = val.strip().lower()
            if t not in ('n/a', 'download/upload mgr') and not t.startswith('\x5c'):
                valid.add(t)
    return valid

VALID_TAGS = load_valid_tags()

def parse_date(s):
    if not s:
        return None
    m = re.match(r'(\d{4})/(\d{1,2})/(\d{1,2})', s.strip())
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    return None

def load_csv(path):
    with open(path, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def is_open(row):
    return row.get('State', '').strip() not in CLOSED_STATES

def fmea_val(row):
    try:
        return int(row.get('FMEA Total', '0') or 0)
    except ValueError:
        return 0

def get_tags(row):
    return [t.strip().lower() for t in row.get('Tag', '').split(',') if t.strip()]

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

issues = load_csv(ISSUE_PATH)
reqs   = load_csv(REQ_PATH)
print(f"Loaded: {len(issues)} issues, {len(reqs)} requirements")

open_issues    = [r for r in issues if is_open(r)]
open_reqs      = [r for r in reqs   if is_open(r)]
cb_open             = [r for r in open_issues if r.get('Severity', '').strip() in ('Blocker', 'Critical')]
fmea_high_open      = [r for r in open_issues if fmea_val(r) >= FMEA_HIGH]
cb_open_reqs        = [r for r in open_reqs   if r.get('Severity', '').strip() in ('Blocker', 'Critical')]
fmea_high_open_reqs = [r for r in open_reqs   if fmea_val(r) >= FMEA_HIGH]

year_data = defaultdict(lambda: {'ic': 0, 'il': 0, 'rc': 0, 'rl': 0})
for r in issues:
    d = parse_date(r.get('Creation Date', ''))
    if d: year_data[d.year]['ic'] += 1
    d2 = parse_date(r.get('Resolution date', ''))
    if d2: year_data[d2.year]['il'] += 1
for r in reqs:
    d = parse_date(r.get('Creation Date', ''))
    if d: year_data[d.year]['rc'] += 1
    d2 = parse_date(r.get('Resolution date', ''))
    if d2: year_data[d2.year]['rl'] += 1
years = sorted(year_data.keys())

MONTH_NAMES = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
monthly_keys = []
monthly_labels = []
_y, _mo = 2025, 1
while (_y, _mo) <= (TODAY.year, TODAY.month):
    monthly_keys.append(f"{_y}-{_mo:02d}")
    monthly_labels.append(f"{MONTH_NAMES[_mo-1]} {str(_y)[2:]}")
    _mo += 1
    if _mo > 12:
        _mo = 1
        _y += 1
monthly_data = defaultdict(lambda: {'ic': 0, 'il': 0, 'rc': 0, 'rl': 0})
monthly_keys_set = set(monthly_keys)
for r in issues:
    d = parse_date(r.get('Creation Date', ''))
    if d:
        k = f"{d.year}-{d.month:02d}"
        if k in monthly_keys_set: monthly_data[k]['ic'] += 1
    d2 = parse_date(r.get('Resolution date', ''))
    if d2:
        k = f"{d2.year}-{d2.month:02d}"
        if k in monthly_keys_set: monthly_data[k]['il'] += 1
for r in reqs:
    d = parse_date(r.get('Creation Date', ''))
    if d:
        k = f"{d.year}-{d.month:02d}"
        if k in monthly_keys_set: monthly_data[k]['rc'] += 1
    d2 = parse_date(r.get('Resolution date', ''))
    if d2:
        k = f"{d2.year}-{d2.month:02d}"
        if k in monthly_keys_set: monthly_data[k]['rl'] += 1

SA_LABELS  = ['24 Q1','24 Q2','24 Q3','24 Q4','25 Q1','25 Q2','25 Q3','25 Q4','26 Q1','26 Q2']
SA_CUTOFFS = [
    date(2024,3,31), date(2024,6,30), date(2024,9,30), date(2024,12,31),
    date(2025,3,31), date(2025,6,30), date(2025,9,30), date(2025,12,31),
    date(2026,3,31), TODAY,
]
sa_issue_total, sa_req_total, sa_combined = [], [], []
for cutoff in SA_CUTOFFS:
    ni = sum(1 for r in issues for d in [parse_date(r.get('Creation Date',''))] if d and d <= cutoff)
    nr = sum(1 for r in reqs   for d in [parse_date(r.get('Creation Date',''))] if d and d <= cutoff)
    sa_issue_total.append(ni)
    sa_req_total.append(nr)
    sa_combined.append(ni + nr)

sev_issue = {sv: 0 for sv in SEV_ORDER}
sev_req   = {sv: 0 for sv in SEV_ORDER}
for r in open_issues:
    sv = r.get('Severity', '').strip()
    if sv in sev_issue: sev_issue[sv] += 1
for r in open_reqs:
    sv = r.get('Severity', '').strip()
    if sv in sev_req: sev_req[sv] += 1

region_cb   = defaultdict(int)
region_open = defaultdict(int)
for r in open_issues:
    rg = r.get('Region', 'Unknown').strip() or 'Unknown'
    region_open[rg] += 1
    if r.get('Severity', '').strip() in ('Blocker', 'Critical'):
        region_cb[rg] += 1
all_regions = sorted(set(region_cb) | set(region_open), key=lambda x: region_cb[x], reverse=True)

region_req_open = defaultdict(int)
for r in open_reqs:
    rg = r.get('Region', 'Unknown').strip() or 'Unknown'
    region_req_open[rg] += 1

tag_cb = defaultdict(int)
for r in open_issues:
    if r.get('Severity', '').strip() in ('Blocker', 'Critical'):
        for t in get_tags(r):
            if t in VALID_TAGS:
                tag_cb[t] += 1
top_tags = sorted(tag_cb.items(), key=lambda x: -x[1])[:10]

PINNED_TAGS = ['step_control', '德馬泰克', 'dgc_fae']
tag_issue_open = defaultdict(int)
tag_req_open   = defaultdict(int)
for r in open_issues:
    for t in get_tags(r):
        if t in PINNED_TAGS:
            tag_issue_open[t] += 1
for r in open_reqs:
    for t in get_tags(r):
        if t in PINNED_TAGS:
            tag_req_open[t] += 1

version_open = defaultdict(int)
for r in open_issues:
    pf = r.get('Planned For', '').strip() or 'Unassigned'
    version_open[categorize_version(pf)] += 1
version_order  = DEFS['version_mapping']['display_order']
version_labels = [v for v in version_order if version_open[v] > 0]
version_counts = [version_open[v] for v in version_labels]

version_total_all = defaultdict(int)
for r in issues:
    pf = r.get('Planned For', '').strip() or 'Unassigned'
    version_total_all[categorize_version(pf)] += 1

req_version_open  = defaultdict(int)
req_version_total = defaultdict(int)
for r in reqs:
    pf = r.get('Planned For', '').strip() or 'Unassigned'
    req_version_total[categorize_version(pf)] += 1
    if is_open(r):
        req_version_open[categorize_version(pf)] += 1

ver_sched = DEFS.get('version_schedule', {})
gantt_labels = [v for v in version_order if v in ver_sched and (version_total_all[v] > 0 or req_version_total[v] > 0)]
version_gantt = []
for v in gantt_labels:
    total      = version_total_all[v]
    closed     = total - version_open[v]
    req_total  = req_version_total[v]
    req_closed = req_total - req_version_open[v]
    sched      = ver_sched[v]
    rel_d      = date.fromisoformat(sched['release_date'])
    version_gantt.append({
        'label':        v,
        'start_date':   sched['start_date'],
        'release_date': sched['release_date'],
        'total':        total,
        'closed':       closed,
        'pct':          round(closed / total * 100, 1) if total > 0 else 0.0,
        'days_left':    (rel_d - TODAY).days,
        'req_total':    req_total,
        'req_closed':   req_closed,
        'req_pct':      round(req_closed / req_total * 100, 1) if req_total > 0 else 0.0,
    })

fmea_tier = {
    'high': sum(1 for r in open_reqs if fmea_val(r) >= FMEA_HIGH),
    'mid':  sum(1 for r in open_reqs if FMEA_MID_LOWER <= fmea_val(r) <= FMEA_MID_UPPER),
    'low':  sum(1 for r in open_reqs if fmea_val(r) < FMEA_MID_LOWER),
}

state_counts = defaultdict(int)
for r in issues:
    state_counts[r.get('State', '').strip()] += 1
state_sorted = sorted(state_counts.items(), key=lambda x: -x[1])

req_state_counts = defaultdict(int)
for r in reqs:
    req_state_counts[r.get('State', '').strip()] += 1
req_state_sorted = sorted(req_state_counts.items(), key=lambda x: -x[1])

data = {
    'meta': {
        'generated_at': str(TODAY),
        'total_issues': len(issues),
        'total_reqs':   len(reqs),
    },
    'kpi': {
        'open_issues':    len(open_issues),
        'open_reqs':      len(open_reqs),
        'cb_open':             len(cb_open),
        'fmea_high_open':      len(fmea_high_open),
        'cb_open_reqs':        len(cb_open_reqs),
        'fmea_high_open_reqs': len(fmea_high_open_reqs),
        'fmea_threshold':      FMEA_HIGH,
    },
    'trend': {
        'years':         years,
        'issue_created': [year_data[y]['ic'] for y in years],
        'issue_closed':  [year_data[y]['il'] for y in years],
        'req_created':   [year_data[y]['rc'] for y in years],
        'req_closed':    [year_data[y]['rl'] for y in years],
    },
    'monthly': {
        'labels':         SA_LABELS,
        'issue_total':    sa_issue_total,
        'req_total':      sa_req_total,
        'combined_total': sa_combined,
    },
    'severity': {
        'labels':     SEV_ORDER,
        'issue_open': [sev_issue[sv] for sv in SEV_ORDER],
        'req_open':   [sev_req[sv]   for sv in SEV_ORDER],
    },
    'region': {
        'labels':        all_regions,
        'issue_cb_open': [region_cb[r]       for r in all_regions],
        'issue_open':    [region_open[r]     for r in all_regions],
        'req_open':      [region_req_open[r] for r in all_regions],
    },
    'tags': {
        'labels':  [t[0] for t in top_tags],
        'cb_open': [t[1] for t in top_tags],
    },
    'tag_open': {
        'labels':     PINNED_TAGS,
        'issue_open': [tag_issue_open[t] for t in PINNED_TAGS],
        'req_open':   [tag_req_open[t]   for t in PINNED_TAGS],
    },
    'version': {
        'labels':     version_labels,
        'issue_open': version_counts,
    },
    'version_gantt': version_gantt,
    'fmea_tier': fmea_tier,
    'state': {
        'labels': [s[0] for s in state_sorted],
        'counts': [s[1] for s in state_sorted],
    },
    'req_state': {
        'labels': [s[0] for s in req_state_sorted],
        'counts': [s[1] for s in req_state_sorted],
    },
}

DATA_JSON = json.dumps(data, ensure_ascii=False)

TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IABGVOC Issue &amp; Requirement Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root{--sidebar:#1E0A4C;--purple:#6B21D9;--magenta:#E91E8C;--body-bg:#F0EFF6;--border:#E2E0EC;--text:#1E0A4C;--muted:#7B7A8E;}
*{margin:0;padding:0;box-sizing:border-box;}
html,body{font-family:'Segoe UI',system-ui,sans-serif;background:var(--body-bg);}
.app{display:flex;flex-direction:column;min-height:100vh;}
.body{display:flex;align-items:flex-start;}
.content{flex:1;padding:10px;display:flex;flex-direction:column;gap:8px;overflow-x:hidden;min-width:0;}
header{background:#1e293b;border-bottom:1px solid #334155;color:#fff;display:flex;align-items:center;gap:16px;padding:16px 32px;}
.header-text h1{font-size:1.25rem;font-weight:700;color:#f1f5f9;}
.header-text p{font-size:0.8rem;color:#94a3b8;margin-top:2px;}.card{background:#fff;border-radius:8px;border:1px solid var(--border);transition:box-shadow .2s;}
.card:hover{box-shadow:0 3px 14px rgba(107,33,217,.12);}
.kpi-row{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;}
.kpi-card{padding:10px 12px;cursor:default;}
.kpi-label{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.4px;color:var(--muted);margin-bottom:6px;}
.kpi-val{font-size:17px;font-weight:800;color:var(--text);}
.kpi-val.lg{font-size:14px;}
.kpi-donut-card{display:flex;align-items:center;gap:10px;}
.kpi-donut-wrap{flex-shrink:0;}
.kpi-donut-info{display:flex;flex-direction:column;min-width:0;}
.kpi-sub{font-size:10px;color:var(--muted);margin-bottom:4px;}
.middle-row{display:flex;flex-direction:column;gap:8px;}
.state-row{display:grid;grid-template-columns:1fr 1fr;gap:8px;height:260px;}
.state-panel{padding:10px 12px;display:flex;flex-direction:column;overflow:hidden;}
.state-inner{display:flex;gap:20px;flex:1;align-items:center;min-height:0;justify-content:center;}
.state-donut-wrap{flex-shrink:0;width:200px;height:200px;}
.state-list{width:210px;flex-shrink:0;display:flex;flex-direction:column;gap:5px;justify-content:center;}
.state-item{display:flex;align-items:center;gap:5px;font-size:10px;}
.si-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
.si-lbl{flex:1;color:var(--text);}
.si-val{font-weight:700;color:var(--text);flex-shrink:0;min-width:28px;text-align:right;}
.si-pct{color:var(--muted);flex-shrink:0;min-width:36px;text-align:right;}
.chart-pair{display:grid;grid-template-columns:1fr 1fr;gap:8px;height:260px;}
.center-panel{padding:10px 12px;display:flex;flex-direction:column;overflow:hidden;}
.line-card{width:100%;overflow:visible;}
.panel-title{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.4px;color:var(--text);margin-bottom:8px;}
.chart-wrap{position:relative;height:500px;}
.chart-scroll{width:100%;overflow-x:auto;overflow-y:hidden;height:310px;}
.line-legend{display:flex;justify-content:center;gap:20px;margin-top:8px;font-size:9px;color:#555;flex-wrap:wrap;}
.ll-item{display:flex;align-items:center;gap:5px;cursor:pointer;user-select:none;transition:opacity .15s;}
.ll-item:hover{opacity:.7;}
.ll-item.hidden{opacity:.35;text-decoration:line-through;}
.ll-swatch{display:inline-block;width:24px;height:0;border-top-width:2px;border-top-style:solid;}
.ll-dash{border-top-style:dashed;}
.gp-header{display:flex;align-items:flex-end;padding-bottom:6px;border-bottom:2px solid var(--border);margin-bottom:4px;}
.gp-lbl{width:130px;flex-shrink:0;font-size:11px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.4px;}
.gp-tl{flex:1;position:relative;height:24px;overflow:hidden;}
.gp-stats-hd{width:210px;flex-shrink:0;font-size:11px;color:var(--muted);text-align:right;padding-left:8px;}
.gp-row{display:flex;align-items:center;padding:10px 0;border-bottom:1px solid #F5F4FB;}
.gp-name{width:130px;flex-shrink:0;font-size:13px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.gp-area{flex:1;position:relative;height:44px;}
.gp-bar{position:absolute;top:0;height:100%;border-radius:6px;overflow:hidden;}
.gp-fill{height:100%;border-radius:6px;}
.gp-barlbl{position:absolute;top:50%;transform:translateY(-50%);font-size:13px;font-weight:700;white-space:nowrap;}
.gp-stat{width:210px;flex-shrink:0;font-size:11px;padding-left:8px;line-height:1.7;text-align:right;}
.summary-row{display:grid;grid-template-columns:1fr 1fr;gap:8px;}
.summary-card{padding:12px 16px;}
.summary-title{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--muted);margin-bottom:10px;border-bottom:1px solid var(--border);padding-bottom:6px;}
.summary-item{display:flex;align-items:flex-start;gap:8px;margin-bottom:8px;}
.summary-icon{flex-shrink:0;font-size:13px;line-height:1.5;}
.summary-label{font-size:10px;font-weight:700;color:var(--text);width:52px;flex-shrink:0;line-height:1.5;}
.summary-text{font-size:11px;color:var(--text);flex:1;min-height:20px;line-height:1.5;outline:none;border-bottom:1px dashed #c8c5dc;padding-bottom:1px;}
.summary-text:empty::before{content:attr(data-ph);color:#b0adc7;pointer-events:none;}
.summary-text:focus{border-bottom-color:var(--purple);}
</style>
</head>
<body>
<div class="app">
<header>
  <img src='data:image/png;base64,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' style="height:40px;" alt="logo">
  <div class="header-text">
    <h1>IABGVOC ISSUE &amp; REQUIREMENT DASHBOARD</h1>
    <p id="gen-date"></p>
  </div>
</header>
<div class="body">
<div class="content">
  <div class="summary-row">
    <div class="card summary-card">
      <div class="summary-title">執行摘要</div>
      <div class="summary-item">
        <span class="summary-icon">🟢</span>
        <span class="summary-label">Plan</span>
        <div class="summary-text" contenteditable="true" data-ph="請填入…"></div>
      </div>
      <div class="summary-item">
        <span class="summary-icon">🟡</span>
        <span class="summary-label">Progress</span>
        <div class="summary-text" contenteditable="true" data-ph="請填入…"></div>
      </div>
      <div class="summary-item">
        <span class="summary-icon">🔴</span>
        <span class="summary-label">Problem</span>
        <div class="summary-text" contenteditable="true" data-ph="請填入…"></div>
      </div>
    </div>
    <div class="card summary-card">
      <div class="summary-title">重要討論</div>
      <div class="summary-item">
        <span class="summary-icon">🟢</span>
        <span class="summary-label">決策</span>
        <div class="summary-text" contenteditable="true" data-ph="請填入…"></div>
      </div>
      <div class="summary-item">
        <span class="summary-icon">🟡</span>
        <span class="summary-label">討論中</span>
        <div class="summary-text" contenteditable="true" data-ph="請填入…"></div>
      </div>
      <div class="summary-item">
        <span class="summary-icon">🔴</span>
        <span class="summary-label">爭議項目</span>
        <div class="summary-text" contenteditable="true" data-ph="請填入…"></div>
      </div>
    </div>
  </div>
  <div class="kpi-row">
    <div class="card kpi-card kpi-donut-card">
      <div class="kpi-donut-wrap"><svg viewBox="0 0 40 40" width="56" height="56">
        <circle cx="20" cy="20" r="16" fill="none" stroke="#E5E3EF" stroke-width="5"/>
        <circle cx="20" cy="20" r="16" fill="none" stroke="#E5E3EF" stroke-width="5" stroke-dasharray="0 100.53" stroke-linecap="round" transform="rotate(-90 20 20)" id="d1-arc"/>
        <text x="20" y="23" text-anchor="middle" font-size="8.5" font-weight="800" fill="#1E0A4C" id="d1-pct">—</text>
      </svg></div>
      <div class="kpi-donut-info">
        <div class="kpi-label" style="margin-bottom:2px;">Open Issues</div>
        <div class="kpi-sub">Open vs Total</div>
        <div class="kpi-val lg" id="d1-val">&#8212;</div>
      </div>
    </div>
    <div class="card kpi-card kpi-donut-card">
      <div class="kpi-donut-wrap"><svg viewBox="0 0 40 40" width="56" height="56">
        <circle cx="20" cy="20" r="16" fill="none" stroke="#E5E3EF" stroke-width="5"/>
        <circle cx="20" cy="20" r="16" fill="none" stroke="#E5E3EF" stroke-width="5" stroke-dasharray="0 100.53" stroke-linecap="round" transform="rotate(-90 20 20)" id="d2-arc"/>
        <text x="20" y="23" text-anchor="middle" font-size="8.5" font-weight="800" fill="#1E0A4C" id="d2-pct">—</text>
      </svg></div>
      <div class="kpi-donut-info">
        <div class="kpi-label" style="margin-bottom:2px;">Blocker / Critical</div>
        <div class="kpi-sub">of Open Issues</div>
        <div class="kpi-val lg" id="d2-val">&#8212;</div>
      </div>
    </div>
    <div class="card kpi-card kpi-donut-card">
      <div class="kpi-donut-wrap"><svg viewBox="0 0 40 40" width="56" height="56">
        <circle cx="20" cy="20" r="16" fill="none" stroke="#E5E3EF" stroke-width="5"/>
        <circle cx="20" cy="20" r="16" fill="none" stroke="#E5E3EF" stroke-width="5" stroke-dasharray="0 100.53" stroke-linecap="round" transform="rotate(-90 20 20)" id="d3-arc"/>
        <text x="20" y="23" text-anchor="middle" font-size="8.5" font-weight="800" fill="#1E0A4C" id="d3-pct">—</text>
      </svg></div>
      <div class="kpi-donut-info">
        <div class="kpi-label" style="margin-bottom:2px;">FMEA High Risk</div>
        <div class="kpi-sub">FMEA &ge; <span id="d3-thr"></span></div>
        <div class="kpi-val lg" id="d3-val">&#8212;</div>
      </div>
    </div>
    <div class="card kpi-card kpi-donut-card">
      <div class="kpi-donut-wrap"><svg viewBox="0 0 40 40" width="56" height="56">
        <circle cx="20" cy="20" r="16" fill="none" stroke="#E5E3EF" stroke-width="5"/>
        <circle cx="20" cy="20" r="16" fill="none" stroke="#E5E3EF" stroke-width="5" stroke-dasharray="0 100.53" stroke-linecap="round" transform="rotate(-90 20 20)" id="d4-arc"/>
        <text x="20" y="23" text-anchor="middle" font-size="8.5" font-weight="800" fill="#1E0A4C" id="d4-pct">—</text>
      </svg></div>
      <div class="kpi-donut-info">
        <div class="kpi-label" style="margin-bottom:2px;">Open Reqs</div>
        <div class="kpi-sub">Open vs Total</div>
        <div class="kpi-val lg" id="d4-val">&#8212;</div>
      </div>
    </div>
    <div class="card kpi-card kpi-donut-card">
      <div class="kpi-donut-wrap"><svg viewBox="0 0 40 40" width="56" height="56">
        <circle cx="20" cy="20" r="16" fill="none" stroke="#E5E3EF" stroke-width="5"/>
        <circle cx="20" cy="20" r="16" fill="none" stroke="#E5E3EF" stroke-width="5" stroke-dasharray="0 100.53" stroke-linecap="round" transform="rotate(-90 20 20)" id="d5-arc"/>
        <text x="20" y="23" text-anchor="middle" font-size="8.5" font-weight="800" fill="#1E0A4C" id="d5-pct">—</text>
      </svg></div>
      <div class="kpi-donut-info">
        <div class="kpi-label" style="margin-bottom:2px;">Blocker / Critical Reqs</div>
        <div class="kpi-sub">of Open Reqs</div>
        <div class="kpi-val lg" id="d5-val">&#8212;</div>
      </div>
    </div>
    <div class="card kpi-card kpi-donut-card">
      <div class="kpi-donut-wrap"><svg viewBox="0 0 40 40" width="56" height="56">
        <circle cx="20" cy="20" r="16" fill="none" stroke="#E5E3EF" stroke-width="5"/>
        <circle cx="20" cy="20" r="16" fill="none" stroke="#E5E3EF" stroke-width="5" stroke-dasharray="0 100.53" stroke-linecap="round" transform="rotate(-90 20 20)" id="d6-arc"/>
        <text x="20" y="23" text-anchor="middle" font-size="8.5" font-weight="800" fill="#1E0A4C" id="d6-pct">—</text>
      </svg></div>
      <div class="kpi-donut-info">
        <div class="kpi-label" style="margin-bottom:2px;">FMEA High Risk Reqs</div>
        <div class="kpi-sub">FMEA &ge; <span id="d6-thr"></span></div>
        <div class="kpi-val lg" id="d6-val">&#8212;</div>
      </div>
    </div>
  </div>
  <div class="middle-row">
    <div class="state-row">
      <div class="card state-panel">
        <div class="panel-title">Issue State Distribution</div>
        <div class="state-inner">
          <div class="state-donut-wrap"><canvas id="issueDonutChart"></canvas></div>
          <div class="state-list" id="issue-state-list"></div>
        </div>
      </div>
      <div class="card state-panel">
        <div class="panel-title">Req State Distribution</div>
        <div class="state-inner">
          <div class="state-donut-wrap"><canvas id="reqDonutChart"></canvas></div>
          <div class="state-list" id="req-state-list"></div>
        </div>
      </div>
    </div>
    <div class="chart-pair">
      <div class="card center-panel">
        <div class="panel-title">Open Issues by Region</div>
        <div class="state-inner">
          <div class="state-donut-wrap"><canvas id="barChart"></canvas></div>
          <div class="state-list" id="region-list"></div>
        </div>
      </div>
      <div class="card center-panel">
        <div class="panel-title">Open Requirements by Region</div>
        <div class="state-inner">
          <div class="state-donut-wrap"><canvas id="reqRegionChart"></canvas></div>
          <div class="state-list" id="req-region-list"></div>
        </div>
      </div>
    </div>
    <div class="card center-panel" style="height:auto;overflow:visible;">
      <div class="panel-title">Issue Status by Version</div>
      <div id="issue-gantt" style="padding:4px 0;"></div>
    </div>
    <div class="card center-panel" style="height:auto;overflow:visible;">
      <div class="panel-title">Requirements Status by Version</div>
      <div id="req-gantt" style="padding:4px 0;"></div>
    </div>
    <div class="card center-panel line-card">
      <div class="panel-title">Issue &amp; Requirement 累計總數（逐季）</div>
      <div class="chart-wrap"><canvas id="lineChart"></canvas></div>
      <div class="line-legend">
        <div class="ll-item"><span class="ll-swatch" style="border-color:#C62828;"></span>Issue 總數</div>
        <div class="ll-item"><span class="ll-swatch" style="border-color:#1976D2;"></span>Req 總數</div>
        <div class="ll-item"><span class="ll-swatch" style="border-color:#000000;"></span>Issue+Req 總數</div>
      </div>
    </div>
  </div>
</div>
</div>
</div>
<script>
const DATA = __DATA__;

// Header
document.getElementById('gen-date').textContent = DATA.meta.generated_at;

// KPI cards
function drawKpi(arcId, pctId, valId, open, total) {
  open  = (open  != null) ? open  : 0;
  total = (total != null) ? total : 0;
  const pct  = total > 0 ? Math.round(open / total * 100) : 0;
  const circ = 100.53;
  const arc  = document.getElementById(arcId);
  arc.setAttribute('stroke-dasharray', (pct * circ / 100).toFixed(2) + ' ' + circ);
  arc.setAttribute('stroke', pct > 50 ? '#E53935' : '#43A047');
  document.getElementById(pctId).textContent = pct + '%';
  document.getElementById(valId).textContent = open.toLocaleString() + ' vs ' + total.toLocaleString();
}
drawKpi('d1-arc','d1-pct','d1-val', DATA.kpi.open_issues,         DATA.meta.total_issues);
drawKpi('d2-arc','d2-pct','d2-val', DATA.kpi.cb_open,             DATA.kpi.open_issues);
document.getElementById('d3-thr').textContent = DATA.kpi.fmea_threshold;
drawKpi('d3-arc','d3-pct','d3-val', DATA.kpi.fmea_high_open,      DATA.meta.total_issues);
drawKpi('d4-arc','d4-pct','d4-val', DATA.kpi.open_reqs,           DATA.meta.total_reqs);
drawKpi('d5-arc','d5-pct','d5-val', DATA.kpi.cb_open_reqs,        DATA.kpi.open_reqs);
document.getElementById('d6-thr').textContent = DATA.kpi.fmea_threshold;
drawKpi('d6-arc','d6-pct','d6-val', DATA.kpi.fmea_high_open_reqs, DATA.meta.total_reqs);

// State donut charts (Issue + Req split)
const STATE_COLORS = {
  'Closed':              '#388E3C',
  'Review & Approval':   '#81C784',
  'In Progress':         '#1976D2',
  'Verification':        '#F9A825',
  'Review':              '#C62828',
};
const STATE_COLOR_DEFAULT = '#9E9E9E';
function stateColor(lbl) { return STATE_COLORS[lbl] || STATE_COLOR_DEFAULT; }

function buildStateList(containerId, labels, counts, colorFn) {
  colorFn = colorFn || stateColor;
  const el = document.getElementById(containerId);
  const total = counts.reduce((a, b) => a + b, 0);
  labels.forEach((lbl, i) => {
    const pct = total > 0 ? Math.round(counts[i] / total * 100) : 0;
    const div = document.createElement('div');
    div.className = 'state-item';
    div.innerHTML = '<span class="si-dot" style="background:' + colorFn(lbl) + '"></span>'
      + '<span class="si-lbl">' + lbl + '</span>'
      + '<span class="si-val">' + counts[i].toLocaleString() + '</span>'
      + '<span class="si-pct">(' + pct + '%)</span>';
    el.appendChild(div);
  });
}
buildStateList('issue-state-list', DATA.state.labels, DATA.state.counts);
buildStateList('req-state-list', DATA.req_state.labels, DATA.req_state.counts);

new Chart(document.getElementById('issueDonutChart'), {
  type: 'doughnut',
  data: {
    labels: DATA.state.labels,
    datasets: [{ data: DATA.state.counts, backgroundColor: DATA.state.labels.map(stateColor), borderWidth: 2, borderColor: '#fff' }]
  },
  options: {
    responsive: true, maintainAspectRatio: false, cutout: '60%',
    plugins: {
      legend: { display: false },
      tooltip: { callbacks: { label: ctx => ctx.label + ': ' + ctx.raw.toLocaleString() } }
    }
  }
});

new Chart(document.getElementById('reqDonutChart'), {
  type: 'doughnut',
  data: {
    labels: DATA.req_state.labels,
    datasets: [{ data: DATA.req_state.counts, backgroundColor: DATA.req_state.labels.map(stateColor), borderWidth: 2, borderColor: '#fff' }]
  },
  options: {
    responsive: true, maintainAspectRatio: false, cutout: '60%',
    plugins: {
      legend: { display: false },
      tooltip: { callbacks: { label: ctx => ctx.label + ': ' + ctx.raw.toLocaleString() } }
    }
  }
});

// Region color map
const REGION_COLORS = {
  'IA Internal-SC':       '#ADD8E6',
  'DGC-China':            '#FFCDD2',
  'IA Internal-IMSBU':    '#C8E6C9',
  'IA Internal-CoreTech': '#E1BEE7',
};
const REGION_COLOR_DEFAULT = '#CFD8DC';
function regionColor(lbl) { return REGION_COLORS[lbl] || REGION_COLOR_DEFAULT; }

// Open Issues by Region donut chart
buildStateList('region-list', DATA.region.labels, DATA.region.issue_open, regionColor);
new Chart(document.getElementById('barChart'), {
  type: 'doughnut',
  data: {
    labels: DATA.region.labels,
    datasets: [{ data: DATA.region.issue_open,
                 backgroundColor: DATA.region.labels.map(regionColor),
                 borderWidth: 2, borderColor: '#fff' }]
  },
  options: {
    responsive: true, maintainAspectRatio: false, cutout: '60%',
    plugins: {
      legend: { display: false },
      tooltip: { callbacks: { label: ctx => ctx.label + ': ' + ctx.raw.toLocaleString() } }
    }
  }
});

// Open Requirements by Region donut chart
buildStateList('req-region-list', DATA.region.labels, DATA.region.req_open, regionColor);
new Chart(document.getElementById('reqRegionChart'), {
  type: 'doughnut',
  data: {
    labels: DATA.region.labels,
    datasets: [{ data: DATA.region.req_open,
                 backgroundColor: DATA.region.labels.map(regionColor),
                 borderWidth: 2, borderColor: '#fff' }]
  },
  options: {
    responsive: true, maintainAspectRatio: false, cutout: '60%',
    plugins: {
      legend: { display: false },
      tooltip: { callbacks: { label: ctx => ctx.label + ': ' + ctx.raw.toLocaleString() } }
    }
  }
});

// Issue verification Gantt
(function() {
  var el    = document.getElementById('issue-gantt');
  var GP_S  = new Date('2025-10-01');
  var GP_E  = new Date('2026-12-31');
  var GP_NOW = new Date(DATA.meta.generated_at);
  var GP_MS = GP_E - GP_S;
  var MABBR = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  function lp(d) { return Math.max(0, Math.min(100, (d - GP_S) / GP_MS * 100)); }
  function wp(s, e) { return Math.max(0.3, Math.min(100, (e - s) / GP_MS * 100)); }
  var todayL = lp(GP_NOW).toFixed(2);
  var ticks = '';
  var mc = new Date(GP_S.getFullYear(), GP_S.getMonth(), 1);
  while (mc <= GP_E) {
    var isJan = mc.getMonth() === 0;
    var isQ   = mc.getMonth() % 3 === 0;
    var lbl   = isJan ? String(mc.getFullYear()) : (isQ ? MABBR[mc.getMonth()] : '');
    if (lbl) {
      ticks += '<span style="position:absolute;left:' + lp(mc).toFixed(2) + '%;'
             + 'font-size:11px;font-weight:' + (isJan ? 700 : 400) + ';'
             + 'color:' + (isJan ? '#1E0A4C' : '#9CA3AF') + ';'
             + 'white-space:nowrap;padding-left:2px;'
             + 'border-left:1px solid ' + (isJan ? '#CBD5E1' : '#E2E0EC') + '">' + lbl + '</span>';
    }
    mc.setMonth(mc.getMonth() + 1);
  }
  var todayHdr = '<div style="position:absolute;left:' + todayL + '%;top:0;height:100%;'
               + 'width:2px;background:#E91E8C;z-index:4;">'
               + '<span style="position:absolute;bottom:100%;left:3px;font-size:11px;'
               + 'color:#E91E8C;font-weight:700;white-space:nowrap">Today</span></div>';
  var rows = (DATA.version_gantt || []).map(function(o) {
    var startD = new Date(o.start_date);
    var relD   = new Date(o.release_date);
    var barL   = lp(startD).toFixed(2);
    var bw     = wp(startD, relD).toFixed(2);
    var isDone    = o.total > 0 && o.closed === o.total;
    var isPast    = relD < GP_NOW;
    var isCurrent = startD <= GP_NOW && GP_NOW <= relD;
    var barClr = isDone ? '#43A047' : isPast ? '#E53935' : isCurrent ? '#3B82F6' : '#9CA3AF';
    var bgClr  = isDone ? '#E8F5E9' : isPast ? '#FEECEC' : isCurrent ? '#EBF3FF' : '#F1F1F1';
    var daysStr = '', daysClr = '#7B7A8E';
    if (!isDone) {
      if (o.days_left > 0) {
        daysStr = '剩 ' + o.days_left + 'd';
        daysClr = o.days_left < 30 ? '#E53935' : (o.days_left < 90 ? '#F59E0B' : '#43A047');
      } else {
        daysStr = '逾期 ' + (-o.days_left) + 'd';
        daysClr = '#9CA3AF';
      }
    }
    var nameClr = isPast ? '#9CA3AF' : '#1E0A4C';
    var lblLeft = (parseFloat(barL) + parseFloat(bw) + 0.8).toFixed(2);
    var todayBar = '<div style="position:absolute;top:0;bottom:0;left:' + todayL + '%;'
                 + 'width:2px;background:#E91E8C;z-index:3;border-radius:1px;"></div>';
    var shortLbl = o.label.replace('DIADesigner ', '');
    return '<div class="gp-row">'
      + '<div class="gp-name" style="color:' + nameClr + '">' + shortLbl + '</div>'
      + '<div class="gp-area">'
        + '<div class="gp-bar" style="left:' + barL + '%;width:' + bw + '%;background:' + bgClr + '">'
          + '<div class="gp-fill" style="width:' + o.pct.toFixed(1) + '%;background:' + barClr + '"></div>'
        + '</div>'
        + '<span class="gp-barlbl" style="left:' + lblLeft + '%;color:#1E0A4C">' + o.pct.toFixed(1) + '%</span>'
        + todayBar
      + '</div>'
      + '<div class="gp-stat">'
        + '<span style="font-weight:700;color:#1E0A4C">' + o.closed + '/' + o.total + '</span>'
        + '<span style="color:#7B7A8E;font-size:10px">&nbsp;(' + o.pct.toFixed(1) + '%)</span>'
        + (daysStr ? '&nbsp;&nbsp;<span style="color:' + daysClr + ';font-weight:600">' + daysStr + '</span>' : '')
        + '<br><span style="color:#9CA3AF;font-size:10px">' + o.release_date + '</span>'
      + '</div>'
      + '</div>';
  }).join('');
  el.innerHTML = '<div>'
    + '<div class="gp-header">'
      + '<div class="gp-lbl">版本</div>'
      + '<div class="gp-tl">' + ticks + todayHdr + '</div>'
      + '<div class="gp-stats-hd">已關閉/總數 &nbsp;·&nbsp; 剩餘 / 發行日</div>'
    + '</div>'
    + rows
    + '</div>';
}());

// Requirements verification Gantt
(function() {
  var el    = document.getElementById('req-gantt');
  var GP_S  = new Date('2025-10-01');
  var GP_E  = new Date('2026-12-31');
  var GP_NOW = new Date(DATA.meta.generated_at);
  var GP_MS = GP_E - GP_S;
  var MABBR = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  function lp(d) { return Math.max(0, Math.min(100, (d - GP_S) / GP_MS * 100)); }
  function wp(s, e) { return Math.max(0.3, Math.min(100, (e - s) / GP_MS * 100)); }
  var todayL = lp(GP_NOW).toFixed(2);
  var ticks = '';
  var mc = new Date(GP_S.getFullYear(), GP_S.getMonth(), 1);
  while (mc <= GP_E) {
    var isJan = mc.getMonth() === 0;
    var isQ   = mc.getMonth() % 3 === 0;
    var lbl   = isJan ? String(mc.getFullYear()) : (isQ ? MABBR[mc.getMonth()] : '');
    if (lbl) {
      ticks += '<span style="position:absolute;left:' + lp(mc).toFixed(2) + '%;'
             + 'font-size:11px;font-weight:' + (isJan ? 700 : 400) + ';'
             + 'color:' + (isJan ? '#1E0A4C' : '#9CA3AF') + ';'
             + 'white-space:nowrap;padding-left:2px;'
             + 'border-left:1px solid ' + (isJan ? '#CBD5E1' : '#E2E0EC') + '">' + lbl + '</span>';
    }
    mc.setMonth(mc.getMonth() + 1);
  }
  var todayHdr = '<div style="position:absolute;left:' + todayL + '%;top:0;height:100%;'
               + 'width:2px;background:#E91E8C;z-index:4;">'
               + '<span style="position:absolute;bottom:100%;left:3px;font-size:11px;'
               + 'color:#E91E8C;font-weight:700;white-space:nowrap">Today</span></div>';
  var rows = (DATA.version_gantt || []).map(function(o) {
    var startD = new Date(o.start_date);
    var relD   = new Date(o.release_date);
    var barL   = lp(startD).toFixed(2);
    var bw     = wp(startD, relD).toFixed(2);
    var isDone    = o.req_total > 0 && o.req_closed === o.req_total;
    var isPast    = relD < GP_NOW;
    var isCurrent = startD <= GP_NOW && GP_NOW <= relD;
    var barClr = isDone ? '#43A047' : isPast ? '#E53935' : isCurrent ? '#3B82F6' : '#9CA3AF';
    var bgClr  = isDone ? '#E8F5E9' : isPast ? '#FEECEC' : isCurrent ? '#EBF3FF' : '#F1F1F1';
    var daysStr = '', daysClr = '#7B7A8E';
    if (!isDone) {
      if (o.days_left > 0) {
        daysStr = '剩 ' + o.days_left + 'd';
        daysClr = o.days_left < 30 ? '#E53935' : (o.days_left < 90 ? '#F59E0B' : '#43A047');
      } else {
        daysStr = '逾期 ' + (-o.days_left) + 'd';
        daysClr = '#9CA3AF';
      }
    }
    var nameClr = isPast ? '#9CA3AF' : '#1E0A4C';
    var lblLeft = (parseFloat(barL) + parseFloat(bw) + 0.8).toFixed(2);
    var todayBar = '<div style="position:absolute;top:0;bottom:0;left:' + todayL + '%;'
                 + 'width:2px;background:#E91E8C;z-index:3;border-radius:1px;"></div>';
    var shortLbl = o.label.replace('DIADesigner ', '');
    return '<div class="gp-row">'
      + '<div class="gp-name" style="color:' + nameClr + '">' + shortLbl + '</div>'
      + '<div class="gp-area">'
        + '<div class="gp-bar" style="left:' + barL + '%;width:' + bw + '%;background:' + bgClr + '">'
          + '<div class="gp-fill" style="width:' + o.req_pct.toFixed(1) + '%;background:' + barClr + '"></div>'
        + '</div>'
        + '<span class="gp-barlbl" style="left:' + lblLeft + '%;color:#1E0A4C">' + o.req_pct.toFixed(1) + '%</span>'
        + todayBar
      + '</div>'
      + '<div class="gp-stat">'
        + '<span style="font-weight:700;color:#6B21D9">' + o.req_closed + '/' + o.req_total + '</span>'
        + '<span style="color:#7B7A8E;font-size:10px">&nbsp;(' + o.req_pct.toFixed(1) + '%)</span>'
        + (daysStr ? '&nbsp;&nbsp;<span style="color:' + daysClr + ';font-weight:600">' + daysStr + '</span>' : '')
        + '<br><span style="color:#9CA3AF;font-size:10px">' + o.release_date + '</span>'
      + '</div>'
      + '</div>';
  }).join('');
  el.innerHTML = '<div>'
    + '<div class="gp-header">'
      + '<div class="gp-lbl">版本</div>'
      + '<div class="gp-tl">' + ticks + todayHdr + '</div>'
      + '<div class="gp-stats-hd">已關閉/總數 &nbsp;·&nbsp; 剩餘 / 發行日</div>'
    + '</div>'
    + rows
    + '</div>';
}());

// Line chart: 3 cumulative lines
const _lineCanvas = document.getElementById('lineChart');

const lineChart = new Chart(_lineCanvas, {
  type: 'line',
  data: {
    labels: DATA.monthly.labels,
    datasets: [
      { label: 'Issue 總數',    data: DATA.monthly.issue_total,
        borderColor: '#C62828', borderWidth: 2, pointRadius: 3, tension: .3,
        fill: false, pointBackgroundColor: '#C62828' },
      { label: 'Req 總數',     data: DATA.monthly.req_total,
        borderColor: '#1976D2', borderWidth: 2, pointRadius: 3, tension: .3,
        fill: false, pointBackgroundColor: '#1976D2' },
      { label: 'Issue+Req 總數', data: DATA.monthly.combined_total,
        borderColor: '#000000', borderWidth: 2, pointRadius: 3, tension: .3,
        fill: false, pointBackgroundColor: '#000000' }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: 'index', intersect: false },
    plugins: {
      legend: { display: false },
      tooltip: { mode: 'index', intersect: false }
    },
    scales: {
      y: { grid: { color: '#F0EFF6' }, ticks: { font: { size: 9 } } },
      x: { grid: { display: false }, ticks: { font: { size: 9 }, maxRotation: 0 } }
    }
  }
});
document.querySelectorAll('.ll-item').forEach((item, i) => {
  item.addEventListener('click', () => {
    const meta = lineChart.getDatasetMeta(i);
    meta.hidden = !meta.hidden;
    lineChart.update();
    item.classList.toggle('hidden', meta.hidden);
  });
});
</script>
</body>
</html>"""

html = TEMPLATE.replace('__DATA__', DATA_JSON)
with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Dashboard generated: {OUT_PATH}")

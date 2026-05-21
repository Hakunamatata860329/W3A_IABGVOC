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
        'labels':        monthly_labels,
        'issue_created': [monthly_data[k]['ic'] for k in monthly_keys],
        'issue_closed':  [monthly_data[k]['il'] for k in monthly_keys],
        'req_created':   [monthly_data[k]['rc'] for k in monthly_keys],
        'req_closed':    [monthly_data[k]['rl'] for k in monthly_keys],
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
header{background:var(--sidebar);color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 18px;height:46px;flex-shrink:0;position:sticky;top:0;z-index:10;}
.h-left{display:flex;align-items:center;gap:10px;}
.h-title{font-size:13px;font-weight:700;letter-spacing:.3px;}
.h-nav{display:flex;align-items:stretch;margin-left:20px;}
.h-nav-item{display:flex;align-items:center;padding:0 16px;font-size:12px;cursor:pointer;color:#C5C0D9;border-bottom:2px solid transparent;height:100%;}
.h-nav-item:hover{color:#fff;background:rgba(255,255,255,.06);}
.h-nav-item.active{color:#fff;border-bottom-color:var(--magenta);}
.h-right{display:flex;align-items:center;gap:6px;font-size:12px;color:#C5C0D9;}
.h-right strong{color:#fff;}
.card{background:#fff;border-radius:8px;border:1px solid var(--border);transition:box-shadow .2s;}
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
.chart-wrap{position:relative;height:210px;}
.chart-scroll{width:100%;overflow-x:auto;overflow-y:hidden;height:310px;}
.line-legend{display:flex;justify-content:center;gap:20px;margin-top:8px;font-size:9px;color:#555;flex-wrap:wrap;}
.ll-item{display:flex;align-items:center;gap:5px;cursor:pointer;user-select:none;transition:opacity .15s;}
.ll-item:hover{opacity:.7;}
.ll-item.hidden{opacity:.35;text-decoration:line-through;}
.ll-swatch{display:inline-block;width:24px;height:0;border-top-width:2px;border-top-style:solid;}
.ll-dash{border-top-style:dashed;}
.line-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:8px;}
.ls{text-align:center;background:#F7F5FF;border-radius:6px;padding:6px;}
.ls-year{font-size:10px;font-weight:700;color:var(--purple);margin-bottom:4px;}
.ls-lbl{font-size:8px;color:var(--muted);margin-bottom:3px;line-height:1.3;}
.ls-val{font-size:14px;font-weight:800;color:var(--text);}
</style>
</head>
<body>
<div class="app">
<header>
  <div class="h-left">
    <img src="../logo.png" style="height:32px;width:auto;" alt="logo">
    <span class="h-title">IABGVOC ISSUE &amp; REQUIREMENT DASHBOARD</span>
  </div>
  <div class="h-right">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#C5C0D9" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/>
      <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
    </svg>
    <span><strong>Generated</strong>&nbsp;&nbsp;<span id="gen-date"></span></span>
  </div>
</header>
<div class="body">
<div class="content">
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
        <div class="panel-title">Open Issues + Requirements by Region</div>
        <div class="state-inner">
          <div class="state-donut-wrap"><canvas id="barChart"></canvas></div>
          <div class="state-list" id="region-list"></div>
        </div>
      </div>
      <div class="card center-panel">
        <div class="panel-title">Open Issues + Requirements by Tag</div>
        <div class="state-inner">
          <div class="state-donut-wrap"><canvas id="tagChart"></canvas></div>
          <div class="state-list" id="tag-list"></div>
        </div>
      </div>
    </div>
    <div class="card center-panel line-card">
      <div class="panel-title">Issue &amp; Requirement Trend (2025–2026)</div>
      <div class="chart-scroll"><div class="chart-wrap" id="lineChart-wrap"><canvas id="lineChart"></canvas></div></div>
      <div class="line-legend">
        <div class="ll-item"><span class="ll-swatch" style="border-color:#6B21D9;"></span>Issue Created</div>
        <div class="ll-item"><span class="ll-swatch" style="border-color:#1E0A4C;"></span>Issue Closed</div>
        <div class="ll-item"><span class="ll-swatch ll-dash" style="border-color:#00BCD4;"></span>Req Created</div>
        <div class="ll-item"><span class="ll-swatch ll-dash" style="border-color:#E91E8C;"></span>Req Closed</div>
      </div>
      <div class="line-stats">
        <div class="ls">
          <div class="ls-year" id="stat-year">&#8212;</div>
          <div class="ls-lbl">Issue Created</div>
          <div class="ls-val" id="stat-ic">&#8212;</div>
        </div>
        <div class="ls">
          <div class="ls-year">&nbsp;</div>
          <div class="ls-lbl">Issue Closed</div>
          <div class="ls-val" id="stat-il">&#8212;</div>
        </div>
        <div class="ls">
          <div class="ls-year">&nbsp;</div>
          <div class="ls-lbl">Req Created</div>
          <div class="ls-val" id="stat-rc">&#8212;</div>
        </div>
        <div class="ls">
          <div class="ls-year">&nbsp;</div>
          <div class="ls-lbl">Req Closed</div>
          <div class="ls-val" id="stat-rl">&#8212;</div>
        </div>
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
const C1 = ['#26C6DA','#6B21D9','#CE93D8','#9B59D4','#00BCD4','#9E9E9E'];
const C2 = ['#FDD835','#FF7043','#42A5F5','#AB47BC','#66BB6A','#EC407A'];

function buildStateList(containerId, labels, counts, colors) {
  const el = document.getElementById(containerId);
  const total = counts.reduce((a, b) => a + b, 0);
  labels.forEach((lbl, i) => {
    const pct = total > 0 ? Math.round(counts[i] / total * 100) : 0;
    const div = document.createElement('div');
    div.className = 'state-item';
    div.innerHTML = '<span class="si-dot" style="background:' + colors[i] + '"></span>'
      + '<span class="si-lbl">' + lbl + '</span>'
      + '<span class="si-val">' + counts[i].toLocaleString() + '</span>'
      + '<span class="si-pct">(' + pct + '%)</span>';
    el.appendChild(div);
  });
}
buildStateList('issue-state-list', DATA.state.labels, DATA.state.counts, C1);
buildStateList('req-state-list', DATA.req_state.labels, DATA.req_state.counts, C2);

new Chart(document.getElementById('issueDonutChart'), {
  type: 'doughnut',
  data: {
    labels: DATA.state.labels,
    datasets: [{ data: DATA.state.counts, backgroundColor: C1, borderWidth: 2, borderColor: '#fff' }]
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
    datasets: [{ data: DATA.req_state.counts, backgroundColor: C2, borderWidth: 2, borderColor: '#fff' }]
  },
  options: {
    responsive: true, maintainAspectRatio: false, cutout: '60%',
    plugins: {
      legend: { display: false },
      tooltip: { callbacks: { label: ctx => ctx.label + ': ' + ctx.raw.toLocaleString() } }
    }
  }
});

// Region donut chart: issue_open + req_open per region
const regionTotal = DATA.region.issue_open.map((v, i) => v + DATA.region.req_open[i]);
const RC = ['#6B21D9','#00BCD4','#E91E8C','#FDD835','#FF7043','#42A5F5','#66BB6A'];
buildStateList('region-list', DATA.region.labels, regionTotal, RC.slice(0, regionTotal.length));
new Chart(document.getElementById('barChart'), {
  type: 'doughnut',
  data: {
    labels: DATA.region.labels,
    datasets: [{ data: regionTotal,
                 backgroundColor: RC.slice(0, regionTotal.length),
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

// Tag donut chart: issue_open + req_open per pinned tag
const tagTotal = DATA.tag_open.issue_open.map((v, i) => v + DATA.tag_open.req_open[i]);
const TC = ['#FF7043','#6B21D9','#00BCD4','#FDD835','#66BB6A'];
buildStateList('tag-list', DATA.tag_open.labels, tagTotal, TC.slice(0, tagTotal.length));
new Chart(document.getElementById('tagChart'), {
  type: 'doughnut',
  data: {
    labels: DATA.tag_open.labels,
    datasets: [{ data: tagTotal,
                 backgroundColor: TC.slice(0, tagTotal.length),
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

// Line chart: 4 lines + hover-driven stat boxes
function updateLineStats(idx) {
  document.getElementById('stat-year').textContent = DATA.monthly.labels[idx];
  document.getElementById('stat-ic').textContent = DATA.monthly.issue_created[idx].toLocaleString();
  document.getElementById('stat-il').textContent = DATA.monthly.issue_closed[idx].toLocaleString();
  document.getElementById('stat-rc').textContent = DATA.monthly.req_created[idx].toLocaleString();
  document.getElementById('stat-rl').textContent = DATA.monthly.req_closed[idx].toLocaleString();
}
updateLineStats(DATA.monthly.labels.length - 1);

const _lineCanvas   = document.getElementById('lineChart');
const _scrollEl     = _lineCanvas.closest('.chart-scroll');
const _containerW   = _scrollEl.clientWidth;
const MONTHS_VISIBLE = 6;
const _lineWidth    = Math.round(DATA.monthly.labels.length * _containerW / MONTHS_VISIBLE);
_lineCanvas.width   = _lineWidth;
_lineCanvas.height  = 310;
const _lineWrap = document.getElementById('lineChart-wrap');
_lineWrap.style.width  = _lineWidth + 'px';
_lineWrap.style.height = '310px';

const lineChart = new Chart(_lineCanvas, {
  type: 'line',
  data: {
    labels: DATA.monthly.labels,
    datasets: [
      { label: 'Issue Created', data: DATA.monthly.issue_created,
        borderColor: '#6B21D9', borderWidth: 2, pointRadius: 3, tension: .3,
        fill: false, pointBackgroundColor: '#6B21D9' },
      { label: 'Issue Closed',  data: DATA.monthly.issue_closed,
        borderColor: '#1E0A4C', borderWidth: 2, pointRadius: 3, tension: .3,
        fill: false, pointBackgroundColor: '#1E0A4C' },
      { label: 'Req Created',   data: DATA.monthly.req_created,
        borderColor: '#00BCD4', borderWidth: 2, pointRadius: 3, tension: .3,
        fill: false, borderDash: [6, 4], pointBackgroundColor: '#00BCD4' },
      { label: 'Req Closed',    data: DATA.monthly.req_closed,
        borderColor: '#E91E8C', borderWidth: 2, pointRadius: 3, tension: .3,
        fill: false, borderDash: [6, 4], pointBackgroundColor: '#E91E8C' }
    ]
  },
  options: {
    responsive: false,
    interaction: { mode: 'index', intersect: false },
    onHover: (evt, elements) => {
      if (elements.length > 0) updateLineStats(elements[0].index);
    },
    plugins: {
      legend: { display: false },
      tooltip: { mode: 'index', intersect: false }
    },
    scales: {
      y: { grid: { color: '#F0EFF6' }, ticks: { font: { size: 8 } } },
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

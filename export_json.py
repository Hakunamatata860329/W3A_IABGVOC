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
cb_open        = [r for r in open_issues if r.get('Severity', '').strip() in ('Blocker', 'Critical')]
fmea_high_open = [r for r in open_issues if fmea_val(r) >= FMEA_HIGH]

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
        'cb_open':        len(cb_open),
        'fmea_high_open': len(fmea_high_open),
        'fmea_threshold': FMEA_HIGH,
    },
    'trend': {
        'years':         years,
        'issue_created': [year_data[y]['ic'] for y in years],
        'issue_closed':  [year_data[y]['il'] for y in years],
        'req_created':   [year_data[y]['rc'] for y in years],
        'req_closed':    [year_data[y]['rl'] for y in years],
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
html,body{height:100%;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;background:var(--body-bg);}
.app{display:flex;flex-direction:column;height:100vh;}
.body{display:flex;flex:1;overflow:hidden;}
.content{flex:1;overflow-y:auto;padding:10px;display:flex;flex-direction:column;gap:8px;}
header{background:var(--sidebar);color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 18px;height:46px;flex-shrink:0;}
.h-left{display:flex;align-items:center;gap:10px;}
.logo-diamond{width:32px;height:32px;background:#C62828;clip-path:polygon(50% 0%,100% 50%,50% 100%,0% 50%);display:grid;place-items:center;}
.logo-diamond svg{width:14px;height:14px;fill:white;}
.h-title{font-size:13px;font-weight:700;letter-spacing:.3px;}
.h-right{display:flex;align-items:center;gap:6px;font-size:12px;color:#C5C0D9;}
.h-right strong{color:#fff;}
aside{width:176px;background:var(--sidebar);color:#fff;display:flex;flex-direction:column;padding:12px 0;flex-shrink:0;overflow-y:auto;}
.nav-item{display:flex;align-items:center;gap:8px;padding:9px 14px;font-size:12px;cursor:pointer;border-left:3px solid transparent;color:#C0BBDA;transition:background .15s;}
.nav-item:hover{background:rgba(255,255,255,.07);}
.nav-item.active{border-left-color:var(--magenta);color:#fff;background:rgba(255,255,255,.05);}
.sb-section{padding:0 14px;margin-top:18px;}
.sb-head{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:#7B6FAA;margin-bottom:8px;}
.fi{padding:6px 8px;font-size:11px;color:#A89FCC;cursor:pointer;border-radius:4px;transition:all .15s;}
.fi:hover,.fi.active{background:rgba(107,33,217,.45);color:#fff;}
.pill-grid{display:grid;grid-template-columns:1fr 1fr;gap:5px;}
.pill{padding:5px;font-size:10px;font-weight:600;background:rgba(255,255,255,.08);border-radius:4px;text-align:center;cursor:pointer;color:#A89FCC;transition:all .15s;}
.pill:hover,.pill.active{background:var(--purple);color:#fff;}
.card{background:#fff;border-radius:8px;border:1px solid var(--border);transition:box-shadow .2s;}
.card:hover{box-shadow:0 3px 14px rgba(107,33,217,.12);}
.kpi-row{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;flex-shrink:0;}
.kpi-card{padding:10px 12px;cursor:default;}
.kpi-label{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.4px;color:var(--muted);margin-bottom:6px;}
.kpi-val{font-size:17px;font-weight:800;color:var(--text);}
.kpi-val.lg{font-size:14px;}
.kpi-val.magenta{color:var(--magenta);font-size:22px;}
.pat-sub{font-size:8px;color:var(--muted);margin-top:2px;margin-bottom:5px;}
.pat-track{display:flex;align-items:center;gap:5px;}
.pat-bar{flex:1;height:7px;background:#E5E3EF;border-radius:4px;overflow:hidden;}
.pat-fill{height:100%;background:var(--purple);border-radius:4px;transition:width .5s;}
.pat-end{font-size:9px;color:var(--muted);}
.middle-row{display:grid;grid-template-columns:220px 1fr;gap:8px;flex:1;min-height:0;}
.left-panel{display:flex;flex-direction:column;padding:12px;}
.proj-stats{display:flex;justify-content:space-around;padding-bottom:8px;border-bottom:1px solid var(--border);flex-shrink:0;}
.ps{text-align:center;flex:1;}
.ps-lbl{font-size:8px;color:var(--muted);margin-bottom:2px;word-break:break-all;line-height:1.2;}
.ps-val{font-size:15px;font-weight:800;color:var(--text);}
.donut-wrap{flex:1;position:relative;min-height:0;display:flex;align-items:center;}
.donut-wrap canvas{max-width:100%;max-height:100%;}
.sector-stats{display:flex;justify-content:space-around;padding-top:8px;border-top:1px solid var(--border);flex-shrink:0;}
.ss{text-align:center;font-size:9px;color:var(--muted);flex:1;}
.ss strong{display:block;font-size:14px;font-weight:800;color:var(--text);}
.ss span{font-size:8px;}
.center-col{display:flex;flex-direction:column;gap:8px;}
.center-top,.center-bot{padding:10px 12px;display:flex;flex-direction:column;}
.panel-title{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.4px;color:var(--text);margin-bottom:8px;}
.chart-wrap{position:relative;flex:1;min-height:0;}
.line-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:8px;flex-shrink:0;}
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
    <div class="logo-diamond"><svg viewBox="0 0 20 20"><polygon points="10,2 18,10 10,18 2,10"/></svg></div>
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
<aside>
  <div class="nav-item active" onclick="setNav(this)">&#128202; Main Dashboard</div>
  <div class="nav-item" onclick="setNav(this)">&#128269; Issue Details</div>
  <div class="nav-item" onclick="setNav(this)">&#128203; Req Details</div>
  <div class="sb-section">
    <div class="sb-head">Year</div>
    <div id="year-filters"></div>
  </div>
  <div class="sb-section">
    <div class="sb-head">Issue State</div>
    <div id="state-filters"></div>
  </div>
  <div class="sb-section">
    <div class="sb-head">Region</div>
    <div id="region-filters" class="pill-grid"></div>
  </div>
</aside>
<div class="content">
  <div class="kpi-row">
    <div class="card kpi-card">
      <div class="kpi-label">Total Issues</div>
      <div class="kpi-val" id="kpi1-val">&#8212;</div>
    </div>
    <div class="card kpi-card">
      <div class="kpi-label">Open Issues</div>
      <div class="kpi-val" id="kpi2-val">&#8212;</div>
    </div>
    <div class="card kpi-card">
      <div class="kpi-label">Total Reqs</div>
      <div class="kpi-val lg" id="kpi3-val">&#8212;</div>
    </div>
    <div class="card kpi-card">
      <div class="kpi-label">Open Reqs</div>
      <div class="kpi-val lg" id="kpi4-val">&#8212;</div>
    </div>
    <div class="card kpi-card">
      <div class="kpi-label">Blocker / Critical</div>
      <div class="kpi-val lg" id="kpi5-val">&#8212;</div>
    </div>
    <div class="card kpi-card">
      <div class="kpi-label">FMEA High Risk</div>
      <div class="kpi-val magenta" id="kpi6-pct">&#8212;</div>
      <div class="pat-sub">FMEA &ge; <span id="kpi6-thr"></span></div>
      <div class="pat-track">
        <div class="pat-bar"><div class="pat-fill" id="kpi6-fill" style="width:0%"></div></div>
        <span class="pat-end">100%</span>
      </div>
    </div>
  </div>
  <div class="middle-row">
    <div class="card left-panel">
      <div class="proj-stats" id="proj-stats"></div>
      <div class="donut-wrap"><canvas id="donutChart"></canvas></div>
      <div class="sector-stats" id="sector-stats"></div>
    </div>
    <div class="center-col">
      <div class="card center-top" style="height:46%">
        <div class="panel-title">Open Issues + Requirements by Region</div>
        <div class="chart-wrap"><canvas id="barChart"></canvas></div>
      </div>
      <div class="card center-bot" style="flex:1;min-height:0">
        <div class="panel-title">Issue &amp; Requirement Trend by Year</div>
        <div class="chart-wrap"><canvas id="lineChart"></canvas></div>
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
</div>
<script>
const DATA = __DATA__;

function setNav(el) {
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  el.classList.add('active');
}
function toggleFi(el) { el.classList.toggle('active'); }
function togglePill(el) { el.classList.toggle('active'); }

// Populate sidebar filters from real data
const yf = document.getElementById('year-filters');
DATA.trend.years.forEach((y, i) => {
  const d = document.createElement('div');
  d.className = 'fi' + (i === DATA.trend.years.length - 1 ? ' active' : '');
  d.textContent = y;
  d.onclick = () => toggleFi(d);
  yf.appendChild(d);
});
const sf = document.getElementById('state-filters');
DATA.state.labels.slice(0, 6).forEach((s, i) => {
  const d = document.createElement('div');
  d.className = 'fi' + (i === 0 ? ' active' : '');
  d.textContent = s;
  d.onclick = () => toggleFi(d);
  sf.appendChild(d);
});
const rf = document.getElementById('region-filters');
DATA.region.labels.slice(0, 6).forEach((r, i) => {
  const d = document.createElement('div');
  d.className = 'pill' + (i === 0 ? ' active' : '');
  d.textContent = r;
  d.onclick = () => togglePill(d);
  rf.appendChild(d);
});

// Header
document.getElementById('gen-date').textContent = DATA.meta.generated_at;

// KPI cards
document.getElementById('kpi1-val').textContent = DATA.meta.total_issues.toLocaleString();
document.getElementById('kpi2-val').textContent = DATA.kpi.open_issues.toLocaleString();
document.getElementById('kpi3-val').textContent = DATA.meta.total_reqs.toLocaleString();
document.getElementById('kpi4-val').textContent = DATA.kpi.open_reqs.toLocaleString();
document.getElementById('kpi5-val').textContent = DATA.kpi.cb_open.toLocaleString();
const fmeaPct = DATA.meta.total_issues > 0
  ? Math.round(DATA.kpi.fmea_high_open / DATA.meta.total_issues * 100) : 0;
document.getElementById('kpi6-pct').textContent = fmeaPct + '%';
document.getElementById('kpi6-thr').textContent = DATA.kpi.fmea_threshold;
document.getElementById('kpi6-fill').style.width = fmeaPct + '%';

// Donut top stats: top 3 Issue states
const ps = document.getElementById('proj-stats');
DATA.state.labels.slice(0, 3).forEach((lbl, i) => {
  const div = document.createElement('div');
  div.className = 'ps';
  div.innerHTML = '<div class="ps-lbl">' + lbl + '</div>'
    + '<div class="ps-val">' + DATA.state.counts[i].toLocaleString() + '</div>';
  ps.appendChild(div);
});

// Donut bottom stats: top 2 Req states
const ss = document.getElementById('sector-stats');
DATA.req_state.labels.slice(0, 2).forEach((lbl, i) => {
  const div = document.createElement('div');
  div.className = 'ss';
  div.innerHTML = '<strong>' + DATA.req_state.counts[i].toLocaleString() + '</strong>'
    + '<span>' + lbl + '</span>';
  ss.appendChild(div);
});

// Dual-ring doughnut (outer = Issue states, inner = Req states)
const C1 = ['#26C6DA','#6B21D9','#CE93D8','#9B59D4','#00BCD4','#9E9E9E'];
const C2 = ['#FDD835','#FF7043','#42A5F5','#AB47BC','#66BB6A','#EC407A'];
new Chart(document.getElementById('donutChart'), {
  type: 'doughnut',
  data: {
    labels: DATA.state.labels.slice(0, 6),
    datasets: [
      { label: 'Issue State', data: DATA.state.counts.slice(0, 6),
        backgroundColor: C1, borderWidth: 2, borderColor: '#fff' },
      { label: 'Req State',   data: DATA.req_state.counts.slice(0, 6),
        backgroundColor: C2, borderWidth: 2, borderColor: '#fff' }
    ]
  },
  options: {
    responsive: true, maintainAspectRatio: true, cutout: '45%',
    plugins: {
      legend: { position: 'bottom',
        labels: { font: { size: 8 }, boxWidth: 9, padding: 5, color: '#555' } },
      tooltip: {
        callbacks: {
          label: ctx => (ctx.datasetIndex === 0 ? 'Issue ' : 'Req ')
            + ctx.label + ': ' + ctx.raw.toLocaleString()
        }
      }
    }
  }
});

// Bar chart: region total = issue_open + req_open
const regionTotal = DATA.region.issue_open.map((v, i) => v + DATA.region.req_open[i]);
new Chart(document.getElementById('barChart'), {
  type: 'bar',
  data: {
    labels: DATA.region.labels,
    datasets: [{ data: regionTotal, backgroundColor: '#6B21D9',
                 borderRadius: 3, borderSkipped: false }]
  },
  options: {
    responsive: true, maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: { callbacks: { label: c => 'Total: ' + c.raw.toLocaleString() } }
    },
    scales: {
      y: { grid: { color: '#F0EFF6' }, ticks: { font: { size: 9 } } },
      x: { grid: { display: false }, ticks: { font: { size: 9 } } }
    }
  },
  plugins: [{
    id: 'vl',
    afterDatasetsDraw(chart) {
      const { ctx, data } = chart;
      chart.getDatasetMeta(0).data.forEach((bar, i) => {
        ctx.save();
        ctx.fillStyle = '#333'; ctx.font = 'bold 9px sans-serif'; ctx.textAlign = 'center';
        ctx.fillText(data.datasets[0].data[i].toLocaleString(), bar.x, bar.y - 4);
        ctx.restore();
      });
    }
  }]
});

// Line chart: 4 lines + hover-driven stat boxes
function updateLineStats(idx) {
  document.getElementById('stat-year').textContent = DATA.trend.years[idx];
  document.getElementById('stat-ic').textContent = DATA.trend.issue_created[idx].toLocaleString();
  document.getElementById('stat-il').textContent = DATA.trend.issue_closed[idx].toLocaleString();
  document.getElementById('stat-rc').textContent = DATA.trend.req_created[idx].toLocaleString();
  document.getElementById('stat-rl').textContent = DATA.trend.req_closed[idx].toLocaleString();
}
updateLineStats(DATA.trend.years.length - 1);

new Chart(document.getElementById('lineChart'), {
  type: 'line',
  data: {
    labels: DATA.trend.years,
    datasets: [
      { label: 'Issue Created', data: DATA.trend.issue_created,
        borderColor: '#6B21D9', borderWidth: 2, pointRadius: 3, tension: .3,
        fill: false, pointBackgroundColor: '#6B21D9' },
      { label: 'Issue Closed',  data: DATA.trend.issue_closed,
        borderColor: '#1E0A4C', borderWidth: 2, pointRadius: 3, tension: .3,
        fill: false, pointBackgroundColor: '#1E0A4C' },
      { label: 'Req Created',   data: DATA.trend.req_created,
        borderColor: '#00BCD4', borderWidth: 2, pointRadius: 3, tension: .3,
        fill: false, borderDash: [6, 4], pointBackgroundColor: '#00BCD4' },
      { label: 'Req Closed',    data: DATA.trend.req_closed,
        borderColor: '#E91E8C', borderWidth: 2, pointRadius: 3, tension: .3,
        fill: false, borderDash: [6, 4], pointBackgroundColor: '#E91E8C' }
    ]
  },
  options: {
    responsive: true, maintainAspectRatio: false,
    interaction: { mode: 'index', intersect: false },
    onHover: (evt, elements) => {
      if (elements.length > 0) updateLineStats(elements[0].index);
    },
    plugins: {
      legend: { position: 'bottom',
        labels: { font: { size: 9 }, boxWidth: 22, padding: 8, color: '#555' } },
      tooltip: { mode: 'index', intersect: false }
    },
    scales: {
      y: { grid: { color: '#F0EFF6' }, ticks: { font: { size: 8 } } },
      x: { grid: { display: false }, ticks: { font: { size: 9 }, maxRotation: 0 } }
    }
  }
});
</script>
</body>
</html>"""

html = TEMPLATE.replace('__DATA__', DATA_JSON)
with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Dashboard generated: {OUT_PATH}")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IABGVOC Multi-Page Dashboard Generator.

Generates output/pm.html + sc/dgc/imsbu/mok.html from JIRA CSVs.
Also archives a weekly snapshot under weekly_report/YYYY-Wxx/.
"""

import base64
import csv
import json
import os
import re
from bisect import bisect_right
from datetime import date, timedelta
from collections import defaultdict

import openpyxl
from export_week import write_reports

# ── Config ────────────────────────────────────────────────────────────────────
_ROOT      = os.path.dirname(os.path.abspath(__file__))
ISSUE_PATH = os.path.join(_ROOT, "data", "IABGVOC Issue.csv")
REQ_PATH   = os.path.join(_ROOT, "data", "IABGVOC Requirement.csv")
XLSX_PATH  = os.path.join(_ROOT, "data",
             "OneSW-Form-0023-TC_DIADesigner Function Check List (1).xlsx")
DEFS_PATH  = os.path.join(_ROOT, "iabgvoc-definitions.json")
LOGO_PATH  = os.path.join(_ROOT, "logo.png")
OUT_DIR    = os.path.join(_ROOT, "output")
TODAY      = date.today()

with open(DEFS_PATH, encoding="utf-8") as _f:
    DEFS = json.load(_f)

CLOSED_STATES  = frozenset(DEFS["closed_states"])
_thr           = DEFS["thresholds"]
FMEA_HIGH      = _thr["fmea_high"]
FMEA_MID_LOWER = _thr["fmea_mid_lower"]
FMEA_MID_UPPER = _thr["fmea_mid_upper"]
PAGES          = DEFS.get("pages", [])
SUMMARY        = DEFS.get("summary", {})
DISCUSSIONS    = DEFS.get("discussions", {})

# ── Logo ─────────────────────────────────────────────────────────────────────
_logo_b64 = ""
if os.path.exists(LOGO_PATH):
    with open(LOGO_PATH, "rb") as _f:
        _logo_b64 = base64.b64encode(_f.read()).decode()

# ── Helpers ───────────────────────────────────────────────────────────────────
def _load_csv(path):
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def _parse_date(s):
    if not s:
        return None
    m = re.match(r"(\d{4})/(\d{1,2})/(\d{1,2})", s.strip())
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None
    return None


def _is_open(row):
    return row.get("State", "").strip() not in CLOSED_STATES


def _fmea(row):
    try:
        return int(row.get("FMEA Total", "0") or 0)
    except ValueError:
        return 0


def _ph(val):
    v = (val or "").strip()
    return "" if v in ("（請填入）", "（請填入…）") else v


# ── Load raw data ─────────────────────────────────────────────────────────────
issues_all = _load_csv(ISSUE_PATH)
reqs_all   = _load_csv(REQ_PATH)
print(f"Loaded: {len(issues_all)} issues, {len(reqs_all)} requirements")

def _load_valid_tags():
    wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)
    ws = wb["DIADesigner Function List"]
    valid = set()
    for row in ws.iter_rows(min_row=2, values_only=True):
        val = row[3] if len(row) > 3 else None
        if val and isinstance(val, str) and val.strip():
            t = val.strip().lower()
            if t not in ("n/a", "download/upload mgr") and not t.startswith("\x5c"):
                valid.add(t)
    return valid
VALID_TAGS = _load_valid_tags()

# ── Weekly trend helpers ───────────────────────────────────────────────────────
_TREND_START = date(2025, 1, 6)
_trend_weeks = []
_w = _TREND_START
while _w <= TODAY:
    _trend_weeks.append(_w)
    _w += timedelta(weeks=1)
TREND_LABELS = [f"{w.year}/{w.month}/{w.day}" for w in _trend_weeks]


def _compute_weekly_trend(issues, reqs):
    creation = sorted(filter(None, (
        _parse_date(r.get("Creation Date", "")) for r in issues + reqs
    )))
    closure = sorted(filter(None, (
        _parse_date(r.get("Resolution date", ""))
        for r in issues + reqs
        if r.get("State", "").strip() in CLOSED_STATES
    )))
    total_list  = [bisect_right(creation, w + timedelta(days=6)) for w in _trend_weeks]
    closed_list = [bisect_right(closure,  w + timedelta(days=6)) for w in _trend_weeks]
    return total_list, closed_list



# ── Per-page data builder ─────────────────────────────────────────────────────
def _compute_page_data(issues, reqs):
    open_issues = [r for r in issues if _is_open(r)]
    open_reqs   = [r for r in reqs   if _is_open(r)]

    # State distribution (open only, sorted by count desc)
    issue_state_cnt = defaultdict(int)
    for row in open_issues:
        issue_state_cnt[row.get("State", "").strip()] += 1
    issue_state_sorted = sorted(issue_state_cnt.items(), key=lambda x: -x[1])

    req_state_cnt = defaultdict(int)
    for row in open_reqs:
        req_state_cnt[row.get("State", "").strip()] += 1
    req_state_sorted = sorted(req_state_cnt.items(), key=lambda x: -x[1])

    # FMEA tier distribution
    def _fmea_tiers(rows):
        return [
            sum(1 for r in rows if _fmea(r) >= FMEA_HIGH),
            sum(1 for r in rows if FMEA_MID_LOWER <= _fmea(r) <= FMEA_MID_UPPER),
            sum(1 for r in rows if _fmea(r) < FMEA_MID_LOWER),
        ]

    trend_total, trend_closed = _compute_weekly_trend(issues, reqs)

    return {
        "meta": {
            "generated_at": str(TODAY),
            "total_issues": len(issues),
            "total_reqs":   len(reqs),
        },
        "state_dist": {
            "issue": {
                "labels": [s[0] for s in issue_state_sorted],
                "counts": [s[1] for s in issue_state_sorted],
            },
            "req": {
                "labels": [s[0] for s in req_state_sorted],
                "counts": [s[1] for s in req_state_sorted],
            },
        },
        "fmea_dist": {
            "issue":      _fmea_tiers(open_issues),
            "req":        _fmea_tiers(open_reqs),
            "thresholds": {
                "high":      FMEA_HIGH,
                "mid_lower": FMEA_MID_LOWER,
                "mid_upper": FMEA_MID_UPPER,
            },
        },
        "trend": {
            "labels": TREND_LABELS,
            "total":  trend_total,
            "closed": trend_closed,
        },
    }


# ── Role dropdown builder ─────────────────────────────────────────────────────
def _build_role_dropdown(current_role):
    links = ""
    for p in PAGES:
        cls = ' class="active"' if p["role"] == current_role else ""
        links += f'      <a href="{p["role"]}.html"{cls}>{p["label"]}</a>\n'
    lbl = next((p["label"] for p in PAGES if p["role"] == current_role), current_role.upper())
    return (
        f'<div class="role-dropdown">\n'
        f'    <button class="role-btn" id="role-btn">{lbl} &#9662;</button>\n'
        f'    <div class="role-menu" id="role-menu">\n'
        f"{links}"
        f"    </div>\n"
        f"  </div>"
    )


# ── Shared CSS ────────────────────────────────────────────────────────────────
_SHARED_CSS = """
:root{--purple:#6B21D9;--magenta:#E91E8C;--body-bg:#F0EFF6;--border:#E2E0EC;--text:#1E0A4C;--muted:#7B7A8E;}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Segoe UI',Arial,sans-serif;background:var(--body-bg);color:var(--text);min-height:100vh;}
.header{background:#1e293b;border-bottom:1px solid #334155;padding:16px 32px;display:flex;align-items:center;gap:16px;}
.header img{height:40px;}
.header-text h1{font-size:1.25rem;font-weight:700;color:#f1f5f9;}
.header-text p{font-size:0.8rem;color:#94a3b8;margin-top:2px;}
.main{padding:10px 16px;display:grid;gap:8px;}
.card{background:#fff;border-radius:8px;border:1px solid var(--border);transition:box-shadow .2s;}
.card:hover{box-shadow:0 3px 14px rgba(107,33,217,.12);}
.panel-title{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.4px;color:var(--text);margin-bottom:8px;display:flex;align-items:center;}
.summary-row{display:grid;grid-template-columns:1fr 1fr;gap:8px;}
.summary-card{padding:12px 16px;}
.summary-title{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--muted);margin-bottom:10px;border-bottom:1px solid var(--border);padding-bottom:6px;}
.summary-item{display:flex;align-items:flex-start;gap:8px;margin-bottom:8px;}
.summary-icon{flex-shrink:0;font-size:13px;line-height:1.5;}
.summary-label{font-size:10px;font-weight:700;color:var(--text);width:52px;flex-shrink:0;line-height:1.5;}
.summary-text{font-size:11px;color:var(--text);flex:1;min-height:20px;line-height:1.5;outline:none;border-bottom:1px dashed #c8c5dc;padding-bottom:1px;}
.summary-text:empty::before{content:attr(data-ph);color:#b0adc7;pointer-events:none;}
.summary-text:focus{border-bottom-color:var(--purple);}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:8px;}
.state-panel{padding:10px 12px;display:flex;flex-direction:column;}
.state-inner{display:flex;flex-direction:column;gap:10px;flex:1;align-items:center;min-height:0;width:100%;}
.state-donut-wrap{flex-shrink:0;width:min(100%,260px);aspect-ratio:1;}
.state-list{width:100%;flex-shrink:0;display:flex;flex-direction:column;border-top:1px solid var(--border);}
.state-item{display:flex;align-items:center;gap:8px;font-size:11px;padding:5px 2px;border-bottom:1px solid var(--border);}
.si-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
.si-lbl{flex:1;color:var(--text);}
.si-val{font-weight:700;color:var(--text);flex-shrink:0;min-width:28px;text-align:right;}
.si-pct{color:var(--muted);flex-shrink:0;min-width:42px;text-align:right;}
.chart-panel{padding:10px 12px;display:flex;flex-direction:column;}
.role-dropdown{margin-left:auto;position:relative;}
.role-btn{background:transparent;border:1px solid #475569;color:#f1f5f9;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:0.85rem;font-weight:600;display:flex;align-items:center;gap:6px;white-space:nowrap;}
.role-btn:hover{background:#334155;}
.role-menu{display:none;position:absolute;right:0;top:calc(100% + 6px);background:#1e293b;border:1px solid #475569;border-radius:8px;min-width:120px;z-index:100;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,.5);}
.role-menu.open{display:block;}
.role-menu a{display:block;padding:10px 20px;color:#f1f5f9;text-decoration:none;font-size:0.875rem;font-weight:500;}
.role-menu a:hover{background:#334155;}
.role-menu a.active{background:#312e81;color:#a5b4fc;font-weight:700;pointer-events:none;}
.week-dropdown{margin-left:8px;position:relative;}
.week-btn{background:transparent;border:1px solid #475569;color:#f1f5f9;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:0.85rem;font-weight:600;display:flex;align-items:center;gap:6px;white-space:nowrap;}
.week-btn:hover{background:#334155;}
.week-menu{display:none;position:absolute;right:0;top:calc(100% + 6px);background:#1e293b;border:1px solid #475569;border-radius:8px;min-width:160px;z-index:100;box-shadow:0 4px 20px rgba(0,0,0,.5);max-height:400px;overflow-y:auto;}
.week-menu.open{display:block;}
.week-section{border-bottom:1px solid #334155;}
.week-section:last-child{border-bottom:none;}
.week-month-header{display:block;padding:6px 16px 2px;font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:#94a3b8;}
.week-menu a{display:block;padding:7px 20px 7px 28px;color:#f1f5f9;text-decoration:none;font-size:0.875rem;font-weight:500;}
.week-menu a:hover{background:#334155;}
.week-menu a.active{background:#312e81;color:#a5b4fc;font-weight:700;pointer-events:none;}

"""


# ── HTML generator ─────────────────────────────────────────────────────────────
def _generate_html(role, label, data):
    role_dropdown    = _build_role_dropdown(role)
    data_json        = json.dumps(data, ensure_ascii=False)
    logo_tag         = f"<img src='data:image/png;base64,{_logo_b64}' alt='logo'>" if _logo_b64 else ""
    plan_val         = _ph(SUMMARY.get("plan", ""))
    progress_val     = _ph(SUMMARY.get("progress", ""))
    problem_val      = _ph(SUMMARY.get("problem", ""))
    decision_val     = _ph(DISCUSSIONS.get("decision", ""))
    indiscussion_val = _ph(DISCUSSIONS.get("in_discussion", ""))
    conflict_val     = _ph(DISCUSSIONS.get("conflict", ""))

    # Trend section — PM only shows all-role lines
    if role == "pm":
        trend_html = """
  <!-- All-Role Weekly Trend (PM only) -->
  <div class="card chart-panel" style="border-top:3px solid var(--purple);">
    <div class="panel-title">
      Issue &amp; Requirement 累積趨勢（各 Region）
      <span style="font-size:10px;font-weight:400;color:var(--muted);text-transform:none;letter-spacing:0;margin-left:6px;">週為單位・2025/1/6 起</span>
    </div>
    <div style="position:relative;height:400px;"><canvas id="chart-trend"></canvas></div>
  </div>
"""
        trend_js = """
/* ── All-role trend chart (PM only) */
(function() {
  var ctx = document.getElementById('chart-trend').getContext('2d');
  var ROLE_COLORS = {pm:'#1E0A4C',sc:'#2563EB',dgc:'#DC2626',imsbu:'#16A34A',mok:'#D97706'};
  var ROLE_LABELS = {pm:'PM (All)',sc:'SC',dgc:'DGC',imsbu:'IMSBU',mok:'MOK'};
  var roleOrder = ['sc','dgc','imsbu','mok','pm'];
  var datasets = [];
  roleOrder.forEach(function(r) {
    var t = DATA.all_trends[r];
    if (!t) return;
    datasets.push({
      label: ROLE_LABELS[r] || t.label,
      data: t.total,
      borderColor: ROLE_COLORS[r],
      backgroundColor: 'transparent',
      borderWidth: r === 'pm' ? 2.5 : 1.8,
      pointRadius: 0,
      pointHoverRadius: 4,
      fill: false,
      tension: 0.4,
      borderDash: r === 'pm' ? [5, 3] : []
    });
  });
  new Chart(ctx, {
    type: 'line',
    data: { labels: DATA.trend.labels, datasets: datasets },
    options: {
      responsive: true, maintainAspectRatio: false,
      animation: {duration:900,easing:'easeInOutQuart'},
      interaction: {mode:'index',intersect:false},
      plugins: {
        legend: {display:true,position:'top',align:'end',labels:{usePointStyle:true,pointStyle:'line',boxWidth:24,boxHeight:2,padding:16,font:{size:11,weight:'600'},color:'#1E0A4C'}},
        tooltip: {backgroundColor:'#1e293b',titleColor:'#94a3b8',bodyColor:'#f1f5f9',borderColor:'#334155',borderWidth:1,padding:10,cornerRadius:8,
          callbacks: {
            title: function(c) { return 'Week of ' + c[0].label; },
            label: function(c) { return '  ' + c.dataset.label + ':  ' + c.parsed.y; }
          }
        }
      },
      scales: {
        x: {ticks:{maxTicksLimit:18,maxRotation:45,font:{size:10},color:'#7B7A8E'},grid:{color:'#EDE9F6'},border:{display:false}},
        y: {min:0,ticks:{font:{size:10},color:'#7B7A8E',padding:8},grid:{color:'#EDE9F6'},border:{display:false}}
      }
    }
  });
})();
"""
    else:
        trend_html = ""
        trend_js   = ""

    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>IABGVOC Dashboard — {label}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
{_SHARED_CSS}
</style>
</head>
<body>

<div class="header">
  {logo_tag}
  <div class="header-text">
    <h1>IABGVOC Issue &amp; Requirement Dashboard</h1>
    <p>Generated: {TODAY}</p>
  </div>
  {role_dropdown}
  __WEEK_NAV__
</div>

<div class="main">

  <!-- Executive Summary -->
  <div class="summary-row">
    <div class="card summary-card">
      <div class="summary-title">執行摘要</div>
      <div class="summary-item">
        <span class="summary-icon">\U0001f7e2</span>
        <span class="summary-label">Plan</span>
        <div class="summary-text" contenteditable="true" data-ph="請填入…">{plan_val}</div>
      </div>
      <div class="summary-item">
        <span class="summary-icon">\U0001f7e1</span>
        <span class="summary-label">Progress</span>
        <div class="summary-text" contenteditable="true" data-ph="請填入…">{progress_val}</div>
      </div>
      <div class="summary-item">
        <span class="summary-icon">\U0001f534</span>
        <span class="summary-label">Problem</span>
        <div class="summary-text" contenteditable="true" data-ph="請填入…">{problem_val}</div>
      </div>
    </div>
    <div class="card summary-card">
      <div class="summary-title">重要討論</div>
      <div class="summary-item">
        <span class="summary-icon">\U0001f7e2</span>
        <span class="summary-label">決策</span>
        <div class="summary-text" contenteditable="true" data-ph="請填入…">{decision_val}</div>
      </div>
      <div class="summary-item">
        <span class="summary-icon">\U0001f7e1</span>
        <span class="summary-label">討論中</span>
        <div class="summary-text" contenteditable="true" data-ph="請填入…">{indiscussion_val}</div>
      </div>
      <div class="summary-item">
        <span class="summary-icon">\U0001f534</span>
        <span class="summary-label">爭議項目</span>
        <div class="summary-text" contenteditable="true" data-ph="請填入…">{conflict_val}</div>
      </div>
    </div>
  </div>

  <!-- Open by State -->
  <div class="two-col">
    <div class="card state-panel">
      <div class="panel-title">Open Issues by State</div>
      <div class="state-inner">
        <div class="state-donut-wrap" id="wrap-issue-state"></div>
        <div class="state-list" id="issue-state-list"></div>
      </div>
    </div>
    <div class="card state-panel">
      <div class="panel-title">Open Reqs by State</div>
      <div class="state-inner">
        <div class="state-donut-wrap" id="wrap-req-state"></div>
        <div class="state-list" id="req-state-list"></div>
      </div>
    </div>
  </div>

  <!-- FMEA Distribution -->
  <div class="two-col">
    <div class="card state-panel">
      <div class="panel-title">Open Issues — FMEA Distribution</div>
      <div class="state-inner">
        <div class="state-donut-wrap" id="wrap-issue-fmea"></div>
        <div class="state-list" id="issue-fmea-list"></div>
      </div>
    </div>
    <div class="card state-panel">
      <div class="panel-title">Open Reqs — FMEA Distribution</div>
      <div class="state-inner">
        <div class="state-donut-wrap" id="wrap-req-fmea"></div>
        <div class="state-list" id="req-fmea-list"></div>
      </div>
    </div>
  </div>


{trend_html}
</div>

<script>
const DATA = {data_json};

/* ── SVG Donut ────────────────────────────────────────────────────────────────────── */
function makeSVGDonut(wrapEl, labels, data, colors, centerVal) {{
  if (!wrapEl) return;
  const total = data.reduce((a, b) => a + b, 0);
  if (total === 0) return;
  const ns = 'http://www.w3.org/2000/svg';
  const cx = 100, cy = 100, R = 86, r = 52;
  const uid = 'f' + Math.random().toString(36).slice(2, 8);
  const svg = document.createElementNS(ns, 'svg');
  svg.setAttribute('viewBox', '0 0 200 200');
  svg.style.cssText = 'width:100%;height:100%;overflow:visible;display:block';
  const defs = document.createElementNS(ns, 'defs');
  defs.innerHTML = '<filter id="' + uid + '" x="-15%" y="-15%" width="130%" height="130%">'
    + '<feDropShadow dx="0" dy="2" stdDeviation="3.5" flood-color="#1E0A4C" flood-opacity="0.13"/>'
    + '</filter>';
  svg.appendChild(defs);
  const g = document.createElementNS(ns, 'g');
  g.setAttribute('filter', 'url(#' + uid + ')');
  let startA = -Math.PI / 2;
  data.forEach(function(val, i) {{
    if (val === 0) return;
    const sweep = (val / total) * 2 * Math.PI;
    const endA  = startA + sweep;
    const large = sweep > Math.PI ? 1 : 0;
    const cos1 = Math.cos(startA), sin1 = Math.sin(startA);
    const cos2 = Math.cos(endA),   sin2 = Math.sin(endA);
    const path = document.createElementNS(ns, 'path');
    path.setAttribute('d', [
      'M '+(cx+R*cos1)+' '+(cy+R*sin1),
      'A '+R+' '+R+' 0 '+large+' 1 '+(cx+R*cos2)+' '+(cy+R*sin2),
      'L '+(cx+r*cos2)+' '+(cy+r*sin2),
      'A '+r+' '+r+' 0 '+large+' 0 '+(cx+r*cos1)+' '+(cy+r*sin1),
      'Z'
    ].join(' '));
    path.setAttribute('fill', colors[i % colors.length]);
    path.setAttribute('stroke', '#fff');
    path.setAttribute('stroke-width', '2.5');
    path.style.cssText = 'transition:filter 0.18s;cursor:pointer';
    path.addEventListener('mouseenter', function() {{ this.style.filter = 'brightness(1.18)'; }});
    path.addEventListener('mouseleave', function() {{ this.style.filter = ''; }});
    const title = document.createElementNS(ns, 'title');
    title.textContent = labels[i] + ': ' + val;
    path.appendChild(title);
    g.appendChild(path);
    if (sweep > 0.25) {{
      const midA = startA + sweep / 2;
      const mr   = (R + r) / 2;
      const t    = document.createElementNS(ns, 'text');
      t.setAttribute('x', cx + mr * Math.cos(midA));
      t.setAttribute('y', cy + mr * Math.sin(midA));
      t.setAttribute('text-anchor', 'middle');
      t.setAttribute('dominant-baseline', 'central');
      t.setAttribute('font-size', '12');
      t.setAttribute('font-weight', '700');
      t.setAttribute('fill', '#fff');
      t.setAttribute('pointer-events', 'none');
      t.textContent = val;
      g.appendChild(t);
    }}
    startA = endA;
  }});
  svg.appendChild(g);
  const ct = document.createElementNS(ns, 'text');
  ct.setAttribute('x', '100'); ct.setAttribute('y', '100');
  ct.setAttribute('text-anchor', 'middle');
  ct.setAttribute('dominant-baseline', 'central');
  ct.setAttribute('font-size', '22');
  ct.setAttribute('font-weight', '700');
  ct.setAttribute('fill', '#1E0A4C');
  ct.setAttribute('pointer-events', 'none');
  ct.textContent = centerVal;
  svg.appendChild(ct);
  wrapEl.innerHTML = '';
  wrapEl.appendChild(svg);
}}

/* ── Build list ────────────────────────────────────────────────────────────────────────────── */
function buildList(containerId, labels, counts, colorFn) {{
  const el    = document.getElementById(containerId);
  if (!el) return;
  const total = counts.reduce((a, b) => a + b, 0);
  labels.forEach(function(lbl, i) {{
    const pct = total > 0 ? Math.round(counts[i] / total * 100) : 0;
    const div = document.createElement('div');
    div.className = 'state-item';
    div.innerHTML = '<span class="si-dot" style="background:' + colorFn(lbl) + '"></span>'
      + '<span class="si-lbl">' + lbl + '</span>'
      + '<span class="si-val">' + counts[i].toLocaleString() + '</span>'
      + '<span class="si-pct">(' + pct + '%)</span>';
    el.appendChild(div);
  }});
}}

/* ── Open by State donuts ──────────────────────────────────────────────────────────────── */
var STATE_COLORS = {{'Review':'#C62828','In Progress':'#1976D2','Verification':'#F9A825','Review & Approval':'#81C784'}};
function stateColor(l) {{ return STATE_COLORS[l] || '#9E9E9E'; }}

var issueStateTotal = DATA.state_dist.issue.counts.reduce(function(a,b){{return a+b;}}, 0);
buildList('issue-state-list', DATA.state_dist.issue.labels, DATA.state_dist.issue.counts, stateColor);
makeSVGDonut(document.getElementById('wrap-issue-state'), DATA.state_dist.issue.labels, DATA.state_dist.issue.counts, DATA.state_dist.issue.labels.map(stateColor), issueStateTotal);

var reqStateTotal = DATA.state_dist.req.counts.reduce(function(a,b){{return a+b;}}, 0);
buildList('req-state-list', DATA.state_dist.req.labels, DATA.state_dist.req.counts, stateColor);
makeSVGDonut(document.getElementById('wrap-req-state'), DATA.state_dist.req.labels, DATA.state_dist.req.counts, DATA.state_dist.req.labels.map(stateColor), reqStateTotal);

/* ── FMEA distribution donuts ──────────────────────────────────────────────────────────── */
var thr = DATA.fmea_dist.thresholds;
var FMEA_LABELS = [
  'High (≥' + thr.high + ')',
  'Mid (' + thr.mid_lower + '–' + thr.mid_upper + ')',
  'Low (<' + thr.mid_lower + ')'
];
var FMEA_COLORS = ['#E53935', '#F59E0B', '#43A047'];
function fmeaColor(l) {{ return FMEA_COLORS[FMEA_LABELS.indexOf(l)] || '#9E9E9E'; }}

var issueFmeaTotal = DATA.fmea_dist.issue.reduce(function(a,b){{return a+b;}}, 0);
buildList('issue-fmea-list', FMEA_LABELS, DATA.fmea_dist.issue, fmeaColor);
makeSVGDonut(document.getElementById('wrap-issue-fmea'), FMEA_LABELS, DATA.fmea_dist.issue, FMEA_COLORS, issueFmeaTotal);

var reqFmeaTotal = DATA.fmea_dist.req.reduce(function(a,b){{return a+b;}}, 0);
buildList('req-fmea-list', FMEA_LABELS, DATA.fmea_dist.req, fmeaColor);
makeSVGDonut(document.getElementById('wrap-req-fmea'), FMEA_LABELS, DATA.fmea_dist.req, FMEA_COLORS, reqFmeaTotal);


{trend_js}

/* ── Dropdown toggles ─────────────────────────────────────────────────────────────────────── */
['role','week'].forEach(function(id) {{
  var btn  = document.getElementById(id + '-btn');
  var menu = document.getElementById(id + '-menu');
  if (btn && menu) {{
    btn.addEventListener('click', function(e) {{ e.stopPropagation(); menu.classList.toggle('open'); }});
    document.addEventListener('click', function() {{ menu.classList.remove('open'); }});
  }}
}});
</script>
</body>
</html>"""


# ── Main ──────────────────────────────────────────────────────────────────────
os.makedirs(OUT_DIR, exist_ok=True)

page_data_map = {}
for page in PAGES:
    role   = page["role"]
    region = page.get("region_filter")
    if region:
        iss = [r for r in issues_all if r.get("Region", "").strip() == region]
        rqs = [r for r in reqs_all   if r.get("Region", "").strip() == region]
    else:
        iss = issues_all
        rqs = reqs_all
    page_data_map[role] = _compute_page_data(iss, rqs)
    print(f"  Built page: {role} ({len(iss)} issues, {len(rqs)} reqs)")

# PM page gets all-role trend lines
page_data_map["pm"]["all_trends"] = {
    page["role"]: {
        "label":  page["label"],
        "total":  page_data_map[page["role"]]["trend"]["total"],
        "closed": page_data_map[page["role"]]["trend"]["closed"],
    }
    for page in PAGES
}

page_htmls = {}
for page in PAGES:
    page_htmls[page["role"]] = _generate_html(page["role"], page["label"], page_data_map[page["role"]])

write_reports(page_htmls, OUT_DIR, _ROOT)
print("Done.")

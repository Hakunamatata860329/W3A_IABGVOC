#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Weekly report export helpers for IABGVOC dashboard.
Called by export_dashboard.py to write HTML files to weekly_report/ and output/.
"""

import json
import os
from bisect import insort
from collections import defaultdict
from datetime import date


def get_run_week_info(d=None):
    if d is None:
        d = date.today()
    iso_year, iso_week, _ = d.isocalendar()
    week_of_month = (d.day - 1) // 7 + 1
    return {
        "dir_name":      f"{iso_year}-W{iso_week:02d}",
        "year":          iso_year,
        "month_num":     d.month,
        "month":         d.strftime("%b"),
        "week_of_month": week_of_month,
        "date":          str(d),
    }


def scan_existing_weeks(base_dir):
    result = []
    if not os.path.isdir(base_dir):
        return result
    for name in sorted(os.listdir(base_dir)):
        meta_path = os.path.join(base_dir, name, "meta.json")
        if os.path.isfile(meta_path):
            with open(meta_path, encoding="utf-8") as f:
                result.append(json.load(f))
    return result


def build_week_nav_html(all_weeks, current_info, role, path_prefix):
    """Build the two-level month→week dropdown HTML.

    First level: year/month header (e.g. 2026/May).
    Second level: individual weeks within the month.
    """
    by_ym = defaultdict(list)
    for w in all_weeks:
        key = (w.get("year", 0), w.get("month_num", 0))
        by_ym[key].append(w)

    btn_label = f"{current_info['month']} Week {current_info['week_of_month']}"
    sections = ""

    for (year, month_num) in sorted(by_ym.keys()):
        items = sorted(by_ym[(year, month_num)], key=lambda x: x["week_of_month"])
        month_str = items[0].get("month", "")
        items_html = ""
        for w in items:
            is_active = w["dir_name"] == current_info["dir_name"]
            label = f"Week {w['week_of_month']}"
            if is_active:
                items_html += f'\n      <a class="active">{label}</a>'
            else:
                href = f"{path_prefix}{w['dir_name']}/{role}.html"
                items_html += f'\n      <a href="{href}">{label}</a>'
        if items_html:
            display = f"{year}/{month_str}"
            sections += (
                f'\n    <div class="week-section">'
                f'<span class="week-month-header">{display}</span>'
                f"{items_html}\n    </div>"
            )

    return (
        f'<div class="week-dropdown">'
        f'\n    <button class="week-btn" id="week-btn">{btn_label} &#9662;</button>'
        f'\n    <div class="week-menu" id="week-menu">{sections}\n    </div>'
        f"\n  </div>"
    )


def write_reports(page_htmls, out_dir, root):
    """Write all page HTMLs to weekly_report/YYYY-Wxx/ and out_dir/.

    Args:
        page_htmls: dict of role -> HTML string (with __WEEK_NAV__ placeholder).
        out_dir:    Path to the output/ directory.
        root:       Project root (parent of weekly_report/).
    """
    week_info  = get_run_week_info()
    weekly_dir = os.path.join(root, "weekly_report")
    week_dir   = os.path.join(weekly_dir, week_info["dir_name"])
    os.makedirs(week_dir, exist_ok=True)

    with open(os.path.join(week_dir, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(week_info, f, ensure_ascii=False, indent=2)

    all_weeks = scan_existing_weeks(weekly_dir)
    os.makedirs(out_dir, exist_ok=True)

    for role, base_html in page_htmls.items():
        nav_weekly = build_week_nav_html(all_weeks, week_info, role, "../")
        with open(os.path.join(week_dir, f"{role}.html"), "w", encoding="utf-8") as f:
            f.write(base_html.replace("__WEEK_NAV__", nav_weekly))

        nav_output = build_week_nav_html(all_weeks, week_info, role, "../weekly_report/")
        with open(os.path.join(out_dir, f"{role}.html"), "w", encoding="utf-8") as f:
            f.write(base_html.replace("__WEEK_NAV__", nav_output))

    roles_str = ", ".join(f"{r}.html" for r in page_htmls)
    print(f"Generated: weekly_report/{week_info['dir_name']}/ + output/ ({roles_str})")

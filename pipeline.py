#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IABGVOC Pipeline 管理器

用法：
  python pipeline.py              # 預設：執行 dashboard
  python pipeline.py --step dashboard
"""

import argparse
import os
import subprocess
import sys
import time

_ROOT = os.path.dirname(os.path.abspath(__file__))

STEPS = {
    "dashboard": ("export_dashboard.py", "Dashboard → output/pm.html, sc/dgc/imsbu/mok.html"),
}

DEFAULT_STEPS = ["dashboard"]


def run_step(name):
    script, description = STEPS[name]
    print(f"\n{'─' * 52}")
    print(f"  [{name}]  {description}")
    print(f"{'─' * 52}")
    t0 = time.time()
    result = subprocess.run([sys.executable, os.path.join(_ROOT, script)], cwd=_ROOT)
    elapsed = time.time() - t0
    if result.returncode != 0:
        print(f"\n✗  [{name}] 失敗（exit {result.returncode}）")
        return False
    print(f"\n✓  [{name}] 完成（{elapsed:.1f}s）")
    return True


def main():
    step_help = "\n".join(f"  {k:<14} {v[1]}" for k, v in STEPS.items())
    parser = argparse.ArgumentParser(
        description="IABGVOC pipeline 管理器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"\n可用步驟：\n{step_help}\n\n預設步驟：{' → '.join(DEFAULT_STEPS)}\n",
    )
    parser.add_argument(
        "--step", metavar="STEP", nargs="+",
        help="指定執行的步驟，可多個（空格分隔）",
    )
    args = parser.parse_args()

    if args.step:
        invalid = [s for s in args.step if s not in STEPS]
        if invalid:
            parser.error(f"未知步驟：{', '.join(invalid)}\n可用：{', '.join(STEPS)}")
        steps = args.step
    else:
        steps = DEFAULT_STEPS

    print(f"\n執行步驟：{' → '.join(steps)}")
    t_start = time.time()

    for step in steps:
        if not run_step(step):
            print(f"\n  Pipeline 中止於步驟 [{step}]\n")
            sys.exit(1)

    total = time.time() - t_start
    print(f"\n{'═' * 52}")
    print(f"  全部完成（{total:.1f}s）：{' → '.join(steps)}")
    print(f"{'═' * 52}\n")


if __name__ == "__main__":
    main()

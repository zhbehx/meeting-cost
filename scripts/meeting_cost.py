#!/usr/bin/env python3
"""算清一个会烧掉多少钱：单次成本 / 年成本 / 折算成直觉单位 / 最小化方案。

用法：
    python scripts/meeting_cost.py --people 11 --minutes 60 --repeat weekly --salary 22000
    python scripts/meeting_cost.py --people 8 --minutes 90 --repeat weekly --loaded 1.4 --json
    python scripts/meeting_cost.py --list-freq          # 查看频率折算表

退出码：0 正常；参数错误 2。
"""

from __future__ import annotations

import argparse
import json
import sys

WORK_DAYS_PER_MONTH = 21.75
HOURS_PER_DAY = 8
MONTHS_PER_YEAR = 14  # 含年终，用于「够雇几个人」的换算

FREQ_TIMES = {
    "daily": 250, "weekly": 50, "biweekly": 25, "monthly": 12,
    "quarterly": 4, "once": 1,
}
FREQ_LABEL = {
    "daily": "每个工作日", "weekly": "每周", "biweekly": "每两周",
    "monthly": "每月", "quarterly": "每季度", "once": "一次性",
}

# 拿不到真实薪资时的默认值（元/月）
ROLE_SALARY = {
    "intern": 4000, "junior": 10000, "senior": 22000,
    "manager": 40000, "exec": 70000,
}


def hourly(salary: float) -> float:
    return salary / WORK_DAYS_PER_MONTH / HOURS_PER_DAY


def compute(people: int, minutes: float, repeat: str, salary: float,
            prepare: float, recover: float, loaded: float) -> dict:
    occupied_min = minutes + prepare + recover
    rate = hourly(salary) * loaded

    one_meeting = people * occupied_min / 60 * rate
    times = FREQ_TIMES[repeat]
    year_cost = one_meeting * times

    person_hours_one = people * occupied_min / 60
    person_hours_year = person_hours_one * times
    person_days_year = person_hours_year / HOURS_PER_DAY

    headcount = year_cost / (salary * MONTHS_PER_YEAR) if salary else 0
    laptops = year_cost / 12000
    coffees = year_cost / 30

    # 最小化：减人到 60%、时长压到 33%、频率减半（仅对高频会议）
    lean_people = max(2, round(people * 0.6))
    lean_minutes = max(15, round(minutes / 3))
    lean_repeat = repeat if repeat in ("once", "quarterly") else (
        "biweekly" if repeat in ("daily", "weekly") else repeat)
    lean_one = lean_people * (lean_minutes + prepare + recover) / 60 * rate
    lean_year = lean_one * FREQ_TIMES[lean_repeat]
    saving = year_cost - lean_year

    return {
        "people": people,
        "minutes": minutes,
        "repeat": repeat,
        "repeat_label": FREQ_LABEL[repeat],
        "times_per_year": times,
        "salary": salary,
        "hourly_rate": round(rate, 1),
        "loaded": loaded,
        "prepare_min": prepare,
        "recover_min": recover,
        "occupied_min_per_person": occupied_min,
        "cost_per_meeting": round(one_meeting),
        "cost_per_year": round(year_cost),
        "person_hours_per_year": round(person_hours_year, 1),
        "person_days_per_year": round(person_days_year, 1),
        "equivalent_headcount": round(headcount, 2),
        "equivalent_laptops": round(laptops),
        "equivalent_coffees": round(coffees),
        "lean": {
            "people": lean_people,
            "minutes": lean_minutes,
            "repeat": lean_repeat,
            "repeat_label": FREQ_LABEL[lean_repeat],
            "cost_per_year": round(lean_year),
            "saving": round(max(0, saving)),
            "saving_pct": round(max(0, saving) / year_cost * 100, 1) if year_cost else 0,
        },
    }


def money(v: float) -> str:
    if v >= 10000:
        return f"{v / 10000:.1f} 万"
    return f"{v:,.0f} 元"


def render(r: dict) -> str:
    out = []
    out.append(f"这个会的价格：{money(r['cost_per_meeting'])}（单次）"
               f"｜{money(r['cost_per_year'])}（每年）")
    out.append(f"  参会 {r['people']} 人 × 占用 {r['occupied_min_per_person']} 分钟"
               f"（会 {r['minutes']} 分 + 准备 {r['prepare_min']} + 恢复 {r['recover_min']}）"
               f" × 时薪 ¥{r['hourly_rate']}")
    out.append(f"  频率：{r['repeat_label']}，每年 {r['times_per_year']} 次")
    out.append("")
    out.append("换算成你能感知的东西：")
    out.append(f"  每年消耗 {r['person_hours_per_year']:.0f} 人时 = {r['person_days_per_year']:.0f} 个工作日")
    out.append(f"  ≈ {r['equivalent_headcount']} 个全职人力（按月薪 {money(r['salary'])} × 14 薪算）")
    out.append(f"  ≈ {r['equivalent_laptops']} 台 MacBook  /  {r['equivalent_coffees']} 杯咖啡")
    out.append("")
    lean = r["lean"]
    out.append("如果必须开，最小化方案：")
    out.append(f"  {r['people']} 人 {r['minutes']} 分钟 {r['repeat_label']}"
               f"  →  {lean['people']} 人 {lean['minutes']} 分钟 {lean['repeat_label']}")
    out.append(f"  年成本 {money(r['cost_per_year'])} → {money(lean['cost_per_year'])}"
               f"，省 {money(lean['saving'])}（{lean['saving_pct']}%）")
    out.append("")
    out.append("判断该不该开：会后能不能产出「决定了什么 + 谁做什么 + 何时」？")
    out.append("  能 → 该开，但按上面的最小化方案压。")
    out.append("  不能 → 改成文档/看板异步读，省下的钱比会议本身多。")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="计算会议成本")
    ap.add_argument("--people", type=int, default=8, help="参会人数（默认 8）")
    ap.add_argument("--minutes", type=float, default=60, help="会议时长，分钟（默认 60）")
    ap.add_argument("--repeat", choices=list(FREQ_TIMES), default="weekly", help="频率（默认 weekly）")
    ap.add_argument("--salary", type=float, default=22000, help="人均月薪（默认 22000）")
    ap.add_argument("--role", choices=list(ROLE_SALARY), default=None,
                    help="按岗位取默认月薪（会覆盖 --salary）")
    ap.add_argument("--prepare", type=float, default=15, help="会前准备分钟/人（默认 15）")
    ap.add_argument("--recover", type=float, default=10, help="会后恢复分钟/人（默认 10）")
    ap.add_argument("--loaded", type=float, default=1.0,
                    help="企业综合成本系数（1.0 只算工资，1.4 更接近真实）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--list-freq", action="store_true", help="列出频率折算表后退出")
    args = ap.parse_args(argv)

    if args.list_freq:
        for k, v in FREQ_TIMES.items():
            print(f"  {k:<10} {FREQ_LABEL[k]:<8} 每年 {v} 次")
        return 0

    if args.people < 1 or args.minutes <= 0 or args.salary <= 0:
        print("参数不合法：人数需 ≥1，时长与月薪需 >0。", file=sys.stderr)
        return 2

    salary = ROLE_SALARY[args.role] if args.role else args.salary
    r = compute(args.people, args.minutes, args.repeat, salary,
                args.prepare, args.recover, args.loaded)

    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(render(r))
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main(sys.argv[1:]))

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_TIMEOUT_SECONDS = 60.0

METHOD_ORDER = ["greedy", "local_search", "MIP", "CP", "DP"]

HYPERPARAMETERS = {
    "greedy": {
        "REPAIR_FILL_ROUNDS": 2,
        "GREEDY_ORDER": "(e_i - s_i, e_i, -d_i)",
        "BEST_DAY_RULE": "choose feasible day with largest current load",
        "REPAIR_MEMBER_ORDER": "d_i ascending",
        "FILL_ORDER": "(-d_i, e_i - s_i, e_i)",
        "NEW_DAY_FILL_RULE": "stop opening a new day when total >= min_load",
    },
    "local_search": {
        "INITIAL_REPAIR_FILL_ROUNDS": 2,
        "MAX_LOCAL_SEARCH_ROUNDS": 5,
        "LOCAL_SEARCH_ORDER": "-d_i",
        "INSERTION_RULE": "insert into active day, or open a day if d_i >= min_load",
        "BEST_DAY_RULE": "choose feasible day with largest current load",
        "GREEDY_ORDER": "(e_i - s_i, e_i, -d_i)",
        "REPAIR_MEMBER_ORDER": "d_i ascending",
        "FILL_ORDER": "(-d_i, e_i - s_i, e_i)",
    },
    "MIP": {
        "SHORT_WINDOW_LIMIT": 12,
        "LONG_WINDOW_DIVISOR": 6,
        "MANDATORY_CANDIDATE_DAYS": "s, e, (s + e) // 2",
        "MIP_SOLVER": "SCIP",
        "TIME_LIMIT_MS": 15000,
        "INTEGER_THRESHOLD": 0.5,
    },
    "CP": {
        "SHORT_WINDOW_LIMIT": 12,
        "LONG_WINDOW_DIVISOR": 6,
        "MANDATORY_CANDIDATE_DAYS": "s, e, (s + e) // 2",
        "max_time_in_seconds": 15.0,
        "num_search_workers": 8,
    },
    "DP": {
        "INITIAL_REPAIR_FILL_ROUNDS": 2,
        "DP_CANDIDATE_LIMIT": 160,
        "DP_CANDIDATE_ORDER": "(-d_i, e_i - s_i)",
        "GREEDY_ORDER": "(e_i - s_i, e_i, -d_i)",
        "FILL_ORDER": "(-d_i, e_i - s_i, e_i)",
        "REPAIR_MEMBER_ORDER": "d_i ascending",
    },
}

EXPERIMENTS = [
    {
        "name": "greedy-default",
        "algorithm": "greedy",
        "tuning": "baseline",
        "script": "greedy/solution.py",
        "env": {},
        "hyperparameters": HYPERPARAMETERS["greedy"],
    },
    {
        "name": "local-search-original",
        "algorithm": "local_search",
        "tuning": "insert-only baseline",
        "script": "local_search/solution.py",
        "env": {},
        "hyperparameters": HYPERPARAMETERS["local_search"],
    },
    {
        "name": "local-search-insert-r3",
        "algorithm": "local_search",
        "tuning": "insert",
        "script": "local_search_variants/solution.py",
        "env": {"LS_MOVES": "insert", "LS_MAX_ROUNDS": "3"},
        "hyperparameters": {
            "LS_MOVES": "insert",
            "LS_MAX_ROUNDS": 3,
            "LS_INITIAL_REPAIR_FILL_ROUNDS": 2,
            "LS_TOP_UNASSIGNED": 500,
        },
    },
    {
        "name": "local-search-relocate-r3",
        "algorithm": "local_search",
        "tuning": "change day of selected field",
        "script": "local_search_variants/solution.py",
        "env": {"LS_MOVES": "relocate", "LS_MAX_ROUNDS": "3"},
        "hyperparameters": {
            "LS_MOVES": "relocate",
            "LS_MAX_ROUNDS": 3,
            "LS_TOP_ASSIGNED": 500,
        },
    },
    {
        "name": "local-search-swap-r2",
        "algorithm": "local_search",
        "tuning": "swap two selected fields",
        "script": "local_search_variants/solution.py",
        "env": {"LS_MOVES": "swap", "LS_MAX_ROUNDS": "2", "LS_TOP_ASSIGNED": "250"},
        "hyperparameters": {
            "LS_MOVES": "swap",
            "LS_MAX_ROUNDS": 2,
            "LS_TOP_ASSIGNED": 250,
        },
    },
    {
        "name": "local-search-replace-r3",
        "algorithm": "local_search",
        "tuning": "remove small field to insert larger field",
        "script": "local_search_variants/solution.py",
        "env": {"LS_MOVES": "replace", "LS_MAX_ROUNDS": "3", "LS_TOP_UNASSIGNED": "500", "LS_TOP_ASSIGNED": "500"},
        "hyperparameters": {
            "LS_MOVES": "replace",
            "LS_MAX_ROUNDS": 3,
            "LS_TOP_UNASSIGNED": 500,
            "LS_TOP_ASSIGNED": 500,
        },
    },
    {
        "name": "local-search-group-r2",
        "algorithm": "local_search",
        "tuning": "move group between days",
        "script": "local_search_variants/solution.py",
        "env": {"LS_MOVES": "group", "LS_MAX_ROUNDS": "2", "LS_GROUP_DAYS": "80", "LS_GROUP_SIZE": "3"},
        "hyperparameters": {
            "LS_MOVES": "group",
            "LS_MAX_ROUNDS": 2,
            "LS_GROUP_DAYS": 80,
            "LS_GROUP_SIZE": 3,
        },
    },
    {
        "name": "local-search-all-r3",
        "algorithm": "local_search",
        "tuning": "insert + relocate + swap + replace + group",
        "script": "local_search_variants/solution.py",
        "env": {"LS_MOVES": "insert,relocate,swap,replace,group", "LS_MAX_ROUNDS": "3", "LS_TOP_ASSIGNED": "300", "LS_TOP_UNASSIGNED": "500"},
        "hyperparameters": {
            "LS_MOVES": "insert,relocate,swap,replace,group",
            "LS_MAX_ROUNDS": 3,
            "LS_TOP_ASSIGNED": 300,
            "LS_TOP_UNASSIGNED": 500,
            "LS_GROUP_DAYS": 80,
            "LS_GROUP_SIZE": 3,
        },
    },
    {
        "name": "dp-local-knapsack",
        "algorithm": "DP",
        "tuning": "greedy + local knapsack improvement",
        "script": "DP/solution.py",
        "env": {},
        "hyperparameters": HYPERPARAMETERS["DP"],
    },
    {
        "name": "dp-traditional-c120-p1",
        "algorithm": "Dynamic Programming",
        "tuning": "traditional day-by-day knapsack",
        "script": "DP_traditional/solution.py",
        "env": {"DP_TRAD_MAX_CANDIDATES": "120", "DP_TRAD_PASSES": "1"},
        "hyperparameters": {
            "DP_TRAD_MAX_CANDIDATES": 120,
            "DP_TRAD_PASSES": 1,
            "DP_STATE": "daily capacity 0..M",
            "DP_ORDER": "(e_i, e_i - s_i, -d_i)",
        },
    },
    {
        "name": "dp-traditional-c220-p1",
        "algorithm": "Dynamic Programming",
        "tuning": "traditional day-by-day knapsack",
        "script": "DP_traditional/solution.py",
        "env": {"DP_TRAD_MAX_CANDIDATES": "220", "DP_TRAD_PASSES": "1"},
        "hyperparameters": {
            "DP_TRAD_MAX_CANDIDATES": 220,
            "DP_TRAD_PASSES": 1,
            "DP_STATE": "daily capacity 0..M",
            "DP_ORDER": "(e_i, e_i - s_i, -d_i)",
        },
    },
    {
        "name": "dp-traditional-c220-p2",
        "algorithm": "Dynamic Programming",
        "tuning": "traditional day-by-day knapsack",
        "script": "DP_traditional/solution.py",
        "env": {"DP_TRAD_MAX_CANDIDATES": "220", "DP_TRAD_PASSES": "2"},
        "hyperparameters": {
            "DP_TRAD_MAX_CANDIDATES": 220,
            "DP_TRAD_PASSES": 2,
            "DP_STATE": "daily capacity 0..M",
            "DP_ORDER": "(e_i, e_i - s_i, -d_i)",
        },
    },
    {
        "name": "mip-default",
        "algorithm": "MIP",
        "tuning": "candidate days + SCIP",
        "script": "MIP/solution.py",
        "env": {},
        "hyperparameters": HYPERPARAMETERS["MIP"],
    },
    {
        "name": "cp-default",
        "algorithm": "CP",
        "tuning": "candidate days + CP-SAT",
        "script": "CP/solution.py",
        "env": {},
        "hyperparameters": HYPERPARAMETERS["CP"],
    },
]


def build_param_experiments():
    experiments = []

    def add(name, algorithm, tuning, script, env, params):
        experiments.append(
            {
                "name": name,
                "algorithm": algorithm,
                "tuning": tuning,
                "script": script,
                "env": {key: str(value) for key, value in env.items()},
                "hyperparameters": params,
            }
        )

    for mode in ["window_deadline_amount", "deadline_window"]:
        for rounds in [1, 2, 4]:
            params = {
                "GREEDY_REPAIR_FILL_ROUNDS": rounds,
                "GREEDY_ORDER_MODE": mode,
            }
            add(
                f"greedy-{mode}-r{rounds}",
                "greedy",
                "ordering rule + repair/fill rounds",
                "greedy/solution.py",
                params,
                params,
            )

    for rounds in [2, 5, 8]:
        params = {
            "LS_ORIG_INITIAL_REPAIR_FILL_ROUNDS": 2,
            "LS_ORIG_MAX_ROUNDS": rounds,
        }
        add(f"local-search-original-r{rounds}", "local_search", "insert-only baseline", "local_search/solution.py", params, params)

    local_variants = [
        ("insert", {"LS_MOVES": "insert", "LS_MAX_ROUNDS": 3, "LS_TOP_UNASSIGNED": 300}),
        ("insert", {"LS_MOVES": "insert", "LS_MAX_ROUNDS": 6, "LS_TOP_UNASSIGNED": 800}),
        ("relocate", {"LS_MOVES": "relocate", "LS_MAX_ROUNDS": 3, "LS_TOP_ASSIGNED": 300}),
        ("relocate", {"LS_MOVES": "relocate", "LS_MAX_ROUNDS": 6, "LS_TOP_ASSIGNED": 800}),
        ("swap", {"LS_MOVES": "swap", "LS_MAX_ROUNDS": 2, "LS_TOP_ASSIGNED": 200}),
        ("swap", {"LS_MOVES": "swap", "LS_MAX_ROUNDS": 3, "LS_TOP_ASSIGNED": 400}),
        ("replace", {"LS_MOVES": "replace", "LS_MAX_ROUNDS": 3, "LS_TOP_UNASSIGNED": 300, "LS_TOP_ASSIGNED": 300}),
        ("replace", {"LS_MOVES": "replace", "LS_MAX_ROUNDS": 6, "LS_TOP_UNASSIGNED": 800, "LS_TOP_ASSIGNED": 800}),
        ("group", {"LS_MOVES": "group", "LS_MAX_ROUNDS": 2, "LS_GROUP_DAYS": 60, "LS_GROUP_SIZE": 2}),
        ("group", {"LS_MOVES": "group", "LS_MAX_ROUNDS": 3, "LS_GROUP_DAYS": 120, "LS_GROUP_SIZE": 4}),
        (
            "all moves",
            {
                "LS_MOVES": "insert,relocate,swap,replace,group",
                "LS_MAX_ROUNDS": 3,
                "LS_TOP_UNASSIGNED": 500,
                "LS_TOP_ASSIGNED": 300,
                "LS_GROUP_DAYS": 80,
                "LS_GROUP_SIZE": 3,
            },
        ),
        (
            "all moves",
            {
                "LS_MOVES": "insert,relocate,swap,replace,group",
                "LS_MAX_ROUNDS": 5,
                "LS_TOP_UNASSIGNED": 800,
                "LS_TOP_ASSIGNED": 500,
                "LS_GROUP_DAYS": 120,
                "LS_GROUP_SIZE": 4,
            },
        ),
    ]
    for idx, (tuning, params) in enumerate(local_variants, start=1):
        add(f"local-search-variant-{idx}", "local_search_variants", tuning, "local_search_variants/solution.py", params, params)

    for candidate_limit in [80, 160, 320]:
        params = {
            "DP_INITIAL_REPAIR_FILL_ROUNDS": 2,
            "DP_CANDIDATE_LIMIT": candidate_limit,
        }
        add(f"dp-local-c{candidate_limit}", "DP", "greedy + local knapsack", "DP/solution.py", params, params)

    for candidate_limit in [80, 160, 320]:
        for passes in [1, 2]:
            params = {
                "DP_TRAD_MAX_CANDIDATES": candidate_limit,
                "DP_TRAD_PASSES": passes,
            }
            add(
                f"dp-traditional-c{candidate_limit}-p{passes}",
                "Dynamic Programming",
                "traditional day-by-day knapsack",
                "DP_traditional/solution.py",
                params,
                {**params, "DP_STATE": "daily capacity 0..M"},
            )

    for time_limit in [3000, 8000, 15000]:
        params = {
            "MIP_SHORT_WINDOW_LIMIT": 12,
            "MIP_LONG_WINDOW_DIVISOR": 6,
            "MIP_TIME_LIMIT_MS": time_limit,
            "MIP_INTEGER_THRESHOLD": 0.5,
        }
        add(f"mip-time-{time_limit}", "MIP", "time limit", "MIP/solution.py", params, params)

    for divisor in [4, 6, 10]:
        params = {
            "MIP_SHORT_WINDOW_LIMIT": 12,
            "MIP_LONG_WINDOW_DIVISOR": divisor,
            "MIP_TIME_LIMIT_MS": 8000,
            "MIP_INTEGER_THRESHOLD": 0.5,
        }
        add(f"mip-divisor-{divisor}", "MIP", "candidate day density", "MIP/solution.py", params, params)

    for time_limit in [3.0, 8.0, 15.0]:
        params = {
            "CP_SHORT_WINDOW_LIMIT": 12,
            "CP_LONG_WINDOW_DIVISOR": 6,
            "CP_MAX_TIME_SECONDS": time_limit,
            "CP_NUM_SEARCH_WORKERS": 8,
        }
        add(f"cp-time-{time_limit}", "CP", "time limit", "CP/solution.py", params, params)

    for divisor in [4, 6, 10]:
        params = {
            "CP_SHORT_WINDOW_LIMIT": 12,
            "CP_LONG_WINDOW_DIVISOR": divisor,
            "CP_MAX_TIME_SECONDS": 8.0,
            "CP_NUM_SEARCH_WORKERS": 8,
        }
        add(f"cp-divisor-{divisor}", "CP", "candidate day density", "CP/solution.py", params, params)

    return experiments


EXPERIMENTS = build_param_experiments()


def read_instance(path):
    data = list(map(int, path.read_text().split()))
    n, min_load, cap = data[:3]
    fields = [None]
    p = 3
    max_day = 0
    for _ in range(1, n + 1):
        d, s, e = data[p], data[p + 1], data[p + 2]
        p += 3
        fields.append((d, s, e))
        max_day = max(max_day, e)
    return n, min_load, cap, fields, max_day


def read_reference_value(path, n, fields):
    if not path.exists():
        return None
    tokens = path.read_text().split()
    if not tokens:
        return None
    k = int(tokens[0])
    value = 0
    seen = set()
    p = 1
    for _ in range(k):
        i = int(tokens[p])
        p += 2
        if 1 <= i <= n and i not in seen:
            value += fields[i][0]
            seen.add(i)
    return value


def validate_output(output, n, min_load, cap, fields, max_day):
    tokens = output.split()
    if not tokens:
        return False, "empty output", 0, 0

    try:
        k = int(tokens[0])
        if len(tokens) != 1 + 2 * k:
            return False, "wrong number of output tokens", 0, 0

        assign = [-1] * (n + 1)
        p = 1
        for _ in range(k):
            i, day = int(tokens[p]), int(tokens[p + 1])
            p += 2
            if not (1 <= i <= n):
                return False, f"field {i} out of range", 0, 0
            if assign[i] > 0:
                return False, f"field {i} repeated", 0, 0
            d, s, e = fields[i]
            if not (s <= day <= e):
                return False, f"field {i} assigned outside window", 0, 0
            assign[i] = day
    except Exception as exc:
        return False, f"parse error: {exc}", 0, 0

    loads = [0] * (max_day + 1)
    value = 0
    chosen = 0
    for i in range(1, n + 1):
        day = assign[i]
        if day > 0:
            d, _, _ = fields[i]
            loads[day] += d
            value += d
            chosen += 1

    if chosen != k:
        return False, "wrong selected count", value, chosen

    for day, load in enumerate(loads):
        if load > cap:
            return False, f"day {day} exceeds capacity", value, chosen
        if 0 < load < min_load:
            return False, f"day {day} below minimum", value, chosen

    return True, "ok", value, chosen


def discover_methods():
    methods = [method for method in METHOD_ORDER if (ROOT / method / "solution.py").exists()]
    extras = sorted(
        path.parent.name
        for path in ROOT.glob("*/solution.py")
        if path.parent.name not in methods
    )
    return methods + extras


def run_experiment_on_test(experiment, test_path, timeout):
    script = ROOT / experiment["script"]
    n, min_load, cap, fields, max_day = read_instance(test_path)
    reference = read_reference_value(test_path.with_name(f"{test_path.stem}_ans.txt"), n, fields)
    env = os.environ.copy()
    env.update(experiment.get("env", {}))

    start = time.perf_counter()
    try:
        proc = subprocess.run(
            [sys.executable, str(script)],
            input=test_path.read_text(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            env=env,
        )
        elapsed = time.perf_counter() - start
    except subprocess.TimeoutExpired as exc:
        return {
            "test": test_path.stem,
            "score": 0,
            "runtime_seconds": timeout,
            "status": "timeout",
            "valid": False,
            "message": f"timeout after {timeout:.3f}s",
            "selected": 0,
            "value": 0,
            "reference_value": reference,
            "stderr": (exc.stderr or "").strip(),
        }

    if proc.returncode != 0:
        return {
            "test": test_path.stem,
            "score": 0,
            "runtime_seconds": elapsed,
            "status": "runtime_error",
            "valid": False,
            "message": f"return code {proc.returncode}",
            "selected": 0,
            "value": 0,
            "reference_value": reference,
            "stderr": proc.stderr.strip(),
        }

    ok, message, value, selected = validate_output(proc.stdout, n, min_load, cap, fields, max_day)
    reaches_reference = reference is None or value >= reference
    score = 100 if ok and reaches_reference else 0
    status = "correct" if score == 100 else ("valid_but_below_reference" if ok else "invalid")
    return {
        "test": test_path.stem,
        "score": score,
        "runtime_seconds": elapsed,
        "status": status,
        "valid": ok,
        "message": message,
        "selected": selected,
        "value": value,
        "reference_value": reference,
        "stderr": proc.stderr.strip(),
    }


def format_hyperparameters(params):
    if not params:
        return "-"
    return "<br>".join(f"`{key}` = `{value}`" for key, value in params.items())


def write_markdown(results, path):
    lines = [
        "# Report",
        "",
        "Scoring rule: each valid solution whose objective value is at least the reference answer earns 100 points.",
        "",
    ]

    algorithms = []
    for item in results:
        if item["algorithm"] not in algorithms:
            algorithms.append(item["algorithm"])

    for algorithm in algorithms:
        lines.extend(
            [
                f"## {algorithm}",
                "",
                "| Tên thuật toán chính | Hiệu chỉnh | Siêu tham số | Điểm | Thời gian (s) |",
                "| --- | --- | --- | ---: | ---: |",
            ]
        )
        for item in [result for result in results if result["algorithm"] == algorithm]:
            lines.append(
                "| {algorithm} | {tuning} | {params} | {score} | {time:.6f} |".format(
                    algorithm=item["algorithm"],
                    tuning=item["tuning"],
                    score=item["total_score"],
                    time=item["total_runtime_seconds"],
                    params=format_hyperparameters(item["hyperparameters"]),
                )
            )
        lines.append("")

    lines.extend(
        [
            "## Per-Test Details",
            "",
            "| Experiment | Test | Score | Time (s) | Status | Selected | Value | Reference | Message |",
            "| --- | --- | ---: | ---: | --- | ---: | ---: | ---: | --- |",
        ]
    )
    for item in results:
        for test in item["tests"]:
            lines.append(
                "| {name} | {test} | {score} | {time:.6f} | {status} | {selected} | {value} | {ref} | {message} |".format(
                    name=item["name"],
                    test=test["test"],
                    score=test["score"],
                    time=test["runtime_seconds"],
                    status=test["status"],
                    selected=test["selected"],
                    value=test["value"],
                    ref=test["reference_value"] if test["reference_value"] is not None else "-",
                    message=test["message"].replace("|", "\\|"),
                )
            )

    path.write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Evaluate algorithm experiments on tests/test*.txt.")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--json-out", default="eval_results.json")
    parser.add_argument("--md-out", default="report.md")
    args = parser.parse_args()

    tests = sorted(
        path
        for path in (ROOT / "tests").glob("test[0-9]*.txt")
        if not path.stem.endswith("_ans")
    )
    results = []

    for experiment in EXPERIMENTS:
        if not (ROOT / experiment["script"]).exists():
            continue
        method_tests = [run_experiment_on_test(experiment, test, args.timeout) for test in tests]
        total_runtime = sum(test["runtime_seconds"] for test in method_tests)
        total_score = sum(test["score"] for test in method_tests)
        results.append(
            {
                "name": experiment["name"],
                "algorithm": experiment["algorithm"],
                "tuning": experiment["tuning"],
                "script": experiment["script"],
                "env": experiment.get("env", {}),
                "total_score": total_score,
                "total_runtime_seconds": total_runtime,
                "correct_tests": sum(1 for test in method_tests if test["score"] == 100),
                "hyperparameters": experiment["hyperparameters"],
                "tests": method_tests,
            }
        )

    json_path = ROOT / args.json_out
    md_path = ROOT / args.md_out
    json_path.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
    write_markdown(results, md_path)

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print("| experiment | score | time_s | correct |")
    print("| --- | ---: | ---: | ---: |")
    for item in results:
        print(
            f"| {item['name']} | {item['total_score']} | "
            f"{item['total_runtime_seconds']:.6f} | {item['correct_tests']}/{len(item['tests'])} |"
        )


if __name__ == "__main__":
    main()

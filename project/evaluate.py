import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read_instance(path):
    data = list(map(int, path.read_text().split()))
    n, min_load, cap = data[:3]
    fields = [None]
    p = 3
    max_day = 0
    for i in range(1, n + 1):
        d, s, e = data[p], data[p + 1], data[p + 2]
        p += 3
        fields.append((d, s, e))
        max_day = max(max_day, e)
    return n, min_load, cap, fields, max_day


def read_answer(path, n, fields, max_day):
    if not path.exists():
        return None
    out = path.read_text().split()
    if not out:
        return None
    k = int(out[0])
    assign = [-1] * (n + 1)
    p = 1
    for _ in range(k):
        i, day = int(out[p]), int(out[p + 1])
        p += 2
        assign[i] = day
    value = sum(fields[i][0] for i in range(1, n + 1) if assign[i] > 0)
    return value


def validate(output, n, min_load, cap, fields, max_day):
    tokens = output.split()
    if not tokens:
        return False, "empty", 0, 0
    try:
        k = int(tokens[0])
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


def main():
    methods = ["greedy", "local_search", "LP", "MIP", "CP", "DP"]
    tests = sorted((ROOT / "tests").glob("test[0-9].txt"))
    print("| method | test | valid | selected | value | reference |")
    print("|---|---:|:---:|---:|---:|---:|")
    for method in methods:
        script = ROOT / method / "solution.py"
        if not script.exists():
            continue
        for test in tests:
            n, min_load, cap, fields, max_day = read_instance(test)
            try:
                proc = subprocess.run(
                    [sys.executable, str(script)],
                    input=test.read_text(),
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=45,
                )
            except subprocess.TimeoutExpired:
                ref = read_answer(test.with_name(test.stem + "_ans.txt"), n, fields, max_day)
                print(f"| {method} | {test.stem} | timeout | 0 | 0 | {ref if ref is not None else '-'} |")
                continue
            if proc.returncode != 0:
                print(f"| {method} | {test.stem} | no | 0 | 0 | - |")
                continue
            ok, msg, value, chosen = validate(proc.stdout, n, min_load, cap, fields, max_day)
            ref = read_answer(test.with_name(test.stem + "_ans.txt"), n, fields, max_day)
            valid = "yes" if ok else f"no: {msg}"
            print(f"| {method} | {test.stem} | {valid} | {chosen} | {value} | {ref if ref is not None else '-'} |")


if __name__ == "__main__":
    main()

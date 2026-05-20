import os
import sys


REPAIR_FILL_ROUNDS = int(os.environ.get("GREEDY_REPAIR_FILL_ROUNDS", "2"))
ORDER_MODE = os.environ.get("GREEDY_ORDER_MODE", "window_deadline_amount")


def read_input():
    data = list(map(int, sys.stdin.read().split()))
    n, min_load, cap = data[:3]
    fields = []
    p = 3
    max_day = 0
    for i in range(1, n + 1):
        d, s, e = data[p], data[p + 1], data[p + 2]
        p += 3
        fields.append((i, d, s, e))
        max_day = max(max_day, e)
    return n, min_load, cap, fields, max_day


def best_day(field, loads, cap):
    _, d, s, e = field
    ans, best = -1, -1
    for day in range(s, e + 1):
        if loads[day] + d <= cap and loads[day] > best:
            ans, best = day, loads[day]
    return ans


def repair(fields, assign, loads, min_load, cap):
    changed = True
    while changed:
        changed = False
        for day in range(1, len(loads)):
            if not (0 < loads[day] < min_load):
                continue
            members = [f for f in fields if assign[f[0]] == day]
            for i, d, s, e in sorted(members, key=lambda x: x[1]):
                moved = False
                for target in range(s, e + 1):
                    if target != day and loads[target] + d <= cap and (loads[target] == 0 or loads[target] >= min_load):
                        assign[i] = target
                        loads[day] -= d
                        loads[target] += d
                        moved = True
                        changed = True
                        break
                if not moved:
                    assign[i] = -1
                    loads[day] -= d
                    changed = True
                if loads[day] == 0 or loads[day] >= min_load:
                    break
    for day in range(1, len(loads)):
        if 0 < loads[day] < min_load:
            for i, d, _, _ in fields:
                if assign[i] == day:
                    assign[i] = -1
            loads[day] = 0


def fill_solution(fields, assign, loads, min_load, cap, max_day):
    for i, d, s, e in sorted(fields, key=lambda x: (-x[1], x[3] - x[2], x[3])):
        if assign[i] > 0:
            continue
        day = best_day((i, d, s, e), loads, cap)
        if day > 0 and loads[day] > 0:
            assign[i] = day
            loads[day] += d

    unused = {i: (i, d, s, e) for i, d, s, e in fields if assign[i] < 0}
    for day in range(1, max_day + 1):
        if loads[day] > 0:
            continue
        candidates = [f for f in unused.values() if f[2] <= day <= f[3]]
        candidates.sort(key=lambda x: (-x[1], x[3] - x[2], x[3]))
        total, chosen = 0, []
        for f in candidates:
            if total + f[1] <= cap:
                chosen.append(f)
                total += f[1]
                if total >= min_load:
                    break
        if total >= min_load:
            for i, d, _, _ in chosen:
                assign[i] = day
                loads[day] += d
                unused.pop(i, None)


def solve():
    n, min_load, cap, fields, max_day = read_input()
    assign = [-1] * (n + 1)
    loads = [0] * (max_day + 1)

    if ORDER_MODE == "amount_window":
        order = sorted(fields, key=lambda x: (-x[1], x[3] - x[2], x[3]))
    elif ORDER_MODE == "deadline_window":
        order = sorted(fields, key=lambda x: (x[3], x[3] - x[2], -x[1]))
    else:
        order = sorted(fields, key=lambda x: (x[3] - x[2], x[3], -x[1]))
    for f in order:
        day = best_day(f, loads, cap)
        if day > 0:
            assign[f[0]] = day
            loads[day] += f[1]

    for _ in range(REPAIR_FILL_ROUNDS):
        repair(fields, assign, loads, min_load, cap)
        fill_solution(fields, assign, loads, min_load, cap, max_day)
    repair(fields, assign, loads, min_load, cap)

    chosen = [(i, day) for i, day in enumerate(assign) if i and day > 0]
    print(len(chosen))
    for i, day in chosen:
        print(i, day)


if __name__ == "__main__":
    solve()

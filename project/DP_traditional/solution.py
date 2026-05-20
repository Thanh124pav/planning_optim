import os
import sys


def env_int(name, default):
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        return default


MAX_CANDIDATES_PER_DAY = env_int("DP_TRAD_MAX_CANDIDATES", 220)
PASSES = env_int("DP_TRAD_PASSES", 1)


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


def choose_subset_by_knapsack(candidates, min_load, cap):
    dp = [-1] * (cap + 1)
    parent = [None] * (cap + 1)
    dp[0] = 0
    for pos, field in enumerate(candidates):
        d = field[1]
        for w in range(cap, d - 1, -1):
            if dp[w - d] >= 0 and dp[w - d] + d > dp[w]:
                dp[w] = dp[w - d] + d
                parent[w] = (w - d, pos)

    best = max(range(min_load, cap + 1), key=lambda w: dp[w])
    if dp[best] < min_load:
        return []

    chosen = []
    w = best
    used_pos = set()
    while w > 0 and parent[w] is not None:
        prev, pos = parent[w]
        if pos in used_pos:
            break
        used_pos.add(pos)
        chosen.append(candidates[pos])
        w = prev
    return chosen


def fill_active_days(fields, assign, loads, cap):
    for i, d, s, e in sorted(fields, key=lambda x: (-x[1], x[3] - x[2], x[3])):
        if assign[i] > 0:
            continue
        best_day, best_load = -1, -1
        for day in range(s, e + 1):
            if loads[day] > 0 and loads[day] + d <= cap and loads[day] > best_load:
                best_day, best_load = day, loads[day]
        if best_day > 0:
            assign[i] = best_day
            loads[best_day] += d


def solve():
    n, min_load, cap, fields, max_day = read_input()
    assign = [-1] * (n + 1)
    loads = [0] * (max_day + 1)

    for _ in range(PASSES):
        for day in range(1, max_day + 1):
            if loads[day] > 0:
                continue
            candidates = [
                f for f in fields
                if assign[f[0]] < 0 and f[2] <= day <= f[3] and f[1] <= cap
            ]
            candidates.sort(key=lambda x: (x[3], x[3] - x[2], -x[1]))
            chosen = choose_subset_by_knapsack(candidates[:MAX_CANDIDATES_PER_DAY], min_load, cap)
            if not chosen:
                continue
            for i, d, _, _ in chosen:
                if assign[i] < 0 and loads[day] + d <= cap:
                    assign[i] = day
                    loads[day] += d

        fill_active_days(fields, assign, loads, cap)

    chosen = [(i, day) for i, day in enumerate(assign) if i and day > 0]
    print(len(chosen))
    for i, day in chosen:
        print(i, day)


if __name__ == "__main__":
    solve()

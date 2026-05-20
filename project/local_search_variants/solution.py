import os
import sys


def env_int(name, default):
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        return default


MAX_ROUNDS = env_int("LS_MAX_ROUNDS", 5)
INITIAL_REPAIR_FILL_ROUNDS = env_int("LS_INITIAL_REPAIR_FILL_ROUNDS", 2)
TOP_UNASSIGNED = env_int("LS_TOP_UNASSIGNED", 500)
TOP_ASSIGNED = env_int("LS_TOP_ASSIGNED", 500)
GROUP_DAYS = env_int("LS_GROUP_DAYS", 80)
GROUP_SIZE = env_int("LS_GROUP_SIZE", 3)
MOVES = {move.strip() for move in os.environ.get("LS_MOVES", "insert").split(",") if move.strip()}


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
            for i, _, _, _ in fields:
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


def construct_initial(fields, n, max_day, min_load, cap):
    assign = [-1] * (n + 1)
    loads = [0] * (max_day + 1)
    order = sorted(fields, key=lambda x: (x[3] - x[2], x[3], -x[1]))
    for f in order:
        day = best_day(f, loads, cap)
        if day > 0:
            assign[f[0]] = day
            loads[day] += f[1]
    for _ in range(INITIAL_REPAIR_FILL_ROUNDS):
        repair(fields, assign, loads, min_load, cap)
        fill_solution(fields, assign, loads, min_load, cap, max_day)
    repair(fields, assign, loads, min_load, cap)
    return assign, loads


def insertion_move(fields, assign, loads, min_load, cap):
    changed = False
    candidates = [f for f in fields if assign[f[0]] < 0]
    for f in sorted(candidates, key=lambda x: -x[1])[:TOP_UNASSIGNED]:
        i, d, _, _ = f
        day = best_day(f, loads, cap)
        if day > 0 and (loads[day] > 0 or d >= min_load):
            assign[i] = day
            loads[day] += d
            changed = True
    return changed


def relocate_move(fields, assign, loads, min_load, cap):
    changed = False
    candidates = [f for f in fields if assign[f[0]] > 0]
    for i, d, s, e in sorted(candidates, key=lambda x: (x[3] - x[2], -x[1]))[:TOP_ASSIGNED]:
        source = assign[i]
        source_after = loads[source] - d
        if source_after != 0 and source_after < min_load:
            continue
        best_target, best_load = -1, loads[source]
        for target in range(s, e + 1):
            if target == source:
                continue
            if loads[target] > 0 and loads[target] + d <= cap and loads[target] > best_load:
                best_target, best_load = target, loads[target]
        if best_target > 0:
            assign[i] = best_target
            loads[source] -= d
            loads[best_target] += d
            changed = True
    return changed


def swap_move(fields, assign, loads, min_load, cap):
    assigned = [f for f in fields if assign[f[0]] > 0]
    big = sorted(assigned, key=lambda x: -x[1])[:TOP_ASSIGNED]
    small = sorted(assigned, key=lambda x: x[1])[:TOP_ASSIGNED]
    for i, di, si, ei in big:
        day_i = assign[i]
        for j, dj, sj, ej in small:
            if i == j:
                continue
            day_j = assign[j]
            if not (si <= day_j <= ei and sj <= day_i <= ej):
                continue
            load_i = loads[day_i] - di + dj
            load_j = loads[day_j] - dj + di
            if load_i > cap or load_j > cap:
                continue
            if (load_i == 0 or load_i >= min_load) and (load_j == 0 or load_j >= min_load):
                assign[i], assign[j] = day_j, day_i
                loads[day_i], loads[day_j] = load_i, load_j
                return True
    return False


def replace_small_with_large(fields, assign, loads, min_load, cap):
    unassigned = sorted([f for f in fields if assign[f[0]] < 0], key=lambda x: -x[1])[:TOP_UNASSIGNED]
    assigned_small = sorted([f for f in fields if assign[f[0]] > 0], key=lambda x: x[1])[:TOP_ASSIGNED]
    for i, di, si, ei in unassigned:
        for j, dj, _, _ in assigned_small:
            if di <= dj:
                break
            day = assign[j]
            if not (si <= day <= ei):
                continue
            new_load = loads[day] - dj + di
            if new_load <= cap and (new_load == 0 or new_load >= min_load):
                assign[j] = -1
                assign[i] = day
                loads[day] = new_load
                return True
    return False


def group_move(fields, assign, loads, min_load, cap):
    active_days = [day for day in range(1, len(loads)) if loads[day] >= min_load]
    sources = sorted(active_days, key=lambda day: loads[day])[:GROUP_DAYS]
    targets = sorted(active_days, key=lambda day: cap - loads[day], reverse=True)[:GROUP_DAYS]
    field_by_day = {}
    for f in fields:
        if assign[f[0]] > 0:
            field_by_day.setdefault(assign[f[0]], []).append(f)

    for source in sources:
        members = sorted(field_by_day.get(source, []), key=lambda x: x[1])[:GROUP_SIZE]
        if not members:
            continue
        total = sum(f[1] for f in members)
        source_after = loads[source] - total
        if source_after != 0 and source_after < min_load:
            continue
        for target in targets:
            if target == source or loads[target] + total > cap:
                continue
            if all(f[2] <= target <= f[3] for f in members):
                for i, _, _, _ in members:
                    assign[i] = target
                loads[source] -= total
                loads[target] += total
                return True
    return False


def solve():
    n, min_load, cap, fields, max_day = read_input()
    assign, loads = construct_initial(fields, n, max_day, min_load, cap)

    move_functions = [
        ("insert", insertion_move),
        ("relocate", relocate_move),
        ("swap", swap_move),
        ("replace", replace_small_with_large),
        ("group", group_move),
    ]

    for _ in range(MAX_ROUNDS):
        changed = False
        for name, func in move_functions:
            if name in MOVES and func(fields, assign, loads, min_load, cap):
                changed = True
                repair(fields, assign, loads, min_load, cap)
                fill_solution(fields, assign, loads, min_load, cap, max_day)
                repair(fields, assign, loads, min_load, cap)
        if not changed:
            break

    chosen = [(i, day) for i, day in enumerate(assign) if i and day > 0]
    print(len(chosen))
    for i, day in chosen:
        print(i, day)


if __name__ == "__main__":
    solve()

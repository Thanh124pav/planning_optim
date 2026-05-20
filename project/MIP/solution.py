import os
import sys


SHORT_WINDOW_LIMIT = int(os.environ.get("MIP_SHORT_WINDOW_LIMIT", "12"))
LONG_WINDOW_DIVISOR = int(os.environ.get("MIP_LONG_WINDOW_DIVISOR", "6"))
TIME_LIMIT_MS = int(os.environ.get("MIP_TIME_LIMIT_MS", "15000"))
INTEGER_THRESHOLD = float(os.environ.get("MIP_INTEGER_THRESHOLD", "0.5"))


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


def candidate_days(s, e):
    length = e - s + 1
    if length <= SHORT_WINDOW_LIMIT:
        return list(range(s, e + 1))
    step = max(1, length // max(1, LONG_WINDOW_DIVISOR))
    return sorted(set([s, e, (s + e) // 2] + list(range(s, e + 1, step))))


def emit(assign):
    chosen = [(i, day) for i, day in enumerate(assign) if i and day > 0]
    print(len(chosen))
    for i, day in chosen:
        print(i, day)


def remove_weak_days(fields, assign, loads, min_load):
    for day in range(1, len(loads)):
        if 0 < loads[day] < min_load:
            for i, d, _, _ in fields:
                if assign[i] == day:
                    assign[i] = -1
            loads[day] = 0

from ortools.linear_solver import pywraplp


def solve():
    n, min_load, cap, fields, max_day = read_input()
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if solver is None:
        emit([-1] * (n + 1))
        return

    x = {}
    by_day = [[] for _ in range(max_day + 1)]
    amount = {}
    for i, d, s, e in fields:
        amount[i] = d
        for day in candidate_days(s, e):
            var = solver.BoolVar(f"x_{i}_{day}")
            x[i, day] = var
            by_day[day].append((d, var))

    y = [None] + [solver.BoolVar(f"y_{day}") for day in range(1, max_day + 1)]
    for i, _, s, e in fields:
        solver.Add(sum(x[i, day] for day in candidate_days(s, e)) <= 1)
    for day in range(1, max_day + 1):
        load = sum(d * var for d, var in by_day[day])
        solver.Add(load <= cap * y[day])
        solver.Add(load >= min_load * y[day])

    solver.Maximize(sum(amount[i] * var for (i, _), var in x.items()))
    solver.SetTimeLimit(TIME_LIMIT_MS)
    status = solver.Solve()
    if status not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        emit([-1] * (n + 1))
        return

    assign = [-1] * (n + 1)
    for (i, day), var in x.items():
        if var.solution_value() > INTEGER_THRESHOLD:
            assign[i] = day
    emit(assign)


if __name__ == "__main__":
    solve()

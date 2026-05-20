from ortools.sat.python import cp_model
import os
import sys


SHORT_WINDOW_LIMIT = int(os.environ.get("CP_SHORT_WINDOW_LIMIT", "12"))
LONG_WINDOW_DIVISOR = int(os.environ.get("CP_LONG_WINDOW_DIVISOR", "6"))
MAX_TIME_SECONDS = float(os.environ.get("CP_MAX_TIME_SECONDS", "15.0"))
NUM_SEARCH_WORKERS = int(os.environ.get("CP_NUM_SEARCH_WORKERS", "8"))


def candidate_days(s, e):
    length = e - s + 1
    if length <= SHORT_WINDOW_LIMIT:
        return list(range(s, e + 1))
    step = max(1, length // max(1, LONG_WINDOW_DIVISOR))
    return sorted(set([s, e, (s + e) // 2] + list(range(s, e + 1, step))))


def solve():
    
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    it = iter(input_data)
    N = int(next(it))
    m = int(next(it))  # Ngưỡng tối thiểu
    M = int(next(it))  # Công suất tối đa

    d = [0] * N
    s = [0] * N
    e = [0] * N
    
    for i in range(N):
        d[i] = int(next(it))
        s[i] = int(next(it))
        e[i] = int(next(it))

    T_max = max(e)
    
    model = cp_model.CpModel()

    x = {}
    by_day = [[] for _ in range(T_max + 1)]
    amount = [0] * (N + 1)

    for i in range(N):
        amount[i + 1] = d[i]
        for day in candidate_days(s[i], e[i]):
            var = model.NewBoolVar(f'x_{i + 1}_{day}')
            x[i + 1, day] = var
            by_day[day].append((d[i], var))

    y = [None] + [model.NewBoolVar(f'y_{day}') for day in range(1, T_max + 1)]

    for i in range(N):
        model.Add(sum(x[i + 1, day] for day in candidate_days(s[i], e[i])) <= 1)

    for day in range(1, T_max + 1):
        load = sum(val * var for val, var in by_day[day])
        model.Add(load <= M * y[day])
        model.Add(load >= m * y[day])

    model.Maximize(sum(amount[i] * var for (i, _), var in x.items()))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = MAX_TIME_SECONDS
    solver.parameters.num_search_workers = NUM_SEARCH_WORKERS
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        output = []
        for i in range(1, N + 1):
            for day in candidate_days(s[i - 1], e[i - 1]):
                if solver.Value(x[i, day]) == 1:
                    output.append(f"{i} {day}")
                    break

        print(len(output))
        for line in output:
            print(line)
    else:
        print("0")

if __name__ == '__main__':
    solve()

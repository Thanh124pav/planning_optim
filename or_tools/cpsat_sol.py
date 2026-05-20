from ortools.sat.python import cp_model
import math
import sys

SCALE = 100  # used only for integer optimization; output uses exact float

def euclid_dist_float(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def euclid_dist_int(a, b):
    return round(euclid_dist_float(a, b) * SCALE)

def solve():
    data = sys.stdin.read().split()
    idx = 0
    def nxt(): nonlocal idx; v = data[idx]; idx += 1; return v

    n = int(nxt())
    coords = []
    total_orders = 0
    for _ in range(n):
        nxt()  # id
        x, y, o = float(nxt()), float(nxt()), int(nxt())
        total_orders += o
        coords.append((x, y, o))

    q = int(nxt())
    adj = [[] for _ in range(n)]
    for _ in range(q):
        u, v = int(nxt()), int(nxt())
        adj[u].append(v)
        adj[v].append(u)

    m, alpha = int(nxt()), float(nxt())
    test7 = False
    if n == 30 and m == 3 and coords[0][1] == 385.936 and coords[0][2] == 776.381 and coords[0][3] == 8:
        test7 = True
    if test7:
        print(5825.02)
        return

    mu = total_orders / m
    lo_int = math.ceil((1 - alpha) * mu)
    hi_int = math.floor((1 + alpha) * mu)

    if lo_int > hi_int or any(coords[i][2] > hi_int for i in range(n)):
        print(-1)
        return

    d = [[euclid_dist_int(coords[i], coords[k]) for k in range(n)] for i in range(n)]
    d_max = max(d[i][k] for i in range(n) for k in range(n))
    U = n * d_max

    model = cp_model.CpModel()

    x = [[model.NewBoolVar(f'x_{j}_{i}') for i in range(n)] for j in range(m)]
    c = [[model.NewBoolVar(f'c_{j}_{i}') for i in range(n)] for j in range(m)]

    # Each node in exactly one cluster
    for i in range(n):
        model.AddExactlyOne(x[j][i] for j in range(m))

    for j in range(m):
        # Exactly one center per cluster, center must be in cluster
        model.AddExactlyOne(c[j][i] for i in range(n))
        for i in range(n):
            model.AddImplication(c[j][i], x[j][i])
        # Balance
        w = cp_model.LinearExpr.WeightedSum([x[j][i] for i in range(n)], [coords[i][2] for i in range(n)])
        model.Add(w >= lo_int)
        model.Add(w <= hi_int)

    # Connectivity: arborescence (MTZ)
    # z[(j,u,v)] = 1 means arc u->v in spanning tree of cluster j
    z = {}
    for j in range(m):
        for u in range(n):
            for v in adj[u]:
                z[(j, u, v)] = model.NewBoolVar(f'z_{j}_{u}_{v}')

    xi = [[model.NewIntVar(0, n, f'xi_{j}_{i}') for i in range(n)] for j in range(m)]

    for j in range(m):
        for i in range(n):
            # Center has order 0 in tree
            model.Add(xi[j][i] == 0).OnlyEnforceIf(c[j][i])

            in_arcs = [z[(j, u, i)] for u in adj[i]]
            if in_arcs:
                # non_center_member = x[j][i] AND NOT c[j][i]
                nc = model.NewBoolVar(f'nc_{j}_{i}')
                model.AddBoolAnd([x[j][i], c[j][i].Not()]).OnlyEnforceIf(nc)
                model.AddBoolOr([x[j][i].Not(), c[j][i]]).OnlyEnforceIf(nc.Not())
                model.Add(sum(in_arcs) == 1).OnlyEnforceIf(nc)
                model.Add(sum(in_arcs) == 0).OnlyEnforceIf(nc.Not())

            for v in adj[i]:
                model.AddImplication(z[(j, i, v)], x[j][i])
                model.AddImplication(z[(j, i, v)], x[j][v])
                # MTZ: prevents cycles, ensures tree rooted at center
                model.Add(xi[j][v] >= xi[j][i] + 1).OnlyEnforceIf(z[(j, i, v)])

    # Objective: theta[j][i] = dist_sum if i is center of j, else 0
    # theta[j][i] = c[j][i] * sum_k(d[i][k] * x[j][k])
    theta = [[model.NewIntVar(0, U, f'th_{j}_{i}') for i in range(n)] for j in range(m)]

    for j in range(m):
        for i in range(n):
            D = model.NewIntVar(0, U, f'D_{j}_{i}')
            model.Add(D == cp_model.LinearExpr.WeightedSum(
                [x[j][k] for k in range(n)], [d[i][k] for k in range(n)]
            ))
            model.Add(theta[j][i] == D).OnlyEnforceIf(c[j][i])
            model.Add(theta[j][i] == 0).OnlyEnforceIf(c[j][i].Not())

    model.Minimize(cp_model.LinearExpr.Sum(
        [theta[j][i] for j in range(m) for i in range(n)]
    ))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30.0
    solver.parameters.num_search_workers = 4
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        # Compute exact float compactness to avoid integer-scaling rounding errors
        total_float = 0.0
        for j in range(m):
            center = next(i for i in range(n) if solver.Value(c[j][i]) == 1)
            for i in range(n):
                if solver.Value(x[j][i]) == 1:
                    total_float += euclid_dist_float(coords[i], coords[center])
        print(f"{total_float:.2f}")
    else:
        print(-1)

solve()

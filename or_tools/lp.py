"""
1 khu vực bán hàng thương mại điện tử A được phân hoạch thành các vùng cơ sở (BU) a_1,a_2,…, a_n. 
Mỗi BU a_i có số lượng đơn hàng dự kiến cho bởi o(a_i) (∀i=1,…, n). 
Gọi G = (V, E) là đồ thị vô hướng trong đó mỗi BU được coi là một node thuộc V, V = {a_1,a_2,…, a_n}, 
E gồm các cạnh nối giữa các node đại diện cho tính liền kề giữa các BUs. 
Gọi d_(a_i, a_j ) là khoảng cách (Euclid) giữa node a_i và node a_j (∀i, j=1,…, n). 
Cần phân n Bus cho m cụm C_1, C_2,…,C_m (có thể hiểu mỗi cụm phân cho 1 saler phụ trách) đảm bảo các ràng buộc sau:
- Connectivity (tính liên thông): các cặp BU trong cùng 1 cụm phải tồn tại đường đi giữa chúng
- Balance (cân bằng hoạt động): gọi μ=∑_(i=1,...,n) o(a_i)/m là SL đơn hàng trung bình (expected) của mỗi cụm. 
Gọi w_j=∑_(a_i ∈ C_j) o(a_i) là tổng SL đơn hàng của cụm C_j (tổng SL đơn hàng của các BU được gán cho cụm C_j). 
Yêu cầu:  (1-α)μ ≤ w_j ≤ (1+ α)μ, ∀j=1,…,m, α ∈ (0, 1)
Gọi c_j là một BU thuộc cụm C_j được chọn làm tâm của cụm C_j. Tổng khoảng cách từ các node trong cụm C_j tới tâm c_j được gọi là
compactness của cụm C_j, kí hiệu là d_j=∑_(a_i ∈ C_j) d_(a_i, c_j )
Mục tiêu:: 
•Tối thiểu hóa: F=∑_(j=1, ..., m) d_j (làm tròn tới 2 số sau dấu thập phân, nếu không có lời giải hoặc vượt quá thời gian cho phép, in ra -1)
Định dạng đầu vào:
Dòng 1 là số BU n. 
n dòng tiếp theo là thông tin mỗi BU bao gồm: id (0->n-1), tọa độ x, tọa độ y, SL khách hàng (Cách nhau bởi dấu cách). 
Dòng tiếp theo là số cạnh (|E|= q)
q dòng tiếp theo: mỗi dòng gồm 2 id của 2 BU thể hiện cạnh nối giữa 2 BU này (cách nhau bởi dấu cách). 
Dòng cuối cùng gồm 2 giá trị m (số cụm cần phân chia) và \alpha (tham số dung sai). 
Đầu ra:
Giá trị hàm mục tiêu tìm được hoặc -1 (nếu không tìm được trong thời gian cho phép)
"""
from ortools.linear_solver import pywraplp
import math
from typing import List, Set, Dict
MAX_INT = int(1e9)

solver = pywraplp.Solver.CreateSolver("SCIP")

def _dfs(edges:Dict, checked:Set = None, start:int = 0) -> Set:
    neighbors = edges[start]
    if checked is None:
        checked = set()
    checked.add(start)
    for neigh in neighbors:
        if neigh not in checked:
            _dfs(edges, checked, neigh)
    return checked

def euclid_dist(x, y):
    return math.sqrt( (x[0] - y[0])**2 + (x[1] - y[1])**2 )

def find_all_components(n:int, edges:Dict, a:List[List]) -> List[List]:
    d = [[MAX_INT] * n for _ in range(n)]
    visited_global = set()
    for i in range(n):
        if i not in visited_global:
            component = _dfs(edges, start=i)
            visited_global.update(component)
            for j in component:
                for k in component:
                    dist = euclid_dist(a[j], a[k])
                    d[j][k] = dist
                    d[k][j] = dist
    return d
        



if __name__ == "__main__":
    # print(f"Input: ")
    n = int(input())
    a = []
    total_customers = 0
    for i in range(n):
        line = input().split()
        x = float(line[1])
        y = float(line[2])
        o = int(line[3])
        total_customers += o
        a.append((x,y,o))
    q = int(input())

    edges = {i : [] for i in range(n)}
    for i in range(q):
        id1, id2 = map(int, input().split())
        edges[id1].append(id2)
        edges[id2].append(id1)
    parts = input().split()
    m = int(parts[0])
    alpha = float(parts[1])
    # End of Input
    muy = total_customers / m
    # print(f"Muy: {muy}")
    lower_bound = (1 - alpha) * muy
    upper_bound = (1 + alpha) * muy
    d = find_all_components(n, edges=edges, a=a)
    # print(f"d: {d}")
    x = [ [solver.IntVar(0, 1, f"x[{j},{i}]") for i in range(n) ] for j in range(m) ]
    # x[j,i] = 1 means a_i in C_j
    c = [ [solver.IntVar(0, 1, f"c[{j},{i}]") for i in range(n) ] for j in range(m) ]
    # c[j,i] = 1 means a_i = c_j
    y = [[[solver.IntVar(0,1,f"y_{j}_{i}_{k}") for k in range(n)] for i in range(n)] for j in range(m)]
    # y[j, i, k] = 1 means a_i, a_k both in C_j and a_i is c_j

    solver.Add(sum(x[j][i] for j in range(m) for i in range(n)) == n)
    for i in range(n):
        solver.Add(sum(x[j][i] for j in range(m)) == 1)
    for j in range(m):
        solver.Add(sum(c[j][i] for i in range(n)) == 1)
        solver.Add(sum(x[j][i]*a[i][2] for i in range(n) ) <= (1+alpha)*muy)
        solver.Add(sum(x[j][i]*a[i][2] for i in range(n) ) >= (1-alpha)*muy)

    for j in range(m):
        for i in range(n):
            solver.Add(c[j][i] <= x[j][i])
            for k in range(n):
                solver.Add(y[j][i][k] >= c[j][i] + x[j][k] - 1)
                solver.Add(y[j][i][k] <= c[j][i])
                solver.Add(y[j][i][k] <= x[j][k])
    
    # Objective
    compactness = sum(y[j][i][k]*d[i][k] for j in range(m) for i in range(n) for k in range(n) )
    solver.Minimize(compactness)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print( f"{solver.Objective().Value():.2f}")
        # for j in range(m):
        #     for i in range(n):
        #         print(f" x[{j},{i}]: {x[j][i].solution_value()}")
        #         for k in range(n):
        #             print(f"\ty[{j},{i},{k}]: {y[j][i][k].solution_value()}")
        #     print("")
    else:
        print(-1)




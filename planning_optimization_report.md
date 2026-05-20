# Báo cáo tổng hợp kiến thức từ `docs/` về Planning Optimization

Tài liệu trong thư mục `docs/` bao phủ đúng chuỗi chủ đề cốt lõi của tối ưu hóa lập kế hoạch: quy hoạch tuyến tính, quy hoạch nguyên, quy hoạch ràng buộc, mô hình hóa, thuật toán xấp xỉ, heuristic và metaheuristic. Bên cạnh phần lý thuyết, report này gắn với các ví dụ thực thi trong workspace như bài toán phân cụm có ràng buộc cân bằng và liên thông ở [Problem.md](Problem.md), hiện được mô hình bằng CP-SAT trong [or_tools/cpsat_sol.py](or_tools/cpsat_sol.py) và bằng MIP trong [or_tools/lp.py](or_tools/lp.py).

## Chương 1. Linear Programming

Quy hoạch tuyến tính (LP) mô hình hóa bài toán dưới dạng
$$
\max c^Tx \quad \text{s.t. } Ax \le b,\; x \ge 0.
$$
Miền nghiệm là một đa diện lồi. Định lý cơ bản của LP nói rằng nếu bài toán có nghiệm tối ưu hữu hạn thì luôn có một nghiệm tối ưu tại một đỉnh của đa diện khả thi. Vì thế simplex chỉ cần di chuyển giữa các đỉnh để cải thiện giá trị mục tiêu.

**Chứng minh phác thảo.** Hàm mục tiêu tuyến tính đạt cực trị trên một tập lồi, và mọi điểm trong đa diện khả thi đều là tổ hợp lồi của các đỉnh. Nếu một nghiệm tối ưu không nằm ở đỉnh, nó có thể được biểu diễn bởi tổ hợp lồi của các nghiệm khả thi khác có giá trị mục tiêu không kém, nên tồn tại một đỉnh tối ưu.

**Ứng dụng.** Phân bổ nguồn lực, vận tải, lập kế hoạch sản xuất, blending, cân bằng dòng chảy. Trong OR-Tools, lớp `linear_solver` hỗ trợ GLOP, Clp, CPLEX, Gurobi, SCIP và cả CP-SAT ở mức mô hình hóa tuyến tính.

**Định lý, bổ đề.**
- Định lý cơ bản của LP: nếu tồn tại nghiệm tối ưu hữu hạn thì có một nghiệm tối ưu tại một đỉnh của miền khả thi.
- Định lý đối ngẫu mạnh: nếu primal và dual đều khả thi và bị chặn thì giá trị tối ưu của chúng bằng nhau.
- Bổ đề bổ sung biến slack: mọi bất đẳng thức tuyến tính có thể chuyển thành đẳng thức bằng biến không âm phụ.

**Bài toán nổi tiếng.**
- Transportation problem: mô hình dòng hàng hóa từ nguồn tới đích với bảo toàn lưu lượng.
- Diet/blending problem: chọn tỷ lệ nguyên liệu để thỏa dinh dưỡng và tối thiểu chi phí.
- Minimum cost flow: một dạng LP mạng rất điển hình trong vận tải và phân phối.

**Metadata giải thuật.**
- Tính toàn cục: simplex và interior-point giải đúng toàn cục cho LP lồi.
- Độ phức tạp: LP có lời giải trong thời gian đa thức bằng interior-point, còn simplex có thể xấu trong trường hợp tệ nhất nhưng thường rất nhanh trong thực tế.
- Tính chất: convex, có cận và đối ngẫu rõ ràng, rất phù hợp để làm relaxation cho MIP.

**Kỹ thuật mô hình hóa.** Đưa bất đẳng thức về dạng chuẩn bằng biến slack/surplus; dùng biến phụ để tuyến tính hóa các biểu thức tổng; chuẩn hóa dữ liệu để cải thiện ổn định số; với bài toán trong [Problem.md](Problem.md), có thể dùng biến nhị phân gán cụm và hàm mục tiêu tổng khoảng cách.

**Kỹ thuật phi tuyến thường gặp.**
- Trị tuyệt đối: $|x|$ được tuyến tính hóa bằng biến phụ $t$ với $t\ge x$, $t\ge -x$.
- Max/min: $t=\max(x,y)$ mô hình bằng $t\ge x$, $t\ge y$, rồi tối ưu hóa $t$ phù hợp.
- Tích biến liên tục và nhị phân: dùng biến phụ và big-$M$ hoặc convex hull formulation.

**OR-Tools thể hiện thế nào.** Với LP thuần, dùng `pywraplp.Solver.CreateSolver("GLOP")` hoặc `ModelBuilder`; thêm ràng buộc bằng `AddLinearConstraint`/`Objective` rồi giải bằng `Solve()`. Khi bài toán có logic đơn giản, có thể chuyển sang `CP-SAT` để dùng chung pipeline mô hình hóa, nhưng phần lõi LP vẫn nên giữ ở dạng tuyến tính chặt.

**Mã giả ứng dụng: Transportation problem.**
```text
input: supply[i], demand[j], cost[i][j]
create variables x[i][j] >= 0
minimize sum(cost[i][j] * x[i][j])
for each i: sum_j x[i][j] <= supply[i]
for each j: sum_i x[i][j] >= demand[j]
solve LP
return flows x[i][j]
```

**Mã giả ứng dụng: Diet/blending.**
```text
input: ingredients i with nutrient a[k][i], cost c[i], bounds lb[k], ub[k]
create continuous variables x[i] >= 0
minimize sum(c[i] * x[i])
for each nutrient k:
  lb[k] <= sum(a[k][i] * x[i]) <= ub[k]
normalize if needed: sum(x[i]) = 1 or target mass = constant
solve LP
return recipe proportions x[i]
```

**Ví dụ OR-Tools.** Ví dụ [examples/java/LinearProgramming.java](or-tools/examples/java/LinearProgramming.java) tạo 3 biến liên tục không âm, thêm 3 ràng buộc tuyến tính và tối đa hóa $10x_1+6x_2+4x_3$. Mô hình ở đây đúng kiểu LP chuẩn: biến quyết định liên tục, ràng buộc dạng tổng trọng số, và objective tuyến tính. Đây là mẫu rất gần với các bài toán blending và product mix.

**Diễn giải mô hình hóa.**
- `makeNumVar(0, +inf)` biểu diễn biến liên tục không âm.
- `makeConstraint(-inf, rhs)` biểu diễn ràng buộc dạng $\le$.
- `objective.setCoefficient(...)` tạo hàm mục tiêu tuyến tính.
- `solve()` trả về nghiệm tối ưu của relaxation lồi.

```text
Input: LP chuẩn
while còn cột vào có reduced cost cải thiện:
  chọn biến vào cơ sở
  chọn biến ra cơ sở bằng ratio test
  pivot
return nghiệm cơ sở tối ưu
```

## Chương 2. Integer Linear Programming

Quy hoạch tuyến tính nguyên (ILP/MIP) thêm điều kiện $x_i \in \mathbb{Z}$ cho một số hoặc toàn bộ biến:
$$
\max c^Tx \quad \text{s.t. } Ax \le b,\; x \in \mathbb{Z}^p \times \mathbb{R}^{n-p}.
$$
Bài toán này nói chung là NP-khó, nên các bộ giải thực tế dùng nhánh-cận, cắt mặt phẳng và heuristic tìm nghiệm tốt sớm.

**Chứng minh phác thảo cho branch and bound.** Mỗi nút của cây tương ứng với một miền con. Cận trên của nút được suy ra từ bài toán thư giãn LP. Nếu cận trên không vượt nghiệm hiện tại tốt nhất thì toàn bộ miền con bị loại mà không mất nghiệm tối ưu; nếu mọi biến nguyên thì ta có nghiệm hợp lệ. Do cây phân hoạch toàn bộ miền nghiệm nguyên, thuật toán là đúng.

**Ứng dụng.** Knapsack, assignment, scheduling, facility location, TSP, set cover. Trong OR-Tools, `SCIP`, `CBC`, `CPLEX`, `Gurobi` và `CP-SAT` đều có thể xử lý MIP; `or_tools/lp.py` cho thấy cùng một bài toán phân cụm có thể được đưa vào MIP.

**Định lý, bổ đề.**
- Nếu bài toán LP thư giãn đã không khả thi thì bài toán nguyên cũng không khả thi.
- Tính đúng của branch and bound dựa trên cận trên/cận dưới hợp lệ và việc phân hoạch đầy đủ miền nghiệm nguyên.
- Bổ đề cắt mặt phẳng: nếu một bất đẳng thức loại bỏ nghiệm phân số nhưng giữ lại mọi nghiệm nguyên thì nó là một cut hợp lệ.

**Bài toán nổi tiếng.**
- Knapsack 0-1: chọn tập vật phẩm tối đa giá trị dưới giới hạn trọng lượng.
- Set covering / set partitioning: chọn các tập con để phủ hoặc phân hoạch tập phần tử.
- Traveling Salesman Problem: dùng ràng buộc subtour elimination, MTZ hoặc cut-based formulation.

**Metadata giải thuật.**
- Tính toàn cục: đúng toàn cục khi search cây được duyệt đủ hoặc cắt hợp lệ.
- Độ phức tạp: NP-khó nói chung.
- Hiệu năng thực tế: phụ thuộc rất mạnh vào relaxation, cut generation, branching rule và heuristic khởi tạo.

**Kỹ thuật mô hình hóa.** Dùng biến nhị phân cho chọn/không chọn; linearization cho tích nhị phân $z=xy$ bằng
$$
z\le x,\quad z\le y,\quad z\ge x+y-1.
$$
Với ràng buộc logic, dùng indicator constraints hoặc big-$M$; với miền lớn, thêm cận chặt để tăng hiệu quả cắt nhánh.

**Big-M.** Nếu $y\in\{0,1\}$ điều khiển mệnh đề $x\le b$ khi $y=1$ và nới lỏng khi $y=0$, có thể viết $x\le b + M(1-y)$ với $M$ đủ lớn. Cần chọn $M$ nhỏ nhất có thể để tránh relaxation quá yếu.

**OR-Tools thể hiện thế nào.** Với MIP, `SCIP` và `CP-SAT` là hai lựa chọn phổ biến. Trong Python, `CpModel` cho phép tạo `BoolVar`, `IntVar`, `AddExactlyOne`, `AddBoolOr`, `OnlyEnforceIf`, `AddMultiplicationEquality`; còn `pywraplp` phù hợp khi muốn giữ mô hình tuyến tính và để solver MIP xử lý branch-and-bound.

**Mã giả ứng dụng: 0-1 knapsack.**
```text
input: value[i], weight[i], capacity
create binary x[i]
maximize sum(value[i] * x[i])
subject to sum(weight[i] * x[i]) <= capacity
solve MIP/CP-SAT
return selected items
```

**Mã giả ứng dụng: Set covering.**
```text
input: universe U, family of sets S[i], cost c[i]
create binary x[i]
minimize sum(c[i] * x[i])
for each element e in U:
  sum(x[i] for i covering e) >= 1
solve MIP/CP-SAT
return chosen sets
```

**Mã giả ứng dụng: TSP với subtour elimination.**
```text
input: distance matrix d[i][j]
create binary x[i][j] = 1 if edge i->j is used
each node has exactly one incoming and one outgoing arc
add subtour elimination or MTZ constraints
minimize sum(d[i][j] * x[i][j])
solve MIP/CP-SAT
```

**Mã giả ứng dụng: TSP với MTZ.**
```text
input: n cities, distance matrix d
create binary x[i][j] for i != j
create order variables u[i]
each city has one incoming and one outgoing arc
u[i] - u[j] + n * x[i][j] <= n - 1 for i,j > 0
minimize total tour cost
solve MIP
```

**Ví dụ OR-Tools.** Ví dụ [examples/java/IntegerProgramming.java](or-tools/examples/java/IntegerProgramming.java) minh họa MIP rất nhỏ: hai biến nguyên không âm, một bất đẳng thức tuyến tính và hàm mục tiêu minimization. Dù bài toán đơn giản, cấu trúc của nó là đúng mẫu cho knapsack, assignment và nhiều mô hình nguyên khác: biến nguyên, objective tuyến tính, ràng buộc tuyến tính, rồi để solver branch-and-bound xử lý.

**Diễn giải mô hình hóa.**
- `makeIntVar(0, +inf)` khóa miền biến thành số nguyên không âm.
- Ràng buộc `3 x1 + 2 x2 >= 17` là một cận tuyến tính trực tiếp, không cần big-M vì bản thân mô hình đã tuyến tính.
- Solver backend có thể là SCIP/CBC/GLPK/SAT/XPRESS; cùng một mô hình nhưng chiến lược search khác nhau.

**Ví dụ OR-Tools cho lựa chọn nguyên kinh điển.** [examples/contrib/KnapsackMIP.java](or-tools/examples/contrib/KnapsackMIP.java) và [examples/contrib/DietMIP.java](or-tools/examples/contrib/DietMIP.java) là hai mẫu tốt cho bài toán chọn vật phẩm và phối trộn: biến nhị phân/biến liên tục, tổng trọng số hoặc dinh dưỡng, và objective tối ưu chi phí hay lợi ích.

```text
solve LP relaxation
if nghiệm nguyên: cập nhật best
else:
  chọn biến phân số
  branch thành 2 miền con
  cắt miền con có bound kém
```

## Chương 3. Constraint Programming

Quy hoạch ràng buộc (CP) biểu diễn bài toán bằng biến, miền giá trị và tập ràng buộc. Bộ giải không tối ưu trực tiếp trên ma trận như LP mà dựa vào propagation để thu hẹp miền, rồi dùng search có kiểm soát để tìm nghiệm.

**Chứng minh phác thảo.** Propagation phải sound: mọi giá trị bị loại đều không thể thuộc một nghiệm hợp lệ. Nếu search duyệt hết cây gán và propagation không loại nhầm giá trị, thì khi có nghiệm hợp lệ nó sẽ được tìm thấy; do đó CP kết hợp soundness của propagation và completeness của backtracking.

**Ứng dụng.** Lập lịch, timetabling, routing, phân công, bài toán đồ thị. OR-Tools khuyến nghị dùng CP-SAT cho hầu hết bài toán CP hiện đại; `or_tools/cpsat_sol.py` là ví dụ trực tiếp cho bài toán phân cụm có ràng buộc connectivity và balance.

**Định lý, bổ đề.**
- Soundness của propagation: mọi giá trị bị loại đều không nằm trong bất kỳ nghiệm hợp lệ nào.
- Completeness của backtracking search: nếu duyệt đầy đủ và propagation sound thì mọi nghiệm khả thi sẽ được tìm thấy.
- Bổ đề domain consistency: một ràng buộc mạnh hơn khi mọi giá trị trong miền còn lại đều tham gia ít nhất một nghiệm mở rộng.

**Bài toán nổi tiếng.**
- Sudoku và Latin square: điển hình cho `AllDifferent`.
- Job-shop scheduling: mô hình bằng interval variables và `NoOverlap`/`Cumulative`.
- Graph coloring và routing: dùng ràng buộc đồ thị, circuit và channeling.

**Metadata giải thuật.**
- Tính toàn cục: CP có thể tìm nghiệm tối ưu toàn cục nếu search đầy đủ; còn khi dùng heuristic thuần thì chỉ có tính thực dụng.
- Độ phức tạp: nói chung NP-khó vì search có thể là mũ.
- Sức mạnh chính: propagation + symmetry breaking thường làm giảm search space rất mạnh trên bài toán cấu trúc tốt.

**Kỹ thuật mô hình hóa.** Ưu tiên global constraints như `AllDifferent`, `Circuit`, `NoOverlap`, `Cumulative`; dùng channeling để nối nhiều góc nhìn của cùng biến; khai thác symmetry breaking để giảm tìm kiếm.

**Kỹ thuật phi tuyến thường gặp.**
- Trị tuyệt đối, max/min, dấu logic: dùng biến nhị phân và reification.
- Tích nhị phân: dùng constraint hỗ trợ Boolean hoặc linearization khi chuyển sang CP-SAT.
- Điều kiện if-then-else: dùng implication và ràng buộc reified.

**OR-Tools thể hiện thế nào.** Trong `cp_model`, các mảnh mô hình quan trọng là `NewIntVar`, `NewBoolVar`, `AddAllDifferent`, `AddCircuit`, `AddNoOverlap`, `AddCumulative`, `OnlyEnforceIf`, `AddImplication`, `AddAllowedAssignments`. Với bài toán có phần tuyến tính và phần logic, CP-SAT là lựa chọn mặc định tốt hơn CP cổ điển vì nó kết hợp propagation, SAT và linear relaxation.

**Mã giả ứng dụng: Sudoku.**
```text
input: bảng 9x9
create IntVar cell[r][c] in 1..9
add AllDifferent on each row, column, and 3x3 block
fix given clues
solve CP-SAT
return completed grid
```

**Mã giả ứng dụng: Graph coloring.**
```text
input: graph G = (V, E), number of colors K
create IntVar color[v] in 1..K for each vertex
for each edge (u, v): add color[u] != color[v]
optionally minimize K using binary activation variables
solve CP-SAT
return coloring
```

**Ví dụ OR-Tools.** [or-tools/ortools/sat/samples/NQueensSat.cs](or-tools/ortools/sat/samples/NQueensSat.cs) là ví dụ CP-SAT kinh điển: mỗi cột là một biến nguyên biểu diễn hàng đặt hậu, `AddAllDifferent` đảm bảo không hai hậu cùng hàng, và hai dãy affine `queen[i] + i`, `queen[i] - i` được dùng với `AddAllDifferent` để loại bỏ xung đột đường chéo. Đây là mẫu rất rõ của cách CP-SAT xử lý ràng buộc tổ hợp.

**Diễn giải mô hình hóa.**
- Biến `queens[i]` là vị trí hàng của hậu ở cột `i`.
- `AddAllDifferent(queens)` mã hóa ràng buộc mọi hàng khác nhau.
- `AddAllDifferent(diag1)`, `AddAllDifferent(diag2)` biến điều kiện đường chéo thành ràng buộc global.

**Ví dụ CP-SAT khác.** [or-tools/ortools/sat/samples/MinimalJobshopSat.cs](or-tools/ortools/sat/samples/MinimalJobshopSat.cs) và [or-tools/ortools/sat/samples/ScheduleRequestsSat.cs](or-tools/ortools/sat/samples/ScheduleRequestsSat.cs) thể hiện mô hình job-shop: mỗi task là một interval variable, các task trên cùng máy dùng `AddNoOverlap`, và các task trong cùng job được nối bởi ràng buộc precedence. Mục tiêu là minimize makespan qua `AddMaxEquality`.

**Mã giả ứng dụng: Job-shop scheduling.**
```text
input: tasks, machines, duration
create interval variables for each task
for each machine: AddNoOverlap(tasks on machine)
for each job: add precedence constraints between consecutive tasks
minimize makespan
solve CP-SAT
```

**Mã giả ứng dụng: Routing with time windows.**
```text
input: depot, customers, travel times, service times, time windows
create routing model and distance/time callbacks
add capacity and time dimensions
for each customer: enforce time window bounds
choose first solution strategy and local search metaheuristic
solve
return routes and arrival times
```

**Ví dụ OR-Tools.** [examples/java/CapacitatedVehicleRoutingProblemWithTimeWindows.java](or-tools/examples/java/CapacitatedVehicleRoutingProblemWithTimeWindows.java) là mẫu điển hình cho routing: dữ liệu gồm vị trí khách hàng, demand, time window, penalty và fleet. Model tạo `RoutingIndexManager`, `RoutingModel`, sau đó thêm dimensions cho thời gian và tải, rồi gắn callback Manhattan distance làm chi phí di chuyển. Đây là cách OR-Tools mô hình hóa VRP thực tế: callback cho chi phí, dimensions cho ràng buộc, và penalty cho bỏ qua khách hàng.

**Diễn giải mô hình hóa.**
- Callback transit biến khoảng cách thành chi phí cạnh.
- `addDimension(...)` tạo ràng buộc cộng dồn cho thời gian và capacity.
- Penalty cho dropped order cho phép bài toán luôn có nghiệm khả thi gần đúng.

```text
propagate(ràng buộc)
if mọi miền đơn:
  kiểm tra nghiệm
else:
  chọn biến tốt nhất
  thử từng giá trị theo thứ tự heuristic
```

## Chương 4. Modelling

Phần modelling là cầu nối giữa bài toán thực tế và bộ giải. Một mô hình tốt thường gồm 4 lớp: biến quyết định, ràng buộc bắt buộc, hàm mục tiêu, và kỹ thuật tuyến tính hóa/phụ trợ. Với bài toán trong [Problem.md](Problem.md), mô hình tự nhiên là biến $x_{j,i}$ cho BU $i$ thuộc cụm $j$, biến $c_{j,i}$ cho tâm cụm, thêm ràng buộc mỗi BU thuộc đúng một cụm, cân bằng tải và liên thông.

**Nguyên tắc mô hình hóa.** Mọi phát biểu nghiệp vụ cần được chuyển thành một trong ba dạng: bất đẳng thức tuyến tính, ràng buộc logic rời rạc, hoặc ràng buộc toàn cục. Công thức càng ngắn gọn, bộ giải càng dễ suy luận.

**Định lý, bổ đề.**
- Bổ đề tuyến tính hóa: nhiều biểu thức phi tuyến trong mô hình tối ưu có thể đưa về dạng tuyến tính bằng biến phụ và ràng buộc bao hàm.
- Bổ đề channeling: hai biểu diễn khác nhau của cùng một thực thể có thể đồng bộ hóa bằng cặp ràng buộc suy diễn hai chiều.

**Bài toán nổi tiếng.**
- Facility location: biến mở cơ sở và gán khách hàng.
- Balanced clustering: bài toán trong [Problem.md](Problem.md).
- Vehicle routing with time windows: bài toán chuẩn trong routing.

**Metadata giải thuật.**
- Modeling không phải là một giải thuật tối ưu riêng mà là lớp thiết kế; chất lượng mô hình quyết định mạnh đến tốc độ solver.
- Mô hình tốt thường chặt hơn (stronger relaxation), ít đối xứng hơn và có ít biến phụ dư thừa.

**Kỹ thuật mô hình hóa thường dùng.**
- Biến phụ để tuyến tính hóa max/min, trị tuyệt đối, tích nhị phân.
- Cận dưới/cận trên chặt để giảm không gian tìm kiếm.
- Tách cấu trúc đối xứng giữa các cụm/xe/ca làm việc.
- Dùng relaxation để lấy cận và kiểm tra khả thi sớm.

**Big-M và các biến thể.**
- Dùng khi cần kích hoạt/vô hiệu hóa ràng buộc theo biến nhị phân.
- Nếu có thể, thay bằng indicator constraint hoặc formulation mạnh hơn để tránh chọn M quá lớn.
- Với liên kết logic phức tạp, ưu tiên nhiều bất đẳng thức chặt thay vì một big-M yếu.

**OR-Tools thể hiện thế nào.** Phần modelling trên OR-Tools thường là “đóng gói” nghiệp vụ vào các biến và constraint theo đúng cấu trúc solver đang dùng: `pywraplp` cho mô hình tuyến tính/MIP, `cp_model` cho mô hình logic-rời rạc, và `routing` cho các bài toán xe/định tuyến. Cùng một bài toán có thể có nhiều biểu diễn; biểu diễn tốt nhất là biểu diễn làm cho propagation hoặc relaxation mạnh nhất.

**Mã giả ứng dụng: Balanced clustering có liên thông.**
```text
input: graph G, weights o[i], m clusters, tolerance alpha
create x[j][i] = 1 if node i in cluster j
create c[j][i] = 1 if node i is center of cluster j
for each node i: sum_j x[j][i] = 1
for each cluster j: sum_i c[j][i] = 1
balance each cluster in [(1-alpha)mu, (1+alpha)mu]
enforce connectivity using tree/arborescence variables
minimize total within-cluster distance to center
solve CP-SAT or MIP
```

## Chương 5. Approximation Algorithms

Thuật toán xấp xỉ tìm nghiệm đa thức thời gian với bảo đảm gần tối ưu. Với bài toán tối đa hóa, nếu thuật toán cho nghiệm $f$ thỏa
$$
f \ge \alpha f^*,\quad 0<\alpha<1,
$$
thì ta có tỷ lệ xấp xỉ $\alpha$.

**Chứng minh phác thảo.** Tạo một bất biến hoặc so sánh cặp giữa nghiệm của thuật toán và nghiệm tối ưu. Trong greedy hoặc primal-dual, ta thường chứng minh mỗi bước “trả giá” cho một phần giá trị tối ưu, từ đó suy ra tỉ lệ toàn cục.

**Ứng dụng.** Knapsack, set cover, TSP, vertex cover. Trong slide `chap6-approximation-algorithm.pdf`, knapsack và TSP là hai ví dụ trọng tâm.

**Định lý, bổ đề.**
- Nếu thuật toán là $\alpha$-approximation cho bài toán tối đa hóa thì nghiệm trả về luôn thỏa $f\ge \alpha f^*$.
- Định lý làm tròn ngẫu nhiên/LP rounding là nền tảng cho nhiều kết quả xấp xỉ kinh điển.
- Với primal-dual, cận đối ngẫu thường được dùng để chứng minh tỷ lệ xấp xỉ.

**Bài toán nổi tiếng.**
- Vertex cover 2-approx.
- Set cover $O(\log n)$-approx.
- Metric TSP 1.5-approx bằng Christofides.

**Metadata giải thuật.**
- Tính toàn cục: không bảo đảm tối ưu nhưng có bảo đảm xấp xỉ.
- Độ phức tạp: thường đa thức thời gian.
- Điểm mạnh: có chứng minh bảo đảm chất lượng; điểm yếu: nghiệm có thể xa tối ưu nếu cấu trúc bài toán xấu.

**Kỹ thuật mô hình hóa.** Relaxation LP, làm tròn nghiệm, greedy có chứng minh, primal-dual, và chia bài toán lớn thành các bài toán con dễ xấp xỉ hơn.

**Phi tuyến và big-M.** Trong approximation, tuyến tính hóa thường dùng để tạo relaxation đủ mạnh; nếu dùng big-M, mục tiêu là giữ relaxation sát để việc làm tròn vẫn cho bảo đảm xấp xỉ tốt.

**OR-Tools thể hiện thế nào.** Với approximation, OR-Tools thường đóng vai trò hỗ trợ: giải LP relaxation bằng `linear_solver`, sinh cận từ mô hình tuyến tính, rồi làm tròn nghiệm thủ công hoặc dùng heuristic. Cách này đặc biệt hữu ích cho set cover, knapsack phân số, facility location và các bài toán mạng.

**Mã giả ứng dụng: Vertex cover 2-approx.**
```text
input: graph G = (V, E)
C = empty set
while E not empty:
  pick any edge (u, v)
  C.add(u); C.add(v)
  remove all edges incident to u or v
return C
```

**Mã giả ứng dụng: Greedy set cover.**
```text
input: universe U, sets S1..Sk, cost c[i]
C = empty
while U not covered:
  pick set i minimizing c[i] / newly_covered(i)
  add i to C
  remove covered elements from U
return C
```

**Ví dụ OR-Tools.** [examples/contrib/SetCovering.java](or-tools/examples/contrib/SetCovering.java) là ví dụ chuẩn cho set covering: biến nhị phân biểu diễn việc chọn từng tập, mỗi phần tử trong universe phải được phủ ít nhất một lần, và objective là minimize tổng chi phí. Mẫu này rất gần với các bài toán chọn trạm, chọn kho, chọn ca làm việc hoặc cover yêu cầu.

**Diễn giải mô hình hóa.**
- Mỗi tập $S_i$ tương ứng một biến nhị phân $x_i$.
- Với mỗi phần tử $e$, ràng buộc $\sum_{i:e\in S_i} x_i \ge 1$ đảm bảo phủ.
- Nếu có cost, objective là tổng trọng số các biến được chọn.

```text
relax bài toán về LP
giải LP
round nghiệm theo quy tắc có chứng minh
return nghiệm nguyên và bound
```

## Chương 6. Heuristic Methods

Heuristic nhắm đến nghiệm tốt nhanh, không đảm bảo tối ưu hay tỷ lệ xấp xỉ. Các tài liệu `chap7-heuristic.pdf` và `week11-12-heuristic.pdf` nhấn mạnh greedy, local search và neighborhood design.

**Chứng minh phác thảo.** Heuristic thường không có chứng minh tối ưu toàn cục; thay vào đó ta chứng minh tính đúng của hàm đánh giá cục bộ, hoặc chứng minh nghiệm cuối cùng là local optimum theo một neighborhood nhất định.

**Ứng dụng.** TSP, VRP, knapsack, scheduling, phân cụm. OR-Tools routing là ví dụ điển hình cho bài toán đường đi/xe, nơi heuristic khởi tạo rất quan trọng trước khi search sâu hơn.

### 6.1 Greedy

Greedy xây nghiệm bằng cách chọn bước tốt nhất cục bộ theo một tiêu chí tĩnh. Điểm mạnh là đơn giản, nhanh, dễ cài đặt; điểm yếu là dễ mắc kẹt vào quyết định tham lam ban đầu.

**Bài toán nổi tiếng.**
- Knapsack xấp xỉ bằng density.
- Set cover bằng cost per newly covered element.
- TSP bằng nearest neighbor.
- VRP bằng cheapest insertion hoặc regret insertion.

**OR-Tools thể hiện thế nào.** Trong routing, greedy thường xuất hiện dưới dạng `first_solution_strategy` như PATH_CHEAPEST_ARC, PARALLEL_CHEAPEST_INSERTION hoặc SAVINGS. Với các bài toán ngoài routing, greedy thường được dùng để sinh nghiệm khởi tạo rồi chuyển sang CP-SAT hoặc MIP để tinh chỉnh.

**Mã giả chi tiết.**
```text
input: candidate set X, evaluation score s(x)
solution = empty
while chưa hoàn tất:
  feasible_candidates = {x in X that can be added without breaking hard constraints}
  if feasible_candidates empty: break or repair
  choose x* = argmin/argmax s(x) in feasible_candidates
  add x* to solution
  update state, constraints, and candidate scores
return solution
```

**Mã giả ứng dụng: TSP với nearest neighbor.**
```text
input: distance matrix d, start node r
tour = [r]
unvisited = V \ {r}
while unvisited not empty:
  last = tour[-1]
  next = argmin_{v in unvisited} d[last][v]
  append next to tour
  remove next from unvisited
close the tour
return tour
```

### 6.2 Local Search

Local search bắt đầu từ một nghiệm khả thi rồi lặp lại việc thay đổi bằng neighborhood để giảm hàm mục tiêu. Toàn bộ sức mạnh nằm ở thiết kế neighborhood và chiến lược chọn láng giềng.

**Bài toán nổi tiếng.**
- TSP với 2-opt, 3-opt, Or-opt.
- VRP với relocate, exchange, cross-exchange, 2-opt*.
- Scheduling với swap trên thứ tự công việc.
- Clustering với swap assignment giữa các cụm.

**OR-Tools thể hiện thế nào.** Trong routing, local search là lõi của các metaheuristic như GUIDED_LOCAL_SEARCH. Ta chỉnh bằng `local_search_metaheuristic`, `time_limit`, `solution_limit`, và các dimension để ràng buộc không gian tìm kiếm. Ở mức mô hình hóa, local search thường dùng nghiệm của solver làm đầu vào và cải thiện nó bằng move thủ công hoặc built-in search.

**Mã giả chi tiết.**
```text
input: initial feasible solution x
repeat:
  neighborhood = generate_neighbors(x)
  best_neighbor = x
  for y in neighborhood:
    if y feasible and cost(y) < cost(best_neighbor):
      best_neighbor = y
  if cost(best_neighbor) < cost(x):
    x = best_neighbor
  else:
    stop
return x
```

**Mã giả ứng dụng: local search cho clustering.**
```text
input: assignment of nodes to clusters
repeat:
  consider moving one node to another cluster
  compute delta in balance and objective
  accept best feasible move that improves cost
until no improving move exists
return assignment
```

### 6.3 Hill Climbing

Leo đồi là local search với quy tắc chấp nhận rất nghiêm ngặt: chỉ nhận move cải thiện, thường là best-improvement hoặc first-improvement. Đây là biến thể dễ hiểu nhất của local search.

**Bài toán nổi tiếng.**
- TSP và layout optimization.
- Assignment problems với swap cải thiện.
- Parameter tuning và feature selection ở mức heuristic.

**OR-Tools thể hiện thế nào.** Hill climbing không phải là một chế độ riêng trong OR-Tools, nhưng nó là tinh thần của các chiến lược local search đơn giản: chỉ nhận lời giải mới nếu objective tốt hơn và giữ feasible. Với routing, có thể coi nhiều bước cải thiện cục bộ là hill climbing có hướng dẫn.

**Mã giả chi tiết.**
```text
input: initial solution x
while true:
  best_delta = 0
  best_move = none
  for each move m in neighborhood(x):
    y = apply(x, m)
    delta = cost(x) - cost(y)
    if y feasible and delta > best_delta:
      best_delta = delta
      best_move = m
  if best_move is none:
    break
  x = apply(x, best_move)
return x
```

**Mã giả ứng dụng: hill climbing cho scheduling.**
```text
input: schedule x
repeat:
  try swapping two tasks on a machine
  compute makespan or tardiness
  accept only if objective decreases
until no improving swap
return schedule
```

### 6.4 Tabu Search

Tabu search là local search có bộ nhớ: nó cho phép đi sang nghiệm xấu hơn trong ngắn hạn nhưng tránh lặp lại các bước vừa qua bằng tabu list. Nhờ đó nó thoát tốt hơn khỏi local optimum.

**Bài toán nổi tiếng.**
- TSP.
- QAP.
- VRP.
- Timetabling và scheduling.

**OR-Tools thể hiện thế nào.** Trong routing solver, `TABU_SEARCH` là một metaheuristic có sẵn. Khi dùng, OR-Tools vẫn dựa trên neighborhood moves, nhưng bộ nhớ ngắn hạn được tích hợp trong search để tránh lặp. Đây là lựa chọn tốt khi local search thuần bị mắc kẹt quá sớm.

**Mã giả chi tiết.**
```text
input: initial solution x
tabu_list = empty queue
best = x
while stop condition not met:
  candidates = all feasible neighbors of x not forbidden by aspiration
  choose y = best candidate by objective even if not improving
  move = transformation from x to y
  add move to tabu_list with tenure t
  if cost(y) < cost(best): best = y
  x = y
  decrement tabu tenures and remove expired entries
return best
```

**Mã giả ứng dụng: tabu search cho TSP.**
```text
input: tour x
tabu edges = empty
best = x
repeat:
  generate 2-opt or swap neighbors
  forbid moves that recreate tabu edges unless aspiration holds
  select the best admissible neighbor y
  update tabu memory with moved edges
  if cost(y) < cost(best): best = y
  x = y
return best
```

### 6.5 Simulated Annealing

Simulated annealing chấp nhận cả bước xấu với xác suất phụ thuộc nhiệt độ. Khi nhiệt độ cao, thuật toán khám phá rộng; khi nhiệt độ giảm, nó trở nên tham lam hơn và tập trung khai thác vùng tốt.

**Bài toán nổi tiếng.**
- TSP.
- Job-shop scheduling.
- Clustering và layout.
- Cân bằng tải hoặc thiết kế mạng với nhiều ràng buộc mềm.

**OR-Tools thể hiện thế nào.** Trong routing, `SIMULATED_ANNEALING` có thể được chọn như một local search metaheuristic. Thực tế, người dùng thường kết hợp với first solution strategy tốt để SA có nền khởi tạo đủ chất lượng trước khi “làm nguội”.

**Mã giả chi tiết.**
```text
input: initial solution x, temperature T, cooling schedule
best = x
while T > Tmin:
  y = random neighbor of x
  delta = cost(y) - cost(x)
  if delta <= 0:
    x = y
  else if random(0,1) < exp(-delta / T):
    x = y
  if cost(x) < cost(best):
    best = x
  T = cooling(T)
return best
```

**Mã giả ứng dụng: simulated annealing cho VRP.**
```text
input: feasible routes x
T = T0
repeat until T small:
  y = move randomly by relocate/swap/2-opt*
  if y feasible or repairable:
    accept using annealing rule
  update best solution seen
  T = alpha * T
return best
```

**Giải thuật nổi tiếng và bài toán điển hình.**
- Greedy construction: nearest neighbor cho TSP, cheapest insertion cho VRP, density greedy cho knapsack.
- Local search: 2-opt/3-opt cho TSP, relocate/swap cho VRP, hill climbing cho clustering.
- Tabu search: nổi bật cho TSP, QAP, scheduling, facility location.
- Simulated annealing: hay dùng cho layout, TSP, clustering và job-shop scheduling.
- Genetic algorithm: hợp cho TSP, VRP, scheduling với mã hóa theo hoán vị hoặc chromosome theo tuyến/ca làm việc.

**Mã giả ứng dụng: VRP bằng insertion + local search.**
```text
input: customers, depot, vehicle capacity
initialize empty routes
insert customers one by one using cheapest or regret insertion
apply relocate, swap, and 2-opt* moves
repair infeasibility if needed
return routes
```

**Ví dụ OR-Tools.** Các mẫu trong `routing` như [examples/java/CapacitatedVehicleRoutingProblemWithTimeWindows.java](or-tools/examples/java/CapacitatedVehicleRoutingProblemWithTimeWindows.java) và các sample VRP tương đương trong `ortools/constraint_solver/samples` cho thấy local search được xây trên nghiệm khởi tạo của routing solver. Dù đây là ví dụ routing, về bản chất nó minh họa heuristic: tạo lời giải ban đầu nhanh, rồi cải thiện bằng move cục bộ có hướng dẫn.

**Diễn giải mô hình hóa.**
- `first_solution_strategy` đóng vai trò greedy khởi tạo.
- `local_search_metaheuristic` điều khiển cải thiện lân cận.
- Dimensions và callback là cách OR-Tools biến ràng buộc thực tế thành hạ tầng tìm kiếm.

**Kỹ thuật mô hình hóa chi tiết.**
- Xác định representation: hoán vị cho TSP, chuỗi ghé thăm cho VRP, vector gán cho clustering.
- Xây hàm đánh giá tổng hợp: chi phí gốc + penalty vi phạm ràng buộc mềm.
- Chọn neighborhood theo bài toán: swap, insert, relocate, ejection chain, 2-opt, 3-opt.
- Dùng restarts, multi-start, candidate list và aspiration criteria để tránh kẹt cực trị cục bộ.

**Kỹ thuật mô hình hóa.** Xây nghiệm ban đầu bằng nearest neighbor, regret insertion hoặc greedy by score; định nghĩa neighborhood như swap, relocate, 2-opt; dùng restart và multi-start để giảm mắc kẹt.

**Phi tuyến và penalty.** Nếu mô hình gốc có ràng buộc phức tạp, heuristic thường chuyển hard constraints thành penalty trong hàm đánh giá để tìm kiếm linh hoạt hơn.

**Metadata giải thuật.**
- Tính toàn cục: không bảo đảm.
- Độ phức tạp: phụ thuộc vào kích thước neighborhood; thường thấp hơn MIP/CP đầy đủ.
- Điểm mạnh: chạy nhanh, dễ tùy biến, cho nghiệm ban đầu tốt.

```text
x = build_initial_solution()
repeat:
  N = neighborhood(x)
  x' = best_improving_neighbor(N)
  if x' tốt hơn: x = x'
until không cải thiện
return x
```

**Định lý, bổ đề.**
- Không có định lý tối ưu toàn cục nói chung cho heuristic.
- Bổ đề thực hành thường dùng là: một local search chỉ cần chứng minh mọi move cải thiện đều được xét đầy đủ trong neighborhood thì nghiệm cuối là local optimum theo neighborhood đó.

**Bài toán nổi tiếng.**
- TSP với nearest neighbor, 2-opt, 3-opt.
- Knapsack với greedy theo density.
- VRP với insertion heuristics và local improvement.

**Metadata giải thuật.**
- Tính toàn cục: không bảo đảm.
- Độ phức tạp: phụ thuộc vào kích thước neighborhood; thường thấp hơn MIP/CP đầy đủ.
- Điểm mạnh: chạy nhanh, dễ tùy biến, cho nghiệm ban đầu tốt.

**Kỹ thuật mô hình hóa chi tiết.**
- Xác định representation: hoán vị cho TSP, chuỗi ghé thăm cho VRP, vector gán cho clustering.
- Xây hàm đánh giá tổng hợp: chi phí gốc + penalty vi phạm ràng buộc mềm.
- Chọn neighborhood theo bài toán: swap, insert, relocate, ejection chain, 2-opt, 3-opt.
- Dùng restarts, multi-start, candidate list và aspiration criteria để tránh kẹt cực trị cục bộ.

**Kỹ thuật mô hình hóa.** Xây nghiệm ban đầu bằng nearest neighbor, regret insertion hoặc greedy by score; định nghĩa neighborhood như swap, relocate, 2-opt; dùng restart và multi-start để giảm mắc kẹt.

**Phi tuyến và penalty.** Nếu mô hình gốc có ràng buộc phức tạp, heuristic thường chuyển hard constraints thành penalty trong hàm đánh giá để tìm kiếm linh hoạt hơn.

```text
x = build_initial_solution()
repeat:
  N = neighborhood(x)
  x' = best_improving_neighbor(N)
  if x' tốt hơn: x = x'
until không cải thiện
```

## Chương 7. Metaheuristic Methods

Metaheuristic là lớp chiến lược điều phối heuristic nhằm cân bằng khai thác và khám phá. Tài liệu `chap8-Metaheuristic.pdf` nhấn mạnh tabu search, simulated annealing và genetic algorithm.

**Chứng minh phác thảo.** Với simulated annealing, xác suất chấp nhận bước xấu
$$
p = e^{-\Delta/T}
$$
giúp thuật toán vẫn có khả năng thoát local minimum; khi $T$ giảm dần, chiến lược chuyển sang khai thác. Tabu search dùng bộ nhớ để tránh quay vòng; GA dùng chọn lọc và lai ghép để lan truyền cấu trúc tốt.

**Ứng dụng.** VRP, scheduling, facility location, clustering lớn. Trong thực tế OR-Tools routing và CP-SAT thường được kết hợp với heuristic/metaheuristic để sinh nghiệm khởi tạo tốt hoặc tinh chỉnh nghiệm.

**Giải thuật nổi tiếng và bài toán điển hình.**
- Tabu search: TSP, vehicle routing, QAP, timetabling.
- Simulated annealing: TSP, job-shop scheduling, layout, clustering.
- Genetic algorithm: TSP, nurse rostering, flexible job-shop, partitioning.
- GRASP/ILS: facility location, routing, scheduling và các bài toán chọn tập.

**OR-Tools thể hiện thế nào.** Trong routing solver, nhiều metaheuristic đã được gói sẵn dưới tham số search. Khi bài toán không hoàn toàn là routing, CP-SAT hoặc MIP thường cung cấp nghiệm khởi tạo, còn metaheuristic đóng vai trò cải thiện nghiệm bằng neighborhood lớn và chiến lược chấp nhận linh hoạt.

**Ví dụ OR-Tools.** [examples/java/RandomTsp.java](or-tools/examples/java/RandomTsp.java) và các sample TSP/VRP trong `ortools/constraint_solver/samples` là các ví dụ rất gần với metaheuristic thực tế: một tour ban đầu được tạo nhanh, sau đó search local và metaheuristic trong routing solver sửa các đoạn đường để giảm chi phí.

**Diễn giải mô hình hóa.**
- Bài toán được mã hóa bằng một tour hoặc một tập tuyến xe.
- Các move như 2-opt, swap, relocate được routing solver khai thác như neighborhood.
- Tham số tìm kiếm thay đổi hành vi từ greedy sang tabu/annealing/guided local search.

**Mã giả ứng dụng: Tabu search cho TSP.**
```text
input: initial tour x
tabu_list = empty
best = x
repeat until stop:
  N = all allowed 2-opt or swap moves not in tabu_list
  x' = best move in N
  move = move used to get x'
  if cost(x') < cost(best): best = x'
  add move to tabu_list with tenure
  x = x'
return best
```

**Mã giả ứng dụng: Simulated annealing cho scheduling.**
```text
input: initial schedule x, temperature T
best = x
while T > Tmin:
  y = random neighbor of x
  if cost(y) < cost(x) or random() < exp(-(cost(y)-cost(x))/T):
    x = y
    if cost(x) < cost(best): best = x
  T = cooling(T)
return best
```

**Mã giả ứng dụng: Genetic algorithm cho VRP.**
```text
input: population of route encodings
evaluate fitness with distance + penalties
repeat:
  select parents
  crossover routes
  mutate by swap/relocate
  repair infeasible children
  keep elite solutions
return best individual
```

**Định lý, bổ đề.**
- Với simulated annealing, nếu lịch nhiệt thỏa điều kiện giảm đủ chậm thì có thể hội tụ về tối ưu toàn cục trong mô hình lý thuyết lý tưởng.
- Tabu search dựa trên bổ đề chống chu trình: memory ngắn hạn giúp tránh quay lại các nghiệm vừa thăm.
- GA không có bảo đảm tối ưu, nhưng có thể được phân tích qua các toán tử chọn lọc và lai ghép như một quá trình tìm kiếm ngẫu nhiên.

**Bài toán nổi tiếng.**
- TSP và VRP quy mô lớn.
- Job-shop scheduling.
- Clustering, partitioning và facility location với nhiều ràng buộc mềm.

**Metadata giải thuật.**
- Tính toàn cục: thường không bảo đảm, nhưng có thể tăng xác suất tìm nghiệm rất tốt.
- Độ phức tạp: mỗi vòng lặp thường đa thức, nhưng số vòng lặp phụ thuộc tham số và tiêu chí dừng.
- Điểm mạnh: cân bằng exploration/exploitation tốt, hợp với bài toán lớn và mô hình không lồi.

**Kỹ thuật mô hình hóa chi tiết.**
- Dùng representation đủ giàu để một move cục bộ có ý nghĩa, nhưng không quá phức tạp để đánh giá chậm.
- Tách hard constraints và soft constraints; hard constraints thường được repair, soft constraints được tính qua penalty.
- Điều khiển diversification/intensification bằng tabu tenure, lịch nhiệt, mutation rate, elitism và restart.

**Kỹ thuật mô hình hóa.** Chọn representation phù hợp; định nghĩa fitness/penalty rõ ràng; thiết kế lịch nhiệt, tabu tenure, mutation rate; thêm ràng buộc mềm qua hàm phạt thay vì hard constraints khi cần tăng tính linh hoạt.

**Phi tuyến và big-M.** Metaheuristic thường không cần big-M trực tiếp trong lõi tìm kiếm, nhưng khi lai với MILP/CP-SAT thì big-M và tuyến tính hóa vẫn rất quan trọng để đánh giá nghiệm, ràng buộc mềm và cận hóa.

```text
x = solution_khoi_tao()
while chưa dừng:
  y = sinh_láng_giềng(x)
  nếu accept(y, x, trạng thái): x = y
  cập nhật bộ nhớ / nhiệt độ / quần thể
return best_seen
```

## Các Bài Toán Trong `docs/` Và Cách Mô Hình Hóa

Các slide trong `docs/` lặp đi lặp lại một số bài toán điển hình. Mỗi bài toán có một “kiểu mô hình” đặc trưng:

- Assignment: biến nhị phân $x_{ij}$ cho biết tác vụ $i$ được gán cho máy/người $j$; ràng buộc mỗi tác vụ gán đúng một nơi, objective tối thiểu chi phí hoặc makespan. Trong OR-Tools thường dùng `AddExactlyOne` ở CP-SAT hoặc tổng tuyến tính trong MIP.
- TSP: biến cung $x_{ij}$, mỗi đỉnh có đúng một cung vào và một cung ra; thêm subtour elimination, MTZ hoặc `AddCircuit` nếu dùng CP-SAT/routing.
- VRP / routing: biến tuyến đi theo arc, dimensions cho capacity và time window, penalty cho bỏ điểm nếu cần. OR-Tools routing solver là biểu diễn tự nhiên nhất.
- Knapsack: biến nhị phân $x_i$, ràng buộc tổng trọng lượng, objective tổng giá trị. Đây là mẫu LP/MIP cơ bản nhất.
- Set cover / set partitioning: biến chọn tập, ràng buộc phủ từng phần tử, objective tổng chi phí.
- Facility location: biến mở cơ sở $y_j$ và biến gán $x_{ij}$; ràng buộc gán chỉ xảy ra nếu cơ sở mở, thường tuyến tính hóa bằng $x_{ij} \le y_j$.
- Sudoku / N-queens / graph coloring: biến nguyên miền nhỏ, dùng global constraints như `AllDifferent`, hoặc ràng buộc bất đẳng thức trên cạnh/đường chéo.
- Job-shop scheduling: interval variables, `AddNoOverlap` theo máy, precedence theo công đoạn, objective makespan.

**Mã giả khung mô hình hóa chung.**
```text
input: bài toán thực tế P
chọn biến quyết định phù hợp
viết ràng buộc bắt buộc (assignment, capacity, precedence, connectivity)
thêm ràng buộc mềm và penalty nếu cần
chọn objective
solve bằng LP/MIP/CP-SAT/routing
```

## Ràng Buộc Trên Đồ Thị

### Liên Thông

Để mô hình một tập đỉnh/cung liên thông, thường dùng một trong các cách sau:

- Flow formulation: chọn một gốc $r$, dùng biến chọn cạnh/cung $x$ và biến luồng $f$ để truyền một đơn vị “dòng” từ gốc tới các đỉnh còn lại. Liên hệ quan trọng là
  $$
  0 \le f_{uv} \le (|V|-1) x_{uv}
  $$
  để luồng chỉ đi qua cạnh/cung được chọn. Nếu không có đường đi, không thể thỏa cân bằng luồng.
- Spanning-tree formulation: nếu chọn $n$ đỉnh thì dùng đúng $n-1$ cạnh/cung và thêm ràng buộc loại chu trình.
- Cut formulation: với mọi tập con $S$ không chứa gốc, yêu cầu có ít nhất một cạnh đi ra $\delta(S)$ để tránh cô lập.
- CP-SAT/routing: trong bài toán tuyến đường, `AddCircuit` hoặc `AddMultipleCircuit` trực tiếp ngăn subtour.

Trong mô hình có hướng, $f$ là biến “dòng” còn $x$ là biến chọn cung. Hai biến này phải được nối bằng chặn trên:
$$
0 \le f_{uv} \le M x_{uv}
$$
để cung không được chọn thì không thể mang dòng. Với bài toán liên thông, conservation trên $f$ bảo đảm mọi đỉnh đều nhận được dòng từ gốc.

**Mã giả liên thông bằng flow.**
```text
input: graph G=(V,E), root r
create binary edge vars x[e]
create flow vars f[e] >= 0
for each v != r:
  sum_u f[u,v] - sum_w f[v,w] = 1
for root r:
  sum_w f[r,w] - sum_u f[u,r] = |V|-1
for each edge e:
  f[e] <= M * x[e]
solve
```

### Là Một Cây (Không Có Loop)

Một cây thường được mô hình bằng hai điều kiện: liên thông và không chu trình. Có thể thể hiện theo ba cách:

- Chọn đúng $|V|-1$ cạnh và cấm chu trình bằng subtour elimination.
- Rooted arborescence: mỗi đỉnh (trừ gốc) có đúng một cha, gốc có bậc vào bằng 0.
- MTZ order variables: gán thứ tự $u_i$ để cấm quay vòng.

**Mã giả cây có gốc.**
```text
input: graph G=(V,E), root r
create binary x[u][v] for arcs
for each v != r: sum_u x[u][v] = 1
for root r: sum_u x[u][r] = 0
add order variables u[v]
u[v] >= u[u] + 1 - M*(1 - x[u][v])
solve
```

### Đồ Thị Có Hướng

Với đồ thị có hướng, biến quyết định thường là cung $x_{uv}$ thay vì cạnh vô hướng. Các ràng buộc phổ biến là:

- In-degree/out-degree: mỗi đỉnh có số cung vào/ra đúng theo yêu cầu, ví dụ $\sum_u x_{uv}=1$ và $\sum_w x_{vw}=1$ cho một chu trình Hamilton.
- Flow conservation: tổng vào trừ tổng ra bằng nhu cầu/ràng buộc cân bằng, và biến luồng $f$ phải bị chặn bởi biến chọn cung $x$ như $0\le f_{uv}\le U x_{uv}$.
- Path/circuit constraints: dùng `AddCircuit` cho tour, hoặc `AddAllowedAssignments`/reification cho đường đi đặc biệt.

Khi cần cây có gốc hay arborescence, ta thường kết hợp arc selection với flow như sau: mỗi cung được chọn phải có thể mang dòng, và tổng dòng vào/ra ở mỗi đỉnh cho biết đỉnh đó có nằm trong thành phần nối với gốc hay không.

**Mã giả đồ thị có hướng.**
```text
input: directed graph D=(V,A)
create binary x[u][v] for arcs
create flow f[u][v] >= 0 on arcs
for each v:
  sum_u x[u][v] = indeg_target(v)
  sum_w x[v][w] = outdeg_target(v)
if connectivity needed:
  choose root r
  for each v != r:
    sum_u f[u][v] - sum_w f[v][w] = 1
  for root r:
    sum_w f[r][w] - sum_u f[u][r] = |V|-1
  for each arc (u,v):
    f[u][v] <= M * x[u][v]
add connectivity or flow constraints if needed
solve
```

**Mã giả đồ thị có hướng.**
```text
input: directed graph D=(V,A)
create binary x[u][v] for arcs
create flow f[u][v] >= 0 if connectivity needed
for each v:
  sum_u x[u][v] = indeg_target(v)
  sum_w x[v][w] = outdeg_target(v)
if connectivity needed:
  choose root r
  for each v != r:
    sum_u f[u][v] - sum_w f[v][w] = 1
  for root r:
    sum_w f[r][w] - sum_u f[u][r] = |V|-1
  for each arc (u,v):
    f[u][v] <= U * x[u][v]
add connectivity or flow constraints if needed
solve
```

### Gợi Ý Trong OR-Tools

- `pywraplp` phù hợp cho flow, assignment, facility location và các mô hình đồ thị tuyến tính.
- `cp_model` phù hợp cho N-queens, coloring, Sudoku, job-shop và các ràng buộc logic trên đồ thị.
- `routing` phù hợp cho TSP/VRP và các biến thể có thời gian, tải, penalty.

## Siêu Tham Số Trong Heuristic

Siêu tham số quyết định cách heuristic khám phá không gian nghiệm. Chúng không phải biến quyết định của bài toán mà là biến điều khiển chiến lược tìm kiếm.

Một cách viết phổ biến là dùng độ lệch chi phí của move:
$$
\Delta = cost(y) - cost(x)
$$
và hàm điểm tổng hợp
$$
score = \Delta_{obj} + \gamma \cdot penalty - \rho \cdot diversity.
$$
Ở đây $\gamma$ thường là trọng số phạt, $\rho$ là hệ số khuyến khích đa dạng hóa, $\lambda$ là penalty weight, $\eta$ là độ ngẫu nhiên, và $\tau$ thường được dùng cho tabu tenure hoặc tie-breaking tùy thuật toán.

**Ký hiệu thường dùng.**
- $\Delta$: độ thay đổi objective khi thực hiện một move, thường $\Delta = f(y)-f(x)$.
- $\gamma$: hệ số phạt hoặc hệ số tăng cường cho vi phạm ràng buộc mềm.
- $\rho$: tỷ lệ làm nguội, tỷ lệ đột biến, hoặc xác suất giữ lại cá thể tốt tùy ngữ cảnh.
- $T_0$, $T_{min}$: nhiệt độ đầu/cuối của simulated annealing.
- $k$: kích thước neighborhood, số láng giềng, hoặc số vòng nhìn trước.
- $\lambda$: trọng số cân bằng giữa cost gốc và penalty.

### Greedy

- Tie-breaking ($\theta$): cách phá hòa khi nhiều lựa chọn có cùng điểm số. Ảnh hưởng mạnh đến nghiệm khởi tạo.
- Lookahead depth ($d$ hoặc $h$): số bước nhìn trước khi chọn. Nhìn trước nhiều hơn thường tốt hơn nhưng chậm hơn.
- Penalty weight ($\lambda$): trọng số giữa chi phí gốc và vi phạm ràng buộc mềm.
- Candidate list size ($k$): chỉ xét một số ứng viên tốt nhất để giảm thời gian.
- Randomization rate ($\eta$): xác suất chọn ngẫu nhiên thay vì chọn tốt nhất.

### Local Search / Hill Climbing

- Neighborhood type ($\mathcal{N}$): swap, insert, relocate, 2-opt, 3-opt. Neighborhood càng mạnh thì có thể cho nghiệm tốt hơn nhưng đắt hơn.
- Move evaluation budget ($B$): số move được kiểm tra mỗi vòng.
- Acceptance rule: first-improvement hay best-improvement. First-improvement nhanh, best-improvement kỹ hơn.
- Step size / perturbation ($\delta$): độ lớn của move hoặc nhiễu khi cần thoát kẹt.
- Restart policy ($R$): khi kẹt local optimum thì khởi động lại từ nghiệm khác.

### Tabu Search

- Tabu tenure ($\tau$): số vòng một move bị cấm. Tenure lớn giúp tránh quay vòng nhưng có thể hạn chế khám phá.
- Aspiration criterion ($A$): cho phép phá tabu nếu move tạo nghiệm tốt nhất từ trước đến nay.
- Diversification/intensification ($\rho$, $\iota$): lúc nào cần khám phá rộng, lúc nào cần khai thác vùng tốt.
- Candidate list size ($k$): số láng giềng được xét mỗi vòng.
- Penalty update factor ($\gamma$): hệ số tăng/giảm phạt cho các thuộc tính muốn tránh/ưu tiên.

### Simulated Annealing

- Initial temperature $T_0$: nhiệt độ ban đầu càng cao thì chấp nhận bước xấu càng nhiều.
- Cooling rate $\alpha$ hoặc $\rho$: tốc độ giảm nhiệt. $\alpha$ gần 1 thì giảm chậm, dễ tìm tốt hơn nhưng lâu hơn.
- Final temperature $T_{min}$: ngưỡng dừng.
- Iterations per temperature ($L$): số move ở mỗi mức nhiệt.
- Acceptance noise scale ($\sigma$): độ lớn nhiễu trong sinh láng giềng hoặc tiêu chí chấp nhận.

### Genetic Algorithm

- Population size ($N_p$): quần thể lớn tăng đa dạng nhưng tốn chi phí đánh giá.
- Crossover rate ($p_c$): xác suất lai ghép hai cha mẹ.
- Mutation rate ($p_m$): xác suất đột biến để thoát đồng nhất sớm.
- Elitism ($e$): giữ lại một số cá thể tốt nhất qua các thế hệ.
- Selection pressure ($\sigma$): mức ưu tiên cá thể tốt trong chọn lọc.
- Diversity coefficient ($\rho$): mức khuyến khích giữ đa dạng quần thể.

### Liên Hệ Với OR-Tools

Trong routing của OR-Tools, các siêu tham số thực tế thường là `first_solution_strategy`, `local_search_metaheuristic`, `time_limit`, `solution_limit`, cùng các dimension/cost coefficient. Chúng điều khiển trực tiếp chất lượng nghiệm ban đầu, mức độ exploration, và thời gian solver được phép dùng.

## Kết luận

Chuỗi tài liệu trong `docs/` cho thấy một pipeline rất tự nhiên cho planning optimization: LP cho cận và thư giãn, ILP/CP-SAT cho mô hình ràng buộc nguyên, modelling để nối bài toán thực tế với bộ giải, approximation cho bảo đảm gần tối ưu, và heuristic/metaheuristic cho quy mô lớn hoặc yêu cầu thời gian gấp. Với bài toán trong [Problem.md](Problem.md), cách làm hiệu quả nhất thường là bắt đầu từ mô hình CP-SAT hoặc MIP, sau đó bổ sung heuristic khởi tạo để tăng chất lượng nghiệm và giảm thời gian tìm kiếm.
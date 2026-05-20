# Detailed Solutions

Tài liệu này trình bày các lời giải trong project theo cùng một cấu trúc:

```text
Mô hình hóa -> Ý tưởng -> Lời giải chi tiết -> Siêu tham số -> Nhận xét
```

Bài toán chung: có `N` ruộng, ruộng `i` có sản lượng `d_i` và chỉ được thu hoạch trong khoảng ngày `[s_i, e_i]`. Nhà máy mỗi ngày chỉ hoạt động nếu tổng sản lượng ngày đó bằng `0` hoặc nằm trong đoạn `[m, M]`. Mục tiêu là chọn và gán ngày thu hoạch cho các ruộng sao cho tổng sản lượng được thu hoạch là lớn nhất.

Nghiệm được biểu diễn bằng:

```text
x_i = ngày thu hoạch của ruộng i
x_i = -1 nếu ruộng i không được chọn
```

Với mỗi ngày `t`, gọi:

```text
load[t] = tổng d_i của các ruộng được gán vào ngày t
```

Nghiệm hợp lệ khi:

```text
x_i = -1 hoặc s_i <= x_i <= e_i
load[t] = 0 hoặc m <= load[t] <= M
```

Điểm của một nghiệm là:

```text
sum d_i với mọi ruộng i có x_i > 0
```

---

## 1. Greedy

### Mô hình hóa

Greedy xem bài toán như bài toán gán các item vào các bin theo thời gian:

- ruộng là item;
- ngày là bin;
- `d_i` vừa là trọng lượng vừa là giá trị;
- mỗi bin có capacity trên `M`;
- nếu bin được dùng thì phải đạt ngưỡng dưới `m`;
- item `i` chỉ được đặt vào các bin trong `[s_i, e_i]`.

Không có biến tối ưu toàn cục. Thuật toán xây nghiệm trực tiếp bằng mảng:

```text
assign[i] = ngày đã gán cho ruộng i, hoặc -1
loads[t] = tổng sản lượng của ngày t
```

### Ý tưởng

Greedy dựa trên ba trực giác:

1. Ruộng có cửa sổ thời gian ngắn khó xếp hơn, nên nên xử lý trước.
2. Ngày đã có tải nên được ưu tiên lấp thêm, vì như vậy dễ giữ điều kiện `load[t] >= m`.
3. Mỗi lần gán chỉ cần đảm bảo không vượt capacity `M`; các ngày yếu dưới `m` sẽ được sửa sau.

Thứ tự mặc định:

```text
1. cửa sổ ngắn hơn: e_i - s_i nhỏ hơn
2. deadline sớm hơn: e_i nhỏ hơn
3. sản lượng lớn hơn: d_i lớn hơn
```

Khi xét một ruộng, thuật toán chọn ngày khả thi có tải hiện tại lớn nhất.

### Lời giải chi tiết

Bước 1: Khởi tạo.

```text
assign[i] = -1
loads[t] = 0
```

Bước 2: Sắp xếp ruộng theo độ khó.

```text
sort fields by (e_i - s_i, e_i, -d_i)
```

Bước 3: Gán tham lam từng ruộng.

Với mỗi ruộng `i`, quét các ngày `t` từ `s_i` tới `e_i`.

Chọn ngày `best_day` sao cho:

```text
loads[t] + d_i <= M
loads[t] là lớn nhất có thể
```

Nếu tìm được, gán:

```text
assign[i] = best_day
loads[best_day] += d_i
```

Bước 4: Repair các ngày yếu.

Sau greedy có thể có ngày:

```text
0 < loads[t] < m
```

Ngày này không hợp lệ. Hàm `repair()` xử lý như sau:

1. Lấy các ruộng đang nằm trong ngày yếu.
2. Sắp xếp các ruộng đó theo `d_i` tăng dần.
3. Thử chuyển từng ruộng sang ngày khác trong cửa sổ của nó.
4. Chỉ chuyển nếu ngày đích không vượt `M` và ngày đích đang rỗng hoặc đã đủ `m`.
5. Nếu không chuyển được thì loại ruộng khỏi nghiệm.
6. Lặp đến khi ngày yếu trở thành rỗng hoặc đủ `m`.

Bước 5: Fill nghiệm.

Hàm `fill_solution()` làm hai việc:

1. Với các ngày đang hoạt động, thử nhét thêm ruộng chưa chọn nếu còn capacity.
2. Với các ngày rỗng, thử mở ngày mới bằng cách gom một nhóm ruộng sao cho tổng đạt ít nhất `m` và không vượt `M`.

### Pseudocode

```text
GREEDY(fields, m, M):
    assign <- all -1
    loads <- all 0

    sort fields by (window length, ending day, -amount)

    for field i in sorted fields:
        best_day <- feasible day with largest current load
        if best_day exists:
            assign i to best_day
            update loads

    repeat REPAIR_FILL_ROUNDS times:
        repair weak days
        fill active and empty days

    repair weak days
    return assign
```

### Siêu tham số

- `GREEDY_REPAIR_FILL_ROUNDS`: số vòng repair/fill.
- `GREEDY_ORDER_MODE`: cách sắp xếp ruộng ban đầu.

### Nhận xét

Greedy nhanh và ổn định nhất trong các heuristic hiện tại. Nó không đảm bảo tối ưu toàn cục, nhưng tạo nghiệm hợp lệ rất nhanh cho input lớn.

---

## 2. Local Search

### Mô hình hóa

Local search dùng cùng biểu diễn nghiệm với greedy:

```text
assign[i] = ngày gán cho ruộng i, hoặc -1
loads[t] = tải của ngày t
```

Nghiệm ban đầu được tạo bằng greedy. Sau đó thuật toán tìm nghiệm tốt hơn bằng các bước thay đổi nhỏ trên nghiệm hiện tại.

### Ý tưởng

Greedy có thể bỏ sót một số ruộng do quyết định sớm. Local search bắt đầu từ nghiệm greedy rồi thử cải thiện bằng cách thêm ruộng chưa chọn vào một ngày khả thi.

Lân cận của bản local search gốc là:

```text
insert một ruộng chưa chọn vào một ngày hợp lệ
```

Sau mỗi lượt insert, thuật toán repair/fill lại để giữ nghiệm hợp lệ.

### Lời giải chi tiết

Bước 1: Tạo nghiệm ban đầu bằng greedy.

```text
assign, loads = GREEDY_CONSTRUCTION()
```

Bước 2: Lặp cải thiện.

Ở mỗi vòng:

1. Sắp xếp các ruộng theo `d_i` giảm dần.
2. Bỏ qua ruộng đã được chọn.
3. Với ruộng chưa chọn, tìm ngày khả thi có tải lớn nhất.
4. Chỉ insert nếu:

```text
loads[day] + d_i <= M
```

và:

```text
ngày đó đã hoạt động hoặc d_i >= m
```

Điều kiện thứ hai tránh mở một ngày mới yếu dưới `m`.

Bước 3: Sau mỗi vòng, chạy:

```text
repair -> fill_solution -> repair
```

Bước 4: Dừng khi không còn cải thiện hoặc đạt giới hạn vòng.

### Pseudocode

```text
LOCAL_SEARCH(fields, m, M):
    assign, loads <- GREEDY(fields, m, M)

    improved <- true
    rounds <- 0

    while improved and rounds < MAX_LOCAL_SEARCH_ROUNDS:
        improved <- false
        rounds <- rounds + 1

        sort fields by -d_i

        for each unassigned field i:
            day <- best feasible day
            if day exists and (loads[day] > 0 or d_i >= m):
                assign i to day
                update loads
                improved <- true

        repair
        fill_solution
        repair

    return assign
```

### Siêu tham số

- `LS_ORIG_INITIAL_REPAIR_FILL_ROUNDS`: số vòng repair/fill để tạo nghiệm ban đầu.
- `LS_ORIG_MAX_ROUNDS`: số vòng local search tối đa.

### Nhận xét

Đây là local search đúng nghĩa nhưng lân cận khá hẹp. Nó chỉ thêm ruộng chưa chọn, không đổi ngày, không swap, không thay thế ruộng nhỏ bằng ruộng lớn. Vì vậy bản mở rộng `local_search_variants` được thêm để thử các lân cận mạnh hơn.

---

## 3. Local Search Variants

### Mô hình hóa

Bản này vẫn dùng:

```text
assign[i]
loads[t]
```

Khác biệt nằm ở tập move. Mỗi move là một phép biến đổi nghiệm hiện tại, sau đó repair/fill để đảm bảo nghiệm hợp lệ.

### Ý tưởng

Một local search tốt phụ thuộc nhiều vào lân cận. Bản gốc chỉ có insert nên khó thoát khỏi quyết định ban đầu của greedy. Các biến thể được thêm vào để thử nhiều loại thay đổi:

```text
insert   : thêm ruộng chưa chọn
relocate : đổi ngày của một ruộng đã chọn
swap     : đổi ngày giữa hai ruộng
replace  : bỏ ruộng nhỏ để nhét ruộng lớn
group    : chuyển một nhóm ruộng giữa hai ngày
```

Các move có thể chạy riêng lẻ hoặc phối hợp.

### Lời giải chi tiết

#### 3.1. Insert

Insert giống local search gốc.

Với mỗi ruộng chưa chọn:

```text
tìm ngày khả thi có loads[t] lớn nhất
```

Nếu ngày đó đang hoạt động hoặc riêng ruộng đủ mở ngày mới:

```text
assign[i] = day
loads[day] += d_i
```

#### 3.2. Relocate: đổi ngày của một ruộng đã chọn

Move này xét một ruộng đang được chọn và thử chuyển nó sang ngày khác trong cửa sổ.

Giả sử ruộng `i` đang ở ngày `a`, muốn chuyển sang ngày `b`.

Điều kiện:

```text
s_i <= b <= e_i
loads[b] + d_i <= M
loads[a] - d_i = 0 hoặc loads[a] - d_i >= m
```

Điều kiện cuối đảm bảo ngày nguồn sau khi mất ruộng vẫn hợp lệ.

Move này không trực tiếp tăng objective, nhưng có thể dồn tải sang ngày tốt hơn, tạo chỗ cho các move khác.

#### 3.3. Swap: đổi ngày giữa hai ruộng

Xét hai ruộng `i` và `j` đang được chọn.

Ruộng `i` ở ngày `a`, ruộng `j` ở ngày `b`. Swap hợp lệ nếu:

```text
s_i <= b <= e_i
s_j <= a <= e_j
```

Sau swap:

```text
load[a]' = load[a] - d_i + d_j
load[b]' = load[b] - d_j + d_i
```

Cần:

```text
load[a]' = 0 hoặc m <= load[a]' <= M
load[b]' = 0 hoặc m <= load[b]' <= M
```

Swap cũng không trực tiếp tăng objective, nhưng giúp thay đổi cấu trúc nghiệm.

#### 3.4. Replace: loại ruộng nhỏ để nhét ruộng lớn

Move này xét một ruộng chưa chọn `i` có sản lượng lớn và một ruộng đã chọn `j` có sản lượng nhỏ.

Nếu `i` có thể đặt vào ngày hiện tại của `j`, và:

```text
d_i > d_j
loads[day_j] - d_j + d_i <= M
```

thì thay:

```text
assign[j] = -1
assign[i] = day_j
```

Move này trực tiếp tăng objective thêm:

```text
d_i - d_j
```

#### 3.5. Group Move: chuyển nhóm ruộng giữa hai ngày

Move này lấy một nhóm nhỏ ruộng từ ngày nguồn `a` và thử chuyển cả nhóm sang ngày đích `b`.

Điều kiện:

```text
mọi ruộng trong nhóm đều có thể thu hoạch ở ngày b
loads[b] + total_group <= M
loads[a] - total_group = 0 hoặc >= m
```

Move này giúp giải phóng một ngày hoặc gom tải vào ngày khác.

### Pseudocode

```text
LOCAL_SEARCH_VARIANTS(fields, m, M, MOVES):
    assign, loads <- GREEDY(fields, m, M)

    for round in 1..MAX_ROUNDS:
        changed <- false

        for move in MOVES:
            if move improves or restructures solution:
                apply move
                repair
                fill_solution
                repair
                changed <- true

        if not changed:
            break

    return assign
```

### Siêu tham số

- `LS_MOVES`: danh sách move được bật.
- `LS_MAX_ROUNDS`: số vòng tối đa.
- `LS_TOP_UNASSIGNED`: số ruộng chưa chọn được xét trong insert/replace.
- `LS_TOP_ASSIGNED`: số ruộng đã chọn được xét trong relocate/swap/replace.
- `LS_GROUP_DAYS`: số ngày nguồn/đích được xét trong group move.
- `LS_GROUP_SIZE`: kích thước nhóm chuyển.

### Nhận xét

Các move mở rộng làm local search đúng nghĩa hơn bản gốc. Tuy nhiên trên bộ test hiện tại, greedy đã rất mạnh nên các move chủ yếu tăng thời gian, chưa cải thiện điểm.

---

## 4. DP: Greedy + Local Knapsack Improvement

### Mô hình hóa

File `DP/solution.py` không dùng DP toàn cục. Nó dùng:

1. Greedy để tạo nghiệm ban đầu.
2. DP knapsack cục bộ theo từng ngày để lấp capacity còn trống.

Với mỗi ngày `t`, sau greedy ta có:

```text
remaining = M - loads[t]
```

Xét các ruộng chưa chọn có thể thu hoạch ở ngày `t`.

### Ý tưởng

Bài toán toàn cục quá lớn để DP chính xác vì phải lưu trạng thái của nhiều ngày. Nhưng với một ngày cố định, bài toán lấp phần capacity còn lại giống 0/1 knapsack:

```text
chọn một tập ruộng chưa dùng
tổng d_i <= remaining
tối đa hóa tổng d_i
```

Vì trọng lượng và giá trị đều là `d_i`, DP cố gắng lấp càng đầy capacity càng tốt.

### Lời giải chi tiết

Bước 1: Tạo nghiệm greedy.

Giống lời giải greedy:

```text
sort by (window length, deadline, -amount)
assign each field to best feasible day
repair/fill
```

Bước 2: Với từng ngày `t`, tính:

```text
remaining = M - loads[t]
```

Nếu `remaining <= 0`, bỏ qua.

Bước 3: Lấy candidate:

```text
assign[i] = -1
s_i <= t <= e_i
d_i <= remaining
```

Sắp xếp candidate:

```text
(-d_i, e_i - s_i)
```

Chỉ giữ `DP_CANDIDATE_LIMIT` ruộng đầu để giảm thời gian.

Bước 4: Chạy 0/1 knapsack.

Trạng thái:

```text
dp[w] = tổng sản lượng tốt nhất có thể đạt với capacity w
```

Khởi tạo:

```text
dp[0] = 0
dp[w] = -1 nếu chưa đạt được
```

Chuyển:

```text
for each candidate i:
    for w from remaining down to d_i:
        dp[w] = max(dp[w], dp[w - d_i] + d_i)
```

Mảng `parent` lưu truy vết để biết ruộng nào được chọn.

Bước 5: Gán các ruộng DP chọn vào ngày `t`, rồi repair/fill lại.

### Pseudocode

```text
DP_LOCAL_KNAPSACK(fields, m, M):
    assign, loads <- GREEDY(fields, m, M)

    for day in all days:
        remaining <- M - loads[day]
        candidates <- unassigned fields available on day
        keep first DP_CANDIDATE_LIMIT candidates

        chosen <- KNAPSACK(candidates, remaining)

        assign chosen fields to day

    repair
    fill_solution
    repair
    return assign
```

### Siêu tham số

- `DP_INITIAL_REPAIR_FILL_ROUNDS`: số vòng repair/fill ban đầu.
- `DP_CANDIDATE_LIMIT`: số candidate tối đa cho mỗi bài toán knapsack cục bộ.

### Nhận xét

Đây là DP cải biên, không phải DP truyền thống toàn bài. Nó hiệu quả vì chỉ giải các bài toán knapsack nhỏ sau khi greedy đã tạo nền tốt.

---

## 5. Dynamic Programming Truyền Thống

### Mô hình hóa

`DP_traditional/solution.py` xây nghiệm trực tiếp theo từng ngày. Với mỗi ngày, thuật toán giải một bài toán knapsack:

```text
chọn tập ruộng chưa gán có thể thu hoạch trong ngày t
sao cho m <= tổng d_i <= M
và tổng d_i lớn nhất
```

Trạng thái DP cho một ngày:

```text
dp[w] = tổng sản lượng tốt nhất đạt được ở capacity w
```

Vì giá trị bằng trọng lượng, mục tiêu là tìm tổng gần `M` nhất nhưng ít nhất `m`.

### Ý tưởng

Thay vì mô hình hóa nhiều ngày cùng lúc, thuật toán xử lý từng ngày độc lập:

1. Với ngày `t`, chọn một nhóm ruộng tốt bằng knapsack.
2. Gán nhóm đó vào ngày `t`.
3. Các ruộng đã gán sẽ không được dùng lại.
4. Sau khi mở các ngày bằng DP, lấp thêm các ngày đang hoạt động bằng greedy.

Đây là kiểu DP truyền thống hơn vì mỗi bước dùng trạng thái capacity `0..M` rõ ràng.

### Lời giải chi tiết

Bước 1: Khởi tạo:

```text
assign[i] = -1
loads[t] = 0
```

Bước 2: Duyệt từng ngày.

Với ngày `t`, nếu ngày đó chưa có tải, lấy candidate:

```text
assign[i] = -1
s_i <= t <= e_i
d_i <= M
```

Sắp xếp candidate:

```text
(e_i, e_i - s_i, -d_i)
```

Tức ưu tiên deadline sớm, cửa sổ ngắn, sản lượng lớn.

Bước 3: Giới hạn candidate.

Chỉ giữ:

```text
DP_TRAD_MAX_CANDIDATES
```

ruộng để tránh chi phí quá lớn.

Bước 4: Chạy knapsack.

```text
dp[0] = 0
dp[w] = -1 nếu chưa đạt được
```

Với mỗi ruộng candidate `i`:

```text
for w from M down to d_i:
    if dp[w - d_i] reachable:
        dp[w] = max(dp[w], dp[w - d_i] + d_i)
```

Sau đó chọn:

```text
best w trong [m, M] có dp[w] lớn nhất
```

Truy vết `parent` để lấy các ruộng được chọn.

Bước 5: Gán nhóm ruộng vào ngày `t`.

Bước 6: Sau mỗi pass, gọi `fill_active_days()` để nhét thêm ruộng chưa chọn vào các ngày đã hoạt động nếu còn capacity.

### Pseudocode

```text
DP_TRADITIONAL(fields, m, M):
    assign <- all -1
    loads <- all 0

    repeat DP_TRAD_PASSES times:
        for day in all days:
            candidates <- unassigned fields available on day
            sort candidates by (deadline, window length, -amount)
            candidates <- first DP_TRAD_MAX_CANDIDATES

            chosen <- KNAPSACK(candidates, m, M)
            if chosen exists:
                assign chosen fields to day
                update loads

        fill_active_days

    return assign
```

### Siêu tham số

- `DP_TRAD_MAX_CANDIDATES`: số candidate tối đa cho mỗi ngày.
- `DP_TRAD_PASSES`: số pass duyệt toàn bộ ngày.

### Nhận xét

Đây là DP rõ ràng hơn về mặt tên gọi, nhưng vẫn là heuristic vì xử lý từng ngày độc lập và giới hạn candidate. DP chính xác toàn cục cho bài toán này sẽ rất lớn vì phải lưu trạng thái của nhiều ngày cùng lúc.

---

## 6. MIP

### Mô hình hóa

MIP mô hình hóa bài toán bằng biến nhị phân.

Với mỗi ruộng `i` và ngày ứng viên `t`:

```text
x[i,t] in {0,1}
```

Ý nghĩa:

```text
x[i,t] = 1 nếu ruộng i được thu hoạch vào ngày t
```

Với mỗi ngày `t`:

```text
y[t] in {0,1}
```

Ý nghĩa:

```text
y[t] = 1 nếu ngày t được mở
y[t] = 0 nếu ngày t không hoạt động
```

### Hàm mục tiêu

Tối đa hóa tổng sản lượng:

```text
maximize sum_i sum_t d_i * x[i,t]
```

### Ràng buộc

Mỗi ruộng chọn nhiều nhất một ngày:

```text
sum_t x[i,t] <= 1
```

Tải ngày:

```text
load[t] = sum_i d_i * x[i,t]
```

Capacity trên:

```text
load[t] <= M * y[t]
```

Ngưỡng dưới:

```text
load[t] >= m * y[t]
```

Hai ràng buộc này tạo logic:

```text
y[t] = 0 => load[t] = 0
y[t] = 1 => m <= load[t] <= M
```

Cửa sổ thời gian:

Biến `x[i,t]` chỉ được tạo nếu `t` là ngày ứng viên nằm trong `[s_i, e_i]`.

### Ý tưởng

MIP là mô hình tự nhiên nhất cho bài toán. Nếu tạo biến cho mọi cặp `(i,t)`, số biến có thể quá lớn. Vì vậy code dùng hàm `candidate_days()` để giảm miền ngày:

- cửa sổ ngắn: giữ toàn bộ ngày;
- cửa sổ dài: giữ ngày đầu, ngày cuối, ngày giữa và một số ngày cách đều.

Sau đó dùng solver SCIP để tìm nghiệm nguyên.

### Lời giải chi tiết

Bước 1: Tạo biến `x[i,t]` cho các ngày ứng viên.

Bước 2: Tạo biến `y[t]` cho mỗi ngày.

Bước 3: Thêm ràng buộc mỗi ruộng chọn tối đa một lần.

Bước 4: Thêm ràng buộc tải ngày:

```text
load[t] <= M * y[t]
load[t] >= m * y[t]
```

Bước 5: Tối đa hóa tổng sản lượng.

Bước 6: Chạy SCIP với time limit.

Bước 7: Nếu solver trả nghiệm feasible hoặc optimal, đọc các biến `x[i,t] = 1` và xuất nghiệm.

### Siêu tham số

- `MIP_SHORT_WINDOW_LIMIT`: cửa sổ ngắn giữ toàn bộ ngày.
- `MIP_LONG_WINDOW_DIVISOR`: mật độ lấy mẫu ngày ứng viên.
- `MIP_TIME_LIMIT_MS`: time limit của solver.
- `MIP_INTEGER_THRESHOLD`: ngưỡng đọc biến nhị phân từ nghiệm solver.

### Nhận xét

MIP đúng với tên gọi, nhưng là MIP thu gọn vì không dùng toàn bộ ngày trong cửa sổ dài. Time limit ảnh hưởng rất rõ tới điểm.

---

## 7. CP

### Mô hình hóa

CP dùng OR-Tools CP-SAT. Mô hình biến gần giống MIP:

```text
x[i,t] Boolean
y[t] Boolean
```

Trong đó:

```text
x[i,t] = 1 nếu ruộng i được thu hoạch vào ngày t
y[t] = 1 nếu ngày t hoạt động
```

### Hàm mục tiêu

```text
maximize sum_i sum_t d_i * x[i,t]
```

### Ràng buộc

Mỗi ruộng chọn nhiều nhất một ngày:

```text
sum_t x[i,t] <= 1
```

Tải ngày:

```text
load[t] = sum_i d_i * x[i,t]
```

Liên kết với biến mở ngày:

```text
load[t] <= M * y[t]
load[t] >= m * y[t]
```

Biến chỉ được tạo trên các ngày ứng viên hợp lệ, nên không cần thêm ràng buộc ngoài cửa sổ.

### Ý tưởng

CP-SAT mạnh với mô hình Boolean và ràng buộc tổ hợp. So với MIP, mô hình giống nhau nhưng solver khác:

- MIP dùng relaxation tuyến tính và branch-and-bound/branch-and-cut.
- CP-SAT dùng SAT search, propagation, integer reasoning và parallel search.

Giống MIP, CP cũng giảm số biến bằng `candidate_days()`.

### Lời giải chi tiết

Bước 1: Tạo tập ngày ứng viên cho mỗi ruộng.

Bước 2: Tạo biến Boolean `x[i,t]`.

Bước 3: Tạo biến Boolean `y[t]`.

Bước 4: Thêm ràng buộc:

```text
sum_t x[i,t] <= 1
load[t] <= M * y[t]
load[t] >= m * y[t]
```

Bước 5: Tối đa hóa tổng sản lượng.

Bước 6: Chạy CP-SAT với:

```text
max_time_in_seconds
num_search_workers
```

Bước 7: Nếu tìm được nghiệm feasible hoặc optimal, xuất các ruộng có `x[i,t] = 1`.

### Siêu tham số

- `CP_SHORT_WINDOW_LIMIT`: cửa sổ ngắn giữ toàn bộ ngày.
- `CP_LONG_WINDOW_DIVISOR`: mật độ lấy mẫu ngày ứng viên.
- `CP_MAX_TIME_SECONDS`: time limit của CP-SAT.
- `CP_NUM_SEARCH_WORKERS`: số worker song song.

### Nhận xét

CP đúng với tên gọi CP-SAT, nhưng cũng là mô hình thu gọn vì dùng candidate days. Khi time limit thấp, solver có thể chưa tìm được nghiệm đủ tốt cho mọi test; tăng time limit giúp tăng điểm.


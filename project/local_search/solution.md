# Local Search Solution

## 1. Mô hình hóa bài toán

Nghiệm được biểu diễn bởi vector:

```text
x[1], x[2], ..., x[N]
```

Trong đó:

- `x[i] = t` nếu ruộng `i` được thu hoạch vào ngày `t`.
- `x[i] = -1` nếu ruộng `i` không được chọn.

Với mỗi ngày `t`, định nghĩa:

```text
load[t] = sum d_i với mọi i có x[i] = t
```

Ràng buộc hợp lệ:

```text
s_i <= x[i] <= e_i nếu x[i] > 0
load[t] <= M
load[t] = 0 hoặc load[t] >= m
```

Hàm mục tiêu:

```text
maximize total = sum d_i của các ruộng được chọn
```

## 2. Vì sao dùng local search

Greedy tạo nghiệm nhanh, nhưng quyết định sớm có thể làm bỏ sót các ruộng lớn hoặc làm capacity ở vài ngày bị dùng chưa tốt. Local search bắt đầu từ nghiệm greedy rồi cải thiện bằng các bước nhỏ trong lân cận của nghiệm hiện tại.

Lân cận được dùng trong code là:

```text
thêm một ruộng chưa chọn vào một ngày khả thi
```

Sau mỗi lần thêm, nghiệm được sửa lại để đảm bảo mọi ngày hoạt động đều đạt ngưỡng `m`.

## 3. Thuật toán chi tiết

### Bước 1: Tạo nghiệm ban đầu

Chạy cùng phương pháp greedy:

1. Sắp xếp ruộng khó xếp trước.
2. Gán mỗi ruộng vào ngày đang có tải lớn nhất nhưng chưa vượt `M`.
3. Repair các ngày có tải dưới `m`.
4. Fill thêm các ruộng chưa chọn vào ngày đang hoạt động.

### Bước 2: Cải thiện cục bộ

Ở mỗi vòng local search:

1. Sắp xếp các ruộng theo `d_i` giảm dần.
2. Với mỗi ruộng chưa chọn, tìm ngày tốt nhất trong `[s_i, e_i]`.
3. Chỉ thêm ruộng nếu:

```text
load[day] + d_i <= M
```

và ngày đó đã hoạt động hoặc riêng ruộng đó đủ để mở ngày mới.

4. Sau một lượt thêm, chạy `repair()` để loại bỏ hoặc di chuyển các ruộng ở ngày yếu.
5. Chạy `fill_solution()` để tận dụng thêm capacity còn trống.
6. Dừng khi không còn cải thiện hoặc đạt số vòng giới hạn.

## 4. Vai trò của repair

Local search có thể tạo ngày có tải dưới `m`. Vì vậy repair là bắt buộc. Repair đảm bảo invariant cuối mỗi vòng:

```text
mọi ngày t: load[t] = 0 hoặc m <= load[t] <= M
```

Nếu một ngày yếu không thể được cứu bằng di chuyển ruộng, các ruộng ở ngày đó bị loại khỏi nghiệm.

## 5. Pseudocode

```text
LOCAL-SEARCH-SOLVE(fields, m, M):
    assign, load <- GREEDY-CONSTRUCTION(fields, m, M)
    improved <- true
    round <- 0

    while improved = true and round < MAX_ROUNDS:
        improved <- false
        round <- round + 1

        sort fields by larger d_i first

        for each field i:
            if field i is already assigned:
                continue

            best_day <- feasible day in [s_i, e_i]
                        with largest current load
                        and load[best_day] + d_i <= M

            if best_day exists and
               (best_day is already active or d_i >= m):
                assign i to best_day
                update load[best_day]
                improved <- true

        REPAIR-WEAK-DAYS(assign, load, fields, m, M)
        FILL-SOLUTION(assign, load, fields, m, M)
        REPAIR-WEAK-DAYS(assign, load, fields, m, M)

    return assign
```

```text
GREEDY-CONSTRUCTION(fields, m, M):
    run the same greedy ordering and assignment rule
    used in the Greedy solution
    repair weak days
    fill remaining capacity
    return assign, load
```

The local-search neighborhood is therefore a one-field insertion move. The repair and fill steps keep the solution feasible after each improvement round.

## 6. Độ phức tạp

Mỗi vòng local search xét tối đa `N` ruộng và quét cửa sổ ngày của từng ruộng. Nếu `W` là độ dài cửa sổ trung bình:

```text
O(rounds * N * W)
```

Số vòng được giới hạn nhỏ, nên phù hợp với test lớn.

## 7. Cách chạy

```bash
../.plan_optim/bin/python local_search/solution.py < tests/test5.txt
```

## 8. Siêu tham số

Các siêu tham số trong `local_search/solution.py`:

| Siêu tham số | Giá trị | Vị trí trong code | Ý nghĩa |
| --- | ---: | --- | --- |
| `INITIAL_REPAIR_FILL_ROUNDS` | `2` vòng | `for _ in range(2)` trước local search | Số lần chạy cặp `repair()` và `fill_solution()` để tạo nghiệm ban đầu từ greedy. |
| `MAX_LOCAL_SEARCH_ROUNDS` | `5` vòng | `while improved and rounds < 5` | Giới hạn số vòng cải thiện cục bộ. |
| `LOCAL_SEARCH_ORDER` | `-d_i` | `for f in sorted(fields, key=lambda x: -x[1])` | Trong mỗi vòng local search, xét ruộng chưa chọn theo sản lượng giảm dần. |
| `INSERTION_RULE` | Ngày active hoặc `d_i >= min_load` | `if day > 0 and (loads[day] > 0 or d >= min_load)` | Chỉ thêm ruộng vào ngày đã có tải, hoặc mở ngày mới nếu riêng ruộng đó đủ ngưỡng tối thiểu. |
| `BEST_DAY_RULE` | Chọn ngày có `load[t]` lớn nhất còn đủ chỗ | `best_day()` | Ưu tiên nhét ruộng vào ngày đang được dùng nhiều nhất nhưng không vượt capacity. |
| `GREEDY_ORDER` | `(e_i - s_i, e_i, -d_i)` | `order = sorted(fields, key=lambda x: (x[3] - x[2], x[3], -x[1]))` | Thứ tự tạo nghiệm ban đầu: cửa sổ ngắn trước, deadline sớm trước, sản lượng lớn trước. |
| `REPAIR_MEMBER_ORDER` | `d_i` tăng dần | `sorted(members, key=lambda x: x[1])` | Khi sửa ngày yếu, thử di chuyển hoặc bỏ các ruộng nhỏ trước. |
| `FILL_ORDER` | `(-d_i, e_i - s_i, e_i)` | `fill_solution()` | Thứ tự lấp ruộng chưa chọn: sản lượng lớn trước, cửa sổ ngắn trước, deadline sớm trước. |

Các tham số `min_load` và `cap` là input của bài toán, tương ứng với `m` và `M`, không phải siêu tham số.

# Greedy Solution

## 1. Mô hình hóa bài toán

Ta có `N` thửa ruộng. Với mỗi ruộng `i`:

- `d_i`: sản lượng của ruộng.
- `s_i, e_i`: khoảng ngày hợp lệ để thu hoạch.
- `x_i`: ngày được chọn để thu hoạch ruộng `i`.
- `x_i = -1` nếu ruộng `i` không được chọn.

Với mỗi ngày `t`, gọi:

```text
load[t] = tổng d_i của các ruộng có x_i = t
```

Một nghiệm hợp lệ phải thỏa:

```text
x_i = -1 hoặc s_i <= x_i <= e_i
load[t] = 0 hoặc m <= load[t] <= M
```

Mục tiêu:

```text
maximize sum d_i với mọi ruộng i được chọn
```

Bản chất bài toán giống một bài toán gán việc vào các ngày có capacity trên `M` và ngưỡng kích hoạt dưới `m`. Vì `N` và số ngày có thể tới `10000`, greedy được dùng để tạo nghiệm nhanh thay vì giải chính xác toàn cục.

## 2. Ý tưởng thuật toán

Thuật toán xây nghiệm theo từng ruộng. Trực giác chính:

- Ruộng có cửa sổ thời gian ngắn khó xếp hơn, nên được xử lý trước.
- Nếu một ngày đã có tải, thêm ruộng vào ngày đó giúp dễ đạt hoặc giữ mức `m`.
- Mỗi ngày không được vượt quá capacity `M`.

Thứ tự xét ruộng:

```text
1. cửa sổ ngắn hơn: e_i - s_i nhỏ hơn
2. deadline sớm hơn: e_i nhỏ hơn
3. sản lượng lớn hơn: d_i lớn hơn
```

Khi xét ruộng `i`, thuật toán chọn ngày `t` trong `[s_i, e_i]` sao cho:

```text
load[t] + d_i <= M
```

và `load[t]` hiện tại là lớn nhất. Nói cách khác, ta ưu tiên nhét ruộng vào ngày đang được sử dụng nhiều nhất nhưng vẫn còn capacity.

## 3. Pha sửa nghiệm

Sau pha greedy ban đầu, có thể tồn tại ngày có:

```text
0 < load[t] < m
```

Ngày như vậy không hợp lệ vì nhà máy không chạy nếu lượng sản phẩm dưới `m`. Hàm `repair()` xử lý các ngày yếu này:

1. Lấy các ruộng đang nằm trong ngày yếu.
2. Ưu tiên ruộng nhỏ trước vì dễ di chuyển hơn.
3. Thử chuyển ruộng đó sang một ngày khác trong cửa sổ của nó nếu:

```text
load[target] + d_i <= M
target đang rỗng hoặc target đã đủ m
```

4. Nếu không chuyển được, bỏ ruộng đó khỏi nghiệm.
5. Lặp cho tới khi mọi ngày đều rỗng hoặc đủ `m`.

## 4. Pha lấp đầy

Sau khi sửa nghiệm, thuật toán tiếp tục cải thiện:

- Với các ruộng chưa chọn, thử thêm vào các ngày đang hoạt động nếu còn capacity.
- Nếu còn ngày rỗng, thử mở ngày mới bằng cách gom một nhóm ruộng có thể thu hoạch trong ngày đó sao cho tổng sản lượng đạt ít nhất `m` và không vượt `M`.

Pha này giúp tránh việc greedy ban đầu bỏ phí capacity hoặc bỏ qua ngày có thể mở hợp lệ.

## 5. Pseudocode

```text
GREEDY-SOLVE(fields, m, M):
    assign[i] <- -1 for every field i
    load[t] <- 0 for every day t

    sort fields by:
        shorter window first
        earlier ending day first
        larger amount first

    for each field i in sorted fields:
        best_day <- -1
        best_load <- -1
        for each day t from s_i to e_i:
            if load[t] + d_i <= M and load[t] > best_load:
                best_day <- t
                best_load <- load[t]
        if best_day != -1:
            assign[i] <- best_day
            load[best_day] <- load[best_day] + d_i

    repeat 2 times:
        REPAIR-WEAK-DAYS(assign, load, fields, m, M)
        FILL-SOLUTION(assign, load, fields, m, M)

    REPAIR-WEAK-DAYS(assign, load, fields, m, M)
    return assign
```

```text
REPAIR-WEAK-DAYS(assign, load, fields, m, M):
    while there exists a day t with 0 < load[t] < m:
        members <- fields assigned to t
        sort members by smaller d_i first

        for each field i in members:
            moved <- false
            for each target day u from s_i to e_i:
                if u != t and load[u] + d_i <= M
                   and (load[u] = 0 or load[u] >= m):
                    move field i from t to u
                    moved <- true
                    break

            if moved = false:
                remove field i from the solution

            if load[t] = 0 or load[t] >= m:
                break

    for each day t:
        if 0 < load[t] < m:
            remove every field assigned to t
```

```text
FILL-SOLUTION(assign, load, fields, m, M):
    sort unassigned fields by larger amount first

    for each unassigned field i:
        choose active day t in [s_i, e_i]
        with maximum load[t] such that load[t] + d_i <= M
        if such day exists:
            assign i to t

    for each empty day t:
        candidates <- unassigned fields available on day t
        sort candidates by larger amount first
        chosen <- empty set
        total <- 0

        for each field i in candidates:
            if total + d_i <= M:
                add i to chosen
                total <- total + d_i
            if total >= m:
                assign all fields in chosen to day t
                break
```

## 6. Độ phức tạp

Gọi `W` là độ dài trung bình của cửa sổ `[s_i, e_i]`.

- Sắp xếp ruộng: `O(N log N)`.
- Gán greedy: xấp xỉ `O(NW)`.
- Repair/fill chạy vài vòng cố định nên vẫn giữ mức thực tế gần `O(NW + D*N)` trong đó `D` là số ngày.

Đây là heuristic, không đảm bảo tối ưu toàn cục, nhưng chạy nhanh và tạo nghiệm hợp lệ cho input lớn.

## 7. Cách chạy

```bash
../.plan_optim/bin/python greedy/solution.py < tests/test5.txt
```

## 8. Siêu tham số

Các siêu tham số trong `greedy/solution.py`:

| Siêu tham số | Giá trị | Vị trí trong code | Ý nghĩa |
| --- | ---: | --- | --- |
| `REPAIR_FILL_ROUNDS` | `2` vòng | `for _ in range(2)` | Số lần chạy cặp `repair()` và `fill_solution()` sau pha greedy ban đầu. |
| `GREEDY_ORDER` | `(e_i - s_i, e_i, -d_i)` | `order = sorted(fields, key=lambda x: (x[3] - x[2], x[3], -x[1]))` | Thứ tự xét ruộng: cửa sổ ngắn trước, deadline sớm trước, sản lượng lớn trước. |
| `BEST_DAY_RULE` | Chọn ngày có `load[t]` lớn nhất còn đủ chỗ | `best_day()` | Ưu tiên nhét ruộng vào ngày đang được dùng nhiều nhất nhưng không vượt capacity. |
| `REPAIR_MEMBER_ORDER` | `d_i` tăng dần | `sorted(members, key=lambda x: x[1])` | Khi sửa ngày yếu, thử di chuyển hoặc bỏ các ruộng nhỏ trước. |
| `FILL_ORDER` | `(-d_i, e_i - s_i, e_i)` | `fill_solution()` | Thứ tự lấp ruộng chưa chọn: sản lượng lớn trước, cửa sổ ngắn trước, deadline sớm trước. |
| `NEW_DAY_FILL_RULE` | Dừng khi `total >= min_load` | `if total >= min_load: break` | Khi mở ngày mới, gom candidate cho tới khi đạt ngưỡng tối thiểu của nhà máy. |

Các tham số `min_load` và `cap` là input của bài toán, tương ứng với `m` và `M`, không phải siêu tham số.

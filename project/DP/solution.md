# DP Solution

## 1. Mô hình hóa bài toán

Bài toán có thể nhìn như bài toán đóng gói các ruộng vào các ngày:

- Mỗi ruộng là một item có trọng lượng/giá trị `d_i`.
- Mỗi ngày là một bin có capacity `M`.
- Một bin nếu được dùng thì phải có tổng tải ít nhất `m`.
- Item `i` chỉ được đặt vào các bin `t` thỏa `s_i <= t <= e_i`.

Nghiệm:

```text
x_i = ngày thu hoạch của ruộng i, hoặc -1 nếu bỏ qua
```

Mục tiêu:

```text
maximize sum d_i của các ruộng được chọn
```

## 2. Vì sao không dùng DP toàn cục

Một DP chính xác trên toàn bộ bài toán sẽ phải lưu trạng thái tải của rất nhiều ngày hoặc trạng thái gán của nhiều ruộng. Với:

```text
N <= 10000
M <= 10000
s_i, e_i <= 10000
```

DP toàn cục là không khả thi vì số trạng thái nổ theo số ngày và capacity.

Do đó file này dùng DP cục bộ theo từng ngày để cải thiện nghiệm.

## 3. Chiến lược tổng thể

Thuật toán gồm hai pha:

1. Tạo nghiệm ban đầu bằng greedy.
2. Với từng ngày, dùng 0/1 knapsack DP để lấp capacity còn trống bằng các ruộng chưa chọn.

Sau đó chạy repair để đảm bảo mọi ngày hoạt động đạt ngưỡng `m`.

## 4. Pha greedy ban đầu

Greedy sắp xếp ruộng theo:

```text
cửa sổ ngắn hơn -> deadline sớm hơn -> sản lượng lớn hơn
```

Mỗi ruộng được đặt vào ngày trong cửa sổ có tải hiện tại lớn nhất nhưng chưa vượt `M`.

Sau đó:

- xóa hoặc sửa ngày có tải dưới `m`,
- lấp thêm các ngày đang hoạt động,
- mở ngày mới nếu có thể gom đủ sản lượng `m`.

Pha này tạo nghiệm hợp lệ trước khi DP cải thiện.

## 5. DP lấp capacity từng ngày

Với mỗi ngày `t`, gọi:

```text
remaining = M - load[t]
```

Xét các ruộng chưa chọn và có thể thu hoạch vào ngày `t`:

```text
candidate = { i | x_i = -1 và s_i <= t <= e_i và d_i <= remaining }
```

Ta giải bài toán knapsack:

```text
maximize tổng d_i được thêm vào ngày t
subject to tổng d_i <= remaining
```

Vì giá trị và trọng lượng đều là `d_i`, DP chỉ cần tối đa hóa tổng trọng lượng lấp được.

Trạng thái:

```text
dp[w] = tổng sản lượng tốt nhất đạt được với capacity w
```

Chuyển:

```text
dp[w] = max(dp[w], dp[w - d_i] + d_i)
```

Mảng `parent` lưu truy vết để biết ruộng nào được chọn.

## 6. Giới hạn candidate

Nếu lấy toàn bộ ruộng chưa chọn cho mọi ngày, chi phí rất lớn. Code chỉ lấy một số candidate tốt nhất theo:

```text
sản lượng lớn trước, cửa sổ ngắn trước
```

Điều này biến DP thành heuristic thực tế, không phải DP tối ưu toàn cục.

## 7. Repair cuối

Sau khi DP thêm ruộng, có thể xuất hiện ngày mới hoặc ngày thay đổi tải. Vì vậy code chạy lại:

```text
repair -> fill -> repair
```

để đảm bảo:

```text
load[t] = 0 hoặc m <= load[t] <= M
```

## 8. Pseudocode

```text
DP-SOLVE(fields, m, M):
    assign, load <- GREEDY-CONSTRUCTION(fields, m, M)

    for each day t:
        remaining <- M - load[t]
        if remaining <= 0:
            continue

        candidates <- unassigned fields i such that:
            s_i <= t <= e_i
            d_i <= remaining

        sort candidates by:
            larger d_i first
            shorter window first

        keep only the first C candidates

        chosen <- KNAPSACK-FILL(candidates, remaining)

        for each field i in chosen:
            if i is still unassigned and load[t] + d_i <= M:
                assign i to day t
                load[t] <- load[t] + d_i

    REPAIR-WEAK-DAYS(assign, load, fields, m, M)
    FILL-SOLUTION(assign, load, fields, m, M)
    REPAIR-WEAK-DAYS(assign, load, fields, m, M)

    return assign
```

```text
KNAPSACK-FILL(candidates, capacity):
    dp[w] <- -infinity for every w from 0 to capacity
    parent[w] <- null
    dp[0] <- 0

    for each candidate field i at position pos:
        for w from capacity down to d_i:
            if dp[w - d_i] is reachable and
               dp[w - d_i] + d_i > dp[w]:
                dp[w] <- dp[w - d_i] + d_i
                parent[w] <- (w - d_i, pos)

    target <- w with maximum dp[w]
    reconstruct selected fields by following parent[target]
    return selected fields
```

This DP is local to one day. It does not solve the whole problem exactly, but it improves the current solution by filling unused daily capacity with a knapsack-style selection.

## 9. Độ phức tạp

Với mỗi ngày, DP có chi phí:

```text
O(C * M)
```

Trong đó `C` là số candidate được giữ lại cho ngày đó. Vì `C` bị giới hạn, thuật toán chạy được trên test lớn.

## 10. Cách chạy

```bash
../.plan_optim/bin/python DP/solution.py < tests/test5.txt
```

## 11. Siêu tham số

Các siêu tham số trong `DP/solution.py`:

| Siêu tham số | Giá trị | Vị trí trong code | Ý nghĩa |
| --- | ---: | --- | --- |
| `INITIAL_REPAIR_FILL_ROUNDS` | `2` vòng | `for _ in range(2)` trước pha DP | Số lần chạy cặp `repair()` và `fill_solution()` để làm sạch và lấp nghiệm greedy ban đầu. |
| `DP_CANDIDATE_LIMIT` | `160` ruộng/ngày | `candidates = ...[:160]` | Số candidate tối đa giữ lại cho knapsack DP mỗi ngày. Giảm thời gian chạy khi số ruộng chưa chọn rất lớn. |
| `DP_CANDIDATE_ORDER` | `(-d_i, e_i - s_i)` | `sorted(candidates, key=lambda x: (-x[1], x[3] - x[2]))` | Ưu tiên ruộng có sản lượng lớn và cửa sổ ngắn khi chọn candidate cho DP. |
| `GREEDY_ORDER` | `(e_i - s_i, e_i, -d_i)` | `order = sorted(fields, key=lambda x: (x[3] - x[2], x[3], -x[1]))` | Thứ tự tạo nghiệm ban đầu: cửa sổ ngắn trước, deadline sớm trước, sản lượng lớn trước. |
| `FILL_ORDER` | `(-d_i, e_i - s_i, e_i)` | `fill_solution()` | Thứ tự lấp thêm ruộng chưa chọn: sản lượng lớn trước, cửa sổ ngắn trước, deadline sớm trước. |
| `REPAIR_MEMBER_ORDER` | `d_i` tăng dần | `sorted(members, key=lambda x: x[1])` | Khi sửa ngày yếu, thử di chuyển hoặc bỏ các ruộng nhỏ trước vì dễ xếp lại hơn. |

Các tham số `min_load` và `cap` là input của bài toán, tương ứng với `m` và `M`, không phải siêu tham số.

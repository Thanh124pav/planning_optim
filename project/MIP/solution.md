# MIP Solution

## 1. Mô hình mixed-integer programming

MIP mô hình hóa trực tiếp bài toán gốc bằng biến nhị phân.

Với mỗi ruộng `i` và ngày ứng viên `t` trong `[s_i, e_i]`:

```text
x[i,t] in {0,1}
```

Ý nghĩa:

```text
x[i,t] = 1 nếu ruộng i được thu hoạch vào ngày t
x[i,t] = 0 nếu không
```

Với mỗi ngày `t`:

```text
y[t] in {0,1}
```

Ý nghĩa:

```text
y[t] = 1 nếu nhà máy hoạt động ngày t
y[t] = 0 nếu ngày t không dùng
```

## 2. Hàm mục tiêu

```text
maximize sum_i sum_t d_i * x[i,t]
```

Mục tiêu là tối đa hóa tổng sản lượng của các ruộng được thu hoạch.

## 3. Ràng buộc

### Mỗi ruộng được chọn tối đa một ngày

```text
sum_t x[i,t] <= 1       với mọi i
```

Ruộng có thể bị bỏ qua, nên ràng buộc là `<= 1`, không phải `= 1`.

### Liên kết tải ngày với biến kích hoạt

Gọi tải của ngày `t`:

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

Hai ràng buộc này ép:

- Nếu `y[t] = 0`, thì `load[t] = 0`.
- Nếu `y[t] = 1`, thì `m <= load[t] <= M`.

### Cửa sổ thời gian

Biến `x[i,t]` chỉ tồn tại với ngày hợp lệ:

```text
s_i <= t <= e_i
```

Điều này làm mô hình nhỏ hơn và tự động loại các assignment sai cửa sổ.

## 4. Giải bằng OR-Tools

Code dùng:

```python
pywraplp.Solver.CreateSolver("SCIP")
```

SCIP giải mô hình nguyên bằng branch-and-bound/branch-and-cut. Với input nhỏ hoặc vừa, MIP có thể tìm nghiệm tối ưu. Với input lớn, số biến rất nhiều nên code:

- chỉ tạo biến trên tập ngày ứng viên,
- đặt time limit,
- lấy incumbent feasible nếu solver tìm được.

## 5. Khác biệt so với LP

LP dùng `x[i,t] in [0,1]`, nên có nghiệm phân số và cần làm tròn. MIP dùng:

```text
x[i,t] in {0,1}
y[t] in {0,1}
```

Vì vậy nghiệm solver trả về đã là nghiệm nguyên hợp lệ, không cần rounding.

## 6. Đặc điểm

MIP là mô hình tự nhiên nhất cho bài toán này. Ưu điểm là ràng buộc rõ ràng và có khả năng chứng minh tối ưu nếu solver chạy đủ lâu. Nhược điểm là mô hình lớn với `N = 10000` có thể rất nặng, nên candidate days được dùng để giảm số biến.

Không có fallback sang heuristic trong file này; lời giải dùng OR-Tools MIP.

## 7. Cách chạy

```bash
../.plan_optim/bin/python MIP/solution.py < tests/test5.txt
```

## 8. Siêu tham số

Các siêu tham số trong `MIP/solution.py`:

| Siêu tham số | Giá trị | Vị trí trong code | Ý nghĩa |
| --- | ---: | --- | --- |
| `SHORT_WINDOW_LIMIT` | `12` | `if length <= 12` trong `candidate_days()` | Cửa sổ thu hoạch có độ dài không quá 12 ngày sẽ giữ toàn bộ ngày ứng viên. |
| `LONG_WINDOW_DIVISOR` | `6` | `step = max(1, length // 6)` | Với cửa sổ dài, khoảng cách lấy mẫu ngày ứng viên xấp xỉ bằng `length / 6`. |
| `MANDATORY_CANDIDATE_DAYS` | `s`, `e`, `(s + e) // 2` | `candidate_days()` | Luôn giữ ngày đầu, ngày cuối và ngày giữa của cửa sổ. |
| `MIP_SOLVER` | `SCIP` | `pywraplp.Solver.CreateSolver("SCIP")` | Solver MIP dùng để giải mô hình nguyên. |
| `TIME_LIMIT_MS` | `15000` ms | `solver.SetTimeLimit(15000)` | Giới hạn thời gian giải MIP. Hết thời gian thì lấy nghiệm feasible nếu solver có incumbent. |
| `INTEGER_THRESHOLD` | `0.5` | `if var.solution_value() > 0.5` | Ngưỡng đọc biến nhị phân từ nghiệm solver để xuất assignment. |

Các tham số `min_load` và `cap` là input của bài toán, tương ứng với `m` và `M`, không phải siêu tham số.

# CP Solution

## 1. Mô hình constraint programming

Lời giải CP dùng OR-Tools CP-SAT. Đây vẫn là mô hình biến Boolean, nhưng solver xử lý bằng constraint programming kết hợp SAT/integer optimization.

Với mỗi ruộng `i` và ngày ứng viên `t`:

```text
x[i,t] is Boolean
```

Ý nghĩa:

```text
x[i,t] = 1 nếu ruộng i được thu hoạch vào ngày t
```

Với mỗi ngày `t`:

```text
y[t] is Boolean
```

Ý nghĩa:

```text
y[t] = 1 nếu ngày t được mở
```

## 2. Hàm mục tiêu

CP-SAT tối đa hóa:

```text
sum_i sum_t d_i * x[i,t]
```

Đây là tổng sản lượng của các ruộng được chọn.

## 3. Ràng buộc

### Một ruộng không thể thu hoạch nhiều lần

```text
sum_t x[i,t] <= 1
```

Vì ruộng có thể không được chọn, dùng `<= 1`.

### Tải mỗi ngày

```text
load[t] = sum_i d_i * x[i,t]
```

Ràng buộc capacity:

```text
load[t] <= M * y[t]
```

Ràng buộc kích hoạt nhà máy:

```text
load[t] >= m * y[t]
```

Kết hợp hai ràng buộc:

- `y[t] = 0` kéo theo `load[t] = 0`.
- `y[t] = 1` kéo theo `m <= load[t] <= M`.

### Cửa sổ ngày

Biến `x[i,t]` chỉ được tạo khi `t` nằm trong `[s_i, e_i]`. Vì vậy solver không thể gán ruộng ra ngoài cửa sổ.

## 4. Giảm kích thước mô hình

CP-SAT với toàn bộ ngày có thể tạo ra quá nhiều biến Boolean. File dùng `candidate_days(s,e)`:

- cửa sổ ngắn: giữ toàn bộ ngày;
- cửa sổ dài: chọn endpoint, midpoint và một số ngày cách đều.

Đây là cách xấp xỉ để mô hình CP chạy được trên các test lớn.

## 5. Cách CP-SAT giải

CP-SAT tìm nghiệm bằng search trên các biến Boolean, kết hợp:

- propagation từ các ràng buộc tuyến tính,
- SAT search,
- branch-and-bound theo objective,
- multi-thread search với `num_search_workers = 8`.

Code đặt time limit:

```python
solver.parameters.max_time_in_seconds = 15.0
```

Nếu solver tìm được nghiệm feasible, nghiệm đó được xuất ra. Nếu không có nghiệm trong thời gian cho phép, chương trình in nghiệm rỗng hợp lệ.

## 6. So sánh với MIP

MIP và CP dùng mô hình Boolean gần giống nhau. Khác biệt nằm ở solver:

- MIP dùng SCIP qua linear solver.
- CP dùng CP-SAT, thường mạnh với mô hình Boolean và constraint combinatorial.

Trong các test hiện tại, CP-SAT tìm được nghiệm hợp lệ tốt cho cả 5 test.

Không có fallback sang greedy trong file này; lời giải dùng OR-Tools CP-SAT.

## 7. Cách chạy

```bash
../.plan_optim/bin/python CP/solution.py < tests/test5.txt
```

## 8. Siêu tham số

Các siêu tham số đang được đặt trực tiếp trong `CP/solution.py` và `CP/sol2.py`:

| Siêu tham số | Giá trị | Vị trí trong code | Ý nghĩa |
| --- | ---: | --- | --- |
| `SHORT_WINDOW_LIMIT` | `12` | `if length <= 12` trong `candidate_days()` | Cửa sổ thu hoạch có độ dài không quá 12 ngày sẽ giữ toàn bộ ngày ứng viên. |
| `LONG_WINDOW_DIVISOR` | `6` | `step = max(1, length // 6)` | Với cửa sổ dài, khoảng cách lấy mẫu ngày ứng viên xấp xỉ bằng `length / 6`. |
| `MANDATORY_CANDIDATE_DAYS` | `s`, `e`, `(s + e) // 2` | `candidate_days()` | Luôn giữ ngày đầu, ngày cuối và ngày giữa của cửa sổ. |
| `max_time_in_seconds` | `15.0` giây | `solver.parameters.max_time_in_seconds = 15.0` | Giới hạn thời gian tìm kiếm của CP-SAT. Hết thời gian thì lấy nghiệm feasible tốt nhất nếu có. |
| `num_search_workers` | `8` | `solver.parameters.num_search_workers = 8` | Số worker song song cho CP-SAT. |

Các tham số `m` và `M` không phải siêu tham số của thuật toán; chúng là dữ liệu đầu vào của bài toán.

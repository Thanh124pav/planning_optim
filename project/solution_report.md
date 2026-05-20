# Báo cáo các phương pháp giải bài toán lập kế hoạch thu hoạch

## 1. Giới thiệu bài toán

Bài toán đặt ra yêu cầu lập kế hoạch thu hoạch cho `N` thửa ruộng cùng trồng một loại nông sản. Mỗi thửa ruộng `i` có sản lượng `d_i` và chỉ có thể được thu hoạch trong khoảng thời gian từ ngày `s_i` đến ngày `e_i`. Nhà máy xử lý có công suất tối đa mỗi ngày là `M`; đồng thời, nếu tổng sản lượng đưa vào nhà máy trong một ngày nhỏ hơn `m`, nhà máy sẽ không hoạt động vì hiệu quả vận hành không đảm bảo.

Vì vậy, mỗi thửa ruộng có thể được chọn để thu hoạch hoặc bị bỏ qua. Nếu được chọn, ruộng phải được gán vào đúng một ngày nằm trong cửa sổ thời gian hợp lệ của nó. Mục tiêu của bài toán là tìm kế hoạch thu hoạch sao cho tổng sản lượng được thu hoạch là lớn nhất, trong khi mọi ngày hoạt động của nhà máy đều có tổng sản lượng nằm trong đoạn `[m, M]`.

Một nghiệm của bài toán được biểu diễn bởi vector:

```text
x_1, x_2, ..., x_N
```

Trong đó `x_i` là ngày thu hoạch của ruộng `i`, và `x_i = -1` nếu ruộng `i` không được chọn. Với mỗi ngày `t`, ta ký hiệu:

```text
load[t] = tổng sản lượng của các ruộng được gán vào ngày t
```

Một nghiệm hợp lệ phải thỏa mãn hai nhóm điều kiện. Thứ nhất, nếu ruộng `i` được chọn thì ngày thu hoạch phải nằm trong cửa sổ `[s_i, e_i]`. Thứ hai, với mỗi ngày `t`, tải của ngày đó phải bằng `0` hoặc nằm trong đoạn `[m, M]`. Điều kiện này phản ánh việc nhà máy hoặc không hoạt động, hoặc nếu hoạt động thì phải xử lý đủ sản lượng tối thiểu và không vượt quá công suất tối đa.

Do kích thước dữ liệu có thể lớn, với `N` và số ngày đều có thể lên tới `10000`, bài toán không dễ giải chính xác bằng các phương pháp vét cạn. Nhóm đã xây dựng và thử nghiệm nhiều hướng tiếp cận khác nhau, bao gồm greedy, local search, dynamic programming, mixed-integer programming và constraint programming. Các phần sau trình bày chi tiết mô hình hóa, ý tưởng và cách triển khai của từng phương pháp.

## 2. Phương pháp Greedy

Phương pháp greedy xem bài toán như một bài toán gán các ruộng vào các ngày. Mỗi ruộng được coi là một item có trọng lượng và giá trị đều bằng sản lượng `d_i`; mỗi ngày được coi là một bin có sức chứa tối đa `M`. Điểm đặc biệt của bài toán là một bin nếu được sử dụng thì phải đạt tải tối thiểu `m`, đồng thời mỗi item chỉ được đặt vào một tập bin nhất định tương ứng với cửa sổ thời gian `[s_i, e_i]`.

Ý tưởng chính của greedy là xử lý trước các ruộng khó xếp. Một ruộng có cửa sổ thời gian càng ngắn thì càng ít lựa chọn ngày thu hoạch, do đó nếu để xử lý muộn, khả năng không còn ngày phù hợp sẽ cao hơn. Vì vậy, thuật toán sắp xếp các ruộng theo thứ tự ưu tiên: cửa sổ thời gian ngắn hơn trước, ngày kết thúc sớm hơn trước, và nếu vẫn hòa thì sản lượng lớn hơn trước.

Sau khi có thứ tự xét ruộng, thuật toán gán từng ruộng vào một ngày khả thi. Với ruộng `i`, thuật toán quét các ngày từ `s_i` đến `e_i` và chọn ngày có tải hiện tại lớn nhất nhưng vẫn còn đủ capacity để chứa thêm `d_i`. Quy tắc này có ý nghĩa thực tế: nếu một ngày đã có tải, việc thêm ruộng vào ngày đó giúp ngày này dễ đạt hoặc duy trì ngưỡng tối thiểu `m`; đồng thời hạn chế việc mở quá nhiều ngày mới có tải nhỏ.

Tuy nhiên, sau pha gán tham lam ban đầu, vẫn có thể xuất hiện các ngày có tải dương nhưng nhỏ hơn `m`. Những ngày này không hợp lệ vì nhà máy không thể hoạt động với tải dưới ngưỡng tối thiểu. Do đó thuật toán có một pha sửa nghiệm, gọi là `repair`. Trong pha này, với mỗi ngày yếu, thuật toán lấy các ruộng đang được gán vào ngày đó, ưu tiên xử lý các ruộng có sản lượng nhỏ trước vì chúng dễ di chuyển hơn. Mỗi ruộng được thử chuyển sang một ngày khác trong cửa sổ hợp lệ của nó, miễn là ngày đích không vượt quá `M` và đang rỗng hoặc đã đủ ngưỡng `m`. Nếu không thể chuyển, ruộng đó bị loại khỏi nghiệm.

Sau khi sửa các ngày yếu, thuật toán tiếp tục cải thiện nghiệm bằng pha `fill`. Pha này thử đưa các ruộng chưa chọn vào những ngày đang hoạt động nếu các ngày đó còn capacity. Ngoài ra, với các ngày đang rỗng, thuật toán thử gom một nhóm ruộng chưa chọn có thể thu hoạch trong ngày đó sao cho tổng sản lượng đạt ít nhất `m` và không vượt `M`, từ đó mở thêm một ngày hoạt động hợp lệ.

Tóm lại, greedy không giải bài toán một cách tối ưu toàn cục, nhưng nó xây dựng nghiệm nhanh, hợp lệ và thường có chất lượng tốt. Đây cũng là nền tảng được nhiều phương pháp khác sử dụng để tạo nghiệm ban đầu.

## 3. Phương pháp Local Search

Local search bắt đầu từ một nghiệm ban đầu và cải thiện nghiệm đó bằng các thay đổi cục bộ. Trong project này, nghiệm ban đầu của local search được tạo bằng phương pháp greedy đã mô tả ở trên. Sau đó thuật toán tìm cách bổ sung thêm các ruộng chưa được chọn vào kế hoạch hiện tại.

Biểu diễn nghiệm của local search giống với greedy: mảng `assign[i]` lưu ngày thu hoạch của ruộng `i`, còn mảng `loads[t]` lưu tổng sản lượng của ngày `t`. Điều này giúp việc kiểm tra tính hợp lệ và cập nhật nghiệm sau mỗi thay đổi trở nên đơn giản.

Ở phiên bản local search cơ bản, lân cận của một nghiệm được định nghĩa bởi thao tác thêm một ruộng chưa chọn vào một ngày khả thi. Trong mỗi vòng lặp, thuật toán sắp xếp các ruộng theo sản lượng giảm dần để ưu tiên thử các ruộng có đóng góp lớn. Với mỗi ruộng chưa chọn, thuật toán tìm ngày tốt nhất trong cửa sổ thời gian của nó, tức ngày có tải hiện tại lớn nhất nhưng vẫn còn capacity. Ruộng chỉ được thêm vào nếu ngày đó đã đang hoạt động hoặc nếu riêng sản lượng của ruộng đủ lớn để mở một ngày mới, tức `d_i >= m`.

Sau một lượt thêm ruộng, nghiệm có thể bị thay đổi cấu trúc. Vì vậy, thuật toán chạy lại các bước `repair` và `fill` để đảm bảo mọi ngày hoạt động đều hợp lệ và tận dụng thêm capacity còn trống. Quá trình này lặp lại cho đến khi không còn cải thiện hoặc đạt số vòng tối đa.

Ưu điểm của local search là giữ được tốc độ nhanh của greedy nhưng có thêm khả năng cải thiện nghiệm. Tuy nhiên, phiên bản cơ bản chỉ sử dụng thao tác thêm ruộng, nên không thể sửa những quyết định sai đã được đưa ra ở nghiệm greedy ban đầu. Vì lý do đó, nhóm đã mở rộng local search bằng nhiều loại lân cận khác nhau.

## 4. Các biến thể mở rộng của Local Search

Để làm local search linh hoạt hơn, nhóm bổ sung nhiều phép biến đổi nghiệm khác nhau. Mục tiêu của các biến thể này là cho phép thuật toán không chỉ thêm ruộng mới, mà còn có thể tái cấu trúc nghiệm hiện tại.

Biến thể thứ nhất là đổi ngày của một ruộng đã chọn, còn gọi là `relocate`. Với một ruộng đang được gán vào ngày `a`, thuật toán thử chuyển nó sang một ngày khác `b` nằm trong cửa sổ thời gian hợp lệ. Việc chuyển chỉ được chấp nhận nếu ngày đích không vượt quá capacity và ngày nguồn sau khi mất ruộng vẫn rỗng hoặc còn đạt ngưỡng tối thiểu `m`. Phép biến đổi này không trực tiếp làm tăng tổng sản lượng, nhưng nó có thể tạo ra khoảng trống ở một số ngày để các bước sau thêm được ruộng mới.

Biến thể thứ hai là hoán đổi hai ruộng, gọi là `swap`. Giả sử ruộng `i` đang ở ngày `a` và ruộng `j` đang ở ngày `b`. Thuật toán thử đổi ngày của hai ruộng này cho nhau. Phép đổi chỉ hợp lệ nếu ruộng `i` có thể thu hoạch ở ngày `b`, ruộng `j` có thể thu hoạch ở ngày `a`, và tải của cả hai ngày sau khi đổi vẫn nằm trong giới hạn hợp lệ. Tương tự relocate, swap chủ yếu giúp thay đổi cấu trúc nghiệm để thoát khỏi một số lựa chọn cục bộ kém.

Biến thể thứ ba là loại một ruộng nhỏ để nhét một ruộng lớn hơn, gọi là `replace`. Thuật toán xét một ruộng chưa chọn có sản lượng lớn và một ruộng đã chọn có sản lượng nhỏ hơn. Nếu ruộng lớn có thể được đặt vào ngày hiện tại của ruộng nhỏ và tải của ngày đó sau khi thay thế không vượt quá `M`, thuật toán loại ruộng nhỏ ra khỏi nghiệm và đưa ruộng lớn vào. Đây là phép biến đổi có khả năng làm tăng trực tiếp giá trị mục tiêu, với mức tăng bằng `d_i - d_j`.

Biến thể thứ tư là chuyển cả một nhóm ruộng giữa hai ngày, gọi là `group move`. Thay vì di chuyển một ruộng đơn lẻ, thuật toán chọn một nhóm nhỏ ruộng từ ngày nguồn và thử chuyển toàn bộ nhóm sang ngày đích. Điều kiện là mọi ruộng trong nhóm đều có thể thu hoạch vào ngày đích, ngày đích còn đủ capacity, và ngày nguồn sau khi mất nhóm vẫn hợp lệ. Phép biến đổi này hữu ích khi cần gom tải vào một ngày và giải phóng một ngày khác.

Các biến thể trên có thể được chạy riêng lẻ hoặc kết hợp. Khi chạy kết hợp, thuật toán lần lượt thử các move như insert, relocate, swap, replace và group trong mỗi vòng local search. Sau mỗi move thành công, thuật toán lại gọi `repair` và `fill` để đưa nghiệm về trạng thái hợp lệ và tận dụng thêm cơ hội cải thiện.

Về mặt bản chất, các biến thể này làm local search trở nên đúng nghĩa hơn, vì không gian lân cận rộng hơn và thuật toán có khả năng chỉnh sửa các quyết định trước đó. Tuy nhiên, trên bộ test hiện tại, greedy đã tạo nghiệm rất tốt, nên các move mở rộng chủ yếu làm tăng thời gian chạy mà chưa tạo ra cải thiện đáng kể về điểm.

## 5. Phương pháp DP cải biên: Greedy kết hợp Knapsack cục bộ

Phương pháp trong folder `DP` không phải là dynamic programming toàn cục cho toàn bộ bài toán. Thay vào đó, đây là một phương pháp lai giữa greedy và dynamic programming cục bộ. Thuật toán trước tiên tạo một nghiệm ban đầu bằng greedy, sau đó dùng bài toán knapsack 0/1 để cải thiện từng ngày riêng lẻ.

Sau khi có nghiệm greedy, với mỗi ngày `t`, ta biết tải hiện tại `loads[t]`. Nếu ngày đó còn capacity, lượng capacity còn lại là:

```text
remaining = M - loads[t]
```

Thuật toán xét các ruộng chưa được chọn, có thể thu hoạch vào ngày `t`, và có sản lượng không vượt quá `remaining`. Từ các ruộng này, bài toán con cần giải là chọn một tập ruộng sao cho tổng sản lượng không vượt quá `remaining` và càng lớn càng tốt. Đây chính là dạng knapsack 0/1, trong đó trọng lượng và giá trị của mỗi item đều bằng `d_i`.

Trạng thái DP được định nghĩa theo capacity:

```text
dp[w] = tổng sản lượng tốt nhất có thể đạt được với capacity w
```

Ban đầu `dp[0] = 0`, các trạng thái khác chưa đạt được. Với mỗi ruộng candidate có sản lượng `d_i`, thuật toán duyệt `w` giảm dần từ `remaining` về `d_i` và cập nhật:

```text
dp[w] = max(dp[w], dp[w - d_i] + d_i)
```

Duyệt giảm dần giúp đảm bảo mỗi ruộng chỉ được chọn tối đa một lần. Sau khi hoàn thành DP, thuật toán chọn trạng thái có giá trị tốt nhất và truy vết để biết các ruộng được chọn. Các ruộng này được gán vào ngày `t`, sau đó thuật toán tiếp tục với ngày tiếp theo.

Để kiểm soát thời gian chạy, thuật toán không đưa toàn bộ ruộng chưa chọn vào DP của mỗi ngày. Thay vào đó, các candidate được sắp xếp theo sản lượng lớn trước và cửa sổ ngắn trước, rồi chỉ giữ một số lượng giới hạn. Siêu tham số quan trọng ở đây là `DP_CANDIDATE_LIMIT`.

Phương pháp này có ưu điểm là tận dụng được sức mạnh của DP trong các bài toán con nhỏ, đồng thời tránh được sự bùng nổ trạng thái nếu cố gắng giải toàn cục. Tuy nhiên, vì mỗi bài toán DP chỉ nhìn một ngày tại một thời điểm và phụ thuộc vào nghiệm greedy ban đầu, phương pháp này vẫn là heuristic chứ không đảm bảo tối ưu toàn cục.

## 6. Dynamic Programming truyền thống theo từng ngày

Để có một phiên bản dynamic programming rõ ràng hơn, nhóm xây dựng thêm phương pháp `DP_traditional`. Phương pháp này không bắt đầu từ nghiệm greedy, mà trực tiếp duyệt qua các ngày và dùng knapsack để chọn nhóm ruộng mở ngày đó.

Với mỗi ngày `t`, thuật toán xét các ruộng chưa được gán và có thể thu hoạch trong ngày này. Bài toán con là chọn một tập ruộng sao cho tổng sản lượng nằm trong đoạn `[m, M]` và càng lớn càng tốt. Đây là bài toán knapsack với capacity `M` và yêu cầu nghiệm cuối phải đạt ít nhất `m`.

Trạng thái DP được định nghĩa như sau:

```text
dp[w] = tổng sản lượng tốt nhất đạt được ở mức capacity w
```

Do giá trị và trọng lượng đều bằng sản lượng, mục tiêu là tìm tổng `w` gần `M` nhất nhưng không nhỏ hơn `m`. Sau khi chạy DP, thuật toán chọn trạng thái tốt nhất trong đoạn `[m, M]`, truy vết các ruộng đã chọn và gán chúng vào ngày hiện tại.

Để giảm chi phí tính toán, trước khi chạy DP cho một ngày, thuật toán sắp xếp candidate theo deadline sớm, cửa sổ ngắn và sản lượng lớn, sau đó chỉ lấy một số lượng giới hạn. Siêu tham số `DP_TRAD_MAX_CANDIDATES` quyết định số ruộng tối đa được đưa vào DP cho mỗi ngày. Ngoài ra, thuật toán có thể duyệt nhiều pass qua toàn bộ các ngày, được điều khiển bởi siêu tham số `DP_TRAD_PASSES`.

Sau khi các ngày được mở bằng DP, thuật toán chạy thêm một bước lấp đầy các ngày đang hoạt động bằng các ruộng chưa chọn nếu còn capacity. Điều này giúp cải thiện tổng sản lượng mà vẫn giữ nghiệm hợp lệ.

So với phương pháp DP cải biên, phiên bản này thể hiện rõ hơn tinh thần dynamic programming truyền thống vì mỗi ngày được giải bằng một bảng trạng thái capacity `0..M`. Tuy nhiên, nó vẫn chưa phải DP chính xác toàn cục, vì quyết định chọn ruộng cho một ngày có thể ảnh hưởng đến các ngày sau, trong khi thuật toán xử lý ngày theo thứ tự và không quay lui toàn cục.

## 7. Phương pháp Mixed-Integer Programming

Mixed-Integer Programming, gọi tắt là MIP, là cách mô hình hóa trực tiếp bài toán bằng biến nhị phân. Với mỗi ruộng `i` và mỗi ngày ứng viên `t`, ta tạo biến:

```text
x[i,t] in {0,1}
```

Biến này bằng `1` nếu ruộng `i` được thu hoạch vào ngày `t`, và bằng `0` nếu không. Ngoài ra, với mỗi ngày `t`, ta tạo biến:

```text
y[t] in {0,1}
```

Biến `y[t]` cho biết ngày `t` có được mở hay không. Nếu `y[t] = 0`, ngày đó không hoạt động và không được có ruộng nào gán vào. Nếu `y[t] = 1`, tổng tải của ngày đó phải nằm trong đoạn `[m, M]`.

Hàm mục tiêu của mô hình là tối đa hóa tổng sản lượng được thu hoạch:

```text
maximize sum_i sum_t d_i * x[i,t]
```

Ràng buộc thứ nhất đảm bảo mỗi ruộng được chọn nhiều nhất một ngày:

```text
sum_t x[i,t] <= 1
```

Ràng buộc thứ hai và thứ ba liên kết tải ngày với biến mở ngày. Gọi:

```text
load[t] = sum_i d_i * x[i,t]
```

Ta có:

```text
load[t] <= M * y[t]
load[t] >= m * y[t]
```

Nếu `y[t] = 0`, hai ràng buộc này ép `load[t] = 0`. Nếu `y[t] = 1`, chúng ép `m <= load[t] <= M`. Như vậy, logic vận hành của nhà máy được mô hình hóa trực tiếp bằng ràng buộc tuyến tính.

Trong lý thuyết, ta có thể tạo biến `x[i,t]` cho mọi ngày `t` thuộc cửa sổ `[s_i, e_i]`. Tuy nhiên, với dữ liệu lớn, số biến có thể rất cao. Vì vậy, lời giải MIP trong project sử dụng hàm `candidate_days()` để rút gọn miền ngày. Với cửa sổ ngắn, thuật toán giữ toàn bộ ngày; với cửa sổ dài, thuật toán giữ ngày đầu, ngày cuối, ngày giữa và một số ngày cách đều. Đây là một cải biên quan trọng giúp mô hình chạy được trong thời gian hợp lý.

Sau khi xây dựng mô hình, chương trình dùng solver SCIP thông qua OR-Tools để giải. Solver chạy trong một giới hạn thời gian nhất định. Nếu tìm được nghiệm feasible hoặc optimal, chương trình đọc các biến `x[i,t]` có giá trị bằng `1` và xuất ra kế hoạch thu hoạch.

MIP là phương pháp có mô hình rõ ràng và gần nhất với bài toán gốc. Ưu điểm của nó là có khả năng chứng minh tối ưu nếu solver chạy đủ lâu trên mô hình đầy đủ. Nhược điểm là chi phí tính toán lớn, đặc biệt khi số biến nhiều. Trong thực nghiệm, time limit là siêu tham số ảnh hưởng mạnh đến điểm số và thời gian chạy.

## 8. Phương pháp Constraint Programming

Constraint Programming, cụ thể trong project là CP-SAT của OR-Tools, sử dụng mô hình biến Boolean tương tự MIP nhưng được giải bằng cơ chế khác. Với mỗi ruộng `i` và ngày ứng viên `t`, chương trình tạo biến Boolean:

```text
x[i,t]
```

Biến này cho biết ruộng `i` có được thu hoạch vào ngày `t` hay không. Với mỗi ngày `t`, chương trình tạo biến Boolean:

```text
y[t]
```

Biến này biểu diễn việc nhà máy có hoạt động vào ngày đó hay không.

Hàm mục tiêu vẫn là tối đa hóa tổng sản lượng:

```text
maximize sum_i sum_t d_i * x[i,t]
```

Các ràng buộc cũng giống với MIP. Mỗi ruộng được chọn nhiều nhất một ngày:

```text
sum_t x[i,t] <= 1
```

Tải của ngày `t` được tính bằng:

```text
load[t] = sum_i d_i * x[i,t]
```

Và được liên kết với biến mở ngày:

```text
load[t] <= M * y[t]
load[t] >= m * y[t]
```

Sự khác biệt chính giữa CP và MIP nằm ở solver. MIP dựa nhiều vào relaxation tuyến tính và branch-and-bound, trong khi CP-SAT kết hợp SAT solving, constraint propagation, integer reasoning và tìm kiếm song song. Vì bài toán có nhiều biến Boolean và ràng buộc tổ hợp, CP-SAT là một lựa chọn phù hợp.

Tương tự MIP, lời giải CP cũng sử dụng `candidate_days()` để giảm số biến. Việc này giúp mô hình nhỏ hơn, nhưng cũng làm lời giải trở thành mô hình xấp xỉ trên tập ngày ứng viên, không phải mô hình đầy đủ trên toàn bộ cửa sổ thời gian.

Sau khi tạo mô hình, chương trình đặt giới hạn thời gian `CP_MAX_TIME_SECONDS` và số worker song song `CP_NUM_SEARCH_WORKERS`. Nếu solver tìm được nghiệm feasible hoặc optimal trong thời gian cho phép, nghiệm đó được xuất ra. Nếu không tìm được nghiệm, chương trình in nghiệm rỗng.

Ưu điểm của CP là biểu diễn tự nhiên các ràng buộc logic và thường xử lý tốt các bài toán tổ hợp. Nhược điểm là thời gian chạy vẫn có thể lớn với input lớn, và chất lượng nghiệm phụ thuộc đáng kể vào time limit cũng như cách rút gọn tập ngày ứng viên.

## 9. So sánh và nhận xét chung

Các phương pháp heuristic như greedy, local search và dynamic programming cục bộ có ưu điểm lớn về tốc độ. Chúng chạy rất nhanh trên bộ test lớn và trong thực nghiệm hiện tại đều đạt điểm cao. Greedy đặc biệt hiệu quả vì quy tắc sắp xếp theo cửa sổ ngắn và deadline sớm phù hợp với bản chất ràng buộc thời gian của bài toán.

Local search mở rộng giúp tăng khả năng tái cấu trúc nghiệm, nhưng trên bộ test hiện tại chưa tạo ra cải thiện rõ rệt so với greedy. Điều này cho thấy nghiệm greedy ban đầu đã khá tốt, hoặc các test chưa đủ khó để thể hiện lợi thế của các move như swap, replace và group move. Tuy vậy, về mặt thiết kế thuật toán, các biến thể local search vẫn có ý nghĩa vì chúng mở rộng không gian tìm kiếm và có thể hữu ích trên các bộ test phức tạp hơn.

Hai phương pháp dynamic programming đều sử dụng knapsack như bài toán con. Phiên bản DP cải biên dựa trên nghiệm greedy rồi lấp capacity còn trống, nên rất nhanh và thực dụng. Phiên bản DP truyền thống theo từng ngày thể hiện rõ hơn bản chất quy hoạch động, nhưng vẫn là heuristic vì xử lý từng ngày độc lập và giới hạn số candidate.

MIP và CP là hai phương pháp mô hình hóa toán học rõ ràng nhất. Chúng biểu diễn trực tiếp biến chọn ruộng, biến mở ngày và các ràng buộc capacity. Tuy nhiên, do kích thước bài toán lớn, cả hai đều phải rút gọn tập ngày ứng viên và phụ thuộc vào time limit. Trong thực nghiệm, khi time limit thấp, MIP và CP có thể chưa đạt đủ điểm; khi tăng time limit, chất lượng nghiệm được cải thiện nhưng thời gian chạy tăng đáng kể.

Nhìn chung, nếu ưu tiên tốc độ và nghiệm tốt trong thời gian ngắn, greedy hoặc các biến thể heuristic là lựa chọn phù hợp. Nếu cần mô hình hóa chặt chẽ hơn và có khả năng tiến gần nghiệm tối ưu, MIP và CP là các hướng đáng dùng, nhưng cần chấp nhận chi phí tính toán cao hơn.


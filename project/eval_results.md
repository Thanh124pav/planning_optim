# Report

Scoring rule: each valid solution whose objective value is at least the reference answer earns 100 points.

## greedy

| Tên thuật toán chính | Hiệu chỉnh | Siêu tham số | Điểm | Thời gian (s) |
| --- | --- | --- | ---: | ---: |
| greedy | ordering rule + repair/fill rounds | `GREEDY_REPAIR_FILL_ROUNDS` = `1`<br>`GREEDY_ORDER_MODE` = `window_deadline_amount` | 500 | 0.253291 |
| greedy | ordering rule + repair/fill rounds | `GREEDY_REPAIR_FILL_ROUNDS` = `2`<br>`GREEDY_ORDER_MODE` = `window_deadline_amount` | 500 | 0.263696 |
| greedy | ordering rule + repair/fill rounds | `GREEDY_REPAIR_FILL_ROUNDS` = `4`<br>`GREEDY_ORDER_MODE` = `window_deadline_amount` | 500 | 0.283653 |
| greedy | ordering rule + repair/fill rounds | `GREEDY_REPAIR_FILL_ROUNDS` = `1`<br>`GREEDY_ORDER_MODE` = `deadline_window` | 500 | 0.247065 |
| greedy | ordering rule + repair/fill rounds | `GREEDY_REPAIR_FILL_ROUNDS` = `2`<br>`GREEDY_ORDER_MODE` = `deadline_window` | 500 | 0.270955 |
| greedy | ordering rule + repair/fill rounds | `GREEDY_REPAIR_FILL_ROUNDS` = `4`<br>`GREEDY_ORDER_MODE` = `deadline_window` | 500 | 0.293706 |

## local_search

| Tên thuật toán chính | Hiệu chỉnh | Siêu tham số | Điểm | Thời gian (s) |
| --- | --- | --- | ---: | ---: |
| local_search | insert-only baseline | `LS_ORIG_INITIAL_REPAIR_FILL_ROUNDS` = `2`<br>`LS_ORIG_MAX_ROUNDS` = `2` | 500 | 0.294584 |
| local_search | insert-only baseline | `LS_ORIG_INITIAL_REPAIR_FILL_ROUNDS` = `2`<br>`LS_ORIG_MAX_ROUNDS` = `5` | 500 | 0.280823 |
| local_search | insert-only baseline | `LS_ORIG_INITIAL_REPAIR_FILL_ROUNDS` = `2`<br>`LS_ORIG_MAX_ROUNDS` = `8` | 500 | 0.296064 |

## local_search_variants

| Tên thuật toán chính | Hiệu chỉnh | Siêu tham số | Điểm | Thời gian (s) |
| --- | --- | --- | ---: | ---: |
| local_search_variants | insert | `LS_MOVES` = `insert`<br>`LS_MAX_ROUNDS` = `3`<br>`LS_TOP_UNASSIGNED` = `300` | 500 | 0.289941 |
| local_search_variants | insert | `LS_MOVES` = `insert`<br>`LS_MAX_ROUNDS` = `6`<br>`LS_TOP_UNASSIGNED` = `800` | 500 | 0.290299 |
| local_search_variants | relocate | `LS_MOVES` = `relocate`<br>`LS_MAX_ROUNDS` = `3`<br>`LS_TOP_ASSIGNED` = `300` | 500 | 0.336540 |
| local_search_variants | relocate | `LS_MOVES` = `relocate`<br>`LS_MAX_ROUNDS` = `6`<br>`LS_TOP_ASSIGNED` = `800` | 500 | 0.332941 |
| local_search_variants | swap | `LS_MOVES` = `swap`<br>`LS_MAX_ROUNDS` = `2`<br>`LS_TOP_ASSIGNED` = `200` | 500 | 0.326257 |
| local_search_variants | swap | `LS_MOVES` = `swap`<br>`LS_MAX_ROUNDS` = `3`<br>`LS_TOP_ASSIGNED` = `400` | 500 | 0.348502 |
| local_search_variants | replace | `LS_MOVES` = `replace`<br>`LS_MAX_ROUNDS` = `3`<br>`LS_TOP_UNASSIGNED` = `300`<br>`LS_TOP_ASSIGNED` = `300` | 500 | 0.277451 |
| local_search_variants | replace | `LS_MOVES` = `replace`<br>`LS_MAX_ROUNDS` = `6`<br>`LS_TOP_UNASSIGNED` = `800`<br>`LS_TOP_ASSIGNED` = `800` | 500 | 0.279776 |
| local_search_variants | group | `LS_MOVES` = `group`<br>`LS_MAX_ROUNDS` = `2`<br>`LS_GROUP_DAYS` = `60`<br>`LS_GROUP_SIZE` = `2` | 500 | 0.350524 |
| local_search_variants | group | `LS_MOVES` = `group`<br>`LS_MAX_ROUNDS` = `3`<br>`LS_GROUP_DAYS` = `120`<br>`LS_GROUP_SIZE` = `4` | 500 | 0.324180 |
| local_search_variants | all moves | `LS_MOVES` = `insert,relocate,swap,replace,group`<br>`LS_MAX_ROUNDS` = `3`<br>`LS_TOP_UNASSIGNED` = `500`<br>`LS_TOP_ASSIGNED` = `300`<br>`LS_GROUP_DAYS` = `80`<br>`LS_GROUP_SIZE` = `3` | 500 | 0.432711 |
| local_search_variants | all moves | `LS_MOVES` = `insert,relocate,swap,replace,group`<br>`LS_MAX_ROUNDS` = `5`<br>`LS_TOP_UNASSIGNED` = `800`<br>`LS_TOP_ASSIGNED` = `500`<br>`LS_GROUP_DAYS` = `120`<br>`LS_GROUP_SIZE` = `4` | 500 | 0.540197 |

## DP

| Tên thuật toán chính | Hiệu chỉnh | Siêu tham số | Điểm | Thời gian (s) |
| --- | --- | --- | ---: | ---: |
| DP | greedy + local knapsack | `DP_INITIAL_REPAIR_FILL_ROUNDS` = `2`<br>`DP_CANDIDATE_LIMIT` = `80` | 500 | 0.353220 |
| DP | greedy + local knapsack | `DP_INITIAL_REPAIR_FILL_ROUNDS` = `2`<br>`DP_CANDIDATE_LIMIT` = `160` | 500 | 0.364007 |
| DP | greedy + local knapsack | `DP_INITIAL_REPAIR_FILL_ROUNDS` = `2`<br>`DP_CANDIDATE_LIMIT` = `320` | 500 | 0.342644 |

## Dynamic Programming

| Tên thuật toán chính | Hiệu chỉnh | Siêu tham số | Điểm | Thời gian (s) |
| --- | --- | --- | ---: | ---: |
| Dynamic Programming | traditional day-by-day knapsack | `DP_TRAD_MAX_CANDIDATES` = `80`<br>`DP_TRAD_PASSES` = `1`<br>`DP_STATE` = `daily capacity 0..M` | 500 | 2.252074 |
| Dynamic Programming | traditional day-by-day knapsack | `DP_TRAD_MAX_CANDIDATES` = `80`<br>`DP_TRAD_PASSES` = `2`<br>`DP_STATE` = `daily capacity 0..M` | 500 | 2.290426 |
| Dynamic Programming | traditional day-by-day knapsack | `DP_TRAD_MAX_CANDIDATES` = `160`<br>`DP_TRAD_PASSES` = `1`<br>`DP_STATE` = `daily capacity 0..M` | 500 | 2.511162 |
| Dynamic Programming | traditional day-by-day knapsack | `DP_TRAD_MAX_CANDIDATES` = `160`<br>`DP_TRAD_PASSES` = `2`<br>`DP_STATE` = `daily capacity 0..M` | 500 | 2.674431 |
| Dynamic Programming | traditional day-by-day knapsack | `DP_TRAD_MAX_CANDIDATES` = `320`<br>`DP_TRAD_PASSES` = `1`<br>`DP_STATE` = `daily capacity 0..M` | 500 | 2.633748 |
| Dynamic Programming | traditional day-by-day knapsack | `DP_TRAD_MAX_CANDIDATES` = `320`<br>`DP_TRAD_PASSES` = `2`<br>`DP_STATE` = `daily capacity 0..M` | 500 | 2.772513 |

## MIP

| Tên thuật toán chính | Hiệu chỉnh | Siêu tham số | Điểm | Thời gian (s) |
| --- | --- | --- | ---: | ---: |
| MIP | time limit | `MIP_SHORT_WINDOW_LIMIT` = `12`<br>`MIP_LONG_WINDOW_DIVISOR` = `6`<br>`MIP_TIME_LIMIT_MS` = `3000`<br>`MIP_INTEGER_THRESHOLD` = `0.5` | 500 | 78.362713 |
| MIP | time limit | `MIP_SHORT_WINDOW_LIMIT` = `12`<br>`MIP_LONG_WINDOW_DIVISOR` = `6`<br>`MIP_TIME_LIMIT_MS` = `8000`<br>`MIP_INTEGER_THRESHOLD` = `0.5` | 500 | 76.476499 |
| MIP | time limit | `MIP_SHORT_WINDOW_LIMIT` = `12`<br>`MIP_LONG_WINDOW_DIVISOR` = `6`<br>`MIP_TIME_LIMIT_MS` = `15000`<br>`MIP_INTEGER_THRESHOLD` = `0.5` | 500 | 77.064906 |
| MIP | candidate day density | `MIP_SHORT_WINDOW_LIMIT` = `12`<br>`MIP_LONG_WINDOW_DIVISOR` = `4`<br>`MIP_TIME_LIMIT_MS` = `8000`<br>`MIP_INTEGER_THRESHOLD` = `0.5` | 500 | 75.453315 |
| MIP | candidate day density | `MIP_SHORT_WINDOW_LIMIT` = `12`<br>`MIP_LONG_WINDOW_DIVISOR` = `6`<br>`MIP_TIME_LIMIT_MS` = `8000`<br>`MIP_INTEGER_THRESHOLD` = `0.5` | 500 | 75.221817 |
| MIP | candidate day density | `MIP_SHORT_WINDOW_LIMIT` = `12`<br>`MIP_LONG_WINDOW_DIVISOR` = `10`<br>`MIP_TIME_LIMIT_MS` = `8000`<br>`MIP_INTEGER_THRESHOLD` = `0.5` | 500 | 76.159334 |

## CP

| Tên thuật toán chính | Hiệu chỉnh | Siêu tham số | Điểm | Thời gian (s) |
| --- | --- | --- | ---: | ---: |
| CP | time limit | `CP_SHORT_WINDOW_LIMIT` = `12`<br>`CP_LONG_WINDOW_DIVISOR` = `6`<br>`CP_MAX_TIME_SECONDS` = `3.0`<br>`CP_NUM_SEARCH_WORKERS` = `8` | 500 | 22.841665 |
| CP | time limit | `CP_SHORT_WINDOW_LIMIT` = `12`<br>`CP_LONG_WINDOW_DIVISOR` = `6`<br>`CP_MAX_TIME_SECONDS` = `8.0`<br>`CP_NUM_SEARCH_WORKERS` = `8` | 500 | 22.560315 |
| CP | time limit | `CP_SHORT_WINDOW_LIMIT` = `12`<br>`CP_LONG_WINDOW_DIVISOR` = `6`<br>`CP_MAX_TIME_SECONDS` = `15.0`<br>`CP_NUM_SEARCH_WORKERS` = `8` | 500 | 22.814409 |
| CP | candidate day density | `CP_SHORT_WINDOW_LIMIT` = `12`<br>`CP_LONG_WINDOW_DIVISOR` = `4`<br>`CP_MAX_TIME_SECONDS` = `8.0`<br>`CP_NUM_SEARCH_WORKERS` = `8` | 500 | 22.991063 |
| CP | candidate day density | `CP_SHORT_WINDOW_LIMIT` = `12`<br>`CP_LONG_WINDOW_DIVISOR` = `6`<br>`CP_MAX_TIME_SECONDS` = `8.0`<br>`CP_NUM_SEARCH_WORKERS` = `8` | 500 | 23.136648 |
| CP | candidate day density | `CP_SHORT_WINDOW_LIMIT` = `12`<br>`CP_LONG_WINDOW_DIVISOR` = `10`<br>`CP_MAX_TIME_SECONDS` = `8.0`<br>`CP_NUM_SEARCH_WORKERS` = `8` | 500 | 23.547360 |

## Per-Test Details

| Experiment | Test | Score | Time (s) | Status | Selected | Value | Reference | Message |
| --- | --- | ---: | ---: | --- | ---: | ---: | ---: | --- |
| greedy-window_deadline_amount-r1 | test1 | 100 | 0.038563 | correct | 100 | 1020 | 1020 | ok |
| greedy-window_deadline_amount-r1 | test2 | 100 | 0.061879 | correct | 5000 | 128868 | 127122 | ok |
| greedy-window_deadline_amount-r1 | test3 | 100 | 0.038852 | correct | 1000 | 49589 | 48733 | ok |
| greedy-window_deadline_amount-r1 | test4 | 100 | 0.081797 | correct | 10000 | 255386 | 250298 | ok |
| greedy-window_deadline_amount-r1 | test5 | 100 | 0.032200 | correct | 10 | 58 | 58 | ok |
| greedy-window_deadline_amount-r2 | test1 | 100 | 0.034256 | correct | 100 | 1020 | 1020 | ok |
| greedy-window_deadline_amount-r2 | test2 | 100 | 0.061384 | correct | 5000 | 128868 | 127122 | ok |
| greedy-window_deadline_amount-r2 | test3 | 100 | 0.039924 | correct | 1000 | 49589 | 48733 | ok |
| greedy-window_deadline_amount-r2 | test4 | 100 | 0.095715 | correct | 10000 | 255386 | 250298 | ok |
| greedy-window_deadline_amount-r2 | test5 | 100 | 0.032417 | correct | 10 | 58 | 58 | ok |
| greedy-window_deadline_amount-r4 | test1 | 100 | 0.034405 | correct | 100 | 1020 | 1020 | ok |
| greedy-window_deadline_amount-r4 | test2 | 100 | 0.066559 | correct | 5000 | 128868 | 127122 | ok |
| greedy-window_deadline_amount-r4 | test3 | 100 | 0.037051 | correct | 1000 | 49589 | 48733 | ok |
| greedy-window_deadline_amount-r4 | test4 | 100 | 0.113441 | correct | 10000 | 255386 | 250298 | ok |
| greedy-window_deadline_amount-r4 | test5 | 100 | 0.032196 | correct | 10 | 58 | 58 | ok |
| greedy-deadline_window-r1 | test1 | 100 | 0.031362 | correct | 100 | 1020 | 1020 | ok |
| greedy-deadline_window-r1 | test2 | 100 | 0.056659 | correct | 5000 | 128868 | 127122 | ok |
| greedy-deadline_window-r1 | test3 | 100 | 0.037987 | correct | 1000 | 49589 | 48733 | ok |
| greedy-deadline_window-r1 | test4 | 100 | 0.086505 | correct | 10000 | 255386 | 250298 | ok |
| greedy-deadline_window-r1 | test5 | 100 | 0.034551 | correct | 10 | 58 | 58 | ok |
| greedy-deadline_window-r2 | test1 | 100 | 0.039521 | correct | 100 | 1020 | 1020 | ok |
| greedy-deadline_window-r2 | test2 | 100 | 0.063253 | correct | 5000 | 128868 | 127122 | ok |
| greedy-deadline_window-r2 | test3 | 100 | 0.039350 | correct | 1000 | 49589 | 48733 | ok |
| greedy-deadline_window-r2 | test4 | 100 | 0.094848 | correct | 10000 | 255386 | 250298 | ok |
| greedy-deadline_window-r2 | test5 | 100 | 0.033983 | correct | 10 | 58 | 58 | ok |
| greedy-deadline_window-r4 | test1 | 100 | 0.042327 | correct | 100 | 1020 | 1020 | ok |
| greedy-deadline_window-r4 | test2 | 100 | 0.066783 | correct | 5000 | 128868 | 127122 | ok |
| greedy-deadline_window-r4 | test3 | 100 | 0.040933 | correct | 1000 | 49589 | 48733 | ok |
| greedy-deadline_window-r4 | test4 | 100 | 0.100993 | correct | 10000 | 255386 | 250298 | ok |
| greedy-deadline_window-r4 | test5 | 100 | 0.042671 | correct | 10 | 58 | 58 | ok |
| local-search-original-r2 | test1 | 100 | 0.035515 | correct | 100 | 1020 | 1020 | ok |
| local-search-original-r2 | test2 | 100 | 0.076855 | correct | 5000 | 128868 | 127122 | ok |
| local-search-original-r2 | test3 | 100 | 0.043380 | correct | 1000 | 49589 | 48733 | ok |
| local-search-original-r2 | test4 | 100 | 0.103740 | correct | 10000 | 255386 | 250298 | ok |
| local-search-original-r2 | test5 | 100 | 0.035094 | correct | 10 | 58 | 58 | ok |
| local-search-original-r5 | test1 | 100 | 0.034287 | correct | 100 | 1020 | 1020 | ok |
| local-search-original-r5 | test2 | 100 | 0.065338 | correct | 5000 | 128868 | 127122 | ok |
| local-search-original-r5 | test3 | 100 | 0.040584 | correct | 1000 | 49589 | 48733 | ok |
| local-search-original-r5 | test4 | 100 | 0.106699 | correct | 10000 | 255386 | 250298 | ok |
| local-search-original-r5 | test5 | 100 | 0.033915 | correct | 10 | 58 | 58 | ok |
| local-search-original-r8 | test1 | 100 | 0.035690 | correct | 100 | 1020 | 1020 | ok |
| local-search-original-r8 | test2 | 100 | 0.070304 | correct | 5000 | 128868 | 127122 | ok |
| local-search-original-r8 | test3 | 100 | 0.043169 | correct | 1000 | 49589 | 48733 | ok |
| local-search-original-r8 | test4 | 100 | 0.112503 | correct | 10000 | 255386 | 250298 | ok |
| local-search-original-r8 | test5 | 100 | 0.034398 | correct | 10 | 58 | 58 | ok |
| local-search-variant-1 | test1 | 100 | 0.058980 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-1 | test2 | 100 | 0.060949 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-1 | test3 | 100 | 0.039541 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-1 | test4 | 100 | 0.095265 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-1 | test5 | 100 | 0.035204 | correct | 10 | 58 | 58 | ok |
| local-search-variant-2 | test1 | 100 | 0.035328 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-2 | test2 | 100 | 0.062007 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-2 | test3 | 100 | 0.054767 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-2 | test4 | 100 | 0.096204 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-2 | test5 | 100 | 0.041992 | correct | 10 | 58 | 58 | ok |
| local-search-variant-3 | test1 | 100 | 0.037449 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-3 | test2 | 100 | 0.076393 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-3 | test3 | 100 | 0.042944 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-3 | test4 | 100 | 0.127787 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-3 | test5 | 100 | 0.051968 | correct | 10 | 58 | 58 | ok |
| local-search-variant-4 | test1 | 100 | 0.039572 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-4 | test2 | 100 | 0.076062 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-4 | test3 | 100 | 0.046468 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-4 | test4 | 100 | 0.133487 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-4 | test5 | 100 | 0.037354 | correct | 10 | 58 | 58 | ok |
| local-search-variant-5 | test1 | 100 | 0.037559 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-5 | test2 | 100 | 0.076539 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-5 | test3 | 100 | 0.044871 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-5 | test4 | 100 | 0.122974 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-5 | test5 | 100 | 0.044315 | correct | 10 | 58 | 58 | ok |
| local-search-variant-6 | test1 | 100 | 0.048011 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-6 | test2 | 100 | 0.081610 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-6 | test3 | 100 | 0.047712 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-6 | test4 | 100 | 0.133392 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-6 | test5 | 100 | 0.037776 | correct | 10 | 58 | 58 | ok |
| local-search-variant-7 | test1 | 100 | 0.037568 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-7 | test2 | 100 | 0.064967 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-7 | test3 | 100 | 0.039754 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-7 | test4 | 100 | 0.098763 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-7 | test5 | 100 | 0.036400 | correct | 10 | 58 | 58 | ok |
| local-search-variant-8 | test1 | 100 | 0.037799 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-8 | test2 | 100 | 0.062715 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-8 | test3 | 100 | 0.041253 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-8 | test4 | 100 | 0.096506 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-8 | test5 | 100 | 0.041502 | correct | 10 | 58 | 58 | ok |
| local-search-variant-9 | test1 | 100 | 0.041295 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-9 | test2 | 100 | 0.069140 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-9 | test3 | 100 | 0.057849 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-9 | test4 | 100 | 0.147405 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-9 | test5 | 100 | 0.034835 | correct | 10 | 58 | 58 | ok |
| local-search-variant-10 | test1 | 100 | 0.038622 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-10 | test2 | 100 | 0.077930 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-10 | test3 | 100 | 0.043748 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-10 | test4 | 100 | 0.126676 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-10 | test5 | 100 | 0.037203 | correct | 10 | 58 | 58 | ok |
| local-search-variant-11 | test1 | 100 | 0.039594 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-11 | test2 | 100 | 0.110737 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-11 | test3 | 100 | 0.053895 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-11 | test4 | 100 | 0.190589 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-11 | test5 | 100 | 0.037897 | correct | 10 | 58 | 58 | ok |
| local-search-variant-12 | test1 | 100 | 0.037446 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-12 | test2 | 100 | 0.149565 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-12 | test3 | 100 | 0.056568 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-12 | test4 | 100 | 0.262678 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-12 | test5 | 100 | 0.033940 | correct | 10 | 58 | 58 | ok |
| dp-local-c80 | test1 | 100 | 0.032881 | correct | 100 | 1020 | 1020 | ok |
| dp-local-c80 | test2 | 100 | 0.093355 | correct | 5000 | 128868 | 127122 | ok |
| dp-local-c80 | test3 | 100 | 0.038850 | correct | 1000 | 49589 | 48733 | ok |
| dp-local-c80 | test4 | 100 | 0.155437 | correct | 10000 | 255386 | 250298 | ok |
| dp-local-c80 | test5 | 100 | 0.032697 | correct | 10 | 58 | 58 | ok |
| dp-local-c160 | test1 | 100 | 0.045452 | correct | 100 | 1020 | 1020 | ok |
| dp-local-c160 | test2 | 100 | 0.094181 | correct | 5000 | 128868 | 127122 | ok |
| dp-local-c160 | test3 | 100 | 0.041043 | correct | 1000 | 49589 | 48733 | ok |
| dp-local-c160 | test4 | 100 | 0.148452 | correct | 10000 | 255386 | 250298 | ok |
| dp-local-c160 | test5 | 100 | 0.034880 | correct | 10 | 58 | 58 | ok |
| dp-local-c320 | test1 | 100 | 0.033234 | correct | 100 | 1020 | 1020 | ok |
| dp-local-c320 | test2 | 100 | 0.091043 | correct | 5000 | 128868 | 127122 | ok |
| dp-local-c320 | test3 | 100 | 0.039810 | correct | 1000 | 49589 | 48733 | ok |
| dp-local-c320 | test4 | 100 | 0.146626 | correct | 10000 | 255386 | 250298 | ok |
| dp-local-c320 | test5 | 100 | 0.031931 | correct | 10 | 58 | 58 | ok |
| dp-traditional-c80-p1 | test1 | 100 | 0.031804 | correct | 100 | 1020 | 1020 | ok |
| dp-traditional-c80-p1 | test2 | 100 | 0.463398 | correct | 5000 | 128868 | 127122 | ok |
| dp-traditional-c80-p1 | test3 | 100 | 0.296446 | correct | 1000 | 49589 | 48733 | ok |
| dp-traditional-c80-p1 | test4 | 100 | 1.428056 | correct | 10000 | 255386 | 250298 | ok |
| dp-traditional-c80-p1 | test5 | 100 | 0.032370 | correct | 10 | 58 | 58 | ok |
| dp-traditional-c80-p2 | test1 | 100 | 0.030906 | correct | 100 | 1020 | 1020 | ok |
| dp-traditional-c80-p2 | test2 | 100 | 0.484484 | correct | 5000 | 128868 | 127122 | ok |
| dp-traditional-c80-p2 | test3 | 100 | 0.301963 | correct | 1000 | 49589 | 48733 | ok |
| dp-traditional-c80-p2 | test4 | 100 | 1.441973 | correct | 10000 | 255386 | 250298 | ok |
| dp-traditional-c80-p2 | test5 | 100 | 0.031101 | correct | 10 | 58 | 58 | ok |
| dp-traditional-c160-p1 | test1 | 100 | 0.032492 | correct | 100 | 1020 | 1020 | ok |
| dp-traditional-c160-p1 | test2 | 100 | 0.480744 | correct | 5000 | 128868 | 127122 | ok |
| dp-traditional-c160-p1 | test3 | 100 | 0.410954 | correct | 1000 | 49589 | 48733 | ok |
| dp-traditional-c160-p1 | test4 | 100 | 1.556872 | correct | 10000 | 255386 | 250298 | ok |
| dp-traditional-c160-p1 | test5 | 100 | 0.030100 | correct | 10 | 58 | 58 | ok |
| dp-traditional-c160-p2 | test1 | 100 | 0.032516 | correct | 100 | 1020 | 1020 | ok |
| dp-traditional-c160-p2 | test2 | 100 | 0.488937 | correct | 5000 | 128868 | 127122 | ok |
| dp-traditional-c160-p2 | test3 | 100 | 0.516976 | correct | 1000 | 49589 | 48733 | ok |
| dp-traditional-c160-p2 | test4 | 100 | 1.604481 | correct | 10000 | 255386 | 250298 | ok |
| dp-traditional-c160-p2 | test5 | 100 | 0.031520 | correct | 10 | 58 | 58 | ok |
| dp-traditional-c320-p1 | test1 | 100 | 0.031780 | correct | 100 | 1020 | 1020 | ok |
| dp-traditional-c320-p1 | test2 | 100 | 0.497492 | correct | 5000 | 128868 | 127122 | ok |
| dp-traditional-c320-p1 | test3 | 100 | 0.444214 | correct | 1000 | 49589 | 48733 | ok |
| dp-traditional-c320-p1 | test4 | 100 | 1.628564 | correct | 10000 | 255386 | 250298 | ok |
| dp-traditional-c320-p1 | test5 | 100 | 0.031698 | correct | 10 | 58 | 58 | ok |
| dp-traditional-c320-p2 | test1 | 100 | 0.033718 | correct | 100 | 1020 | 1020 | ok |
| dp-traditional-c320-p2 | test2 | 100 | 0.515668 | correct | 5000 | 128868 | 127122 | ok |
| dp-traditional-c320-p2 | test3 | 100 | 0.457552 | correct | 1000 | 49589 | 48733 | ok |
| dp-traditional-c320-p2 | test4 | 100 | 1.734722 | correct | 10000 | 255386 | 250298 | ok |
| dp-traditional-c320-p2 | test5 | 100 | 0.030853 | correct | 10 | 58 | 58 | ok |
| mip-time-3000 | test1 | 100 | 0.213948 | correct | 100 | 1020 | 1020 | ok |
| mip-time-3000 | test2 | 100 | 19.245431 | correct | 5000 | 128868 | 127122 | ok |
| mip-time-3000 | test3 | 100 | 2.884583 | correct | 1000 | 49589 | 48733 | ok |
| mip-time-3000 | test4 | 100 | 55.833988 | correct | 10000 | 255386 | 250298 | ok |
| mip-time-3000 | test5 | 100 | 0.184763 | correct | 10 | 58 | 58 | ok |
| mip-time-8000 | test1 | 100 | 0.234461 | correct | 100 | 1020 | 1020 | ok |
| mip-time-8000 | test2 | 100 | 19.059987 | correct | 5000 | 128868 | 127122 | ok |
| mip-time-8000 | test3 | 100 | 2.936823 | correct | 1000 | 49589 | 48733 | ok |
| mip-time-8000 | test4 | 100 | 54.071009 | correct | 10000 | 255386 | 250298 | ok |
| mip-time-8000 | test5 | 100 | 0.174219 | correct | 10 | 58 | 58 | ok |
| mip-time-15000 | test1 | 100 | 0.199694 | correct | 100 | 1020 | 1020 | ok |
| mip-time-15000 | test2 | 100 | 18.985138 | correct | 5000 | 128868 | 127122 | ok |
| mip-time-15000 | test3 | 100 | 2.792061 | correct | 1000 | 49589 | 48733 | ok |
| mip-time-15000 | test4 | 100 | 54.910510 | correct | 10000 | 255386 | 250298 | ok |
| mip-time-15000 | test5 | 100 | 0.177502 | correct | 10 | 58 | 58 | ok |
| mip-divisor-4 | test1 | 100 | 0.202052 | correct | 100 | 1020 | 1020 | ok |
| mip-divisor-4 | test2 | 100 | 18.151281 | correct | 5000 | 128868 | 127122 | ok |
| mip-divisor-4 | test3 | 100 | 2.748686 | correct | 1000 | 49589 | 48733 | ok |
| mip-divisor-4 | test4 | 100 | 54.160475 | correct | 10000 | 255386 | 250298 | ok |
| mip-divisor-4 | test5 | 100 | 0.190821 | correct | 10 | 58 | 58 | ok |
| mip-divisor-6 | test1 | 100 | 0.216255 | correct | 100 | 1020 | 1020 | ok |
| mip-divisor-6 | test2 | 100 | 18.335731 | correct | 5000 | 128868 | 127122 | ok |
| mip-divisor-6 | test3 | 100 | 2.756265 | correct | 1000 | 49589 | 48733 | ok |
| mip-divisor-6 | test4 | 100 | 53.743101 | correct | 10000 | 255386 | 250298 | ok |
| mip-divisor-6 | test5 | 100 | 0.170465 | correct | 10 | 58 | 58 | ok |
| mip-divisor-10 | test1 | 100 | 0.209483 | correct | 100 | 1020 | 1020 | ok |
| mip-divisor-10 | test2 | 100 | 18.545323 | correct | 5000 | 128868 | 127122 | ok |
| mip-divisor-10 | test3 | 100 | 2.743522 | correct | 1000 | 49589 | 48733 | ok |
| mip-divisor-10 | test4 | 100 | 54.465913 | correct | 10000 | 255386 | 250298 | ok |
| mip-divisor-10 | test5 | 100 | 0.195093 | correct | 10 | 58 | 58 | ok |
| cp-time-3.0 | test1 | 100 | 0.848376 | correct | 100 | 1020 | 1020 | ok |
| cp-time-3.0 | test2 | 100 | 6.232922 | correct | 5000 | 128868 | 127122 | ok |
| cp-time-3.0 | test3 | 100 | 1.839395 | correct | 1000 | 49589 | 48733 | ok |
| cp-time-3.0 | test4 | 100 | 13.240832 | correct | 10000 | 255386 | 250298 | ok |
| cp-time-3.0 | test5 | 100 | 0.680140 | correct | 10 | 58 | 58 | ok |
| cp-time-8.0 | test1 | 100 | 0.694041 | correct | 100 | 1020 | 1020 | ok |
| cp-time-8.0 | test2 | 100 | 6.285724 | correct | 5000 | 128868 | 127122 | ok |
| cp-time-8.0 | test3 | 100 | 1.575069 | correct | 1000 | 49589 | 48733 | ok |
| cp-time-8.0 | test4 | 100 | 13.338389 | correct | 10000 | 255386 | 250298 | ok |
| cp-time-8.0 | test5 | 100 | 0.667093 | correct | 10 | 58 | 58 | ok |
| cp-time-15.0 | test1 | 100 | 0.718036 | correct | 100 | 1020 | 1020 | ok |
| cp-time-15.0 | test2 | 100 | 6.377166 | correct | 5000 | 128868 | 127122 | ok |
| cp-time-15.0 | test3 | 100 | 1.678610 | correct | 1000 | 49589 | 48733 | ok |
| cp-time-15.0 | test4 | 100 | 13.352413 | correct | 10000 | 255386 | 250298 | ok |
| cp-time-15.0 | test5 | 100 | 0.688183 | correct | 10 | 58 | 58 | ok |
| cp-divisor-4 | test1 | 100 | 0.737373 | correct | 100 | 1020 | 1020 | ok |
| cp-divisor-4 | test2 | 100 | 6.524202 | correct | 5000 | 128868 | 127122 | ok |
| cp-divisor-4 | test3 | 100 | 1.606785 | correct | 1000 | 49589 | 48733 | ok |
| cp-divisor-4 | test4 | 100 | 13.480870 | correct | 10000 | 255386 | 250298 | ok |
| cp-divisor-4 | test5 | 100 | 0.641832 | correct | 10 | 58 | 58 | ok |
| cp-divisor-6 | test1 | 100 | 0.730043 | correct | 100 | 1020 | 1020 | ok |
| cp-divisor-6 | test2 | 100 | 6.199292 | correct | 5000 | 128868 | 127122 | ok |
| cp-divisor-6 | test3 | 100 | 1.662356 | correct | 1000 | 49589 | 48733 | ok |
| cp-divisor-6 | test4 | 100 | 13.725572 | correct | 10000 | 255386 | 250298 | ok |
| cp-divisor-6 | test5 | 100 | 0.819385 | correct | 10 | 58 | 58 | ok |
| cp-divisor-10 | test1 | 100 | 0.860129 | correct | 100 | 1020 | 1020 | ok |
| cp-divisor-10 | test2 | 100 | 6.313948 | correct | 5000 | 128868 | 127122 | ok |
| cp-divisor-10 | test3 | 100 | 1.674441 | correct | 1000 | 49589 | 48733 | ok |
| cp-divisor-10 | test4 | 100 | 13.993272 | correct | 10000 | 255386 | 250298 | ok |
| cp-divisor-10 | test5 | 100 | 0.705570 | correct | 10 | 58 | 58 | ok |

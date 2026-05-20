# Report

Scoring rule: each valid solution whose objective value is at least the reference answer earns 100 points.

## greedy

| Tên thuật toán chính | Hiệu chỉnh | Siêu tham số | Điểm | Thời gian (s) |
| --- | --- | --- | ---: | ---: |
| greedy | repair/fill rounds | `GREEDY_REPAIR_FILL_ROUNDS` = `1`<br>`GREEDY_ORDER_MODE` = `window_deadline_amount` | 500 | 0.143130 |
| greedy | repair/fill rounds | `GREEDY_REPAIR_FILL_ROUNDS` = `2`<br>`GREEDY_ORDER_MODE` = `window_deadline_amount` | 500 | 0.145264 |
| greedy | repair/fill rounds | `GREEDY_REPAIR_FILL_ROUNDS` = `4`<br>`GREEDY_ORDER_MODE` = `window_deadline_amount` | 500 | 0.158121 |
| greedy | ordering rule | `GREEDY_REPAIR_FILL_ROUNDS` = `2`<br>`GREEDY_ORDER_MODE` = `window_deadline_amount` | 500 | 0.143698 |
| greedy | ordering rule | `GREEDY_REPAIR_FILL_ROUNDS` = `2`<br>`GREEDY_ORDER_MODE` = `amount_window` | 100 | 280.017602 |
| greedy | ordering rule | `GREEDY_REPAIR_FILL_ROUNDS` = `2`<br>`GREEDY_ORDER_MODE` = `deadline_window` | 500 | 0.157361 |

## local_search

| Tên thuật toán chính | Hiệu chỉnh | Siêu tham số | Điểm | Thời gian (s) |
| --- | --- | --- | ---: | ---: |
| local_search | insert-only baseline | `LS_ORIG_INITIAL_REPAIR_FILL_ROUNDS` = `2`<br>`LS_ORIG_MAX_ROUNDS` = `2` | 500 | 0.168210 |
| local_search | insert-only baseline | `LS_ORIG_INITIAL_REPAIR_FILL_ROUNDS` = `2`<br>`LS_ORIG_MAX_ROUNDS` = `5` | 500 | 0.170638 |
| local_search | insert-only baseline | `LS_ORIG_INITIAL_REPAIR_FILL_ROUNDS` = `2`<br>`LS_ORIG_MAX_ROUNDS` = `8` | 500 | 0.167184 |

## local_search_variants

| Tên thuật toán chính | Hiệu chỉnh | Siêu tham số | Điểm | Thời gian (s) |
| --- | --- | --- | ---: | ---: |
| local_search_variants | insert | `LS_MOVES` = `insert`<br>`LS_MAX_ROUNDS` = `3`<br>`LS_TOP_UNASSIGNED` = `300` | 500 | 0.165644 |
| local_search_variants | insert | `LS_MOVES` = `insert`<br>`LS_MAX_ROUNDS` = `6`<br>`LS_TOP_UNASSIGNED` = `800` | 500 | 0.167502 |
| local_search_variants | relocate | `LS_MOVES` = `relocate`<br>`LS_MAX_ROUNDS` = `3`<br>`LS_TOP_ASSIGNED` = `300` | 500 | 0.193940 |
| local_search_variants | relocate | `LS_MOVES` = `relocate`<br>`LS_MAX_ROUNDS` = `6`<br>`LS_TOP_ASSIGNED` = `800` | 500 | 0.213484 |
| local_search_variants | swap | `LS_MOVES` = `swap`<br>`LS_MAX_ROUNDS` = `2`<br>`LS_TOP_ASSIGNED` = `200` | 500 | 0.208095 |
| local_search_variants | swap | `LS_MOVES` = `swap`<br>`LS_MAX_ROUNDS` = `3`<br>`LS_TOP_ASSIGNED` = `400` | 500 | 0.221657 |
| local_search_variants | replace | `LS_MOVES` = `replace`<br>`LS_MAX_ROUNDS` = `3`<br>`LS_TOP_UNASSIGNED` = `300`<br>`LS_TOP_ASSIGNED` = `300` | 500 | 0.170849 |
| local_search_variants | replace | `LS_MOVES` = `replace`<br>`LS_MAX_ROUNDS` = `6`<br>`LS_TOP_UNASSIGNED` = `800`<br>`LS_TOP_ASSIGNED` = `800` | 500 | 0.169352 |
| local_search_variants | group | `LS_MOVES` = `group`<br>`LS_MAX_ROUNDS` = `2`<br>`LS_GROUP_DAYS` = `60`<br>`LS_GROUP_SIZE` = `2` | 500 | 0.189917 |
| local_search_variants | group | `LS_MOVES` = `group`<br>`LS_MAX_ROUNDS` = `3`<br>`LS_GROUP_DAYS` = `120`<br>`LS_GROUP_SIZE` = `4` | 500 | 0.195928 |
| local_search_variants | all moves | `LS_MOVES` = `insert,relocate,swap,replace,group`<br>`LS_MAX_ROUNDS` = `3`<br>`LS_TOP_UNASSIGNED` = `500`<br>`LS_TOP_ASSIGNED` = `300`<br>`LS_GROUP_DAYS` = `80`<br>`LS_GROUP_SIZE` = `3` | 500 | 0.312456 |
| local_search_variants | all moves | `LS_MOVES` = `insert,relocate,swap,replace,group`<br>`LS_MAX_ROUNDS` = `5`<br>`LS_TOP_UNASSIGNED` = `800`<br>`LS_TOP_ASSIGNED` = `500`<br>`LS_GROUP_DAYS` = `120`<br>`LS_GROUP_SIZE` = `4` | 500 | 0.417406 |

## DP

| Tên thuật toán chính | Hiệu chỉnh | Siêu tham số | Điểm | Thời gian (s) |
| --- | --- | --- | ---: | ---: |
| DP | greedy + local knapsack | `DP_INITIAL_REPAIR_FILL_ROUNDS` = `2`<br>`DP_CANDIDATE_LIMIT` = `80` | 500 | 0.249595 |
| DP | greedy + local knapsack | `DP_INITIAL_REPAIR_FILL_ROUNDS` = `2`<br>`DP_CANDIDATE_LIMIT` = `160` | 500 | 0.246210 |
| DP | greedy + local knapsack | `DP_INITIAL_REPAIR_FILL_ROUNDS` = `2`<br>`DP_CANDIDATE_LIMIT` = `320` | 500 | 0.238451 |

## Dynamic Programming

| Tên thuật toán chính | Hiệu chỉnh | Siêu tham số | Điểm | Thời gian (s) |
| --- | --- | --- | ---: | ---: |
| Dynamic Programming | traditional day-by-day knapsack | `DP_TRAD_MAX_CANDIDATES` = `80`<br>`DP_TRAD_PASSES` = `1`<br>`DP_STATE` = `daily capacity 0..M` | 500 | 1.889445 |
| Dynamic Programming | traditional day-by-day knapsack | `DP_TRAD_MAX_CANDIDATES` = `80`<br>`DP_TRAD_PASSES` = `2`<br>`DP_STATE` = `daily capacity 0..M` | 500 | 1.947058 |
| Dynamic Programming | traditional day-by-day knapsack | `DP_TRAD_MAX_CANDIDATES` = `160`<br>`DP_TRAD_PASSES` = `1`<br>`DP_STATE` = `daily capacity 0..M` | 500 | 2.142409 |
| Dynamic Programming | traditional day-by-day knapsack | `DP_TRAD_MAX_CANDIDATES` = `160`<br>`DP_TRAD_PASSES` = `2`<br>`DP_STATE` = `daily capacity 0..M` | 500 | 2.186653 |
| Dynamic Programming | traditional day-by-day knapsack | `DP_TRAD_MAX_CANDIDATES` = `320`<br>`DP_TRAD_PASSES` = `1`<br>`DP_STATE` = `daily capacity 0..M` | 500 | 2.199718 |
| Dynamic Programming | traditional day-by-day knapsack | `DP_TRAD_MAX_CANDIDATES` = `320`<br>`DP_TRAD_PASSES` = `2`<br>`DP_STATE` = `daily capacity 0..M` | 500 | 2.103459 |

## MIP

| Tên thuật toán chính | Hiệu chỉnh | Siêu tham số | Điểm | Thời gian (s) |
| --- | --- | --- | ---: | ---: |
| MIP | time limit | `MIP_SHORT_WINDOW_LIMIT` = `12`<br>`MIP_LONG_WINDOW_DIVISOR` = `6`<br>`MIP_TIME_LIMIT_MS` = `3000`<br>`MIP_INTEGER_THRESHOLD` = `0.5` | 300 | 14.600876 |
| MIP | time limit | `MIP_SHORT_WINDOW_LIMIT` = `12`<br>`MIP_LONG_WINDOW_DIVISOR` = `6`<br>`MIP_TIME_LIMIT_MS` = `8000`<br>`MIP_INTEGER_THRESHOLD` = `0.5` | 400 | 26.348190 |
| MIP | time limit | `MIP_SHORT_WINDOW_LIMIT` = `12`<br>`MIP_LONG_WINDOW_DIVISOR` = `6`<br>`MIP_TIME_LIMIT_MS` = `15000`<br>`MIP_INTEGER_THRESHOLD` = `0.5` | 500 | 37.223351 |
| MIP | candidate day density | `MIP_SHORT_WINDOW_LIMIT` = `12`<br>`MIP_LONG_WINDOW_DIVISOR` = `4`<br>`MIP_TIME_LIMIT_MS` = `8000`<br>`MIP_INTEGER_THRESHOLD` = `0.5` | 400 | 27.593526 |
| MIP | candidate day density | `MIP_SHORT_WINDOW_LIMIT` = `12`<br>`MIP_LONG_WINDOW_DIVISOR` = `6`<br>`MIP_TIME_LIMIT_MS` = `8000`<br>`MIP_INTEGER_THRESHOLD` = `0.5` | 400 | 25.710212 |
| MIP | candidate day density | `MIP_SHORT_WINDOW_LIMIT` = `12`<br>`MIP_LONG_WINDOW_DIVISOR` = `10`<br>`MIP_TIME_LIMIT_MS` = `8000`<br>`MIP_INTEGER_THRESHOLD` = `0.5` | 400 | 22.878606 |

## CP

| Tên thuật toán chính | Hiệu chỉnh | Siêu tham số | Điểm | Thời gian (s) |
| --- | --- | --- | ---: | ---: |
| CP | time limit | `CP_SHORT_WINDOW_LIMIT` = `12`<br>`CP_LONG_WINDOW_DIVISOR` = `6`<br>`CP_MAX_TIME_SECONDS` = `3.0`<br>`CP_NUM_SEARCH_WORKERS` = `8` | 300 | 11.935382 |
| CP | time limit | `CP_SHORT_WINDOW_LIMIT` = `12`<br>`CP_LONG_WINDOW_DIVISOR` = `6`<br>`CP_MAX_TIME_SECONDS` = `8.0`<br>`CP_NUM_SEARCH_WORKERS` = `8` | 400 | 17.872501 |
| CP | time limit | `CP_SHORT_WINDOW_LIMIT` = `12`<br>`CP_LONG_WINDOW_DIVISOR` = `6`<br>`CP_MAX_TIME_SECONDS` = `15.0`<br>`CP_NUM_SEARCH_WORKERS` = `8` | 500 | 29.696679 |
| CP | candidate day density | `CP_SHORT_WINDOW_LIMIT` = `12`<br>`CP_LONG_WINDOW_DIVISOR` = `4`<br>`CP_MAX_TIME_SECONDS` = `8.0`<br>`CP_NUM_SEARCH_WORKERS` = `8` | 400 | 21.599782 |
| CP | candidate day density | `CP_SHORT_WINDOW_LIMIT` = `12`<br>`CP_LONG_WINDOW_DIVISOR` = `6`<br>`CP_MAX_TIME_SECONDS` = `8.0`<br>`CP_NUM_SEARCH_WORKERS` = `8` | 400 | 17.972198 |
| CP | candidate day density | `CP_SHORT_WINDOW_LIMIT` = `12`<br>`CP_LONG_WINDOW_DIVISOR` = `10`<br>`CP_MAX_TIME_SECONDS` = `8.0`<br>`CP_NUM_SEARCH_WORKERS` = `8` | 400 | 20.921658 |

## Per-Test Details

| Experiment | Test | Score | Time (s) | Status | Selected | Value | Reference | Message |
| --- | --- | ---: | ---: | --- | ---: | ---: | ---: | --- |
| greedy-rounds-1 | test1 | 100 | 0.020544 | correct | 100 | 1020 | 1020 | ok |
| greedy-rounds-1 | test2 | 100 | 0.035545 | correct | 5000 | 128868 | 127122 | ok |
| greedy-rounds-1 | test3 | 100 | 0.017626 | correct | 1000 | 49589 | 48733 | ok |
| greedy-rounds-1 | test4 | 100 | 0.054496 | correct | 10000 | 255386 | 250298 | ok |
| greedy-rounds-1 | test5 | 100 | 0.014917 | correct | 10 | 58 | 58 | ok |
| greedy-rounds-2 | test1 | 100 | 0.015984 | correct | 100 | 1020 | 1020 | ok |
| greedy-rounds-2 | test2 | 100 | 0.037982 | correct | 5000 | 128868 | 127122 | ok |
| greedy-rounds-2 | test3 | 100 | 0.018469 | correct | 1000 | 49589 | 48733 | ok |
| greedy-rounds-2 | test4 | 100 | 0.056424 | correct | 10000 | 255386 | 250298 | ok |
| greedy-rounds-2 | test5 | 100 | 0.016405 | correct | 10 | 58 | 58 | ok |
| greedy-rounds-4 | test1 | 100 | 0.015922 | correct | 100 | 1020 | 1020 | ok |
| greedy-rounds-4 | test2 | 100 | 0.038741 | correct | 5000 | 128868 | 127122 | ok |
| greedy-rounds-4 | test3 | 100 | 0.018897 | correct | 1000 | 49589 | 48733 | ok |
| greedy-rounds-4 | test4 | 100 | 0.069759 | correct | 10000 | 255386 | 250298 | ok |
| greedy-rounds-4 | test5 | 100 | 0.014803 | correct | 10 | 58 | 58 | ok |
| greedy-order-window_deadline_amount | test1 | 100 | 0.014828 | correct | 100 | 1020 | 1020 | ok |
| greedy-order-window_deadline_amount | test2 | 100 | 0.036937 | correct | 5000 | 128868 | 127122 | ok |
| greedy-order-window_deadline_amount | test3 | 100 | 0.018310 | correct | 1000 | 49589 | 48733 | ok |
| greedy-order-window_deadline_amount | test4 | 100 | 0.058532 | correct | 10000 | 255386 | 250298 | ok |
| greedy-order-window_deadline_amount | test5 | 100 | 0.015091 | correct | 10 | 58 | 58 | ok |
| greedy-order-amount_window | test1 | 0 | 70.000000 | timeout | 0 | 0 | 1020 | timeout after 70.000s |
| greedy-order-amount_window | test2 | 0 | 70.000000 | timeout | 0 | 0 | 127122 | timeout after 70.000s |
| greedy-order-amount_window | test3 | 0 | 70.000000 | timeout | 0 | 0 | 48733 | timeout after 70.000s |
| greedy-order-amount_window | test4 | 0 | 70.000000 | timeout | 0 | 0 | 250298 | timeout after 70.000s |
| greedy-order-amount_window | test5 | 100 | 0.017602 | correct | 10 | 58 | 58 | ok |
| greedy-order-deadline_window | test1 | 100 | 0.016982 | correct | 100 | 1020 | 1020 | ok |
| greedy-order-deadline_window | test2 | 100 | 0.039196 | correct | 5000 | 128868 | 127122 | ok |
| greedy-order-deadline_window | test3 | 100 | 0.019311 | correct | 1000 | 49589 | 48733 | ok |
| greedy-order-deadline_window | test4 | 100 | 0.066054 | correct | 10000 | 255386 | 250298 | ok |
| greedy-order-deadline_window | test5 | 100 | 0.015819 | correct | 10 | 58 | 58 | ok |
| local-search-original-r2 | test1 | 100 | 0.017233 | correct | 100 | 1020 | 1020 | ok |
| local-search-original-r2 | test2 | 100 | 0.041968 | correct | 5000 | 128868 | 127122 | ok |
| local-search-original-r2 | test3 | 100 | 0.020713 | correct | 1000 | 49589 | 48733 | ok |
| local-search-original-r2 | test4 | 100 | 0.072412 | correct | 10000 | 255386 | 250298 | ok |
| local-search-original-r2 | test5 | 100 | 0.015884 | correct | 10 | 58 | 58 | ok |
| local-search-original-r5 | test1 | 100 | 0.019266 | correct | 100 | 1020 | 1020 | ok |
| local-search-original-r5 | test2 | 100 | 0.040680 | correct | 5000 | 128868 | 127122 | ok |
| local-search-original-r5 | test3 | 100 | 0.020028 | correct | 1000 | 49589 | 48733 | ok |
| local-search-original-r5 | test4 | 100 | 0.073303 | correct | 10000 | 255386 | 250298 | ok |
| local-search-original-r5 | test5 | 100 | 0.017361 | correct | 10 | 58 | 58 | ok |
| local-search-original-r8 | test1 | 100 | 0.016018 | correct | 100 | 1020 | 1020 | ok |
| local-search-original-r8 | test2 | 100 | 0.042147 | correct | 5000 | 128868 | 127122 | ok |
| local-search-original-r8 | test3 | 100 | 0.020890 | correct | 1000 | 49589 | 48733 | ok |
| local-search-original-r8 | test4 | 100 | 0.070312 | correct | 10000 | 255386 | 250298 | ok |
| local-search-original-r8 | test5 | 100 | 0.017817 | correct | 10 | 58 | 58 | ok |
| local-search-variant-1 | test1 | 100 | 0.018194 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-1 | test2 | 100 | 0.041027 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-1 | test3 | 100 | 0.022205 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-1 | test4 | 100 | 0.065771 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-1 | test5 | 100 | 0.018447 | correct | 10 | 58 | 58 | ok |
| local-search-variant-2 | test1 | 100 | 0.018027 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-2 | test2 | 100 | 0.039751 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-2 | test3 | 100 | 0.022061 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-2 | test4 | 100 | 0.068788 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-2 | test5 | 100 | 0.018875 | correct | 10 | 58 | 58 | ok |
| local-search-variant-3 | test1 | 100 | 0.018556 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-3 | test2 | 100 | 0.048182 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-3 | test3 | 100 | 0.024468 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-3 | test4 | 100 | 0.084896 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-3 | test5 | 100 | 0.017837 | correct | 10 | 58 | 58 | ok |
| local-search-variant-4 | test1 | 100 | 0.018197 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-4 | test2 | 100 | 0.047420 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-4 | test3 | 100 | 0.022453 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-4 | test4 | 100 | 0.105298 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-4 | test5 | 100 | 0.020116 | correct | 10 | 58 | 58 | ok |
| local-search-variant-5 | test1 | 100 | 0.019376 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-5 | test2 | 100 | 0.048501 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-5 | test3 | 100 | 0.025131 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-5 | test4 | 100 | 0.095635 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-5 | test5 | 100 | 0.019452 | correct | 10 | 58 | 58 | ok |
| local-search-variant-6 | test1 | 100 | 0.019791 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-6 | test2 | 100 | 0.054886 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-6 | test3 | 100 | 0.024711 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-6 | test4 | 100 | 0.103156 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-6 | test5 | 100 | 0.019113 | correct | 10 | 58 | 58 | ok |
| local-search-variant-7 | test1 | 100 | 0.019921 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-7 | test2 | 100 | 0.040692 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-7 | test3 | 100 | 0.021869 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-7 | test4 | 100 | 0.069221 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-7 | test5 | 100 | 0.019145 | correct | 10 | 58 | 58 | ok |
| local-search-variant-8 | test1 | 100 | 0.019009 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-8 | test2 | 100 | 0.039873 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-8 | test3 | 100 | 0.022282 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-8 | test4 | 100 | 0.068694 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-8 | test5 | 100 | 0.019493 | correct | 10 | 58 | 58 | ok |
| local-search-variant-9 | test1 | 100 | 0.019686 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-9 | test2 | 100 | 0.047110 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-9 | test3 | 100 | 0.022526 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-9 | test4 | 100 | 0.082210 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-9 | test5 | 100 | 0.018384 | correct | 10 | 58 | 58 | ok |
| local-search-variant-10 | test1 | 100 | 0.019160 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-10 | test2 | 100 | 0.049201 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-10 | test3 | 100 | 0.023387 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-10 | test4 | 100 | 0.087011 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-10 | test5 | 100 | 0.017170 | correct | 10 | 58 | 58 | ok |
| local-search-variant-11 | test1 | 100 | 0.019519 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-11 | test2 | 100 | 0.086599 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-11 | test3 | 100 | 0.029335 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-11 | test4 | 100 | 0.157512 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-11 | test5 | 100 | 0.019492 | correct | 10 | 58 | 58 | ok |
| local-search-variant-12 | test1 | 100 | 0.019253 | correct | 100 | 1020 | 1020 | ok |
| local-search-variant-12 | test2 | 100 | 0.118432 | correct | 5000 | 128868 | 127122 | ok |
| local-search-variant-12 | test3 | 100 | 0.033045 | correct | 1000 | 49589 | 48733 | ok |
| local-search-variant-12 | test4 | 100 | 0.226642 | correct | 10000 | 255386 | 250298 | ok |
| local-search-variant-12 | test5 | 100 | 0.020034 | correct | 10 | 58 | 58 | ok |
| dp-local-c80 | test1 | 100 | 0.018218 | correct | 100 | 1020 | 1020 | ok |
| dp-local-c80 | test2 | 100 | 0.069683 | correct | 5000 | 128868 | 127122 | ok |
| dp-local-c80 | test3 | 100 | 0.022549 | correct | 1000 | 49589 | 48733 | ok |
| dp-local-c80 | test4 | 100 | 0.122172 | correct | 10000 | 255386 | 250298 | ok |
| dp-local-c80 | test5 | 100 | 0.016973 | correct | 10 | 58 | 58 | ok |
| dp-local-c160 | test1 | 100 | 0.018236 | correct | 100 | 1020 | 1020 | ok |
| dp-local-c160 | test2 | 100 | 0.067192 | correct | 5000 | 128868 | 127122 | ok |
| dp-local-c160 | test3 | 100 | 0.023705 | correct | 1000 | 49589 | 48733 | ok |
| dp-local-c160 | test4 | 100 | 0.120607 | correct | 10000 | 255386 | 250298 | ok |
| dp-local-c160 | test5 | 100 | 0.016469 | correct | 10 | 58 | 58 | ok |
| dp-local-c320 | test1 | 100 | 0.017598 | correct | 100 | 1020 | 1020 | ok |
| dp-local-c320 | test2 | 100 | 0.064988 | correct | 5000 | 128868 | 127122 | ok |
| dp-local-c320 | test3 | 100 | 0.022990 | correct | 1000 | 49589 | 48733 | ok |
| dp-local-c320 | test4 | 100 | 0.116060 | correct | 10000 | 255386 | 250298 | ok |
| dp-local-c320 | test5 | 100 | 0.016815 | correct | 10 | 58 | 58 | ok |
| dp-traditional-c80-p1 | test1 | 100 | 0.016847 | correct | 100 | 1020 | 1020 | ok |
| dp-traditional-c80-p1 | test2 | 100 | 0.382254 | correct | 5000 | 128868 | 127122 | ok |
| dp-traditional-c80-p1 | test3 | 100 | 0.242793 | correct | 1000 | 49589 | 48733 | ok |
| dp-traditional-c80-p1 | test4 | 100 | 1.230455 | correct | 10000 | 255386 | 250298 | ok |
| dp-traditional-c80-p1 | test5 | 100 | 0.017095 | correct | 10 | 58 | 58 | ok |
| dp-traditional-c80-p2 | test1 | 100 | 0.016785 | correct | 100 | 1020 | 1020 | ok |
| dp-traditional-c80-p2 | test2 | 100 | 0.372357 | correct | 5000 | 128868 | 127122 | ok |
| dp-traditional-c80-p2 | test3 | 100 | 0.263555 | correct | 1000 | 49589 | 48733 | ok |
| dp-traditional-c80-p2 | test4 | 100 | 1.276025 | correct | 10000 | 255386 | 250298 | ok |
| dp-traditional-c80-p2 | test5 | 100 | 0.018336 | correct | 10 | 58 | 58 | ok |
| dp-traditional-c160-p1 | test1 | 100 | 0.024477 | correct | 100 | 1020 | 1020 | ok |
| dp-traditional-c160-p1 | test2 | 100 | 0.414893 | correct | 5000 | 128868 | 127122 | ok |
| dp-traditional-c160-p1 | test3 | 100 | 0.377993 | correct | 1000 | 49589 | 48733 | ok |
| dp-traditional-c160-p1 | test4 | 100 | 1.309325 | correct | 10000 | 255386 | 250298 | ok |
| dp-traditional-c160-p1 | test5 | 100 | 0.015721 | correct | 10 | 58 | 58 | ok |
| dp-traditional-c160-p2 | test1 | 100 | 0.018147 | correct | 100 | 1020 | 1020 | ok |
| dp-traditional-c160-p2 | test2 | 100 | 0.397399 | correct | 5000 | 128868 | 127122 | ok |
| dp-traditional-c160-p2 | test3 | 100 | 0.371300 | correct | 1000 | 49589 | 48733 | ok |
| dp-traditional-c160-p2 | test4 | 100 | 1.383910 | correct | 10000 | 255386 | 250298 | ok |
| dp-traditional-c160-p2 | test5 | 100 | 0.015897 | correct | 10 | 58 | 58 | ok |
| dp-traditional-c320-p1 | test1 | 100 | 0.017449 | correct | 100 | 1020 | 1020 | ok |
| dp-traditional-c320-p1 | test2 | 100 | 0.419790 | correct | 5000 | 128868 | 127122 | ok |
| dp-traditional-c320-p1 | test3 | 100 | 0.383406 | correct | 1000 | 49589 | 48733 | ok |
| dp-traditional-c320-p1 | test4 | 100 | 1.362909 | correct | 10000 | 255386 | 250298 | ok |
| dp-traditional-c320-p1 | test5 | 100 | 0.016164 | correct | 10 | 58 | 58 | ok |
| dp-traditional-c320-p2 | test1 | 100 | 0.017340 | correct | 100 | 1020 | 1020 | ok |
| dp-traditional-c320-p2 | test2 | 100 | 0.368777 | correct | 5000 | 128868 | 127122 | ok |
| dp-traditional-c320-p2 | test3 | 100 | 0.350813 | correct | 1000 | 49589 | 48733 | ok |
| dp-traditional-c320-p2 | test4 | 100 | 1.351885 | correct | 10000 | 255386 | 250298 | ok |
| dp-traditional-c320-p2 | test5 | 100 | 0.014644 | correct | 10 | 58 | 58 | ok |
| mip-time-3000 | test1 | 100 | 0.528347 | correct | 100 | 1020 | 1020 | ok |
| mip-time-3000 | test2 | 0 | 4.670745 | valid_but_below_reference | 0 | 0 | 127122 | ok |
| mip-time-3000 | test3 | 100 | 2.750518 | correct | 1000 | 49589 | 48733 | ok |
| mip-time-3000 | test4 | 0 | 6.522876 | valid_but_below_reference | 0 | 0 | 250298 | ok |
| mip-time-3000 | test5 | 100 | 0.128390 | correct | 10 | 58 | 58 | ok |
| mip-time-8000 | test1 | 100 | 0.135632 | correct | 100 | 1020 | 1020 | ok |
| mip-time-8000 | test2 | 100 | 10.980217 | correct | 4960 | 127851 | 127122 | ok |
| mip-time-8000 | test3 | 100 | 3.277932 | correct | 1000 | 49589 | 48733 | ok |
| mip-time-8000 | test4 | 0 | 11.855109 | valid_but_below_reference | 0 | 0 | 250298 | ok |
| mip-time-8000 | test5 | 100 | 0.099300 | correct | 10 | 58 | 58 | ok |
| mip-time-15000 | test1 | 100 | 0.121241 | correct | 100 | 1020 | 1020 | ok |
| mip-time-15000 | test2 | 100 | 15.038823 | correct | 4990 | 128717 | 127122 | ok |
| mip-time-15000 | test3 | 100 | 2.919911 | correct | 1000 | 49589 | 48733 | ok |
| mip-time-15000 | test4 | 100 | 19.030356 | correct | 9901 | 252770 | 250298 | ok |
| mip-time-15000 | test5 | 100 | 0.113020 | correct | 10 | 58 | 58 | ok |
| mip-divisor-4 | test1 | 100 | 0.155187 | correct | 100 | 1020 | 1020 | ok |
| mip-divisor-4 | test2 | 100 | 10.903870 | correct | 4960 | 127851 | 127122 | ok |
| mip-divisor-4 | test3 | 100 | 3.283294 | correct | 1000 | 49589 | 48733 | ok |
| mip-divisor-4 | test4 | 0 | 13.136458 | valid_but_below_reference | 0 | 0 | 250298 | ok |
| mip-divisor-4 | test5 | 100 | 0.114717 | correct | 10 | 58 | 58 | ok |
| mip-divisor-6 | test1 | 100 | 0.110497 | correct | 100 | 1020 | 1020 | ok |
| mip-divisor-6 | test2 | 100 | 11.007136 | correct | 4960 | 127851 | 127122 | ok |
| mip-divisor-6 | test3 | 100 | 2.768203 | correct | 1000 | 49589 | 48733 | ok |
| mip-divisor-6 | test4 | 0 | 11.728446 | valid_but_below_reference | 0 | 0 | 250298 | ok |
| mip-divisor-6 | test5 | 100 | 0.095929 | correct | 10 | 58 | 58 | ok |
| mip-divisor-10 | test1 | 100 | 0.113593 | correct | 100 | 1020 | 1020 | ok |
| mip-divisor-10 | test2 | 100 | 10.061560 | correct | 4960 | 127851 | 127122 | ok |
| mip-divisor-10 | test3 | 100 | 2.568085 | correct | 1000 | 49589 | 48733 | ok |
| mip-divisor-10 | test4 | 0 | 10.046997 | valid_but_below_reference | 0 | 0 | 250298 | ok |
| mip-divisor-10 | test5 | 100 | 0.088372 | correct | 10 | 58 | 58 | ok |
| cp-time-3.0 | test1 | 100 | 1.012986 | correct | 100 | 1020 | 1020 | ok |
| cp-time-3.0 | test2 | 0 | 3.760669 | valid_but_below_reference | 0 | 0 | 127122 | ok |
| cp-time-3.0 | test3 | 100 | 1.261385 | correct | 1000 | 49589 | 48733 | ok |
| cp-time-3.0 | test4 | 0 | 5.321520 | valid_but_below_reference | 0 | 0 | 250298 | ok |
| cp-time-3.0 | test5 | 100 | 0.578822 | correct | 10 | 58 | 58 | ok |
| cp-time-8.0 | test1 | 100 | 0.482655 | correct | 100 | 1020 | 1020 | ok |
| cp-time-8.0 | test2 | 100 | 6.438640 | correct | 5000 | 128868 | 127122 | ok |
| cp-time-8.0 | test3 | 100 | 1.678451 | correct | 1000 | 49589 | 48733 | ok |
| cp-time-8.0 | test4 | 0 | 8.849704 | valid_but_below_reference | 0 | 0 | 250298 | ok |
| cp-time-8.0 | test5 | 100 | 0.423051 | correct | 10 | 58 | 58 | ok |
| cp-time-15.0 | test1 | 100 | 0.480218 | correct | 100 | 1020 | 1020 | ok |
| cp-time-15.0 | test2 | 100 | 5.968153 | correct | 5000 | 128868 | 127122 | ok |
| cp-time-15.0 | test3 | 100 | 1.627263 | correct | 1000 | 49589 | 48733 | ok |
| cp-time-15.0 | test4 | 100 | 20.350981 | correct | 10000 | 255386 | 250298 | ok |
| cp-time-15.0 | test5 | 100 | 1.270063 | correct | 10 | 58 | 58 | ok |
| cp-divisor-4 | test1 | 100 | 0.702276 | correct | 100 | 1020 | 1020 | ok |
| cp-divisor-4 | test2 | 100 | 6.826365 | correct | 5000 | 128868 | 127122 | ok |
| cp-divisor-4 | test3 | 100 | 1.510825 | correct | 1000 | 49589 | 48733 | ok |
| cp-divisor-4 | test4 | 0 | 11.925572 | valid_but_below_reference | 0 | 0 | 250298 | ok |
| cp-divisor-4 | test5 | 100 | 0.634743 | correct | 10 | 58 | 58 | ok |
| cp-divisor-6 | test1 | 100 | 0.508782 | correct | 100 | 1020 | 1020 | ok |
| cp-divisor-6 | test2 | 100 | 6.391913 | correct | 5000 | 128868 | 127122 | ok |
| cp-divisor-6 | test3 | 100 | 1.728819 | correct | 1000 | 49589 | 48733 | ok |
| cp-divisor-6 | test4 | 0 | 8.662319 | valid_but_below_reference | 0 | 0 | 250298 | ok |
| cp-divisor-6 | test5 | 100 | 0.680366 | correct | 10 | 58 | 58 | ok |
| cp-divisor-10 | test1 | 100 | 0.734739 | correct | 100 | 1020 | 1020 | ok |
| cp-divisor-10 | test2 | 100 | 6.166623 | correct | 5000 | 128868 | 127122 | ok |
| cp-divisor-10 | test3 | 100 | 1.473064 | correct | 1000 | 49589 | 48733 | ok |
| cp-divisor-10 | test4 | 0 | 12.099526 | valid_but_below_reference | 0 | 0 | 250298 | ok |
| cp-divisor-10 | test5 | 100 | 0.447706 | correct | 10 | 58 | 58 | ok |

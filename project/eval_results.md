# Evaluation Results

Scoring rule: each valid solution whose objective value is at least the reference answer earns 100 points.

| Method | Total score | Total time (s) | Correct tests | Hyperparameters |
| --- | ---: | ---: | ---: | --- |
| greedy | 500 | 0.199309 | 5/5 | `REPAIR_FILL_ROUNDS` = `2`<br>`GREEDY_ORDER` = `(e_i - s_i, e_i, -d_i)`<br>`BEST_DAY_RULE` = `choose feasible day with largest current load`<br>`REPAIR_MEMBER_ORDER` = `d_i ascending`<br>`FILL_ORDER` = `(-d_i, e_i - s_i, e_i)`<br>`NEW_DAY_FILL_RULE` = `stop opening a new day when total >= min_load` |
| local_search | 500 | 0.210729 | 5/5 | `INITIAL_REPAIR_FILL_ROUNDS` = `2`<br>`MAX_LOCAL_SEARCH_ROUNDS` = `5`<br>`LOCAL_SEARCH_ORDER` = `-d_i`<br>`INSERTION_RULE` = `insert into active day, or open a day if d_i >= min_load`<br>`BEST_DAY_RULE` = `choose feasible day with largest current load`<br>`GREEDY_ORDER` = `(e_i - s_i, e_i, -d_i)`<br>`REPAIR_MEMBER_ORDER` = `d_i ascending`<br>`FILL_ORDER` = `(-d_i, e_i - s_i, e_i)` |
| MIP | 500 | 40.521791 | 5/5 | `SHORT_WINDOW_LIMIT` = `12`<br>`LONG_WINDOW_DIVISOR` = `6`<br>`MANDATORY_CANDIDATE_DAYS` = `s, e, (s + e) // 2`<br>`MIP_SOLVER` = `SCIP`<br>`TIME_LIMIT_MS` = `15000`<br>`INTEGER_THRESHOLD` = `0.5` |
| CP | 500 | 34.306020 | 5/5 | `SHORT_WINDOW_LIMIT` = `12`<br>`LONG_WINDOW_DIVISOR` = `6`<br>`MANDATORY_CANDIDATE_DAYS` = `s, e, (s + e) // 2`<br>`max_time_in_seconds` = `15.0`<br>`num_search_workers` = `8` |
| DP | 500 | 0.286280 | 5/5 | `INITIAL_REPAIR_FILL_ROUNDS` = `2`<br>`DP_CANDIDATE_LIMIT` = `160`<br>`DP_CANDIDATE_ORDER` = `(-d_i, e_i - s_i)`<br>`GREEDY_ORDER` = `(e_i - s_i, e_i, -d_i)`<br>`FILL_ORDER` = `(-d_i, e_i - s_i, e_i)`<br>`REPAIR_MEMBER_ORDER` = `d_i ascending` |

## Per-Test Details

| Method | Test | Score | Time (s) | Status | Selected | Value | Reference | Message |
| --- | --- | ---: | ---: | --- | ---: | ---: | ---: | --- |
| greedy | test1 | 100 | 0.023830 | correct | 100 | 1020 | 1020 | ok |
| greedy | test2 | 100 | 0.045345 | correct | 5000 | 128868 | 127122 | ok |
| greedy | test3 | 100 | 0.027015 | correct | 1000 | 49589 | 48733 | ok |
| greedy | test4 | 100 | 0.085024 | correct | 10000 | 255386 | 250298 | ok |
| greedy | test5 | 100 | 0.018096 | correct | 10 | 58 | 58 | ok |
| local_search | test1 | 100 | 0.019487 | correct | 100 | 1020 | 1020 | ok |
| local_search | test2 | 100 | 0.051384 | correct | 5000 | 128868 | 127122 | ok |
| local_search | test3 | 100 | 0.031097 | correct | 1000 | 49589 | 48733 | ok |
| local_search | test4 | 100 | 0.088347 | correct | 10000 | 255386 | 250298 | ok |
| local_search | test5 | 100 | 0.020414 | correct | 10 | 58 | 58 | ok |
| MIP | test1 | 100 | 0.304297 | correct | 100 | 1020 | 1020 | ok |
| MIP | test2 | 100 | 17.172835 | correct | 4991 | 128716 | 127122 | ok |
| MIP | test3 | 100 | 3.402965 | correct | 1000 | 49589 | 48733 | ok |
| MIP | test4 | 100 | 19.500062 | correct | 9901 | 252770 | 250298 | ok |
| MIP | test5 | 100 | 0.141631 | correct | 10 | 58 | 58 | ok |
| CP | test1 | 100 | 0.765879 | correct | 100 | 1020 | 1020 | ok |
| CP | test2 | 100 | 7.789958 | correct | 5000 | 128868 | 127122 | ok |
| CP | test3 | 100 | 2.044702 | correct | 1000 | 49589 | 48733 | ok |
| CP | test4 | 100 | 22.765981 | correct | 10000 | 255386 | 250298 | ok |
| CP | test5 | 100 | 0.939501 | correct | 10 | 58 | 58 | ok |
| DP | test1 | 100 | 0.022027 | correct | 100 | 1020 | 1020 | ok |
| DP | test2 | 100 | 0.073827 | correct | 5000 | 128868 | 127122 | ok |
| DP | test3 | 100 | 0.026035 | correct | 1000 | 49589 | 48733 | ok |
| DP | test4 | 100 | 0.142865 | correct | 10000 | 255386 | 250298 | ok |
| DP | test5 | 100 | 0.021525 | correct | 10 | 58 | 58 | ok |

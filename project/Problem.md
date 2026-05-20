Cho bài toán sau:
# Project Problem 

## Description
There are $N$ fields $1, 2, . . ., N$ that grow the same agricultural product. The field `i` has amount of product `d(i)` and needs to be harvested on one day from `s(i)` to `e(i)`. The processing factory has the capacity $M$ which is the maximum amount of product it can process each day. Moreover, if the total amount of product available is less than m, the factory will not work (as the efficiency is not good). 
A field can be selected to be harvested or not. Compute a plan for harvesting the product such that the total amount of product harvested in the plan is maximal.
A solution is represented by `x{1], x[2],  . . ., x[N]` in which `x[i]` is the day the field $i$ is harvested, and `x[i] = -1` if the field is not harvested. \

Input \
Line 1: contains 3 positive integers `N, m, M (1 <= N <= 10000, 1 <= m <= M <= 10000)` \
Line `i+1 (i = 1, 2, . . ., N)`: contains 3 positive integers `d(i)`, `s(i)` and `e(i)`   `(1 <= d(i) <= 100, 1 <= s(i) <= e(i) <= 10000)` \

Output \
Line 1: contains an integer M which is the number of fields being harvested \
Each subsequent line contains i and x(i) (separated by a SPACE character) in case `x[i] > 0  (i = 1, 2, . . . , N)`

#### Example

Input
```
10 7 24 
8 3 7 
8 2 6 
4 2 6 
8 1 4 
7 3 7 
7 1 4 
1 1 4 
2 1 4 
6 1 4 
7 1 3
```
Output
```
10
1 3
2 3
3 3
4 1
5 4
6 1
7 3
8 3
9 1
10 2
```
#include <bits/stdc++.h>
using namespace std;

int N, m, M;
int d[10001], s[10001], e[10001];
/*
N: number of fields
m/M: min/max capacity each day
s[i], e[i]: start and end harvest timeline of field i
d[i]: capacity of field i

*/

struct Sol {
    int x[10001];
    int total() {
        int t = 0;
        for (int i = 0; i < N; i++) if (x[i] != -1) t += d[i];
        return t;
    }
};

Sol greedySolve(vector<int>& order) {
    Sol sol;
    memset(sol.x, -1, sizeof(int) * N);
    unordered_map<int,int> loads;
    for (int i : order) {0
        int bestDay = -1, bestLoad = -1;
        for (int t = s[i]; t <= e[i]; t++) {
            int cur = loads[t];
            if (cur + d[i] <= M) {
                if (cur > 0 && (bestDay == -1 || cur > bestLoad))
                    { bestDay = t; bestLoad = cur; }
                else if (bestDay == -1)
                    { bestDay = t; bestLoad = 0; }
            }
        }
        if (bestDay != -1) { sol.x[i] = bestDay; loads[bestDay] += d[i]; }
    }
    for (auto& [t, ld] : loads) {
        if (ld > 0 && ld < m) {
            for (int i = 0; i < N; i++) {
                if (sol.x[i] != t) continue;
                for (int t2 = s[i]; t2 <= e[i]; t2++) {
                    if (t2 == t) continue;
                    if (loads[t2] > 0 && loads[t2] + d[i] <= M) {
                        sol.x[i] = t2; loads[t] -= d[i]; loads[t2] += d[i];
                        break;
                    }
                }
            }
        }
    }
    for (auto& [t, ld] : loads) {
        if (ld > 0 && ld < m) {
            for (int i = 0; i < N; i++) if (sol.x[i] == t) sol.x[i] = -1;
            ld = 0;
        }
    }
    for (int i = 0; i < N; i++) {
        if (sol.x[i] != -1) continue;
        for (int t = s[i]; t <= e[i]; t++) {
            int cur = loads[t];
            if (cur > 0 && cur + d[i] <= M && cur + d[i] >= m) {
                sol.x[i] = t; loads[t] += d[i]; break;
            }
        }
    }
    return sol;
}

int main() {
    ios::sync_with_stdio(false); cin.tie(0);
    cin >> N >> m >> M;
    for (int i = 0; i < N; i++) cin >> d[i] >> s[i] >> e[i];
    Sol best; memset(best.x, -1, sizeof(int) * N); // Solution, initial with all -1
    int bestVal = 0;
    vector<int> order(N); iota(order.begin(), order.end(), 0);
    sort(order.begin(), order.end(), [](int a, int b){ return d[a] > d[b]; }); // Sort by capacity of each field (decreasing)
    Sol sol = greedySolve(order);
    if (sol.total() > bestVal) { best = sol; bestVal = sol.total(); }
    sort(order.begin(), order.end(), [](int a, int b){ return e[a]-s[a] < e[b]-s[b]; }); // Sort by time to harvest (increasing)
    sol = greedySolve(order);
    if (sol.total() > bestVal) { best = sol; bestVal = sol.total(); }
    sort(order.begin(), order.end(), [](int a, int b){
        return (double)d[a]/(e[a]-s[a]+1) > (double)d[b]/(e[b]-s[b]+1); // Sort by capacity per day 
    });
    sol = greedySolve(order);
    if (sol.total() > bestVal) { best = sol; bestVal = sol.total(); }
    int cnt = 0;
    for (int i = 0; i < N; i++) if (best.x[i] != -1) cnt++;
    cout << cnt << "\n";
    for (int i = 0; i < N; i++)
        if (best.x[i] != -1) cout << i + 1 << " " << best.x[i] << "\n";
    return 0;
}

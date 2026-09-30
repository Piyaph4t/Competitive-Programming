#include <bits/stdc++.h>
#include <numeric>
#include <utility>
using namespace std;

#define fi first
#define se second
int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<pair<int, int>> vec(n);
    int ans[n];
    vector<int> a, b;
    a.reserve(n);
    b.reserve(n);
    for (int i = 0; i < n; ++i) {
        cin >> vec[i].fi;
        ans[i] = vec[i].fi;
        vec[i].se = i;
    }

    sort(vec.begin(), vec.end(), greater<pair<int, int>>());

    for (int i = 0; i + 1 < n; i += 2) {
        pair<int, int> mx, mn;
        mx = max(vec[i], vec[i + 1]);
        mn = min(vec[i], vec[i + 1]);

        if (accumulate(a.begin(), a.end(), 0) > accumulate(b.begin(), b.end(), 0)) {
            a.push_back(mn.se);
            b.push_back(mx.se);
        } else {
            a.push_back(mx.se);
            b.push_back(mn.se);
        }
    }
    for (int& x : a)
        cout << ans[x] << " ";
    cout << "\n";
    for (int& x : b)
        cout << ans[x] << " ";
    cout << "\n";
    return 0;
}

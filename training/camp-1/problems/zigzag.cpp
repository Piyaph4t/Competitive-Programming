#include <algorithm>
#include <bits/stdc++.h>
using namespace std;

int odd_even[100010];
int main() {

    int n;
    int m = -1;
    do {
        cin >> n;
        odd_even[++m] = n % 2;
    } while (n > 0);
    int ans = 0;
    int cnt = 0;
    for (int i = 0; i + 1 < m; i++) {

        if (odd_even[i] != odd_even[i + 1]) {
            cnt++;
            ans = max(ans, cnt);
        } else {
            cnt = 0;
        }
    }
    cout << (ans+1) /2 << "\n";
    return 0;
}

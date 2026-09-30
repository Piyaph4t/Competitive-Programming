#include <algorithm>
#include <bits/stdc++.h>

using namespace std;

typedef long long ll;

int cnt[256];
bool is_pair[256];
int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);
    string s;
    cin >> s;

    for (char& x : s)
        cnt[(int)x]++;

#ifdef DEBUG
    for (int c = 'A'; c <= 'Z'; ++c) {
        if (cnt[c]) cout << (char)c << ": " << cnt[c] << "\n";
    }
#endif
    string p;
    bool found_odd = false;
    char odd_char = 0;
    for (int i = 'A'; i <= 'Z'; ++i) {
        if (cnt[i] == 0) continue;

        if (cnt[i] % 2) {
            if (found_odd) {
                cout << "NO SOLUTION";
                return 0;
            }
            found_odd = true;
            odd_char = (char)i;
#ifdef DEBUG
            cout << "Odd_char => " << odd_char << "\n";
#endif
        }
        p += string(cnt[i] / 2, (char)i);
    }
    cout << p;
    if (odd_char) cout << odd_char;
    reverse(p.begin(), p.end());
    cout << p;
    cout << "\n";
    return 0;
}

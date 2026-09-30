#include <bits/stdc++.h>
using namespace std;
void solve() {
    int n,k; cin >> n >> k;
    int ps[n+ 10];
    memset(ps, 0, (n+10)*sizeof(int));
    string s ; cin >> s ;
    for(int i=1;i<=n ;i++){
        if(s[i-1] == 'W') ps[i]++;
        ps[i]+=ps[i-1];
    }
    #ifdef DEBUG
    cout << "\n";
    for(int i=0;i <= n; i++) {
        cout << ps[i] << " ";
    }
    cout << "\n";
    #endif
    int ans = INT_MAX;
    for(int i=0;i<=n-k;i++){
        ans = min(ans, ps[i+k] - ps[i]);
    }
    #ifdef DEBUG
    cout << "ans: ";
    #endif
    cout << ans << "\n";
}

int main(){
    int t=1;
    cin >> t;
    while(t--){
        solve();
    }
    return 0;
}

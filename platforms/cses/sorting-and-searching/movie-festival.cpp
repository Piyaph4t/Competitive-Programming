#include <bits/stdc++.h>
using namespace std;

#define fi first
#define se second
int main(){
    ios_base::sync_with_stdio(0), cin.tie(nullptr);

    int n ; cin >> n;
    vector<pair<int,int>> vec(n);
    for(auto &[a,b]: vec)
        cin >> a >> b;

    auto comp = [](const pair<int,int> &a,const  pair<int,int> &b){
        if( a.se != b.se )
            return a.se < b.se;
        return a.fi > b.fi;
    };

    #ifdef DEBUG
        for(auto &[a,b] : vec){
            printf("start: %d, end: %d\n", a, b);
        }
    #endif

    sort(vec.begin(), vec.end(), comp);

    int ans = 0, curr = -1;
    for(int i=0;i < n;i++){
        if(curr <= vec[i].fi){
            ans++;
            curr = vec[i].se;
        }
    }
    cout << ans << "\n";
    return 0;
}

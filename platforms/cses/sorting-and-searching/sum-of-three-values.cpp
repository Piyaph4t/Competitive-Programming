#include <algorithm>
#include <cstdio>
#include <iostream>
#include <vector>
using namespace std;
#define fi first

typedef long long ll ;

#define se second
int main(){
    ll n, x ; cin >> n >> x;
    vector<pair<ll,ll>> arr(n);
    for(int i=0; i<n;++i ){
        cin >> arr[i].fi;
        arr[i].se = i;
    }

    sort(arr.begin(), arr.end());

    for(int i=0; i<n ;i++){
        for(int j=i+1; j < n;++j ){

            ll sum = arr[i].fi + arr[j].fi;
            if(sum >= x)
                break;
            ll target = x - sum;
            auto it =
                lower_bound(arr.begin()+j+1, arr.end(), target,
                    [](const pair<ll,ll> &a, const ll &b) {return a.fi < b;});

            if(it == arr.end())
                continue;
            if((*it).fi + sum == x) {
                ll ans[] = { arr[i].se+1, arr[j].se+1, (*it).se+1};
                sort(ans, ans+3);
                printf("%lld %lld %lld\n", ans[0], ans[1], ans[2]);
                return 0;
            }
        }
    }
    cout << "IMPOSSIBLE\n";
    return 0;
}

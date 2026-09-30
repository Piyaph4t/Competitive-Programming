#include <bits/stdc++.h>


using namespace std;
typedef long long ll;


const int maxn = 2e5 + 10;
ll prefix[maxn];
ll n,m;
void ask(){
    ll b;cin >> b;
    ll low = 0, high = n, mid;
    ll room = 0;
    while(low <= high) {
        mid = low + (high - low)/2;
        if( prefix[mid] >= b){
            room = mid;
            high = mid - 1;
        }else {
            low = mid + 1;
        }
    }
    //  #ifdef DEBUG
    //  printf("low:%d mid:%d high:%d\n", low, mid, high);
    //  #endif
    printf("%lld %lld\n" , room , b - prefix[room - 1]);
}
int main(){
    cin.tie(nullptr)->sync_with_stdio(0);

    cin >> n >> m;
    ll a;
    for(int i=1;i<=n;i++){
        cin >> a;
        prefix[i] = prefix[i-1] + a;
    }


    while(m--){
        ask();
    }
    return 0;
}

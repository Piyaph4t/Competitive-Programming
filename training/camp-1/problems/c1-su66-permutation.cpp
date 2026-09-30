#include <bits/stdc++.h>
using namespace std;

int main(){
    int n; string s;
    cin >> n >> s;
    long long ans = 0, fac = 1;
    int i=0;

    for(int i=0;i<n;i++){
        int c = 0;
        for(int j=0;j<n-i-1;j++)
            if(s[n-i-1]>s[j]) c++;
        ans += abs(s[n-i-1] - 'A' - c ) * fac;
        fac*= (i+1);
    }
    cout << ++ans << "\n";
    return 0;
}

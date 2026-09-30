#include <stdint.h>
#include <stdio.h>
int reverse(int x){
    long long ans = 0;
    long long sign = 1;
    int mx = (int)2e31;
    int mn = (int)(-2e31 - 1);
    if (x<0)
        sign = -1;
    x*=sign;

    while(x > 0){
        ans = ans * 10 + x%10;
        if(ans > mx || ans * -1 <= mn)
            return 0;
        x/=10;
    }
    return ans*sign;
}
int main(){
    printf("%d", reverse(-321));
}

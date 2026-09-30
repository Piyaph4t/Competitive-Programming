#include <stdio.h>
#include <stdlib.h>

int comp(const void* a, const void* b) {
    return *(int*)a - *(int*)b;
}
int main() {
    int n;
    scanf("%d", &n);
    int coin[n];
    for (int i = 0; i < n; scanf("%d", coin + i++))
        ;
    qsort(coin, n, sizeof(*coin), comp);
    long long reach  = 0;

    for(int i=0;i<n;++i){
        if(coin[i] > reach + 1){
            printf("%lld\n", reach + 1);
            return 0;
        }
        reach += coin[i];
    }

    printf("%lld\n", reach + 1);
    return 0;
}

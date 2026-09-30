#include <stdio.h>
#include <stdlib.h>

typedef long long ll;

int comp(const void* a, const void* b) {
    return *(ll*)a - *(ll*)b;
}

int main() {
    size_t n;
    scanf("%zu", &n);
    ll arr[n];
    for (int i = 0; i < n; scanf("%lld", arr + i++))
        ;
    qsort(arr, n, sizeof(*arr), comp);

    ll median = arr[(n + 1) / 2 - 1];
    if (n % 2 == 0) {
        median += arr[(n + 1) / 2 ];
        median /= 2;
    }
    #ifdef DEBUG
        printf("median: %lld\n", median);
    #endif
    ll ans = 0;
    for (int i = 0; i < n; i++) {
        ans += llabs(median - arr[i]);
    }

    printf("%lld\n", ans);
    return 0;
}

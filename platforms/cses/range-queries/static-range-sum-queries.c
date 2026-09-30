#include <stdio.h>

typedef unsigned long long ull ;
ull prefix_sum[(int)2e5 + 1];
int main() {
    int n, q;
    scanf("%d%d", &n, &q);
    ull a, b;
    for (int i = 1; i <= n; i++) {
        scanf("%d", &a);
        prefix_sum[i] = prefix_sum[i - 1] + a;
    }
    while (q--) {
        scanf("%lld%lld", &a, &b);
        printf("%lld\n", prefix_sum[b] - prefix_sum[a - 1]);
    }

    return 0;
}

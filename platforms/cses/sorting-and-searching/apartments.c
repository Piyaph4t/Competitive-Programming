#include <math.h>
#include <stdio.h>
#include <stdlib.h>

typedef long long ll;
int comp(const void* a, const void* b) {
    return *(ll*)a - *(ll*)b;
}
int main() {
    int n, m, k;
    scanf("%d%d%d", &n, &m, &k);
    ll app[n], apr[m];
    for (int i = 0; i < n; i++)
        scanf("%llu", app + i);

    for (int i = 0; i < m; i++)
        scanf("%llu", apr + i);

    qsort(app, n, sizeof(app[0]), comp);
    qsort(apr, m, sizeof(apr[0]), comp);

    ll ans = 0;
    int i = 0, j = 0;
    while (i < n && j < m) {
        if (llabs(app[i] - apr[j]) <= k)
            ++i, ++j, ++ans;
        else if (app[i] > apr[j])
            j++;
        else
            ++i;
    }
    printf("%lld\n", ans);
    return 0;
}

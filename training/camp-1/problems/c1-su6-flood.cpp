
#include <cstring>
#include <stdio.h>
#define max(a, b) (((a) > (b)) ? (a) : (b))
#define min(a, b) (((a) < (b)) ? (a) : (b))
int main() {

    int n;
    scanf("%d", &n);
    int h[n], l[n], r[n];
    memset(h, 0, n * sizeof(int));
    memset(l, 0, n * sizeof(int));
    memset(r, 0, n * sizeof(int));
    for (int i = 0; i < n; ++i) {
        scanf("%d", h + i);
    }
    l[0] = h[0];
    r[n - 1] = h[n - 1];
    for (int i = 1; i < n; i++) {
        l[i] = max(l[i - 1], h[i]);
        r[n - i - 1] = max(r[n - i], h[n - i - 1]);
    }
    int water = 0;
    for (int i = 0; i < n; i++) {
        water += min(r[i], l[i]) - h[i];
    }
    printf("%d\n", water);
    return 0;
}

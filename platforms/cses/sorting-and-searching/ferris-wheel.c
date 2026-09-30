#include <stdio.h>
#include <stdlib.h>

int comp(const void* a, const void* b) {
    return *(int*)a - *(int*)b;
}

int main() {
    int n, x;
    scanf("%d%d", &n, &x);
    int w[n];
    for (int i = 0; i < n; scanf("%d", w + i++))
        ;
    qsort(w, n, sizeof(int), comp);

    int low = 0, high = n - 1;
    int count = 0;
    while (low <= high) {

        if (w[high] + w[low] <= x) low++;
        high--;
        count++;
    }
    printf("%d\n", count);
    return 0;
}

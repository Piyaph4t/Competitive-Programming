#include <stdio.h>
#include <stdlib.h>

int comp(const void* a, const void* b) {
    return *(int*)a - *(int*)(b);
}
int main() {
    int n;
    scanf("%d", &n);
    int arr[n];
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

#ifdef DEBUG
    for (int i = 0; i < n; i++) {
        printf("%d ,", arr[i]);
    }
#endif

    // sort
    qsort(arr, n, sizeof(int), comp);
    int c = 1;
    for (int i = 0; i < n - 1; i++) {
        if (arr[i] != arr[i + 1]) {
            c++;
            // printf("arr[%d]: %d\n", i, arr[i]);
        }
    }

    printf("%d\n", c);
    return 0;
}

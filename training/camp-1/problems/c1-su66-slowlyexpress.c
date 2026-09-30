#include <stdio.h>
#include <stdlib.h>
int main() {
    int n = 0;
    int total = 0;
    for (;;) {
        scanf("%d", &n);
        if (n < 0) break;
        total += n;
        int car = total / 800;
        total -= car * 800;
        if (total >= 500) {

            total /= 800;
            car++;
        }
        printf("%d\n", car);
    }

    return 0;
}

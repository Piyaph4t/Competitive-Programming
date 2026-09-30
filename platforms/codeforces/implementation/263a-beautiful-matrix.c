#include <stdio.h>
#include <stdlib.h>
int main() {
    int move = 0;
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            int n;
            scanf("%d", &n);
            if (n) {
               printf("%d\n", abs(2-j) + abs(2-i));
               return 0;
            }
        }
    }
    return 0;
}

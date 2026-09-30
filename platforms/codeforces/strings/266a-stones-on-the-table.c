#include <stdlib.h>
#include <stdio.h>

int main() {
    int n;
    char c[51];
    memset(c, 0, sizeof(c));
    scanf("%d%s", &n, c);
    int count = 0;

    char* s = c;
    while (*s) {
        char* sc = s;
        while (*s && *s == *(s + 1)) {
            s++;
        }
        count += s - sc;
        s++;
    }
    printf("%d\n", count);
    return 0;
}

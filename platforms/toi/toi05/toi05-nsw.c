/**
 * TASK: NSW
 * LANG: C
 * AUTHOR: Piyaphat Jaiboon
 * CENTER: Silapakorn
 */


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>
#include <float.h>
#include <math.h>
#include <inttypes.h>

typedef int32_t  i32;
typedef uint32_t u32;
typedef int64_t  i64;
typedef uint64_t u64;
typedef double   f64;

#define MOD 1000000007LL

#define loop(i, n) for (i64 i = 0; i < (i64)(n); ++i)
#define range(i, start, end) for (i64 i = (i64)(start); i <= (i64)(end); ++i)
#define rev_range(i, start, end) for (i64 i = (i64)(start); i >= (i64)(end); --i)

#define min_val(a, b) ((a) < (b) ? (a) : (b))
#define max_val(a, b) ((a) > (b) ? (a) : (b))

static inline i64 read_i64(void) {
    i64 x = 0;
    int sign = 1;
    char ch = getchar();
    while (ch < '0' || ch > '9') {
        if (ch == '-') sign = -1;
        ch = getchar();
    }
    while (ch >= '0' && ch <= '9') {
        x = x * 10 + (ch - '0');
        ch = getchar();
    }
    return x * sign;
}

static inline i32 read_i32(void) {
    return (i32)read_i64();
}

// ============================================================================
// OVERFLOW-SAFE QSORT COMPARATORS
// ============================================================================
#define USE_QSORT 0
#if (USE_QSORT)
int compare_i64_asc(const void *a, const void *b) {
    i64 arg1 = *(const i64 *)a;
    i64 arg2 = *(const i64 *)b;
    return (arg1 > arg2) - (arg1 < arg2);
}

int compare_i64_desc(const void *a, const void *b) {
    return compare_i64_asc(b, a);
}

int compare_i32_asc(const void *a, const void *b) {
    i32 arg1 = *(const i32 *)a;
    i32 arg2 = *(const i32 *)b;
    return (arg1 > arg2) - (arg1 < arg2);
}

int compare_i32_desc(const void *a, const void *b) {
    return compare_i32_asc(b, a);
}
#endif

void solve() {

}

int main(void) {
    bool multi_test_cases = false;

    i32 test_cases = 1;
    if (multi_test_cases)
        test_cases = read_i32();

    while(test_cases--) {
        solve();
    }

    return 0;
}

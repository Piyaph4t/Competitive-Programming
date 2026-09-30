/*
TASK: ROI
LANG: C
AUTHOR: Piyaphat Jaiboon
CENTER: Silapakon
*/
#include <float.h>
#include <inttypes.h>
#include <math.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// ============================================================================
// DEV-STYLE FIXED-WIDTH TYPE ALIASES
// ============================================================================
typedef int32_t i32;
typedef uint32_t u32;
typedef int64_t i64;
typedef uint64_t u64;
typedef double f64;

#define MOD 1000000007LL

// ============================================================================
// OVERFLOW-SAFE LOOPS & UTILITIES
// ============================================================================
#define loop(i, n) for (size_t i = 0; i < (size_t)(n); ++i)
#define range(i, start, end) for (size_t i = (size_t)(start); i <= (size_t)(end); ++i)
#define rev_range(i, start, end) \
  for (size_t i = (size_t)(start); i >= (size_t)(end); --i)

#define min_val(a, b) ((a) < (b) ? (a) : (b))
#define max_val(a, b) ((a) > (b) ? (a) : (b))

// ============================================================================
// FAST & OVERFLOW-SAFE I/O
// ============================================================================
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

static inline i32 read_i32(void) { return (i32)read_i64(); }

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

// ============================================================================
// MAIN SOLUTION LOGIC
// ============================================================================

void solve() {
  f64 C;
  f64 sale_price = 0.0;
  f64 min_profit = DBL_MAX;
  i32 ans_cost = 0 ;
  i32 ans_nbook = 0;
  C = read_i32();

  for (i32 n_book = 1000; n_book <= 15000; n_book += 500) {
    for (i32 cost = 74; cost <= 144; cost++) {
        f64 dy_cost = n_book * (100 - (n_book-1000)/500);
        f64 totol_cost = C + dy_cost;
        f64 sold_book =( (100 - ( 0.8569 * exp(((f64)cost-100.0) * 0.09)) ) * n_book * 0.01);
        f64 profit = sold_book * cost - totol_cost;
        if(profit > 0 && profit < min_profit) {
            min_profit = profit;
            ans_cost = cost;
            ans_nbook = n_book;
        }
    }
  }
  printf("%d\n%d\n%.2lf\n", ans_nbook, ans_cost, min_profit);
}

int main(void) {
  bool multi_test_cases = false;

  i32 test_cases = 1;
  if (multi_test_cases) test_cases = read_i32();

  while (test_cases--) {
    solve();
  }

  return 0;
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char abacus[10][18];
int main() {
  int n;
  scanf("%d", &n);

  for (int i = 0; i < 10; i++)
    strcpy(abacus[i], "********");
  strcpy(abacus[3], "-----------------");
  strcpy(abacus[2], "                 ");
  strcpy(abacus[4], "                 ");

  int col = 7;
  while (n) {
    int digit = n % 10;
    if (digit >= 5) {
      abacus[1][col] = ' ';
      abacus[2][col] = '*';
      digit -= 5;
    }

    for (int d = 0; d < digit; ++d) {
      abacus[4 + d][col] = '*';
      abacus[4 + d + 1][col] = ' ';
    }

    n /= 10;
    col--;
  }
  for (int i = 0; i < 10; ++i) {
    if (i == 3) {
      puts(abacus[3]);
      continue;
    }
    for (int j = 0; j < 8; ++j) {
        printf("%c ", abacus[i][j]);
    }
    puts("");
  }
}

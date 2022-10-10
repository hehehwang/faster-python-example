#include <stdio.h>
#include <stdlib.h>
#include <string.h>

long long* worker(long long* works, int work_length, int criteria) {
  const long long MXN = 1000000;
  long long* ret = (long long*)malloc(sizeof(long long) * MXN * 2);
  memset(ret, -1, sizeof(long long) * MXN * 2);
  long long ri = 0;
  for (long long i = 0; i < work_length * 2; i += 2) {
    long long x = works[i];
    long long y = works[i + 1];
    // printf("%lld, %lld\n", x, y);
    if (x * x + y * y <= criteria * criteria) {
      ret[ri] = x;
      ret[ri + 1] = y;
      ri += 2;
    }
  }

  return ret;
}
// int main() {
//   long long todo[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
//   long long* ret = worker(todo, 5, 5);
//   for (int i = 0; i < 10; i++) {
//     printf("%lld ", ret[i]);
//   }
// }
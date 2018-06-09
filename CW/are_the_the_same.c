#include <stdbool.h>

bool comp(int* a, int* b, int sizeArray) {
  int A[sizeArray];
  int B[sizeArray];
  memcpy(A, a, sizeArray * sizeof(int));
  memcpy(B, b, sizeArray * sizeof(int));
  for (int i = 0; i < sizeArray; i++) {
    for (int j = 0; j < sizeArray; j++) {
      if (A[i] * A[i] == B[j]) {
        B[j] = -1;
        break;
      }
    }
  }
  for (int i = 0; i < sizeArray; i++) {
    if (B[i] != -1) {
      return false;
    }
  }
  return true;
}

#include "allocator.h"
#include "tests.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    srand(time(NULL));
    printf("Select test:\n  1. Allocations and frees\n  2. Re-allocations\n> ");
    char test = (char)getchar();
    if (test == '1') {
        printf("Running 'allocations and frees' test\n\n");
        allocations_and_frees();
    } else if (test == '2') {
        printf("Running 're-allocations' test\n\n");
        re_allocations();
    } else {
        printf("Failed to recognize the input\n");
    }
    return 0;
}
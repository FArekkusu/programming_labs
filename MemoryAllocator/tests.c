#include "allocator.h"
#include <stdlib.h>
#include <stdio.h>

void allocations_and_frees() {
    int maximum_blocks = 20, used_blocks = 0, number_of_tests = 100;
    void *blocks[maximum_blocks];
    for (int i = 0; i < number_of_tests; i++) {
        if (rand() % maximum_blocks >= used_blocks) {
            size_t size = 1 + rand() % 160;
            printf("TRYING TO ALLOCATE %zu\n", size);
            void *block = mem_alloc(size);
            if (block)
                blocks[used_blocks++] = block;
        } else {
            int index = rand() % used_blocks;
            printf("TRYING TO FREE %p\n", blocks[index]);
            mem_free(blocks[index]);
            for (int j = index; j < used_blocks - 1; j++)
                blocks[j] = blocks[j + 1];
            used_blocks--;
        }
        mem_dump();
    }
}

void re_allocations() {
    int maximum_blocks = 20, number_of_tests = 100;
    void *blocks[maximum_blocks];
    for (int i = 0; i < maximum_blocks; i++) {
        size_t size = 1 + rand() % 160;
        printf("TRYING TO ALLOCATE %zu\n", size);
        blocks[i] = mem_alloc(size);
    }

    for (int i = 0; i < number_of_tests; i++) {
        int index = rand() % maximum_blocks;
        size_t size = 1 + rand() % 160;
        printf("TRYING TO REALLOCATE %p FOR %zu\n", blocks[index], size);
        blocks[index] = mem_realloc(blocks[index], size);
        mem_dump();
    }
}
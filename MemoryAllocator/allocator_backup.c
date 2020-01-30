#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static const size_t max_heap_size = 1 << 12;
static char *heap = NULL, *max_address;
static const uint64_t step = sizeof(uint64_t);
static const uint64_t header_size = step * 3;

inline static uint64_t *get_next(const char *position) {
    return (uint64_t *)position;
}

inline static uint64_t *get_prev(const char *position) {
    return (uint64_t *)(position + step);
}

inline static uint64_t *get_used(const char *position) {
    return (uint64_t *)(position + step * 2);
}

inline static uint64_t get_size(const char *position) {
    if (!*get_next(position))
        return 0;
    return (char *)(*get_next(position)) - (char *)position - header_size;
}

inline static size_t get_aligned_size(size_t size) {
    return (size + step - 1) & ~(step - 1);
}

static void initialize_heap() {
    heap = (char *)calloc(max_heap_size, sizeof(char));
    max_address = (char *)(heap + max_heap_size);

    char *left_guard = heap,
            *right_guard = (char *)(heap + max_heap_size - header_size),
            *data = (char *)(heap + header_size);

    *get_next(left_guard) = *get_prev(right_guard) = (uint64_t)data;
    *get_used(left_guard) = *get_used(right_guard) = 1;
    *get_prev(data) = (uint64_t)left_guard;
    *get_next(data) = (uint64_t)right_guard;
}

void mem_dump() {
    if (!heap) {
        printf("HEAP IS NOT INITIALIZED\n\n");
        return;
    }

    char *current_position = heap;
    uint64_t prev, next;
    char line[56] = "-------------------------------------------------------";

    printf("%s%s\n", line, line);
    printf("HEAP = %p\n\n", heap);

    while (1) {
        prev = *get_prev(current_position);
        next = *get_next(current_position);

        printf("PREV = %-7p   CURRENT = %-7p   NEXT = %-7p   SIZE = %-4llu   USED = %llu\n",
               (char *)prev, current_position, (char *)next, get_size(current_position), *get_used(current_position));

        if (!(current_position = (char *)next))
            break;
    }

    printf("%s%s\n\n", line, line);
}

void *mem_alloc(size_t size) {
    printf("TRYING TO ALLOCATE %zu\n", size);
    if (!heap)
        initialize_heap();

    if (!size)
        return NULL;

    char *found_position = NULL, *current_position = heap + header_size;
    size_t actual_size = get_aligned_size(size);
    uint64_t next, used, too_small;

    while ((next = *get_next(current_position))) {
        used = *get_used(current_position);
        size = get_size(current_position);
        too_small = size < actual_size + header_size;
        if (!used && !too_small && (!found_position || size < get_size(found_position))) {
            found_position = current_position;
            break;
        }
        current_position = (char *)next;
    }

    if (!found_position)
        return NULL;

    *get_used(found_position) = 1;
    size = get_size(found_position);
    next = *get_next(found_position);
    if (size - actual_size <= header_size)
        return found_position + header_size;

    *get_next(found_position) = (uint64_t)(found_position + actual_size + header_size);
    *get_prev((char *)next) = *get_next(found_position);
    *get_next((char *)(*get_next(found_position))) = (uint64_t)next;
    *get_prev((char *)(*get_prev((char *)next))) = (uint64_t)found_position;
    *get_used((char *)(*get_next(found_position))) = 0;
    return found_position + header_size;
}

void mem_free(void *addr) {
    char *block = addr - header_size;
    printf("TRYING TO FREE %p (BLOCK AT %p)\n", addr, block);
    *get_used((char *)block) = 0;
    char *prev = (char *)(*get_prev(block)),
            *next = (char *)(*get_next(block));
    if (!*get_used(next)) {
        *get_next(block) = (uint64_t)(*get_next(next));
        *get_prev((char *)(*get_next(next))) = (uint64_t)block;
        next = (char *)(*get_next(block));
    }

    if (!*get_used(prev)) {
        *get_next(prev) = (uint64_t)next;
        *get_prev(next) = (uint64_t)prev;
    }
}

void *mem_realloc(void *addr, size_t size) {
    printf("TRYING TO REALLOCATE %p (BLOCK AT %p) FOR %zu\n", addr, addr - header_size, size);
    if (!size)
        return addr;

    if (!addr)
        return mem_alloc(size);

    size_t actual_size = get_aligned_size(size);
    char *block = addr - header_size,
            *next = (char *)(*get_next(block));
    uint64_t block_size = get_size(block);

    if (block_size == actual_size)
        return addr;

    if (block_size > actual_size) {
        if (block_size - actual_size <= header_size) return addr;
        *get_next(block) = (uint64_t)(block + header_size + actual_size);
        *get_prev((char *)(*get_next(block))) = (uint64_t)block;
        *get_next((char *)(*get_next(block))) = (uint64_t)next;
        *get_prev(next) = *get_next(block);
        mem_free((char *)(*get_next(block) + header_size));
        return addr;
    }

    uint64_t sum = block_size + get_size(next) + header_size;
    if (sum >= actual_size && !*get_used(next)) {
        if (sum - actual_size <= header_size)
            actual_size = sum;
        if (sum == actual_size) {
            *get_next(block) = *get_next(next);
            *get_prev((char *)(*get_next(block))) = (uint64_t)block;
        } else {
            *get_next(block) = (uint64_t)(block + header_size + actual_size);
            *get_prev((char *)(*get_next(next))) = *get_next(block);
            *get_next((char *)(*get_next(block))) = *get_next(next);
            *get_prev((char *)(*get_next(block))) = (uint64_t)block;
        }
        return addr;
    }

    void *new_block = mem_alloc(actual_size);
    if (!new_block)
        return addr;
    memcpy(new_block, addr, get_size(block));
    mem_free(addr);
    return new_block;
}
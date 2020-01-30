#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const size_t max_heap_size = 1 << 12;
static char *heap = NULL, *max_address;
static const uint64_t step = sizeof(uint64_t);
static const uint64_t header_size = step * 2;

inline static uint64_t *_get_size(const char *block) {
    return (uint64_t *)block;
}

inline static size_t get_size(const char *block) {
    return *_get_size(block) >> 1 << 1;
}

inline static char get_used(const char *block) {
    return *_get_size(block) & 1;
}

inline static void set_size(const char *block, size_t size, char used) {
    *_get_size(block) = size + used;
}

inline static uint64_t *get_next(const char *block) {
    return (uint64_t *)(block + header_size + get_size(block));
}

inline static uint64_t *_get_prev(const char *block) {
    return (uint64_t *)(block + step);
}

inline static uint64_t *get_prev(const char *block) {
    return (uint64_t *)(*_get_prev(block));
}

inline static void set_prev(const char *block, const char *ptr) {
    *_get_prev(block) = (uint64_t)ptr;
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

    set_size(left_guard, 0, 1);
    set_size(right_guard, 0, 1);
    set_size(data, max_heap_size - header_size * 3, 0);
    set_prev(data, left_guard);
    set_prev(right_guard, data);
}

void mem_dump() {
    if (!heap) {
        printf("HEAP IS NOT INITIALIZED\n\n");
        return;
    }

    char *current_position = heap, *next;
    char line[53] = "----------------------------------------------------";

    printf("%s%s\n", line, line);
    printf("HEAP = %p\n\n", heap);

    while (1) {
        next = (char *)get_next(current_position);
        size_t size = get_size(current_position);

        printf("PREV = %p   CURRENT = %p   NEXT = %p   SIZE = %-4zu   USED = %d\n",
               get_prev(current_position),
               current_position,
               next,
               size,
               get_used(current_position));

        if (current_position != heap && !size)
            break;

        current_position = next;
    }

    printf("%s%s\n\n", line, line);
}

void *mem_alloc(size_t size) {
    if (!heap)
        initialize_heap();

    if (!size)
        return NULL;

    char *found_position = NULL, *current_position = heap;
    size_t aligned_size = get_aligned_size(size);
    char *next, *new_next;
    char used, too_small;

    while (1) {
        used = get_used(current_position);
        size = get_size(current_position);
        too_small = size < aligned_size + header_size;

        if (!used && !too_small) {
            found_position = current_position;
            break;
        }
        current_position = (char *)get_next(current_position);
        if (!get_size(current_position)) break;
    }

    if (!found_position)
        return NULL;

    size = get_size(found_position);
    next = (char *)get_next(found_position);
    if (size <= aligned_size + header_size) {
        set_size(found_position, size, 1);
        return found_position + header_size;
    }

    set_size(found_position, aligned_size, 1);
    new_next = (char *)get_next(found_position);
    set_size(new_next, size - aligned_size - header_size, 0);
    set_prev(new_next, found_position);
    set_prev(next, new_next);

    return found_position + header_size;
}

void mem_free(void *addr) {
    char *block = addr - header_size;
    set_size(block, get_size(block), 0);
    char *prev = (char *)get_prev(block),
            *next = (char *)get_next(block);
    if (!get_used(next)) {
        set_size(block, get_size(block) + get_size(next) + header_size, 0);
        set_prev((char *)get_next(next), block);
        next = (char *)get_next(block);
    }

    if (!get_used(prev)) {
        set_size(prev, get_size(prev) + get_size(block) + header_size, 0);
        set_prev(next, prev);
    }
}

void *mem_realloc(void *addr, size_t size) {
    if (!size)
        return addr;

    if (!addr)
        return mem_alloc(size);

    size_t aligned_size = get_aligned_size(size);
    char *block = addr - header_size,
            *next = (char *)get_next(block),
            *new_next;
    uint64_t block_size = get_size(block);

    if (block_size == aligned_size) {
        return addr;
    }

    if (block_size > aligned_size) {
        if (block_size <= aligned_size + header_size) {
            set_size(block, block_size, 1);
            return addr;
        }
        set_size(block, aligned_size, 1);
        new_next = (char *)get_next(block);
        set_size(new_next, block_size - aligned_size - header_size, 0);
        set_prev(new_next, block);
        set_prev(next, new_next);
        mem_free(new_next + header_size);
        return addr;
    }

    uint64_t sum = block_size + get_size(next) + header_size;
    if (sum >= aligned_size && !get_used(next)) {
        if (sum <= aligned_size + header_size) {
            new_next = (char *)get_next(next);
            set_size(block, sum, 1);
            set_prev(new_next, block);
        } else {
            set_size(block, aligned_size, 1);
            new_next = (char *)get_next(block);
            set_size(new_next, sum - aligned_size - header_size, 0);
            set_prev(new_next, block);
            set_prev((char *)get_next(next), new_next);
        }
        return addr;
    }

    void *new_block = mem_alloc(aligned_size);
    if (!new_block)
        return addr;
    memcpy(new_block, addr, get_size(block));
    mem_free(addr);
    return new_block;
}
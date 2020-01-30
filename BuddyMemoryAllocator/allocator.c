#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MIN_ALLOC_LOG2 4
#define MAX_ALLOC_LOG2 12
#define MIN_ALLOC (1 << MIN_ALLOC_LOG2)
#define BUFFER_SIZE (1 << MAX_ALLOC_LOG2)
#define LISTS_COUNT (MAX_ALLOC_LOG2 - MIN_ALLOC_LOG2 + 1)

typedef struct list {
  struct list *prev, *next;
} List;

static char *buffer = NULL;
static List lists[LISTS_COUNT];
static size_t block_sizes[1 << (MAX_ALLOC_LOG2 - MIN_ALLOC_LOG2)] = {0};

static void list_init(List *list) {
  list->prev = list;
  list->next = list;
}

static void list_push(List *list, List *node) {
  List *last = list->prev;
  node->prev = last;
  node->next = list;
  last->next = node;
  list->prev = node;
}

static void list_remove(List *node) {
  List *prev = node->prev, *next = node->next;
  prev->next = next;
  next->prev = prev;
}

static List *list_pop(List *list) {
  List *last = list->prev;
  if (list == last) return NULL;
  list_remove(last);
  return last;
}

static int list_for_request(size_t request) {
  int list = LISTS_COUNT - 1;
  size_t size = MIN_ALLOC;
  while (size < request) {
    size *= 2;
    list--;
  }
  return list;
}

static void buffer_initialize() {
  buffer = (char *)calloc(BUFFER_SIZE, sizeof(char));
  for (int i = 0; i < LISTS_COUNT; i++)
    list_init(&lists[i]);
  list_push(&lists[0], (List *)buffer);
}

void *mem_alloc(size_t size) {
  if (!size)
    return NULL;

  if (size > BUFFER_SIZE)
    return NULL;
  
  if (!buffer)
    buffer_initialize();
  
  int fitting_list = list_for_request(size);
  size_t actual_size = 1 << (LISTS_COUNT - fitting_list + 3);
  int growing_list = fitting_list;
  while (growing_list >= 0) {
    size_t *ptr = (size_t *)list_pop(&lists[growing_list]);
    if (!ptr) {
      growing_list--;
      continue;
    }
    while (growing_list != fitting_list) {
      size_t buddy_size = 1 << (LISTS_COUNT - growing_list + 2);
      List *buddy = (List *)((char *)ptr + buddy_size);
      block_sizes[((char *)buddy - buffer) / MIN_ALLOC] = buddy_size;
      list_push(&lists[growing_list+1], buddy);
      growing_list++;
    }
    block_sizes[((char *)ptr - buffer) / MIN_ALLOC] = actual_size - 1;
    return (void *)ptr;
  }
  return NULL;
}

void mem_free(void *addr) {
  char *block = (char *)addr;
  size_t block_size = block_sizes[(block - buffer) / MIN_ALLOC] + 1;
  int fitting_list = list_for_request(block_size);
  while (fitting_list) {
    size_t cur_block_size = 1 << (LISTS_COUNT - fitting_list + 3);
    int position = (block - buffer) / cur_block_size;
    int buddy_position = position ^ 1;
    char *buddy_block = (char *)((buddy_position * cur_block_size) + buffer);
    size_t buddy_size = block_sizes[(buddy_block - buffer) / MIN_ALLOC];
    if (buddy_size & 1)
      break;
    if (cur_block_size != buddy_size)
      break;
    list_remove((List *)buddy_block);
    if (position & 1)
      block = buddy_block;
    fitting_list--;
  }
  list_push(&lists[fitting_list], (List *)block);
}

void *mem_realloc(void *addr, size_t size) {
  if (!size)
    return addr;

  if (!addr)
    return mem_alloc(size);

  char *block = (char *)addr;
  size_t block_size = block_sizes[(block - buffer) / MIN_ALLOC] + 1;
  if (list_for_request(size) == list_for_request(block_size))
    return addr;
  
  void *new_block = mem_alloc(size);
  if (!new_block)
    return addr;
  if (size > block_size)
    size = block_size;
  memcpy(new_block, addr, size);
  mem_free(addr);
  return new_block;
}

static void print_list(int index) {
  List *list = &lists[index];
  List *next = list->next;
  size_t size = 1 << (LISTS_COUNT - index + 3);
  printf("%lu:\n", size);
  while (list != next) {
    printf(" %p\n", next);
    next = next->next;
  }
}

void mem_dump() {
  if (!buffer) {
    printf("BUFFER IS NOT INITIALIZED\n\n");
    return;
  }
  printf("BUFFER = %p\n", buffer);
  for (int i = 0; i < LISTS_COUNT; i++)
    print_list(i);
  printf("\n");
}
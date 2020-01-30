cmake_minimum_required(VERSION 3.14)
project(BuddySystemAllocator C)

set(CMAKE_C_STANDARD 11)
set(PLATFORM 64)

add_executable(BuddySystemAllocator main.c allocator.c allocator.h tests.c tests.h)
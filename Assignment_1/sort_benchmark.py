# sort_benchmark.py
# Run: python3 sort_benchmark.py > py_times.csv

import time
import random
import sys

def merge_sort(a):
    # returns a new sorted list
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    i = j = 0
    out = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out

def quick_sort(a):
    # returns a new sorted list (simple pivot = last)
    if len(a) <= 1:
        return a
    pivot = a[-1]
    left = [x for x in a[:-1] if x <= pivot]
    right = [x for x in a[:-1] if x > pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)

def time_one(fn, arr, repeats=3):
    best = 10**18
    for _ in range(repeats):
        a = arr[:]  # copy
        t0 = time.perf_counter_ns()
        _ = fn(a)
        t1 = time.perf_counter_ns()
        best = min(best, t1 - t0)
    return best / 1e6  # ms

def main():
    ns = [1000, 2000, 5000, 10000, 20000, 50000, 100000]
    repeats = 3

    print("language,algorithm,n,best_ms")
    for n in ns:
        random.seed(12345)  # fixed seed for fairness
        base = list(range(n))
        random.shuffle(base)

        m_ms = time_one(merge_sort, base, repeats=repeats)
        q_ms = time_one(quick_sort, base, repeats=repeats)

        print(f"Python,mergesort,{n},{m_ms:.3f}")
        print(f"Python,quicksort,{n},{q_ms:.3f}")

if __name__ == "__main__":
    main()


import time
import random
import csv
import os
import sys

# ---------------------------
# Make imports work reliably
# ---------------------------
# This file is in: Assignment_2/task2/benchmark.py
# We add this folder to sys.path so "from disjoint_set import DisjointSet" works.
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  # .../Assignment_2/task2
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from disjoint_set import DisjointSet  # disjoint_set.py must be inside Assignment_2/task2/


def benchmark_once(n, unions, finds, seed=42):
    random.seed(seed)
    ds = DisjointSet()

    # MAKE-SET
    t0 = time.perf_counter()
    for i in range(n):
        ds.make_set(i)
    t1 = time.perf_counter()
    make_time = t1 - t0

    # UNION
    t0 = time.perf_counter()
    for _ in range(unions):
        a = random.randrange(n)
        b = random.randrange(n)
        ds.union(a, b)
    t1 = time.perf_counter()
    union_time = t1 - t0

    # FIND-SET
    t0 = time.perf_counter()
    for _ in range(finds):
        a = random.randrange(n)
        ds.find_set(a)
    t1 = time.perf_counter()
    find_time = t1 - t0

    return make_time, union_time, find_time


if __name__ == "__main__":
    # Sizes to show scaling trend
    sizes = [10_000, 50_000, 100_000, 200_000]

    # Number of operations relative to n
    unions_factor = 1
    finds_factor = 2

    rows = [["n", "make_set_s", "union_s", "find_set_s"]]

    for n in sizes:
        make_t, union_t, find_t = benchmark_once(
            n=n,
            unions=n * unions_factor,
            finds=n * finds_factor,
            seed=42,
        )
        rows.append([n, make_t, union_t, find_t])
        print(f"n={n}: make={make_t:.4f}s, union={union_t:.4f}s, find={find_t:.4f}s")

    # ---------------------------
    # Save results inside:
    # Assignment_2/task2/results/
    # ---------------------------
    results_dir = os.path.join(CURRENT_DIR, "results")
    os.makedirs(results_dir, exist_ok=True)

    out_csv = os.path.join(results_dir, "times.csv")
    with open(out_csv, "w", newline="") as f:
        csv.writer(f).writerows(rows)

    print(f"Saved results to {out_csv}")

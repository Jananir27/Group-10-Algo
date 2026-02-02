// sort_benchmark.c
// Portable timing version using clock() (no clock_gettime needed)
//
// Compile:
//   gcc -O2 -std=c11 sort_benchmark.c -o sort_benchmark_exec
//
// Run:
//   ./sort_benchmark_exec > c_times.csv

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/* -------------------- timing -------------------- */
/* Returns CPU time in milliseconds (portable). */
static inline double now_ms(void) {
    return (double)clock() * 1000.0 / (double)CLOCKS_PER_SEC;
}

/* -------------------- input generation -------------------- */
static void fill_random(int *a, int n, unsigned seed) {
    srand(seed);
    for (int i = 0; i < n; i++) a[i] = rand();
}

/* -------------------- MERGE SORT -------------------- */
static void merge(int *a, int *tmp, int lo, int mid, int hi) {
    int i = lo, j = mid, k = lo;
    while (i < mid && j < hi) {
        if (a[i] <= a[j]) tmp[k++] = a[i++];
        else              tmp[k++] = a[j++];
    }
    while (i < mid) tmp[k++] = a[i++];
    while (j < hi)  tmp[k++] = a[j++];

    for (int t = lo; t < hi; t++) a[t] = tmp[t];
}

static void mergesort_rec(int *a, int *tmp, int lo, int hi) {
    if (hi - lo <= 1) return;
    int mid = lo + (hi - lo) / 2;
    mergesort_rec(a, tmp, lo, mid);
    mergesort_rec(a, tmp, mid, hi);
    merge(a, tmp, lo, mid, hi);
}

static void merge_sort(int *a, int n) {
    int *tmp = (int*)malloc((size_t)n * sizeof(int));
    if (!tmp) {
        fprintf(stderr, "malloc failed\n");
        exit(1);
    }
    mergesort_rec(a, tmp, 0, n);
    free(tmp);
}

/* -------------------- QUICK SORT -------------------- */
/* Lomuto partition, pivot = last element.
   Average case good for random data; worst-case on sorted input. */
static int partition(int *a, int lo, int hi) { // hi inclusive
    int pivot = a[hi];
    int i = lo - 1;
    for (int j = lo; j < hi; j++) {
        if (a[j] <= pivot) {
            i++;
            int tmp = a[i]; a[i] = a[j]; a[j] = tmp;
        }
    }
    int tmp = a[i + 1]; a[i + 1] = a[hi]; a[hi] = tmp;
    return i + 1;
}

static void quicksort_rec(int *a, int lo, int hi) {
    if (lo >= hi) return;
    int p = partition(a, lo, hi);
    quicksort_rec(a, lo, p - 1);
    quicksort_rec(a, p + 1, hi);
}

static void quick_sort(int *a, int n) {
    if (n > 0) quicksort_rec(a, 0, n - 1);
}

/* -------------------- BENCH -------------------- */
/* Runs the sort several times and returns best (minimum) ms. */
static double bench(void (*sortfn)(int*, int), const int *base, int n, int repeats) {
    int *a = (int*)malloc((size_t)n * sizeof(int));
    if (!a) {
        fprintf(stderr, "malloc failed\n");
        exit(1);
    }

    double best = 1e18;

    for (int r = 0; r < repeats; r++) {
        memcpy(a, base, (size_t)n * sizeof(int));

        double t0 = now_ms();
        sortfn(a, n);
        double t1 = now_ms();

        double dt = t1 - t0;
        if (dt < best) best = dt;
    }

    free(a);
    return best;
}

int main(void) {
    /* Adjust sizes if needed */
    int ns[] = {1000, 2000, 5000, 10000, 20000, 50000, 100000};
    int count = (int)(sizeof(ns) / sizeof(ns[0]));
    int repeats = 5;

    printf("language,algorithm,n,best_ms\n");

    for (int i = 0; i < count; i++) {
        int n = ns[i];

        int *base = (int*)malloc((size_t)n * sizeof(int));
        if (!base) {
            fprintf(stderr, "malloc failed\n");
            exit(1);
        }

        /* fixed seed -> same input distribution each run (fairness) */
        fill_random(base, n, 12345u);

        double m_ms = bench(merge_sort, base, n, repeats);
        double q_ms = bench(quick_sort,  base, n, repeats);

        printf("C,mergesort,%d,%.3f\n", n, m_ms);
        printf("C,quicksort,%d,%.3f\n", n, q_ms);

        free(base);
    }

    return 0;
}


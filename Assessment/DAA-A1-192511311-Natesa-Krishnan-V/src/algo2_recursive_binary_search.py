"""
Algorithm 2 - Recursive Binary Search
Name: Natesa Krishnan V | Registration No.: 192511311 | Group: A

Preprocessing: sort the records (measured separately and included in total time).
Search: compare the key with the middle element and recurse on one half.
Basic operation: the three-way key comparison with arr[mid] (counted once per call
that examines an element). Recurrence:  T(n) = T(floor(n/2)) + 1,  T(0) = 0.
Run:  python src/algo2_recursive_binary_search.py
"""
import csv
import gc
import os

from dataset_generator import (SIZES, KEY_FOUND, KEY_NOT_FOUND, RESULTS_DIR,
                               banner, best_time, load_dataset)

ALGORITHM = "Recursive Binary Search"


def binary_search(arr, key, lo, hi):
    """Recursive binary search on sorted arr[lo..hi].
    Returns (index or -1, number of key comparisons)."""
    if lo > hi:                       # base case: empty sub-array, no comparison
        return -1, 0
    mid = (lo + hi) // 2
    if arr[mid] == key:               # one key comparison per recursive call
        return mid, 1
    if arr[mid] < key:
        idx, c = binary_search(arr, key, mid + 1, hi)   # right half
    else:
        idx, c = binary_search(arr, key, lo, mid - 1)   # left half
    return idx, c + 1


def search(arr, key):
    return binary_search(arr, key, 0, len(arr) - 1)


def run(sizes=SIZES, write_csv=True, verbose=True):
    # Garbage collection is switched off while timing (as timeit does) so that
    # collector pauses do not distort the measurements.
    gc.disable()
    try:
        return _run(sizes, write_csv, verbose)
    finally:
        gc.enable()


def _run(sizes, write_csv, verbose):
    rows = []
    for n in sizes:
        data = load_dataset(n)
        # ---- preprocessing: sorting (measured separately) ----
        pre_reps = max(1, 100_000 // n)
        pre, sorted_data = best_time(sorted, (data,), pre_reps)
        search_reps = 2000
        for key in (KEY_FOUND, KEY_NOT_FOUND):
            st, (idx, comps) = best_time(search, (sorted_data, key), search_reps)
            total = pre + st
            rows.append({
                "algorithm": ALGORITHM, "input_size": n, "search_key": key,
                "result": "FOUND" if idx >= 0 else "NOT FOUND",
                "index": idx, "comparisons": comps,
                "preprocessing_time_seconds": f"{pre:.9f}",
                "preprocessing_time_ms": f"{pre * 1000:.6f}",
                "search_time_seconds": f"{st:.9f}",
                "search_time_ms": f"{st * 1000:.6f}",
                "total_time_seconds": f"{total:.9f}",
                "total_time_ms": f"{total * 1000:.6f}",
                "search_repetitions": search_reps,
            })
            if verbose:
                print(f"n={n:>9,} | key={key} | {rows[-1]['result']:<9} | index(sorted)={idx:>8} | "
                      f"comparisons={comps:>3} | sort={pre * 1000:>10.4f} ms | "
                      f"search={st * 1000:>9.6f} ms | total={total * 1000:>10.4f} ms")
    if write_csv:
        os.makedirs(RESULTS_DIR, exist_ok=True)
        path = os.path.join(RESULTS_DIR, "binary_search_results.csv")
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        if verbose:
            print(f"\nSaved: {path}")
    return rows


if __name__ == "__main__":
    banner("Algorithm 2: Recursive Binary Search")
    run()

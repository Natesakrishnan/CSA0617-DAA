"""
Algorithm 1 - Linear Search (iterative)
Name: Natesa Krishnan V | Registration No.: 192511311 | Group: A

Scans the unsorted records from index 0 until the key is found or the data ends.
Basic operation: the key comparison  data[i] == key.
Run:  python src/algo1_linear_search.py
"""
import csv
import gc
import os

from dataset_generator import (SIZES, KEY_FOUND, KEY_NOT_FOUND, RESULTS_DIR,
                               banner, best_time, load_dataset)

ALGORITHM = "Linear Search"


def linear_search(data, key):
    """Iterative linear search. Returns (index or -1, number of key comparisons)."""
    comparisons = 0
    for i, value in enumerate(data):
        comparisons += 1              # basic operation: one key comparison
        if value == key:
            return i, comparisons
    return -1, comparisons


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
        data = load_dataset(n)                    # loading time is NOT measured
        reps = max(5, 1_000_000 // n)             # repetitions to average timing
        for key in (KEY_FOUND, KEY_NOT_FOUND):
            elapsed, (idx, comps) = best_time(linear_search, (data, key), reps)
            rows.append({
                "algorithm": ALGORITHM, "input_size": n, "search_key": key,
                "result": "FOUND" if idx >= 0 else "NOT FOUND",
                "index": idx, "comparisons": comps,
                "execution_time_seconds": f"{elapsed:.9f}",
                "execution_time_ms": f"{elapsed * 1000:.6f}",
                "repetitions": reps,
            })
            if verbose:
                r = rows[-1]
                print(f"n={n:>9,} | key={key} | {r['result']:<9} | index={idx:>8} | "
                      f"comparisons={comps:>9,} | time={elapsed * 1000:>10.4f} ms (avg of {reps})")
    if write_csv:
        os.makedirs(RESULTS_DIR, exist_ok=True)
        path = os.path.join(RESULTS_DIR, "linear_search_results.csv")
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        if verbose:
            print(f"\nSaved: {path}")
    return rows


if __name__ == "__main__":
    banner("Algorithm 1: Linear Search (iterative)")
    run()

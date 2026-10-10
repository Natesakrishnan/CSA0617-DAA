"""
Algorithm 3 - Hash Table Search (Group A)
Name: Natesa Krishnan V | Registration No.: 192511311 | Group: A

Own implementation of a hash table with separate chaining:
  * table size m = smallest prime >= n / 0.75   (target load factor alpha ~ 0.75)
  * hash function h(key) = key mod m
  * preprocessing: insert all n records (key -> original index)
Basic operation: key comparison inside the bucket chain (plus one hash computation).
Run:  python src/algo3_hash_table.py
"""
import csv
import gc
import math
import os

from dataset_generator import (SIZES, KEY_FOUND, KEY_NOT_FOUND, RESULTS_DIR,
                               banner, best_time, load_dataset)

ALGORITHM = "Hash Table Search"
LOAD_TARGET = 0.75


def next_prime(x):
    x = max(2, int(x))
    while True:
        if all(x % d for d in range(2, math.isqrt(x) + 1)):
            return x
        x += 1


class HashTable:
    """Hash table with separate chaining (buckets are lists of (key, value))."""

    def __init__(self, expected_n, load_target=LOAD_TARGET):
        self.m = next_prime(math.ceil(max(expected_n, 1) / load_target))
        self.buckets = [None] * self.m
        self.size = 0

    def insert(self, key, value):                 # O(1): append to chain
        h = key % self.m
        b = self.buckets[h]
        if b is None:
            self.buckets[h] = [(key, value)]
        else:
            b.append((key, value))
        self.size += 1

    def search(self, key):
        """Returns (value or -1, key_comparisons, total_operations).
        total_operations = 1 hash computation + key comparisons in the chain."""
        comps = 0
        b = self.buckets[key % self.m]
        if b is not None:
            for k, v in b:
                comps += 1                        # basic operation: key comparison
                if k == key:
                    return v, comps, comps + 1
        return -1, comps, comps + 1

    def load_factor(self):
        return self.size / self.m

    def max_chain(self):
        return max((len(b) for b in self.buckets if b is not None), default=0)


def build_table(data):
    t = HashTable(len(data))
    for i, key in enumerate(data):
        t.insert(key, i)
    return t


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
        pre_reps = max(1, 100_000 // n)
        pre, table = best_time(build_table, (data,), pre_reps)
        search_reps = 2000
        for key in (KEY_FOUND, KEY_NOT_FOUND):
            st, (val, comps, ops) = best_time(table.search, (key,), search_reps)
            total = pre + st
            rows.append({
                "algorithm": ALGORITHM, "input_size": n, "search_key": key,
                "result": "FOUND" if val >= 0 else "NOT FOUND",
                "index_or_key": val if val >= 0 else key,
                "key_comparisons": comps, "operations": ops,
                "table_size": table.m, "load_factor": f"{table.load_factor():.4f}",
                "max_chain_length": table.max_chain(),
                "preprocessing_time_seconds": f"{pre:.9f}",
                "preprocessing_time_ms": f"{pre * 1000:.6f}",
                "search_time_seconds": f"{st:.9f}",
                "search_time_ms": f"{st * 1000:.6f}",
                "total_time_seconds": f"{total:.9f}",
                "total_time_ms": f"{total * 1000:.6f}",
                "search_repetitions": search_reps,
            })
            if verbose:
                print(f"n={n:>9,} | key={key} | {rows[-1]['result']:<9} | "
                      f"index/key={rows[-1]['index_or_key']:>9} | ops={ops:>2} | "
                      f"build={pre * 1000:>10.4f} ms | search={st * 1000:>9.6f} ms | "
                      f"total={total * 1000:>10.4f} ms")
    if write_csv:
        os.makedirs(RESULTS_DIR, exist_ok=True)
        path = os.path.join(RESULTS_DIR, "hash_table_results.csv")
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        if verbose:
            print(f"\nSaved: {path}")
    return rows


if __name__ == "__main__":
    banner("Algorithm 3: Hash Table Search (Group A)")
    run()

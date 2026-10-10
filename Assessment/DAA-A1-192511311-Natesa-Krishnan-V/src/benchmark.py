"""
Benchmark + correctness tests - DAA Assignment 1
Name: Natesa Krishnan V | Registration No.: 192511311 | Group: A

  python src/benchmark.py                 -> run all 3 algorithms on all 4 datasets,
                                             write results/results.csv (+ the 3 per-algorithm CSVs)
  python src/benchmark.py --correctness   -> run the Task 8 correctness test-suite
"""
import csv
import math
import os
import random
import sys

from dataset_generator import (SIZES, SEED, KEY_FOUND, KEY_NOT_FOUND, RESULTS_DIR,
                               banner, load_dataset)
import algo1_linear_search as a1
import algo2_recursive_binary_search as a2
import algo3_hash_table as a3

COMBINED_FIELDS = ["algorithm", "input_size", "search_key", "result", "index",
                   "comparisons_operations", "preprocessing_time_seconds",
                   "preprocessing_time_ms", "search_time_seconds", "search_time_ms",
                   "total_time_seconds", "total_time_ms"]


def combine(r1, r2, r3):
    out = []
    for r in r1:
        out.append({"algorithm": r["algorithm"], "input_size": r["input_size"],
                    "search_key": r["search_key"], "result": r["result"],
                    "index": r["index"], "comparisons_operations": r["comparisons"],
                    "preprocessing_time_seconds": "0.000000000", "preprocessing_time_ms": "0.000000",
                    "search_time_seconds": r["execution_time_seconds"],
                    "search_time_ms": r["execution_time_ms"],
                    "total_time_seconds": r["execution_time_seconds"],
                    "total_time_ms": r["execution_time_ms"]})
    for r in r2:
        out.append({"algorithm": r["algorithm"], "input_size": r["input_size"],
                    "search_key": r["search_key"], "result": r["result"],
                    "index": r["index"], "comparisons_operations": r["comparisons"],
                    **{k: r[k] for k in COMBINED_FIELDS[6:]}})
    for r in r3:
        out.append({"algorithm": r["algorithm"], "input_size": r["input_size"],
                    "search_key": r["search_key"], "result": r["result"],
                    "index": r["index_or_key"], "comparisons_operations": r["operations"],
                    **{k: r[k] for k in COMBINED_FIELDS[6:]}})
    return out


def benchmark():
    banner("Benchmark (all algorithms x all dataset sizes)")
    r1 = a1.run(verbose=False)
    r2 = a2.run(verbose=False)
    r3 = a3.run(verbose=False)
    rows = combine(r1, r2, r3)
    for n in SIZES:
        print(f"\n##### DATASET SIZE n = {n:,} #####")
        print(f"{'Algorithm':<24}{'Key':<11}{'Result':<11}{'Comps/Ops':>10}"
              f"{'Preproc(ms)':>14}{'Search(ms)':>13}{'Total(ms)':>14}")
        for r in rows:
            if r["input_size"] == n:
                print(f"{r['algorithm']:<24}{r['search_key']:<11}{r['result']:<11}"
                      f"{r['comparisons_operations']:>10}"
                      f"{float(r['preprocessing_time_ms']):>14.4f}"
                      f"{float(r['search_time_ms']):>13.6f}"
                      f"{float(r['total_time_ms']):>14.4f}")
        res = {(r["algorithm"], r["search_key"]): r["result"] for r in rows if r["input_size"] == n}
        agree = all(len({res[(a, k)] for a in (a1.ALGORITHM, a2.ALGORITHM, a3.ALGORITHM)}) == 1
                    for k in (KEY_FOUND, KEY_NOT_FOUND))
        print(f"All three algorithms agree on results: {agree}")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = os.path.join(RESULTS_DIR, "results.csv")
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COMBINED_FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"\nSaved: {path}")
    return 0


# ---------------------------------------------------------------- correctness
class Checker:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def check(self, name, cond):
        if cond:
            self.passed += 1
            print(f"  [PASS] {name}")
        else:
            self.failed += 1
            print(f"  [FAIL] {name}")


def correctness():
    banner("Task 8 - Correctness Tests")
    c = Checker()
    rng = random.Random(SEED)
    for n in SIZES:
        print(f"\n--- Dataset n = {n:,} ---")
        data = load_dataset(n)
        sdata = sorted(data)
        table = a3.build_table(data)
        members = set(data)
        bound = math.floor(math.log2(n)) + 1

        i1, c1 = a1.linear_search(data, KEY_FOUND)
        i2, c2 = a2.search(sdata, KEY_FOUND)
        v3, k3, _ = table.search(KEY_FOUND)
        c.check(f"{KEY_FOUND} FOUND by all three (linear idx={i1}, binary idx={i2}, hash idx={v3})",
                i1 >= 0 and i2 >= 0 and v3 >= 0 and data[i1] == KEY_FOUND
                and sdata[i2] == KEY_FOUND and data[v3] == KEY_FOUND)
        i1, c1 = a1.linear_search(data, KEY_NOT_FOUND)
        i2, c2 = a2.search(sdata, KEY_NOT_FOUND)
        v3, k3, _ = table.search(KEY_NOT_FOUND)
        c.check(f"{KEY_NOT_FOUND} NOT FOUND by all three", i1 == -1 and i2 == -1 and v3 == -1)
        c.check(f"Linear not-found comparisons == n ({c1} == {n})", c1 == n)
        c.check(f"Binary not-found comparisons <= floor(log2 n)+1 ({c2} <= {bound})", c2 <= bound)

        first, last = data[0], data[-1]
        i, cc = a1.linear_search(data, first)
        c.check(f"Linear best case: first element found with 1 comparison (got {cc})", i == 0 and cc == 1)
        i, cc = a1.linear_search(data, last)
        c.check(f"Linear worst case: last element found with n comparisons (got {cc})", i == n - 1 and cc == n)
        i, cc = a2.search(sdata, sdata[(n - 1) // 2])
        c.check(f"Binary best case: middle element found with 1 comparison (got {cc})", cc == 1)

        present = rng.sample(data, 100)
        absent = []
        while len(absent) < 100:
            x = rng.randrange(191_000_000, 193_000_000)
            if x not in members and x != KEY_NOT_FOUND:
                absent.append(x)
        ok = True
        for key in present + absent:
            exp = key in members
            r1 = a1.linear_search(data, key)[0] >= 0
            r2 = a2.search(sdata, key)[0] >= 0
            r3 = table.search(key)[0] >= 0
            if not (r1 == r2 == r3 == exp):
                ok = False
        c.check("200 random keys (100 present + 100 absent): all three agree with set membership", ok)

    print("\n--- Edge cases ---")
    c.check("Empty list: linear/binary/hash all NOT FOUND",
            a1.linear_search([], 5)[0] == -1 and a2.search([], 5)[0] == -1
            and a3.build_table([]).search(5)[0] == -1)
    c.check("Single element, present", a1.linear_search([7], 7)[0] == 0 and a2.search([7], 7)[0] == 0
            and a3.build_table([7]).search(7)[0] == 0)
    c.check("Single element, absent", a1.linear_search([7], 8)[0] == -1 and a2.search([7], 8)[0] == -1
            and a3.build_table([7]).search(8)[0] == -1)
    small = [30, 10, 20, 50, 40]
    ss = sorted(small)
    t = a3.build_table(small)
    c.check("Small unsorted list: every element found, neighbours absent",
            all(a1.linear_search(small, x)[0] >= 0 and a2.search(ss, x)[0] >= 0 and t.search(x)[0] >= 0 for x in small)
            and all(a1.linear_search(small, x)[0] == -1 and a2.search(ss, x)[0] == -1 and t.search(x)[0] == -1
                    for x in (5, 15, 25, 35, 45, 55)))

    print("\n" + "=" * 64)
    print(f"TOTAL: {c.passed} passed, {c.failed} failed")
    print("ALL TESTS PASSED" if c.failed == 0 else "SOME TESTS FAILED")
    return 0 if c.failed == 0 else 1


if __name__ == "__main__":
    if "--correctness" in sys.argv:
        sys.exit(correctness())
    sys.exit(benchmark())

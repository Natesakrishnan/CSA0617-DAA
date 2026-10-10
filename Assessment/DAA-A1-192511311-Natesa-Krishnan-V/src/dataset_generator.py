"""
Dataset generator - DAA Assignment 1
Name: Natesa Krishnan V | Registration No.: 192511311 | Group: A

Generates four deterministic datasets of student registration numbers
(1,000 / 10,000 / 100,000 / 1,000,000 records) using random seed 1311.

Method (per dataset of size n):
  1. rng = random.Random(1311)
  2. draw n+1 DISTINCT integers from [191,000,000 , 193,000,000)
  3. discard the two search keys (192511311 and 192511312) if they were drawn,
     keep the first n-1 remaining values
  4. insert the FOUND key 192511311 at a pseudo-random position (from the same rng)
Result: n unique, UNSORTED registration numbers; 192511311 is present exactly once,
192511312 is never present.

Run:  python src/dataset_generator.py
"""
import csv
import os
import random
import sys
import time

NAME = "Natesa Krishnan V"
REG_NO = "192511311"
GROUP = "A"
SEED = 1311
SIZES = [1000, 10000, 100000, 1000000]
KEY_FOUND = 192511311
KEY_NOT_FOUND = 192511312
RANGE_LOW = 191_000_000          # inclusive
RANGE_HIGH = 193_000_000         # exclusive

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
RESULTS_DIR = os.path.join(ROOT, "results")


def banner(title):
    line = "=" * 64
    print(line)
    print(f" DAA Assignment 1 - {title}")
    print(f" Name            : {NAME}")
    print(f" Registration No.: {REG_NO}")
    print(f" Group           : {GROUP}   (Dataset seed: {SEED})")
    print(line)


def best_time(func, args, reps, trials=3):
    """Average time of func(*args) over `reps` calls; repeated for `trials` trials and the
    fastest trial is reported (timeit-style, to suppress OS/background noise).
    Returns (seconds_per_call, result_of_last_call)."""
    best = None
    result = None
    for _ in range(trials):
        start = time.perf_counter()
        for _ in range(reps):
            result = func(*args)
        t = (time.perf_counter() - start) / reps
        if best is None or t < best:
            best = t
    return best, result


def dataset_path(n):
    return os.path.join(DATA_DIR, f"students_{n}.csv")


def generate(n):
    """Return the deterministic list of n registration numbers (unsorted)."""
    rng = random.Random(SEED)
    cand = rng.sample(range(RANGE_LOW, RANGE_HIGH), n + 1)
    cand = [x for x in cand if x not in (KEY_FOUND, KEY_NOT_FOUND)][: n - 1]
    pos = rng.randrange(n)
    cand.insert(pos, KEY_FOUND)
    return cand


def write_dataset(n):
    os.makedirs(DATA_DIR, exist_ok=True)
    data = generate(n)
    with open(dataset_path(n), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["registration_number"])
        for x in data:
            w.writerow([x])
    return data


def load_dataset(n):
    """Load students_<n>.csv as a list of ints (generates it first if missing)."""
    path = dataset_path(n)
    if not os.path.exists(path):
        write_dataset(n)
    with open(path, newline="") as f:
        r = csv.reader(f)
        next(r)  # header
        return [int(row[0]) for row in r]


def main():
    banner("Dataset Generator")
    all_ok = True
    for n in SIZES:
        data = write_dataset(n)
        unique = len(set(data)) == n
        has_found = data.count(KEY_FOUND) == 1
        has_not = KEY_NOT_FOUND not in set(data)
        ok = len(data) == n and unique and has_found and has_not
        all_ok &= ok
        print(f"students_{n}.csv : {len(data):>9,} records | unique={unique} | "
              f"{KEY_FOUND} present at index {data.index(KEY_FOUND):>7,} | "
              f"{KEY_NOT_FOUND} absent={has_not} | {'OK' if ok else 'FAILED'}")
    print("-" * 64)
    print("All datasets generated and verified." if all_ok else "VERIFICATION FAILED")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())

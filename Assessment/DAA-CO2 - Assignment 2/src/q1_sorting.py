"""Q1 - Selection, Bubble and Insertion sort under different data conditions.

Every sort returns (sorted_list, comparisons, swaps_or_moves).
  - Selection sort: a "swap" is counted only when the minimum is not already in place.
  - Bubble sort: includes the standard early-exit flag (stop when a pass makes no swap).
  - Insertion sort: a "move" is one element shifted right, plus one placement of the key.
"""
import random
import time


def selection_sort(a):
    a = list(a)
    n = len(a)
    comps = swaps = 0
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            comps += 1
            if a[j] < a[m]:
                m = j
        if m != i:
            a[i], a[m] = a[m], a[i]
            swaps += 1
    return a, comps, swaps


def bubble_sort(a):
    a = list(a)
    n = len(a)
    comps = swaps = 0
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            comps += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    return a, comps, swaps


def insertion_sort(a):
    a = list(a)
    comps = moves = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comps += 1
            if a[j] > key:
                a[j + 1] = a[j]
                moves += 1
                j -= 1
            else:
                break
        if j + 1 != i:
            a[j + 1] = key
            moves += 1
    return a, comps, moves


def count_inversions(a):
    """Number of pairs (i<j) with a[i] > a[j]; an O(n^2) count is fine at these sizes."""
    n = len(a)
    return sum(1 for i in range(n) for j in range(i + 1, n) if a[i] > a[j])


def make_datasets(n, seed=1311):
    """Four designed inputs of size n. Keys are integer priority scores."""
    rng = random.Random(seed + n)
    base = list(range(n))

    random_data = base[:]
    rng.shuffle(random_data)

    # ~95% in order: start sorted, then locally displace 5% of positions.
    nearly = base[:]
    for _ in range(max(1, int(0.05 * n))):
        i = rng.randrange(n)
        j = min(n - 1, max(0, i + rng.randint(-3, 3)))
        nearly[i], nearly[j] = nearly[j], nearly[i]

    # Worst-case style: strictly reversed order (every pair is an inversion).
    reversed_data = base[::-1]

    # Edge case: every key identical (heavy duplication).
    duplicates = [7] * n

    return {
        "nearly_sorted_95pct": nearly,
        "random": random_data,
        "reversed": reversed_data,
        "all_equal_edge": duplicates,
    }


ALGORITHMS = {
    "Selection": selection_sort,
    "Bubble": bubble_sort,
    "Insertion": insertion_sort,
}


def run(sizes=(250, 500, 1000, 2000), repeats=2):
    rows = []
    for n in sizes:
        for ds_name, data in make_datasets(n).items():
            inv = count_inversions(data) if n <= 2000 else None
            ordered_adjacent = sum(1 for i in range(n - 1) if data[i] <= data[i + 1]) / (n - 1)
            expected = sorted(data)
            for alg_name, fn in ALGORITHMS.items():
                result, comps, swaps = fn(data)
                assert result == expected, f"{alg_name} failed on {ds_name} n={n}"
                best = float("inf")
                for _ in range(repeats):
                    t0 = time.perf_counter()
                    fn(data)
                    best = min(best, time.perf_counter() - t0)
                rows.append({
                    "dataset": ds_name,
                    "n": n,
                    "algorithm": alg_name,
                    "comparisons": comps,
                    "swaps_or_moves": swaps,
                    "time_ms": round(best * 1000, 4),
                    "inversions": inv,
                    "adjacent_in_order_pct": round(100 * ordered_adjacent, 2),
                })
    return rows


if __name__ == "__main__":
    for r in run(sizes=(500,)):
        print(r)

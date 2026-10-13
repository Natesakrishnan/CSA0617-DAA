"""Q6 - Exhaustive search for the payload-limited package selection (0/1 knapsack form).

Representation: a candidate is an n-bit integer mask; bit i = 1 means package i is loaded.
Generation: masks 0 .. 2^n - 1 enumerate every subset exactly once.
Feasibility: total weight <= payload limit.
Evaluation: sum of humanitarian value over the loaded packages.
Retention: keep the feasible mask with the highest value seen so far.
"""
import random
import time


def exhaustive_search(items, limit):
    """items: list of (weight, value). Return dict with optimum and counters."""
    n = len(items)
    best_value = -1
    best_mask = 0
    candidates = 0
    feasible = 0
    weight_ops = 0
    for mask in range(1 << n):
        candidates += 1
        w = 0
        v = 0
        for i in range(n):
            weight_ops += 1
            if (mask >> i) & 1:
                w += items[i][0]
                v += items[i][1]
        if w <= limit:
            feasible += 1
            if v > best_value:
                best_value = v
                best_mask = mask
    chosen = [i for i in range(n) if (best_mask >> i) & 1]
    return {"best_value": best_value, "best_set": chosen, "candidates": candidates,
            "feasible": feasible, "item_checks": weight_ops}


def dp_reference(items, limit):
    """Independent dynamic-programming optimum, used only to cross-check exhaustive search."""
    best = [0] * (limit + 1)
    for w, v in items:
        for c in range(limit, w - 1, -1):
            best[c] = max(best[c], best[c - w] + v)
    return best[limit]


def hand_instance():
    """Small instance whose optimum can be checked by hand.
    Items A..E = (weight, value). Limit 10.
    Feasible subsets with the highest value: {A, B, D} weight 10, value 15.
    """
    items = [(2, 3), (3, 4), (4, 5), (5, 8), (9, 10)]
    names = ["A", "B", "C", "D", "E"]
    return items, names, 10, 15, ["A", "B", "D"]


def random_instance(n, seed=1311):
    rng = random.Random(seed + n)
    items = [(rng.randint(1, 20), rng.randint(5, 50)) for _ in range(n)]
    limit = int(0.4 * sum(w for w, _ in items))
    return items, limit


def run(sizes=(8, 10, 12, 14, 16, 18, 20)):
    rows = []

    # Correctness check on the hand instance.
    items, names, limit, expected_value, expected_set = hand_instance()
    res = exhaustive_search(items, limit)
    chosen_names = [names[i] for i in res["best_set"]]
    assert res["best_value"] == expected_value and sorted(chosen_names) == sorted(expected_set)
    rows.append({"instance": "hand_5_items", "n": 5, "candidates": res["candidates"],
                 "feasible": res["feasible"], "best_value": res["best_value"],
                 "best_set": "+".join(sorted(chosen_names)), "dp_value": dp_reference(items, limit),
                 "time_ms": None})

    for n in sizes:
        items, limit = random_instance(n)
        t0 = time.perf_counter()
        res = exhaustive_search(items, limit)
        elapsed = time.perf_counter() - t0
        dp = dp_reference(items, limit)
        assert res["best_value"] == dp, "exhaustive optimum disagrees with DP"
        rows.append({"instance": f"random_{n}", "n": n, "candidates": res["candidates"],
                     "feasible": res["feasible"], "best_value": res["best_value"],
                     "best_set": "", "dp_value": dp,
                     "time_ms": round(elapsed * 1000, 3)})
    return rows


if __name__ == "__main__":
    for r in run(sizes=(8, 12)):
        print(r)

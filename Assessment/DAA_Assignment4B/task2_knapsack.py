"""Task 2 - Greedy (fractional knapsack) vs Dynamic Programming (0/1 knapsack).
Items are (id, weight, value).  Algorithm functions return data + operation counters; printing is separate.
"""
import random
import time
import tracemalloc
from functools import cmp_to_key


# ------------------------------------------------------------------ Solution A: greedy
def sort_by_ratio(items, counter):
    """Sort by value/weight descending, counting key comparisons."""
    def cmp(a, b):
        counter["comparisons"] += 1
        ra, rb = a[2] / a[1], b[2] / b[1]
        return -1 if ra > rb else (1 if ra < rb else 0)
    return sorted(items, key=cmp_to_key(cmp))


def fractional_greedy(items, capacity):
    """Fractional knapsack - provably optimal.  Returns (value, picks, steps, counters)."""
    ctr = {"comparisons": 0, "scan_steps": 0}
    remaining, value, picks, steps = capacity, 0.0, [], []
    for iid, w, v in sort_by_ratio(items, ctr):
        ctr["scan_steps"] += 1
        if remaining == 0:
            break
        take = min(w, remaining)
        frac = take / w
        value += v * frac
        remaining -= take
        picks.append((iid, frac))
        steps.append(f"{iid}: w={w} v={v} ratio={v/w:.2f} -> take {frac:.0%} ({take} units), capacity left={remaining}, value={value:g}")
    return value, picks, steps, ctr


def greedy_01(items, capacity):
    """The SAME ratio intuition applied to 0/1 (take whole item if it fits, never take fractions)."""
    ctr = {"comparisons": 0, "scan_steps": 0}
    remaining, value, picks, steps = capacity, 0, [], []
    for iid, w, v in sort_by_ratio(items, ctr):
        ctr["scan_steps"] += 1
        if w <= remaining:
            remaining -= w
            value += v
            picks.append(iid)
            steps.append(f"{iid}: w={w} v={v} ratio={v/w:.2f} -> TAKE, capacity left={remaining}, value={value}")
        else:
            steps.append(f"{iid}: w={w} v={v} ratio={v/w:.2f} -> skip (needs {w}, only {remaining} left)")
    return value, picks, steps, ctr


def greedy_01_plus_best_single(items, capacity):
    """Classic 1/2-approximation: better of ratio-greedy and the single most valuable item that fits."""
    value, picks, _, ctr = greedy_01(items, capacity)
    fits = [it for it in items if it[1] <= capacity]
    if fits:
        best = max(fits, key=lambda it: it[2])
        if best[2] > value:
            return best[2], [best[0]], ctr
    return value, picks, ctr


# ------------------------------------------------------------------ Solution B: 0/1 DP
def knapsack_dp(items, capacity):
    """K[i][c] = best value using the first i items with capacity c.  Returns (value, picks, table, counters)."""
    n = len(items)
    table = [[0] * (capacity + 1) for _ in range(n + 1)]
    ctr = {"cell_evaluations": 0, "table_cells": (n + 1) * (capacity + 1)}
    for i in range(1, n + 1):
        _, w, v = items[i - 1]
        for c in range(capacity + 1):
            ctr["cell_evaluations"] += 1
            best = table[i - 1][c]                       # skip item i
            if w <= c and table[i - 1][c - w] + v > best:  # take item i
                best = table[i - 1][c - w] + v
            table[i][c] = best
    picks, c = [], capacity
    for i in range(n, 0, -1):                              # trace back
        if table[i][c] != table[i - 1][c]:
            picks.append(items[i - 1][0])
            c -= items[i - 1][1]
    return table[n][capacity], picks[::-1], table, ctr


def show(items, capacity, title):
    print(f"--- {title} (capacity={capacity}) ---")
    print("Item  Weight  Value  Value/Weight")
    for iid, w, v in items:
        print(f"{iid:<5} {w:>6} {v:>6} {v/w:>12.2f}")


def run_case(items, capacity, title):
    show(items, capacity, title)
    fv, fp, fsteps, fc = fractional_greedy(items, capacity)
    print("\n[A] Fractional greedy decision sequence:")
    for s in fsteps:
        print("   ", s)
    print(f"    Selected: {[(i, f'{f:.0%}') for i, f in fp]}   Value = {fv:g}   counters={fc}")
    gv, gp, gsteps, gc = greedy_01(items, capacity)
    print("\n[A'] Same ratio rule forced into 0/1 form (whole items only):")
    for s in gsteps:
        print("   ", s)
    print(f"    Selected: {gp}   Value = {gv}   counters={gc}")
    dv, dp_picks, _, dc = knapsack_dp(items, capacity)
    print(f"\n[B] 0/1 DP: Selected = {dp_picks}   Value = {dv}   counters={dc}")
    print(f"    Greedy(0/1) is optimal? {gv == dv}   gap = {dv - gv}\n")
    return fv, gv, dv


if __name__ == "__main__":
    print("=== 2.1 NORMAL CASE ===")
    d1 = [("I1", 10, 60), ("I2", 20, 100), ("I3", 20, 70), ("I4", 15, 30), ("I5", 25, 50), ("I6", 40, 40)]
    run_case(d1, 50, "Dataset D1")

    print("=== 2.1b Same ratio rule where a fraction IS needed (classic) ===")
    d1b = [("X", 10, 60), ("Y", 20, 100), ("Z", 30, 120)]
    run_case(d1b, 50, "Dataset D1b")

    print("=== 2.2 BREAK THE GREEDY INTUITION ===")
    d2 = [("A", 6, 12), ("B", 5, 9), ("C", 5, 9)]
    fv, gv, dv = run_case(d2, 10, "Dataset D2 (student-designed counterexample)")
    print("First wrong commitment: taking item A (highest ratio 2.00, weight 6) leaves capacity 4;")
    print("neither B nor C (weight 5) can ever fit again, so the optimum {B,C} = 18 is unreachable.\n")

    print("=== 2.3 ENGINEERING COMPARISON ===")
    random.seed(7)
    print("(a) Quality over 2000 random instances (n=15, W=50, weights 1-20, values 1-50)")
    trials, opt_hits, ratios, hyb_ratios, worst = 2000, 0, [], [], (1, None)
    for _ in range(trials):
        items = [(f"i{k}", random.randint(1, 20), random.randint(1, 50)) for k in range(15)]
        gv, _, _, _ = greedy_01(items, 50)
        hv, _, _ = greedy_01_plus_best_single(items, 50)
        dv, *_ = knapsack_dp(items, 50)
        opt_hits += gv == dv
        ratios.append(gv / dv)
        hyb_ratios.append(hv / dv)
        if gv / dv < worst[0]:
            worst = (gv / dv, (gv, dv))
    print(f"    greedy optimal in {opt_hits}/{trials} = {opt_hits/trials:.1%};  mean quality = {sum(ratios)/trials:.4f};  worst = {worst[0]:.4f} (greedy={worst[1][0]}, optimum={worst[1][1]})")
    print(f"    greedy+best-single: mean quality = {sum(hyb_ratios)/trials:.4f};  worst = {min(hyb_ratios):.4f}")

    print("\n(b) Work and memory as the problem grows  (value 1-100, weight 1-50, capacity W)")
    print(f"{'n':>6} {'W':>7} | {'greedy cmp':>10} {'greedy scan':>11} {'greedy mem(items)':>17} | {'DP cell evals':>13} {'DP table cells':>14} {'DP peak MB':>10} | {'t_greedy ms':>11} {'t_DP ms':>9}")
    for n, W in [(10, 100), (100, 1000), (500, 5000), (1000, 5000), (1000, 10000)]:
        items = [(f"i{k}", random.randint(1, 50), random.randint(1, 100)) for k in range(n)]
        t0 = time.perf_counter(); _, _, _, gc = greedy_01(items, W); tg = (time.perf_counter() - t0) * 1000
        t0 = time.perf_counter(); _, _, _, dc = knapsack_dp(items, W); td = (time.perf_counter() - t0) * 1000   # timed WITHOUT profiler
        tracemalloc.start()
        knapsack_dp(items, W)                                                                                   # separate run for memory
        peak = tracemalloc.get_traced_memory()[1] / 1e6
        tracemalloc.stop()
        print(f"{n:>6} {W:>7} | {gc['comparisons']:>10} {gc['scan_steps']:>11} {n:>17} | {dc['cell_evaluations']:>13} {dc['table_cells']:>14} {peak:>10.1f} | {tg:>11.2f} {td:>9.1f}")

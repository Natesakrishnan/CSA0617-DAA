"""Q4 - Brute-force closest pair of drones.

Every unordered pair {i, j} with i < j is examined exactly once, so the number of
candidate pairs is n(n-1)/2. Distances are compared in squared form with integer
coordinates, which keeps the arithmetic exact.
"""
import random
import time
import math


def gen_points(n, seed=1311, span=100000):
    """n distinct integer points in [0, span]^2 (drone positions at one instant)."""
    rng = random.Random(seed + n)
    pts = set()
    while len(pts) < n:
        pts.add((rng.randint(0, span), rng.randint(0, span)))
    pts = list(pts)
    rng.shuffle(pts)
    return pts


def brute_closest(points):
    """Return (best_pair, distance, pairs_examined, distance_calculations)."""
    n = len(points)
    best_sq = None
    best_pair = None
    pairs = 0
    calcs = 0
    for i in range(n):
        xi, yi = points[i]
        for j in range(i + 1, n):
            pairs += 1
            calcs += 1
            dx = xi - points[j][0]
            dy = yi - points[j][1]
            d2 = dx * dx + dy * dy
            if best_sq is None or d2 < best_sq:
                best_sq = d2
                best_pair = (points[i], points[j])
    return best_pair, math.sqrt(best_sq), pairs, calcs


def run(sizes=(100, 200, 400, 800, 1600), repeats=2):
    rows = []
    for n in sizes:
        pts = gen_points(n)
        (pair, dist, pairs, calcs) = brute_closest(pts)
        assert pairs == n * (n - 1) // 2
        best = float("inf")
        for _ in range(repeats):
            t0 = time.perf_counter()
            brute_closest(pts)
            best = min(best, time.perf_counter() - t0)
        rows.append({
            "n": n,
            "theoretical_pairs_n(n-1)/2": n * (n - 1) // 2,
            "pairs_examined": pairs,
            "distance_calculations": calcs,
            "closest_distance": round(dist, 4),
            "time_ms": round(best * 1000, 3),
        })
    return rows


if __name__ == "__main__":
    for r in run(sizes=(200,)):
        print(r)

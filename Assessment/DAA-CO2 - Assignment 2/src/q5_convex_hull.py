"""Q5 - Brute-force convex hull derived from the supplied geometric principle.

Principle used: a directed segment i -> j is a hull edge (with the interior on its left)
when every other point lies on the left side of the line through i and j, or exactly on
that line.

Decision rule implemented, using the sign of the cross product
    cross(i, j, k) = (xj - xi)*(yk - yi) - (yj - yi)*(xk - xi)
  - cross > 0  : k is left of i->j
  - cross < 0  : k is right of i->j  -> i->j is NOT a hull edge (stop early)
  - cross = 0  : k is collinear with i and j. If k lies inside the closed segment
                 [i, j] it does not affect the edge. If k lies outside the segment,
                 the segment is only part of a longer boundary edge -> reject it.

All coordinates are integers, so the sign test is exact (no floating-point error).
Validation: the endpoints are compared with an independent monotone-chain (Andrew) hull.
"""
import random
import time


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _in_closed_segment(p, a, b):
    if cross(a, b, p) != 0:
        return False
    return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])


def brute_force_hull(points):
    """Return (hull vertices in CCW order, orientation tests performed, candidate pairs)."""
    n = len(points)
    orient_tests = 0
    candidate_pairs = 0
    next_of = {}
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            candidate_pairs += 1
            pi, pj = points[i], points[j]
            is_edge = True
            for k in range(n):
                if k == i or k == j:
                    continue
                orient_tests += 1
                c = cross(pi, pj, points[k])
                if c < 0:
                    is_edge = False
                    break
                if c == 0 and not _in_closed_segment(points[k], pi, pj):
                    is_edge = False
                    break
            if is_edge:
                next_of[i] = j

    if not next_of:
        return [], orient_tests, candidate_pairs

    start = min(next_of)
    hull = [start]
    cur = next_of[start]
    while cur != start:
        hull.append(cur)
        cur = next_of[cur]
    return [points[i] for i in hull], orient_tests, candidate_pairs


def monotone_chain(points):
    """Independent reference hull (strict vertices only), CCW order."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def _canonical(hull):
    """Rotate a CCW vertex list so it starts at its smallest point (for comparison)."""
    if not hull:
        return []
    k = hull.index(min(hull))
    return hull[k:] + hull[:k]


def random_points(n, seed=1311, span=1000):
    rng = random.Random(seed + n)
    pts = set()
    while len(pts) < n:
        pts.add((rng.randint(0, span), rng.randint(0, span)))
    return list(pts)


def test_configurations():
    """Two designed configurations plus the scaling inputs used in run()."""
    # A: boundary and interior points mixed.
    config_a = random_points(30, seed=7)
    # B: challenge set - the bottom hull edge contains two collinear points, (4,0) and
    # (8,0), which must be absorbed by the extreme pair (0,0)-(12,0) rather than
    # reported as separate edges; the left and right edges are axis-aligned; and
    # interior points sit close to the boundary (e.g. (3,2), (9,3)).
    config_b = [(0, 0), (4, 0), (8, 0), (12, 0), (12, 6), (6, 12), (0, 6),
                (3, 2), (9, 3), (5, 5), (6, 6), (7, 4)]
    return {"A_mixed_boundary_interior": config_a, "B_collinear_challenge": config_b}


def run(sizes=(10, 20, 40, 60, 80, 100), repeats=1):
    rows = []
    for name, pts in test_configurations().items():
        hull, tests, pairs = brute_force_hull(pts)
        ref = monotone_chain(pts)
        ok = _canonical(hull) == _canonical(ref)
        rows.append({"config": name, "n": len(pts), "hull_vertices": len(hull),
                     "matches_monotone_chain": ok, "orientation_tests": tests,
                     "candidate_pairs": pairs, "time_ms": None})
        assert ok, f"hull mismatch on {name}"

    for n in sizes:
        pts = random_points(n)
        best = float("inf")
        for _ in range(repeats):
            t0 = time.perf_counter()
            hull, tests, pairs = brute_force_hull(pts)
            best = min(best, time.perf_counter() - t0)
        ok = _canonical(hull) == _canonical(monotone_chain(pts))
        assert ok
        rows.append({"config": "scaling_random", "n": n, "hull_vertices": len(hull),
                     "matches_monotone_chain": ok, "orientation_tests": tests,
                     "candidate_pairs": pairs, "time_ms": round(best * 1000, 3)})
    return rows


if __name__ == "__main__":
    for cfg, pts in test_configurations().items():
        hull, _, _ = brute_force_hull(pts)
        print(cfg, hull)

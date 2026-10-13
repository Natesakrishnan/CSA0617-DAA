"""Q7 - Diagnose, redesign and validate.

Chosen solution: brute-force closest pair from Q4.

A. Diagnosis (from Q4 evidence)
   The original algorithm computes n(n-1)/2 distances, i.e. every pair, including pairs
   that are very far apart. Its distance-calculation count grows quadratically and
   nothing is ever skipped. The repeated work is the examination of pairs that cannot
   possibly beat the current best distance.

B. Design objective
   Reduce distance calculations by at least 90% at n = 1600 on uniform random input,
   while keeping the answer exactly equal to the brute-force answer.

C. Revised strategy (sort-and-sweep with a provable pruning rule)
   Preprocessing: sort points by x (O(n log n)).
   Key property: if the points are sorted by x, then for a fixed i the x-gap to later
   points j only grows. Once (x_j - x_i)^2 >= best_sq, no later j can give a smaller
   distance, so the inner loop can stop. The best distance is updated as we go.
   Extra memory: O(n) for the sorted copy.
   Trade-off: worst case (many points sharing nearly the same x) still approaches n^2.

D. Prediction (written before running): distance calculations should fall from
   n(n-1)/2 to roughly linear in n on uniform random points; execution time should drop
   accordingly; the redesign should be no less accurate; on a vertical-line input the
   pruning gives no benefit (the limitation the design deliberately keeps).

E. Validation: same inputs as Q4, plus a collinear vertical-line stress input.
"""
import math
import time

from q4_closest_pair import brute_closest, gen_points


def pruned_closest(points):
    """Return (best_pair, distance, pairs_examined, distance_calculations)."""
    order = sorted(points)                 # preprocessing: sort by x, then y
    n = len(order)
    best_sq = None
    best_pair = None
    examined = 0
    calcs = 0
    for i in range(n):
        xi, yi = order[i]
        for j in range(i + 1, n):
            xj, yj = order[j]
            examined += 1
            dx = xj - xi
            if best_sq is not None and dx * dx >= best_sq:
                break                      # no later j can beat best_sq
            calcs += 1
            dy = yj - yi
            d2 = dx * dx + dy * dy
            if best_sq is None or d2 < best_sq:
                best_sq = d2
                best_pair = (order[i], order[j])
    return best_pair, math.sqrt(best_sq), examined, calcs


def vertical_line(n):
    """Stress input: all points share x (pruning cannot remove any pair)."""
    return [(0, 3 * k) for k in range(n)]


def run(sizes=(100, 200, 400, 800, 1600), repeats=2):
    rows = []
    for n in sizes:
        pts = gen_points(n)
        b_pair, b_dist, b_pairs, b_calcs = brute_closest(pts)
        o_pair, o_dist, o_examined, o_calcs = pruned_closest(pts)
        assert abs(b_dist - o_dist) < 1e-9, "redesign disagrees with brute force"

        t_brute = min(_timed(brute_closest, pts) for _ in range(repeats))
        t_pruned = min(_timed(pruned_closest, pts) for _ in range(repeats))
        rows.append({
            "input": "uniform_random", "n": n,
            "original_distance_calcs": b_calcs, "redesign_distance_calcs": o_calcs,
            "original_pairs_examined": b_pairs, "redesign_pairs_examined": o_examined,
            "reduction_pct": round(100 * (1 - o_calcs / b_calcs), 2),
            "original_time_ms": round(t_brute * 1000, 3),
            "redesign_time_ms": round(t_pruned * 1000, 3),
            "answers_equal": abs(b_dist - o_dist) < 1e-9,
        })

    for n in (200, 800):
        pts = vertical_line(n)
        b = brute_closest(pts)
        o = pruned_closest(pts)
        rows.append({
            "input": "vertical_line_stress", "n": n,
            "original_distance_calcs": b[3], "redesign_distance_calcs": o[3],
            "original_pairs_examined": b[2], "redesign_pairs_examined": o[2],
            "reduction_pct": round(100 * (1 - o[3] / b[3]), 2),
            "original_time_ms": None, "redesign_time_ms": None,
            "answers_equal": abs(b[1] - o[1]) < 1e-9,
        })
    return rows


def _timed(fn, arg):
    t0 = time.perf_counter()
    fn(arg)
    return time.perf_counter() - t0


if __name__ == "__main__":
    for r in run(sizes=(200,)):
        print(r)

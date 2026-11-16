"""Task 6 - Travelling salesperson (delivery route) by Held-Karp dynamic programming.

Node 0 is the distribution hub; delivery locations are 1..n.
State  : DP[S][j]  with S a bitmask over locations 1..n (bit j-1 set <=> location j visited), j in S = current location.
Base   : DP[{j}][j] = cost[0][j]
Step   : DP[S][j]   = min over i in S\\{j} of  DP[S\\{j}][i] + cost[i][j]
Answer : min over j of  DP[all][j] + cost[j][0]
"""
import itertools
import math
import random
import time
import tracemalloc

INF = float("inf")


def held_karp(cost):
    """Return (best_cost, route_as_node_list, stats).  cost is an (n+1)x(n+1) matrix, node 0 = hub."""
    n = len(cost) - 1
    if n < 1:
        raise ValueError("need at least one delivery location")
    full = (1 << n) - 1
    dp = [[INF] * (n + 1) for _ in range(1 << n)]
    parent = [[-1] * (n + 1) for _ in range(1 << n)]
    states = transitions = 0
    for j in range(1, n + 1):                               # base states: hub -> j
        dp[1 << (j - 1)][j] = cost[0][j]
        states += 1
    for mask in range(1, 1 << n):                           # increasing masks => subsets are always solved first
        for j in range(1, n + 1):
            bit = 1 << (j - 1)
            if not mask & bit or mask == bit:
                continue
            prev = mask ^ bit
            states += 1
            for i in range(1, n + 1):
                if prev & (1 << (i - 1)):
                    transitions += 1
                    cand = dp[prev][i] + cost[i][j]
                    if cand < dp[mask][j]:
                        dp[mask][j], parent[mask][j] = cand, i
    best, last = INF, -1
    for j in range(1, n + 1):                               # close the tour: return to the hub
        total = dp[full][j] + cost[j][0]
        if total < best:
            best, last = total, j
    route, mask, j = [], full, last
    while j != -1:
        route.append(j)
        mask, j = mask ^ (1 << (j - 1)), parent[mask][j]
    route.reverse()
    return best, [0] + route + [0], {"states": states, "transitions": transitions, "table_entries": (1 << n) * n}


def brute_force(cost):
    """Independent reference: try every permutation of the delivery locations."""
    n = len(cost) - 1
    results = []
    for perm in itertools.permutations(range(1, n + 1)):
        path = (0,) + perm + (0,)
        results.append((sum(cost[a][b] for a, b in zip(path, path[1:])), path))
    return sorted(results)


COORDS = {"Hub": (0, 0), "A": (4, 7), "B": (9, 2), "C": (6, 10), "D": (12, 8), "E": (3, 3), "F": (8, 6)}


def cost_matrix_from_coords(coords):
    pts = list(coords.values())
    return [[round(math.dist(p, q)) for q in pts] for p in pts]


def show_matrix(names, m):
    print("      " + "".join(f"{n:>5}" for n in names))
    for n, row in zip(names, m):
        print(f"{n:>5} " + "".join(f"{x:>5}" for x in row))


if __name__ == "__main__":
    names = list(COORDS)
    C = cost_matrix_from_coords(COORDS)
    print("=== 6.3 Input cost matrix (hub + 6 locations; rounded Euclidean distances) ===")
    show_matrix(names, C)
    best, route, stats = held_karp(C)
    print("\nOptimal route :", " -> ".join(names[k] for k in route))
    print("Visit order   :", [names[k] for k in route[1:-1]])
    legs = [f"{names[a]}->{names[b]}={C[a][b]}" for a, b in zip(route, route[1:])]
    print("Legs          :", ", ".join(legs))
    print("Minimum Travel Cost =", best, "  stats:", stats)

    print("\n=== 6.4 Validation: hub + 4 delivery locations (A,B,C,D) ===")
    C4 = [row[:5] for row in C[:5]]
    ref = brute_force(C4)
    dp_best, dp_route, _ = held_karp(C4)
    print(f"{'#':>2} {'route':<28}{'cost':>5}")
    for k, (c, path) in enumerate(ref, 1):
        print(f"{k:>2} {' -> '.join(names[x] for x in path):<28}{c:>5}")
    print(f"Exhaustive optimum = {ref[0][0]} ;  DP optimum = {dp_best}  route {' -> '.join(names[x] for x in dp_route)} ;  match = {ref[0][0] == dp_best}")
    tied = [p for c, p in ref if c == ref[0][0]]
    print(f"Number of optimal routes in the reference: {len(tied)} (a route and its reverse have equal cost in a symmetric matrix)")
    random.seed(3)
    mism = 0
    for _ in range(300):
        n = random.randint(1, 7)
        M = [[0 if a == b else random.randint(1, 50) for b in range(n + 1)] for a in range(n + 1)]   # asymmetric on purpose
        mism += held_karp(M)[0] != brute_force(M)[0][0]
    print("300 random asymmetric instances (1-7 locations): DP vs exhaustive mismatches =", mism)
    print("Boundary: 1 location, cost 5 out / 9 back -> DP =", held_karp([[0, 5], [9, 0]])[0], "(expected 14)")

    print("\n=== 6.5 State-space growth (random complete graphs) ===")
    print(f"{'n':>3} {'DP states':>10} {'n*2^(n-1)':>10} {'transitions':>12} {'table entries n*2^n':>20} {'n! routes':>14} {'time (s)':>9} {'peak MB':>8}")
    rnd = random.Random(5)
    rows = []
    for n in range(4, 16):
        M = [[0 if a == b else rnd.randint(5, 100) for b in range(n + 1)] for a in range(n + 1)]
        t0 = time.perf_counter()
        _, _, st = held_karp(M)
        dt = time.perf_counter() - t0
        tracemalloc.start()
        held_karp(M)
        peak = tracemalloc.get_traced_memory()[1] / 1e6
        tracemalloc.stop()
        rows.append((n, st["states"], dt))
        print(f"{n:>3} {st['states']:>10} {n * 2 ** (n - 1):>10} {st['transitions']:>12} {st['table_entries']:>20} {math.factorial(n):>14} {dt:>9.3f} {peak:>8.1f}")

    print("\n=== 6.6 Extrapolation for 200 delivery locations ===")
    n = 200
    print(f"subsets of locations: 2^200 = {2 ** n:.3e}")
    print(f"DP states            : 200 * 2^199 = {n * 2 ** (n - 1):.3e}")
    print(f"even at 10^9 states per second this needs {n * 2 ** (n - 1) / 1e9 / 3.15e7:.3e} years")
    print(f"table memory at 8 bytes/entry: {n * 2 ** n * 8:.3e} bytes")

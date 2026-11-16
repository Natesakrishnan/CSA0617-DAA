"""Task 4 - Assembly-line scheduling by Dynamic Programming (two lines, n stations).

Conventions (0-based station index i):
  a[l][i]  processing time of station i on line l          e[l]  entry time of line l      x[l] exit time of line l
  t[l][i]  time to transfer AWAY from line l after station i, before station i+1 (i = 0..n-2)
DP:  f[l][i] = fastest time to finish station i on line l
     f[l][0] = e[l] + a[l][0]
     f[l][i] = a[l][i] + min( f[l][i-1]                   (stay),
                              f[1-l][i-1] + t[1-l][i-1] )  (transfer from the other line)
     answer  = min_l ( f[l][n-1] + x[l] )
"""
import copy
import sys

BASE = {
    "a": [[7, 9, 3, 4, 8, 4], [8, 5, 6, 4, 5, 7]],
    "t": [[2, 3, 1, 3, 4], [2, 1, 2, 2, 1]],
    "e": [2, 4],
    "x": [3, 2],
}


def validate(p):
    n = len(p["a"][0])
    if n == 0 or len(p["a"][1]) != n:
        raise ValueError("both lines need the same, non-zero number of stations")
    if any(len(p["t"][l]) != n - 1 for l in (0, 1)):
        raise ValueError("each transfer list needs n-1 entries")
    if any(v < 0 for row in p["a"] + p["t"] for v in row) or min(p["e"] + p["x"]) < 0:
        raise ValueError("times must be non-negative")


def assembly_dp(p):
    """Return (best_time, route, f, choice, trace).  route = [(line, station)], lines are 0/1."""
    validate(p)
    a, t, e, x = p["a"], p["t"], p["e"], p["x"]
    n = len(a[0])
    f = [[0] * n for _ in range(2)]
    came_from = [[None] * n for _ in range(2)]      # line used at station i-1 for the best way into (l,i)
    trace = []
    for l in (0, 1):
        f[l][0] = e[l] + a[l][0]
    for i in range(1, n):
        row = {"station": i + 1}
        for l in (0, 1):
            other = 1 - l
            stay = f[l][i - 1] + a[l][i]
            move = f[other][i - 1] + t[other][i - 1] + a[l][i]
            if stay <= move:                         # ties keep the production on the same line
                f[l][i], came_from[l][i], pick = stay, l, "Stay"
            else:
                f[l][i], came_from[l][i], pick = move, other, "Transfer"
            row[l] = (stay, move, pick)
        trace.append(row)
    finish = [f[l][n - 1] + x[l] for l in (0, 1)]
    last = 0 if finish[0] <= finish[1] else 1
    best = finish[last]
    route, l = [], last
    for i in range(n - 1, -1, -1):                   # route reconstruction by following came_from
        route.append((l, i))
        if i > 0:
            l = came_from[l][i]
    route.reverse()
    return best, route, f, finish, trace


def print_trace(p, f, finish, trace):
    print("Stage 1 (entry):  f1 = e1 + a1[1] = %d    f2 = e2 + a2[1] = %d" % (f[0][0], f[1][0]))
    print(f"{'Stn':>3} | {'L1 by Stay':>10} {'L1 by Transfer':>14} {'Selected':>9} {'f1':>4} || {'L2 by Stay':>10} {'L2 by Transfer':>14} {'Selected':>9} {'f2':>4}")
    for row in trace:
        s1, m1, p1 = row[0]
        s2, m2, p2 = row[1]
        i = row["station"] - 1
        print(f"{row['station']:>3} | {s1:>10} {m1:>14} {p1:>9} {f[0][i]:>4} || {s2:>10} {m2:>14} {p2:>9} {f[1][i]:>4}")
    print(f"Exit: L1 finish = f1 + x1 = {finish[0]};  L2 finish = f2 + x2 = {finish[1]}")


def print_route(route, best):
    print("Entry")
    prev = None
    for l, i in route:
        tag = ""
        if prev is not None and prev != l:
            tag = f"  <-- TRANSFER Line {prev + 1} -> Line {l + 1}"
        print(" |" + tag)
        print(f" v\nLine {l + 1} - Station {i + 1}")
        prev = l
    print(" |\n v\nExit")
    transfers = [(route[k][1] + 1, route[k][0] + 1, route[k + 1][0] + 1) for k in range(len(route) - 1) if route[k][0] != route[k + 1][0]]
    print(f"Lines used per station: {[l + 1 for l, _ in route]}")
    print(f"Transfer points (after station, from line, to line): {transfers}")
    print(f"Minimum Production Time = {best}")


def run(title, p):
    print(f"##### {title} #####")
    print("a1 =", p["a"][0], " a2 =", p["a"][1])
    print("t1 =", p["t"][0], " t2 =", p["t"][1], " e =", p["e"], " x =", p["x"])
    best, route, f, finish, trace = assembly_dp(p)
    print_trace(p, f, finish, trace)
    print_route(route, best)
    print()
    return best, route


if __name__ == "__main__":
    which = sys.argv[1:] or ["base"]
    if "base" in which:
        run("4.1/4.2 BASE CASE", BASE)
    # ---- regression / validation helpers --------------------------------------------------
    import itertools
    import random

    def brute_force(p):
        n = len(p["a"][0])
        best = float("inf")
        for lines in itertools.product((0, 1), repeat=n):          # every possible line choice per station
            cost = p["e"][lines[0]] + p["a"][lines[0]][0]
            for i in range(1, n):
                cost += p["a"][lines[i]][i] + (p["t"][lines[i - 1]][i - 1] if lines[i] != lines[i - 1] else 0)
            best = min(best, cost + p["x"][lines[-1]])
        return best

    if "exp43" in which:
        # PREDICTION (recorded before running): raising t2 after station 2 (Line2->Line1) from 1 to 20 changes the route;
        # that transfer disappears; production stays on Line 1 for stations 1-3; total rises but by only ~1-3 units.
        p = copy.deepcopy(BASE)
        p["t"][1][1] = 20
        run("4.3 TRANSFER t2[after station 2] raised 1 -> 20", p)
    if "exp44" in which:
        p = copy.deepcopy(BASE)
        p["a"][1][3] = 15                                         # Line 2 / Station 4 slows from 4 to 15
        run("4.4 DISRUPTION: Line 2 Station 4 processing time 4 -> 15", p)
    if "tests" in which:
        print("##### REGRESSION TESTS #####")
        print("Base case: DP =", assembly_dp(BASE)[0], " brute force =", brute_force(BASE))
        random.seed(1)
        bad = 0
        for _ in range(1000):
            n = random.randint(1, 9)
            q = {"a": [[random.randint(1, 20) for _ in range(n)] for _ in range(2)],
                 "t": [[random.randint(0, 10) for _ in range(n - 1)] for _ in range(2)],
                 "e": [random.randint(0, 9), random.randint(0, 9)], "x": [random.randint(0, 9), random.randint(0, 9)]}
            bad += assembly_dp(q)[0] != brute_force(q)
        print("1000 random instances (n = 1..9): mismatches DP vs brute force =", bad)
        one = {"a": [[5], [3]], "t": [[], []], "e": [1, 4], "x": [2, 2]}
        print("Boundary n=1: DP =", assembly_dp(one)[0], "(expected min(1+5+2, 4+3+2) = 8)  route =", assembly_dp(one)[1])
        try:
            assembly_dp({"a": [[1, 2], [3]], "t": [[1], []], "e": [0, 0], "x": [0, 0]})
        except ValueError as err:
            print("Invalid input rejected:", err)

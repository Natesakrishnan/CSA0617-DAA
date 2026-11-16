"""Task 3 - Routing engine: Dijkstra, Bellman-Ford (with negative-cycle detection), Floyd, Warshall."""
import heapq

INF = float("inf")
VERTICES = list("ABCDEFGH")

# Directed weighted network: (from, to, cost)
BASE_EDGES = [
    ("A", "B", 3), ("A", "C", 4), ("B", "D", 2), ("C", "B", 6), ("C", "E", 3),
    ("D", "F", 4), ("E", "D", 5), ("E", "G", 6), ("F", "H", 3), ("G", "H", 2),
    ("D", "G", 7), ("B", "E", 8), ("F", "G", 1), ("G", "E", 2),
]


def with_edge_changed(edges, u, v, new_w):
    return [(a, b, new_w if (a, b) == (u, v) else w) for a, b, w in edges]


def adjacency(vertices, edges):
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))
    return adj


def build_path(pred, source, target):
    if target != source and pred[target] is None:
        return None
    path = [target]
    while path[-1] != source:
        path.append(pred[path[-1]])
    return path[::-1]


# ---------------------------------------------------------------- Stage A : Dijkstra
def dijkstra(vertices, edges, source):
    """Classic Dijkstra: a vertex is FINAL once popped; final vertices are never revisited."""
    adj = adjacency(vertices, edges)
    dist = {v: INF for v in vertices}
    pred = {v: None for v in vertices}
    dist[source] = 0
    heap, finalised, order = [(0, source)], set(), []
    while heap:
        d, u = heapq.heappop(heap)
        if u in finalised:
            continue
        finalised.add(u)
        order.append((u, d))
        for v, w in adj[u]:
            if v not in finalised and d + w < dist[v]:
                dist[v], pred[v] = d + w, u
                heapq.heappush(heap, (dist[v], v))
    return dist, pred, order


# ---------------------------------------------------------------- Stage B/C : Bellman-Ford
def bellman_ford(vertices, edges, source):
    """Returns (dist, pred, negative_cycle or None, passes_used)."""
    dist = {v: INF for v in vertices}
    pred = {v: None for v in vertices}
    dist[source] = 0
    passes = 0
    for _ in range(len(vertices) - 1):               # at most V-1 passes
        changed = False
        passes += 1
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v], pred[v], changed = dist[u] + w, u, True
        if not changed:                              # early exit
            break
    for u, v, w in edges:                            # V-th pass: any improvement => negative cycle
        if dist[u] != INF and dist[u] + w < dist[v]:
            pred[v] = u
            x = v
            for _ in range(len(vertices)):           # walk back V steps: guaranteed to land ON the cycle
                x = pred[x]
            cycle, y = [x], pred[x]
            while y != x:
                cycle.append(y)
                y = pred[y]
            cycle.append(x)
            return dist, pred, cycle[::-1], passes + 1
    return dist, pred, None, passes


# ---------------------------------------------------------------- Stage D : Floyd and Warshall
def floyd(vertices, edges):
    idx = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    d = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for u, v, w in edges:
        d[idx[u]][idx[v]] = min(d[idx[u]][idx[v]], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d


def warshall(vertices, edges):
    idx = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    r = [[i == j for j in range(n)] for i in range(n)]
    for u, v, _ in edges:
        r[idx[u]][idx[v]] = True
    for k in range(n):
        for i in range(n):
            for j in range(n):
                r[i][j] = r[i][j] or (r[i][k] and r[k][j])
    return r


# ---------------------------------------------------------------- presentation helpers
def show_matrix(vertices, m, fmt):
    print("     " + "".join(f"{v:>5}" for v in vertices))
    for v, row in zip(vertices, m):
        print(f"  {v}  " + "".join(f"{fmt(x):>5}" for x in row))


def show_routes(vertices, dist, pred, source):
    print(f"  {'To':<3}{'Dist':>6}  {'Pred':<5} Path")
    for v in vertices:
        p = build_path(pred, source, v)
        print(f"  {v:<3}{('INF' if dist[v] == INF else dist[v]):>6}  {str(pred[v]) if pred[v] else '-':<5} {' -> '.join(p) if p else 'unreachable'}")


if __name__ == "__main__":
    print("Network: 8 vertices, %d directed edges" % len(BASE_EDGES))
    print("Edges:", ", ".join(f"{u}->{v}({w})" for u, v, w in BASE_EDGES))

    print("\n=== STAGE A : Dijkstra from A (all weights positive) ===")
    d, p, order = dijkstra(VERTICES, BASE_EDGES, "A")
    print("Order in which vertices are finalised:", ", ".join(f"{v}({dd})" for v, dd in order))
    show_routes(VERTICES, d, p, "A")

    print("""
=== STAGE B : PREDICTION (written BEFORE running the modified graph) ===
Change: C->B cost 6 becomes -2.
 1. Dijkstra will NOT stay valid: it pops B (dist 3, via A->B) before C (dist 4). B is then final, but
    the path A->C->B now costs 4-2 = 2 < 3, and Dijkstra refuses to revisit final vertices.
 2. Affected decision: the route to B, and every vertex whose best route runs through B (D, F, G, H, E).
    Expected correct values: B=2 (via C), D=4, F=8, H=11. Dijkstra will report B=3, D=5, F=9, H=12.
""")
    neg_edges = with_edge_changed(BASE_EDGES, "C", "B", -2)
    print("=== STAGE B : RESULTS ===")
    dd, pd, od = dijkstra(VERTICES, neg_edges, "A")
    print("Dijkstra (finalisation order):", ", ".join(f"{v}({x})" for v, x in od))
    show_routes(VERTICES, dd, pd, "A")
    bd, bp, bc, passes = bellman_ford(VERTICES, neg_edges, "A")
    print(f"\nBellman-Ford ({passes} passes, negative cycle: {bc}):")
    show_routes(VERTICES, bd, bp, "A")
    print("\nVertices where Dijkstra is WRONG:", [v for v in VERTICES if dd[v] != bd[v]])
    print("  " + "; ".join(f"{v}: Dijkstra={dd[v]} vs correct={bd[v]}" for v in VERTICES if dd[v] != bd[v]))

    print("\n=== STAGE C : reachable negative cycle (add B->C cost 1; cycle C->B->C = -2+1 = -1) ===")
    cyc_edges = neg_edges + [("B", "C", 1)]
    cd, cp, cyc, passes = bellman_ford(VERTICES, cyc_edges, "A")
    if cyc:
        print(f"NEGATIVE CYCLE DETECTED after {passes} passes (V-th pass still relaxes an edge).")
        print("  Cycle:", " -> ".join(cyc), "  total cost =", sum(w for a, b, w in cyc_edges if (a, b) in set(zip(cyc, cyc[1:]))))
        print("  Shortest-path results are undefined and are NOT returned.")
    print("  (Dijkstra on the same graph would silently print numbers:", dijkstra(VERTICES, cyc_edges, "A")[0], ")")
    # unreachable negative cycle must not raise a false alarm
    iso = BASE_EDGES + [("X", "Y", -3), ("Y", "X", 1), ("Y", "Z", 1), ("Z", "X", -5)]
    _, _, c2, _ = bellman_ford(VERTICES + ["X", "Y", "Z"], iso, "A")
    print("  Control test - negative cycle X,Y,Z NOT reachable from A -> reported cycle:", c2)

    print("\n=== STAGE D : all-pairs on the Stage-A network ===")
    print("Floyd distance matrix (INF = no route):")
    show_matrix(VERTICES, floyd(VERTICES, BASE_EDGES), lambda x: "INF" if x == INF else x)
    print("\nWarshall reachability matrix (1 = reachable):")
    show_matrix(VERTICES, warshall(VERTICES, BASE_EDGES), lambda x: int(x))
    print("\nFloyd with the negative edge C->B = -2 (no negative cycle):")
    fm = floyd(VERTICES, neg_edges)
    show_matrix(VERTICES, fm, lambda x: "INF" if x == INF else x)
    print("Negative-cycle test on Floyd diagonal (Stage-C graph):",
          "negative diagonal entries ->", [v for v, row in zip(VERTICES, floyd(VERTICES, cyc_edges)) if row[VERTICES.index(v)] < 0])

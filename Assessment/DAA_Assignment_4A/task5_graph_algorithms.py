"""
Task 5 - Dijkstra, Bellman-Ford and Floyd-Warshall on the same directed
weighted graph.
"""

import math

EDGES = [
    ("A", "B", 4),
    ("A", "C", 7),
    ("B", "C", 2),
    ("B", "D", 6),
    ("C", "D", 1),
    ("D", "E", 3),
    ("C", "E", 8),
]
VERTICES = ["A", "B", "C", "D", "E"]


def dijkstra(vertices, edges, source):
    dist = {v: math.inf for v in vertices}
    pred = {v: None for v in vertices}
    dist[source] = 0
    visited = set()

    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))

    while len(visited) < len(vertices):
        # Selection of next vertex: smallest tentative distance, unvisited
        candidates = [v for v in vertices if v not in visited]
        u = min(candidates, key=lambda v: dist[v])
        if dist[u] == math.inf:
            break
        visited.add(u)

        for v, w in adj[u]:
            if v not in visited and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u

    return dist, pred


def bellman_ford(vertices, edges, source):
    dist = {v: math.inf for v in vertices}
    dist[source] = 0

    for _ in range(len(vertices) - 1):
        for u, v, w in edges:
            if dist[u] != math.inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # Negative-weight cycle check
    for u, v, w in edges:
        if dist[u] != math.inf and dist[u] + w < dist[v]:
            return dist, True  # negative cycle detected

    return dist, False


def floyd_warshall(vertices, edges):
    dist = {u: {v: math.inf for v in vertices} for u in vertices}
    for v in vertices:
        dist[v][v] = 0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)

    for k in vertices:
        for i in vertices:
            for j in vertices:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist


if __name__ == "__main__":
    print("Dijkstra from A (non-negative weights):")
    dist, pred = dijkstra(VERTICES, EDGES, "A")
    for v in VERTICES:
        print(f"  Dist[{v}] = {dist[v]}   Pred[{v}] = {pred[v]}")

    print("\nBellman-Ford from A (same graph, works even with negative weights):")
    dist_bf, has_neg_cycle = bellman_ford(VERTICES, EDGES, "A")
    for v in VERTICES:
        print(f"  Dist[{v}] = {dist_bf[v]}")
    print(f"  Negative-weight cycle detected: {has_neg_cycle}")

    print("\nFloyd-Warshall (all pairs shortest distances):")
    all_pairs = floyd_warshall(VERTICES, EDGES)
    header = "      " + "".join(f"{v:>6}" for v in VERTICES)
    print(header)
    for i in VERTICES:
        row = f"  {i}: " + "".join(
            f"{all_pairs[i][j] if all_pairs[i][j] != math.inf else 'inf':>6}"
            for j in VERTICES
        )
        print(row)

"""Task 5 - Kruskal, Prim and Boruvka on the same weighted undirected graph, with construction traces."""
import heapq
import itertools
import random

VERTS = list("ABCDEFGH")
BASE = [("A", "B", 4), ("A", "C", 3), ("B", "C", 2), ("B", "D", 6), ("C", "D", 5), ("C", "E", 9), ("D", "E", 7),
        ("D", "F", 11), ("E", "F", 8), ("E", "G", 12), ("F", "G", 10), ("G", "H", 1), ("F", "H", 13)]


def modified(edges):
    """Create ties: B-D 6->5 (ties with C-D) and C-E 9->8, D-E 7->8, (tie with E-F)."""
    new = {("B", "D"): 5, ("C", "E"): 8, ("D", "E"): 8}
    return [(u, v, new.get((u, v), w)) for u, v, w in edges]


class DisjointSet:
    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.finds = 0

    def find(self, x):
        self.finds += 1
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.parent[ra] = rb
        return True


def label(e):
    return f"{e[0]}-{e[1]}({e[2]})"


# ------------------------------------------------------------------ Kruskal
def kruskal(verts, edges, tie_sign=1, trace=None):
    """tie_sign=+1: equal weights keep input order; -1: equal weights reversed."""
    order = sorted(range(len(edges)), key=lambda i: (edges[i][2], tie_sign * i))
    ds, mst, examined = DisjointSet(verts), [], 0
    for i in order:
        u, v, w = edges[i]
        examined += 1
        ok = ds.union(u, v)
        if ok:
            mst.append(edges[i])
        if trace is not None:
            trace.append(f"  consider {label(edges[i]):<8} -> {'ACCEPT' if ok else 'reject (would close a cycle)':<30} forest edges={len(mst)}")
        if len(mst) == len(verts) - 1:
            break
    return mst, {"edges_examined": examined, "find_calls": ds.finds, "sort_size": len(edges)}


# ------------------------------------------------------------------ Prim
def prim(verts, edges, start, tie_sign=1, trace=None):
    adj = {v: [] for v in verts}
    for i, (u, v, w) in enumerate(edges):
        adj[u].append((w, tie_sign * i, v, i))
        adj[v].append((w, tie_sign * i, u, i))
    in_tree, mst, heap = {start}, [], list(adj[start])
    heapq.heapify(heap)
    pushes, pops = len(heap), 0
    if trace is not None:
        trace.append(f"  start at {start}; tree={sorted(in_tree)}")
    while heap and len(in_tree) < len(verts):
        w, _, v, i = heapq.heappop(heap)
        pops += 1
        if v in in_tree:
            continue
        in_tree.add(v)
        mst.append(edges[i])
        if trace is not None:
            trace.append(f"  cheapest crossing edge {label(edges[i]):<8} -> add vertex {v}; tree={sorted(in_tree)}")
        for item in adj[v]:
            if item[2] not in in_tree:
                heapq.heappush(heap, item)
                pushes += 1
    return mst, {"heap_pushes": pushes, "heap_pops": pops}


# ------------------------------------------------------------------ Boruvka
def boruvka(verts, edges, tie_sign=1, trace=None):
    """Every component picks its cheapest outgoing edge (ties broken by edge index) - all picks are merged at once."""
    ds, mst, rounds, scans = DisjointSet(verts), [], 0, 0
    comps = len(verts)
    while comps > 1:
        rounds += 1
        cheapest = {}
        for i, (u, v, w) in enumerate(edges):
            scans += 1
            ru, rv = ds.find(u), ds.find(v)
            if ru == rv:
                continue
            for r in (ru, rv):
                if r not in cheapest or (w, tie_sign * i) < (edges[cheapest[r]][2], tie_sign * cheapest[r]):
                    cheapest[r] = i
        if trace is not None:
            trace.append(f"  Round {rounds}: components before = {comps}")
            for r in sorted(cheapest):
                members = sorted(x for x in verts if ds.find(x) == r)
                trace.append(f"    component {{{','.join(members)}}} cheapest outgoing edge = {label(edges[cheapest[r]])}")
        for i in sorted(set(cheapest.values())):
            u, v, _ = edges[i]
            if ds.union(u, v):
                mst.append(edges[i])
                comps -= 1
        if trace is not None:
            trace.append(f"    merged -> components after = {comps}")
    return mst, {"rounds": rounds, "edge_scans": scans}


def cost(mst):
    return sum(w for _, _, w in mst)


def edge_set(mst):
    return frozenset(tuple(sorted((u, v))) + (w,) for u, v, w in mst)


def all_msts(verts, edges):
    """Brute force: every (V-1)-edge subset that is a spanning tree with minimum cost."""
    best, found = float("inf"), []
    for combo in itertools.combinations(edges, len(verts) - 1):
        ds = DisjointSet(verts)
        if all(ds.union(u, v) for u, v, _ in combo):
            c = cost(combo)
            if c < best:
                best, found = c, [combo]
            elif c == best:
                found.append(combo)
    return best, found


def random_graph(n, m, seed):
    rnd = random.Random(seed)
    verts = list(range(n))
    edges = {(i, rnd.randrange(i), rnd.randint(1, 10**6)) for i in range(1, n)}   # random spanning tree => connected
    pairs = {(min(u, v), max(u, v)) for u, v, _ in edges}
    while len(edges) < m:
        u, v = rnd.sample(verts, 2)
        if (min(u, v), max(u, v)) not in pairs:
            pairs.add((min(u, v), max(u, v)))
            edges.add((u, v, rnd.randint(1, 10**6)))
    return verts, sorted(edges)


if __name__ == "__main__":
    print("Graph edges:", ", ".join(label(e) for e in BASE))
    for name, fn in (("KRUSKAL", lambda t: kruskal(VERTS, BASE, 1, t)),
                     ("PRIM (start A)", lambda t: prim(VERTS, BASE, "A", 1, t)),
                     ("BORUVKA", lambda t: boruvka(VERTS, BASE, 1, t))):
        tr = []
        mst, stats = fn(tr)
        print(f"\n=== {name} on the base graph ===")
        print("\n".join(tr))
        print(f"  MST edges : {', '.join(label(e) for e in mst)}")
        print(f"  Total cost: {cost(mst)}    work counters: {stats}")

    print("\n=== STRESS: tie-creating modification (B-D 6->5, C-E 9->8, D-E 7->8) ===")
    MOD = modified(BASE)
    print("Modified edges:", ", ".join(label(e) for e in MOD))
    best, found = all_msts(VERTS, MOD)
    print(f"Brute force over C(13,7)=1716 subsets: minimum cost = {best}; number of distinct MSTs = {len(found)}")
    for k, m in enumerate(found, 1):
        print(f"  MST#{k}: {', '.join(label(e) for e in sorted(m, key=lambda e: (e[2], e[0])))}")
    valid = {edge_set(m) for m in found}
    runs = [("Kruskal  (ties in input order)", kruskal(VERTS, MOD, 1)[0]),
            ("Kruskal  (ties reversed)", kruskal(VERTS, MOD, -1)[0]),
            ("Prim     (start A, ties in input order)", prim(VERTS, MOD, "A", 1)[0]),
            ("Prim     (start H, ties reversed)", prim(VERTS, MOD, "H", -1)[0]),
            ("Boruvka  (ties by edge index)", boruvka(VERTS, MOD, 1)[0]),
            ("Boruvka  (ties by reversed index)", boruvka(VERTS, MOD, -1)[0])]
    print("\nAlgorithm variants:")
    for nm, mst in runs:
        print(f"  {nm:<42} cost={cost(mst)}  valid MST? {edge_set(mst) in valid}  edges: {', '.join(label(e) for e in sorted(mst, key=lambda e: (e[2], e[0])))}")
    print("  Distinct edge sets produced:", len({edge_set(m) for _, m in runs}), " -> all cost", {cost(m) for _, m in runs})

    print("\n=== Boruvka WITHOUT a consistent tie-break can create a cycle (why the rule matters) ===")
    tri = [("X", "Y", 1), ("Y", "Z", 1), ("Z", "X", 1)]
    picks = {"X": tri[0], "Y": tri[1], "Z": tri[2]}   # X picks X-Y, Y picks Y-Z, Z picks Z-X
    print("  Equal-weight triangle: X picks", label(picks["X"]), ", Y picks", label(picks["Y"]), ", Z picks", label(picks["Z"]),
          "-> 3 edges on 3 vertices = a cycle (an MST has only 2 edges).")

    print("\n=== DEPLOYMENT EVIDENCE: work counters on random graphs ===")
    print(f"{'environment':<28}{'V':>6}{'E':>8} | {'Kruskal examined/sorted':>24} | {'Prim pushes/pops':>18} | {'Boruvka rounds':>14}{'edge scans':>11}")
    for env, n, m in (("A sparse  (E ~ 2V)", 2000, 4000), ("B dense   (E ~ V^2/4)", 400, 40000), ("C large   (E ~ 3V)", 20000, 60000)):
        verts, edges = random_graph(n, m, 11)
        k_mst, ks = kruskal(verts, edges)
        p_mst, ps = prim(verts, edges, 0)
        b_mst, bs = boruvka(verts, edges)
        assert cost(k_mst) == cost(p_mst) == cost(b_mst)
        print(f"{env:<28}{n:>6}{m:>8} | {ks['edges_examined']:>11}/{ks['sort_size']:<12} | {ps['heap_pushes']:>8}/{ps['heap_pops']:<9} | {bs['rounds']:>14}{bs['edge_scans']:>11}")

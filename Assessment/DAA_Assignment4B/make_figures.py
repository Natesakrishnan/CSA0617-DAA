import sys, math
sys.path.insert(0, ".")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
import networkx as nx
from task1_wordwrap import word_wrap
from task3_routing import BASE_EDGES, VERTICES, with_edge_changed, dijkstra, bellman_ford
from task4_assembly import BASE, assembly_dp
from task5_mst import BASE as MBASE, modified, kruskal
from task6_tsp import COORDS, cost_matrix_from_coords, held_karp

OUT = "../img/"
NAVY, TEAL, RED, GREY, ORANGE = "#1F3A5F", "#1B998B", "#D1495B", "#B8C0CC", "#EDA43B"
plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans"})

# ---------- Fig 1 : word-wrap layout
text = ("Dynamic programming solves complex problems by combining optimal solutions of overlapping subproblems and stores results to avoid recomputation").split()
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), gridspec_kw={"width_ratios": [24, 32]})
for ax, W in zip(axes, (24, 32)):
    total, lines, *_ = word_wrap(text, W)
    ax.set_xlim(0, W); ax.set_ylim(-len(lines) - 0.3, 0.9); ax.axis("off")
    ax.set_title(f"Width {W}: total penalty = {total}", color=NAVY, fontweight="bold")
    for k, ln in enumerate(lines):
        y = -k - 0.5
        used = W - ln["unused"]
        ax.add_patch(Rectangle((0, y - 0.35), used, 0.7, color=TEAL, alpha=0.85))
        if ln["unused"]:
            ax.add_patch(Rectangle((used, y - 0.35), ln["unused"], 0.7, color=RED if ln["penalty"] else GREY, alpha=0.55))
        ax.text(0.2, y, " ".join(ln["words"]), va="center", color="white", fontsize=7.5, fontweight="bold")
        ax.text(W + 0.2, y, f"p={ln['penalty']}", va="center", fontsize=8, clip_on=False)
fig.text(0.5, 0.01, "teal = used characters, red = unused spaces that are penalised (unused^2), grey = unused spaces on the free final line", ha="center", fontsize=8.5)
plt.tight_layout(rect=(0, 0.05, 0.97, 1)); plt.savefig(OUT + "fig1_wordwrap.png", dpi=170); plt.close()

# ---------- Fig 2 : greedy vs DP work
ns = [(10, 100), (100, 1000), (500, 5000), (1000, 5000), (1000, 10000)]
greedy = [22, 539, 3824, 8629, 8627]
dpc = [1010, 100100, 2500500, 5001000, 10001000]
fig, ax = plt.subplots(figsize=(7.5, 4))
x = range(len(ns))
ax.bar([i - 0.2 for i in x], greedy, 0.4, color=TEAL, label="Greedy: key comparisons")
ax.bar([i + 0.2 for i in x], dpc, 0.4, color=NAVY, label="0/1 DP: cell evaluations (n x W)")
ax.set_yscale("log"); ax.set_xticks(list(x)); ax.set_xticklabels([f"n={n}\nW={w}" for n, w in ns])
ax.set_ylabel("operations (log scale)"); ax.legend(); ax.set_title("Computational work: greedy vs DP knapsack", color=NAVY, fontweight="bold")
plt.tight_layout(); plt.savefig(OUT + "fig2_knapsack_work.png", dpi=170); plt.close()

# ---------- Fig 3 : routing network
pos = {"A": (0, 2), "B": (2, 3.2), "C": (2, 0.8), "D": (4.2, 3.4), "E": (4.2, 0.6), "F": (6.4, 3.2), "G": (6.4, 1.2), "H": (8.5, 2.2)}
def draw_net(ax, edges, tree_edges, title, neg=()):
    G = nx.DiGraph(); G.add_weighted_edges_from(edges)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color="white", edgecolors=NAVY, node_size=650, linewidths=2)
    nx.draw_networkx_labels(G, pos, ax=ax, font_color=NAVY, font_weight="bold")
    for u, v, w in edges:
        col = RED if (u, v) in neg else (TEAL if (u, v) in tree_edges else GREY)
        lw = 3 if (u, v) in tree_edges or (u, v) in neg else 1.2
        rad = 0.18 if (v, u) in [(a, b) for a, b, _ in edges] else 0.0
        ax.add_patch(FancyArrowPatch(pos[u], pos[v], arrowstyle="-|>", mutation_scale=14, color=col, lw=lw, connectionstyle=f"arc3,rad={rad}", shrinkA=15, shrinkB=15, zorder=1))
        mx, my = (pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2
        off = 0.0
        if rad:
            dx, dy = pos[v][0] - pos[u][0], pos[v][1] - pos[u][1]; L = math.hypot(dx, dy)
            mx += -dy / L * 0.35 * (1 if rad > 0 else -1) * -1; my += dx / L * 0.35 * (1 if rad > 0 else -1) * -1
        ax.text(mx, my + 0.12, str(w), color=RED if (u, v) in neg else NAVY, fontsize=9, fontweight="bold", ha="center", bbox=dict(fc="white", ec="none", pad=0.6))
    ax.set_title(title, color=NAVY, fontweight="bold"); ax.axis("off"); ax.set_xlim(-0.7, 9.2); ax.set_ylim(-0.1, 4.2)
fig, axes = plt.subplots(1, 2, figsize=(13, 4.6))
d, p, _ = dijkstra(VERTICES, BASE_EDGES, "A")
draw_net(axes[0], BASE_EDGES, {(p[v], v) for v in VERTICES if p[v]}, "Stage A: Dijkstra shortest-path tree from A")
neg_edges = with_edge_changed(BASE_EDGES, "C", "B", -2)
bd, bp, _, _ = bellman_ford(VERTICES, neg_edges, "A")
draw_net(axes[1], neg_edges, {(bp[v], v) for v in VERTICES if bp[v]}, "Stage B: C->B = -2 (red). Bellman-Ford tree from A", neg={("C", "B")})
plt.tight_layout(); plt.savefig(OUT + "fig3_network.png", dpi=170); plt.close()

# ---------- Fig 4 : assembly lines
def draw_lines(ax, p, route, title):
    n = len(p["a"][0])
    ax.set_xlim(-1.3, n + 0.8); ax.set_ylim(-0.4, 2.6); ax.axis("off"); ax.set_title(title, color=NAVY, fontweight="bold")
    ys = {0: 1.7, 1: 0.5}
    chosen = {(l, i) for l, i in route}
    for l in (0, 1):
        for i in range(n):
            on = (l, i) in chosen
            ax.add_patch(Rectangle((i + 0.05, ys[l] - 0.32), 0.9, 0.64, fc=TEAL if on else "white", ec=NAVY, lw=2 if on else 1))
            ax.text(i + 0.5, ys[l], f"S{i+1}\n{p['a'][l][i]}", ha="center", va="center", color="white" if on else NAVY, fontsize=9, fontweight="bold")
        ax.text(-0.15, ys[l], f"Line {l+1}\nentry {p['e'][l]}", ha="right", va="center", fontsize=9, color=NAVY)
        ax.text(n + 0.1, ys[l], f"exit {p['x'][l]}", ha="left", va="center", fontsize=9, color=NAVY)
    for (l1, i1), (l2, i2) in zip(route, route[1:]):
        if l1 == l2:
            ax.annotate("", xy=(i2 + 0.05, ys[l2]), xytext=(i1 + 0.95, ys[l1]), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.5))
        else:
            ax.annotate("", xy=(i2 + 0.05, ys[l2] + (0.28 if l2 == 0 else -0.28)), xytext=(i1 + 0.95, ys[l1] + (-0.28 if l1 == 0 else 0.28)), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.5))
            ax.text(i1 + 1.0, 1.1, f"t={p['t'][l1][i1]}", color=RED, fontsize=9, ha="center", fontweight="bold")
import copy
fig, axes = plt.subplots(3, 1, figsize=(9.5, 8.4))
b, r, *_ = assembly_dp(BASE); draw_lines(axes[0], BASE, r, f"Base case: minimum production time = {b}")
p43 = copy.deepcopy(BASE); p43["t"][1][1] = 20; b, r, *_ = assembly_dp(p43); draw_lines(axes[1], p43, r, f"4.3: transfer t2 after station 2 = 20: minimum = {b}")
p44 = copy.deepcopy(BASE); p44["a"][1][3] = 15; b, r, *_ = assembly_dp(p44); draw_lines(axes[2], p44, r, f"4.4: Line 2 station 4 slowed to 15: minimum = {b}")
fig.text(0.5, 0.005, "teal = stations on the optimal route; orange arrow = stay on line; red arrow = transfer (cost t)", ha="center", fontsize=9)
plt.tight_layout(rect=(0, 0.02, 1, 1)); plt.savefig(OUT + "fig4_assembly.png", dpi=170); plt.close()

# ---------- Fig 4b : three-line extension
fig, ax = plt.subplots(figsize=(8, 3.6)); ax.axis("off"); ax.set_xlim(-0.6, 4.6); ax.set_ylim(-0.5, 3.1)
for l in range(3):
    for i in range(3):
        ax.add_patch(Rectangle((i * 1.6, 2.1 - l * 1.0 - 0.3), 1.0, 0.6, fc="white", ec=NAVY, lw=1.5))
        ax.text(i * 1.6 + 0.5, 2.1 - l * 1.0, f"f[{l+1}][{i+1}]", ha="center", va="center", color=NAVY, fontweight="bold")
    ax.text(-0.15, 2.1 - l * 1.0, f"Line {l+1}", ha="right", va="center", color=NAVY)
for i in range(2):
    for a in range(3):
        for b in range(3):
            c = ORANGE if a == b else RED
            ax.annotate("", xy=((i + 1) * 1.6, 2.1 - b * 1.0), xytext=(i * 1.6 + 1.0, 2.1 - a * 1.0), arrowprops=dict(arrowstyle="-|>", color=c, lw=1.2 if a == b else 0.9, alpha=0.8))
ax.set_title("Three lines: each f[j][i] now chooses among 3 predecessors (1 stay + 2 transfers)", color=NAVY, fontweight="bold", fontsize=10)
plt.tight_layout(); plt.savefig(OUT + "fig4b_three_lines.png", dpi=170); plt.close()

# ---------- Fig 5 : MST graphs
mpos = {"A": (0, 2), "B": (1.6, 3.2), "C": (1.6, 0.9), "D": (3.4, 2.6), "E": (3.8, 0.5), "F": (5.6, 2.2), "G": (7.2, 3.1), "H": (7.6, 1.0)}
def draw_mst(ax, edges, mst, title):
    G = nx.Graph(); G.add_weighted_edges_from(edges)
    sel = {tuple(sorted((u, v))) for u, v, _ in mst}
    nx.draw_networkx_nodes(G, mpos, ax=ax, node_color="white", edgecolors=NAVY, node_size=600, linewidths=2)
    nx.draw_networkx_labels(G, mpos, ax=ax, font_color=NAVY, font_weight="bold")
    for u, v, w in edges:
        on = tuple(sorted((u, v))) in sel
        ax.plot([mpos[u][0], mpos[v][0]], [mpos[u][1], mpos[v][1]], color=TEAL if on else GREY, lw=3.5 if on else 1.2, zorder=0, ls="-" if on else "--")
        ax.text((mpos[u][0] + mpos[v][0]) / 2, (mpos[u][1] + mpos[v][1]) / 2, str(w), fontsize=9, fontweight="bold", color=NAVY, ha="center", va="center", bbox=dict(fc="white", ec="none", pad=0.8))
    ax.set_title(title, color=NAVY, fontweight="bold", fontsize=10); ax.axis("off"); ax.set_xlim(-0.5, 8.2); ax.set_ylim(0, 3.8)
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
m0, _ = kruskal(list("ABCDEFGH"), MBASE); draw_mst(axes[0], MBASE, m0, "Base graph: unique MST, cost 36")
MOD = modified(MBASE)
m1, _ = kruskal(list("ABCDEFGH"), MOD, 1); draw_mst(axes[1], MOD, m1, "Tie graph: MST #1 (B-D, C-E), cost 37")
m2, _ = kruskal(list("ABCDEFGH"), MOD, -1); draw_mst(axes[2], MOD, m2, "Tie graph: MST #4 (C-D, D-E), cost 37")
plt.tight_layout(); plt.savefig(OUT + "fig5_mst.png", dpi=170); plt.close()

# ---------- Fig 6 : TSP route + growth + lattice
names = list(COORDS); C = cost_matrix_from_coords(COORDS); best, route, _ = held_karp(C)
fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
ax = axes[0]
for k, (nm, (x, y)) in enumerate(COORDS.items()):
    ax.scatter(x, y, s=420, c=ORANGE if nm == "Hub" else "white", edgecolors=NAVY, linewidths=2, zorder=3)
    ax.text(x, y, nm if nm != "Hub" else "H", ha="center", va="center", fontweight="bold", color=NAVY, zorder=4)
for k, (a, b) in enumerate(zip(route, route[1:]), 1):
    (x1, y1), (x2, y2) = COORDS[names[a]], COORDS[names[b]]
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.4, shrinkA=14, shrinkB=14))
    ax.text((x1 + x2) / 2 + 0.25, (y1 + y2) / 2 + 0.25, f"{k}:{C[a][b]}", fontsize=8.5, color=RED, fontweight="bold")
ax.set_title(f"Optimal route, cost {best}: " + "-".join(n[0] for n in [names[i] for i in route]), color=NAVY, fontweight="bold", fontsize=10)
ax.set_aspect("equal"); ax.axis("off")
ax = axes[1]
ns = list(range(4, 16)); states = [n * 2 ** (n - 1) for n in ns]; facts = [math.factorial(n) for n in ns]
ax.semilogy(ns, facts, "o-", color=RED, label="n! (exhaustive routes)"); ax.semilogy(ns, states, "s-", color=NAVY, label="n 2^(n-1) (DP states)")
ax.set_xlabel("number of delivery locations n"); ax.set_ylabel("count (log scale)"); ax.legend(); ax.grid(alpha=0.3, which="both")
ax.set_title("DP removes repetition but still grows exponentially", color=NAVY, fontweight="bold", fontsize=10)
plt.tight_layout(); plt.savefig(OUT + "fig6_tsp.png", dpi=170); plt.close()

# lattice of states for n=3
fig, ax = plt.subplots(figsize=(10, 4.6)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 5)
cols = {1: ["{1},1", "{2},2", "{3},3"], 2: ["{1,2},1", "{1,2},2", "{1,3},1", "{1,3},3", "{2,3},2", "{2,3},3"], 3: ["{1,2,3},1", "{1,2,3},2", "{1,2,3},3"]}
xs = {1: 1.0, 2: 5.0, 3: 9.0}; P = {}
for s, labels in cols.items():
    for k, lb in enumerate(labels):
        P[lb] = (xs[s], 4.5 - k * (4.0 / (len(labels) - 1 if len(labels) > 1 else 1)) if len(labels) > 3 else 4.0 - k * 1.5)
        ax.text(*P[lb], f"DP[{lb.split('}')[0]}}}][{lb.split(',')[-1]}]", ha="center", va="center", fontsize=9, color="white", fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.35", fc=NAVY if s < 3 else TEAL, ec="none"))
def link(a, b): ax.annotate("", xy=(P[b][0] - 0.95, P[b][1]), xytext=(P[a][0] + 0.95, P[a][1]), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.1))
for a, b in [("{1},1", "{1,2},2"), ("{2},2", "{1,2},1"), ("{1},1", "{1,3},3"), ("{3},3", "{1,3},1"), ("{2},2", "{2,3},3"), ("{3},3", "{2,3},2"),
             ("{1,2},1", "{1,2,3},3"), ("{1,2},2", "{1,2,3},3"), ("{1,3},1", "{1,2,3},2"), ("{1,3},3", "{1,2,3},2"), ("{2,3},2", "{1,2,3},1"), ("{2,3},3", "{1,2,3},1")]:
    link(a, b)
ax.text(1.0, 4.85, "size 1 (base)", ha="center", color=NAVY, fontweight="bold"); ax.text(5.0, 4.85, "size 2", ha="center", color=NAVY, fontweight="bold"); ax.text(9.0, 4.85, "size 3 (full) + return to hub", ha="center", color=NAVY, fontweight="bold")
ax.set_title("DP[S][j] for 3 delivery locations: every state is built from states with one fewer visited location", color=NAVY, fontweight="bold", fontsize=10)
plt.tight_layout(); plt.savefig(OUT + "fig6b_lattice.png", dpi=170); plt.close()
print("ok")

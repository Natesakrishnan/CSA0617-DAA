"""Q5 - draw the brute-force hull for the two designed configurations (boundary visual)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from q5_convex_hull import brute_force_hull, test_configurations


def main():
    cfgs = test_configurations()
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6))
    for ax, (name, pts) in zip(axes, cfgs.items()):
        hull, tests, pairs = brute_force_hull(pts)
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        ax.scatter(xs, ys, color="#555555", s=18, zorder=3)
        hx = [p[0] for p in hull] + [hull[0][0]]
        hy = [p[1] for p in hull] + [hull[0][1]]
        ax.plot(hx, hy, color="#d1495b", linewidth=1.8, zorder=2)
        ax.set_title(f"{name}\n{len(hull)} hull vertices, {tests} orientation tests", fontsize=9)
        ax.set_aspect("equal")
        ax.grid(alpha=0.3)
    fig.tight_layout()
    out = os.path.join(ROOT, "results", "figures", "q5_hull_boundaries.png")
    fig.savefig(out, dpi=160)
    print("wrote", out)


if __name__ == "__main__":
    main()

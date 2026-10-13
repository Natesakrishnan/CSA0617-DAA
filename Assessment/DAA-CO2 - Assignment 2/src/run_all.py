"""Run every experiment, save raw data as CSV, and draw the figures used in the report.

Usage (from the project root):  python3 src/run_all.py
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import q1_sorting
import q2_sequential_search
import q3_string_matching
import q4_closest_pair
import q5_convex_hull
import q6_exhaustive_knapsack
import q7_redesign

DATA = os.path.join(ROOT, "data")
FIG = os.path.join(ROOT, "results", "figures")
os.makedirs(DATA, exist_ok=True)
os.makedirs(FIG, exist_ok=True)


def save(name, rows):
    path = os.path.join(DATA, name)
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {path} ({len(rows)} rows)")
    return rows


def plot_q1(rows):
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for ds in ["nearly_sorted_95pct", "random", "reversed", "all_equal_edge"]:
        for alg in ["Selection", "Bubble", "Insertion"]:
            pts = sorted([r for r in rows if r["dataset"] == ds and r["algorithm"] == alg],
                         key=lambda r: r["n"])
            ax.plot([r["n"] for r in pts], [r["comparisons"] for r in pts],
                    marker="o", label=f"{alg} / {ds}", linestyle="-" if alg == "Insertion" else "--")
    ax.set_xlabel("n (number of orders)")
    ax.set_ylabel("comparisons")
    ax.set_title("Q1: comparisons by algorithm and data condition")
    ax.legend(fontsize=6, ncol=2)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "q1_comparisons.png"), dpi=160)
    plt.close(fig)


def plot_q2(rows):
    fig, ax = plt.subplots(figsize=(6.5, 4))
    for case in ["success_first", "success_middle", "success_last", "unsuccessful"]:
        pts = sorted([r for r in rows if r["case"] == case], key=lambda r: r["n"])
        ax.plot([r["n"] for r in pts], [r["comparisons"] for r in pts], marker="o", label=case)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("list size n")
    ax.set_ylabel("comparisons")
    ax.set_title("Q2: sequential search comparisons")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "q2_sequential.png"), dpi=160)
    plt.close(fig)


def plot_q3(rows):
    fig, ax = plt.subplots(figsize=(6.5, 4))
    for case in sorted({r["case"] for r in rows}):
        pts = sorted([r for r in rows if r["case"] == case], key=lambda r: r["n_text"])
        ax.plot([r["n_text"] for r in pts], [r["char_comparisons"] for r in pts], marker="o", label=case)
    ax.set_xlabel("text length n")
    ax.set_ylabel("character comparisons")
    ax.set_title("Q3: brute-force string matching")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "q3_string_matching.png"), dpi=160)
    plt.close(fig)


def plot_q4(rows):
    fig, ax = plt.subplots(figsize=(6.5, 4))
    ns = [r["n"] for r in rows]
    ax.plot(ns, [r["distance_calculations"] for r in rows], marker="o", label="observed distance calcs")
    ax.plot(ns, [r["theoretical_pairs_n(n-1)/2"] for r in rows], linestyle="--", label="n(n-1)/2")
    ax.set_xlabel("n drones")
    ax.set_ylabel("distance calculations")
    ax.set_title("Q4: brute-force closest pair growth")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "q4_closest_pair.png"), dpi=160)
    plt.close(fig)


def plot_q5(rows):
    fig, ax = plt.subplots(figsize=(6.5, 4))
    pts = [r for r in rows if r["config"] == "scaling_random"]
    ax.plot([r["n"] for r in pts], [r["orientation_tests"] for r in pts], marker="o", label="orientation tests")
    ax.plot([r["n"] for r in pts], [r["n"] ** 3 for r in pts], linestyle="--", label="n^3 reference")
    ax.set_xlabel("n points")
    ax.set_ylabel("cross-product tests")
    ax.set_title("Q5: brute-force hull work growth")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "q5_hull_growth.png"), dpi=160)
    plt.close(fig)


def plot_q6(rows):
    fig, ax = plt.subplots(figsize=(6.5, 4))
    pts = [r for r in rows if str(r["instance"]).startswith("random_")]
    ax.plot([r["n"] for r in pts], [r["candidates"] for r in pts], marker="o", label="candidate subsets")
    ax.plot([r["n"] for r in pts], [r["time_ms"] for r in pts], marker="s", label="time (ms)")
    ax.set_yscale("log")
    ax.set_xlabel("number of packages n")
    ax.set_ylabel("count / ms (log scale)")
    ax.set_title("Q6: exhaustive search growth")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "q6_knapsack_growth.png"), dpi=160)
    plt.close(fig)


def plot_q7(rows):
    fig, ax = plt.subplots(figsize=(6.5, 4))
    pts = [r for r in rows if r["input"] == "uniform_random"]
    ax.plot([r["n"] for r in pts], [r["original_distance_calcs"] for r in pts], marker="o", label="original (brute force)")
    ax.plot([r["n"] for r in pts], [r["redesign_distance_calcs"] for r in pts], marker="s", label="redesign (sort + prune)")
    ax.set_xlabel("n drones")
    ax.set_ylabel("distance calculations")
    ax.set_title("Q7: original vs redesigned closest pair")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "q7_redesign.png"), dpi=160)
    plt.close(fig)


def main():
    print("== Q1 sorting ==")
    q1 = save("q1_sorting.csv", q1_sorting.run())
    plot_q1(q1)

    print("== Q2 sequential search ==")
    q2 = save("q2_sequential_search.csv", q2_sequential_search.run())
    plot_q2([r for r in q2 if r["position"] is not None or r["case"] == "unsuccessful"])

    print("== Q3 string matching ==")
    q3 = save("q3_string_matching.csv", q3_string_matching.run())
    plot_q3(q3)

    print("== Q4 closest pair ==")
    q4 = save("q4_closest_pair.csv", q4_closest_pair.run())
    plot_q4(q4)

    print("== Q5 convex hull ==")
    q5 = save("q5_convex_hull.csv", q5_convex_hull.run())
    plot_q5(q5)

    print("== Q6 exhaustive search ==")
    q6 = save("q6_exhaustive_search.csv", q6_exhaustive_knapsack.run())
    plot_q6(q6)

    print("== Q7 redesign ==")
    q7 = save("q7_redesign.csv", q7_redesign.run())
    plot_q7(q7)

    print("done")


if __name__ == "__main__":
    main()

"""
Graph generator - DAA Assignment 1
Name: Natesa Krishnan V | Registration No.: 192511311 | Group: A

Reads results/results.csv (real measured data) and writes PNG graphs to results/graphs/.
Run:  python src/generate_graphs.py
"""
import math
import os
import statistics

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from dataset_generator import (RESULTS_DIR, KEY_FOUND, KEY_NOT_FOUND, banner)

GRAPH_DIR = os.path.join(RESULTS_DIR, "graphs")
ALGS = ["Linear Search", "Recursive Binary Search", "Hash Table Search"]
COLORS = {"Linear Search": "tab:red", "Recursive Binary Search": "tab:blue",
          "Hash Table Search": "tab:green"}
MARK = {"Linear Search": "o", "Recursive Binary Search": "s", "Hash Table Search": "^"}
SUB = "Natesa Krishnan V | Reg. No. 192511311 | Group A | seed 1311"
MS_TO_S = 1e-3


def series(df, alg, key, col):
    d = df[(df.algorithm == alg) & (df.search_key == key)].sort_values("input_size")
    return d["input_size"].tolist(), d[col].tolist()


def style(ax, xlabel, ylabel, title):
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize=10)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=7)


def runtime_graph(df):
    fig, axes = plt.subplots(1, 3, figsize=(17, 5))
    for alg in ALGS:
        for key, ls in ((KEY_FOUND, "-"), (KEY_NOT_FOUND, "--")):
            lab = f"{alg} ({'found' if key == KEY_FOUND else 'not found'})"
            x, y = series(df, alg, key, "search_time_ms")
            axes[0].plot(x, y, ls, color=COLORS[alg], marker=MARK[alg], label=lab)
    style(axes[0], "Input size n (records)", "Search time per query (ms)",
          "(a) Search time only (preprocessing excluded)")
    for alg in ALGS[1:]:
        x, y = series(df, alg, KEY_FOUND, "preprocessing_time_ms")
        axes[1].plot(x, y, color=COLORS[alg], marker=MARK[alg], label=f"{alg}: sort / build")
    style(axes[1], "Input size n (records)", "Preprocessing time (ms)",
          "(b) One-off preprocessing cost")
    for alg in ALGS:
        x, y = series(df, alg, KEY_NOT_FOUND, "total_time_ms")
        axes[2].plot(x, y, color=COLORS[alg], marker=MARK[alg], label=f"{alg}")
    style(axes[2], "Input size n (records)", "Preprocessing + ONE search (ms)",
          "(c) Total time for a single query (not-found key)")
    fig.suptitle("Input size vs execution time - measured\n" + SUB, fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(GRAPH_DIR, "runtime_comparison.png"), dpi=150)
    plt.close(fig)


def comparisons_graph(df):
    fig, ax = plt.subplots(figsize=(8, 5.5))
    for alg in ALGS:
        for key, ls in ((KEY_FOUND, "-"), (KEY_NOT_FOUND, "--")):
            x, y = series(df, alg, key, "comparisons_operations")
            unit = "operations (1 hash + comparisons)" if alg == ALGS[2] else "comparisons"
            ax.plot(x, y, ls, color=COLORS[alg], marker=MARK[alg],
                    label=f"{alg} - {unit} ({'found' if key == KEY_FOUND else 'not found'})")
    style(ax, "Input size n (records)", "Key comparisons / key operations per query",
          "Input size vs comparisons / key operations - measured\n" + SUB)
    fig.tight_layout()
    fig.savefig(os.path.join(GRAPH_DIR, "comparisons_comparison.png"), dpi=150)
    plt.close(fig)


def theory_graph(df):
    hs = pd.read_csv(os.path.join(RESULTS_DIR, "hash_table_results.csv"))
    alpha = {int(r.input_size): float(r.load_factor) for r in hs.itertuples()}
    fig, axes = plt.subplots(2, 3, figsize=(17, 9))
    key = KEY_NOT_FOUND
    sizes = sorted(df.input_size.unique())
    theory_cmp = {
        "Linear Search": ([n for n in sizes], "theory: n"),
        "Recursive Binary Search": ([math.floor(math.log2(n)) + 1 for n in sizes], "theory: floor(log2 n)+1"),
        "Hash Table Search": ([1 + alpha[n] for n in sizes], "theory: 1 + alpha (hash + expected chain scan)"),
    }
    for j, alg in enumerate(ALGS):
        x, y = series(df, alg, key, "comparisons_operations")
        ax = axes[0][j]
        ax.plot(x, y, color=COLORS[alg], marker=MARK[alg], label=f"measured ({alg}, not found)")
        ax.plot(sizes, theory_cmp[alg][0], "k--", marker="x", label=theory_cmp[alg][1])
        style(ax, "n", "comparisons / operations", f"{alg}: operation count")
        # time vs scaled theory
        xt, yt = series(df, alg, key, "search_time_ms")
        if alg == "Linear Search":
            f = lambda n: n
            lab = "scaled theory c*n"
        elif alg == "Recursive Binary Search":
            f = lambda n: math.log2(n)
            lab = "scaled theory c*log2(n)"
        else:
            f = lambda n: 1.0
            lab = "scaled theory c*1"
        c = statistics.median(t / f(n) for n, t in zip(xt, yt))
        ax2 = axes[1][j]
        ax2.plot(xt, yt, color=COLORS[alg], marker=MARK[alg], label="measured search time (ms)")
        ax2.plot(xt, [c * f(n) for n in xt], "k--", marker="x", label=lab + f" (c={c:.3g} ms)")
        style(ax2, "n", "search time (ms)", f"{alg}: running time")
    fig.suptitle("Theory vs experiment (not-found key = worst case for searching)\n" + SUB, fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(GRAPH_DIR, "theory_vs_experiment.png"), dpi=150)
    plt.close(fig)


def cumulative_graph(df):
    n = 1_000_000
    fig, ax = plt.subplots(figsize=(8, 5.5))
    qs = [10 ** (k / 4) for k in range(0, 4 * 6 + 1)]
    for alg in ALGS:
        d = df[(df.algorithm == alg) & (df.input_size == n) & (df.search_key == KEY_NOT_FOUND)].iloc[0]
        pre, st = float(d.preprocessing_time_seconds), float(d.search_time_seconds)
        ax.plot(qs, [pre + q * st for q in qs], color=COLORS[alg], label=alg)
    ax.axhline(3600, color="gray", linestyle=":", label="1 hour of CPU time")
    style(ax, "Number of search queries q", "Cumulative time: preprocessing + q searches (s)",
          f"Cumulative cost for n = 1,000,000 (not-found key)\n" + SUB)
    fig.tight_layout()
    fig.savefig(os.path.join(GRAPH_DIR, "cumulative_cost_1M.png"), dpi=150)
    plt.close(fig)


def main():
    banner("Graph Generator")
    os.makedirs(GRAPH_DIR, exist_ok=True)
    df = pd.read_csv(os.path.join(RESULTS_DIR, "results.csv"))
    runtime_graph(df)
    comparisons_graph(df)
    theory_graph(df)
    cumulative_graph(df)
    for f in sorted(os.listdir(GRAPH_DIR)):
        print("Saved:", os.path.join(GRAPH_DIR, f))


if __name__ == "__main__":
    main()

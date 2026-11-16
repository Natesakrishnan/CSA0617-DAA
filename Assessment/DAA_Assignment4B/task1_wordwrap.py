"""Task 1 - Word wrap as a Dynamic Programming problem.

Penalty model (assumption stated in the report):
    non-final line : penalty = (unused spaces) ** 2
    final line     : penalty = 0
DP definition (suffix form):
    dp[i] = minimum total penalty for arranging words[i:], i.e. words i..n-1
    dp[n] = 0
    dp[i] = min over j (i <= j < n, line i..j fits) of  line_penalty(i, j) + dp[j+1]
"""
import sys

INF = float("inf")


def validate(words, width):
    """Reject inputs for which no legal arrangement exists."""
    if width <= 0:
        raise ValueError("line width must be positive")
    for w in words:
        if len(w) > width:
            raise ValueError(f"word '{w}' (length {len(w)}) is longer than width {width}")


def line_length(words, i, j):
    """Characters needed to print words i..j separated by single spaces."""
    return sum(len(w) for w in words[i:j + 1]) + (j - i)


def line_penalty(words, i, j, width):
    """Penalty of putting words i..j on one line (INF if it does not fit)."""
    unused = width - line_length(words, i, j)
    if unused < 0:
        return INF
    if j == len(words) - 1:          # final line carries no penalty
        return 0
    return unused ** 2


def word_wrap(words, width):
    """Return (total_penalty, lines, dp, next_break, candidates).  Pure algorithm, no printing."""
    validate(words, width)
    n = len(words)
    dp = [INF] * (n + 1)
    next_break = [None] * (n + 1)    # next_break[i] = index of the LAST word on the line starting at i
    candidates = [[] for _ in range(n + 1)]
    dp[n] = 0
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if line_length(words, i, j) > width:
                break
            pen = line_penalty(words, i, j, width)
            total = pen + dp[j + 1]
            candidates[i].append((j, pen, total))
            if total < dp[i]:
                dp[i] = total
                next_break[i] = j
    lines, i = [], 0
    while i < n:                      # reconstruct the arrangement
        j = next_break[i]
        unused = width - line_length(words, i, j)
        lines.append({"words": words[i:j + 1], "unused": unused,
                      "penalty": line_penalty(words, i, j, width)})
        i = j + 1
    return dp[0], lines, dp, next_break, candidates


def print_layout(total, lines, width):
    print(f"Line width = {width}   Minimum total penalty = {total}")
    ruler = "".join(str(k % 10) for k in range(1, width + 1))
    if width <= 60:
        print("      |" + ruler + "|")
    for k, ln in enumerate(lines, 1):
        text = " ".join(ln["words"])
        text = text if width <= 60 else text[:40] + " ... " + text[-20:]
        print(f"L{k:<3}  |{text:<{min(width,60)}}|  words={len(ln['words'])}  unused={ln['unused']:>2}  penalty={ln['penalty']}")


def print_dp_trace(words, width, dp, next_break, candidates):
    print(f"DP states for width {width}:  dp[i] = best penalty for words[i:]  (dp[{len(words)}] = 0)")
    print(f"{'i':>2} {'word':<14}{'candidate lines (last word j: line penalty + dp[j+1] = total)':<70}{'dp[i]':>6} {'best j':>7}")
    for i in range(len(words) - 1, -1, -1):
        cand = "; ".join(f"j={j}:{p}+{dp[j+1]}={t}" for j, p, t in candidates[i])
        print(f"{i:>2} {words[i]:<14}{cand:<70}{dp[i]:>6} {next_break[i]:>7}")
    print(f"{len(words):>2} {'<end>':<14}{'':<70}{0:>6} {'-':>7}")


if __name__ == "__main__":
    text = ("Dynamic programming solves complex problems by combining optimal "
            "solutions of overlapping subproblems and stores results to avoid recomputation")
    words = text.split()
    base_width = 24
    print("=== 1.1 / 1.2  BASE CASE ===")
    print("Words:", len(words), " lengths:", [len(w) for w in words])
    total, lines, dp, nb, cand = word_wrap(words, base_width)
    print_layout(total, lines, base_width)
    print()
    print_dp_trace(words, base_width, dp, nb, cand)
    print("\n=== 1.3  REQUIREMENT CHANGE (widths 16, 32, 40) ===")
    for w in (16, 32, 40):
        t, ls, *_ = word_wrap(words, w)
        print_layout(t, ls, w)
        print()
    print("=== 1.4  BOUNDARY TESTS ===")
    tests = {
        "B1 exact fit: 'aaaa bbbb cc' width 12 (line is exactly full, zero slack)": (["aaaa", "bbbb", "cc"], 12),
        "B2 word length == width: ['abcdef','gh','ijklmn'] width 6": (["abcdef", "gh", "ijklmn"], 6),
        "B3 single word: ['hello'] width 5": (["hello"], 5),
        "B4 whole text fits on one line: width 150": (words, 150),
    }
    for name, (ws, w) in tests.items():
        print(name)
        t, ls, *_ = word_wrap(ws, w)
        print_layout(t, ls, w)
        print()
    print("B5 word longer than width -> must raise an error:")
    try:
        word_wrap(["supercalifragilistic", "ok"], 10)
    except ValueError as e:
        print("  ValueError:", e)

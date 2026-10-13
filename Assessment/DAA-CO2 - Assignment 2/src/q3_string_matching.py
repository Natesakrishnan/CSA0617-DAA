"""Q3 - Brute-force string matching with character-comparison counting.

Algorithm: for each alignment i, compare pattern characters left to right until the
first mismatch (or a full match). Comparisons = number of single character tests.
"""
import random


def brute_force_match(text, pattern):
    """Return (first match index or -1, character comparisons)."""
    n, m = len(text), len(pattern)
    comps = 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comps += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            return i, comps
    return -1, comps


def make_cases(n, seed=1311):
    rng = random.Random(seed + n)
    cases = {}

    # Case 1 - low work: 26-letter random text, pattern uses letters that rarely occur
    # at the start of an alignment, so most alignments fail at the first character.
    letters = "abcdefghijklmnopqrstuvwxyz"
    text_low = "".join(rng.choice(letters[:20]) for _ in range(n))
    cases["low_work_random26"] = (text_low, "zxqvjk")

    # Case 2 - engineered worst case: text is all 'a', pattern is a^(m-1) b.
    # Each alignment matches m-1 characters before failing on the last one.
    m = 100
    cases["worst_case_a_runs"] = ("a" * n, "a" * (m - 1) + "b")

    # Case 3 - additional condition: binary random text with a pattern copied from
    # the middle of the text (a successful match occurs). Tests average behaviour
    # on a small alphabet where partial matches are common.
    text_bin = "".join(rng.choice("ab") for _ in range(n))
    start = n // 2
    cases["binary_random_match_mid"] = (text_bin, text_bin[start:start + 12])
    return cases


def run(sizes=(1000, 2000, 4000, 8000)):
    rows = []
    for n in sizes:
        for name, (text, pattern) in make_cases(n).items():
            pos, comps = brute_force_match(text, pattern)
            n_align = len(text) - len(pattern) + 1
            rows.append({
                "case": name,
                "n_text": len(text),
                "m_pattern": len(pattern),
                "alignments": n_align,
                "match_index": pos,
                "char_comparisons": comps,
                "comparisons_per_text_char": round(comps / len(text), 3),
                "worst_bound_(n-m+1)*m": n_align * len(pattern),
            })
    return rows


if __name__ == "__main__":
    for r in run(sizes=(1000,)):
        print(r)

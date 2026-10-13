"""Q2 - Sequential search on a temporary list of tool-issue records.

Each record is a tool ID plus technician, time and bay. The search key is the Tool ID.
Comparisons are counted as the number of key equality tests performed.
"""
import random
import time


def build_records(n, seed=1311):
    """Build n records with unique tool IDs in a shuffled (issue-order) list."""
    rng = random.Random(seed + n)
    ids = [f"T-{i:06d}" for i in range(n)]
    rng.shuffle(ids)
    return [
        {"tool_id": tid, "technician_id": f"TECH-{rng.randint(1, 500):04d}",
         "issue_time": f"{rng.randint(0, 23):02d}:{rng.randint(0, 59):02d}",
         "work_bay": f"BAY-{rng.randint(1, 40):02d}"}
        for tid in ids
    ]


def sequential_search(records, key):
    """Return (position or -1, comparisons)."""
    comps = 0
    for idx, rec in enumerate(records):
        comps += 1
        if rec["tool_id"] == key:
            return idx, comps
    return -1, comps


def run(sizes=(100, 1000, 10000, 100000), random_lookups=200, seed=1311):
    rows = []
    rng = random.Random(seed)
    for n in sizes:
        records = build_records(n, seed)
        ids_in_list = [r["tool_id"] for r in records]

        # Designed successful-search positions: first, middle, last, and absent key.
        cases = {
            "success_first": records[0]["tool_id"],
            "success_middle": records[n // 2]["tool_id"],
            "success_last": records[-1]["tool_id"],
            "unsuccessful": f"T-{n + 999:06d}",
        }
        for case, key in cases.items():
            pos, comps = sequential_search(records, key)
            rows.append({"n": n, "case": case, "position": pos, "comparisons": comps,
                         "time_us": None})

        # Average over random successful lookups (sampled for large n).
        sample = [rng.choice(ids_in_list) for _ in range(random_lookups)]
        total_comps = 0
        t0 = time.perf_counter()
        for key in sample:
            _, c = sequential_search(records, key)
            total_comps += c
        elapsed = time.perf_counter() - t0
        rows.append({"n": n, "case": "random_successful_avg", "position": None,
                     "comparisons": round(total_comps / random_lookups, 2),
                     "time_us": round(1e6 * elapsed / random_lookups, 3)})

        # Average over absent keys (always n comparisons).
        absent_total = 0
        t0 = time.perf_counter()
        for k in range(random_lookups):
            _, c = sequential_search(records, f"T-{n + 1000 + k:06d}")
            absent_total += c
        elapsed = time.perf_counter() - t0
        rows.append({"n": n, "case": "unsuccessful_avg", "position": None,
                     "comparisons": round(absent_total / random_lookups, 2),
                     "time_us": round(1e6 * elapsed / random_lookups, 3)})
    return rows


if __name__ == "__main__":
    for r in run(sizes=(1000,)):
        print(r)

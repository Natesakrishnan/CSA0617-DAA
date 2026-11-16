"""
Task 2 - Job Sequencing with Deadlines (Greedy)
Greedy-choice rule: process jobs in descending order of profit; place each
job in the latest free slot <= its deadline.
"""


def job_sequencing(jobs):
    """
    jobs: list of dicts {"id": str, "deadline": int, "profit": float}
    returns: (schedule, total_profit)
             schedule is a list indexed 1..max_deadline (index 0 unused)
    """
    jobs_sorted = sorted(jobs, key=lambda j: j["profit"], reverse=True)

    max_deadline = max(j["deadline"] for j in jobs)
    schedule = [None] * (max_deadline + 1)  # 1-indexed slots
    total_profit = 0

    for job in jobs_sorted:
        slot = min(job["deadline"], max_deadline)
        while slot >= 1:
            if schedule[slot] is None:
                schedule[slot] = job["id"]
                total_profit += job["profit"]
                break
            slot -= 1
        # if slot reaches 0, the job is rejected

    return schedule[1:], total_profit


if __name__ == "__main__":
    jobs = [
        {"id": "A", "deadline": 2, "profit": 80},
        {"id": "B", "deadline": 1, "profit": 35},
        {"id": "C", "deadline": 2, "profit": 60},
        {"id": "D", "deadline": 3, "profit": 40},
        {"id": "E", "deadline": 1, "profit": 25},
    ]

    schedule, total_profit = job_sequencing(jobs)
    print("Job Sequencing with Deadlines")
    for slot, job_id in enumerate(schedule, start=1):
        print(f"  Slot {slot}: {job_id if job_id else '-'}")
    print(f"Total profit = {total_profit}")

    # --- Task 2.5: challenge case (A's deadline changed 2 -> 1) ---
    jobs_modified = [dict(j) for j in jobs]
    jobs_modified[0]["deadline"] = 1  # job A
    schedule2, total_profit2 = job_sequencing(jobs_modified)
    print("\nModified input (A's deadline 2 -> 1)")
    for slot, job_id in enumerate(schedule2, start=1):
        print(f"  Slot {slot}: {job_id if job_id else '-'}")
    print(f"Total profit = {total_profit2}")

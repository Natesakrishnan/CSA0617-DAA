"""
Task 6 - Energy-Aware Job Scheduling (Design Challenge)
Weighted Interval Scheduling, solved with Dynamic Programming.
"""


def energy_aware_scheduling(jobs):
    """
    jobs: list of dicts {"id": str, "start": int, "finish": int, "value": float}
    returns: (max_value, selected_jobs)
    """
    jobs_sorted = sorted(jobs, key=lambda j: j["finish"])
    n = len(jobs_sorted)

    # p[i] = index (1-based) of the latest job compatible with job i (0 if none)
    p = [0] * (n + 1)
    for i in range(1, n + 1):
        job_i = jobs_sorted[i - 1]
        for j in range(i - 1, 0, -1):
            if jobs_sorted[j - 1]["finish"] <= job_i["start"]:
                p[i] = j
                break

    dp = [0] * (n + 1)
    take = [False] * (n + 1)

    for i in range(1, n + 1):
        value_i = jobs_sorted[i - 1]["value"]
        include_value = value_i + dp[p[i]]
        exclude_value = dp[i - 1]
        if include_value > exclude_value:
            dp[i] = include_value
            take[i] = True
        else:
            dp[i] = exclude_value
            take[i] = False

    max_value = dp[n]

    selected = []
    i = n
    while i > 0:
        if take[i]:
            selected.append(jobs_sorted[i - 1]["id"])
            i = p[i]
        else:
            i -= 1

    selected.reverse()
    return max_value, selected


if __name__ == "__main__":
    jobs = [
        {"id": "J1", "start": 1, "finish": 3, "value": 20},
        {"id": "J2", "start": 2, "finish": 5, "value": 50},
        {"id": "J3", "start": 4, "finish": 6, "value": 30},
        {"id": "J4", "start": 6, "finish": 8, "value": 40},
        {"id": "J5", "start": 5, "finish": 9, "value": 60},
        {"id": "J6", "start": 8, "finish": 10, "value": 30},
        {"id": "J7", "start": 9, "finish": 11, "value": 50},
        {"id": "J8", "start": 11, "finish": 13, "value": 40},
    ]

    max_value, selected = energy_aware_scheduling(jobs)
    print("Energy-Aware Job Scheduling")
    print(f"Max energy-saving value = {max_value}")
    print(f"Selected jobs = {selected}")

    # Stage 6: adversarial test - one high-value job overlapping five
    # compatible lower-value jobs whose sum exceeds it.
    adversarial_jobs = [
        {"id": "X1", "start": 0, "finish": 10, "value": 100},
        {"id": "X2", "start": 0, "finish": 2, "value": 30},
        {"id": "X3", "start": 2, "finish": 4, "value": 30},
        {"id": "X4", "start": 4, "finish": 6, "value": 30},
        {"id": "X5", "start": 6, "finish": 8, "value": 30},
        {"id": "X6", "start": 8, "finish": 10, "value": 30},
    ]
    max_value2, selected2 = energy_aware_scheduling(adversarial_jobs)
    print("\nAdversarial test (Stage 6)")
    print(f"Max energy-saving value = {max_value2}")
    print(f"Selected jobs = {selected2}")
    print("('Highest value first' greedy would have picked only X1 -> value 100)")

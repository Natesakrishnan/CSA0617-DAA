import random

def median_of_medians_select(values, k):
    """Return zero-based k-th smallest element with deterministic pivot selection."""
    if not 0 <= k < len(values):
        raise ValueError("k is outside the list")
    if len(values) <= 5:
        return sorted(values)[k]
    groups = [values[i:i+5] for i in range(0, len(values), 5)]
    medians = [sorted(group)[len(group)//2] for group in groups]
    pivot = median_of_medians_select(medians, len(medians)//2)
    lows = [x for x in values if x < pivot]
    highs = [x for x in values if x > pivot]
    equals = [x for x in values if x == pivot]
    if k < len(lows):
        return median_of_medians_select(lows, k)
    if k < len(lows) + len(equals):
        return pivot
    return median_of_medians_select(highs, k-len(lows)-len(equals))

def subset_sums(values):
    sums = [0]
    for x in values:
        sums += [s + x for s in sums]
    return sums

def meet_in_middle_subset_sum(values, target):
    mid = len(values)//2
    left = subset_sums(values[:mid])
    right = sorted(subset_sums(values[mid:]))
    i, j = 0, len(right)-1
    while i < len(left) and j >= 0:
        total = left[i] + right[j]
        if total == target:
            return True
        if total < target: i += 1
        else: j -= 1
    return False

if __name__ == "__main__":
    data = [23, 4, 15, 8, 42, 16, 9, 31, 7, 19, 2]
    k = 5
    print("Q6 MEDIAN OF MEDIANS")
    print(f"{k}-th smallest (1-based):", median_of_medians_select(data, k-1))
    nums, target = [3, 34, 4, 12, 5, 2], 9
    print("\nQ6 MEET-IN-THE-MIDDLE")
    print("Values:", nums, "Target:", target)
    print("Subset exists:", meet_in_middle_subset_sum(nums, target))
    print("Time: O(2^(n/2) log(2^(n/2))) for this sorting-based combination")
    print("Space: O(2^(n/2))")

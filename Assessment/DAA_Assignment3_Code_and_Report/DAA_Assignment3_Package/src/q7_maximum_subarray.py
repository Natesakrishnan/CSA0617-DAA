def max_subarray_dc(a):
    """Maximum contiguous subarray sum using divide and conquer."""
    def solve(lo, hi):
        if lo == hi:
            return a[lo]
        mid = (lo + hi)//2
        left_best = solve(lo, mid)
        right_best = solve(mid+1, hi)
        total, best_left = 0, float("-inf")
        for i in range(mid, lo-1, -1):
            total += a[i]
            best_left = max(best_left, total)
        total, best_right = 0, float("-inf")
        for i in range(mid+1, hi+1):
            total += a[i]
            best_right = max(best_right, total)
        return max(left_best, right_best, best_left + best_right)
    if not a:
        raise ValueError("Array must not be empty")
    return solve(0, len(a)-1)

def max_subarray_brute(a):
    best = float("-inf")
    for i in range(len(a)):
        total = 0
        for j in range(i, len(a)):
            total += a[j]
            best = max(best, total)
    return best

if __name__ == "__main__":
    data = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    dc = max_subarray_dc(data)
    baseline = max_subarray_brute(data)
    print("Q7 DESIGN FROM FIRST PRINCIPLES: MAXIMUM SUBARRAY")
    print("Input:", data)
    print("Divide-and-conquer result:", dc)
    print("Brute-force result:", baseline)
    print("Correct:", dc == baseline)
    print("Recurrence: T(n) = 2T(n/2) + O(n)")
    print("Time: O(n log n); auxiliary recursion space: O(log n)")

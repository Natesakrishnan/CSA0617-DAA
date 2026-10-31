def max_min_dc(a):
    """Return (minimum, maximum, comparison_count) using divide and conquer."""
    comparisons = 0
    def solve(lo, hi):
        nonlocal comparisons
        if lo == hi:
            return a[lo], a[lo]
        if hi == lo + 1:
            comparisons += 1
            if a[lo] < a[hi]:
                return a[lo], a[hi]
            return a[hi], a[lo]
        mid = (lo + hi) // 2
        mn1, mx1 = solve(lo, mid)
        mn2, mx2 = solve(mid + 1, hi)
        comparisons += 2
        return min(mn1, mn2), max(mx1, mx2)
    if not a:
        raise ValueError("Input must not be empty")
    mn, mx = solve(0, len(a) - 1)
    return mn, mx, comparisons

def binary_search(a, target):
    lo, hi, comparisons = 0, len(a) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        comparisons += 1
        if a[mid] == target:
            return mid, comparisons
        comparisons += 1
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, comparisons

if __name__ == "__main__":
    data = [18, 4, 27, 9, 2, 31, 12, 6]
    mn, mx, count = max_min_dc(data)
    print("Q1 MAX-MIN")
    print("Data:", data)
    print(f"Minimum={mn}, Maximum={mx}, Comparisons={count}")
    ordered = sorted(data)
    print("\nQ1 BINARY SEARCH")
    print("Sorted data:", ordered)
    for key in (12, 20):
        index, c = binary_search(ordered, key)
        print(f"Target={key}, Index={index}, Comparisons={c}")

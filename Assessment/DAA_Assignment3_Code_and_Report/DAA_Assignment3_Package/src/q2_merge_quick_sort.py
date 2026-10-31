def merge_sort(a):
    if len(a) <= 1:
        return a[:]
    mid = len(a) // 2
    left, right = merge_sort(a[:mid]), merge_sort(a[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]

def quick_sort(a):
    """Last-element pivot; returns sorted list and maximum recursion depth."""
    max_depth = 0
    def sort(items, depth):
        nonlocal max_depth
        max_depth = max(max_depth, depth)
        if len(items) <= 1:
            return items[:]
        pivot = items[-1]
        left = [x for x in items[:-1] if x <= pivot]
        right = [x for x in items[:-1] if x > pivot]
        return sort(left, depth + 1) + [pivot] + sort(right, depth + 1)
    result = sort(a, 1)
    return result, max_depth

if __name__ == "__main__":
    cases = {
        "mixed": [38, 12, 27, 5, 19, 44, 2, 31],
        "ascending": list(range(1, 11)),
    }
    for name, data in cases.items():
        merged = merge_sort(data)
        quicked, depth = quick_sort(data)
        print(f"{name}:")
        print("Merge Sort:", merged)
        print("Quick Sort:", quicked, "| maximum recursion depth:", depth)
        print("Outputs match:", merged == quicked)

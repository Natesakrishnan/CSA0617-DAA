def find_paths(m, n, N, i, j):
    if i < 0 or i >= m or j < 0 or j >= n:
        return 1

    if N == 0:
        return 0

    return (
        find_paths(m, n, N - 1, i - 1, j) +
        find_paths(m, n, N - 1, i + 1, j) +
        find_paths(m, n, N - 1, i, j - 1) +
        find_paths(m, n, N - 1, i, j + 1)
    )


print(find_paths(2, 2, 2, 0, 0))
print(find_paths(1, 3, 3, 0, 1))

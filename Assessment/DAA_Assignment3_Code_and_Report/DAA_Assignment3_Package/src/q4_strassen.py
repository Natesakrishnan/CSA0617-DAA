def add(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

def sub(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

def conventional(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            for j in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def strassen(A, B):
    n = len(A)
    if n <= 2:
        return conventional(A, B)
    m = n // 2
    A11 = [row[:m] for row in A[:m]]
    A12 = [row[m:] for row in A[:m]]
    A21 = [row[:m] for row in A[m:]]
    A22 = [row[m:] for row in A[m:]]
    B11 = [row[:m] for row in B[:m]]
    B12 = [row[m:] for row in B[:m]]
    B21 = [row[:m] for row in B[m:]]
    B22 = [row[m:] for row in B[m:]]
    M1 = strassen(add(A11, A22), add(B11, B22))
    M2 = strassen(add(A21, A22), B11)
    M3 = strassen(A11, sub(B12, B22))
    M4 = strassen(A22, sub(B21, B11))
    M5 = strassen(add(A11, A12), B22)
    M6 = strassen(sub(A21, A11), add(B11, B12))
    M7 = strassen(sub(A12, A22), add(B21, B22))
    C11 = add(sub(add(M1, M4), M5), M7)
    C12 = add(M3, M5)
    C21 = add(M2, M4)
    C22 = add(sub(add(M1, M3), M2), M6)
    top = [C11[i] + C12[i] for i in range(m)]
    bottom = [C21[i] + C22[i] for i in range(m)]
    return top + bottom

def pad_matrix(A, size):
    n = len(A)
    return [row + [0] * (size - n) for row in A] + [[0] * size for _ in range(size - n)]

def strassen_any(A, B):
    n = len(A)
    size = 1
    while size < n:
        size *= 2
    Ap, Bp = pad_matrix(A, size), pad_matrix(B, size)
    Cp = strassen(Ap, Bp)
    return [row[:n] for row in Cp[:n]]

if __name__ == "__main__":
    A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    B = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
    standard, fast = conventional(A, B), strassen_any(A, B)
    print("Q4 STRASSEN MATRIX MULTIPLICATION")
    print("Conventional:", standard)
    print("Strassen:", fast)
    print("Correct:", standard == fast)
    print("Recurrence: T(n) = 7T(n/2) + O(n^2)")
    print("Complexity: O(n^(log2 7)) approximately O(n^2.807)")

def standard_multiply(x, y):
    return x * y

def karatsuba(x, y):
    if x < 10 or y < 10:
        return x * y
    n = max(len(str(abs(x))), len(str(abs(y))))
    half = n // 2
    power = 10 ** half
    a, b = divmod(x, power)
    c, d = divmod(y, power)
    z0 = karatsuba(b, d)
    z2 = karatsuba(a, c)
    z1 = karatsuba(a + b, c + d) - z2 - z0
    return z2 * (power ** 2) + z1 * power + z0

if __name__ == "__main__":
    x, y = 123456789012345, 987654321098765
    normal = standard_multiply(x, y)
    fast = karatsuba(x, y)
    print("Q3 KARATSUBA MULTIPLICATION")
    print("Standard result:", normal)
    print("Karatsuba result:", fast)
    print("Correct:", normal == fast)
    print("Recurrence: T(n) = 3T(n/2) + O(n)")
    print("Complexity: O(n^(log2 3)) approximately O(n^1.585)")

import math

def distance(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])

def brute_force(points):
    best = float("inf")
    pair = None
    checks = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            checks += 1
            d = distance(points[i], points[j])
            if d < best:
                best, pair = d, (points[i], points[j])
    return best, pair, checks

def closest_pair(points):
    """Divide-and-conquer closest pair; returns distance, pair, distance checks."""
    if len(points) < 2:
        raise ValueError("At least two points are required")
    checks = 0
    def solve(px):
        nonlocal checks
        n = len(px)
        if n <= 3:
            best, pair = float("inf"), None
            for i in range(n):
                for j in range(i + 1, n):
                    checks += 1
                    d = distance(px[i], px[j])
                    if d < best: best, pair = d, (px[i], px[j])
            return best, pair
        mid = n // 2
        midx = px[mid][0]
        dl, pl = solve(px[:mid])
        dr, pr = solve(px[mid:])
        best, pair = (dl, pl) if dl <= dr else (dr, pr)
        strip = [p for p in px if abs(p[0] - midx) < best]
        strip.sort(key=lambda p: p[1])
        for i in range(len(strip)):
            j = i + 1
            while j < len(strip) and strip[j][1] - strip[i][1] < best:
                checks += 1
                d = distance(strip[i], strip[j])
                if d < best: best, pair = d, (strip[i], strip[j])
                j += 1
        return best, pair
    ordered = sorted(points)
    d, pair = solve(ordered)
    return d, pair, checks

if __name__ == "__main__":
    pts = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4), (8, 9)]
    b = brute_force(pts)
    dc = closest_pair(pts)
    print("Q5 CLOSEST PAIR")
    print("Brute force:", b)
    print("Divide and conquer:", dc)
    print("Same minimum distance:", abs(b[0] - dc[0]) < 1e-9)

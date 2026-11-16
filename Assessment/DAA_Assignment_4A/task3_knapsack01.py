"""
Task 3 - 0/1 Knapsack (Dynamic Programming)
dp[i][w] = max value achievable using the first i items with capacity w.
"""


def knapsack_01(items, capacity):
    """
    items: list of dicts {"id": str, "weight": int, "value": float}
    capacity: integer capacity
    returns: (max_value, selected_items)
    """
    n = len(items)
    weight = [0] + [it["weight"] for it in items]
    value = [0] + [it["value"] for it in items]

    # dp[i][w]
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weight[i] > w:
                dp[i][w] = dp[i - 1][w]
            else:
                include_value = value[i] + dp[i - 1][w - weight[i]]
                exclude_value = dp[i - 1][w]
                dp[i][w] = max(include_value, exclude_value)

    max_value = dp[n][capacity]

    # Traceback to reconstruct selected items
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(items[i - 1]["id"])
            w -= weight[i]

    selected.reverse()
    return max_value, selected, dp


if __name__ == "__main__":
    items = [
        {"id": "P", "weight": 2, "value": 12},
        {"id": "Q", "weight": 3, "value": 20},
        {"id": "R", "weight": 4, "value": 25},
        {"id": "S", "weight": 5, "value": 30},
    ]
    capacity = 7

    max_value, selected, dp = knapsack_01(items, capacity)
    print("0/1 Knapsack (Dynamic Programming)")
    print(f"Capacity = {capacity}")
    print(f"Max value = {max_value}")
    print(f"Selected items = {selected}")

    print("\nDP table (rows = items considered 0..n, cols = capacity 0..W):")
    for row in dp:
        print(row)

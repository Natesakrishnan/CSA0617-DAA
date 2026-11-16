"""
Task 1 - Fractional Knapsack (Greedy)
Packages may be divided. Greedy-choice rule: sort by value/weight ratio, descending.
"""


def load_vehicle(packages, capacity):
    """
    packages: list of dicts {"id": str, "weight": float, "value": float}
    capacity: total vehicle capacity
    returns: (total_value, selected) where selected is a list of
             (package_id, fraction_taken) pairs
    """
    # Step 1: greedy-choice ratio
    items = [dict(p, ratio=p["value"] / p["weight"]) for p in packages]

    # Step 2: sort by ratio, descending (the greedy-choice rule)
    items.sort(key=lambda p: p["ratio"], reverse=True)

    remaining = capacity
    total_value = 0.0
    selected = []

    # Step 3: greedily fill the vehicle
    for item in items:
        if remaining == 0:
            break
        if item["weight"] <= remaining:
            selected.append((item["id"], 1.0))
            total_value += item["value"]
            remaining -= item["weight"]
        else:
            fraction = remaining / item["weight"]
            selected.append((item["id"], fraction))
            total_value += fraction * item["value"]
            remaining = 0

    return total_value, selected


if __name__ == "__main__":
    packages = [
        {"id": "P1", "weight": 10, "value": 60},
        {"id": "P2", "weight": 20, "value": 100},
        {"id": "P3", "weight": 30, "value": 120},
    ]
    capacity = 50

    total_value, selected = load_vehicle(packages, capacity)
    print("Fractional Knapsack")
    print(f"Capacity = {capacity}")
    for pid, frac in selected:
        print(f"  {pid}: fraction taken = {frac:.3f}")
    print(f"Total value = {total_value:.2f}")

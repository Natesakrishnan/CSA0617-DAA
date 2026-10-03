def rob_linear(nums):
    prev = 0
    curr = 0

    for money in nums:
        prev, curr = curr, max(curr, prev + money)

    return curr


def rob(nums):
    if len(nums) == 1:
        return nums[0]

    return max(
        rob_linear(nums[:-1]),
        rob_linear(nums[1:])
    )


print(rob([2, 3, 2]))
print(rob([1, 2, 3, 1]))

"""
You are given an integer array nums. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position.

Return true if you can reach the last index, or false otherwise.


Example 1:

Input: nums = [2,3,1,1,4]
Output: true
Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.

Example 2:

Input: nums = [3,2,1,0,4]
Output: false
Explanation: You will always arrive at index 3 no matter what. Its maximum jump length is 0, which makes it impossible to reach the last index.

# invariant
for each i, have range(nums[i]) jump
max = 0
if nums[i] == 2 -> 0, 1, 2

for j in [0, 1, 2]:
  if current_i + j == target:
    return true
  else:
    return dfs(j, [curr_i])
"""


# def canJump(nums):
#     goal = len(nums) - 1

#     for i in range(len(nums))[::-1]:
#         print(i, nums[i], goal)
#         if i + nums[i] >= goal:
#             goal = i

#     return not goal


# def canJump(nums):
#     m = 0

#     for i, n in enumerate(nums):
#         if i > m:
#             return False
#         m = max(m, i + n)


from functools import lru_cache


def canJump(nums):
    n = len(nums)

    @lru_cache(None)
    def dp(i):
        if i == n - 1:
            return True

        for j in range(i + 1, min(i + nums[i], n - 1) + 1):
            if dp(j):
                return True

        return False

    return dp(0)


if __name__ == "__main__":
    t = [2, 3, 1, 1, 4]
    # t = [1, 2]

    print(canJump(t))

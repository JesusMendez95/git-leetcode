from typing import List


class Solution:
    def findClosestNumber(self, nums: List[int]) -> int:
        best = nums[0]
        for value in nums[1:]:
            if abs(value) < abs(best):
                best = value
            elif abs(value) == abs(best) and value > best:
                best = value
        return best

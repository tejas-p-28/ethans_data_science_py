class Solution(object):
    def twoSum(self, nums, target):
        result = {}
        for i, num in enumerate(nums):
            need = target - num
            if need in result:
                return [result[need], i]
            result[num] = i

        
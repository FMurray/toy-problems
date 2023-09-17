def single_number(nums) -> int:
    xor = 0
    for num in nums:
        xor ^= num
    return xor
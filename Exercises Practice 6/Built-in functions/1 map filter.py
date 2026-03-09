nums = list(map(int, input().split()))
print(nums)

# Square every number inside list with lambda
nums = list(map(lambda x: x ** 2, nums))
print(nums)

# makes even numbers negative
nums = list(map(lambda x: -x if x % 2 == 0 else x, nums))
print(nums)

# Makes every number non-negative
nums = list(map(lambda x: abs(x), nums))
print(nums)

# Removes even numbers
nums = list(filter(lambda x: x % 2 == 1, nums))
print(nums)

# Subtracts 10 from all numbers
nums = list(map(lambda x: x - 10, nums))
print(nums)

# Removes negative numbers
nums = list(filter(lambda x: x > 0, nums))
print(nums)


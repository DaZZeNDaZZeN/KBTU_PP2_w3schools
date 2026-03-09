from functools import reduce

nums = list(map(int, input().split()))

# sum
s = reduce(lambda a, b: a + b, nums)
print(f"Sum: {s}")

# product
p = reduce(lambda a, b: a * b, nums)
print(f"Product: {p}")

# sum of all even numbers, just use normal loop for this
s_even = reduce(lambda a, b: a + b if a % 2 == 0 and b % 2 == 0 else a if a % 2 == 0 else b if b % 2 == 0 else 0, nums)
print(f"Sum of even numbers: {s_even}")



data = {"user": {"profile": {"settings": {"theme": "dark"}}}}
path = ["user", "profile", "settings", "theme"]

# Traversing the dictionary step-by-step
value = reduce(lambda d, key: d.get(key, {}), path, data)
# Result: "dark"


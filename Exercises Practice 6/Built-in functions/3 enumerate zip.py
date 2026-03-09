names = ["Alice", "Celia", "Airis", "Flos"]

print("Current list of guests")
for i, v in enumerate(names):
    print(f"{i + 1}. {v}")
print("\n")

print("Current list of guests and their statuses")
status = ["VIP", "Regular", "Regular", "VIP"]
for i, n, s in zip(range(1, len(names) + 1), names, status):
    print(f"{i}. {n} - {s}")


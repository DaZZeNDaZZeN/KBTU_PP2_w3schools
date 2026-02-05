# Skipping elements with small length
a = ["abc" "abcdefg", "This is a long string", "shrt"]
i = 0
while i < len(a):
    if len(a[i]) < 5:
        continue
    print(a[i])

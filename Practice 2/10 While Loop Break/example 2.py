# Break and else in while loop
i = 4
while i < 10:
    print(i)
    if i == 6:
        break
else:
    # Will be executed if loop ended without break command
    print("Else block")

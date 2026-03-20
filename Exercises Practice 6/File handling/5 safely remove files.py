import os

path = "text.txt"

if os.path.exists(path):
    os.remove(path)
    print("File deleted")
else:
    print("File not found")


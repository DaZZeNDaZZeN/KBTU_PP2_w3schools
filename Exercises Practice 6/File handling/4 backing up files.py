import shutil
import os

source = "dir1/"
destination = "backup/"

with os.scandir(source) as d:
    for entry in d:
        s = source + entry.name
        dest = destination + entry.name
        shutil.copy2(s, dest)
        print(f"File copied to {dest}")


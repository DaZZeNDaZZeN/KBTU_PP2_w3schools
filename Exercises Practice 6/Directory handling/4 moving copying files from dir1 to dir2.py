import shutil
import os

action = ""
while action != "copy" and action != "move":
    action = input("Action (copy or move): ")

source = "dir1/"
destination = "dir2/"

with os.scandir(source) as d:
    for entry in d:
        s = source + entry.name
        dest = destination + entry.name
        if action == "copy":
            shutil.copy2(s, dest)
            print(f"File copied to {dest}")
        elif action == "move":
            shutil.move(s, dest)
            print(f"File moved to {dest}")



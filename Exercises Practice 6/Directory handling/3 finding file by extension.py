import os

ext = ".txt"

with os.scandir('.') as d:
    for entry in d:
        if not entry.name.endswith(ext):
            continue
        s = "File: " if entry.is_file() else "Folder: " if entry.is_dir() else ""
        print(s + entry.name)

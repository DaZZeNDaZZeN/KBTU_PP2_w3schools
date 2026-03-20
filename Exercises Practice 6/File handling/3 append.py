with open("text.txt", "A") as f:
	f.write("sample data #2")

# veryfing after append
with open("text.txt", "r") as file:
    content = file.read()
    print(content)


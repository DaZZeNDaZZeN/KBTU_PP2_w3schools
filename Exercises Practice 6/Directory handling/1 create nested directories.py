import os

path = "new_folder/nested_folder/"

os.makedirs(path, exist_ok=True)
print("Nested directories created successfully.")


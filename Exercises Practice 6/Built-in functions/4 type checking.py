data = [1, 2, 3]

# Using type()
print(type(data))  # <class 'list'>

# Using isinstance() - Recommended, supports inheritance.
if isinstance(data, list):
    print("This is definitely a list!")


age_str = "25"  # Imagine this came from an input()

# Type Checking
print(f"Start type: {type(age_str)}")

# Conversion
age_int = int(age_str)
new_age = age_int + 1

print(f"Next year you will be {new_age}. (Type: {type(age_int)})")



# Starting with a list that has duplicates
my_list = [1, 2, 2, 3, 4, 4, 5]

# Convert to a set to remove duplicates
my_set = set(my_list) 
# Output: {1, 2, 3, 4, 5}
print(my_set)
# Convert back to a list to keep it ordered and mutable
unique_list = list(my_set)
print(unique_list)
# Convert to a tuple to ensure the data cannot be changed
final_data = tuple(unique_list)
print(final_data)



# The ': int' and '-> int' are hints, not strict rules
def calculate_area(width: int, height: int) -> int:
    return width * height

result = calculate_area(10, 5)
print(f"Area of rectangle: {result}")






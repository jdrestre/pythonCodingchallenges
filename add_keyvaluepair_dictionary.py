"""
Python script to add a Key-Value Pair to the dictionary
"""


def add_key_value(dictionary, key, value):
    """Adds a key-value pair to a dictionary."""
    dictionary[key] = value
    return dictionary


my_dict = {"name": "Juan", "age": 45, "city": "Medellín"}
print("Original dictionary: ", my_dict)

key_to_add = input("Enter the key to add: ")
value_to_add = input("Enter the value for the key: ")

update_dict = add_key_value(my_dict, key_to_add, value_to_add)
print("Updated dictionary: ", update_dict)

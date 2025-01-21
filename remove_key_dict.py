"""
Python script to remove a key from a Dictionary
"""
my_dict = {"name": "Juan David", "age": "45", "city": "Medellín"}
print("Original Dictionary:", my_dict)


def remove_key_from_dict(dictionary, key_to_remove):
    """Removes a key from the dictionary if it exists."""
    if key_to_remove in dictionary:
        del dictionary[key_to_remove]
        print(f"Key '{key_to_remove}' has been removed")
    else:
        print(f"Key '{key_to_remove}' not found in the dictionary")

    return dictionary



key = input("Enter the key to remove: ")
update_dict = remove_key_from_dict(my_dict, key)

print("Update Dictionary:", update_dict)

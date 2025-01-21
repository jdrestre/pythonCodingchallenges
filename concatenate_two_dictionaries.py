"""
Python script to concatenate two Dictionaries
"""

dict1 = {'a': 1, 'b': 2}
print("Dictionary 1:", dict1)
dict2 = {'c': 3, 'd': 4}
print("Dictionary 2:", dict2)

dict1.update(dict2)

print("Concatenated Dictionary:", dict1)

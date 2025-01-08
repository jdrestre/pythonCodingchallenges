"""
Python script to create a new string from made up of first and las 2 characters
"""


def new_string(string):
    """function to create a new string from made up of first and last 2 characters"""
    if len(string) < 2:
        return ''
    return string[:2] + string[-2:]


user_input = input("Enter a string: ")
result = new_string(user_input)
print("New string is: ", result)

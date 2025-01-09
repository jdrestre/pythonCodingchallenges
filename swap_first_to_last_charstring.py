"""
Script to swap the first and last character of a string
"""

def swap_first_last_char(string):
    """function to swap the first and last character of a string"""
    if len(string) <= 1:
        return string

    swapped_string = string[-1] + string[1:-1] + string[0]
    print(string[1:-1])
    return swapped_string

user_input = input("Enter a string: ")
result = swap_first_last_char(user_input)

print(f"String after swapping the first and last characters: {result}")

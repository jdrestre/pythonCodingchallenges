"""
Program to count the number of vowels in a string entered by the user. 
"""


def count_vowels(string):
    """function to count the number of vowels in a string"""
    # Use a list comprehension to count the vowels
    # cSpell: ignore aeiouáéíóú
    return sum([1 for char in string if char in "aeiouáéíóú"])


# Get the user input
RESULT = count_vowels(input("Enter a string: ").lower())
print(f"Number of vowels in the string: {RESULT}")

# Output:
# Enter a string: Hello World
# Number of vowels in the string: 3

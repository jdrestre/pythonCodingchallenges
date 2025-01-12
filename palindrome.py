"""
Python script to check if a string is a palindrome or not.
"""


def is_palindrome(string):
    """function to check if a string is a palindrome"""
    # Verify if the string is empty
    if not string:
        return False
    # Remove spaces and convert to lowercase
    string = string.replace(" ", "").lower()
    # If letters have accents remove them
    string = string.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u") # pylint: disable=line-too-long
    # Compare the string with its reverse
    return string == string[::-1]


# Get the user input
USER_INPUT = input("Enter a string: ")
RESULT = is_palindrome(USER_INPUT)
# Check the result and print the output
if RESULT:
    print(f"{USER_INPUT} is a palindrome")
else:
    print(f"{USER_INPUT} is not a palindrome")

# Output:
# Enter a string: Hello World
# Hello World is not a palindrome
# Enter a string: A Santa at NASA
# A Santa at NASA is a palindrome

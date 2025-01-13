"""
Script in Python that receives two strings and returns if they are anagrams or not.
An anagram is a word or phrase formed by rearranging the letters of another 
word or phrase, using all the original letters exactly once. For example, the 
anagram of the word "listen" could be "silent."
"""


def anagramas_2strings(string1, string2):
    """
    Function that receives two strings and returns if they are anagrams or not.
    """
    string1 = string1.lower().replace(" ", "")
    string2 = string2.lower().replace(" ", "")
    return sorted(string1) == sorted(string2)


# Get the user input
USER_INPUT1 = input("Enter the first string: ")
USER_INPUT2 = input("Enter the second string: ")
RESULT = anagramas_2strings(USER_INPUT1, USER_INPUT2)
# Check the result and print the output
if RESULT:
    print(f"{USER_INPUT1} and {USER_INPUT2} are anagrams")
else:
    print(f"{USER_INPUT1} and {USER_INPUT2} are not anagrams")

# Output:
# Enter the first string: Listen
# Enter the second string: Silent
# Listen and Silent are anagrams

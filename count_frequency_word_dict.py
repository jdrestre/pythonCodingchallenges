"""
Python script to count the frequency of each word in a string using Dictionary
"""


def count_word_frequency(input_string):
    """ Count the frequency of each word in the input string """
    words = input_string.split()
    word_count = {}

    for word in words:
        word = word.lower()
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    return word_count


INPUT_STRING = input("Enter a string: ")
word_frequency = count_word_frequency(INPUT_STRING)
print("\nWord Frequency:")
for WORD, count in word_frequency.items():
    print(f"'{WORD}':{count}")

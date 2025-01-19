"""
Python script to count the occurrences of each word in a string
"""
def count_word_occurrences(input_string):
    """Counts the occurrences of each word in the given input string."""
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

result = count_word_occurrences(INPUT_STRING)
print(result)

print("\nWord occurrences: ")
sorted_result = sorted(result.items(), key=lambda item: item[1], reverse=True)
for WORD, count in sorted_result:
    print(f"{WORD}: {count}")

""" Python script to remove odd indexed characters in a string """
def remove_odd_idexed_chars(input_string):
    """ Remove characters at odd indices from the input string """
    return input_string[::2]
if __name__ == "__main__":
    input_string = input("Enter a string: ")
    result = remove_odd_idexed_chars(input_string)
    print(f"String after removing odd indexed characters:", result)

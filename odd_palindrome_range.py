"""
Python script to find all odd palindrome numbers (capicua) in a range without use recursion
""" # cSpell: ignore capicua

def is_palindrome(n):
    """
    Check if a given number is a palindrome.
    A palindrome is a number that reads the same backward as forward.
    """
    return str(n) == str(n)[::-1]

def odd_palindromes_in_range(start, end):
    """
    Find all odd palindromic numbers within a given range.
    This function takes a start and end value, and returns a list of all odd numbers
    within that range (inclusive) that are also palindromes.
    """
    odd_palindromes = []
    for num in range(start, end + 1):
        if num % 2 != 0 and is_palindrome(num):
            odd_palindromes.append(num)
    return odd_palindromes

START = int(input("Enter the start number: "))
END = int(input("Enter the end number: "))

result = odd_palindromes_in_range(START, END)
print(f"Odd palindrome numbers between {START} and {END} = {result}")

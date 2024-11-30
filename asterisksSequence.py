# Write a function for print a sequence of asterisks in a line until five maximum. And then, print the same sequence in reverse order.

def asterisksSequence():
    for i in range(1, 6):
        print("*" * i)
    for i in range(4, 0, -1):
        print("*" * i)


asterisksSequence()

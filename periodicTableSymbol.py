import periodictable

# Function to get information about an element
def get_element_info(symbol):
    # Check if the symbol is valid
    if not periodictable.elements.symbol(symbol):
        print("Invalid element symbol.")
        return
    # Access information about the specified element
    element = periodictable.elements.symbol(symbol)
    
    # Print information about the element
    print(f"Element: {element.name}")
    print(f"Symbol: {element.symbol}")
    print(f"Atomic Number : {element.number}")
    print(f"Atomic Weight: {element.mass}")
    print(f"Density: {element.density}")

# Prompt the user to input an element symbol
element_symbol = input("Enter the symbol of the element: ")

# Call the function to get information about the specified element
get_element_info(element_symbol)

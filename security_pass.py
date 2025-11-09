"""
Secure password generator with variable size defined by the user.
Includes input validation and security best practices.
"""
import string
import secrets
import sys


def generate_password(size=12):
    """
    Generate a secure password with numbers, letters and symbols.

    Args:
        size (int): Password length (minimum 8 characters)

    Returns:
        str: Generated password
    """
    if size < 8:
        print("⚠️  Warning: A minimum of 8 characters is recommended")
        size = 8

    # Define character sets
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    numbers = string.digits
    symbols = string.punctuation

    # Combine all available characters
    all_characters = uppercase_letters + lowercase_letters + numbers + symbols

    # Ensure password has at least one character of each type
    password = [
        secrets.choice(uppercase_letters),
        secrets.choice(lowercase_letters),
        secrets.choice(numbers),
        secrets.choice(symbols)
    ]

    # Fill the rest of the password with random characters
    password += [secrets.choice(all_characters) for _ in range(size - 4)]

    # Shuffle characters to avoid predictable patterns
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)


def request_size():
    """
    Request password size from user with validation.

    Returns:
        int: Valid password size
    """
    while True:
        try:
            size = input("\nWhat size do you want the password? (minimum 8): ")
            size = int(size)

            if size < 1:
                print("❌ Size must be a positive number. Try again.")
                continue

            return size

        except ValueError:
            print("❌ Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n\n👋 Program cancelled by user.")
            sys.exit(0)


def main():
    """Main program function"""
    print("=" * 50)
    print("🔐 SECURE PASSWORD GENERATOR")
    print("=" * 50)

    size = request_size()
    password = generate_password(size)

    print("\n" + "=" * 50)
    print(f"✅ Generated password: {password}")
    print(f"📏 Length: {len(password)} characters")
    print("=" * 50)

    # Option to generate another password
    while True:
        another = input("\nGenerate another password? (y/n): ").lower()
        if another == 'y':
            size = request_size()
            password = generate_password(size)
            print("\n" + "=" * 50)
            print(f"✅ Generated password: {password}")
            print(f"📏 Length: {len(password)} characters")
            print("=" * 50)
        elif another == 'n':
            print("\n👋 Goodbye! Keep your passwords secure.")
            break
        else:
            print("❌ Please answer 'y' for yes or 'n' for no.")


if __name__ == "__main__":
    main()

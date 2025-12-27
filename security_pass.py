"""
Secure password generator with variable size defined by the user.
Includes input validation, security best practices, and entropy calculation.

Security standards compliance:
- OWASP: Complex character requirements
- NIST SP 800-63B: Minimum entropy recommendations
- Uses secrets module for cryptographically secure randomness
"""
import string
import secrets
import sys
import math


# Security constants
MIN_PASSWORD_LENGTH = 4
MAX_PASSWORD_LENGTH = 128
RECOMMENDED_LENGTH = 16

# Character set definitions
UPPERCASE_LETTERS = string.ascii_uppercase
LOWERCASE_LETTERS = string.ascii_lowercase
NUMBERS = string.digits

# Safe symbols (exclude problematic characters that may cause issues in some contexts)
# Excluded: " ' ` \ (may cause parsing issues in shells/databases)
SAFE_SYMBOLS = "!#$%&*+-=?@^_~"
UNSAFE_SYMBOLS = "\"'`\\|;<>"


def calculate_entropy(password_length, character_set_size):
    """
    Calculate password entropy in bits.
    
    Entropy (bits) = log2(character_set^password_length)
    
    Args:
        password_length (int): Length of the password
        character_set_size (int): Number of unique possible characters
    
    Returns:
        float: Entropy in bits
    """
    if character_set_size <= 1 or password_length <= 0:
        return 0.0
    return password_length * math.log2(character_set_size)


def get_entropy_strength(entropy_bits):
    """
    Classify password strength based on entropy bits.
    
    Security levels (OWASP recommendations):
    - < 28 bits: Weak (crackable in hours)
    - 28-35 bits: Fair (crackable in days/weeks)
    - 36-59 bits: Good (crackable in years)
    - 60+ bits: Strong (practically impossible with current technology)
    
    Args:
        entropy_bits (float): Entropy in bits
    
    Returns:
        tuple: (strength_level, description)
    """
    if entropy_bits < 28:
        return "⚠️  WEAK", "Crackable in hours"
    elif entropy_bits < 36:
        return "⚡ FAIR", "Crackable in days/weeks"
    elif entropy_bits < 60:
        return "✅ GOOD", "Crackable in years (acceptable)"
    else:
        return "🔐 STRONG", "Practically secure"


def generate_password(size=12, include_uppercase=True, include_lowercase=True,
                      include_numbers=True, include_symbols=True, 
                      safe_mode=False):
    """
    Generate a cryptographically secure password.

    Args:
        size (int): Password length (8-128 characters, default 12)
        include_uppercase (bool): Include uppercase letters (A-Z)
        include_lowercase (bool): Include lowercase letters (a-z)
        include_numbers (bool): Include numbers (0-9)
        include_symbols (bool): Include symbols
        safe_mode (bool): Exclude problematic symbols (", ', `, \\)

    Returns:
        tuple: (password_str, entropy_bits, strength_description)
        
    Raises:
        ValueError: If parameters are invalid
    """
    # Validate size
    if not isinstance(size, int):
        raise ValueError("Size must be an integer")
    
    if size < MIN_PASSWORD_LENGTH:
        raise ValueError(f"Minimum length is {MIN_PASSWORD_LENGTH} characters")
    
    if size > MAX_PASSWORD_LENGTH:
        raise ValueError(f"Maximum length is {MAX_PASSWORD_LENGTH} characters")

    # Build character set based on options
    character_pool = ""
    
    if include_uppercase:
        character_pool += UPPERCASE_LETTERS
    if include_lowercase:
        character_pool += LOWERCASE_LETTERS
    if include_numbers:
        character_pool += NUMBERS
    if include_symbols:
        character_pool += SAFE_SYMBOLS if safe_mode else (SAFE_SYMBOLS + UNSAFE_SYMBOLS)

    if not character_pool:
        raise ValueError("At least one character type must be included")

    # Build password ensuring at least one character from each selected type
    password = []
    
    if include_uppercase:
        password.append(secrets.choice(UPPERCASE_LETTERS))
    if include_lowercase:
        password.append(secrets.choice(LOWERCASE_LETTERS))
    if include_numbers:
        password.append(secrets.choice(NUMBERS))
    if include_symbols:
        symbols_set = SAFE_SYMBOLS if safe_mode else (SAFE_SYMBOLS + UNSAFE_SYMBOLS)
        password.append(secrets.choice(symbols_set))

    # Fill remaining positions with random characters from the complete pool
    remaining_length = size - len(password)
    password += [secrets.choice(character_pool) for _ in range(remaining_length)]

    # Shuffle using cryptographically secure random
    secrets.SystemRandom().shuffle(password)
    
    password_str = ''.join(password)
    
    # Calculate entropy
    entropy = calculate_entropy(len(password_str), len(character_pool))
    strength, description = get_entropy_strength(entropy)

    return password_str, entropy, strength


def request_size():
    """
    Request password size from user with validation.

    Returns:
        int: Valid password size (8-128)
    """
    while True:
        try:
            size_input = input(f"\nPassword length [{MIN_PASSWORD_LENGTH}-{MAX_PASSWORD_LENGTH}] "
                             f"(recommended: {RECOMMENDED_LENGTH}): ")
            size = int(size_input)

            if size < MIN_PASSWORD_LENGTH:
                print(f"❌ Minimum length is {MIN_PASSWORD_LENGTH} characters. Try again.")
                continue
            
            if size > MAX_PASSWORD_LENGTH:
                print(f"❌ Maximum length is {MAX_PASSWORD_LENGTH} characters. Try again.")
                continue

            if size < RECOMMENDED_LENGTH:
                print(f"⚠️  Warning: {RECOMMENDED_LENGTH}+ characters recommended for better security")
            
            return size

        except ValueError:
            print("❌ Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n\n👋 Program cancelled by user.")
            sys.exit(0)


def request_options():
    """
    Request password generation options from user.
    
    Returns:
        tuple: (include_uppercase, include_lowercase, include_numbers, 
                include_symbols, safe_mode)
    """
    print("\n" + "-" * 50)
    print("Character set options:")
    print("-" * 50)
    
    while True:
        try:
            options = input("Include uppercase letters (A-Z)? [Y/n]: ").lower()
            include_upper = options != 'n'
            break
        except KeyboardInterrupt:
            print("\n\n👋 Program cancelled by user.")
            sys.exit(0)
    
    while True:
        try:
            options = input("Include lowercase letters (a-z)? [Y/n]: ").lower()
            include_lower = options != 'n'
            break
        except KeyboardInterrupt:
            print("\n\n👋 Program cancelled by user.")
            sys.exit(0)
    
    while True:
        try:
            options = input("Include numbers (0-9)? [Y/n]: ").lower()
            include_nums = options != 'n'
            break
        except KeyboardInterrupt:
            print("\n\n👋 Program cancelled by user.")
            sys.exit(0)
    
    while True:
        try:
            options = input("Include symbols? [Y/n]: ").lower()
            include_syms = options != 'n'
            break
        except KeyboardInterrupt:
            print("\n\n👋 Program cancelled by user.")
            sys.exit(0)
    
    safe_mode = False
    if include_syms:
        while True:
            try:
                safe = input("Use safe symbols only? (excludes \", ', `, \\) [Y/n]: ").lower()
                safe_mode = safe != 'n'
                break
            except KeyboardInterrupt:
                print("\n\n👋 Program cancelled by user.")
                sys.exit(0)
    
    # Ensure at least one option is selected
    if not any([include_upper, include_lower, include_nums, include_syms]):
        print("❌ At least one character type must be selected.")
        return request_options()
    
    return include_upper, include_lower, include_nums, include_syms, safe_mode


def display_password_info(password, entropy, strength):
    """
    Display generated password with detailed security information.
    
    Args:
        password (str): Generated password
        entropy (float): Entropy in bits
        strength (str): Strength classification
    """
    print("\n" + "=" * 60)
    print("✅ PASSWORD GENERATED SUCCESSFULLY")
    print("=" * 60)
    print(f"\nPassword: {password}")
    print(f"Length: {len(password)} characters")
    print(f"\nSecurity Metrics:")
    print(f"  • Entropy: {entropy:.2f} bits")
    print(f"  • Strength: {strength}")
    print(f"  • Character space: {len(set(password))} unique characters")
    print("=" * 60)
    
    # Security recommendations
    if entropy < 50:
        print("\n💡 Tip: Consider increasing length for better security")
    if len(password) > 100:
        print("\n💡 Note: Very long passwords are strong but harder to remember")


def main():
    """Main program function"""
    print("\n" + "=" * 60)
    print("🔐 SECURE PASSWORD GENERATOR v2.0")
    print("=" * 60)
    print("\nSecurity Features:")
    print("  • Uses cryptographically secure random (secrets module)")
    print("  • Entropy calculation for strength assessment")
    print("  • Multiple character set options")
    print("  • Safe symbols mode for problematic contexts")
    print("=" * 60)

    while True:
        try:
            # Get user preferences
            show_options = input("\nCustomize password generation? (y/n): ").lower()
            
            if show_options == 'y':
                include_upper, include_lower, include_nums, include_syms, safe_mode = request_options()
            else:
                # Default secure options
                include_upper, include_lower, include_nums, include_syms, safe_mode = True, True, True, True, True
            
            size = request_size()
            
            # Generate password
            password, entropy, strength = generate_password(
                size=size,
                include_uppercase=include_upper,
                include_lowercase=include_lower,
                include_numbers=include_nums,
                include_symbols=include_syms,
                safe_mode=safe_mode
            )
            
            display_password_info(password, entropy, strength)
            
            # Option to generate another password
            while True:
                another = input("\nGenerate another password? (y/n): ").lower()
                if another in ['y', 'n']:
                    break
                print("❌ Please enter 'y' or 'n'")
            
            if another == 'n':
                print("\n👋 Goodbye! Keep your passwords secure.")
                print("   📌 Tips:")
                print("      • Use unique passwords for each service")
                print("      • Store them in a password manager")
                print("      • Enable 2FA when available")
                print("=" * 60 + "\n")
                sys.exit(0)
                
        except KeyboardInterrupt:
            print("\n\n👋 Program cancelled by user.")
            sys.exit(0)
        except ValueError as e:
            print(f"❌ Error: {e}")
            continue


if __name__ == "__main__":
    main()

# COS60018: Unicode-Aware Password Validator
# Whitelist of 50 safe, atomic emojis.
# Stored as literal UTF-8 characters for readability.


import math # Required for entropy calculations
import shutil # Required for adjusting the results to fit the terminal width

STANDARD_POOL_SIZE = 94

WHITELIST_POOL_SIZE = 144

MAX_EMOJI_POOL_SIZE = 1494 # Maximum atomic emoji pool size. Doesn't include complex emojis.


safe_emojis = [
    # Faces & Expressions
    '😀', '😂', '😊', '😎', '🤔', '😴', '🤯', '🥳', '😭', '😡',
    '😱', '🥶', '🥴', '🤐', '🤠', 
    
    # Animals & Nature
    '🐶', '🐱', '🦊', '🐼', '🐸', '🐙', '🦋', '🌻', '🌲', '🍎',
    '🍓', '🍉', 
    
    # Food & Drink
    '🍕', '🍔', '☕', 
    
    # Objects & Activities
    '🎸', '⚽', '🚗', '🚀', '⌚', '💡', '📚', '🎈', '🎁', '🏆',
    '👑', '💎', '🔔', '🔑', '🔒', 
    
    # Symbols & Gestures (Includes skin-tone compatible 👍)
    '👍', '💙', '🔥', '💧', '💯'
]


def IsValid(password_string):
    """
    Checks to ensure that the password entered is valid according to the criteria:
    - Must be at least 6 characters long.
    - Must contain at least one digit.
    - Must contain at least one atomic emoji from the safe list.
    - Must contain at least one special character.
    - Must not contain complex emojis
    """
    # Check for length
    if len(password_string) < 7:
       print("Your password must be at least 7 characters long. Please try again")
       return False
    # Check for at least one number
    has_number = False
    for char in password_string:
        if char.isdigit():
            has_number = True
            break
    if has_number == False:
        print("Your password must have at least one number in it")
        return False
    # Check for an emoji in the safe list
    has_emoji = False
    for char in password_string:
        if char in safe_emojis:
            has_emoji = True
            break
    if has_emoji == False:
        print("Your password must have at least one emoji from the whitelist in it")
        return False
    # Check for at least one special character
    standard_symbols = "!@#$%^&*()-_=+[]{}|;:'\",.<>/?~\\`"
    has_symbol = False
    for char in password_string:
        if char in standard_symbols:
            has_symbol = True
            break
    if has_symbol == False:
        print("Your password must have at least one special character in it. Please try again.")
        return False
    # Reject invisible joiners and skin tone modifiers
    forbidden_modifiers = [
        '\u200d',       # Zero Width Joiner (glues emojis together)
        '\ufe0f',       # Variation Selector (forces emoji styling)
        '\U0001f3fb',   # Light Skin Tone
        '\U0001f3fc',   # Medium-Light Skin Tone
        '\U0001f3fd',   # Medium Skin Tone
        '\U0001f3fe',   # Medium-Dark Skin Tone
        '\U0001f3ff'    # Dark Skin Tone
    ]
    for char in password_string:
        if char in forbidden_modifiers:
            if char == '\u200d':
                print("Modifier ZWJ has been used")
            elif char == '\ufe0f':
                print("Variation Selector Modifier has been used")
            else:
                print(f"Modifier {char} has been used")
            print("You have used a complex emoji or one with modifiers in it. " \
            "Only emojis in the list above can be used. "\
            "Please try again."
            )
            return False
    print("Your password is VALID!")
    return True
    

def CalculateEntropy(password_string, pool_size):
    """
    Calculates Shannon entropy for a given password and character pool.
    Returns the raw float value representing bits of entropy.
    """
    # Calculate the total length of the password
    password_length = len(password_string)
    
    # Apply Shannon's Entropy Formula: E = L * log2(R)
    entropy_score = password_length * math.log2(pool_size)
    
    # Return the final score in raw format
    return entropy_score

    

def CalculateCrackTime(entropy_score):
    """
    Calculates the expected time to crack based on the entropy and guessing at a rate \
    of 100 billion guesses per second
    """
    guesses_per_second = 100_000_000_000 # Underscores improve readability. Ignored by Python. 
    
    # 2 to the power of the entropy score gives us the total combinations
    total_combinations = 2 ** entropy_score
    
    # Calculate total seconds to guess every combination (divided by 2 to calculate average crack time)
    seconds = total_combinations / guesses_per_second / 2
    
    # Convert seconds into a human readable format
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f} minutes"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.2f} hours"
    elif seconds < 31_536_000:
        days = seconds / 86400
        return f"{days:.2f} days"
    elif seconds < 31_536_000_000_000:
        years = seconds / 31536000
        # The colon and comma automatically format large numbers (e.g., 1,000,000)
        return f"{round(years):,} years"
    elif seconds < 31_536_000_000_000_000:
        million_years = seconds / 31_536_000_000_000   # Underscores improve readability.
        return f"{round(million_years):,} million years"
    elif seconds < 157_680_000_000_000_000:  # ~5 billion years
        billion_years = seconds / 31_536_000_000_000_000
        return f"{round(billion_years):,} billion years"
    else:
        return f"Sun engulfs Earth first."


if __name__ == "__main__":  # Run the program
    print("Your password must contain at least one of the following secure emojis:")

    # Loop through the array and print them in neat rows of 10

    count = 0
    for i in safe_emojis:
        print(i,end=" ")
        count += 1
        if count % 10 == 0:
            print()

    password_is_valid = False
    while password_is_valid == False:
        password = input("\nEnter your new password: ")
        password_is_valid = IsValid(password)

    # Password validity test complete. Now for entropy calculations.
    final_entropy = CalculateEntropy(password, WHITELIST_POOL_SIZE) # standard pool size + 50 emojis
    entropy_no_emojis = CalculateEntropy(password, STANDARD_POOL_SIZE) # standard pool size
    entropy_all_emojis = CalculateEntropy(password, MAX_EMOJI_POOL_SIZE) # standard pool size + 1400 atomic emojis
    crack_time = CalculateCrackTime(final_entropy)
    crack_time_no_emojis = CalculateCrackTime(entropy_no_emojis)
    crack_time_all_emojis = CalculateCrackTime(entropy_all_emojis)


    # Capture the length of the valid password
    password_length = len(password)

    # Query terminal width
    display_width = max(shutil.get_terminal_size(fallback=(112, 24)).columns, 112)
    w = ((display_width - 37) // 3) # 3 columns of equal width. Minus 37 to account for "space | space" * 4, and fixed length columns, POOL SIZE and PASSWORD LENGTH

    # Print a decorative header (Expanded to max terminal width)
    print("\n" + "=" * display_width)
    print(f"{'PASSWORD SECURITY ANALYSIS':^{display_width}}")
    print("=" * display_width)

    # Print the table column titles
    print(f"{'SCENARIO':^{w}} | {'POOL SIZE':^10} | {'PASSWORD LENGTH':^15} | {'ENTROPY (BITS)':^{w}} | {'AVERAGE CRACK TIME':^{w}}")
    print("-" * display_width)

    # Print the data rows with the new length variable
    print(f"{'Standard (No Emojis)':^{w}} | {STANDARD_POOL_SIZE:^10} | {password_length:^15} | {entropy_no_emojis:^{w}.2f} | {crack_time_no_emojis:^{w}}")
    print(f"{'Whitelist (50 Emojis)':^{w}} | {WHITELIST_POOL_SIZE:^10} | {password_length:^15} | {final_entropy:^{w}.2f} | {crack_time:^{w}}")
    print(f"{'All atomic Emojis (~1400)':^{w}} | {MAX_EMOJI_POOL_SIZE:^10} | {password_length:^15} | {entropy_all_emojis:^{w}.2f} | {crack_time_all_emojis:^{w}}")

    # Print a closing border
    print("=" * display_width + "\n")
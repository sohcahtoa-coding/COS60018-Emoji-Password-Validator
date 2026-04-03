# COS60018: Unicode-Aware Password Validator
# Whitelist of 50 safe, atomic emojis.
# Stored as literal UTF-8 characters for readability.


import math # Required for entropy calculations


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

print("Your password must contain at least one of the following secure emojis:")

def IsValid(password_string):
    # Check for length
    if len(password_string) < 6:
       print("Your password must be at least 8 characters long. Please try again")
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
    standard_symbols = "!@#$%^&*()-_=+[]{}|;:'\",.<>/?~"
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
    has_modifier = False
    for char in password_string:
        if char in forbidden_modifiers:
            has_modifier = True
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
    # Calculate the total length of the password
    password_length = len(password_string)
    
    # Apply Shannon's Entropy Formula: E = L * log2(R)
    entropy_score = password_length * math.log2(pool_size)
    
    # Return the final score, rounded to 2 decimal places for a clean terminal output
    return round(entropy_score, 2)
    

def CalculateCrackTime(entropy_score):
    # We assume a modern cracking rig can test 100 billion passwords a second
    guesses_per_second = 100000000000 
    
    # 2 to the power of the entropy score gives us the total combinations
    total_combinations = 2 ** entropy_score
    
    # Calculate total seconds to guess every combination
    seconds = total_combinations / guesses_per_second
    
    # Convert seconds into a human readable format
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.2f} minutes"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.2f} hours"
    elif seconds < 31536000:
        days = seconds / 86400
        return f"{days:.2f} days"
    else:
        years = seconds / 31536000
        # The colon and comma automatically format large numbers (e.g., 1,000,000)
        return f"{round(years):,} years"

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

# print("We can move forward now!")
final_entropy = CalculateEntropy(password,142)
entropy_no_emojis = CalculateEntropy(password,92)
entropy_all_emojis = CalculateEntropy(password, 1492)
crack_time = CalculateCrackTime(final_entropy)
crack_time_no_emojis = CalculateCrackTime(entropy_no_emojis)
crack_time_all_emojis = CalculateCrackTime(entropy_all_emojis)


# Capture the length of the valid password
password_length = len(password)

# 1. Print a decorative header (Expanded to 92 characters to fit the new column)
print("\n" + "=" * 92)
print(f"{'PASSWORD SECURITY ANALYSIS':^92}")
print("=" * 92)

# 2. Print the table column titles
print(f"{'SCENARIO':<25} | {'LENGTH':<8} | {'ENTROPY (BITS)':<15} | {'ESTIMATED CRACK TIME':<35}")
print("-" * 92)

# 3. Print the data rows with the new length variable
print(f"{'Standard (No Emojis)':<25} | {password_length:<8} | {entropy_no_emojis:<15} | {crack_time_no_emojis:<35}")
print(f"{'Whitelist (50 Emojis)':<25} | {password_length:<8} | {final_entropy:<15} | {crack_time:<35}")
print(f"{'All Emojis (~1400)':<25} | {password_length:<8} | {entropy_all_emojis:<15} | {crack_time_all_emojis:<35}")

# 4. Print a closing border
print("=" * 92 + "\n")
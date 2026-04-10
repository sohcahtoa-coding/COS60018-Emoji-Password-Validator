# COS60018 Emoji Password Validator

Emoji Password Validator
This program prompts the user to create a password meeting strict criteria, including a minimum length, at least one number, at least one standard symbol, and at least one emoji.

Because complex emojis are not single characters, the tool will only accept emojis from a hardcoded whitelist of 50 safe, 'atomic' emojis. It will reject complex ones that use invisible joiners or skin tone modifiers.

How It Calculates Strength
Once a valid password is provided, the program will calculate the total possible combinations according to: character pool size ^ password length.

It will then output a clear estimate of exactly how long a high-end PC would take to crack the password by brute-force (100 billion tries per second). This calculated crack time should be seen as an "upper limit". To be accurate, each password character would need to be randomly generated from the pool with no enforced minimums. Also, as humans, we tend to add recognisable patterns to our passwords which generally reduces the strength.

Calculation Methodology
Previous versions of the code calculated Shannon's entropy (in bits) and then calculated total possible combinations by the formula 2^E.

Whilst perfectly valid, it added an unnecessary level of mathematical computation. Logarithmic calculations meant the maths library needed to be imported. Using the permutation method removed the requirement for the maths library and significantly simplified calculations whilst still obtaining the exact same result.

The 7-Character Minimum
The minimum password length is set to just seven characters. This was a deliberate choice to prove a point about how we calculate password strength.

By adding 50 emojis into the mix, the total pool of available characters expands massively. This mathematical jump in possible combinations (or entropy) shows that you can build highly secure, brute-force resistant passwords without forcing people to remember ridiculously long strings. It is all about balancing strong security with actual human usability.


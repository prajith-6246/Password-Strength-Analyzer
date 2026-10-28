import re
import secrets
import string


COMMON_PASSWORDS = {
    "password", "password123", "123456", "123456789", "qwerty",
    "admin", "letmein", "welcome", "iloveyou", "abc123"
}


def analyze_password(password):
    """Return a score, strength label, and improvement suggestions."""
    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters (12 or more is better).")

    if len(password) >= 12:
        score += 1
    else:
        suggestions.append("Make the password 12 characters or longer.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add lowercase letters (a-z).")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add uppercase letters (A-Z).")

    if re.search(r"\d", password):
        score += 1
    else:
        suggestions.append("Include at least one number (0-9).")

    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
    else:
        suggestions.append("Include a special character, such as !, @, or #.")

    if password.lower() in COMMON_PASSWORDS:
        score = 0
        suggestions.append("Avoid common passwords that attackers can easily guess.")

    # Check for repeated characters and simple sequences.
    if len(password) >= 3 and re.search(r"(.)\1\1", password):
        score = max(0, score - 1)
        suggestions.append("Avoid using the same character three or more times in a row.")

    if password.lower() in {"12345678", "abcdefgh", "qwerty123"}:
        score = max(0, score - 1)
        suggestions.append("Avoid predictable keyboard or number sequences.")

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    else:
        strength = "Strong"

    if not suggestions:
        suggestions.append("Good job! This password meets the basic checks.")

    return score, strength, suggestions


def generate_suggestion(length=16):
    """Generate a random password using a cryptographically secure generator."""
    if length < 12:
        length = 12

    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    # Guarantee that the generated password includes each character category.
    required = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*()-_=+"),
    ]

    remaining = [secrets.choice(alphabet) for _ in range(length - len(required))]
    password_chars = required + remaining
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def main():
    print("=== Password Strength Analyzer ===")
    password = input("Enter a password to analyze: ")

    score, strength, suggestions = analyze_password(password)

    print(f"\nStrength: {strength} ({score}/6)")
    print("Suggestions:")
    for suggestion in suggestions:
        print(f"- {suggestion}")

    if strength != "Strong":
        print("\nSuggested stronger password:")
        print(generate_suggestion())


if __name__ == "__main__":
    main()

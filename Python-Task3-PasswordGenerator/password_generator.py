import secrets
import string


def generate_password(length):
    if length < 4:
        raise ValueError("Password length must be at least 4.")

    uppercase = secrets.choice(string.ascii_uppercase)
    lowercase = secrets.choice(string.ascii_lowercase)
    digit = secrets.choice(string.digits)
    special = secrets.choice(string.punctuation)

    all_characters = (
        string.ascii_letters
        + string.digits
        + string.punctuation
    )

    remaining = ''.join(
        secrets.choice(all_characters)
        for _ in range(length - 4)
    )

    password_characters = (
        uppercase
        + lowercase
        + digit
        + special
        + remaining
    )

    password_characters = list(password_characters)

    secrets.SystemRandom().shuffle(password_characters)

    return ''.join(password_characters)
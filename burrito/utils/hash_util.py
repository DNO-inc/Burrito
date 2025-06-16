from random import SystemRandom

from argon2 import PasswordHasher

_hasher = PasswordHasher()


def get_hash(data: str, salt: bytes | None = None) -> str:
    """
    Return hash of the password

    Args:
        data (str): user password

    Returns:
        str: hashed password
    """

    return _hasher.hash(data.encode("utf-8"), salt=salt)


def compare_password(password: str, hashed_password: str) -> bool:
    """
    Return True if password is equal to hashed password

    Args:
        password (str): user password
        hashed_password (str): hashed password

    Returns:
        bool: compare result
    """

    try:
        return _hasher.verify(hashed_password, password)
    except Exception:
        return False


def generate_email_code() -> str:
    """
    Generate a random email code using /dev/urandom (Linux).
    The code is used to verify user's email.

    Returns:
        The generated email code as a string of 3 numbers
    """
    return str(SystemRandom().randint(1000, 9999))

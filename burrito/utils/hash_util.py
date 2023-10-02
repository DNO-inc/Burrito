from random import SystemRandom

from argon2 import PasswordHasher


_hasher = PasswordHasher()


def get_hash(data: str) -> str:
    """_summary_

    Return hash of the password

    Args:
        data (str): user password

    Returns:
        str: hashed password
    """

    return _hasher.hash(data.encode("utf-8"))


def compare_password(password: str, hashed_password: str) -> bool:
    """_summary_

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

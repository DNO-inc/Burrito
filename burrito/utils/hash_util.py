from hashlib import sha3_512


def get_hash(data: str) -> str:
    """Return hash of the password"""

    return sha3_512(
        data.encode("utf-8")
    ).hexdigest()


def compare_password(password: str, hashed_password: str):
    """Return True if password is equal to hashed password"""

    return get_hash(password) == hashed_password

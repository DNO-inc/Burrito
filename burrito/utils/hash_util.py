from hashlib import sha3_512


def get_salt() -> str:
    """Return salt"""

    return "od9fuM_JNsczxi6cEg4aTrSSprVcQSz3L9dwOsLhvi4-UtM4wtkwehh4QGIDMD2EYsvYyBiflMY5Bflhb7ReTOGgJgN_1fHp58xu1xFi5cEIXzEi1_VR9wz3XqWZx8o9Fsf0WBlX1lkJxt0OAB90BT5DsM1tShnTB7b8C6LPC3I"


def get_hash(data: str) -> str:
    """Return hash of the password"""

    return sha3_512(
        (get_salt() + data).encode("utf-8")
    ).hexdigest()


def compare_password(password: str, hashed_password: str) -> bool:
    """Return True if password is equal to hashed password"""

    return get_hash(password) == hashed_password

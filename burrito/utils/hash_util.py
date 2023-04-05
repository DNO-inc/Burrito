from hashlib import sha3_512
from random import SystemRandom


def get_salt() -> str:
    """_summary_

    Return salt

    Returns:
        str: encrypted salt
    """

    return "od9fuM_JNsczxi6cEg4aTrSSprVcQSz3L9dwOsLhvi4-UtM4wtkwehh4QGIDMD2EYsvYyBiflMY5Bflhb7ReTOGgJgN_1fHp58xu1xFi5cEIXzEi1_VR9wz3XqWZx8o9Fsf0WBlX1lkJxt0OAB90BT5DsM1tShnTB7b8C6LPC3I"


def get_hash(data: str) -> str:
    """_summary_

    Return hash of the password

    Args:
        data (str): user password

    Returns:
        str: hashed password
    """

    return sha3_512(
        (get_salt() + data).encode("utf-8")
    ).hexdigest()


def compare_password(password: str, hashed_password: str) -> bool:
    """_summary_

    Return True if password is equal to hashed password

    Args:
        password (str): user password
        hashed_password (str): hashed password

    Returns:
        bool: compare result
    """

    return get_hash(password) == hashed_password


def get_verification_code() -> str:
    """_summary_

    Generate and return email verification code

    Returns:
        str: verification code
    """

    return "".join([str(SystemRandom().randint(0, 9)) for i in range(6)])

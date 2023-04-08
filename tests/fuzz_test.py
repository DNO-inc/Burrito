import string
import random


def get_random_bytes(len_: int = 255) -> bytes:
    """_summary_

    Return random bytes value

    Args:
        len_ (int, optional): bytes count. Defaults to 255.

    Returns:
        bytes: data in bytes
    """

    return random.randbytes(len_)


def get_random_punctuation(len_: int = len(string.punctuation) // 2) -> str:
    """_summary_

    Args:
        len_ (int, optional): string length.
            Defaults to len(string.punctuation)//2.

    Returns:
        str: string contain only punctuation values
    """

    return "".join(random.choices(string.punctuation, k=len_))


def get_random_letters(len_: int = len(string.ascii_letters) // 2) -> str:
    """_summary_

    Args:
        len_ (int, optional): string length.
            Defaults to len(string.ascii_letters)//2.

    Returns:
        str: random ASCII letters
    """

    return "".join(random.choices(string.ascii_letters, k=len_))


def get_random_mixed(len_: int = 255) -> str:
    """_summary_

    Return random ASCII letter mixed with punctuation values

    Args:
        len_ (int, optional): string length. Defaults to 255.

    Returns:
        str: string with mixed values
    """

    data = list(
        get_random_punctuation(len_ // 2) + get_random_letters(len_ // 2)
    )
    random.shuffle(data)

    return "".join(data)


def get_random_with_quotes(len_: int = 255):
    """_summary_

    Args:
        len_ (int, optional): string length. Defaults to 255.

    Returns:
        _type_: string startswith quote
    """

    return "'" + get_random_mixed(len_)


def get_random_with_d_quotes(len_: int = 255):
    """_summary_

    Args:
        len_ (int, optional): string length. Defaults to 255.

    Returns:
        _type_: string startswith double quotes
    """

    return '"' + get_random_mixed(len_)


def get_random_data(len_: int = 255) -> str | bytes:
    """_summary_

    Returns:
        str | bytes: random data
    """

    return random.choice(
        [
            get_random_bytes,
            get_random_punctuation,
            get_random_letters,
            get_random_mixed,
            get_random_with_quotes,
            get_random_with_d_quotes
        ]
    )(len_)

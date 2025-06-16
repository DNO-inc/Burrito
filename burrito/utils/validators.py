import re


def is_valid_login(login: str) -> bool:
    """
    Return user's login if login is valid or return nothing

    Args:
        login (str): users login

    Returns:
        bool: is valid value
    """

    if not isinstance(login, str):
        return False

    if len(login) < 3 or len(login) > 40:
        return False

    pattern = r"^[\w_]*$"

    return bool(re.match(pattern, login))


def is_valid_email(email: str) -> bool:
    """
    Return user's email if email is valid or return nothing

    Args:
        login (str): users email

    Returns:
        bool: is valid value
    """

    if not isinstance(email, str):
        return False

    pattern = r"^[\w\._]*@\w+\.[a-z]*$"

    return bool(re.match(pattern, email))


def is_valid_password(password: str) -> bool:
    """
    Validate password by rules

    Args:
        password (str): user password

    Returns:
        bool: is valid value
    """

    if not isinstance(password, str):
        return False

    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
    return bool(re.match(pattern, password))


def is_valid_firstname(value: str) -> bool:
    if not isinstance(value, str):
        return False

    if len(value) < 2:
        return False

    return True

# TODO: use one function instead?


def is_valid_lastname(value: str) -> bool:
    if not isinstance(value, str):
        return False

    if len(value) < 2:
        return False

    return True


def is_valid_phone(value: str) -> bool:
    if not isinstance(value, str):
        return False
    pattern = r'^\+?[0-9\s\-\(\)]{5,20}$'
    return bool(re.match(pattern, value))

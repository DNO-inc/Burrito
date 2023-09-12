import re


def is_valid_login(login: str) -> bool:
    """_summary_

    Return user's login if login is valid or return nothing

    Args:
        login (str): users login

    Returns:
        bool: is valid value
    """

    if not isinstance(login, str):
        return False

    if len(login) < 3 or len(login) > 20:
        return False

    pattern = r"^[\w_]*$"

    if re.match(pattern, login):
        return True


def is_valid_email(email: str) -> bool:
    """_summary_

    Return user's email if email is valid or return nothing

    Args:
        login (str): users email

    Returns:
        bool: is valid value
    """

    if not isinstance(email, str):
        return False

    pattern = r"^[\w\._]*@\w+\.[a-z]*$"

    if re.match(pattern, email):
        return True


def is_valid_password(password: str) -> bool:
    """_summary_

    Validate password by rules

    Args:
        password (str): user password

    Returns:
        bool: is valid value
    """

    if not isinstance(password, str):
        return False

    if len(password) < 8:
        return False

    return True
#    pattern = ""

#    if re.match(pattern, password):
#        return password


def is_valid_firstname(value: str) -> bool:
    if not isinstance(value, str):
        return False

    if len(value) < 2:
        return False

    return True


def is_valid_lastname(value: str) -> bool:
    if not isinstance(value, str):
        return False

    if len(value) < 5:
        return False

    return True


def is_valid_phone(value: str) -> bool:
    if not isinstance(value, str):
        return False

    if len(value) < 5:
        return False

    return True

import re


def is_valid_login(login: str) -> str | None:
    """_summary_

    Return user's login if login is valid or return nothing

    Args:
        login (str): users login

    Returns:
        str | None: users login or None
    """

    if len(login) < 3:
        return

    pattern = r"^[\w_]*$"

    if re.match(pattern, login):
        return login


def is_valid_email(email: str) -> str | None:
    """_summary_

    Return user's email if email is valid or return nothing

    Args:
        login (str): users email

    Returns:
        str | None: users email or None
    """

    pattern = r"^[\w\._]*@\w+\.[a-z]*$"

    if re.match(pattern, email):
        return email


def is_valid_password(password: str) -> str | None:
    """_summary_

    Validate password by rules

    Args:
        password (str): user password

    Returns:
        str | None: password or nothing
    """

    if len(password) < 8:
        return

    pattern = ""

    if re.match(pattern, password):
        return password

from fastapi import HTTPException, status

from burrito.utils.logger import get_logger
from burrito.utils.transliteration import transliterate
from burrito.utils.converter import GroupConverter, FacultyConverter
from burrito.utils.query_util import MIN_ADMIN_PRIORITY, MIN_CHIEF_ADMIN_PRIORITY

from burrito.schemas.registration_schema import RegistrationSchema

from burrito.models.roles_model import Roles
from burrito.models.user_model import Users


def create_user(
    user_data: RegistrationSchema
) -> Users:
    """_summary_

    Create user with default fields: (login, hashed_password)

    Args:
        login (str): user login
        hashed_password (str): user hashed password

    Returns:
        bool: status creating new user
    """

    role_object: Roles = Roles.get(Roles.name == "USER_ALL")

    # check if provided group/faculty is exist
    if user_data.group is not None:
        GroupConverter.convert(user_data.group)
    FacultyConverter.convert(user_data.faculty)

    try:
        user: Users = Users.create(
            firstname=user_data.firstname,
            lastname=user_data.lastname,
            login=user_data.login,
            password=user_data.password,  # password already hashed by argon2
            group=user_data.group,
            faculty=user_data.faculty,
            phone=user_data.phone,
            email=user_data.email,
            role=role_object
        )
        return user

    except Exception as e:  # pylint: disable=broad-except, invalid-name
        get_logger().info(
            f"""
                login: {user_data.login}
                group: {user_data.group}
                faculty: {user_data.faculty}
                role: {role_object.name}

            """
        )
        get_logger().error(e, exc_info=True)


def create_user_with_cabinet(
    cabinet_id: int,
    cabinet_id_new: str,
    firstname: str,
    lastname: str,
    faculty: int,
    group: int,
    email: int,
) -> Users | None:

    role_object: Roles = Roles.get(Roles.name == "USER_ALL")

    tmp_user_login = transliterate(f"{firstname} {cabinet_id}")

    # TODO: tmp solution, i hope. Assign a `global' faculty to the user if it fails to create
    for i in range(3):
        try:
            user: Users = Users.create(
                cabinet_id=cabinet_id,
                cabinet_id_new=cabinet_id_new,
                firstname=firstname,
                lastname=lastname,
                login=tmp_user_login,
                faculty=faculty if not i else 1,
                group=group if i != 2 else None,
                email=email,
                role=role_object
            )
            return user

        except Exception as e:
            get_logger().error(e)
            get_logger().warning(
                f"""
                Firstname {firstname}
                Lastname {lastname}
                Email {email}
                Login {tmp_user_login}
                Faculty {faculty}
                Group {group}

                """
            )


def get_user_by_login(login: str) -> Users | None:
    """_summary_

    Get user if exist or return None

    Args:
        login (str): user login

    Returns:
        Users | None: return None if user is not exist
    """

    return Users.get_or_none(Users.login == login)


def get_user_by_email_or_none(email: str) -> Users | None:
    """
    Get user if exist or return None

    Args:
        email (str): user email

    Returns:
        Users | None: return None if user is not exist
    """

    return Users.get_or_none(Users.email == email)


def get_user_by_id(user_id: int) -> Users | None:
    """_summary_

    Get user if exist or return None

    Args:
        user_id (int): user id

    Returns:
        Users | None: return None if user is not exist
    """

    _current_user = Users.get_or_none(Users.user_id == user_id)

    if not _current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID ({user_id}) is not exist"
        )

    return _current_user


def get_user_by_id_or_none(user_id: int) -> Users | None:
    """_summary_

    Get user if exist or return None

    Args:
        user_id (int): user id

    Returns:
        Users | None: return None if user is not exist
    """

    return Users.get_or_none(Users.user_id == user_id)


def get_user_by_cabinet_id(cabinet_id: int) -> Users | None:
    """_summary_

    Get user by cabinet ID

    Args:
        cabinet_id (int): user's ID in SSU cabinet

    Returns:
        Users | None: return None if user is not exist
    """

    return Users.get_or_none(Users.cabinet_id == cabinet_id)


def is_admin(user: int | Users) -> bool:
    if isinstance(user, int):
        user = get_user_by_id(user)

    return user.role.priority >= MIN_ADMIN_PRIORITY


def is_chief_admin(user: int | Users) -> bool:
    if isinstance(user, int):
        user = get_user_by_id(user)

    return user.role.priority >= MIN_CHIEF_ADMIN_PRIORITY

from typing import Any

import requests
import jsonschema

from burrito.utils.users_util import (
    get_user_by_email_or_none,
    create_user,
    RegistrationSchema
)
from burrito.utils.hash_util import get_hash
from burrito.utils.config_reader import get_config


def setup_test_user() -> int:
    user = get_user_by_email_or_none("")
    if not user:
        user = create_user(
            RegistrationSchema(
                firstname="test",
                lastname="test",
                login="test",
                password=get_hash("qwertyuiop"),
                faculty=414,
                email=""
            )
        )

    return user.user_id


def get_token_pare() -> dict[str, Any]:
    response = requests.post(
        f"http://{get_config().BURRITO_HOST}:{get_config().BURRITO_PORT}/auth/password/login",
        json={
            "login": "test",
            "password": "qwertyuiop"
        },
        timeout=5
    )

    assert response.status_code == 200

    _response_schema = {
        "type": "object",
        "properties": {
            "user_id": {"type": "number"},
            "login": {"type": "string"},
            "access_token": {"type": "string"},
            "refresh_token": {"type": "string"}
        },
        "required": ["user_id", "login", "access_token", "refresh_token"]
    }

    response_instance = response.json()

    jsonschema.validate(response_instance, _response_schema)

    return response.json()


def get_access_token() -> str:
    return get_token_pare()["access_token"]


def get_refresh_token() -> str:
    return get_token_pare()["refresh_token"]


setup_test_user()

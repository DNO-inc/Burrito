
from burrito.utils.hash_util import get_hash
from burrito.utils.db_utils import create_user_tmp_foo


users = [
    {
        "login": "login",
        "hashed_password": get_hash("password"),
        "group": 1,
        "faculty": 1
    },
    {
        "login": "login2",
        "hashed_password": get_hash("password2"),
        "group": 2,
        "faculty": 2
    }
]


for user in users:
    create_user_tmp_foo(**user)

print("\nTest users was created...")

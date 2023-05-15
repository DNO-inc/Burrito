
from burrito.utils.hash_util import get_hash
from burrito.utils.db_utils import create_user_tmp_foo


users = [
    {
        "login": "login",
        "hashed_password": get_hash("password"),
        "group": "IT-11",
        "faculty": "EliT"
    },
    {
        "login": "login2",
        "hashed_password": get_hash("password2"),
        "group": "LOL-11",
        "faculty": "Biem"
    }
]


for user in users:
    create_user_tmp_foo(**user)

print("\nTest users was created...")

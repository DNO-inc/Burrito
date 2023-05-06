
from burrito.utils.hash_util import get_hash
from burrito.utils.db_utils import create_user


login = "login"
password = "password"

create_user(login, get_hash(password))

print("\nTest user was created:")
print(f"\t[+] Tmp login: {login}")
print(f"\t[+] Tmp password: {password}")

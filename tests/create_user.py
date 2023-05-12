
from burrito.utils.hash_util import get_hash
from burrito.utils.db_utils import create_user_tmp_foo


login = "login"
password = "password"

create_user_tmp_foo(login, get_hash(password), 1, 1)

print("\nTest user was created:")
print(f"\t[+] Tmp login: {login}")
print(f"\t[+] Tmp password: {password}")


from hashlib import sha3_512



def get_hash(data: str) -> str:
    return sha3_512(
        data.encode("utf-8")
    ).hexdigest()

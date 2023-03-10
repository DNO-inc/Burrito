
import requests



data = requests.post("http://localhost:8000/account")
print(data.json())

data = requests.post(
    "http://localhost:8000/auth/password/login",
    json={"login": "test", "password": "test"}
)
access_token = data.json().get("access_token")
print(data.json())

data = requests.post(
    "http://localhost:8000/account",
    headers={
        "Authorization": f"Bearer {access_token}"
    }
)
print(data.json())

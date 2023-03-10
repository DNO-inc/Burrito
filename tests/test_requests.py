
import requests


data = requests.get("http://localhost:8000/user")
print(data.json())

data = requests.post(
    "http://localhost:8000/login",
    json={"username": "test", "password": "test"}

)
access_token = data.json().get("access_token")
print(data.json())

data = requests.get(
    "http://localhost:8000/user",
    headers={
        "Authorization": f"Bearer {access_token}"
    }
)
print(data.json())

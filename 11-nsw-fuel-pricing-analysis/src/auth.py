import requests
from config import TOKEN_URL, AUTH_HEADER


def get_access_token():
    headers = {"Authorization": AUTH_HEADER}
    resp = requests.get(TOKEN_URL, headers=headers)
    resp.raise_for_status()
    return resp.json()["access_token"]


if __name__ == "__main__":
    token = get_access_token()
    print(f"Got token: {token[:10]}...")

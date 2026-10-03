import requests
from config.settings import API_URL


class AuthClient:
    def login(self, email: str, password: str) -> requests.Response:
        return requests.post(
            f"{API_URL}/users/login",
            json={"email": email, "password": password},
            timeout=15,
        )

    def get_token(self, email: str, password: str) -> str:
        response = self.login(email, password)
        response.raise_for_status()
        return response.json()["access_token"]
    def get_profile(self, token: str) -> dict:
        response = requests.get(
            f"{API_URL}/users/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=15,
        )
        response.raise_for_status()
        return response.json()
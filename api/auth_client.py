import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.settings import API_URL


class AuthClient:
    def __init__(self):
        self.session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=1,
            allowed_methods=None,  # повторять и POST
            status_forcelist=[502, 503, 504],
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retry))
    def register(self, user: dict) -> requests.Response:
        return self.session.post(
            f"{API_URL}/users/register",
            json=user,
            timeout=(10, 30),
        )

    def login(self, email: str, password: str) -> requests.Response:
        return self.session.post(
            f"{API_URL}/users/login",
            json={"email": email, "password": password},
            timeout=(10, 30),
        )

    def get_token(self, email: str, password: str) -> str:
        response = self.login(email, password)
        response.raise_for_status()
        return response.json()["access_token"]
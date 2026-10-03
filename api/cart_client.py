import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.settings import API_URL


class CartClient:
    def __init__(self, token: str):
        self.session = requests.Session()
        retry = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retry))
        self.session.headers["Authorization"] = f"Bearer {token}"

    def create_cart(self) -> str:
        response = self.session.post(f"{API_URL}/carts", json={}, timeout=(10, 30))
        response.raise_for_status()
        return response.json()["id"]

    def add_item(self, cart_id: str, product_id: str, quantity: int = 1) -> None:
        response = self.session.post(
            f"{API_URL}/carts/{cart_id}",
            json={"product_id": product_id, "quantity": quantity},
            timeout=(10, 30),
        )
        response.raise_for_status()
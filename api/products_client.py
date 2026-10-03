import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config.settings import API_URL


class ProductsClient:
    def __init__(self):
        self.session = requests.Session()
        retry = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retry))

    def get_products(self, page: int = 1, sort: str | None = None) -> requests.Response:
        params = {"page": page}
        if sort:
            params["sort"] = sort
        return self.session.get(f"{API_URL}/products", params=params, timeout=(10, 30))

    def get_product(self, product_id: str) -> requests.Response:
        return self.session.get(f"{API_URL}/products/{product_id}", timeout=(10, 30))

    def get_all_products(self, sort: str | None = None) -> list[dict]:
        first = self.get_products(1, sort).json()
        items = list(first["data"])
        for page in range(2, first["last_page"] + 1):
            items += self.get_products(page, sort).json()["data"]
        return items
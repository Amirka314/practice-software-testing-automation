import re
from playwright.sync_api import Page
from config.settings import API_URL
from pages.base_page import BasePage


class HomePage(BasePage):
    path = "/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.search_input = page.get_by_test_id("search-query")
        self.search_button = page.get_by_test_id("search-submit")
        self.sort_select = page.get_by_test_id("sort")
        self.product_cards = page.locator("a.card")
        self.product_names = page.get_by_test_id("product-name")
        self.product_prices = page.get_by_test_id("product-price")
        self.no_results = page.get_by_test_id("no-results")

    # pages/home_page.py

    def search(self, query: str) -> list[str]:
        self.search_input.fill(query)

        # Фильтруем строго по запросу поиска search?q=
        with self.page.expect_response(
                lambda r: "/products/search" in r.url and r.status == 200
        ) as response_info:
            self.search_button.click()

        response = response_info.value
        data = response.json()

        # Возвращаем имена товаров из ответа бэкенда
        return [item["name"] for item in data.get("data", [])]

    def sort_by(self, label: str) -> list[str]:
        old_names = self.get_product_names()
        self.sort_select.select_option(label=label)
        return old_names

    def filter_by_category(self, name: str) -> list[str]:
        with self.page.expect_response(
                lambda r: r.url.startswith(f"{API_URL}/products")
                          and r.request.method in ("QUERY", "GET")
                          and "/products/search" not in r.url
                          and r.status == 200
        ) as response_info:
            self.page.get_by_label(name, exact=True).check()
        data = response_info.value.json().get("data", [])
        return [p["name"] for p in data]

    def get_product_names(self) -> list[str]:
        return [t.strip() for t in self.product_names.all_inner_texts()]

    def get_product_prices(self) -> list[float]:
        return [
            float(re.sub(r"[^\d.]", "", t))
            for t in self.product_prices.all_inner_texts()
        ]

    def open_product(self, name: str):
        self.product_names.filter(has_text=name).first.click()
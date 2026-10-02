import re
from playwright.sync_api import Page
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
        self.search_caption = page.get_by_test_id("search_completed")
        self.no_results = page.get_by_test_id("no-results")

    def search(self, query: str):
        self.search_input.fill(query)
        with self.page.expect_response(lambda r: "/products" in r.url and r.status == 200):
            self.search_button.click()

    def sort_by(self, label: str):
        with self.page.expect_response(lambda r: "/products" in r.url and r.status == 200):
            self.sort_select.select_option(label=label)

    def filter_by_category(self, name: str):
        # Ожидаем запрос к /products при клике на чекбокс категории
        with self.page.expect_response(lambda r: "/products" in r.url and r.status == 200):
            self.page.get_by_label(name, exact=True).check()

    def get_product_names(self) -> list[str]:
        return [t.strip() for t in self.product_names.all_inner_texts()]

    def get_product_prices(self) -> list[float]:
        return [
            float(re.sub(r"[^\d.]", "", t))
            for t in self.product_prices.all_inner_texts()
        ]

    def open_product(self, name: str):
        self.product_names.filter(has_text=name).first.click()
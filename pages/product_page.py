from playwright.sync_api import Page

from config.settings import API_URL
from pages.base_page import BasePage


class ProductPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.name = page.get_by_test_id("product-name")
        self.price = page.get_by_test_id("unit-price")
        self.quantity_input = page.get_by_test_id("quantity")
        self.add_to_cart_button = page.get_by_test_id("add-to-cart")
        self.add_to_cart_toast = page.get_by_role("alert")

    def add_to_cart(self, quantity: int = 1):
        if quantity != 1:
            self.quantity_input.fill(str(quantity))

        with self.page.expect_response(
            lambda r: f"{API_URL}/carts" in r.url and r.request.method in ("POST", "PUT") and r.status in (200, 201)
        ):
            self.add_to_cart_button.click()
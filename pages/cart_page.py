
import re

from playwright.sync_api import Page

from pages.base_page import BasePage

class CartPage(BasePage):
    path = "/checkout"

    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_icon = page.get_by_test_id("nav-cart")
        self.cart_quantity_badge = page.get_by_test_id("cart-quantity")
        self.product_titles = page.get_by_test_id("product-title")
        self.product_quantities = page.get_by_test_id("product-quantity")
        self.product_prices = page.get_by_test_id("product-price")
        self.line_prices = page.get_by_test_id("line-price")
        self.cart_total = page.get_by_test_id("cart-total")
        self.delete_buttons = page.locator("a.btn-danger")
        self.proceed_button = page.get_by_test_id("proceed-1")
        # Алиасы для единообразия с тестами checkout
        self.item_titles = self.product_titles
        self.item_quantities = self.product_quantities
        self.unit_prices = self.product_prices
        self.total = self.cart_total
        self.cart_badge = self.cart_quantity_badge

    def open_via_icon(self):
        self.cart_icon.click()

    def open_from_header(self):
        self.cart_icon.click()

    def get_product_titles(self) -> list[str]:
        return [t.strip() for t in self.product_titles.all_inner_texts()]

    def delete_first_item(self):
        self.delete_buttons.first.click()

    @staticmethod
    def to_number(price_str: str) -> float:
        return float(re.sub(r"[^\d.]", "", price_str))

    def update_quantity(self, index: int, quantity: int):
        input_element = self.product_quantities.nth(index)
        input_element.fill(str(quantity))
        input_element.press("Enter")
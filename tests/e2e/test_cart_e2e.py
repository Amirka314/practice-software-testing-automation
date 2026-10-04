import allure
import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.home_page import HomePage


@allure.feature("E2E")
class TestCartE2E:

    @allure.story("Cart prepared via API")
    @allure.title("Корзина, созданная через API, корректно отображается в UI")
    @pytest.mark.smoke
    @pytest.mark.e2e
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cart_created_via_api_is_shown_in_ui(
        self, cart_with_product, page, home_page: HomePage, cart_page: CartPage
    ):
        product = cart_with_product["product"]
        quantity = cart_with_product["quantity"]

        with allure.step("Открыть главную с корзиной, подготовленной через API"):
            home_page.open()
            expect(home_page.product_names.first).to_be_visible()

        with allure.step("Открыть корзину"):
            cart_page.open_from_header()

        with allure.step("Проверить товар и количество"):
            expect(cart_page.item_titles).to_have_text([product["name"]])
            expect(cart_page.item_quantities).to_have_value(str(quantity))

        with allure.step("Проверить итоговую сумму"):
            expected_total = f"${product['price'] * quantity:.2f}"
            expect(cart_page.total).to_contain_text(expected_total)
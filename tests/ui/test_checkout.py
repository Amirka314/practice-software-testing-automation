import re

import allure
import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.product_page import ProductPage

BILLING = {
    "country": "Germany",
    "postal_code": "10115",
    "house_number": "42",
}


@allure.feature("Checkout")
class TestCheckout:

    @allure.story("Purchase")
    @allure.title("Полный путь покупки: оплата наличными")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_purchase_cash_on_delivery(self, logged_in_page, home_page: HomePage,
                                       product_page: ProductPage, cart_page: CartPage,
                                       checkout_page: CheckoutPage):

        with allure.step("Добавить товар в корзину"):
            home_page.open()
            expect(home_page.product_names.first).to_be_visible()
            home_page.open_product(home_page.get_product_names()[0])
            expect(product_page.add_to_cart_button).to_be_enabled()
            product_page.add_to_cart()
            expect(product_page.add_to_cart_toast.first).to_be_visible()

        with allure.step("Открыть корзину и перейти к оформлению"):
            cart_page.open_from_header()
            expect(cart_page.item_titles).to_have_count(1)
            checkout_page.proceed_from_cart()

        with allure.step("Пройти шаг Sign in"):
            expect(checkout_page.proceed_from_sign_in_button).to_be_visible()
            checkout_page.proceed_from_sign_in()

        with allure.step("Заполнить адрес"):
            expect(checkout_page.country).to_be_visible()
            checkout_page.country.select_option(label=BILLING["country"])
            expect(checkout_page.country).to_have_value("DE")
            checkout_page.fill_billing(**BILLING)
            expect(checkout_page.country).to_have_value("DE")
            expect(checkout_page.proceed_from_billing_button).to_be_enabled(timeout=15000)
            checkout_page.proceed_from_billing()

        with allure.step("Выбрать оплату наличными и подтвердить"):
            expect(checkout_page.payment_method).to_be_visible()
            checkout_page.select_payment("Cash on Delivery")
            checkout_page.confirm_payment()
            expect(checkout_page.payment_success_message).to_be_visible()

        with allure.step("Оформить заказ"):
            checkout_page.place_order()
            expect(checkout_page.order_confirmation).to_be_visible()
            assert re.fullmatch(r"INV-\d+", checkout_page.get_invoice_number())
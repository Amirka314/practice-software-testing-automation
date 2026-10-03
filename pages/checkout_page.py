import re

from playwright.sync_api import Page

from pages.base_page import BasePage
from config.settings import API_URL

class CheckoutPage(BasePage):
    path = "/checkout"

    def __init__(self, page: Page):
        super().__init__(page)
        # Шаги мастера
        self.proceed_from_cart_button = page.get_by_test_id("proceed-1")
        self.proceed_from_sign_in_button = page.get_by_test_id("proceed-2")
        self.proceed_from_billing_button = page.get_by_test_id("proceed-3")
        # Адрес
        self.street = page.get_by_test_id("street")  # проверить в DevTools
        self.city = page.get_by_test_id("city")
        self.state = page.get_by_test_id("state")
        self.country = page.get_by_test_id("country")
        self.postal_code = page.get_by_test_id("postal_code")
        self.house_number = page.get_by_test_id("house_number")
        # Оплата
        self.payment_method = page.get_by_test_id("payment-method")
        self.card_number = page.get_by_test_id("credit_card_number")
        self.card_expiry = page.get_by_test_id("expiration_date")
        self.card_cvv = page.get_by_test_id("cvv")
        self.card_holder = page.get_by_test_id("card_holder_name")
        self.finish_button = page.get_by_test_id("finish")
        self.payment_success_message = page.get_by_test_id("payment-success-message")
        # Подтверждение заказа (по тексту, пока нет data-test)
        self.order_confirmation = page.get_by_text(re.compile(r"Your invoice number is"))

    def proceed_from_cart(self):
        self.proceed_from_cart_button.click()

    def proceed_from_sign_in(self):
        self.proceed_from_sign_in_button.click()

    def fill_billing(self, country: str, postal_code: str, house_number: str,
                     street: str = "", city: str = "", state: str = ""):
        self.country.select_option(label=country)
        self.postal_code.fill(postal_code)
        self.house_number.fill(house_number)
        self.house_number.press("Tab")  # запускает автозаполнение и валидацию
        if street:
            self.street.fill(street)
        if city:
            self.city.fill(city)
        if state:
            self.state.fill(state)

    def proceed_from_billing(self):
        self.proceed_from_billing_button.click()

    def select_payment(self, label: str):
        self.payment_method.select_option(label=label)

    def fill_card(self, number: str, expiry: str, cvv: str, holder: str):
        self.card_number.fill(number)
        self.card_expiry.fill(expiry)
        self.card_cvv.fill(cvv)
        self.card_holder.fill(holder)

    def click_confirm(self):
        self.finish_button.click()

    def get_invoice_number(self) -> str:
        match = re.search(r"INV-\d+", self.order_confirmation.inner_text())
        return match.group(0) if match else ""

    def confirm_payment(self):
        with self.page.expect_response(
            lambda r: "/payment/check" in r.url and r.request.method == "POST",
            timeout=10000,
        ):
            self.finish_button.click()

    def place_order(self):
        with self.page.expect_response(
            lambda r: r.url.startswith(f"{API_URL}/invoices")
            and r.request.method == "POST",
            timeout=10000,
        ) as response_info:
            self.finish_button.click()
        return response_info.value


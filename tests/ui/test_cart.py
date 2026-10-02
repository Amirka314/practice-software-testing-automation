import allure
import pytest
from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.product_page import ProductPage


@allure.feature("Cart")
class TestCart:

    @allure.story("Add to cart")
    @allure.title("Добавление товара в корзину из карточки")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_add_product_to_cart(
        self, logged_in_page: Page, home_page: HomePage, product_page: ProductPage, cart_page: CartPage
    ):
        with allure.step("Открыть каталог и зайти в первый товар"):
            home_page.open()
            expect(home_page.product_names.first).to_be_visible()
            product_name = home_page.get_product_names()[0]
            home_page.open_product(product_name)

        with allure.step("Добавить товар в корзину"):
            product_page.add_to_cart(quantity=1)
            expect(cart_page.cart_quantity_badge).to_have_text("1")

        with allure.step("Перейти в корзину и проверить состав"):
            cart_page.open_via_icon()
            expect(cart_page.product_titles.first).to_contain_text(product_name)

    @allure.story("Remove from cart")
    @allure.title("Удаление товара из корзины")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_remove_product_from_cart(
        self, logged_in_page: Page, home_page: HomePage, product_page: ProductPage, cart_page: CartPage
    ):
        with allure.step("Открыть каталог и добавить товар"):
            home_page.open()
            expect(home_page.product_names.first).to_be_visible()
            product_name = home_page.get_product_names()[0]
            home_page.open_product(product_name)
            product_page.add_to_cart(quantity=1)

        with allure.step("Перейти в корзину и удалить товар"):
            cart_page.open_via_icon()
            expect(cart_page.product_titles.first).to_contain_text(product_name)
            cart_page.delete_first_item()

        with allure.step("Проверить, что корзина пуста"):
            expect(cart_page.product_titles).to_have_count(0)

    @allure.story("Totals")
    @allure.title("Итоговая сумма равна цена x количество")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_cart_total_matches_quantity(
        self, logged_in_page: Page, home_page: HomePage, product_page: ProductPage, cart_page: CartPage
    ):
        with allure.step("Добавить товар в корзину"):
            home_page.open()
            expect(home_page.product_names.first).to_be_visible()
            home_page.open_product(home_page.get_product_names()[0])
            expect(product_page.add_to_cart_button).to_be_enabled()
            product_page.add_to_cart()
            expect(product_page.add_to_cart_toast.first).to_be_visible()

        with allure.step("Открыть корзину и изменить количество на 3"):
            cart_page.open_via_icon()
            expect(cart_page.product_titles).to_have_count(1)
            expect(cart_page.product_prices.first).to_be_visible()
            unit_price = cart_page.to_number(cart_page.product_prices.first.inner_text())
            cart_page.update_quantity(0, 3)

        with allure.step("Проверить итоговую сумму"):
            expected_total = f"{unit_price * 3:.2f}"
            expect(cart_page.cart_total).to_contain_text(expected_total)
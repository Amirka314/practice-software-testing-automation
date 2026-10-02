import allure
import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage


@allure.feature("Authentication")
@allure.story("API login")
@allure.title("API-логин авторизует пользователя в браузере")
@pytest.mark.smoke
@pytest.mark.ui
def test_logged_in_page_is_authorized(logged_in_page: Page, home_page: HomePage):
    with allure.step("Открыть главную страницу с предустановленным токеном"):
        home_page.open()

    with allure.step("Проверить, что пользователь авторизован в UI"):
        expect(logged_in_page.get_by_test_id("nav-menu")).to_be_visible()
        expect(logged_in_page.get_by_test_id("nav-sign-in")).to_have_count(0)
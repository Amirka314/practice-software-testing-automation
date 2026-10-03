import re
import allure
import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage

@allure.feature("Authentication")
@allure.story("Login")
class TestLogin:

    @allure.title("Успешный вход с валидными данными")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_successful_login(self, login_page: LoginPage, page: Page, test_user: dict):
        with allure.step("Открыть страницу логина"):
            login_page.open()
        with allure.step("Ввести валидные данные и отправить форму"):
            login_page.login(test_user["email"], test_user["password"])
        with allure.step("Проверить переход на страницу аккаунта"):
            expect(page).to_have_url(re.compile(r"/account"))

    @allure.title("Вход с неверными данными: {case}")
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.parametrize(
        "email,password,error_field,expected,case",
        [
            ("", "", "email_error", "Email is required", "пустой email"),
            ("", "", "password_error", "Password is required", "пустой пароль"),
            ("nouser@example.com", "wrong_password", "error_message",
             "Invalid email or password", "несуществующий пользователь"),
        ],
        ids=["empty_email", "empty_password", "unknown_user"],
    )
    def test_login_negative(self, login_page: LoginPage, email, password, error_field, expected, case):
        with allure.step("Открыть страницу логина"):
            login_page.open()
        with allure.step(f"Попытка входа: {case}"):
            login_page.login(email, password)
        with allure.step(f"Проверить сообщение об ошибке: {expected}"):
            expect(getattr(login_page, error_field)).to_have_text(expected)
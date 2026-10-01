import re
import allure
import pytest
from playwright.sync_api import Page, expect
from config.settings import TEST_USER_EMAIL, TEST_USER_PASSWORD
from pages.login_page import LoginPage

@allure.feature("Authentication")
@allure.story("Login")
class TestLogin:
    @allure.title("Успешный вход с валидными данными")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_successful_login(self, login_page: LoginPage, page: Page):
        with allure.step("Открыть страницу логина"):
            login_page.open()
        with allure.step("Ввести валидные данные и отправить форму"):
            login_page.login(TEST_USER_EMAIL, TEST_USER_PASSWORD)
        with allure.step("Проверить переход на страницу аккаунта"):
            expect(page).to_have_url(re.compile(r"/account"))

    @allure.title("Ошибка при отправке пустой формы")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_login_empty_fields(self, login_page: LoginPage):
        with allure.step("Открыть страницу логина"):
            login_page.open()
        with allure.step("Отправить пустую форму"):
            login_page.login("", "")
        with allure.step("Проверить тексты ошибок валидации под полями"):
            expect(login_page.email_error).to_be_visible()
            expect(login_page.email_error).to_have_text("Email is required")
            expect(login_page.password_error).to_be_visible()
            expect(login_page.password_error).to_have_text("Password is required")

    @allure.title("Вход с неверными данными: {case}")
    @pytest.mark.regression
    @pytest.mark.ui
    @pytest.mark.parametrize(
        "email,password,case",
        [
            ("nouser@example.com", "wrong_password", "несуществующий пользователь"),
            (TEST_USER_EMAIL, "wrong_password", "неверный пароль"),
        ],
        ids=["unknown_user", "wrong_password"],
    )
    def test_invalid_credentials(self, login_page: LoginPage, email, password, case):
        with allure.step("Открыть страницу логина"):
            login_page.open()
        with allure.step(f"Попытка входа: {case}"):
            login_page.login(email, password)
        with allure.step("Проверить появление общего сообщения об ошибке"):
            expect(login_page.error_message).to_be_visible()
            expect(login_page.error_message).to_have_text("Invalid email or password")
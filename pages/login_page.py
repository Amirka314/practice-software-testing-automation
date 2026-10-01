from playwright.sync_api import Page
from pages.base_page import BasePage

class LoginPage(BasePage):
    path = "/auth/login"

    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = page.get_by_test_id("email")
        self.password_input = page.get_by_test_id("password")
        self.submit_button = page.get_by_test_id("login-submit")
        self.error_message = page.get_by_test_id("login-error")
        # Новые локаторы ошибок валидации под полями
        self.email_error = page.get_by_test_id("email-error")
        self.password_error = page.get_by_test_id("password-error")

    def login(self, email: str, password: str):
        if email:
            self.email_input.fill(email)
        else:
            self.email_input.clear()

        if password:
            self.password_input.fill(password)
        else:
            self.password_input.clear()

        self.submit_button.click()
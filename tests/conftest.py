import pytest
from playwright.sync_api import Playwright, Page
from pages.login_page import LoginPage

@pytest.fixture(scope="session", autouse=True)
def set_test_id_attribute(playwright: Playwright):
    """Настраиваем Playwright искать data-test вместо data-testid"""
    playwright.selectors.set_test_id_attribute("data-test")

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Фикстура для передачи LoginPage в тесты"""
    return LoginPage(page)
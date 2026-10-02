import pytest
from playwright.sync_api import Page, Playwright
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.product_page import ProductPage

@pytest.fixture(scope="session", autouse=True)
def set_test_id_attribute(playwright: Playwright):
    playwright.selectors.set_test_id_attribute("data-test")

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)

@pytest.fixture
def home_page(page: Page) -> HomePage:
    return HomePage(page)

@pytest.fixture
def product_page(page: Page) -> ProductPage:
    return ProductPage(page)
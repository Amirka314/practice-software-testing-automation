import pytest
from playwright.sync_api import Page, Playwright

from api.auth_client import AuthClient
from config.settings import TEST_USER_EMAIL, TEST_USER_PASSWORD
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
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


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)


@pytest.fixture
def auth_token() -> str:
    return AuthClient().get_token(TEST_USER_EMAIL, TEST_USER_PASSWORD)


@pytest.fixture
def logged_in_page(context, page: Page, auth_token: str) -> Page:
    context.add_init_script(
        f"window.localStorage.setItem('auth-token', '{auth_token}');"
    )
    return page
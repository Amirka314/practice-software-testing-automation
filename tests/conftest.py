from pathlib import Path

import pytest
from playwright.sync_api import Page, Playwright

from api.auth_client import AuthClient
from api.cart_client import CartClient
from api.products_client import ProductsClient
from config.settings import API_URL, BASE_URL
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from utils.user_factory import build_user


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-infobars",
            "--disable-dev-shm-usage",
        ],
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "locale": "en-US",
    }


@pytest.fixture(scope="session", autouse=True)
def set_test_id_attribute(playwright: Playwright):
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def test_user() -> dict:
    user = build_user()
    response = AuthClient().register(user)
    assert response.status_code == 201, response.text
    return {"email": user["email"], "password": user["password"]}


@pytest.fixture
def auth_token(test_user: dict) -> str:
    return AuthClient().get_token(test_user["email"], test_user["password"])


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
def logged_in_page(context, page: Page, auth_token: str) -> Page:
    context.add_init_script(
        f"window.localStorage.setItem('auth-token', '{auth_token}');"
    )
    return page


@pytest.fixture
def cart_with_product(context, page: Page, auth_token: str) -> dict:
    """Корзина с товаром, созданная через API и подсунутая в браузер."""
    product = ProductsClient().get_products().json()["data"][0]
    quantity = 2

    cart = CartClient(auth_token)
    cart_id = cart.create_cart()
    cart.add_item(cart_id, product["id"], quantity)

    context.add_init_script(
        f"window.localStorage.setItem('auth-token', '{auth_token}');"
        f"window.sessionStorage.setItem('cart_id', '{cart_id}');"
        f"window.sessionStorage.setItem('cart_quantity', '{quantity}');"
    )
    return {"product": product, "quantity": quantity}


def pytest_sessionfinish(session, exitstatus):
    results = Path("allure-results")
    results.mkdir(exist_ok=True)
    (results / "environment.properties").write_text(
        "Browser=Chromium\n"
        f"Base_URL={BASE_URL}\n"
        f"API_URL={API_URL}\n"
        "Language=Python\n"
        "Framework=Pytest + Playwright\n",
        encoding="utf-8",
    )
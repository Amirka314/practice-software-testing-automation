import pytest
from playwright.sync_api import Page, Playwright
from api.cart_client import CartClient
from api.products_client import ProductsClient
from api.auth_client import AuthClient

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from api.auth_client import AuthClient
from utils.user_factory import build_user

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
@pytest.fixture(scope="session")
def test_user() -> dict:
    user = build_user()
    response = AuthClient().register(user)
    assert response.status_code == 201, response.text
    return {"email": user["email"], "password": user["password"]}


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
def auth_token(test_user: dict) -> str:
    return AuthClient().get_token(test_user["email"], test_user["password"])


@pytest.fixture
def logged_in_page(context, page: Page, auth_token: str) -> Page:
    context.add_init_script(
        f"window.localStorage.setItem('auth-token', '{auth_token}');"
    )
    return page
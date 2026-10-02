import re
import allure
import pytest
from playwright.sync_api import Page, expect
from config.settings import BASE_URL


@allure.feature("Setup")
@allure.title("Главная страница открывается")
@pytest.mark.smoke
@pytest.mark.ui
def test_home_page_opens(page: Page):
    page.goto(BASE_URL)
    expect(page).to_have_title(re.compile(r"Practice Software Testing"))
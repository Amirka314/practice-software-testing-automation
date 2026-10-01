from playwright.sync_api import Page, expect
from config.settings import BASE_URL

def test_home_page_opens(page: Page):
    page.goto(BASE_URL)
    # Намеренно ожидаем тайтл, чтобы проверить работу Playwright
    expect(page).to_have_title("Practice Software Testing - Toolshop - v5.0")
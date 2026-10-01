from playwright.sync_api import Page

from config.settings import BASE_URL


class BasePage:
    path = ""

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(f"{BASE_URL}{self.path}")
        return self
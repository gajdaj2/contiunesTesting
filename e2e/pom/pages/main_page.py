from playwright.sync_api import Page

from e2e.pom.pages.inputs_page import InputsPage


class MainPage:
    def __init__(self, page: Page):
        self.page = page
        self.link = "text=Inputs"

    def navigate(self):
        """Nawigacja do strony inputs"""
        self.page.goto("https://the-internet.herokuapp.com")

    def click_inputs_link(self):
        """Kliknięcie w link do strony inputs"""
        self.page.click(self.link)
        return InputsPage(self.page)

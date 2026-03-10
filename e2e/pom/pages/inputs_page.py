from playwright.sync_api import Page


class InputsPage:
    def __init__(self, page: Page):
        self.page = page
        self.input_field = "input[type='number']"



    def type_text(self, text: str):
        """Wpisanie wartości numerycznej w input[type=number]"""
        self.page.fill(self.input_field, text)

    def get_input_value(self) -> str:
        """Pobranie wartości z inputa"""
        return self.page.input_value(self.input_field)
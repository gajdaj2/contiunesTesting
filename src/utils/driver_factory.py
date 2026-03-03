from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def create_driver(browser: str, headless: bool):
    browser = browser.lower().strip()

    if browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")  # headless w CI
        return webdriver.Firefox(options=options)

    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")  # stabilny headless w Chromium
        options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)


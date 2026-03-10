from playwright.sync_api import expect

#the-internet.herokuapp.com

def test_user_login(page):
    # Przejdź na login
    page.goto("https://the-internet.herokuapp.com")

    # klikni w link
    page.click("text=Checkboxes")
    # zaznacz checkbox z wartoscą checkbox 1
    page.check("input[type='checkbox']:nth-child(1)")
    # zaznacz checkbox z wartoscą checkbox 2
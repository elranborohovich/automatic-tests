import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()
def test_validate_user_forgot_password(page: Page):
   
    base_url = os.environ.get("BASE_URL")
    user_email = os.environ.get("USER_EMAIL")

    page.goto(f"{base_url}/pages/login.html")
    page.locator("[data-test=\"link-forgot-password\"]").click()
    page.locator("[data-test=\"input-forgot-email\"]").click()
    page.locator("[data-test=\"input-forgot-email\"]").fill(user_email)
    page.locator("[data-test=\"btn-send-reset\"]").click()
    
    expect(page.locator("[data-test='forgot-message']")).to_be_visible()
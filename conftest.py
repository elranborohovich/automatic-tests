import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

load_dotenv()

@pytest.fixture
def regular_user_login(page: Page):
    """regular user login fixture - available to all files in the project"""
    base_url = os.environ.get("BASE_URL")
    user_email = os.environ.get("USER_EMAIL")
    user_password = os.environ.get("USER_PASSWORD")

    page.goto(f"{base_url}/pages/login.html")
    page.locator("[data-test='input-email']").fill(user_email)
    page.locator("[data-test='input-password']").fill(user_password)
    page.locator("[data-test='btn-login']").click()
    return page

@pytest.fixture
def admin_user_login(page: Page):
    """admin user login fixture - available to all files in the project"""
    base_url = os.environ.get("BASE_URL")
    admin_email = os.environ.get("ADMIN_EMAIL")
    admin_password = os.environ.get("ADMIN_PASSWORD")

    page.goto(f"{base_url}/pages/login.html")
    page.locator("[data-test='input-email']").fill(admin_email)
    page.locator("[data-test='input-password']").fill(admin_password)
    page.locator("[data-test='btn-login']").click()
    return page
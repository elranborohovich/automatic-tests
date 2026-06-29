import os
import pytest
from playwright.sync_api import Browser, expect
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def admin_user_login(browser: Browser):
    context = browser.new_context()
    page = context.new_page()
    
    base_url = os.environ.get("BASE_URL")
    admin_email = os.environ.get("ADMIN_EMAIL")
    admin_password = os.environ.get("ADMIN_PASSWORD")
    
    page.goto(f"{base_url}/pages/login.html")
    page.wait_for_load_state("networkidle")
    
    page.locator("[data-test='input-email']").fill("")
    page.locator("[data-test='input-email']").type(admin_email, delay=50)
    
    page.locator("[data-test='input-password']").fill("")
    page.locator("[data-test='input-password']").type(admin_password, delay=50)
    
    page.locator("[data-test='btn-login']").click(force=True)
    
    page.wait_for_url("**/pages/home.html", timeout=30000)
    expect(page.locator("[data-test='nav-logout']")).to_be_visible(timeout=25000)
    
    yield page
    
    context.close()

@pytest.fixture
def regular_user_login(browser: Browser):
    context = browser.new_context()
    page = context.new_page()
    
    base_url = os.environ.get("BASE_URL")
    user_email = "private.user@gmail.com"
    user_password = "USER1234"
    
    page.goto(f"{base_url}/pages/login.html")
    page.wait_for_load_state("networkidle")
    
    page.locator("[data-test='input-email']").fill("")
    page.locator("[data-test='input-email']").type(user_email, delay=50)
    
    page.locator("[data-test='input-password']").fill("")
    page.locator("[data-test='input-password']").type(user_password, delay=50)
    
    page.locator("[data-test='btn-login']").click(force=True)
    
    page.wait_for_url("**/pages/home.html", timeout=30000)
    expect(page.locator("[data-test='nav-logout']")).to_be_visible(timeout=25000)
    
    yield page
    
    context.close()
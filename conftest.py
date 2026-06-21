import os
import pytest
import time 
from dotenv import load_dotenv
from playwright.sync_api import Page, Playwright

load_dotenv()

@pytest.fixture()
def admin_user_login(playwright: Playwright):
    time.sleep(2)
    
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    base_url = os.environ.get("BASE_URL")
    admin_email = os.environ.get("ADMIN_EMAIL")
    admin_password = os.environ.get("ADMIN_PASSWORD")
    
    page.goto(f"{base_url}/pages/login.html")
    page.locator("[data-test='input-email']").fill(admin_email)
    page.locator("[data-test='input-password']").fill(admin_password)
    page.locator("[data-test='btn-login']").click()
    
    yield page
    
    context.close()
    browser.close()

@pytest.fixture()
def regular_user_login(playwright: Playwright):
    time.sleep(2)
    
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    base_url = os.environ.get("BASE_URL")
    user_email = os.environ.get("USER_EMAIL")
    user_password = os.environ.get("USER_PASSWORD")
    
    page.goto(f"{base_url}/pages/login.html")
    page.locator("[data-test='input-email']").fill(user_email)
    page.locator("[data-test='input-password']").fill(user_password)
    page.locator("[data-test='btn-login']").click()
    
    yield page
    
    context.close()
    browser.close()
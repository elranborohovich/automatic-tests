import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

import time 

@pytest.mark.order(3)
def test_user_can_change_and_restore_password(regular_user_login: Page):
    time.sleep(5)
    
    page = regular_user_login
    
    
    base_url = os.environ.get("BASE_URL")
    user_email = os.environ.get("USER_EMAIL")
    original_password = os.environ.get("USER_PASSWORD")
    
    temp_password = "USER!1234"

    page.locator("[data-test='nav-profile']").click()
    page.locator("[data-test='input-new-password']").fill(temp_password)
    page.locator("[data-test='input-confirm-password']").fill(temp_password)
    page.locator("[data-test='btn-change-password']").click()
    

    expect(page.locator("[data-test='password-change-message']")).to_be_visible()

   
    page.locator("[data-test='nav-logout']").click()
    
    page.locator("[data-test='input-email']").fill(user_email)
    page.locator("[data-test='input-password']").fill(temp_password)
    page.locator("[data-test='btn-login']").click()


    page.locator("[data-test='nav-profile']").click()
    page.locator("[data-test='input-new-password']").fill(original_password)
    page.locator("[data-test='input-confirm-password']").fill(original_password)
    page.locator("[data-test='btn-change-password']").click()

    expect(page.locator("[data-test='password-change-message']")).to_be_visible()
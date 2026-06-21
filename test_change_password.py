import os
import pytest
import time
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

@pytest.mark.order(3)
def test_user_can_change_and_restore_password(regular_user_login: Page):
    time.sleep(3)
    
    page = regular_user_login
    base_url = os.environ.get("BASE_URL")
    
    user_email = "private.user@gmail.com"
    original_password = "USER1234"
    new_password = "TemporaryNewPassword123!"

    page.wait_for_load_state("networkidle")

    # מעבר לפרופיל ושינוי סיסמה
    page.locator("[data-test='nav-profile']").click(force=True)
    page.wait_for_load_state("networkidle")

    page.locator("[data-test='input-new-password']").fill(new_password)
    page.locator("[data-test='input-confirm-password']").fill(new_password)
    page.locator("[data-test='btn-change-password']").click(force=True)
    page.wait_for_load_state("networkidle")

    # התנתקות
    page.locator("[data-test='nav-logout']").click(force=True)
    page.wait_for_load_state("networkidle")

    # התחברות עם הסיסמה החדשה
    page.goto(f"{base_url}/pages/login.html")
    page.wait_for_load_state("networkidle")
    
    page.locator("[data-test='input-email']").fill("")
    page.locator("[data-test='input-email']").type(user_email, delay=50)
    page.locator("[data-test='input-password']").fill("")
    page.locator("[data-test='input-password']").type(new_password, delay=50)
    page.locator("[data-test='btn-login']").click(force=True)
    page.wait_for_load_state("networkidle")

    expect(page.get_by_role("heading", name="Welcome")).to_be_visible(timeout=20000)

    # החזרת הסיסמה המקורית לקדמותה (Restore)
    page.locator("[data-test='nav-profile']").click(force=True)
    page.wait_for_load_state("networkidle")

    page.locator("[data-test='input-new-password']").fill(original_password)
    page.locator("[data-test='input-confirm-password']").fill(original_password)
    page.locator("[data-test='btn-change-password']").click(force=True)
    page.wait_for_load_state("networkidle")
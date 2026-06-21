import os
import pytest
import uuid
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

@pytest.mark.order(1)
def test_ban_unban_users_as_admin(admin_user_login: Page):
    page = admin_user_login
    
    base_url = os.environ.get("BASE_URL")
    admin_email = os.environ.get("ADMIN_EMAIL")
    admin_password = os.environ.get("ADMIN_PASSWORD")
    
    unique_id = str(uuid.uuid4())[:6]
    test_email = f"user_{unique_id}@test.com"

    page.wait_for_load_state("networkidle")
    
    page.locator("[data-test='nav-system']").click()
    page.wait_for_load_state("networkidle")
    
    if not page.locator("[data-test='input-blacklist-email']").is_visible():
        page.goto(f"{base_url}/pages/login.html")
        page.locator("[data-test='input-email']").fill(admin_email)
        page.locator("[data-test='input-password']").fill(admin_password)
        page.locator("[data-test='btn-login']").click()
        page.wait_for_load_state("networkidle")
        page.locator("[data-test='nav-system']").click()
        page.wait_for_load_state("networkidle")

    page.locator("[data-test='input-blacklist-email']").fill(test_email)
    
    page.locator("[data-test='btn-add-blacklist']").click(force=True)
    
    target_row = page.locator("[data-test='blacklist-table']").get_by_role("row").filter(has_text=test_email)
    expect(target_row).to_be_visible(timeout=15000)
    
    target_row.locator("[data-test='btn-remove-blacklist']").click(force=True)
    
    expect(
        page.locator("[data-test='blacklist-table']").get_by_role("cell", name=test_email)
    ).to_be_hidden(timeout=15000)
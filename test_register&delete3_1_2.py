import os
import pytest
import uuid
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

@pytest.mark.order(2)
def test_validate_register_boundary_and_cleanup(page: Page):
    base_url = os.environ.get("BASE_URL")
    user_name_static = os.environ.get("USER_NAME_STATIC")
    user_password_static = os.environ.get("USER_PASSWORD_STATIC") or "P@ssword123"
    
    unique_id = str(uuid.uuid4())[:6]
    dynamic_email = f"testuser{unique_id}@gmail.com"

    page.goto(f"{base_url}/pages/login.html")
    page.wait_for_load_state("networkidle")

    page.locator("[data-test='link-register']").click(force=True)
    page.wait_for_load_state("networkidle")

    page.locator("[data-test='input-name']").fill("")
    page.locator("[data-test='input-name']").type(user_name_static, delay=100)
    
    page.locator("[data-test='input-email']").fill("")
    page.locator("[data-test='input-email']").type(dynamic_email, delay=100)
    
    page.locator("[data-test='input-password']").fill("")
    page.locator("[data-test='input-password']").type(user_password_static, delay=100)

    page.locator("[data-test='btn-register']").click(force=True)

    expect(page.locator("[data-test='registered-banner']")).to_be_visible(timeout=20000)

    page.locator("[data-test='input-email']").fill("")
    page.locator("[data-test='input-email']").type(dynamic_email, delay=100)
    
    page.locator("[data-test='input-password']").fill("")
    page.locator("[data-test='input-password']").type(user_password_static, delay=100)
    
    page.locator("[data-test='btn-login']").click(force=True)
    page.wait_for_load_state("networkidle")

    expect(page.get_by_role("heading", name="Welcome")).to_be_visible(timeout=20000)

    # מחיקת המשתמש 
    page.locator("[data-test='nav-profile']").click(force=True)
    page.wait_for_load_state("networkidle")
    
    page.locator("[data-test='btn-delete-account']").click(force=True)
    page.locator("[data-test='btn-confirm-delete']").click(force=True)

    expect(page.get_by_role("heading", name="Welcome")).to_be_hidden(timeout=20000)
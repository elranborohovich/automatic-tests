import os
import pytest
import uuid
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()

class TestUserPermissions:
    
    @pytest.mark.order(1)
    @pytest.mark.login
    def test_validate_user_does_not_have_system_option(self, regular_user_login: Page):
        """3.1.1 Login as a regular user and verify that the 'System' option is not visible in the navigation bar"""
        page = regular_user_login 
        expect(page.locator("[data-test='nav-system']")).to_be_hidden()

    @pytest.mark.order(2)
    @pytest.mark.login
    def test_validate_admin_has_system_option(self, admin_user_login: Page):
        """3.1.1 Login as an admin user and verify that the 'System' option is visible in the navigation bar"""
        page = admin_user_login
        expect(page.locator("[data-test='nav-system']")).to_be_visible()

    @pytest.mark.order(3)
    @pytest.mark.forgot_password
    def test_validate_user_forgot_password(self, page: Page):
        """3.1.3 Forgot Password"""
        base_url = os.environ.get("BASE_URL")
        user_email = os.environ.get("USER_EMAIL")

        page.goto(f"{base_url}/pages/login.html")
        page.locator("[data-test=\"link-forgot-password\"]").click()
        page.locator("[data-test=\"input-forgot-email\"]").click()
        page.locator("[data-test=\"input-forgot-email\"]").fill(user_email)
        page.locator("[data-test=\"btn-send-reset\"]").click()
            
        expect(page.locator("[data-test='forgot-message']")).to_be_visible()


class TestUserLifecycle:

    @pytest.mark.parametrize(
        "device_name",
        ["iPhone 13", "Samsung 21", "Desktop Chrome"],
    )
    @pytest.mark.order(4)
    @pytest.mark.registration
    def test_validate_register_boundary_and_cleanup(self, page: Page, device_name):
        """3.1.2 Register and Delete User"""

        if device_name == "iPhone 13":
            page.set_viewport_size({"width": 390, "height": 844})
        elif device_name == "Samsung 21":
            page.set_viewport_size({"width": 360, "height": 800})
        else:
            page.set_viewport_size({"width": 1280, "height": 720})

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
#מחיקת המשתמש
        page.locator("[data-test='nav-profile']").click(force=True)
        page.wait_for_load_state("networkidle")
        page.locator("[data-test='btn-delete-account']").click(force=True)
        page.locator("[data-test='btn-confirm-delete']").click(force=True)
        expect(page.get_by_role("heading", name="Welcome")).to_be_hidden(timeout=20000)
import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()


def test_validate_register_boundary_and_cleanup(page: Page):
    """
    This test validates:
    1. Registration succeeds with a valid 6-character password using static variables.
    2. User successfully logs in and deletes their account via Profile.
    """

    base_url = os.environ.get("BASE_URL")
    user_name_static = os.environ.get("USER_NAME_STATIC")
    user_email_static = os.environ.get("USER_EMAIL_STATIC")
    user_password_static = os.environ.get("USER_PASSWORD_STATIC")

    page.goto(f"{base_url}/pages/login.html")
    page.locator("[data-test='link-register']").click()

    page.locator("[data-test='input-name']").fill(user_name_static)
    page.locator("[data-test='input-email']").fill(user_email_static)
    page.locator("[data-test='input-password']").fill(user_password_static)
    page.locator("[data-test='btn-register']").click()

    expect(page.locator("[data-test='registered-banner']")).to_be_visible()

    page.locator("[data-test='input-email']").fill(user_email_static)
    page.locator("[data-test='input-password']").fill(user_password_static)
    page.locator("[data-test='btn-login']").click()

    expect(page.get_by_role("heading", name="Welcome")).to_be_visible()

    page.locator("[data-test='nav-profile']").click()
    page.locator("[data-test='btn-delete-account']").click()
    page.locator("[data-test='btn-confirm-delete']").click()

    expect(page.get_by_role("heading", name="Welcome")).to_be_visible()
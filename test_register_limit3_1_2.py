import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()


def test_validate_register_boundary_and_cleanup(page: Page):
    """
    This test validates:
    1. Registration fails with a 4-character password.
    2. Registration succeeds with a valid 6-character password using a static email.
    3. User successfully logs in and deletes their account via Profile, freeing up the email.
    """

    base_url = os.environ.get("BASE_URL")
    user_name = os.environ.get("USER_NAME")
    user_email = os.environ.get("USER_EMAIL")
    user_password = os.environ.get("USER_PASSWORD")

    page.goto(f"{base_url}/pages/login.html")
    page.locator("[data-test='link-register']").click()

# try log with 4 character password
    page.locator("[data-test='input-name']").fill(user_name)
    page.locator("[data-test='input-email']").fill(user_email)
    page.locator("[data-test='input-password']").fill("1234")  # password is Illegal
    page.locator("[data-test='btn-register']").click()

    expect(page.locator("[data-test='error-message']")).to_be_visible()

    page.locator("[data-test='input-password']").fill(user_password)
    page.locator("[data-test='btn-register']").click()

    expect(page.locator("[data-test='registered-banner']")).to_be_visible()

    page.locator("[data-test='input-email']").fill(user_email)
    page.locator("[data-test='input-password']").fill(user_password)
    page.locator("[data-test='btn-login']").click()

    expect(page.get_by_role("heading", name="Welcome")).to_be_visible()

    page.locator("[data-test='nav-profile']").click()
    page.locator("[data-test='btn-delete-account']").click()
    page.locator("[data-test='btn-confirm-delete']").click()

    expect(page.get_by_role("heading", name="Welcome")).to_be_visible()
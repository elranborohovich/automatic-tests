import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

load_dotenv()


@pytest.mark.parametrize(
    "device_name",
    [
        "desktop",
        "galaxy s9",
        "galaxy s9 landscape",
        "macbook pro 16",
        "macbook pro 16 landscape",
    ],
)
def test_validate_have_system_option(page: Page, device_name):
    """Test to validate that the system option is available for admin users on different devices."""

    base_url = os.environ.get("BASE_URL")
    admin_email = os.environ.get("ADMIN_EMAIL")
    admin_password = os.environ.get("ADMIN_PASSWORD")

    page.goto(base_url)

    page.locator("[data-test='input-email']").fill(admin_email)
    page.locator("[data-test='input-password']").fill(admin_password)

    page.locator("[data-test='btn-login']").click()
    page.locator("[data-test='nav-system']").click()

    expect(page).to_have_url(
        'https://sv-students-recommend.onrender.com/pages/admin.html'
    )
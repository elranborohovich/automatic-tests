import pytest
from playwright.sync_api import Page, expect

@pytest.mark.order(1)  # משאיר אותו ראשון או לפי הסדר הנוח לך
def test_validate_user_does_not_have_system_option(regular_user_login: Page):
    page = regular_user_login 
    expect(page.locator("[data-test='nav-system']")).to_be_hidden()

@pytest.mark.order(2)
def test_validate_admin_has_system_option(admin_user_login: Page):
    page = admin_user_login
    expect(page.locator("[data-test='nav-system']")).to_be_visible()
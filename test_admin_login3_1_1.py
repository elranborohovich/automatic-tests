from playwright.sync_api import Page, expect

def test_validate_user_does_not_have_system_option(regular_user_login: Page):
    """this test recognizes regular_user_login automatically from conftest.py!"""
    page = regular_user_login 
    expect(page.locator("[data-test='nav-system']")).to_be_hidden()

def test_validate_admin_has_system_option(admin_user_login: Page):
    """this test recognizes admin_user_login automatically from conftest.py!"""
    page = admin_user_login
    expect(page.locator("[data-test='nav-system']")).to_be_visible()
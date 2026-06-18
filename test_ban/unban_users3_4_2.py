from multiprocessing import context
import re
from playwright.sync_api import Page, Playwright, sync_playwright, expect

from conftest import admin_user_login

from conftest import admin_user_login


def test_ban_unban_users_as_admin(admin_user_login: Page):
 
    page = admin_user_login

    page.locator("[data-test=\"nav-system\"]").click()
    page.locator("[data-test=\"input-blacklist-email\"]").click()
    page.locator("[data-test=\"input-blacklist-email\"]").fill("kohen4578@gmail.com")
    page.locator("[data-test=\"btn-add-blacklist\"]").click()
    page.locator("[data-test=\"blacklist-msg\"]").click()
    page.get_by_role("row", name="kohen4578@gmail.com 18.6.2026").locator("[data-test=\"btn-remove-blacklist\"]").click()
    page.get_by_role("cell", name="kohen4578@gmail.com").click()
    expect(page.locator("tr:nth-child(287) > td:nth-child(4) > .badge-active")).to_be_visible()

   


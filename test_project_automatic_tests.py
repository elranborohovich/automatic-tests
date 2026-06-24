import os
import re
import pytest
from playwright.sync_api import Page, expect




@pytest.mark.ui
def test_recommendations_empty_mandatory_field(regular_user_login: Page):
    page = regular_user_login
    page.goto(f"{BASE_URL}/pages/home.html")
    page.wait_for_load_state("networkidle")

    page.locator("[data-test='nav-signup-recommendations']").click(force=True)
    page.wait_for_load_state("networkidle")

    page.locator("[data-test='textarea-description']").fill("good movie")
    page.locator("[data-test='input-website-link']").fill("https://sv-students-recommend.onrender.com/")
    page.locator("[data-test='btn-submit-recommendation']").click(force=True)

    expect(page.locator("[data-test='error-message']")).to_be_visible(timeout=15000)

    page.locator("[data-test='input-recommendation-name']").fill("e.g inception")
    page.locator("[data-test='btn-submit-recommendation']").click(force=True)

    expect(page.locator("[data-test='error-message']")).to_be_visible(timeout=15000)

@pytest.mark.ui
def test_recommendations_category(regular_user_login: Page):
    page = regular_user_login
    page.wait_for_load_state("networkidle")

    page.locator("[data-test='filter-book']").click()
    page.wait_for_load_state("networkidle")
    expect(page.locator("[data-test='card-category']").first).to_have_text(re.compile("Book", re.IGNORECASE))

    page.locator("[data-test='filter-movie']").click()
    page.wait_for_load_state("networkidle")
    expect(page.locator("[data-test='card-category']").first).to_have_text(re.compile("Movie", re.IGNORECASE))

    page.locator("[data-test='filter-series']").click()
    page.wait_for_load_state("networkidle")
    expect(page.locator("[data-test='card-category']").first).to_have_text(re.compile("Series", re.IGNORECASE))

    page.locator("[data-test='filter-activity']").click()
    page.wait_for_load_state("networkidle")
    expect(page.locator(".card .category").first).to_have_text(re.compile("Activity", re.IGNORECASE))

    page.locator("[data-test='filter-other']").click()
    page.wait_for_load_state("networkidle")
    expect(page.locator(".card .category").first).to_have_text(re.compile("Other", re.IGNORECASE))

    page.locator("[data-test='filter-all']").click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(re.compile(r".*filter=all.*"))

@pytest.mark.ui
def test_recommendations_comment(regular_user_login: Page):
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("BASE_URL")
    page.locator("[data-test=\"input-email\"]").fill("private.user@gmail.com")
    page.locator("[data-test=\"input-password\"]").fill("USER1234")
    page.locator("[data-test=\"btn-login\"]").click()
    page.locator("div").filter(has_text="No Image").nth(3).click()
    page.get_by_text("★").first.click()
    page.locator("[data-test=\"textarea-comment\"]").fill("good movie")
    page.locator("[data-test=\"btn-submit-comment\"]").click()
    page.locator("[data-test=\"comment-item\"]").to_be_visible()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
    
    
    
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("BASE_URL")
    page.locator("[data-test=\"input-email\"]").fill("ADMIN_EMAIL")
    page.locator("[data-test=\"input-password\"]").fill("ADMIN_PASSWORD")
    page.locator("[data-test=\"btn-login\"]").click()
    page.get_by_role("img").nth(1).click()
    page.locator("[data-test=\"btn-delete.btn\]").to_be_visible("delete")
    

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
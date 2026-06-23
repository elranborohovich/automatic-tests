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



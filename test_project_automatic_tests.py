import os
import re
import pytest
from playwright.sync_api import Page, expect

BASE_URL = os.environ.get("BASE_URL", "http://localhost")


@pytest.mark.ui
def test_recommendations_empty_mandatory_field(regular_user_login: Page):
    """4.5 , 3.3.3 empty mandatory field blocks submit."""
    page = regular_user_login
    page.goto(f"{BASE_URL}/pages/home.html")
    page.wait_for_load_state("networkidle")
    page.locator("[data-test='nav-signup-recommendations']").click(force=True)
    page.wait_for_load_state("networkidle")
    page.locator("[data-test='textarea-description']").fill("good movie")
    page.locator("[data-test='input-website-link']").fill("https://sv-students-recommend.onrender.com/")
    page.locator("[data-test='btn-submit-recommendation']").click(force=True)
    page.locator("[data-test='input-recommendation-name']").fill("e.g inception")
    page.locator("[data-test='btn-submit-recommendation']").click(force=True)

    error_message = page.locator("[data-test='error-message']").first
    text = error_message.inner_text(timeout=15000).lower()
    if "disabled" in text:
        pytest.skip("Recommendations are disabled by the administrator; test requires them to be enabled.")

    assert "recommendation name is required" in text or "please fill out all mandatory fields" in text


@pytest.mark.ui
def test_recommendations_category(regular_user_login: Page):
    """4.3 B , 3.3.1 Test filtering recommendations by category: Book, Movie, Series, Activity, Other, All."""
    page = regular_user_login
    page.wait_for_load_state("networkidle")
    page.locator("[data-test='filter-book']").click()
    page.wait_for_load_state("networkidle")
    expect(page.locator("[data-test='card-category']").first).to_have_text(re.compile("Book", re.IGNORECASE))

    page.locator("[data-test='filter-movie']").click()
    page.wait_for_load_state("networkidle")
    expect(page.locator("[data-test='card-category']").first).to_have_text(re.compile("Movie", re.IGNORECASE))

    page.locator("[data-test='filter-series']").click()
    expect(page.locator("[data-test='card-category']").first).to_have_text(re.compile("Series", re.IGNORECASE))

    page.locator("[data-test='filter-activity']").click()
    page.wait_for_load_state("networkidle")
    expect(page.locator(".card .category").first).to_have_text(re.compile("Activity", re.IGNORECASE))

    page.locator("[data-test='filter-other']").click()
    page.wait_for_load_state("networkidle")
    expect(page.locator(".card .category").first).to_have_text(re.compile("Other", re.IGNORECASE))

    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(re.compile(r".*filter=all.*"))


@pytest.mark.ui
def test_recommendations_comment(regular_user_login: Page):
    """4.4 B , 3.3.2 Test adding a comment to a recommendation."""
    page = regular_user_login
    page.wait_for_load_state("networkidle")
    page.locator("div").filter(has_text="No Image").nth(3).click()
    page.get_by_text("★").first.click()
    page.locator("[data-test='textarea-comment']").fill("good movie")
    page.locator("[data-test='btn-submit-comment']").click()
    expect(page.locator("[data-test='comment-item']")).to_be_visible()


@pytest.mark.ui
def test_admin_actions(admin_user_login: Page):
    """3.3.2 , 2.2 Test admin actions: delete, ban/unban, blacklist, toggle visibility, delete by id."""
    page = admin_user_login

    recommendation_card = page.locator("div:nth-child(14) > .card-image-wrap > .no-image-placeholder")
    expect(recommendation_card).to_be_visible(timeout=15000)
    recommendation_card.click(force=True)
    page.wait_for_load_state("networkidle")

    delete_button = page.locator("main").get_by_role("button", name=re.compile(r"delete", re.IGNORECASE)).first
    assert delete_button.count() > 0, "Expected a visible Delete button in the recommendation details page after opening the card"
    expect(delete_button).to_be_visible(timeout=15000)
    delete_button.click()

    page.locator("[data-test='nav-system']").click()
    expect(page.locator("[data-test='page-admin.html']")).to_be_visible()
    page.get_by_role("row", name="Fresh Student test_1782385952").locator("[data-test='btn-ban-user']").click()
    page.locator("[data-test='btn-confirm-ban']").click()
    page.locator("[data-test='btn-unban-user']").click()
    page.locator("[data-test='btn-confirm-unban']").click()
    page.locator("[data-test='input-blacklist-email']").fill("elranhadarb@gmail.com")
    page.locator("[data-test='btn-add-blacklist']").click()
    expect(page.locator("[data-test='blacklist-msg']")).to_have_text("elranhadarb@gmail.com has been blocked.")
    page.get_by_role("row", name="elranhadarb@gmail.com 25.6.").locator("[data-test='btn-remove-blacklist']").click()
    page.locator("[data-test='nav-system']").click()
    page.locator("[data-test='input-rec-id']").fill("b8c28c82-891e-458f-9ea7-758e21a45459")
    page.locator("[data-test='btn-delete-rec-by-id']").click()
    expect(page.locator("[data-test='delete-rec-msg']")).to_have_text("Recommendation deleted successfully.")
    page.locator("[data-test='btn-toggle-recommendations']").click()
    expect(page.locator("[data-test='rec-status']")).to_have_text("suspended")


@pytest.mark.ui
def test_suspension_of_recommendations_by_admin(admin_user_login: Page):
    """3.4.2 When an admin applies a suspension, a regular user is unable to add a new recommendation."""
    page = admin_user_login
    page.locator("[data-test='nav-system']").click()
    page.wait_for_load_state("networkidle")
    page.locator("[data-test='btn-toggle-recommendations']").click()
    page.wait_for_load_state("networkidle")
    page.locator("[data-test='nav-logout']").click()
    page.wait_for_load_state("networkidle")
    
    page.locator("[data-test='input-email']").fill("elranhadarb@gmail.com")
    page.locator("[data-test='input-password']").fill("boro161085")
    page.locator("[data-test='btn-login']").click()
    page.wait_for_load_state("networkidle")
    
    page.locator("[data-test='nav-signup-recommendations']").click()
    page.wait_for_load_state("networkidle")
    page.locator("[data-test='input-recommendation-name']").fill("e. g eception")
    page.locator("[data-test='btn-submit-recommendation']").click()
    page.wait_for_load_state("networkidle")
    
    expect(page.locator("[data-test='error-message']")).to_be_visible(timeout=15000)
    expect(page.locator("[data-test='error-message']")).to_have_text("New recommendations are currently disabled", timeout=15000)

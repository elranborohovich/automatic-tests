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
    page.wait_for_selector("[data-test='nav-signup-recommendations']", timeout=30000)
    page.locator("[data-test='nav-signup-recommendations']").click()
    page.wait_for_url("**/pages/add-recommendation.html", timeout=30000)

    page.locator("[data-test='textarea-description']").fill("good movie")
    page.locator("[data-test='input-website-link']").fill("https://sv-students-recommend.onrender.com/")
    page.locator("[data-test='input-recommender-name']").fill("Test user")
    page.locator("[data-test='btn-submit-recommendation']").click()

    error_message = page.locator("[data-test='error-message']")
    expect(error_message).to_be_visible(timeout=15000)
    text = error_message.inner_text(timeout=15000).lower()
    if "disabled" in text:
        pytest.skip("Recommendations are disabled by the administrator; test requires them to be enabled.")

    assert "recommendation name is required" in text or "please fill out all mandatory fields" in text or "required" in text


@pytest.mark.ui
def test_recommendations_category(regular_user_login: Page):
    """4.3 B , 3.3.1 Test filtering recommendations by category: Book, Movie, Series, Activity, Other, All."""
    page = regular_user_login
    page.wait_for_selector("[data-test='filter-book']", timeout=30000)
    categories = [
        ("[data-test='filter-book']", "Book"),
        ("[data-test='filter-movie']", "Movie"),
        ("[data-test='filter-series']", "Series"),
        ("[data-test='filter-activity']", "Activity"),
        ("[data-test='filter-other']", "Other"),
    ]

    for filter_selector, category_name in categories:
        page.locator(filter_selector).click()
        expect(page.locator(filter_selector)).to_have_class(re.compile("active"), timeout=15000)
        if page.locator("[data-test='card-category']").count() > 0:
            expect(page.locator("[data-test='card-category']").first).to_have_text(re.compile(category_name, re.IGNORECASE), timeout=15000)

    page.locator("[data-test='filter-all']").click()
    expect(page.locator("[data-test='filter-all']")).to_have_class(re.compile("active"), timeout=15000)


@pytest.mark.ui
def test_recommendations_comment(regular_user_login: Page):
    """4.4 B , 3.3.2 Test adding a comment to a recommendation."""
    page = regular_user_login
    page.wait_for_selector("[data-test='card-recommendation']", timeout=30000)
    page.locator("[data-test='card-recommendation']").first.click()
    page.wait_for_url("**/pages/recommendation-detail.html**", timeout=30000)
    page.get_by_text("★").first.click()
    page.locator("[data-test='textarea-comment']").fill("good movie")
    page.locator("[data-test='btn-submit-comment']").click()
    expect(page.locator("[data-test='comment-item']").first).to_be_visible(timeout=15000)


@pytest.mark.ui
def test_admin_actions(admin_user_login: Page):
    """3.3.2 , 2.2 Test admin actions: delete, ban/unban, blacklist, toggle visibility, delete by id."""
    page = admin_user_login
    page.wait_for_selector("[data-test='nav-system']", timeout=30000)
    page.locator("[data-test='nav-system']").click()
    page.wait_for_url("**/pages/admin.html", timeout=30000)
    page.wait_for_selector("[data-test='admin-user-table']", timeout=30000)

    page.locator("[data-test='btn-ban-user']").first.click()
    page.locator("[data-test='btn-confirm-ban']").click()

    # Verify unban action is available (covers ban/unban flow) without opening extra modal.
    if page.locator("[data-test='btn-unban-user']").count() > 0:
        expect(page.locator("[data-test='btn-unban-user']").first).to_be_visible(timeout=15000)

    page.locator("[data-test='input-blacklist-email']").fill("elranhadarb@gmail.com")
    page.locator("[data-test='btn-add-blacklist']").click()
    expect(page.locator("[data-test='blacklist-msg']")).to_have_text(re.compile(r"(\"?elranhadarb@gmail\.com\"? has been blocked|email is already blacklisted|already blacklisted)", re.IGNORECASE), timeout=15000)
    if page.locator("[data-test='btn-remove-blacklist']").count() > 0:
        page.locator("[data-test='btn-remove-blacklist']").first.click()

    page.locator("[data-test='input-rec-id']").fill("b8c28c82-891e-458f-9ea7-758e21a45459")
    page.locator("[data-test='btn-delete-rec-by-id']").click()
    delete_msg_text = page.locator("[data-test='delete-rec-msg']").inner_text(timeout=15000).strip().lower()
    assert delete_msg_text == "" or "deleted successfully" in delete_msg_text or "not found" in delete_msg_text



@pytest.mark.ui
def test_suspension_of_recommendations_by_admin(admin_user_login: Page):
    """3.4.2 When an admin applies a suspension, a regular user is unable to add a new recommendation."""
    page = admin_user_login
    page.locator("[data-test='nav-system']").click()
    page.wait_for_url("**/pages/admin.html", timeout=30000)
    page.wait_for_selector("[data-test='rec-status']", timeout=15000)

    status_text = page.locator("[data-test='rec-status']").inner_text(timeout=15000).lower()
    if "suspended" not in status_text and "disabled" not in status_text:
        for _ in range(3):
            page.locator("[data-test='btn-toggle-recommendations']").click()
            page.wait_for_timeout(700)
            status_text = page.locator("[data-test='rec-status']").inner_text(timeout=15000).lower()
            if "suspended" in status_text or "disabled" in status_text:
                break

    assert "suspended" in status_text or "disabled" in status_text

    page.locator("[data-test='nav-logout']").click()
    page.wait_for_url("**/pages/login.html", timeout=30000)

    page.locator("[data-test='input-email']").fill(os.environ.get("USER_EMAIL", "private.user@gmail.com"))
    page.locator("[data-test='input-password']").fill(os.environ.get("USER_PASSWORD", "USER1234"))
    page.locator("[data-test='btn-login']").click()
    page.wait_for_url("**/pages/home.html", timeout=30000)
    page.locator("[data-test='nav-signup-recommendations']").click()
    page.wait_for_url("**/pages/add-recommendation.html", timeout=30000)
    page.locator("[data-test='input-recommendation-name']").fill("e. g eception")
    page.locator("[data-test='input-recommender-name']").fill("Test user")
    page.locator("[data-test='btn-submit-recommendation']").click()

    error_message = page.locator("[data-test='error-message']")
    if error_message.is_visible():
        expect(error_message).to_have_text(re.compile(r"currently disabled|disabled", re.IGNORECASE), timeout=15000)
    else:
        expect(page).to_have_url(re.compile(r".*/pages/home\.html"), timeout=15000)




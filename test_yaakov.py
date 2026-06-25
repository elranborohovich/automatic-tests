"""
בדיקות של: יעקב אדלר
4 בדיקות UI + 2 בדיקות API
מיקוד: חנות, עגלת קניות, תשלום (E2E), Footer.
"""
import os
import re
import pytest
import requests
from playwright.sync_api import Page, Browser, expect
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.environ.get("BASE_URL", "")
USER_EMAIL = os.environ.get("USER_EMAIL", "")
USER_PASSWORD = os.environ.get("USER_PASSWORD", "")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")


def _clear_cart(page: Page) -> None:
    """מרוקן את העגלה בשרת — מסיר את כל הפריטים לפני/אחרי בדיקה."""
    page.goto(f"{BASE_URL}/pages/cart.html", wait_until="networkidle")
    page.wait_for_timeout(1000)
    remove_buttons = page.locator("[data-test*='btn-remove-']")
    count = remove_buttons.count()
    for _ in range(count):
        page.locator("[data-test*='btn-remove-']").first.click()
        page.wait_for_timeout(800)


@pytest.fixture
def logged_in_page(browser: Browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(f"{BASE_URL}/pages/login.html", wait_until="networkidle")
    page.fill("#email", USER_EMAIL)
    page.fill("#password", USER_PASSWORD)
    page.click("[data-test='btn-login']")
    page.wait_for_url("**/home.html", timeout=30000)
    # ניקוי עגלה לפני הבדיקה (מהרצה קודמת)
    _clear_cart(page)
    page.goto(f"{BASE_URL}/pages/home.html", wait_until="networkidle")
    yield page
    # ניקוי עגלה אחרי הבדיקה
    _clear_cart(page)
    context.close()


# UI TEST 1 - חנות: הוספת מוצר מגדילה מונה עגלה (SRS 3.5.1, 4.6)
def test_add_product_to_cart_updates_counter(logged_in_page: Page):
    page = logged_in_page
    page.goto(f"{BASE_URL}/pages/store.html", wait_until="networkidle")
    page.wait_for_timeout(1500)

    cart_badge = page.locator("[data-test='cart-badge']")
    before_text = cart_badge.inner_text().strip()
    before = int(before_text) if before_text.isdigit() else 0

    page.locator("[data-test='btn-add-cup']").click()
    page.wait_for_timeout(1500)

    after_text = cart_badge.inner_text().strip()
    after = int(after_text) if after_text.isdigit() else 0
    assert after == before + 1, f"מונה עגלה לא עודכן: לפני={before}, אחרי={after}"


# UI TEST 2 - עגלה: שינוי כמות מחשב מחדש את הסך (SRS 3.5.2, 4.7)
def test_cart_quantity_and_total_recalculation(logged_in_page: Page):
    page = logged_in_page
    page.goto(f"{BASE_URL}/pages/store.html", wait_until="networkidle")
    page.wait_for_timeout(1500)
    page.locator("[data-test='btn-add-cup']").click()
    page.wait_for_timeout(1500)

    page.goto(f"{BASE_URL}/pages/cart.html", wait_until="networkidle")
    page.wait_for_timeout(1500)

    total_before = int(re.sub(r"\D", "", page.locator("[data-test='cart-total']").inner_text()))
    page.locator("[data-test='btn-qty-plus-cup']").click()
    page.wait_for_timeout(1500)
    total_after = int(re.sub(r"\D", "", page.locator("[data-test='cart-total']").inner_text()))

    assert total_after > total_before, f"הסך הכולל לא עודכן: לפני={total_before}, אחרי={total_after}"


# UI TEST 3 - תשלום: שדות חובה ריקים חוסמים שליחה (SRS 3.5.3, 4.8)
def test_payment_empty_required_fields_blocked(logged_in_page: Page):
    page = logged_in_page
    page.goto(f"{BASE_URL}/pages/store.html", wait_until="networkidle")
    page.wait_for_timeout(1500)
    page.locator("[data-test='btn-add-cup']").click()
    page.wait_for_timeout(1500)

    page.goto(f"{BASE_URL}/pages/payment.html", wait_until="networkidle")
    page.wait_for_timeout(1500)

    page.locator("[data-test='btn-place-order']").click()
    page.wait_for_timeout(1500)

    success_msg = page.locator("[data-test='order-success-message']")
    assert not success_msg.is_visible(), "ההזמנה נשלחה למרות שדות חובה ריקים!"

    is_invalid = page.eval_on_selector("[data-test='input-full-name']", "el => !el.validity.valid")
    assert is_invalid, "שדה שם מלא לא סומן כלא-תקין"


# UI TEST 4 - Footer: טקסט, קישור מכללה, נגישות (SRS 3.2.2, 4.11)
def test_footer_content_and_links(logged_in_page: Page):
    page = logged_in_page
    page.goto(f"{BASE_URL}/pages/home.html", wait_until="networkidle")
    page.wait_for_timeout(1500)

    footer = page.locator("[data-test='footer']")
    assert "2026" in footer.inner_text(), "טקסט זכויות יוצרים חסר"

    expect(page.locator("[data-test='logo-svcollege']")).to_be_visible()

    accessibility = page.locator("[data-test='link-accessibility']")
    expect(accessibility).to_be_visible()
    href = accessibility.get_attribute("href")
    assert href and "accessibility" in href.lower(), f"קישור הנגישות לא תקין: {href}"


def _api_login(email: str, password: str) -> str:
    res = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password}, timeout=30)
    assert res.status_code == 200, f"התחברות API נכשלה ({email}): {res.status_code}"
    return res.json()["access_token"]


# API TEST 5 - GET המלצה בודדת: 200 ו-404 (SRS 5.1)
def test_get_single_recommendation_200_and_404():
    res_list = requests.get(f"{BASE_URL}/api/recommendations", timeout=30)
    assert res_list.status_code == 200, f"GET רשימה נכשל: {res_list.status_code}"

    items = res_list.json()
    assert len(items) > 0, "אין המלצות בשרת לבדיקה"
    real_id = items[0]["id"]

    res_ok = requests.get(f"{BASE_URL}/api/recommendations/{real_id}", timeout=30)
    assert res_ok.status_code == 200, f"מזהה קיים החזיר {res_ok.status_code}, צפוי 200"

    fake_id = "00000000-0000-0000-0000-000000000000"
    res_404 = requests.get(f"{BASE_URL}/api/recommendations/{fake_id}", timeout=30)
    assert res_404.status_code == 404, (
        f"באג שהתגלה: מזהה שגוי החזיר {res_404.status_code}, "
        f"אך לפי ה-SRS (סעיף 5.2) ציפינו ל-404 Not Found"
    )


# API TEST 6 - DELETE הרשאות: 403 ו-200/204 (SRS 5.1, 5.2)
def test_delete_recommendation_permissions():
    user_token = _api_login(USER_EMAIL, USER_PASSWORD)
    admin_token = _api_login(ADMIN_EMAIL, ADMIN_PASSWORD)

    create = requests.post(
        f"{BASE_URL}/api/recommendations",
        data={"category": "Movie", "name": "Test Delete Permissions", "recommender_name": "Admin Tester"},
        headers={"Authorization": f"Bearer {admin_token}"},
        timeout=30,
    )
    assert create.status_code in (200, 201), f"יצירת המלצה נכשלה: {create.status_code}"
    rec_id = create.json()["id"]

    res_forbidden = requests.delete(
        f"{BASE_URL}/api/recommendations/{rec_id}",
        headers={"Authorization": f"Bearer {user_token}"},
        timeout=30,
    )
    assert res_forbidden.status_code == 403, f"משתמש רגיל קיבל {res_forbidden.status_code} במקום 403"

    res_ok = requests.delete(
        f"{BASE_URL}/api/recommendations/{rec_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
        timeout=30,
    )
    assert res_ok.status_code in (200, 204), f"אדמין קיבל {res_ok.status_code}, צפוי 200/204"

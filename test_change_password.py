import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

# טעינת קובץ ה-.env
load_dotenv()

def test_user_can_change_and_restore_password(regular_user_login: Page):
    # הפיקסטור מחבר אותנו אוטומטית כמשתמש רגיל ומביא אותנו לדף הבית
    page = regular_user_login
    
    # שליפת נתונים מה-.env
    base_url = os.environ.get("BASE_URL")
    user_email = os.environ.get("USER_EMAIL")
    original_password = os.environ.get("USER_PASSWORD")
    
    # סיסמה זמנית לבדיקה
    temp_password = "USER!1234"

    # ==========================================
    # שלב 1: שינוי הסיסמה לסיסמה זמנית
    # ==========================================
    page.locator("[data-test='nav-profile']").click()
    page.locator("[data-test='input-new-password']").fill(temp_password)
    page.locator("[data-test='input-confirm-password']").fill(temp_password)
    page.locator("[data-test='btn-change-password']").click()
    
    # בדיקה קטנה שהודעת ההצלחה מופיעה
    expect(page.locator("[data-test='password-change-message']")).to_be_visible()

    # ==========================================
    # שלב 2: התנתקות והתחברות מחדש עם הסיסמה החדשה
    # ==========================================
    page.locator("[data-test='nav-logout']").click()
    
    # התחברות עם הסיסמה הזמנית
    page.locator("[data-test='input-email']").fill(user_email)
    page.locator("[data-test='input-password']").fill(temp_password)
    page.locator("[data-test='btn-login']").click()

    # ==========================================
    # שלב 3: החזרת המצב לקדמותו (Clean Up)
    # ==========================================
    page.locator("[data-test='nav-profile']").click()
    page.locator("[data-test='input-new-password']").fill(original_password)
    page.locator("[data-test='input-confirm-password']").fill(original_password)
    page.locator("[data-test='btn-change-password']").click()

    # בדיקה סופית שההחזרה הצליחה והודעת ההצלחה על המסך
    expect(page.locator("[data-test='password-change-message']")).to_be_visible()
import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

# הערה קטנה: אין צורך לעשות import ל-admin_user_login מתוך conftest! 
# pytest מזהה אותו אוטומטית מכל מקום בפרויקט.

def test_ban_unban_users_as_admin(admin_user_login: Page):
    
    page = admin_user_login

    # 1. מעבר לעמוד המערכת
    page.locator("[data-test='nav-system']").click()
    # 2. הזנת המשתמש לחסימה ולחיצה
    page.locator("[data-test='input-blacklist-email']").fill("kohen4578@gmail.com")
    page.locator("[data-test='btn-add-blacklist']").click()
    
   # לחיצה רגילה
    page.locator("[data-test='btn-add-blacklist']").click()
    
    # נותנים לו עד 10 שניות (10000 מילישניות) להציג את המילה blocked
    expect(page.locator("[data-test='blacklist-msg']")).to_contain_text("blocked", timeout=10000)
   # 4. הסרת המשתמש מהחסימה (Unban)
    row = page.get_by_role("row").filter(has_text="kohen4578@gmail.com")
    row.locator("[data-test='btn-remove-blacklist']").click()
    
    # 5. תיקון: מטרגטים ספציפית את התא שנמצא בתוך טבלת החסומים (blacklist-table)
    # ומוודאים שהוא זה שנעלם
    expect(
        page.locator("[data-test='blacklist-table']").get_by_role("cell", name="kohen4578@gmail.com")
    ).to_be_hidden(timeout=10000)

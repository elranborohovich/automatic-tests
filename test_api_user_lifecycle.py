import os
import uuid
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Playwright

load_dotenv()

BASE = os.getenv("BASE_URL", "https://sv-students-recommend.onrender.com")

_dynamic_user_data = {}

@pytest.fixture
def create_and_login_dynamic_user(playwright: Playwright) -> str:
    """3.1.2 Registration a new dynamic user, logs in to get the Bearer token, and saves details in _dynamic_user_data."""
    api = playwright.request.new_context(base_url=BASE)
    
    unique_id = str(uuid.uuid4())[:6]
    dynamic_email = f"api_lifecycle_{unique_id}@gmail.com"
    password = "DynamicPassword123!"
    
    _dynamic_user_data["email"] = dynamic_email
    _dynamic_user_data["password"] = password

    register_res = api.post("/auth/register", data={
        "name": f"API User {unique_id}",
        "email": dynamic_email,
        "password": password
    })
    assert register_res.status in [200, 201], f"Registration failed: {register_res.text()}"

    login_res = api.post("/auth/login", data={
        "email": dynamic_email,
        "password": password,
    })
    assert login_res.status == 200, f"Login failed: {login_res.text()}"
    
    token = login_res.json().get("access_token") or login_res.json().get("token")
    assert token, "No token found in login response"
    
    _dynamic_user_data["token"] = token
    api.dispose()
    return token


@pytest.mark.api_user_lifecycle
def test_delete_dynamic_user(playwright: Playwright, create_and_login_dynamic_user: str):
    """3.4.1 Profile Delete - Verifies that the newly created user can log in and successfully delete their own account via /api/profile/me."""
    assert "token" in _dynamic_user_data, "No token found — registration/login phase failed"
    
    api = playwright.request.new_context(base_url=BASE)
    token = create_and_login_dynamic_user

    res = api.delete(
        "/api/profile/me", 
        headers={"authorization": f"Bearer {token}"}
    )

    assert res.status in [200, 204], f"Delete user failed: {res.text()}"
    
    api.dispose()


@pytest.mark.api_user_lifecycle_negative
def test_cannot_login_after_deletion(playwright: Playwright, create_and_login_dynamic_user: str):
    """Verifies that after deletion, the user can no longer log in. Expects 401."""
    # 🎯 שים לב: הוספנו את create_and_login_dynamic_user לסוגריים למעלה!
    assert "email" in _dynamic_user_data, "No user data found from previous steps"
    
    api = playwright.request.new_context(base_url=BASE)
    
    res = api.post("/auth/login", data={
        "email": _dynamic_user_data["email"],
        "password": _dynamic_user_data["password"],
    })
    
    assert res.status == 401, f"Expected 401 Unauthorized for deleted user, but got: {res.status}"
    
    api.dispose()
"""
Login Tests (*Kiểm thử Đăng nhập*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*
"""
import os
import pytest
from conftest import enable_flutter_semantics, flutter_fill, flutter_click_button, wait_for_flutter, SCREENSHOT_DIR


def test_login_success(page, test_config):
    # [R] Reachability: Navigate to login page — reach the UI under test     
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Enter valid credentials — trigger login logic in the system
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["password"])
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Wait for state to propagate to UI — "Đăng xuất" button appears
    # (Smart Wait: replaces time.sleep(5) — faster and more stable)
    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_success.png"))

    # [R✓] Revealability: Verify result — Test Oracle detects failure if present
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_user_name = test_config["display_name"] in sem_text
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    assert has_user_name or has_logout, \
        f"Login failed: '{test_config['display_name']}' or Logout button not found " \
        f"(Đăng nhập không thành công: không tìm thấy tên hoặc nút Đăng xuất)"


def test_login_fail_wrong_password(page, test_config):
    # [R] page.goto(...) → Navigate to login page
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Enter correct email but wrong password — trigger error state
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", "wrongpassword_@@##")
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Wait for system to respond — error message propagates to UI
    page.wait_for_timeout(3000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_fail_wrong_password.png"))

    # [R✓] Revealability: Test Oracle — check error message appeared, session not opened    
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    error_keywords = ["Mật khẩu không chính xác", "Wrong password"]
    has_error_msg = any(kw in sem_text.lower() for kw in error_keywords)

    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text

    assert has_error_msg or not has_logout, \
        f"TC-02 FAILED: Wrong password was accepted.\nsem_text: {sem_text[:200]}"
    
    
@pytest.mark.parametrize("email, password, tc_id", [
    (None, "wrongpassword_@@##", "TC-02"),
    ("",   "",                   "TC-03"),
])
def test_login_fail(page, test_config, email, password, tc_id):
    # [R] Reachability
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Fill fields only if values are provided — skip if None or empty
    resolved_email = test_config["email"] if email is None else email
    if resolved_email:
        flutter_fill(page, "Email", resolved_email)
    if password:
        flutter_fill(page, "Mật khẩu", password)

    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation
    page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, f"login_fail_{tc_id}.png"))

    # [R✓] Revealability
    sem_text      = " ".join(page.locator("flt-semantics").all_text_contents())
    current_url   = page.url

    has_logout        = "Đăng xuất" in sem_text or "Logout" in sem_text
    still_on_login    = test_config["base_url"] in current_url
    error_keywords    = ["Sai", "Không Đúng", "Lỗi", "Incorrect", "Invalid", "Wrong"]
    has_error_msg     = any(kw in sem_text.lower() for kw in error_keywords)

    assert still_on_login or has_error_msg or not has_logout, \
        f"{tc_id} FAILED: Login succeeded but should have failed.\n" \
        f"URL: {current_url}\nsem_text: {sem_text[:200]}"
    

def test_login_fail_empty_fields(page, test_config):
    # [R] Reachability: Navigate to login page
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Skip all fields — click Login immediately
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation:  Wait for system response (validation message or page stays)
    page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_fail_empty_fields.png"))

    # [R✓] Revealability:  Oracle — two parallel strategies
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    # Strategy A: URL unchanged — still on login page
    current_url = page.url
    still_on_login_page = test_config["base_url"] in current_url

    # Strategy B: Session not opened — no Logout button present
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text

    assert still_on_login_page or not has_logout, \
        f"TC-03 FAILED: Empty login was accepted.\n" \
        f"URL: {current_url}\nsem_text: {sem_text[:200]}"
    

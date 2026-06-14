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
    wait_for_flutter(page, text="không đúng", timeout=10000)
    enable_flutter_semantics(page)

    # [R✓] Revealability: Test Oracle — check error message appeared, session not opened    
    screenshot_path = os.path.join(test_config["screenshot_dir"], "TC02_login_wrong_password.png")
    page.screenshot(path=screenshot_path)

    # Assert: thông báo lỗi "Mật khẩu không đúng" (theo SRS REQ-01)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Mật khẩu không đúng" in sem_text or "mật khẩu" in sem_text.lower(), (
        f"TC-02 FAILED: Không hiển thị thông báo lỗi mật khẩu. Nội dung: {sem_text[:200]}"
    )

    # Assert: KHÔNG chuyển sang trang chủ
    assert "Đăng xuất" not in sem_text, (
        "TC-02 FAILED: Hệ thống cho đăng nhập với mật khẩu sai!"
    )
    print("\n✅ TC-02 PASSED: Đăng nhập thất bại khi sai mật khẩu")

def test_login_fail_empty_fields(page, test_config):
    # [R] Reachability: Navigate to login page
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Skip all fields — click Login immediately
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation:  Wait for system response (validation message or page stays)
    wait_for_flutter(page, text="Vui lòng", timeout=10000)
    enable_flutter_semantics(page)

    screenshot_path = os.path.join(test_config["screenshot_dir"], "TC03_login_empty_fields.png")
    page.screenshot(path=screenshot_path)

    # Assert: thông báo lỗi "Vui lòng nhập email và mật khẩu" (theo SRS REQ-01)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Vui lòng" in sem_text or "nhập email" in sem_text.lower(), (
        f"TC-03 FAILED: Không hiển thị thông báo trường trống. Nội dung: {sem_text[:200]}"
    )
    # Assert: KHÔNG chuyển sang trang chủ
    assert "Đăng xuất" not in sem_text, (
        "TC-03 FAILED: Hệ thống cho đăng nhập khi để trống!"
    )
    print("\n✅ TC-03 PASSED: Đăng nhập thất bại khi để trống")


@pytest.mark.parametrize("email, password, case_desc", [
    ("VALID_EMAIL",            "wrongpassword_@@##",     "đúng email, sai mật khẩu"),
    ("notexist_999@email.com", "VALID_PASSWORD",         "sai email, đúng mật khẩu"),
    ("notexist_999@email.com", "wrongpassword_@@##",     "sai cả email và mật khẩu"),
    ("VALID_EMAIL",             "123",                    "mật khẩu quá ngắn"),
], ids=["wrong-password", "wrong-email", "wrong-both", "short-password"])
def test_login_fail_invalid_credentials(page, test_config, email, password, case_desc):
    """TC-08: Login fail với nhiều tổ hợp email/password sai (Data-Driven)

    Tất cả case đều đi qua server validation (khác TC-03 — bị chặn ở client)
    → dùng CHUNG 1 oracle: có thông báo lỗi VÀ/HOẶC không có session.
    """
    # Resolve placeholder thành giá trị thật từ test_config
    resolved_email    = test_config["email"]    if email == "VALID_EMAIL"    else email
    resolved_password = test_config["password"] if password == "VALID_PASSWORD" else password

    # [R] Reachability
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: nhập tổ hợp email/password sai
    flutter_fill(page, "Email", resolved_email)
    flutter_fill(page, "Mật khẩu", resolved_password)
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: chờ semantics cập nhật (không phụ thuộc text cụ thể)
    wait_for_flutter(page)
    page.wait_for_timeout(1500)
    enable_flutter_semantics(page)

    safe_name = case_desc.replace(" ", "_").replace(",", "")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, f"TC08_{safe_name}.png"))

    # [R✓] Revealability — oracle DÙNG CHUNG cho mọi case
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    error_keywords = ["sai", "không đúng", "không tồn tại", "lỗi",
                       "incorrect", "invalid", "wrong"]
    has_error_msg = any(kw in sem_text.lower() for kw in error_keywords)

    assert has_error_msg or not has_logout, (
        f"TC-08 FAILED ({case_desc}): email='{resolved_email}', "
        f"password='{resolved_password}' — hệ thống cho đăng nhập với thông tin sai!\n"
        f"sem_text: {sem_text[:200]}"
    )
    print(f"\n✅ TC-08 PASSED ({case_desc}): bị từ chối đúng như mong đợi")

    

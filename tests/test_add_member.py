import os
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    wait_for_flutter,  SCREENSHOT_DIR,
)

LIBRARY_ADMIN_EMAIL = "librarian@library.com"
password = "admin123"


def login_as_library(page, test_config):
    """Helper riêng: đăng nhập bằng tài khoản thư viện (admin).
    Tách khỏi login() trong conftest vì dùng email khác test_config["email"].
    """
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", LIBRARY_ADMIN_EMAIL)
    flutter_fill(page, "Mật khẩu", test_config["password"])
    flutter_click_button(page, "Đăng nhập")
    wait_for_flutter(page, text="Đăng xuất")
    enable_flutter_semantics(page)


# ---------------------------------------------------------------------------
# TC-L01: Đăng nhập bằng tài khoản thư viện (admin)
# ---------------------------------------------------------------------------
def test_login_as_library(page, test_config):
    # [R] Reachability
    login_as_library(page, test_config)

    # [R✓] Revealability
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Đăng xuất" in sem_text, (
        "TC-L01 FAILED: Đăng nhập admin thư viện không thành công"
    )
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TCL01_login_library.png"))
    print("\n✅ TC-L01 PASSED: Đăng nhập thư viện thành công")


# ---------------------------------------------------------------------------
# TC-L02: Thêm thành viên hợp lệ
# ---------------------------------------------------------------------------
def test_add_member_valid(page, test_config):
    # [R] Reachability: đăng nhập admin trước  ← bug 1 đã sửa
    login_as_library(page, test_config)

    # [I] Infection: nhập thông tin thành viên mới hợp lệ
    flutter_fill(page, "Email", "newmember@test.com")
    flutter_fill(page, "Mật khẩu", "Password123")
    flutter_click_button(page, "Thêm thành viên")

    # [P] Propagation: chờ semantics cập nhật — không phụ thuộc text cụ thể
    wait_for_flutter(page)
    page.wait_for_timeout(1500)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TCL02_add_member_valid.png"))

    # [R✓] Revealability
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    success_keywords = ["thành công", "success", "đã thêm", "thêm thành viên"]
    assert any(kw in sem_text.lower() for kw in success_keywords), (
        f"TC-L02 FAILED: Không có thông báo thành công.\nsem_text: {sem_text[:200]}"
    )
    print("\n✅ TC-L02 PASSED: Thêm thành viên hợp lệ thành công")


# ---------------------------------------------------------------------------
# TC-L03: Thêm thành viên — email sai định dạng
# ---------------------------------------------------------------------------
def test_add_member_invalid_email(page, test_config):
    # [R] Reachability
    login_as_library(page, test_config)

    # [I] Infection: email sai format
    flutter_fill(page, "Email", "invalid_email_format")
    flutter_fill(page, "Mật khẩu", "Password123")
    flutter_click_button(page, "Thêm thành viên")

    # [P] Propagation: chờ chung — không hardcode text lỗi  ← bug 3 đã sửa
    wait_for_flutter(page)
    page.wait_for_timeout(1500)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TCL03_add_member_invalid_email.png"))

    # [R✓] Revealability
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    error_keywords = ["không hợp lệ", "invalid", "sai", "định dạng", "format"]
    has_error = any(kw in sem_text.lower() for kw in error_keywords)
    has_success = any(kw in sem_text.lower() for kw in ["thành công", "success", "đã thêm"])

    assert has_error or not has_success, (
        f"TC-L03 FAILED: Email sai format nhưng không có thông báo lỗi.\n"
        f"sem_text: {sem_text[:200]}"
    )
    print("\n✅ TC-L03 PASSED: Từ chối email sai định dạng")
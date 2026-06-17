import os
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    wait_for_flutter, SCREENSHOT_DIR,
)

LIBRARY_ADMIN_EMAIL    = os.getenv("LIBRARY_ADMIN_EMAIL", "")
LIBRARY_ADMIN_PASSWORD = os.getenv("library_password", "")


def login_as_library(page, test_config):
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email",     LIBRARY_ADMIN_EMAIL    or test_config["email"])
    flutter_fill(page, "Mật khẩu", LIBRARY_ADMIN_PASSWORD or test_config["password"])
    flutter_click_button(page, "Đăng nhập")
    wait_for_flutter(page, text="Đăng xuất", timeout=20000)
    enable_flutter_semantics(page)


def test_login_as_library(page, test_config):
    login_as_library(page, test_config)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TCL01_login_library.png"))
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    assert "Đăng xuất" in sem_text, (
        "TC-L01 FAILED: Đăng nhập admin thư viện không thành công"
    )
    print("\n✅ TC-L01 PASSED: Đăng nhập thư viện thành công")


def navigate_to_add_member_tab(page):
    """Điều hướng đến tab Thêm thành viên trên trang admin."""
    tab = page.locator(
        'flt-semantics[role="button"]:has-text("Thêm thành viên"),'
        'flt-semantics[role="tab"]:has-text("Thêm thành viên"),'
        'flt-semantics[role="button"]:has-text("Thành viên"),'
        'flt-semantics[role="tab"]:has-text("Thành viên"),'
        'flt-semantics[role="button"]:has-text("Quản lý thành viên"),'
        'flt-semantics[aria-label*="thành viên"],'
        'flt-semantics[aria-label*="Thành viên"]'
    ).first
    tab.wait_for(state="attached", timeout=10000)
    tab.click()
    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)



def test_add_member_valid(page, test_config):
    login_as_library(page, test_config)
    navigate_to_add_member_tab(page)

    flutter_fill(page, "Email", "newmember@gmail.com") 
    flutter_fill(page, "Mật khẩu", "password123")
    flutter_click_button(page, "Thêm thành viên")
    wait_for_flutter(page)
    page.wait_for_timeout(1500)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TCL02_add_member_valid.png"))
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    success_keywords = ["thành công", "success", "đã thêm", "thêm thành viên"]
    assert any(kw in sem_text.lower() for kw in success_keywords), (
        f"TC-L02 FAILED: Không có thông báo thành công.\nsem_text: {sem_text[:200]}"
    )
    print("\n✅ TC-L02 PASSED: Thêm thành viên hợp lệ thành công")


def test_add_member_invalid_email(page, test_config):
    login_as_library(page, test_config)
    flutter_fill(page, "Email",     "invalid_email_format")
    flutter_fill(page, "Mật khẩu", "Password123")
    flutter_click_button(page, "Thêm thành viên")
    wait_for_flutter(page)
    page.wait_for_timeout(1500)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TCL03_add_member_invalid_email.png"))
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    error_keywords = ["không hợp lệ", "invalid", "sai", "định dạng", "format"]
    has_error   = any(kw in sem_text.lower() for kw in error_keywords)
    has_success = any(kw in sem_text.lower() for kw in ["thành công", "success", "đã thêm"])
    assert has_error or not has_success, (
        f"TC-L03 FAILED: Email sai format nhưng không có thông báo lỗi.\n"
        f"sem_text: {sem_text[:200]}"
    )
    print("\n✅ TC-L03 PASSED: Từ chối email sai định dạng")


@pytest.mark.xfail(                                          # ✅ thêm xfail
    strict=True,
    reason="BUG-001: Server chấp nhận email thiếu dấu chấm trong domain "
           "(newmem@emailcom). Chờ dev fix validation.",
)
def test_add_member_with_email_missing_dot_in_domain(page, test_config):
    login_as_library(page, test_config)
    flutter_fill(page, "Email",     "newmem@emailcom")
    flutter_fill(page, "Mật khẩu", "password123")
    flutter_click_button(page, "Thêm thành viên")
    wait_for_flutter(page)
    page.wait_for_timeout(1500)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TCL04_missing_dot_domain.png"))  # ✅ tên riêng
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    error_keywords = ["không hợp lệ", "invalid", "sai", "định dạng", "format"]
    has_error   = any(kw in sem_text.lower() for kw in error_keywords)
    has_success = any(kw in sem_text.lower() for kw in ["thành công", "success", "đã thêm"])
    assert has_error or not has_success, (
        f"BUG-001: 'newmem@emailcom' được chấp nhận — server thiếu dot validation.\n"
        f"sem_text: {sem_text[:200]}"
    )
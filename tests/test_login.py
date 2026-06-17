import os
import pytest
from conftest import (
    enable_flutter_semantics,
    flutter_fill,
    flutter_click_button,
    wait_for_flutter,
    login,
)


# ===========================================================================
# TC-01: Đăng nhập thành công
# REQ-01: email@domain.ext + mật khẩu đúng → chuyển sang trang chủ
# ===========================================================================
def test_login_success(page, test_config):

    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # Nhập thông tin đăng nhập
    flutter_fill(page, "Email", "librarian@library.com")
    flutter_fill(page, "Mật khẩu", "admin123")
    flutter_click_button(page, "Đăng nhập")

    # Smart Wait: chờ trang chủ load — nút "Đăng xuất" phải xuất hiện
    wait_for_flutter(page, text="Đăng xuất", timeout=15000)
    enable_flutter_semantics(page)

    # Chụp màn hình
    screenshot_path = os.path.join(test_config["screenshot_dir"], "TC01_login_success.png")
    page.screenshot(path=screenshot_path)

    # Assert: trang chủ đã load (có nút Đăng xuất)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Đăng xuất" in sem_text, (
        "TC-01 FAILED: Sau đăng nhập không thấy nút 'Đăng xuất'"
    )

    # Assert: tên người dùng xuất hiện trên AppBar
    # REQ-01: Hiển thị tên người dùng + vai trò trên thanh ứng dụng
    assert any(
        keyword in sem_text
        for keyword in ["librarian", "Thủ thư", "Librarian"]
    ), "TC-01 FAILED: Không hiển thị thông tin người dùng trên AppBar"

    print("\n✅ TC-01 PASSED: Đăng nhập thành công")


# ===========================================================================
# TC-02: Đăng nhập thất bại — sai mật khẩu
# REQ-01: Sai mật khẩu → hiển thị "Mật khẩu không đúng"
# ===========================================================================
def test_login_wrong_password(page, test_config):

    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # Nhập email đúng, mật khẩu sai
    flutter_fill(page, "Email", "librarian@library.com")
    flutter_fill(page, "Mật khẩu", "wrongpassword123")
    flutter_click_button(page, "Đăng nhập")

    # Chờ thông báo lỗi xuất hiện
    wait_for_flutter(page, text="không đúng", timeout=10000)
    enable_flutter_semantics(page)

    # Chụp màn hình
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


# ===========================================================================
# TC-03: Đăng nhập thất bại — để trống email và mật khẩu
# REQ-01: Bỏ trống → "Vui lòng nhập email và mật khẩu"
# ===========================================================================
def test_login_empty_fields(page, test_config):
    
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # Không nhập gì, chỉ click đăng nhập
    flutter_click_button(page, "Đăng nhập")

    # Chờ thông báo lỗi
    wait_for_flutter(page, text="Vui lòng", timeout=10000)
    enable_flutter_semantics(page)

    # Chụp màn hình
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


# ===========================================================================
# BONUS B2: Data-Driven Test - Đăng nhập thất bại với nhiều bộ dữ liệu
# ===========================================================================
@pytest.mark.parametrize(
    "email, password, expected_error",
    [
        ("librarian@library.com", "wrongpassword123", "mật khẩu"),
        ("noone@notexist.com", "anypassword", "thành viên"),
        ("", "", "Vui lòng"),
    ],
)

def test_login_failures_data_driven(page, test_config, email, password, expected_error):
    """
    Bonus B2: Kiểm thử hướng dữ liệu (data-driven) cho các kịch bản đăng nhập lỗi.
    """
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    flutter_fill(page, "Email", email)
    flutter_fill(page, "Mật khẩu", password)
    flutter_click_button(page, "Đăng nhập")

    wait_for_flutter(page, text=expected_error, timeout=10000)
    enable_flutter_semantics(page)

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert expected_error in sem_text or expected_error.lower() in sem_text.lower(), (
        f"Expected error '{expected_error}' not found in semantics text: {sem_text[:200]}"
    )
    print(f"\n✅ Data-driven login failure test passed for credentials: '{email}' / '{password}'")

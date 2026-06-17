
import os
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, SCREENSHOT_DIR, wait_for_flutter,
)

def test_logout(page, test_config):
    """TC-11: Logout success (*Đăng xuất thành công*)"""
    # [R] Reachability
    login(page, test_config)

    # [I] Infection: click nút Đăng xuất
    flutter_click_button(page, "Đăng xuất")

    # [P] Propagation: chờ trang login xuất hiện lại
    wait_for_flutter(page, text="Đăng nhập")
    enable_flutter_semantics(page)

    # Screenshot before assert — luôn có bằng chứng dù pass hay fail
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC11_logout.png"))

    # [R✓] Revealability
    assert (
        page.locator('flt-semantics[role="button"]:has-text("Đăng nhập")').count() > 0
        or page.locator('input[aria-label="Email"]').count() > 0
    ), "TC-11 FAILED: Sau khi đăng xuất không quay về trang đăng nhập"


def test_switch_language_to_english(page, test_config):
    """TC-12: Switch language to English (*Chuyển ngôn ngữ sang tiếng Anh*)"""
    # [R] Reachability
    login(page, test_config)

    # [I] Infection: click nút chuyển ngôn ngữ
    flutter_click_button(page, "EN")

    # [P] Propagation: chờ UI cập nhật sang tiếng Anh
    wait_for_flutter(page, text="Borrow")
    enable_flutter_semantics(page)

    # Screenshot before assert 
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC12_switch_language_en.png"))

    # [R✓] Revealability
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents()) 
    assert (
        "Logout" in sem_text
        or "Borrow" in sem_text
        or "Library" in sem_text
    ), f"TC-12 FAILED: UI không chuyển sang tiếng Anh.\nsem_text: {sem_text[:200]}"

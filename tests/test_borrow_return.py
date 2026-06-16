import os
import re
import sys
import pytest
from conftest import (
    enable_flutter_semantics,
    flutter_fill,
    flutter_click_button,
    wait_for_flutter,
    SCREENSHOT_DIR,
)

BASE_URL = "https://stqa.rbc.vn"


def open_image(path):
    try:
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            import subprocess
            subprocess.Popen(["open", path])
        else:
            import subprocess
            subprocess.Popen(["xdg-open", path])
    except Exception:
        pass


def get_semantics_text(page):
    try:
        return page.evaluate("""() => {
            const elements = document.querySelectorAll('flt-semantics');
            const texts = [];
            for (const el of elements) {
                const label = el.getAttribute('aria-label');
                if (label) texts.push(label);
                if (el.textContent) texts.push(el.textContent);
            }
            return texts.join(' ');
        }""")
    except Exception:
        return ""


def my_login(page, email, password):
    page.goto(BASE_URL, wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    email_field = page.locator('input[aria-label="Email"]').first
    email_field.wait_for(state="attached", timeout=15000)
    email_field.click()
    active = page.locator("flt-text-editing-host input, flt-text-editing-host textarea")
    try:
        active.first.wait_for(state="attached", timeout=3000)
        active.first.fill(email)
    except Exception:
        email_field.fill(email)

    pw_field = page.locator('input[aria-label="Mật khẩu"]').first
    pw_field.wait_for(state="attached", timeout=10000)
    pw_field.click()
    try:
        active.first.wait_for(state="attached", timeout=3000)
        active.first.fill(password)
    except Exception:
        pw_field.fill(password)

    page.locator('flt-semantics[role="button"]:has-text("Đăng nhập")').click()

    for text in ["Đăng xuất", "Mượn sách này", "Có sẵn", "Thư viện", "Sách"]:
        try:
            page.locator(
                f'flt-semantics:has-text("{text}"), flt-semantics[aria-label*="{text}"]'
            ).first.wait_for(state="attached", timeout=10000)
            break
        except Exception:
            continue

    enable_flutter_semantics(page)


def navigate_to_muon_tra(page):
    muon_tra = page.locator(
        'flt-semantics[role="tab"][aria-label="Mượn / Trả"],'
        'flt-semantics[role="tab"][aria-label*="Mượn"],'
        'flt-semantics[role="tab"]:has-text("Mượn"),'
        'flt-semantics[role="tab"]:has-text("Trả"),'
        'flt-semantics[aria-label="Mượn / Trả"],'
        'flt-semantics:has-text("Mượn / Trả")'
    ).first
    muon_tra.wait_for(state="visible", timeout=30000)
    muon_tra.click()
    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)


def test_borrow_book(page, test_config):
    my_login(page, "dam.tran@email.com", "password123")

    borrow_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Mượn sách này")'
    ).first
    borrow_btn.wait_for(state="visible", timeout=30000)
    borrow_btn.click()

    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)
    flutter_click_button(page, "Mượn")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    try:
        wait_for_flutter(page, text="thành công")
    except Exception:
        wait_for_flutter(page, text="Đang mượn")

    screenshot = os.path.join(SCREENSHOT_DIR, "TC08_borrow_book.png")
    page.screenshot(path=screenshot)
    open_image(screenshot)

    sem_text = get_semantics_text(page)
    assert "thành công" in sem_text or "Đang mượn" in sem_text, (
        f"TC-08 FAILED: {sem_text[:300]}"
    )


def test_view_borrowed_books(page, test_config):
    my_login(page, "ba.nguyen@email.com", "password123")
    navigate_to_muon_tra(page)

    borrowed_book_indicator = page.locator(
        'flt-semantics[aria-label*="Đang mượn"],'
        'flt-semantics[role="button"]:has-text("Trả sách")'
    ).first
    borrowed_book_indicator.wait_for(state="visible", timeout=10000)

    screenshot = os.path.join(SCREENSHOT_DIR, "TC09_view_borrowed_books.png")
    page.screenshot(path=screenshot)
    open_image(screenshot)

    sem_text = get_semantics_text(page)
    assert (
        borrowed_book_indicator.is_visible()
        or "Đang mượn" in sem_text
        or "Trả sách" in sem_text
        or "BR001" in sem_text
    ), f"TC-09 FAILED: {sem_text[:300]}"


def test_return_book(page, test_config):
    my_login(page, "ba.nguyen@email.com", "password123")
    navigate_to_muon_tra(page)

    return_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Trả sách")'
    ).first
    return_btn.wait_for(state="visible", timeout=15000)
    return_btn.click()
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    sem_text_after = get_semantics_text(page)
    if "Xác nhận" in sem_text_after:
        try:
            confirm = page.locator('flt-semantics[role="button"]:has-text("Trả")').last
            confirm.click()
            page.wait_for_timeout(2000)
            enable_flutter_semantics(page)
        except Exception:
            pass

    try:
        wait_for_flutter(page, text="thành công")
    except Exception:
        wait_for_flutter(page, text="Có sẵn")

    screenshot = os.path.join(SCREENSHOT_DIR, "TC10_return_book.png")
    page.screenshot(path=screenshot)
    open_image(screenshot)

    sem_text = get_semantics_text(page)
    assert (
        "thành công" in sem_text
        or "Có sẵn" in sem_text
        or "Đã trả" in sem_text
        or "trả thành công" in sem_text.lower()
    ), f"TC-10 FAILED: {sem_text[:300]}"


def test_fix_borrow_limit_bug_automated(page, test_config):
    my_login(page, "cu.le@email.com", "password123")

    borrow_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Mượn sách này")'
    ).first
    borrow_btn.wait_for(state="visible", timeout=30000)
    borrow_btn.click()

    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)
    flutter_click_button(page, "Mượn")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    screenshot = os.path.join(SCREENSHOT_DIR, "TC11_borrow_limit_bug.png")
    page.screenshot(path=screenshot)
    open_image(screenshot)

    sem_text = get_semantics_text(page)
    assert "thành công" not in sem_text, (
        f"TC-11 FAILED: {sem_text[:300]}"
    )
    print("Xác nhận tự động: Hệ thống đã chặn mượn cuốn sách thứ 4 thành công.")


def test_borrow_with_suspended_member(page, test_config):
    my_login(page, "cu.le@email.com", "password123")

    borrow_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Mượn sách này")'
    ).first
    borrow_btn.wait_for(state="visible", timeout=30000)
    borrow_btn.click()

    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)
    flutter_click_button(page, "Mượn")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    screenshot = os.path.join(SCREENSHOT_DIR, "TC12_borrow_suspended_member.png")
    page.screenshot(path=screenshot)
    open_image(screenshot)

    sem_text = get_semantics_text(page)
    assert "tạm ngưng" in sem_text.lower() or "khóa" in sem_text.lower() or "từ chối" in sem_text.lower() or "hết hạn" in sem_text.lower(), (
        f"TC-12 FAILED: {sem_text[:300]}"
    )
    assert "thành công" not in sem_text.lower(), (
        f"TC-12 FAILED: {sem_text[:300]}"
    )


def test_borrow_with_expired_member(page, test_config):
    my_login(page, "binh.pham@email.com", "password123")

    borrow_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Mượn sách này")'
    ).first
    borrow_btn.wait_for(state="visible", timeout=30000)
    borrow_btn.click()

    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)
    flutter_click_button(page, "Mượn")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    screenshot = os.path.join(SCREENSHOT_DIR, "TC13_borrow_expired_member.png")
    page.screenshot(path=screenshot)
    open_image(screenshot)

    sem_text = get_semantics_text(page)
    assert "hết hạn" in sem_text.lower() or "lỗi" in sem_text.lower(), (
        f"TC-13 FAILED: {sem_text[:300]}"
    )
    assert "thành công" not in sem_text.lower(), (
        f"TC-13 FAILED: {sem_text[:300]}"
    )

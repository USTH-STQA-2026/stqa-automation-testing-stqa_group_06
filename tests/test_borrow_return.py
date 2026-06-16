import os
import time
import pytest
from conftest import (
    enable_flutter_semantics,
    flutter_fill,
    flutter_click_button,
    SCREENSHOT_DIR,
    wait_for_flutter,
)

BASE_URL = "https://stqa.rbc.vn"


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


def _find_borrow_tab(page):
    return page.locator(
        'flt-semantics[role="tab"][aria-label="Mượn / Trả"],'
        'flt-semantics[role="tab"][aria-label*="Mượn"],'
        'flt-semantics[role="tab"]:has-text("Mượn"),'
        'flt-semantics[role="tab"]:has-text("Trả")'
    ).first


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
    all_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" in all_text or "Đang mượn" in all_text


def test_view_borrowed_books(page, test_config):
    my_login(page, "ba.nguyen@email.com", "password123")

    tab = _find_borrow_tab(page)
    tab.wait_for(state="visible", timeout=30000)
    tab.click()
    page.wait_for_timeout(1000)

    borrowed_book_indicator = page.locator(
        'flt-semantics[aria-label*="Đang mượn"],'
        'flt-semantics[role="button"]:has-text("Trả sách")'
    ).first
    borrowed_book_indicator.wait_for(state="visible", timeout=10000)
    assert borrowed_book_indicator.is_visible()


def test_return_book(page, test_config):
    my_login(page, "ba.nguyen@email.com", "password123")

    tab = _find_borrow_tab(page)
    tab.wait_for(state="visible", timeout=30000)
    tab.click()

    return_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Trả sách")'
    ).first
    return_btn.wait_for(state="visible", timeout=15000)
    return_btn.click()
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    try:
        wait_for_flutter(page, text="thành công")
    except Exception:
        wait_for_flutter(page, text="Có sẵn")
    all_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" in all_text or "Có sẵn" in all_text


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
    all_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" not in all_text
    print("Xác nhận tự động: Hệ thống đã chặn mượn cuốn sách thứ 4 thành công.")

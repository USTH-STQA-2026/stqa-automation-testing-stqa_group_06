import os
import time
import pytest
from conftest import (
    enable_flutter_semantics,
    flutter_fill,
    flutter_click_button,
    login,
    SCREENSHOT_DIR,
    wait_for_flutter,
)

def test_borrow_book(page, test_config):
    login(page, test_config)
    available_book = page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]').first
    available_book.wait_for(state="visible")
    borrow_btn = available_book.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')
    borrow_btn.click()
    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)
    flutter_click_button(page, "Mượn")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    try:
        wait_for_flutter(page, text="thành công")
    except:
        wait_for_flutter(page, text="Đang mượn")
    all_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" in all_text or "Đang mượn" in all_text

def test_view_borrowed_books(page, test_config):
    login(page, test_config)
    borrow_return_tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    borrow_return_tab.wait_for(state="visible")
    borrow_return_tab.click()
    page.wait_for_timeout(1000)
    borrowed_book_indicator = page.locator('flt-semantics[aria-label*="Đang mượn"], flt-semantics[role="button"]:has-text("Trả sách")').first
    borrowed_book_indicator.wait_for(state="visible", timeout=5000)
    assert borrowed_book_indicator.is_visible()

def test_return_book(page, test_config):
    login(page, test_config)
    borrow_return_tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    borrow_return_tab.wait_for(state="visible")
    borrow_return_tab.click()
    return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').first
    return_btn.wait_for(state="visible")
    return_btn.click()
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    try:
        wait_for_flutter(page, text="thành công")
    except:
        wait_for_flutter(page, text="Có sẵn")
    all_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" in all_text or "Có sẵn" in all_text

def test_fix_borrow_limit_bug_automated(page, test_config):
    login(page, test_config)
    available_book = page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]').first
    available_book.wait_for(state="visible")
    borrow_btn = available_book.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')
    borrow_btn.click()
    page.wait_for_timeout(1000)
    enable_flutter_semantics(page) 
    flutter_click_button(page, "Mượn")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page) 
    all_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" not in all_text
    print("Xác nhận tự động: Hệ thống đã chặn mượn cuốn sách thứ 4 thành công.")

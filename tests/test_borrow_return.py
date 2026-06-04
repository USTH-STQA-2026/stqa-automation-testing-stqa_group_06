"""
Borrow & Return Tests (*Kiểm thử Mượn & Trả sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 3 test cases in this file. (*Sinh viên cần hoàn thành TẤT CẢ 3 test case trong file này.*)

Hints (*Gợi ý*):
- Use login() helper to log in (*Dùng login() helper để đăng nhập*)
- "Mượn / Trả" tab: role="tab", aria-label="Mượn / Trả"
- Available books have "Có sẵn" in aria-label, borrowed books have "Đang mượn" (*Sách "Có sẵn" có aria-label chứa "Có sẵn", sách "Đang mượn" chứa "Đang mượn"*)
- Borrow button: 'flt-semantics[role="button"]:has-text("Mượn sách này")' (*Nút mượn*)
- After clicking "Mượn sách này", a confirmation dialog appears — click "Mượn" again (*Sau khi click "Mượn sách này" sẽ hiện dialog xác nhận — cần click nút "Mượn" lần nữa*)
- Return button: 'flt-semantics[role="button"]:has-text("Trả sách")' (*Nút trả*)
"""

import os
import time
import pytest
from conftest import (
    enable_flutter_semantics,
    flutter_fill,
    flutter_click_button,
    login,
    SCREENSHOT_DIR,
)
from conftest import wait_for_flutter

def test_borrow_book(page, test_config):
    """TC-08: Borrow an available book (*Mượn sách có trạng thái 'Có sẵn'*)
    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
    Log in → find an "Available" book → click "Mượn sách này" → confirm dialog → verify book status changes to "Borrowed".
    (*Đăng nhập → tìm sách "Có sẵn" → click "Mượn sách này" → xác nhận dialog → kiểm tra sách chuyển sang trạng thái "Đang mượn".*)

    Suggested steps (*Gợi ý các bước*):
    1. login(page, test_config)
    2. Find available book: page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]') (*Tìm sách Có sẵn*)
    3. Click "Mượn sách này" button inside that book card (*Click nút "Mượn sách này" trong sách đó*)
    4. Wait for confirmation dialog, re-enable semantics (*Đợi dialog xác nhận, bật lại semantics*)
    5. Click "Mượn" button (confirm button in dialog) (*Click nút "Mượn" — nút xác nhận trong dialog*)
    6. Assert: "Đang mượn" or "thành công" appears (*Assert: "Đang mượn" hoặc "thành công" xuất hiện*)
    """
    # 1. login(page, test_config)
    login(page, test_config)
    
    # 2. Find available book: page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]') (*Tìm sách Có sẵn*)
    available_book = page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]').first
    available_book.wait_for(state="visible")
    
    # 3. Click "Mượn sách này" button inside that book card (*Click nút "Mượn sách này" trong sách đó*)
    borrow_btn = available_book.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')
    borrow_btn.click()
    
    # 4. Wait for confirmation dialog, re-enable semantics (*Đợi dialog xác nhận, bật lại semantics*)
    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)
    
    # 5. Click "Mượn" button (confirm button in dialog) (*Click nút "Mượn" — nút xác nhận trong dialog*)
    flutter_click_button(page, "Mượn")
    
    # 6. Assert: "Đang mượn" or "thành công" appears (*Assert: "Đang mượn" hoặc "thành công" xuất hiện*)
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    
    try:
        wait_for_flutter(page, text="thành công")
    except:
        wait_for_flutter(page, text="Đang mượn")


    all_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" in all_text or "Đang mượn" in all_text
def test_view_borrowed_books(page, test_config):
    """TC-09: View borrowed books list (*Xem danh sách sách đang mượn — tab Mượn / Trả*)
    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
    Log in → switch to "Mượn / Trả" tab → verify borrowed books are shown.
    (*Đăng nhập → chuyển sang tab "Mượn / Trả" → kiểm tra có sách đang mượn.*)

    Hints (*Gợi ý*):
    - Click tab: page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    - Verify: books with "Đang mượn" in aria-label, or "Trả sách" button exists (*Kiểm tra: có sách với aria-label chứa "Đang mượn" hoặc có nút "Trả sách"*)
    """
    # 1. Log in
    login(page, test_config)
    
    # 2. Click tab: page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    borrow_return_tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    borrow_return_tab.wait_for(state="visible")
    borrow_return_tab.click()
    
    # 3. Verify: books with "Đang mượn" in aria-label, or "Trả sách" button exists
    page.wait_for_timeout(1000)
    borrowed_book_indicator = page.locator('flt-semantics[aria-label*="Đang mượn"], flt-semantics[role="button"]:has-text("Trả sách")').first
    borrowed_book_indicator.wait_for(state="visible", timeout=5000)
    assert borrowed_book_indicator.is_visible()

def test_return_book(page, test_config):
    """TC-10: Return a borrowed book (*Trả sách đang mượn*)
    🔴 NOT COMPLETED (*CHƯA HOÀN THÀNH*)

    Description (*Mô tả*):
    Log in → go to "Mượn / Trả" tab → click "Trả sách" → verify book is returned.
    (*Đăng nhập → tab "Mượn / Trả" → click "Trả sách" → kiểm tra sách được trả.*)

    Hints (*Gợi ý*):
    - Switch to "Mượn / Trả" tab (*Chuyển tab "Mượn / Trả"*)
    - Find return button: page.locator('flt-semantics[role="button"]:has-text("Trả sách")') (*Tìm nút "Trả sách"*)
    - Click and verify status change or success message (*Click và kiểm tra sách chuyển trạng thái hoặc có thông báo thành công*)
    """
    # 1. Log in
    login(page, test_config)
    
    # 2. Switch to "Mượn / Trả" tab
    borrow_return_tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    borrow_return_tab.wait_for(state="visible")
    borrow_return_tab.click()
    
    # 3. Find return button: page.locator('flt-semantics[role="button"]:has-text("Trả sách")')
    return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').first
    return_btn.wait_for(state="visible")
  
    # 4. Click and verify status change or success message
    return_btn.click()

    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    try:
        wait_for_flutter(page, text="thành công")
    except:
        wait_for_flutter(page, text="Có sẵn")

    # Kiểm tra lại trong text tổng
    all_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" in all_text or "Có sẵn" in all_text, "Trả sách thất bại: không tìm thấy trạng thái cập nhật"
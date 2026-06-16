import os
import pytest
from conftest import (
    SCREENSHOT_DIR,
    enable_flutter_semantics,
    flutter_click_button,
    login,
    wait_for_flutter,
)

MAX_BORROW_LIMIT   = 3
MAX_RETURN_SAFETY  = 20
API_SETTLE_MS      = 2_000
POST_BORROW_MS     = 3_000

def _tab(page, label: str):
    return page.locator(f'flt-semantics[role="tab"][aria-label="{label}"]')

def _available_book(page):
    return page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]').first

def _return_buttons(page):
    return page.locator('flt-semantics[role="button"]:has-text("Trả sách")')

def _borrow_this_btn(book_el):
    return book_el.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')

def _confirm_borrow_btn(page):
    return page.locator('flt-semantics[role="button"]:has-text("Mượn")')

def _borrow_success_indicator(page):
    return page.locator(
        'flt-semantics[aria-label*="thành công"],'
        'flt-semantics[aria-label*="Đang mượn"]'
    ).first

def _borrowed_book_indicator(page):
    return page.locator(
        'flt-semantics[aria-label*="Đang mượn"],'
        'flt-semantics[role="button"]:has-text("Trả sách")'
    ).first

def _borrow_limit_error(page):
    return page.locator(
        'flt-semantics[aria-label*="giới hạn"],'
        'flt-semantics[aria-label*="tối đa"],'
        'flt-semantics[aria-label*="vượt quá"]'
    ).first

def _go_home(page):
    tab = _tab(page, "Trang chủ")
    tab.wait_for(state="attached", timeout=10_000)
    tab.click()
    page.wait_for_timeout(1_000)
    enable_flutter_semantics(page)

def _go_borrow_return(page):
    tab = _tab(page, "Mượn / Trả")
    tab.wait_for(state="attached", timeout=10_000)
    tab.click()
    page.wait_for_timeout(API_SETTLE_MS)
    enable_flutter_semantics(page)

def _clear_all_borrowed_books(page):
    _go_borrow_return(page)
    for attempt in range(MAX_RETURN_SAFETY):
        buttons = _return_buttons(page)
        if buttons.count() == 0:
            return
        buttons.first.click()
        page.wait_for_timeout(API_SETTLE_MS)
        enable_flutter_semantics(page)
    remaining = _return_buttons(page).count()
    if remaining > 0:
        raise RuntimeError(f"Không dọn sạch được sách sau {MAX_RETURN_SAFETY} lần thử.")

def _borrow_one_book(page):
    book = _available_book(page)
    book.wait_for(state="attached", timeout=10_000)
    _borrow_this_btn(book).click()
    _confirm_borrow_btn(page).wait_for(state="attached", timeout=5_000)
    flutter_click_button(page, "Mượn")
    page.wait_for_timeout(POST_BORROW_MS)
    try:
        wait_for_flutter(page, text="thành công")
    except Exception:
        wait_for_flutter(page, text="Đang mượn")
    enable_flutter_semantics(page)

def test_borrow_book(page, test_config):
    login(page, test_config)
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(3_000)
    enable_flutter_semantics(page)
    _clear_all_borrowed_books(page)
    _go_home(page)
    _borrow_one_book(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC_borrow_book.png"))
    indicator = _borrow_success_indicator(page)
    assert indicator.is_attached(), "TC_borrow_book FAILED."

def test_view_borrowed_books(page, test_config):
    login(page, test_config)
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(3_000)
    enable_flutter_semantics(page)
    _clear_all_borrowed_books(page)
    _go_home(page)
    _borrow_one_book(page)
    _go_borrow_return(page)
    indicator = _borrowed_book_indicator(page)
    indicator.wait_for(state="attached", timeout=10_000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC_view_borrowed_books.png"))
    assert indicator.is_attached(), "TC_view_borrowed_books FAILED."

@pytest.mark.xfail(strict=True, reason="BUG-02: Hệ thống cho phép mượn cuốn thứ 4 vượt giới hạn 3 cuốn.")
def test_borrow_limit_enforced(page, test_config):
    login(page, test_config)
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(3_000)
    enable_flutter_semantics(page)
    _clear_all_borrowed_books(page)
    for _ in range(MAX_BORROW_LIMIT):
        _go_home(page)
        _borrow_one_book(page)
    _go_home(page)
    book = _available_book(page)
    book.wait_for(state="attached", timeout=10_000)
    _borrow_this_btn(book).click()
    _confirm_borrow_btn(page).wait_for(state="attached", timeout=5_000)
    flutter_click_button(page, "Mượn")
    page.wait_for_timeout(POST_BORROW_MS)
   except Exception as e:
    print(f"[WARN] Không thấy text 'giới hạn': {e}")
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC_borrow_limit.png"))
    error_toast = _borrow_limit_error(page)
    assert error_toast.is_attached(), "BUG-02 FAILED."

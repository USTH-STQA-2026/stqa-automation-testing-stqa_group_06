import os
import pytest
from conftest import (
    enable_flutter_semantics,
    wait_for_flutter,
    flutter_click_button,
    login,
    SCREENSHOT_DIR,
)

def _borrow_one_book(page, test_config):
    login(page, test_config)
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)

    available_book = page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]').first
    available_book.wait_for(state="attached", timeout=10000)
    borrow_btn = available_book.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')
    borrow_btn.click()

    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)
    flutter_click_button(page, "Mượn")

    # ✅ Cùng pattern — chờ Flutter ổn định trước khi tiếp tục
    page.wait_for_timeout(3000)
    try:
        wait_for_flutter(page, text="thành công")
    except Exception:
        wait_for_flutter(page, text="Đang mượn")
    enable_flutter_semantics(page)


def test_borrow_book(page, test_config):
    login(page, test_config)
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(3000)
    page.evaluate("() => window.scrollTo(0, 0)")
    enable_flutter_semantics(page)

    available_book = page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]').first
    available_book.wait_for(state="attached", timeout=10000)
    borrow_btn = available_book.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')
    borrow_btn.click()

    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)
    flutter_click_button(page, "Mượn")

    # ✅ THAY: không gọi enable_flutter_semantics ngay sau action
    # Dùng wait_for_flutter chờ UI ổn định trước — tránh crash mid-render
    page.wait_for_timeout(3000)          # tăng từ 2000 → 3000: cho Flutter re-render xong
    try:
        wait_for_flutter(page, text="thành công")   # chờ text xuất hiện = render xong
    except Exception:
        wait_for_flutter(page, text="Đang mượn")    # fallback

    # Chỉ gọi enable_flutter_semantics SAU KHI Flutter đã render xong
    enable_flutter_semantics(page)       # ✅ an toàn — UI đã ổn định

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC_borrow_book.png"))
    all_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "thành công" in all_text or "Đang mượn" in all_text, (
        f"Mượn sách thất bại.\nsem_text: {all_text[:200]}"
    )


def test_view_borrowed_books(page, test_config):
    # Setup: mượn 1 cuốn trước — tạo state cần thiết
    _borrow_one_book(page, test_config)         # ← thêm dòng này

    borrow_return_tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    borrow_return_tab.wait_for(state="attached", timeout=10000)
    borrow_return_tab.click()

    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)

    borrowed_book_indicator = page.locator(
        'flt-semantics[aria-label*="Đang mượn"], flt-semantics[role="button"]:has-text("Trả sách")'
    ).first
    borrowed_book_indicator.wait_for(state="attached", timeout=10000)

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC_view_borrowed_books.png"))
    assert borrowed_book_indicator.is_visible(), (
        "Không thấy sách đang mượn hoặc nút Trả sách"
    )


def test_borrow_limit_enforced(page, test_config):
    """TC-BR: Hệ thống chặn mượn quá 3 cuốn cùng lúc.

    Precondition: Account test phải đang mượn đúng 3 cuốn.
    Nếu chưa đủ 3 cuốn → test skip với thông báo rõ ràng.
    """
    login(page, test_config)
    enable_flutter_semantics(page)

    # Kiểm tra precondition TRƯỚC xfail logic
    all_text = " ".join(page.locator("flt-semantics").all_text_contents())
    borrowed_count = all_text.count("Đang mượn")
    if borrowed_count < 3:
        pytest.skip(
            f"Precondition chưa đủ: đang mượn {borrowed_count}/3 cuốn. "
            f"Cần mượn đủ 3 cuốn trước khi chạy test này."
        )

    # Chỉ chạy đến đây khi borrowed_count == 3
    _test_borrow_limit_core(page, test_config)


@pytest.mark.xfail(
    strict=True,
    reason="BUG-02: Hệ thống cho phép mượn cuốn thứ 4 vượt giới hạn 3 cuốn.",
)
def _test_borrow_limit_core(page, test_config):
    available_book = page.locator('flt-semantics[role="group"][aria-label*="Có sẵn"]').first
    available_book.wait_for(state="attached", timeout=10000)
    borrow_btn = available_book.locator('flt-semantics[role="button"]:has-text("Mượn sách này")')
    borrow_btn.click()

    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)
    flutter_click_button(page, "Mượn")

    # ✅ Chờ Flutter render xong TRƯỚC khi gọi enable_flutter_semantics
    page.wait_for_timeout(3000)
    try:
        wait_for_flutter(page, text="thành công")
    except Exception:
        wait_for_flutter(page, text="giới hạn")
    enable_flutter_semantics(page)       # ✅ an toàn — UI đã ổn định

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC_borrow_limit.png"))
    all_text = " ".join(page.locator("flt-semantics").all_text_contents())
    limit_keywords = ["giới hạn", "tối đa", "không thể mượn", "vượt quá", "3 cuốn"]
    has_limit_msg  = any(kw in all_text.lower() for kw in limit_keywords)
    still_borrowed = all_text.count("Đang mượn") == 3

    assert has_limit_msg or still_borrowed, (
        f"BUG-02: Hệ thống cho phép mượn cuốn thứ 4 — vượt giới hạn 3 cuốn!\n"
        f"sem_text: {all_text[:200]}"
    )
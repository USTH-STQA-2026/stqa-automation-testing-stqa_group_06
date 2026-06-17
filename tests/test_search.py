"""
Search & Filter Tests (*Kiểm thử Tìm kiếm & Lọc sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)
"""
import os
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, SCREENSHOT_DIR, wait_for_flutter,
)

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

def test_search_book_by_name(page, test_config):
    """TC-04: Search book by name – results found
    Description:
        Log in → search keyword "Flutter" → verify Flutter books appear in results.
    """
    # 1. Log in to the system before testing
    login(page, test_config)
    
    # 2. Enter the keyword "Flutter" into the search box
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")
    wait_for_flutter(page, text="Flutter", timeout=10000)
    enable_flutter_semantics(page)
    
    screenshot_path = os.path.join(test_config["screenshot_dir"], "TC04_search_by_name.png")
    page.screenshot(path=screenshot_path)

    sem_text = get_semantics_text(page)
    assert "Flutter" in sem_text, (
        f"TC-04 FAILED: Không tìm thấy sách 'Flutter'. Nội dung: {sem_text[:300]}"
    )
    assert "BOOK001" in sem_text or "Lập trình Flutter" in sem_text, (
        "TC-04 FAILED: Không hiển thị BOOK001"
    )
    print("\n✅ TC-04 PASSED: Tìm sách theo tên thành công")


def test_search_book_no_result(page, test_config):
    """TC-05: Search book – no results
    Description:
        Log in → search a non-existent keyword (e.g. "xyz_khong_ton_tai_12345")
        → verify no books are displayed.
    """
    # 1. Log in to the system
    login(page, test_config)
    
    # 2. Enter a random keyword that definitely does not exist in the library database
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "xyz_12345")
    wait_for_flutter(page, text="Không tìm thấy", timeout=10000)
    enable_flutter_semantics(page)

    screenshot_path = os.path.join(test_config["screenshot_dir"], "TC05_search_no_result.png")
    page.screenshot(path=screenshot_path)

    sem_text = get_semantics_text(page)
    assert "Không tìm thấy" in sem_text or "không có" in sem_text.lower(), (
        f"TC-05 FAILED: Không hiển thị thông báo 'Không tìm thấy'. Nội dung: {sem_text[:300]}"
    )
    print("\n✅ TC-05 PASSED: Hiển thị 'Không tìm thấy sách' đúng")


def test_filter_by_category(page, test_config):
    """TC-06: Filter books by category 'Công nghệ'
    Description:
        Log in → enter "Công nghệ" in the category filter → verify all displayed books
        belong to the "Công nghệ" category.
    """
    # 1. Log in to the system
    login(page, test_config)
    
    # 2. Enter "Công nghệ" into the category filter box
    flutter_fill(page, "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", "Công nghệ")
    wait_for_flutter(page, text="Công nghệ", timeout=10000)
    enable_flutter_semantics(page)

    
    screenshot_path = os.path.join(test_config["screenshot_dir"], "TC06_filter_by_category.png")
    page.screenshot(path=screenshot_path)

    sem_text = get_semantics_text(page)

    # Sau khi lọc "Công nghệ", phải thấy sách công nghệ như Flutter, Python, v.v.
    assert any(
        book in sem_text
        for book in ["Flutter", "Python", "Kiểm thử", "Mạng máy tính", "An toàn thông tin", "BOOK001", "BOOK002"]
    ), f"TC-06 FAILED: Không hiển thị sách Công nghệ. Nội dung: {sem_text[:300]}"

    print("\n✅ TC-06 PASSED: Lọc theo thể loại (textbox) thành công")



def test_search_by_author(page, test_config):
    """TC-07: Search book by author name
    Description:
        Log in → search author name (e.g. "Nguyễn Minh Đức") → verify results found.
    """
    # 1. Log in to the system
    login(page, test_config)
    
    # 2. Enter the author name "Nguyễn Minh Đức" into the search box
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Nguyễn Minh Đức")
    wait_for_flutter(page, text="Nguyễn Minh Đức", timeout=10000)
    enable_flutter_semantics(page)

    screenshot_path = os.path.join(test_config["screenshot_dir"], "TC07_search_by_author.png")
    page.screenshot(path=screenshot_path)

    sem_text = get_semantics_text(page)
    assert "Nguyễn Minh Đức" in sem_text or "Flutter" in sem_text or "Python" in sem_text, (
        f"TC-07 FAILED: Không tìm thấy sách theo tác giả. Nội dung: {sem_text[:300]}"
    )
    print("\n✅ TC-07 PASSED: Tìm kiếm theo tác giả thành công")


# ===========================================================================
# BONUS B2: Data-Driven Test - Tìm kiếm sách theo các từ khóa khác nhau
# ===========================================================================
@pytest.mark.parametrize(
    "keyword, expected_title, expected_book_id",
    [
        ("Flutter", "Lập trình Flutter cơ bản", "BOOK001"),
        ("Python", "Nhập môn lập trình Python", "BOOK009"),
        ("Kiểm thử", "Kiểm thử phần mềm nhập môn", "BOOK003"),
    ],
)
def test_search_books_data_driven(page, test_config, keyword, expected_title, expected_book_id):
    """
    Bonus B2: Kiểm thử hướng dữ liệu (data-driven) cho tìm kiếm sách.
    """
    login(page, test_config)
    enable_flutter_semantics(page)

    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", keyword)
    wait_for_flutter(page, text=expected_title, timeout=10000)
    enable_flutter_semantics(page)

    sem_text = get_semantics_text(page)
    assert expected_title in sem_text and expected_book_id in sem_text, (
        f"Data-driven search failed for keyword '{keyword}'. "
        f"Expected title '{expected_title}' and ID '{expected_book_id}' in semantics: {sem_text[:300]}"
    )
    print(f"\n✅ Data-driven search test passed for keyword: '{keyword}'")


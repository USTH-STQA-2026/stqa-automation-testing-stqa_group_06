"""
Search & Filter Tests (*Kiểm thử Tìm kiếm & Lọc sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)
"""
import os
import time
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, SCREENSHOT_DIR,
)

def test_search_book_by_name(page, test_config):
    """TC-04: Search book by name – results found
    Description:
        Log in → search keyword "Flutter" → verify Flutter books appear in results.
    """
    # 1. Log in to the system before testing
    login(page, test_config)
    
    # 2. Enter the keyword "Flutter" into the search box
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")
    
    # Wait 1 second for the system to filter and update the book list on the UI
    page.wait_for_timeout(1000)
    
    # 3. Verify that the count of elements containing "Flutter" in the aria-label is greater than 0
    assert page.locator('flt-semantics[aria-label*="Flutter"]').count() > 0


def test_search_book_no_result(page, test_config):
    """TC-05: Search book – no results
    Description:
        Log in → search a non-existent keyword (e.g. "xyz_khong_ton_tai_12345")
        → verify no books are displayed.
    """
    # 1. Log in to the system
    login(page, test_config)
    
    # 2. Enter a random keyword that definitely does not exist in the library database
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "xyz_khong_ton_tai_12345")
    page.wait_for_timeout(1000)
    
    # 3. Verify that no book cards (role="group" and aria-label containing "Mã: BOOK") are displayed
    assert page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]').count() == 0


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
    page.wait_for_timeout(1000)
    
    # 3. Get the list of all book cards currently appearing on the screen
    books_locator = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    book_count = books_locator.count()
    
    # Ensure there is at least 1 book displayed to run the verification loop
    assert book_count > 0, "No books found belonging to the 'Công nghệ' category to verify."
    
    # 4. Loop through each book card to verify that its aria-label attribute contains "Công nghệ"
    for i in range(book_count):
        aria_label = books_locator.nth(i).get_attribute("aria-label")
        assert "Công nghệ" in aria_label, f"Error: Book #{i+1} does not belong to the 'Công nghệ' category. Details: {aria_label}"


def test_search_by_author(page, test_config):
    """TC-07: Search book by author name
    Description:
        Log in → search author name (e.g. "Nguyễn Minh Đức") → verify results found.
    """
    # 1. Log in to the system
    login(page, test_config)
    
    # 2. Enter the author name "Nguyễn Minh Đức" into the search box
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Nguyễn Minh Đức")
    page.wait_for_timeout(1000)
    
    # 3. Verify that there are books containing the author name "Nguyễn Minh Đức" in their aria-label attribute
    assert page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]').count() > 0

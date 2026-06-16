## AUTOMATED WEB UI TESTING REPORT
### 1. Test Environment:

- **System Under Test:** ABC Library Book Borrowing Management System (https://stqa.rbc.vn)
- **Testing Tools:** Python 3.11.9, Playwright, pytest, pytest-playwright
- **Browser :** Chromium (executed with the `--force-renderer-accessibility` argument to support interaction with the Flutter Web Semantics Tree)
- **GitHub link :** [ https://github.com/USTH-STQA-2026/stqa-automation-testing-stqa_group_06 ]

### Test Account Configuration

- **Member Account:** dam.tran@email.com / password123
- **Librarian Account:** librarian@library.com / admin123

### Test Automation Strategy

**Test Runner**  Pytest discovers and executes test functions. 
**Browser Automation**  Playwright controls the Chromium browser during test execution. 
**UI Interaction** Flutter Accessibility Semantics Tree is used to interact with input fields, buttons, tabs, and records. 
**Test Isolation** Each test is executed using a fresh browser context to ensure independence and avoid side effects. 
**Test Data**  Seed data and configurable test accounts are managed through the `.env` configuration file. 
**Assertions**  Tests verify visible text, ARIA labels, statuses, records, and access behavior against expected results. 
**Evidence**  Screenshots are captured automatically after test execution to support result verification and defect reporting. 


## 2. Test Cases and Execution Status

### Main Test Cases:

| TC-ID | Test Case / Test Scenario | Test Function | Brief Description | Result | REQ | Status | Screenshot |
|--------|----------------------------|-------------------|---------|----------|-------|-------------|
| TC-01 | Login with correct Email and Password | tests/test_login.py | Verify that a member can log in using valid credentials | User is redirected to the member dashboard successfully. | REQ-01 | Pass | screenshots/TC-01.png |
| TC-02 | Login with wrong password | tests/test_login.py | Verify that the system rejects incorrect password | An error message is displayed and login is denied | REQ-01 | Pass | screenshots/TC-02.png |
| TC-03 | Failed login – both Email-Passworrd left blank | tests/test_login.py | Verify that the system validates required login fields. | The system displays the message "Please enter your email and password" and prevents login. | Pass | REQ-01 | screenshots/TC-03.png |
| TC-04 | Search books by title – enter "Flutter" | tests/test_search.py | Verify that users can search for books by title. | The search returns the correct book: BOOK001 (Basic Flutter Programming). | REQ-03 | Pass | screenshots/TC-04.png |
| TC-05 | Search books – enter "xyz_123" | tests/test_search.py | Verify the system behavior when no books match the search keyword. | A "No books found" message is displayed. | REQ-03 | Pass | screenshots/TC-05.png |
| TC-06 | Filter books by category – enter "Technology" | tests/test_search.py | Verify that users can filter books by category. | Entering "Technology" in the category filter textbox displays only Technology books. | REQ-03 | Pass | screenshots/TC-06.png |
| TC-07 | Search books by author | tests/test_search.py | Verify that users can search for books by author name. | Searching for author "Nguyễn Minh Đức" displays the correct books written by this author. | REQ-03 | Pass | screenshots/TC-07.png |
| TC-08 | Borrow a book successfully | tests/test_borrow_return.py | Verify that a member can borrow an available book. | After confirming the borrow action, the selected book status changes to "Borrowed". | REQ-04 | Pass | screenshots/TC-08.png |
| TC-09 | View borrowed books list | tests/test_borrow_return.py | Verify that members can view their active borrowing records. | The "Borrow / Return" tab correctly displays borrowing record BR001. | REQ-04 | Pass | screenshots/TC-09.png |
| TC-10 | Return a book successfully | tests/test_borrow_return.py | Verify that a member can return a borrowed book. | After clicking "Return Book", the book status changes back to "Available". | REQ-05 | Pass | screenshots/TC-10.png |
| TC-11 | Log out successfully | tests/test_general.py | Verify that users can log out of the system. | Clicking the logout icon redirects the user to the login page. |  | Pass | screenshots/TC-11.png |
| TC-12 | Switch the interface language to English | tests/test_general.py | Verify that users can change the application language. | The interface language is successfully changed from Vietnamese to English, and all supported labels and messages are displayed correctly. |  | Pass | screenshots/TC-12.png |

### Extended Test Cases:

| TC-ID | Test Case / Test Scenario | Test Function | Brief Description | Result | Requirement | Status | Screenshot |
|--------|----------------------------|----------------|-------------------|----------|-------------|----------|-------------|
| TC-13 | Borrow the 4th book | tests/test_borrow_return.py | Verify that a member cannot borrow more than 3 books at the same time. | The system allowed the member to borrow a 4th book even though the borrowing limit had already been reached. | REQ-04 | Fail | screenshots/TC-13.png |
| TC-14 | Login with correct Email and Password of Librarian | tests/test_add_member.py | Verify that a librarian can log in using valid credentials. | The librarian was successfully authenticated and redirected to the librarian dashboard. | REQ-01 | Pass | screenshots/TC-14.png |
| TC-15 | Librarian adds a new member with a valid email address | tests/test_add_member.py | Verify that the librarian can create a new member account using a valid email format. | The system failed to create the member account even though a valid email address was provided. | REQ-07 | Fail | screenshots/TC-15.png |
| TC-16 | Librarian adds a new member with an invalid email address (missing "." in the domain) | tests/test_add_member.py | Verify that the system rejects invalid email formats when creating a new member account. | The system accepted the invalid email address and created the member account successfully. | REQ-07 | Fail | screenshots/TC-16.png |

### Data-driven Testing:
-------------|
| TC-ID | Test Case / Test Scenario | Brief Description | Result | Status | Screenshot |
|---------|-----------------------------|-------------------|----------|----------|-------------|
| B2-Login | Data-driven testing – invalid login attempts | tests/test_login.py | Execute the invalid login scenario using multiple datasets. | Tested with three datasets: (1) empty email and password, (2) invalid email with valid password, and (3) valid email with incorrect password. The system correctly rejected all attempts and displayed the corresponding error messages. | Pass | screenshots/B2-D.png |
| B2-Search | Data-driven testing – book search | tests/test_search.py |  Execute the book search scenario using multiple keywords. | Tested with the keywords "Flutter", "Python", and "Kiểm thử". The system returned the expected search results for each keyword. | Pass | screenshots/B2-S.png |


### Summary:

| File | Number of Tests | Main Coverage | Pass | Bug | 
|---------|--------------------|-------------------|----------|----|
| tests/test_login.py | 4 | Login success, invalid credentials, and input validation scenarios. | 4 | 0 |
| tests/test_search.py | 5 | Book searching, filtering by title, author, and category | 5 | 0 |
| tests/test_borrow_return.py | 4 | Borrowing books, returning books, borrowing limits  | 3 | 1 |
| tests/test_general.py | 2 | Logout functionality and language switching. | 2 | 0 |
| tests/test_bonus.py | 3 | Member management, role-based access control  | 1 | 2 |
| **Total** | **18** | **Overall automated Web UI test coverage** | **18** | **3** |


## 3. Bug Report

### BUG-01: 

**Title :** System allows borrowing a fourth book despite the maximum borrowing limit

**Input :**  
A member who already has **3 active borrowed books** attempts to borrow an additional book (the 4th book).

**Expected :**  
The system should reject the request and display an appropriate message such as:  
*"You have reached the maximum borrowing limit of 3 books."*

**Actual :**  
The borrowing request is processed successfully, and the member is able to borrow the fourth book.

**Severity :**  **High** — Violates a core library policy and may lead to inaccurate inventory control and unfair resource allocation.

**Test :**  `tests/test_borrow_return (TC-13)`

**Solution :**
- Implement server-side validation to check the number of active borrowing records before creating a new borrowing transaction. If the member already has 3 borrowed books, the system should reject the request and return an appropriate error message. In addition, the UI should disable or hide the Borrow action when the borrowing limit has been reached to improve the user experience.


### BUG-02: 

**Title :** System rejects a valid email address when creating a new member

**Input :**
Create a new member using the email address **"[newmember@test.com](mailto:newmember@test.com)"**, which follows the standard email format (contains both `@` and `.`).

**Expected :**
The system should successfully create the new member account.

**Actual :**
The member creation request is rejected, and an error message is displayed even though the email address is valid.

**Severity :** **High** — Prevents legitimate users from registering new member accounts and impacts normal system operations.

**Test :** `tests/test_add_member (TC-15)`

**Solution :**
-  Review and update the server-side email validation rules to comply with standard email specifications (e.g., RFC 5322). Ensure that valid email addresses are accepted consistently by both the frontend and backend. Add automated test cases covering various valid and invalid email formats to prevent regression.


### BUG-03:

**Title :** System accepts invalid email addresses when adding a new member

**Input :**
Add a new member using an invalid email address: `newmember@test`

**Expected :**
The system should reject the email address and display an appropriate validation message indicating that the email format is invalid.

**Actual :**
The member is created successfully even though the email address is missing the top-level domain (e.g., ".com") and does not conform to the required email format.

**Severity :** **Medium** — Invalid data can be stored in the system, affecting data quality and potentially causing issues with future communications or account-related functions.

**Solution :**
- Implement robust email format validation on both the frontend and backend using a standard-compliant validation pattern. Ensure that email addresses without a valid top-level domain are rejected. Add automated test cases covering both valid and invalid email formats to prevent similar defects from recurring.

**Test :** `tests/test_add_member (TC-16)`


## 4. Overall Assessment of the System
-  Based on the automated Web UI testing results, the ABC Library Book Borrowing Management System is generally stable and its core functionalities operate as expected. Most test cases related to authentication, book searching, filtering, borrowing and returning books, viewing borrowing records, logging out, and language switching were executed successfully and produced the expected outcomes.

- However, several defects were identified during testing. The system failed to enforce the maximum borrowing limit, allowing members to borrow more books than permitted by business rules. In addition, inconsistencies were found in the email validation mechanism when adding new members: some valid email addresses were rejected, while certain invalid email formats were accepted. These issues indicate that some business rules and input validation checks are either missing or not consistently implemented between the frontend and backend.

-  Overall, the system demonstrates good usability and functional coverage for day-to-day library operations. Nevertheless, the identified defects should be addressed before deployment to ensure data integrity, compliance with business policies, and a better user experience. It is recommended to strengthen server-side validations, expand automated regression test coverage, and perform additional integration testing after the defects have been fixed.


## 5. AI Usage Declaration 
- ChatGPT and Claude
































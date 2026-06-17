# REPORT: CROSS-CHECKING GROUP 12

## 1. MANUAL TESTING

### 1.1, Requirements:

| STT | Tiêu chí | Điểm tối đa | Dương |
|-----|-----------|-------------|--------|
| 1 |  Fork repo starter → tạo repo nhóm (Đặt tên: stqa-manual-<tên-nhóm>)  | 1 | 1 |
| 2 |  Viết ít nhất 20 test case (phủ đủ chức năng chính)- 29 TC   | 1 | 1 |
| 3 |  Áp dụng ít nhất 3 kỹ thuật thiết kế kiểm thử (EP, BVA, Decision Table) | 1 | 1 |
| 4 |  Bao gồm happy path + negative + boundary  | 1 | 1 |
| 5 |  Tạo bug report cho mỗi TC Fail (đầy đủ bước tái hiện, severity) | 1 | 1 |
| 6 |  Viết báo cáo tổng hợp (summary: thống kê, đánh giá, đề xuất) | 1 | 1 | 
| 7 |  Điền thông tin nhóm trong README.md (Bảng Team Information) | 1 | 1 |
| 8 |  Thực thi tất cả TC trên hệ thống (ghi nhận Pass/Fail + actual result)  | 1 | 1 |
| 9 |  Nộp bài qua link repo hoặc Pull Request | 1 | 1 |

### 1.2, Bonus

| Mã | Tiêu chí | Điểm tối đa | Dương |
|-----|-----------|-------------|--------|
| 1 |  Viết 29 test case phủ tất cả 8 REQ  | 0.5 | 0.5 |
| 2 |  Thêm bảng Decision Table hoàn chỉnh cho chức năng Mượn sách | 0.5 | 0.5 |
| 3 |  Mỗi bug report có ảnh chụp minh chứng | 0.5 | 0.5 |
| 4 |  Tổng hợp có đề xuất ưu tiên sửa lỗi (High trước, Low sau) | 0.5 | 0.5 |

- Không có evidence cho test-execution : - 0.5
- Không phân chia test case riêng cho từng REQ (gộp chung): - 0.5

### Tổng điểm cho Manual Testing: 10

## 2. Automation Testing:
### 2.1, Requirements:

| STT | Tiêu chí | Điểm tối đa | Dương |
|-----|-----------|-------------|--------|
| 1 |  Fork repo starter → tạo repo nhóm (Đặt tên: stqa-automation-<tên-nhóm>) | 1 | 1 |
| 2 |  Cấu hình .env với tài khoản test (xem docs/test-accounts.md) | 1 | 1 |
| 3 |  Hoàn thành tất cả 12 test case (TC-01 → TC-12) | 2 | 2 |
| 4 |  Tất cả test phải chạy được (pytest không lỗi cú pháp) – PASS hoặc FAIL đều tính | 2 | 2 |
| 5 |  Mỗi test có screenshot tự động (lưu vào screenshots/) | 2 | 1 |
| 6 |  Điền thông tin nhóm trong README.md (Bảng Team Information) | 1 | 1 | 
| 7 |  Nộp bài qua Pull Request hoặc link repo | 1 | 1 |

### 2.2, Bonus

| Mã | Tiêu chí | Điểm tối đa | Dương |
|-----|-----------|-------------|--------|
| 1 |  Thêm ≥ 3 test case mới ngoài 12 TC cho sẵn | 0 | 0 |
| 2 |  Viết data-driven test (parametrize nhiều bộ dữ liệu cho 1 kịch bản) | 0 | 0 |
| 3 |  Thêm assertion chi tiết (kiểm tra text cụ thể, không chỉ kiểm tra URL) | 0.5 | 0.5 |
| 4 |  Viết mô tả ngắn cho mỗi test trong REPORT.md | 0.5 | 0.5 |

### Tổng điểm cho Automation Testing: 11

## 3. Nhận xét chung:

- Group 12 đã hoàn thành khá tốt các yêu cầu của cả Manual Testing và Automation Testing. Nhóm xây dựng được bộ test case có độ bao phủ tốt, áp dụng các kỹ thuật thiết kế kiểm thử phù hợp và chuẩn bị bug report tương đối đầy đủ. Phần Automation Testing cũng được triển khai ổn định, các test có thể thực thi bằng pytest mà không gặp lỗi cú pháp.

- Tuy nhiên, nhóm vẫn cần cải thiện một số điểm như bổ sung evidence cho quá trình test execution, phân chia test case theo từng requirement để tăng tính truy vết, đồng thời hoàn thiện các test case và screenshot tự động còn thiếu. Nhìn chung, đây là một bài làm tốt, thể hiện sự đầu tư và nắm được quy trình kiểm thử cơ bản.

## 4. Kết quả cuối cùng:

### Manual Testing : 11
### Automation Testing : 10



























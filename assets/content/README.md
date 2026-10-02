# LG Internal Sales — System Content & Configurations

Thư mục này lưu trữ các tệp tin cấu hình nội dung, tài khoản ngân hàng và chính sách vận hành của Cổng Bán Hàng Nội Bộ LG Electronics Việt Nam.

---

## 1. Cấu trúc tệp tin nội dung

| Tệp tin | Định dạng | Mô tả nội dung |
|---|---|---|
| **[`bank_accounts.json`](assets/content/bank_accounts.json)** | JSON | Danh sách tài khoản ngân hàng thụ hưởng chính thức của LGEVH (Vietcombank, Techcombank), số tài khoản, chi nhánh, cú pháp chuyển khoản tiêu chuẩn. |
| **[`system_config.json`](assets/content/system_config.json)** | JSON | Cấu hình hệ thống, định nghĩa phân quyền (Employee vs PM), danh sách chương trình mặc định, hạn mức đăng ký mỗi nhân viên. |

---

## 2. Hướng dẫn thay đổi thông tin ngân hàng thụ hưởng

Khi công ty thay đổi số tài khoản hoặc thêm ngân hàng mới:
1. Mở file `assets/content/bank_accounts.json` và cập nhật các trường: `account_number`, `branch`, `account_holder`.
2. Mở file mã nguồn chính [`Mau_Dang_Ky_Internal_Sales_3009.html`](Mau_Dang_Ky_Internal_Sales_3009.html) và tìm khối giao diện Thẻ 01: `Thế Lệ & Chuyển Khoản` (khoảng dòng 2170–2220) để cập nhật số tài khoản hiển thị và nút sao chép `btn-copy-acc`.

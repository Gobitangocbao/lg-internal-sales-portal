# Google Sheet "Users" — Template Specification

## Tạo trong Spreadsheet: LG Internal Sales Database

Thêm 1 sheet tab mới tên **"Users"** trong Google Sheet ID: `10aN5O3HL79asPGfug75IPv1w_ssGPo8edsASMuG3_aM`

## Cấu trúc cột (Row 1 = Header)

| Cột | Header | Kiểu | Bắt buộc | Mô tả |
|-----|--------|------|----------|-------|
| A | **ID** | Text | ✅ | Mã nhân viên (VD: VH12345). Case-insensitive khi đăng nhập |
| B | **Password** | Text | ✅ | Mật khẩu. Hiện tại plaintext — sẽ nâng cấp SHA256 ở Phase P6 |
| C | **Name** | Text | ✅ | Họ tên đầy đủ (VD: Nguyễn Thị Quỳnh Như) |
| D | **Dept** | Text | ✅ | Bộ phận / Division (VD: HS PM Support) |
| E | **Phone** | Text | | Số điện thoại (VD: 0912345678) |
| F | **Email** | Text | | Email LG (VD: quynhnhu@lge.com) |
| G | **Role** | Text | ✅ | `PM` hoặc `USER` — mặc định `USER` nếu để trống |
| H | **Status** | Text | ✅ | `Active` hoặc `Inactive` — chỉ `Active` mới đăng nhập được |

## Dữ liệu mẫu (để test)

| ID | Password | Name | Dept | Phone | Email | Role | Status |
|----|----------|------|------|-------|-------|------|--------|
| VH12345 | test123 | Nguyễn Thị Quỳnh Như | HS PM Support | 0912345678 | quynhnhu@lge.com | PM | Active |
| VH88921 | test123 | Trần Văn Nam | Audit & Jeong-Do | 0987654321 | vannam@lge.com | USER | Active |
| VH55432 | test123 | Lê Hoàng Anh | HE Sales Division | 0933445566 | hoanganh@lge.com | USER | Active |
| VH33211 | test123 | Hoàng Minh Trí | HA Production | 0911223344 | minhtri@lge.com | USER | Active |
| VH99120 | test123 | Đặng Thanh Hà | Finance & Accounting | 0955667788 | thanhha@lge.com | USER | Active |
| VH00001 | disabled | Test Inactive | IT Support | 0900000000 | test@lge.com | USER | Inactive |

## Ghi chú quan trọng

- Password hiện tại là **plaintext** — sẽ upgrade sang SHA256 hash ở Phase P6
- Mỗi ID phải duy nhất (unique). Server chỉ match ID đầu tiên tìm thấy
- Role `PM` sẽ được dùng trong Phase P4 (PM Dashboard) để hiển thị giao diện quản lý
- Sau khi tạo sheet, **cần re-deploy Apps Script** để script đọc được sheet mới

## Cách tạo

1. Mở Google Sheet: `https://docs.google.com/spreadsheets/d/10aN5O3HL79asPGfug75IPv1w_ssGPo8edsASMuG3_aM`
2. Bấm dấu `+` ở dưới cùng để thêm sheet mới
3. Đặt tên sheet: **Users**
4. Copy header row (ID, Password, Name, Dept, Phone, Email, Role, Status) vào Row 1
5. Nhập dữ liệu mẫu hoặc dữ liệu thật từ Row 2 trở đi
6. Re-deploy Apps Script

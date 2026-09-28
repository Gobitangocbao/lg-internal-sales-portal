# Nối trang đăng ký với Google Sheet (Apps Script)

Mục tiêu: nhân viên bấm Gửi ở Tab 2 (đăng ký) và Tab 3 (khai nộp tiền) thì dữ liệu tự ghi vào sheet **LG Internal Sales Database**.

## Script làm gì
- **Đăng ký (Tab 2):** thêm 1 dòng vào `Registrations`, trạng thái `Chờ nộp tiền`. Giờ Timestamp lấy theo máy chủ Google, múi giờ Việt Nam.
- **Khai nộp (Tab 3):** tìm đơn theo Slot và Mã NV, điền các cột M–R, chuyển trạng thái sang `Đã khai nộp - chờ đối soát`. File biên lai (ảnh hoặc PDF, tối đa 5 MB) được lưu vào thư mục `Bien lai nop tien` trong cùng thư mục Drive.
- **Nhật ký:** mọi lần gửi đều ghi thêm 1 dòng vào `ActivityLog`.

Script **chỉ thêm, không xoá**. Đơn đã khai nộp thì không bị ghi đè; nếu gửi lại, script từ chối và ghi vào nhật ký. Script **không tự gửi email**.

**Chặn trùng slot:** slot đã có đơn còn hiệu lực thì đơn sau bị từ chối ngay, không ghi vào `Registrations` (chỉ ghi vào `ActivityLog` với mã `REGISTER_REJECTED_DUP_SLOT`). Trang báo nhân viên chọn slot khác. Khi PM đổi trạng thái đơn sang `Hủy` hoặc `Từ chối`, slot được mở lại cho người khác đăng ký.

Vượt hạn mức 1 sản phẩm/NV vẫn được ghi kèm cảnh báo, sheet tô đỏ để PM xử lý.

## Trạng thái hiện tại (28/09/2026)
- Đã cài: dự án Apps Script riêng tên **LG Internal Sales API** trong tài khoản chủ sheet (script.google.com). Script tự mở sheet theo `SPREADSHEET_ID`.
- Đã triển khai Web App, phiên bản 1, chạy dưới tên chủ sheet, quyền truy cập "Bất kỳ ai". URL đã dán vào `SHEET_API_URL` trong bản `index.html` trên máy chủ dự án.
- Đã thử: đăng ký, chặn trùng slot, khai nộp tiền đều ghi đúng vào sheet.

## Cài đặt (chủ sheet tự làm, khoảng 5 phút)
1. Mở sheet, vào **Tiện ích mở rộng (Extensions) → Apps Script**.
2. Xoá đoạn mẫu trong `Code.gs` (chỉ có dòng `function myFunction() {}`), rồi dán toàn bộ file `apps-script/Code.gs`. Bấm **Lưu**.
3. Ở ô chọn hàm trên thanh công cụ, chọn **testSetup** rồi bấm **Chạy (Run)**.
   - Google sẽ hỏi quyền. Chị tự đăng nhập và bấm **Cho phép**.
   - Nếu thấy màn hình "Google chưa xác minh ứng dụng này", đó là vì script do chính chị viết. Bấm **Nâng cao**, rồi **Chuyển tới … (không an toàn)**.
   - Chạy xong, trong Drive sẽ có thêm thư mục `Bien lai nop tien`.
4. Bấm **Triển khai (Deploy) → Tùy chọn triển khai mới (New deployment)**.
   - Loại (Type): **Ứng dụng web (Web app)**.
   - Thực thi dưới danh nghĩa (Execute as): **Tôi (Me)**.
   - Ai có quyền truy cập (Who has access): **Bất kỳ ai (Anyone)**.
   - Bấm **Triển khai**, rồi sao chép **URL ứng dụng web** (kết thúc bằng `/exec`).
5. Mở `index.html`, tìm dòng `const SHEET_API_URL = '';` và dán URL vào giữa hai dấu nháy. Hoặc gửi URL cho người phụ trách kỹ thuật để họ dán giúp.
6. Thử 1 đơn giả ở Tab 2 và Tab 3, kiểm tra sheet, rồi xoá tay dòng thử trong `Registrations`.

Khi sửa `Code.gs` về sau, vào **Triển khai → Quản lý triển khai**, bấm sửa bản đang dùng, chọn **Phiên bản mới** để giữ nguyên URL.

## Rủi ro cần biết trước khi dùng thật
- **"Bất kỳ ai"** nghĩa là ai có URL đều **gửi được** dữ liệu vào sheet, nhưng **không đọc được** sheet. URL nằm trong `index.html`, nên không đưa file này ra ngoài LG.
- **Dữ liệu cá nhân** (SĐT, địa chỉ, mã giao dịch ngân hàng, biên lai) sẽ nằm trong Drive của tài khoản chạy script. Nếu đó là Gmail cá nhân, cần hỏi IT/Bảo mật LG xem có được phép không. Phương án an toàn hơn là chạy script bằng tài khoản Google Workspace của công ty.
- Khi `SHEET_API_URL` để trống, trang chạy ở **chế độ bản mẫu**: thông báo ghi rõ là **không lưu**.

# Cổng Đăng Ký Bán Hàng Nội Bộ LG (Internal Sales Portal)

Bản mẫu (prototype) giao diện cho quy trình bán hàng nội bộ dành cho nhân viên LG Electronics Việt Nam:
thông báo mở bán → đăng ký trực tuyến → nộp tiền & upload biên lai → PM đối soát, giao hàng.

> ⚠️ **Repo này phải để PRIVATE.** File có số tài khoản ngân hàng, tên và email nội bộ. Chỉ mời người trong LG có liên quan.

## Xem nhanh
Tải file `index.html` về rồi mở bằng trình duyệt (Chrome/Edge). Không cần cài đặt gì.

## Tình trạng hiện tại
- **Frontend:** có, 1 file HTML + CSS + JavaScript thuần.
- **Lưu dữ liệu:** qua Google Apps Script ghi vào Google Sheet (xem `docs/SETUP_APPS_SCRIPT.md`). Khi `SHEET_API_URL` trong `index.html` để trống, trang chạy chế độ bản mẫu và **không lưu**.
- Link `internalsales.lge.com` trong trang chỉ là chữ minh hoạ.

## Cấu trúc
```
index.html          BẢN CHÍNH THỨC = v9 (chốt 30/09/2026): trang bìa + đăng nhập bằng Mã NV, mỗi NV chỉ 1 đơn hợp lệ. Nội dung giống hệt Mau_Dang_Ky_Internal_Sales_v9_TrangBia.html
index_v7_cu.html    Bản v7 cũ (trước đây là index.html), giữ lại để đối chiếu
Mau_Dang_Ky_Internal_Sales_3009.html   Bản v8 (30/09/2026) đang chờ nhóm kiểm tra: khoá nộp tiền 2 giờ, chọn sản phẩm dạng thẻ, lọc kho. Xem mục 18 trong docs/HANDOVER.md
Mau_Dang_Ky_Internal_Sales_v9_TrangBia.html   Bản v9 (đã chốt, chép sang index.html). Sửa trang thì sửa cả 2 file cho khớp. Xem mục 18 trong docs/HANDOVER.md
docs/HANDOVER.md    Hồ sơ bàn giao chi tiết (đọc mục 0.1 trước): tính năng, lỗi đã biết, backlog, kịch bản kiểm thử
data/LG_Internal_Sales_Database.xlsx   File tổng hợp đăng ký (Dashboard, Registrations, Slots, Config...)
apps-script/Code.gs      Script nhận đơn từ trang, ghi vào Google Sheet (chỉ thêm, không xoá)
docs/SETUP_APPS_SCRIPT.md  Hướng dẫn cài script, triển khai Web App
```

## Cách cùng làm
1. **Đọc `docs/HANDOVER.md` trước.** Mục 10 là các lỗi đã biết, mục 11 là việc cần làm, mục 15 là các câu hỏi còn mở.
2. Người được mời **tự sửa và tự gộp (merge), không cần chủ dự án duyệt**. Có thể sửa thẳng trên nhánh `main`, hoặc tạo nhánh riêng khi thử nghiệm thay đổi lớn rồi tự gộp vào `main`.
3. Trước khi sửa, bấm **Sync / Pull** để lấy bản mới nhất, tránh ghi đè thay đổi của người khác.
4. Ghi lại thay đổi vào mục 18 "Nhật ký thay đổi" trong `docs/HANDOVER.md`.
5. Số liệu giá, model, tài khoản trong file là **dữ liệu mẫu, chưa xác minh**. Không dùng như số thật.

## Quy tắc dự án
- Không bịa số liệu. Chưa chắc thì ghi rõ là chưa chắc.
- Chỉ thêm, không xoá bản cũ khi chưa được chủ dự án đồng ý.
- Không tự gửi email hay công bố ra ngoài. Việc gửi do chủ dự án quyết định.
- Giao diện mang thương hiệu LG phải theo LG BI Guidelines.

## Chủ dự án
Hoàng Minh Hiền, Kiểm toán nội bộ & Đạo đức doanh nghiệp (Jeong-Do), LG.

# Cổng Đăng Ký Bán Hàng Nội Bộ LG (Internal Sales Portal)

Bản mẫu (prototype) giao diện cho quy trình bán hàng nội bộ dành cho nhân viên LG Electronics Việt Nam:
thông báo mở bán → đăng ký trực tuyến → nộp tiền & upload biên lai → PM đối soát, giao hàng.

> ⚠️ **Repo này phải để PRIVATE.** File có số tài khoản ngân hàng, tên và email nội bộ. Chỉ mời người trong LG có liên quan.

## Xem nhanh
Tải file `index.html` về rồi mở bằng trình duyệt (Chrome/Edge). Không cần cài đặt gì.

## Tình trạng hiện tại
- **Frontend:** có, 1 file HTML + CSS + JavaScript thuần.
- **Backend / Database / Domain:** **chưa có**. Dữ liệu chỉ nằm trên trình duyệt, tải lại trang là mất.
- Link `internalsales.lge.com` trong trang chỉ là chữ minh hoạ.

## Cấu trúc
```
index.html          Trang prototype (5 tab: Thư thông báo, Đăng ký, Nộp tiền, Danh sách Slot, SOP)
docs/HANDOVER.md    Hồ sơ bàn giao chi tiết: tính năng, lỗi đã biết, backlog, đề xuất kiến trúc, kịch bản kiểm thử
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

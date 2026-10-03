# BỘ TÀI NGUYÊN BIỂU TƯỢNG ĐỘNG (LG MOTION ICONS & KINETIC SVG SUITE)
**Hệ Thống Biểu Tượng Chuyển Động Chuẩn Mực Cho Cổng Bán Hàng Nội Bộ LG Electronics Việt Nam (LGEVH)**

Thư mục này lưu trữ toàn bộ các tệp đồ họa chuyển động (.GIF) chính thức từ CDN LG.com và các biểu tượng vector động học (.SVG) được thiết kế riêng theo quy chuẩn nhận diện thương hiệu **LG Brand Identity Guidelines V5.2 (Aug 2024)** và hệ thống giao diện số **LG.com Global One Platform Style Guide**.

---

## 1. Danh Mục Tài Nguyên (Asset Inventory)

### A. Hoạt Ảnh GIF Chính Thức (Official LG.com Motion Assets)
Trích xuất trực tiếp từ máy chủ CDN toàn cầu của LG Electronics (`/content/dam/channel/wcms/common/homequicklick-ani/`):

| Tên Tệp | Kích Thước | Số Frame | Chu Kỳ | Khoảng Nghỉ Tĩnh | Ứng Dụng Trong Web |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`ico_offer1_ani.gif`** | 192 × 192 px | 105 frames | 5.92s | 1,480 ms (25%) | Nút **Ưu Đãi Độc Quyền** (Tag xoay mở quạt lộ thẻ đỏ) |
| **`ico_offer2_ani.gif`** | 192 × 192 px | 78 frames | 6.96s | 2,920 ms (42%) | Nút **Voucher / Mã Giảm Giá** (Đường xé tách rời hút về) |
| **`ico_promotions_ani.gif`** | 192 × 192 px | 45 frames | 1.80s | 0 ms (Liên tục) | Nút **Tất Cả Ưu Đãi** (Huy hiệu hoa cúc 12 cánh co giãn thở) |
| **`ico_great-offers_ani.gif`** | 192 × 192 px | 54 frames | 5.04s | 2,000 ms (40%) | Nút **Quà Tặng / Life's Good** (Nắp hộp bật mở tung voucher) |

### B. Biểu Tượng Ngành Hàng Động Học (Handcrafted Kinetic Vector SVGs)
Chế tác độc quyền với CSS keyframes tích hợp sẵn, hiển thị siêu nét trên màn hình Retina / 4K, dung lượng siêu nhẹ (<2KB/tệp):

| Tên Tệp | Đối Tượng | Cơ Chế Động Học | Màu Nhấn |
| :--- | :--- | :--- | :--- |
| **`cat_tv_soundbar.svg`** | TV OLED & Loa Thanh | Quét màn hình OLED (`tvScan`) + Sóng âm loa thanh (`soundPulse`) | `#EA1917` (Active Red) |
| **`cat_instaview_refrigerator.svg`** | Tủ Lạnh InstaView | Gõ kính 2 lần sáng đèn (`instaviewKnock`) + Sóng gõ cửa (`knockRipples`) | `#EA1917` + `#FFF2D6` |
| **`cat_washtower.svg`** | Máy Giặt WashTower | Lồng giặt xoay đảo chiều (`drumSpin`) + Đèn LED trung tâm nhấp nháy (`ctrlBlink`) | `#EA1917` |
| **`cat_air_conditioner.svg`** | Điều Hòa DUALCOOL | Cánh vẫy gió hạ xuống (`flapSwing`) + 3 luồng gió mát uốn lượn (`breezeFlow`) | `#EA1917` |
| **`cat_gram_laptop.svg`** | Laptop LG gram & Màn hình | Màn hình gập mở 25° (`gramOpen`) + Điểm nhấn gram Active Red | `#EA1917` |
| **`cat_vcb_security.svg`** | Quy Chế & Vietcombank | Khiên bảo mật nhịp đập an toàn (`shieldPulse`) | `#EA1917` |

### C. Biểu Tượng SVG Tĩnh Hỗ Trợ (Official Supporting SVGs)
| Tên Tệp | Ý Nghĩa / Chức Năng |
| :--- | :--- |
| **`ico_epc.svg`** | Tư vấn viên / Chuyên viên hỗ trợ nội bộ LGE (Có tai nghe headset) |
| **`ico_vertical3_44.svg`** | Khiên bảo hành & gia hạn dịch vụ LG Care |
| **`ico_lg-thinq_44.svg`** | Biểu tượng nhà thông minh LG ThinQ |
| **`ico_membership_44.svg`** | Thẻ hội viên VIP Membership |
| **`ico_contact_us_44.svg`** | Kênh liên hệ hỗ trợ khách hàng |
| **`ico_promotions_44.svg`** | Bản vẽ tĩnh của huy hiệu hoa cúc khuyến mại |
| **`ico_great-offers_44.svg`** | Bản vẽ tĩnh của hộp quà tặng Life's Good |

---

## 2. Quy Chuẩn Kỹ Thuật (Design System Specifications)

1. **Độ dày nét vẽ (Stroke Weight):** Đồng nhất `2.0px - 2.2px` trên toàn bộ hệ thống SVG.
2. **Bo tròn góc & đầu nét:** `stroke-linecap="round"` và `stroke-linejoin="round"` tạo cảm giác thân thiện, ấm áp và nhân văn.
3. **Bảng màu chuẩn thương hiệu:**
   - **Đỏ Năng Lượng / Mua Hàng:** `#EA1917` (Active Red).
   - **Đỏ Di Sản / Logo:** `#A50034` (Heritage Red).
   - **Nét Viền & Khung:** `#262626` (Dark Charcoal).
   - **Nền Đĩa Tròn Sáng:** `#FFFFFF` với viền `#E6E1D6`.
   - **Nền Đĩa Tròn Tối (Dark Mode):** `#262626` với viền `#383838`.
   - **Hover:** Đĩa chuyển `#F6F3EB` (hoặc `#2F2F2F`), chữ gạch chân `text-decoration: underline; text-underline-offset: 3px`.
4. **Nhịp điệu động học (Kinetic Rhythm):** 25 FPS (40ms/frame), luôn có pha nghỉ tĩnh (1.5s - 3.0s) để tránh rối mắt cho người dùng khi duyệt đơn hàng FCFS.

---

## 3. Hướng Dẫn Cập Nhật & Thay Đổi Icon (SOP)

Cổng Bán Hàng Nội Bộ LG đã được cấu hình theo kiến trúc **Mô-đun hóa tài nguyên (Decoupled Assets Architecture)**. Toàn bộ 8 đĩa tròn danh mục trong [`Mau_Dang_Ky_Internal_Sales_3009.html`](../../Mau_Dang_Ky_Internal_Sales_3009.html) đều liên kết trực tiếp tới các tệp trong thư mục này qua thẻ `<img src="assets/images/quick-links-ani/...">`:

### Quy Trình 1: Thay thế hoặc cập nhật Icon (Hot-Swapping không cần sửa code)
1. **Chỉnh sửa file SVG/GIF:** Mở file SVG hoặc GIF bạn muốn cập nhật trong thư mục `assets/images/quick-links-ani/`.
2. **Lưu đè file:** Lưu trực tiếp thay đổi vào đúng tên file hiện tại (ví dụ: `cat_tv_soundbar.svg`, `cat_washtower.svg`, hoặc `ico_offer1_ani.gif`).
3. **Hiệu lực tức thì:** Mở hoặc tải lại trang web `Mau_Dang_Ky_Internal_Sales_3009.html` — toàn bộ icon mới sẽ hiển thị và tự động chạy hoạt ảnh động học mà **không cần chỉnh sửa một dòng mã HTML/CSS nào**!

### Quy Trình 2: Đổi icon sang một tệp mới có tên khác
1. Chép tệp `.svg` hoặc `.gif` mới vào thư mục `assets/images/quick-links-ani/`.
2. Mở file [`Mau_Dang_Ky_Internal_Sales_3009.html`](../../Mau_Dang_Ky_Internal_Sales_3009.html), tìm đến khối `.lg-quick-category-bar` (dòng 2875–2945).
3. Đổi thuộc tính `src="..."` của nút tương ứng sang tên tệp mới:
   ```html
   <img src="assets/images/quick-links-ani/<ten_file_moi>.svg" alt="..." loading="lazy">
   ```

### Quy Trình 3: Tùy biến hoạt ảnh động học (Keyframes) bên trong SVG
Mỗi tệp `.svg` trong thư mục này là một thực thể độc lập có nhúng sẵn khối `<style>`:
- Bạn có thể điều chỉnh chu kỳ thời gian (ví dụ từ `3.2s` sang `4.0s`), độ trễ `animation-delay`, hoặc thay đổi màu nhấn `#EA1917` (Active Red).
- Mọi trình duyệt hiện đại (Chrome, Safari, Edge, Firefox) đều tự động biên dịch và chạy GPU-accelerated keyframe animation khi nạp qua thẻ `<img>`.

### Quy Trình 4: Kiểm thử hiển thị
Mở tệp [`scratch/motion_icons_preview.html`](../../scratch/motion_icons_preview.html) hoặc [`Mau_Dang_Ky_Internal_Sales_3009.html`](../../Mau_Dang_Ky_Internal_Sales_3009.html) trên trình duyệt để kiểm tra tốc độ khung hình, độ sắc nét Retina/4K và khả năng tương thích Dark Mode trước khi đẩy lên Git.

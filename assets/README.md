# Thư Mục Tài Nguyên Hệ Thống (Assets Directory) — LG Internal Sales Portal

Thư mục `assets/` quản lý tập trung toàn bộ tài nguyên giao diện, đồ họa chuyển động, nội dung cấu hình và tệp mẫu chuẩn của Cổng Bán Hàng Nội Bộ LG Electronics Việt Nam (**LGEVH**).

Toàn bộ tài nguyên được phân loại theo cấu trúc mô-đun hóa độc lập, giúp việc chỉnh sửa, thay thế hoặc cập nhật hình ảnh/icon/tài khoản diễn ra thuận tiện mà **không cần can thiệp vào logic xử lý mã nguồn chính** (`Mau_Dang_Ky_Internal_Sales_3009.html`).

---

## 🧭 Cấu Trúc Phân Mục Tài Nguyên (Assets Directory Architecture)

```text
assets/
├── branding/                         # Bộ nhận diện thương hiệu LG (Logo, Favicon, Brand Identity)
├── content/                          # Cấu hình nghiệp vụ & ngân hàng
│   ├── bank_accounts.json            # Danh sách số tài khoản thụ hưởng (VCB/TCB), cú pháp nộp tiền
│   ├── system_config.json            # Phân quyền, hạn mức, trạng thái đợt bán
│   └── README.md                     # Hướng dẫn cập nhật tài khoản & cấu hình
├── digital-logo-play/                # Bộ hoạt ảnh thương hiệu LG Digital Logo Play chính thức
│   ├── CONTACT-SHEET.png             # Bảng tổng hợp 8 chuyển động biểu cảm
│   ├── MANIFEST.json                 # Đặc tả thông số kỹ thuật từng chuyển động
│   ├── black/                        # Phiên bản nét đen cho nền sáng
│   └── white/                        # Phiên bản nét trắng cho nền tối / Dark Mode
├── images/                           # Hình ảnh đồ họa & biểu tượng chuyển động
│   ├── lg_hero_banner.jpg            # Banner showcase sản phẩm cao cấp LG Electronics
│   └── quick-links-ani/              # [QUAN TRỌNG] BỘ MOTION ICONS & KINETIC SVG SUITE
│       ├── ico_offer1_ani.gif        # Hoạt ảnh GIF chính thức LG.com: Tag xoay mở quạt
│       ├── ico_offer2_ani.gif        # Hoạt ảnh GIF chính thức LG.com: Voucher đường xé
│       ├── ico_promotions_ani.gif    # Hoạt ảnh GIF chính thức LG.com: Huy hiệu hoa cúc thở
│       ├── ico_great-offers_ani.gif  # Hoạt ảnh GIF chính thức LG.com: Hộp quà Life's Good bật nắp
│       ├── cat_tv_soundbar.svg       # Biểu tượng động học: TV OLED & Loa thanh (Quét màn + Sóng âm)
│       ├── cat_instaview_refrigerator.svg # Biểu tượng động học: Tủ lạnh InstaView (Gõ kính 2 lần sáng đèn)
│       ├── cat_washtower.svg         # Biểu tượng động học: Máy giặt WashTower (Lồng xoay đảo chiều)
│       ├── cat_air_conditioner.svg   # Biểu tượng động học: Điều hòa DUALCOOL (Cánh vẫy hạ + Luồng gió mát)
│       ├── cat_gram_laptop.svg       # Biểu tượng động học: Laptop LG gram (Màn hình gập mở 25 độ)
│       ├── cat_vcb_security.svg      # Biểu tượng động học: Khiên bảo mật giao dịch Vietcombank
│       ├── ico_epc.svg               # Biểu tượng SVG chính thức: Chuyên viên tư vấn nội bộ LGE
│       └── README.md                 # Cẩm nang chi tiết & SOP thay thế icon động
├── slogan/                           # Biểu tượng chữ Life's Good chuẩn nhận diện LG BI V5.2
└── templates/                        # Thư viện tệp tin mẫu chuẩn hệ thống
    ├── Mau_Danh_Muc_San_Pham_Internal_Sales.xlsx # Mẫu Excel nạp danh mục sản phẩm cho PM
    ├── LG_Internal_Sales_Master_Database.xlsx    # Bảng tính CSDL mẫu 8 sheets cho Apps Script
    └── README.md                     # Cẩm nang định dạng cột và công thức tính toán
```

---

## 🎨 Quy Trình Chỉnh Sửa & Thay Thế Nhanh (Quick Customization SOP)

### 1. Thay thế hoặc nâng cấp Motion Icon (`assets/images/quick-links-ani/`)
- **Cách thức:** Các nút bấm trên thanh danh mục (`.lg-quick-category-bar`) trong ứng dụng web được liên kết trực tiếp tới các tệp `.svg` và `.gif` trong thư mục này qua thẻ `<img>`.
- **Thực hiện:** Để thay đổi hình ảnh một ngành hàng, bạn chỉ cần ghi đè (overwrite) tệp `.svg` hoặc `.gif` tương ứng trong `assets/images/quick-links-ani/` mà không cần chỉnh sửa bất kỳ dòng mã HTML nào!
- **Đặc tả chi tiết:** Xem hướng dẫn đầy đủ tại [`assets/images/quick-links-ani/README.md`](images/quick-links-ani/README.md).

### 2. Cập nhật Số tài khoản Ngân hàng (`assets/content/bank_accounts.json`)
- Mở file `assets/content/bank_accounts.json` và cập nhật số tài khoản, tên chi nhánh hoặc cú pháp chuyển khoản.
- Xem hướng dẫn tại [`assets/content/README.md`](content/README.md).

### 3. Cập nhật Mẫu danh mục Excel (`assets/templates/`)
- Mở file `assets/templates/Mau_Danh_Muc_San_Pham_Internal_Sales.xlsx` để thêm/bớt cột hoặc model mẫu.
- Xem hướng dẫn tại [`assets/templates/README.md`](templates/README.md).

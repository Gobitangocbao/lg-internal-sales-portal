# LG Motion Kit — bảng tra cứu

19 component, chia theo ba họ chuyển động của LG: **adaptive** (xuất hiện có thứ tự), **connected** (vẽ quan hệ), **fluid** (liên tục, dùng tiết chế).

Chọn ở đây rồi `python3 scripts/lg_motion.py get <id>`. Nhanh hơn: `lg_motion.py search "<việc cần làm>"`.


## Biểu đồ

| id | họ | khổ | dùng khi | từ khoá |
|---|---|---|---|---|
| `bars-compare` | adaptive | 480x260 | So sánh sell-out hoặc doanh số giữa các kênh, có thứ hạng rõ ràng | cột, bar, so sánh, compare, kênh, channel |
| `counter-hero` | adaptive | 420x200 | Slide chỉ có một con số cần đóng đinh — dùng khi con số tự nó là thông điệp | số lớn, counter, hero, thống kê, stat, một con số |
| `donut-share` | connected | 260x250 | Một tỷ lệ duy nhất — thị phần, độ phủ, tiến độ so với mục tiêu | donut, vòng, tròn, tỷ lệ, phần trăm, share |
| `funnel-steps` | connected | 420x260 | Khách rơi ở bước nào — hành trình mua, phễu chuyển đổi | phễu, funnel, chuyển đổi, conversion, hành trình, journey |
| `kpi-row` | adaptive | 560x150 | Ba con số cạnh nhau ở đầu một slide tổng quan hoặc dashboard | kpi, chỉ số, ba số, dashboard, tổng quan, metric |
| `line-trend` | connected | 480x240 | Xu hướng theo thời gian — sell-out, thị phần, coverage qua các tháng | đường, line, xu hướng, trend, thời gian, tháng |
| `progress-target` | connected | 460x130 | Đạt bao nhiêu phần trăm kế hoạch — có mốc mục tiêu nhìn thấy được | tiến độ, progress, mục tiêu, target, kế hoạch, plan |

## Sản phẩm & tính năng

| id | họ | khổ | dùng khi | từ khoá |
|---|---|---|---|---|
| `compare-two` | connected | 520x210 | Cách cũ so với cách LG — đặt cạnh nhau, bên phải là bên thắng | so sánh, compare, trước sau, before after, cũ mới, vs |
| `feature-tiles` | adaptive | 560x230 | Bốn tính năng ngang hàng nhau, không cái nào quan trọng hơn | tính năng, feature, lưới, grid, tile, bốn ô |
| `product-frame` | adaptive | 300x340 | Đặt ảnh sản phẩm cắt nền vào một tấm nền phẳng cho nó chỗ đứng | sản phẩm, product, khung, frame, nền, panel |
| `spec-rows` | adaptive | 480x230 | Ba đến năm dòng thông số sản phẩm, xuất hiện lần lượt | thông số, spec, sản phẩm, product, bảng, table |

## Quy trình & tường thuật

| id | họ | khổ | dùng khi | từ khoá |
|---|---|---|---|---|
| `pillars-three` | adaptive | 540x200 | Ba ý ngang hàng làm xương sống cho một thông điệp | trụ cột, pillar, ba ý, three, giá trị, value |
| `steps-flow` | connected | 560x140 | Một quy trình ba đến bốn bước, nhấn mạnh chúng nối tiếp nhau | bước, step, quy trình, process, flow, chuỗi |
| `timeline-track` | connected | 560x160 | Lộ trình theo mốc thời gian — quý, tháng, giai đoạn triển khai | timeline, trục, thời gian, lộ trình, roadmap, quý |

## Chữ & cấu trúc

| id | họ | khổ | dùng khi | từ khoá |
|---|---|---|---|---|
| `grid-reveal` | connected | 480x270 | Giải thích hệ lưới LG cho người xem, hoặc làm nền cấu trúc cho một slide mở | lưới, grid, hệ thống, system, margin, cấu trúc |
| `headline-rise` | adaptive | 560x200 | Mở đầu một slide hoặc một trang — eyebrow, gạch đỏ, tiêu đề, câu đỡ | tiêu đề, headline, mở đầu, opener, title, eyebrow |
| `quote-pull` | adaptive | 480x180 | Một câu của khách hàng hoặc lãnh đạo, tách ra khỏi phần còn lại | trích dẫn, quote, câu nói, testimonial, khách hàng, phát biểu |

## Trạng thái & nền

| id | họ | khổ | dùng khi | từ khoá |
|---|---|---|---|---|
| `ambient-dots` | fluid | 480x270 | Nền tĩnh cần một chút sống — chỉ dùng khi KHÔNG dùng gradient chính thức | nền, background, ambient, trôi, drift, sống động |
| `loading-dots` | fluid | 120x40 | Trạng thái đang xử lý trong một giao diện — dùng rất tiết chế | loading, chờ, đang xử lý, spinner, state, trạng thái |

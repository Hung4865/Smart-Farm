# 📋 Tổng quan dự án – Smart Farm Management

## 1. Giới thiệu

**Farm Management** là một **Odoo Custom Module** được xây dựng trên nền tảng **Odoo 18** (ERP mã nguồn mở), nhằm số hóa và tự động hóa các quy trình quản lý trong nông trại. Toàn bộ hệ thống được đóng gói và chạy bằng **Docker Compose**, đảm bảo dễ dàng triển khai trên mọi môi trường.

Module được đăng ký với tên `Smart Farm Management` (category: `Agriculture`), tích hợp sẵn vào giao diện Odoo với menu riêng và dashboard trực quan.

---

## 2. Mục tiêu

| Tính năng              | Mô tả                                                                 |
|------------------------|-----------------------------------------------------------------------|
| 📍 Theo dõi GPS        | Ghi nhận tọa độ theo thời gian thực của thiết bị, máy kéo, cảm biến  |
| 🌤️ Ghi log thời tiết   | Gọi API Open-Meteo, lấy nhiệt độ, gió, độ ẩm – lưu vào Odoo ORM     |
| 🔔 Quản lý cảnh báo    | Tạo và theo dõi các cảnh báo nông trại theo mức độ (nguy hiểm/cảnh báo/thông tin) |
| 🖥️ Dashboard tổng quan | Giao diện web hiển thị GPS, thời tiết, cảnh báo, cảm biến và công việc hôm nay |

---

## 3. Kiến trúc hệ thống

```
Farm-Management/
├── README.md                         ← Tài liệu chính của toàn dự án
└── smart_farm/                       ← Odoo Custom Module
    ├── __manifest__.py               ← Khai báo module (name, version, depends, data)
    ├── __init__.py                   ← Import models + controllers
    ├── docker-compose.yml            ← Odoo 18 + PostgreSQL 15 (port 8060)
    ├── requirements.txt              ← Thư viện Python bổ sung (requests)
    ├── .gitignore                    ← Loại trừ cache, venv, data Docker
    ├── models/                       ← Logic nghiệp vụ (Odoo ORM)
    │   ├── __init__.py               ← Import gps, weather, alert
    │   ├── gps.py                    ← Model smart.farm.gps
    │   ├── weather.py                ← Model smart.farm.weather + fetch API
    │   └── alert.py                  ← Model smart.farm.alert + action resolve
    ├── views/                        ← Giao diện XML
    │   ├── dashboard.xml             ← QWeb template dashboard + action URL + menu
    │   ├── menu.xml                  ← Menu chính + sub-menu GPS/Thời tiết/Cảnh báo
    │   ├── gps_views.xml             ← Form & list view cho GPS
    │   ├── weather_views.xml         ← Form & list view cho Thời tiết
    │   └── alert_views.xml           ← Form & list view cho Cảnh báo
    ├── controllers/                  ← HTTP Controller (Web)
    │   ├── __init__.py
    │   └── main.py                   ← Route /smart_farm/dashboard
    ├── security/                     ← Phân quyền truy cập
    │   └── ir.model.access.csv       ← Quyền CRUD cho 3 model
    ├── static/                       ← Assets tĩnh
    │   └── src/
    │       ├── css/dashboard.css     ← CSS tùy chỉnh giao diện dashboard
    │       └── js/dashboard.js       ← JS tương tác (đang phát triển)
    └── docs/                         ← Tài liệu nội bộ
        ├── overview.md               ← File này
        └── CHANGED.md                ← Lịch sử thay đổi
```

---

## 4. Công nghệ sử dụng

| Thành phần        | Công nghệ / Phiên bản              |
|-------------------|------------------------------------|
| ERP Framework     | Odoo **18**                        |
| Cơ sở dữ liệu    | PostgreSQL 15                      |
| Ngôn ngữ          | Python 3                           |
| Giao tiếp API     | REST (Open-Meteo)                  |
| Web Controller    | Odoo HTTP Controller + QWeb        |
| Containerization  | Docker + Docker Compose Plugin     |
| Quản lý mã nguồn  | Git – Feature Branch Workflow      |

---

## 5. Cấu hình hiện tại

| Thông số          | Giá trị                  |
|-------------------|--------------------------|
| Odoo URL          | `http://localhost:8060`  |
| Port container    | `8069` (nội bộ)          |
| Port host         | `8060` (ra ngoài)        |
| Database name     | `Farm_Management`        |
| Admin email       | `admin123@gmail.com`     |
| Odoo image        | `odoo:18`                |
| PostgreSQL image  | `postgres:15`            |
| Module version    | `18.0.1.0.0`             |

---

## 6. Các Model dữ liệu

### `smart.farm.gps`
| Field         | Type      | Mô tả                           |
|---------------|-----------|---------------------------------|
| `name`        | Char      | Tên thiết bị / người dùng       |
| `latitude`    | Float     | Vĩ độ (10 chữ số, 6 thập phân) |
| `longitude`   | Float     | Kinh độ                         |
| `timestamp`   | Datetime  | Thời gian ghi nhận              |
| `device_type` | Selection | phone / tractor / sensor / other|
| `notes`       | Text      | Ghi chú thêm                    |

### `smart.farm.weather`
| Field         | Type      | Mô tả                           |
|---------------|-----------|---------------------------------|
| `name`        | Char      | Tên bản ghi                     |
| `temperature` | Float     | Nhiệt độ (°C)                   |
| `windspeed`   | Float     | Tốc độ gió (km/h)               |
| `humidity`    | Float     | Độ ẩm (%)                       |
| `timestamp`   | Datetime  | Thời gian lấy dữ liệu           |
| `location`    | Char      | Vị trí (mặc định: TP.HCM)      |
| `latitude`    | Float     | Vĩ độ                           |
| `longitude`   | Float     | Kinh độ                         |

### `smart.farm.alert`
| Field         | Type      | Mô tả                                          |
|---------------|-----------|------------------------------------------------|
| `name`        | Char      | Tiêu đề cảnh báo                               |
| `content`     | Text      | Nội dung chi tiết                              |
| `alert_type`  | Selection | danger / warning / info / success              |
| `area`        | Char      | Khu vực liên quan                              |
| `timestamp`   | Datetime  | Thời gian phát sinh                            |
| `is_resolved` | Boolean   | Đã xử lý chưa (action: `action_resolve`)       |

---

## 7. Dashboard (`/smart_farm/dashboard`)

Dashboard được render qua QWeb template `smart_farm.dashboard_main`, bao gồm:

- **Thẻ thống kê**: Diện tích canh tác, số bản ghi GPS, nhiệt độ hiện tại, số cảnh báo chưa xử lý.
- **Card Thời tiết**: Gọi API Open-Meteo trực tiếp (fallback từ DB → mock nếu lỗi).
- **Card Cảnh báo**: Hiển thị 6 cảnh báo mới nhất từ `smart.farm.alert`.
- **Card GPS**: Map đơn giản + danh sách 5 bản ghi GPS gần nhất.
- **Card Cảm biến đất**: Dữ liệu demo (sẽ tích hợp IoT sau).
- **Card Công việc hôm nay**: Task list demo.

---

## 8. Hướng phát triển

- [ ] Hoàn thiện `views/gps_views.xml`, `views/weather_views.xml`, `views/alert_views.xml`
- [ ] Tích hợp cảm biến IoT thực tế qua MQTT
- [ ] Viết Odoo Scheduled Action để tự động lấy thời tiết
- [ ] Phân quyền theo nhóm người dùng (Manager / Worker)
- [ ] Viết unit test cho từng model
- [ ] Thêm biểu đồ thống kê vào Dashboard

---

> 📌 Xem hướng dẫn cài đặt chi tiết tại: [`README.md`](../../README.md)
> 📋 Xem lịch sử thay đổi tại: [`CHANGED.md`](./CHANGED.md)

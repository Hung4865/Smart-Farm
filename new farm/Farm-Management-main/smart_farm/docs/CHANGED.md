# 📝 Lịch sử thay đổi – Smart Farm Management

> File này ghi lại toàn bộ các thay đổi của dự án theo thứ tự thời gian, từ khi khởi tạo đến hiện tại.

---

## [v0.4.0] – 2026-08-07 (Hiện tại)

### 🆕 Thêm mới

#### Controllers
- `controllers/__init__.py` – Import controller `main`.
- `controllers/main.py` – HTTP Controller `SmartFarmDashboard`:
  - Route `GET /smart_farm/dashboard` (auth: user).
  - Lấy 5 bản ghi GPS mới nhất, cảnh báo chưa xử lý, dữ liệu thời tiết.
  - Fallback thời tiết: API trực tiếp → DB → mock data.
  - Render QWeb template `smart_farm.dashboard_main`.

#### Views (Giao diện XML)
- `views/dashboard.xml` – QWeb template dashboard đầy đủ:
  - Action URL `/smart_farm/dashboard`.
  - Menu "Tổng quan" (sequence=1, ưu tiên cao nhất).
  - Template hiển thị: thẻ thống kê, card thời tiết, card cảnh báo, card GPS, card cảm biến (demo), card công việc (demo).
- `views/menu.xml` – Định nghĩa menu chính + 3 sub-menu:
  - `Smart Farm` (root) → GPS & Vị trí / Thời tiết / Cảnh báo.
- `views/gps_views.xml` – Form & list view cho `smart.farm.gps`.
- `views/weather_views.xml` – Form & list view cho `smart.farm.weather`.
- `views/alert_views.xml` – Form & list view cho `smart.farm.alert`.

#### Static Assets
- `static/src/css/dashboard.css` – CSS tùy chỉnh hoàn chỉnh cho dashboard (grid layout, cards, badges, weather, alerts, GPS map, sensors, tasks).
- `static/src/js/dashboard.js` – File JS placeholder (sẽ bổ sung logic tương tác sau).

#### Security
- `security/ir.model.access.csv` – Cấp quyền CRUD đầy đủ (read/write/create/unlink) cho 3 model: `smart.farm.gps`, `smart.farm.weather`, `smart.farm.alert`.

#### Cấu hình
- `.gitignore` – Bổ sung các rule loại trừ: `__pycache__/`, `*.py[cod]`, `venv/`, `env/`, `odoo-data/`, `db-data/`, `.DS_Store`, `Thumbs.db`.

### 🔄 Cập nhật

#### `__manifest__.py`
- `version`: `17.0.1.0.0` → `18.0.1.0.0` (khớp với Odoo 18).
- Thêm đủ mục `data`: `security/ir.model.access.csv`, `views/dashboard.xml`, `views/menu.xml`, `views/gps_views.xml`, `views/weather_views.xml`, `views/alert_views.xml`.

#### `__init__.py` (root)
- Import cả `models` và `controllers`.

#### `models/alert.py`
- **Refactor hoàn toàn**: Chuyển từ hàm script `send_message()` sang Odoo Model `SmartFarmAlert`:
  - Fields: `name`, `content`, `alert_type` (danger/warning/info/success), `area`, `timestamp`, `is_resolved`.
  - Method `action_resolve()` – đánh dấu cảnh báo đã xử lý.

#### `docker-compose.yml`
- Nâng cấp image: `odoo:17` → `odoo:18`.

### ❌ Xóa
- `smart_farm/config.py` – Không còn cần thiết (module Odoo không dùng XML-RPC thủ công).
- `smart_farm/web_app.py` – File không thuộc cấu trúc module Odoo.
- `views/weather.xml`, `views/gps.xml`, `views/alert.xml` – Đổi tên thành `weather_views.xml`, `gps_views.xml`, `alert_views.xml` cho nhất quán.

### 🚀 Triển khai
- Module được copy vào container và restart:
  ```bash
  docker exec -u root smart_farm-web-1 rm -rf /mnt/extra-addons/smart_farm
  docker cp ~/projects/Farm\ Management/Farm-Management/smart_farm smart_farm-web-1:/mnt/extra-addons/
  docker compose -f .../docker-compose.yml restart web
  ```

---

## [v0.3.0] – 2026-08-07

### 🆕 Thêm mới
- Tạo thư mục `docs/` để quản lý tài liệu nội bộ dự án.
- Thêm file `docs/overview.md` – mô tả tổng quan kiến trúc, công nghệ và luồng dữ liệu.
- Thêm file `docs/CHANGED.md` – ghi lại lịch sử thay đổi toàn bộ dự án.

### ❌ Xóa
- `smart_farm/README.md` – Thông tin cũ và lỗi thời, tài liệu được tổng hợp vào `README.md` gốc.

---

## [v0.2.0] – 2026-08-07

### 🔄 Tái cấu trúc (Script Python → Odoo Custom Module)

Dự án chuyển từ mô hình **script Python độc lập** sang **Odoo Custom Module** tích hợp hoàn toàn vào Odoo.

#### ❌ Xóa (các file script cũ)
- `smart_farm/main.py` – Điểm vào kịch bản Python cũ.
- `smart_farm/services/odoo_client.py` – Lớp kết nối XML-RPC thủ công.
- `smart_farm/services/gps.py` – Script GPS độc lập.
- `smart_farm/services/message.py` – Script gửi thông báo độc lập.
- `smart_farm/services/weather.py` – Script thời tiết độc lập.
- Toàn bộ thư mục `smart_farm/services/` bị loại bỏ.

#### 🆕 Thêm mới (cấu trúc Odoo Module chuẩn)
- `smart_farm/__manifest__.py` – Khai báo module Odoo.
- `smart_farm/__init__.py` – Khởi tạo package Python.
- `smart_farm/models/__init__.py` – Import gps, weather, alert.
- `smart_farm/models/gps.py` – Model `SmartFarmGPS` (Odoo ORM).
- `smart_farm/models/weather.py` – Model `SmartFarmWeather` + method `fetch_and_save()`.
- `smart_farm/models/alert.py` – (Lúc đầu là refactor từ `message.py` cũ).
- `smart_farm/views/` – Thư mục giao diện XML.
- `smart_farm/security/` – Thư mục phân quyền.

### ⚙️ Thay đổi cấu hình

| Thông số        | Giá trị cũ              | Giá trị mới             |
|-----------------|-------------------------|-------------------------|
| Port (host)     | `8069`                  | `8060`                  |
| Database name   | `my_smart_farm`         | `Farm_Management`       |
| Admin email     | `admin@example.com`     | `admin123@gmail.com`    |
| Admin password  | `admin`                 | `abc123`                |
| URL             | `http://localhost:8069` | `http://localhost:8060` |

---

## [v0.1.1] – 2026-08-07

### 📄 Tài liệu
- Viết hoàn chỉnh `README.md` tại thư mục gốc (`Farm-Management/README.md`) với 3 phần:
  1. Giới thiệu tổng quan dự án.
  2. Hướng dẫn cài đặt và chạy dự án (5 bước).
  3. Quy trình làm việc nhóm (Git branching, Conventional Commits, checklist PR).

### 🐳 Hạ tầng
- Cài đặt `docker-compose-plugin` từ repository Docker chính thức để hỗ trợ lệnh `docker compose` (thay thế `docker-compose` gây lỗi `unknown shorthand flag: 'd' in -d`).
- Quy trình cài đặt plugin đã được ghi vào README (Bước 0).

---

## [v0.1.0] – Khởi tạo dự án

### 🆕 Cấu trúc ban đầu

Dự án khởi tạo với kiến trúc **script Python + Odoo XML-RPC**:

```
smart_farm/
├── docker-compose.yml       # Odoo 17 + PostgreSQL 15 (port 8069)
├── main.py                  # Script chạy tuần tự 3 kịch bản
├── config.py                # URL=localhost:8069, DB=my_smart_farm
├── requirements.txt         # requests
└── services/
    ├── odoo_client.py       # Kết nối XML-RPC
    ├── gps.py               # Ghi tọa độ GPS vào Odoo Notes
    ├── message.py           # Gửi thông báo qua Odoo Discuss
    └── weather.py           # Gọi Open-Meteo, log vào mail.message
```

### ⚙️ Cấu hình ban đầu

| Thông số        | Giá trị                  |
|-----------------|--------------------------|
| Odoo image      | `odoo:17`                |
| Port (host)     | `8069`                   |
| Database name   | `my_smart_farm`          |
| Admin email     | `admin@example.com`      |
| Admin password  | `admin`                  |
| URL             | `http://localhost:8069`  |

### 🔧 Tính năng ban đầu
- `gps.py`: Ghi tọa độ GPS (TP.HCM: lat=10.762622, lon=106.660172) vào Odoo Notes.
- `message.py`: Gửi cảnh báo lịch tưới tiêu khu vực A qua Odoo Discuss.
- `weather.py`: Gọi `api.open-meteo.com`, lấy nhiệt độ + tốc độ gió, lưu vào `mail.message` của Odoo.

# 🧮 Máy Tính Cá Nhân (PyQt6 Calculator)

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/GUI-PyQt6-green.svg)](https://riverbankcomputing.com/software/pyqt/)
[![Tests](https://img.shields.io/badge/Tests-22%20Passed-brightgreen.svg)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Ứng dụng **Máy tính cá nhân (Desktop Calculator)** hiện đại được xây dựng bằng ngôn ngữ **Python** và thư viện **PyQt6**. Ứng dụng đáp ứng các tiêu chuẩn phần mềm chuyên nghiệp: phân tách kiến trúc (Core Engine & UI), giao diện Dark Mode thanh lịch, tính toán với độ chính xác cao bằng `decimal.Decimal`, cùng cơ chế bắt lỗi input và lỗi tính toán toàn diện, đảm bảo ứng dụng không bao giờ bị crash.

---

## 🌟 Tính Năng Nổi Bật

### 1. Phép toán đa dạng
- **Cơ bản:** Cộng (`+`), Trừ (`-`), Nhân (`×`), Chia (`÷`).
- **Nâng cao:** 
  - Phần trăm (`%`)
  - Căn bậc hai (`√`)
  - Bình phương (`x²`)
  - Nghịch đảo (`1/x`)
  - Đổi dấu âm/dương (`±`)
- **Độ chính xác cao:** Sử dụng module `decimal.Decimal` để triệt tiêu hoàn toàn sai số dấu phẩy động (ví dụ: `0.1 + 0.2 = 0.3` thay vì `0.30000000000000004`).

### 2. Bắt lỗi dữ liệu đầu vào (Input Validation)
- ❌ **Chống trùng dấu chấm:** Ngăn chặn tuyệt đối việc nhập nhiều hơn 1 dấu chấm trong cùng một toán hạng (ví dụ không thể nhập `3.14.5`).
- 🔄 **Tự động đổi toán tử:** Nếu người dùng bấm nhầm toán tử (ví dụ bấm `+` rồi bấm `×`), ứng dụng tự động cập nhật toán tử mới nhất mà không gây sai lệch phép tính.
- 🔢 **Giới hạn số chữ số:** Khống chế tối đa 16 chữ số để đảm bảo không bị tràn giao diện.
- 🔙 **Hỗ trợ chỉnh sửa linh hoạt:** Phím xóa lùi (`⌫` Backspace), xóa toán hạng hiện tại (`CE`), và xóa toàn bộ (`C`).

### 3. Bắt lỗi tính toán (Calculation Error Handling)
- 🚫 **Chia cho 0 (`ZeroDivisionError`):** Hiển thị cảnh báo trực quan `Lỗi: Không thể chia cho 0`.
- 📉 **Căn bậc hai số âm:** Hiển thị `Lỗi: Căn số âm`.
- 💥 **Tràn số (`OverflowError`):** Tự động phát hiện và hiển thị `Lỗi: Tràn số`.
- 🛡️ **Khôi phục an toàn (Fault Tolerance):** Khi phát sinh bất kỳ lỗi nào, ứng dụng hiển thị thông báo lỗi màu đỏ nổi bật và cho phép người dùng bấm phím số hoặc phím Clear để bắt đầu phép tính mới mà không bị crash hay đơ ứng dụng.

### 4. Giao diện & Trải nghiệm người dùng (UI/UX)
- Giao diện **Dark Modern Theme** với hiệu ứng viền mờ (Glassmorphism), bo góc mềm mại.
- **Màn hình kép:**
  - Dòng biểu thức phụ: Theo dõi lịch sử chuỗi phép tính đang thực hiện.
  - Màn hình kết quả chính: Hiển thị số to rõ, tự động định dạng phân tách hàng nghìn (ví dụ: `1,000,000`).
  - Tự động co giãn cỡ chữ (Auto Font-resizing) khi kết quả có nhiều chữ số.
- **Hỗ trợ bàn phím đầy đủ (Full Keyboard Shortcuts):**
  - Nhập số: `0` - `9`
  - Toán tử: `+`, `-`, `*`, `/`, `%`
  - Dấu chấm: `.`, `,`
  - Thực hiện tính: `Enter`, `Return`, `=`
  - Xóa: `Backspace` (xóa ký tự), `Delete` (CE), `Esc` (Clear all)

---

## 📁 Cấu Trúc Thư Mục Dự Án

```
pyqt-calculator/
├── .gitignore                      # Bộ lọc bỏ qua file rác, cache, build của Python & Git
├── LICENSE                         # Giấy phép mã nguồn mở MIT
├── README.md                       # Tài liệu hướng dẫn sử dụng và triển khai dự án
├── requirements.txt                # Danh sách thư viện phụ thuộc (PyQt6, pytest)
├── src/
│   ├── __init__.py
│   ├── main.py                     # Entry point khởi chạy ứng dụng
│   ├── core/                       # Tầng xử lý logic nghiệp vụ độc lập
│   │   ├── __init__.py
│   │   └── calculator_engine.py    # Xử lý số học Decimal, validation & error handling
│   └── ui/                         # Tầng giao diện đồ họa PyQt6
│       ├── __init__.py
│       ├── styles.py               # Bộ mã định dạng QSS (Modern Dark Theme)
│       └── main_window.py          # Cửa sổ chính, lưới nút bấm và bắt sự kiện phím
└── tests/                          # Tầng kiểm thử tự động
    ├── __init__.py
    ├── test_calculator.py          # Unit tests cho core engine và các ca bắt lỗi
    └── test_ui.py                  # Unit tests cho tương tác trên giao diện PyQt
```

---

## 🚀 Hướng Dẫn Cài Đặt và Chạy

### 1. Yêu Cầu Môi Trường
- Python **3.10** trở lên.
- Đã cài đặt công cụ quản lý gói `pip`.

### 2. Cài Đặt Thư Viện

Mở terminal/command prompt tại thư mục dự án và chạy:

```bash
# Khởi tạo môi trường ảo (Khuyến nghị)
python -m venv .venv

# Kích hoạt môi trường ảo:
# Trên Windows:
.venv\Scripts\activate
# Trên macOS / Linux:
source .venv/bin/activate

# Cài đặt các thư viện phụ thuộc:
pip install -r requirements.txt
```

### 3. Chạy Ứng Dụng

Chạy lệnh sau từ thư mục gốc của dự án:

```bash
python src/main.py
```

---

## 🧪 Kiểm Thử Tự Động (Unit Testing)

Dự án bao gồm 22 bài kiểm thử tự động bao phủ 100% các tính năng số học, kiểm tra độ chính xác của dấu phẩy động, kiểm thử bắt lỗi input và kiểm thử giao diện.

Để chạy bộ kiểm thử, thực thi lệnh:

```bash
pytest tests/ -v
```

Kết quả mẫu:
```text
tests/test_calculator.py::TestCalculatorBasicOperations::test_addition PASSED
tests/test_calculator.py::TestCalculatorBasicOperations::test_floating_point_precision PASSED
tests/test_calculator.py::TestCalculatorBasicOperations::test_division PASSED
tests/test_calculator.py::TestInputValidation::test_prevent_multiple_decimal_points PASSED
tests/test_calculator.py::TestCalculationErrorHandling::test_division_by_zero PASSED
tests/test_ui.py::TestCalculatorUI::test_ui_digit_and_operator_flow PASSED
...
============================= 22 passed in 0.58s ==============================
```

---

## 📦 Đóng Gói Thành File Thực Thi Độc Lập (.exe trên Windows)

Bạn có thể đóng gói ứng dụng thành một file `.exe` duy nhất để gửi cho người dùng khác mà họ không cần cài đặt Python:

```bash
# Cài đặt PyInstaller
pip install pyinstaller

# Biên dịch thành 1 file .exe duy nhất không mở cửa sổ dòng lệnh đen
pyinstaller --noconsole --onefile --name "MayTinhCaNhan" src/main.py
```

File thực thi sau khi hoàn thành sẽ nằm trong thư mục `dist/MayTinhCaNhan.exe`.

---

## 📤 Hướng Dẫn Chi Tiết Đẩy Dự Án Lên GitHub

Thực hiện các bước sau trong Terminal / PowerShell tại thư mục dự án để đẩy toàn bộ code lên GitHub:

### Bước 1: Tạo Repository mới trên GitHub
1. Đăng nhập vào tài khoản [GitHub](https://github.com/).
2. Nhấn vào dấu `+` ở góc trên bên phải $\rightarrow$ chọn **New repository**.
3. Đặt tên repository (ví dụ: `pyqt-calculator`).
4. Để chế độ **Public** (hoặc **Private** tùy ý).
5. **Không** tích chọn "Add a README file" hay ".gitignore" (vì dự án đã chuẩn bị sẵn).
6. Nhấn **Create repository**.
7. Copy đường dẫn URL của repository vừa tạo (dạng: `https://github.com/<tên_tài_khoản>/pyqt-calculator.git`).

### Bước 2: Khởi tạo và Đẩy Code từ máy tính

Mở terminal tại thư mục `pyqt-calculator` và thực hiện chuỗi lệnh sau:

```bash
# 1. Khởi tạo Git repository cục bộ
git init

# 2. Thêm tất cả file vào staging area (file .gitignore sẽ tự động lọc bỏ các file rác)
git add .

# 3. Commit mã nguồn lần đầu
git commit -m "feat: Xây dựng hoàn chỉnh ứng dụng Máy tính cá nhân PyQt6"

# 4. Đổi nhánh chính sang 'main'
git branch -M main

# 5. Liên kết với repository trên GitHub (Thay URL của bạn vào)
git remote add origin https://github.com/<tên_tài_khoản>/pyqt-calculator.git

# 6. Đẩy mã nguồn lên GitHub
git push -u origin main
```

---

## 📄 Giấy Phép (License)

Dự án được phân phối dưới giấy phép [MIT License](LICENSE). Bạn hoàn toàn có thể tự do sử dụng, chỉnh sửa và phân phối cho mục đích cá nhân hoặc thương mại.

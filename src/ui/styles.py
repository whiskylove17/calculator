"""
Module định nghĩa phong cách giao diện (QSS Stylesheet) cho ứng dụng máy tính.
Thiết kế Dark Modern Theme sang trọng, bo góc, hiệu ứng hover/pressed mượt mà.
"""

CALCULATOR_STYLESHEET = """
/* Toàn bộ cửa sổ chính */
QMainWindow {
    background-color: #121417;
}

QWidget#CentralWidget {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #181b20, stop:1 #121417);
    border-radius: 16px;
}

/* Màn hình hiển thị chính & phụ */
QFrame#DisplayContainer {
    background-color: #1a1e24;
    border-radius: 14px;
    border: 1px solid #282e38;
    padding: 12px 16px;
}

QLabel#HistoryLabel {
    color: #7d8b99;
    font-family: 'Segoe UI', -apple-system, Roboto, sans-serif;
    font-size: 14px;
    font-weight: 500;
    qproperty-alignment: 'AlignRight | AlignVCenter';
    background: transparent;
    border: none;
    min-height: 22px;
}

QLabel#DisplayLabel {
    color: #ffffff;
    font-family: 'Segoe UI', -apple-system, Roboto, sans-serif;
    font-size: 34px;
    font-weight: 600;
    qproperty-alignment: 'AlignRight | AlignVCenter';
    background: transparent;
    border: none;
    min-height: 48px;
}

QLabel#DisplayLabel[error="true"] {
    color: #ff5252;
    font-size: 20px;
    font-weight: 600;
}

/* Định dạng chung cho nút bấm */
QPushButton {
    font-family: 'Segoe UI', -apple-system, Roboto, sans-serif;
    font-size: 18px;
    font-weight: 600;
    border-radius: 12px;
    border: 1px solid transparent;
    outline: none;
    min-width: 54px;
    min-height: 52px;
}

/* Nhóm phím số (0-9, .) */
QPushButton[btn_type="number"] {
    background-color: #262a32;
    color: #f0f3f6;
    border: 1px solid #323842;
}
QPushButton[btn_type="number"]:hover {
    background-color: #313742;
    border: 1px solid #444d5c;
}
QPushButton[btn_type="number"]:pressed {
    background-color: #1e2127;
}

/* Nhóm phím toán tử cơ bản (+, -, ×, ÷) */
QPushButton[btn_type="operator"] {
    background-color: #ff9500;
    color: #ffffff;
    font-size: 22px;
}
QPushButton[btn_type="operator"]:hover {
    background-color: #ffa726;
}
QPushButton[btn_type="operator"]:pressed {
    background-color: #e68500;
}

/* Phím bằng (=) */
QPushButton[btn_type="equals"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ff9500, stop:1 #e06c00);
    color: #ffffff;
    font-size: 24px;
    font-weight: 700;
    border-radius: 12px;
}
QPushButton[btn_type="equals"]:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ffa726, stop:1 #ef7d13);
}
QPushButton[btn_type="equals"]:pressed {
    background: #cc6000;
}

/* Nhóm phím chức năng đặc biệt (C, CE, ⌫, ±, %, √, x²) */
QPushButton[btn_type="action"] {
    background-color: #343a46;
    color: #38ef7d;
    font-size: 16px;
    border: 1px solid #404857;
}
QPushButton[btn_type="action"]:hover {
    background-color: #404856;
    color: #4eef8d;
    border: 1px solid #525c6e;
}
QPushButton[btn_type="action"]:pressed {
    background-color: #292d37;
}

/* Phím xóa (C / CE / ⌫) nổi bật */
QPushButton[btn_type="clear"] {
    background-color: #36292b;
    color: #ff6b6b;
    font-size: 16px;
    border: 1px solid #4e3538;
}
QPushButton[btn_type="clear"]:hover {
    background-color: #4a3437;
    color: #ff8585;
    border: 1px solid #634347;
}
QPushButton[btn_type="clear"]:pressed {
    background-color: #2a1f21;
}

/* Thanh menu hoặc trạng thái */
QStatusBar {
    color: #5d6773;
    font-size: 11px;
    background: transparent;
}
"""

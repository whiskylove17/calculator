"""
Giao diện chính của ứng dụng Máy tính cá nhân (PyQt6).
Bao gồm màn hình hiển thị hai dòng, lưới phím bấm hiện đại và hỗ trợ bàn phím đầy đủ.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QKeyEvent, QIcon

from core.calculator_engine import CalculatorEngine
from ui.styles import CALCULATOR_STYLESHEET


class CalculatorMainWindow(QMainWindow):
    """Cửa sổ chính của ứng dụng Máy tính cá nhân."""

    def __init__(self):
        super().__init__()
        self.engine = CalculatorEngine()
        self._init_ui()
        self._apply_styles()
        self._update_display()

    def _init_ui(self):
        """Khởi tạo các thành phần giao diện."""
        self.setWindowTitle("Máy Tính Cá Nhân")
        self.setFixedSize(360, 520)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Widget trung tâm
        central_widget = QWidget(self)
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)

        # Layout chính dạng dọc
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # ----------------- Khung Màn Hình Hiển Thị -----------------
        display_frame = QFrame()
        display_frame.setObjectName("DisplayContainer")
        display_layout = QVBoxLayout(display_frame)
        display_layout.setContentsMargins(12, 10, 12, 10)
        display_layout.setSpacing(4)

        # Màn hình phụ (lịch sử/biểu thức)
        self.history_label = QLabel("")
        self.history_label.setObjectName("HistoryLabel")
        display_layout.addWidget(self.history_label)

        # Màn hình chính (số hiện tại / kết quả / lỗi)
        self.display_label = QLabel("0")
        self.display_label.setObjectName("DisplayLabel")
        self.display_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        display_layout.addWidget(self.display_label)

        main_layout.addWidget(display_frame)

        # ----------------- Lưới Nút Bấm -----------------
        grid_layout = QGridLayout()
        grid_layout.setSpacing(8)

        # Cấu hình nút: (Nhãn hiển thị, Loại nút, callback hoặc tham số)
        # Hàng 0: %, CE, C, ⌫
        # Hàng 1: 1/x, x², √, ÷
        # Hàng 2: 7, 8, 9, ×
        # Hàng 3: 4, 5, 6, -
        # Hàng 4: 1, 2, 3, +
        # Hàng 5: ±, 0, ., =
        button_rows = [
            [
                ("%", "action", lambda: self._on_unary_op("percent")),
                ("CE", "clear", self._on_clear_entry),
                ("C", "clear", self._on_clear),
                ("⌫", "clear", self._on_backspace),
            ],
            [
                ("1/x", "action", lambda: self._on_unary_op("reciprocal")),
                ("x²", "action", lambda: self._on_unary_op("square")),
                ("√", "action", lambda: self._on_unary_op("sqrt")),
                ("÷", "operator", lambda: self._on_operator("/")),
            ],
            [
                ("7", "number", lambda: self._on_digit("7")),
                ("8", "number", lambda: self._on_digit("8")),
                ("9", "number", lambda: self._on_digit("9")),
                ("×", "operator", lambda: self._on_operator("*")),
            ],
            [
                ("4", "number", lambda: self._on_digit("4")),
                ("5", "number", lambda: self._on_digit("5")),
                ("6", "number", lambda: self._on_digit("6")),
                ("-", "operator", lambda: self._on_operator("-")),
            ],
            [
                ("1", "number", lambda: self._on_digit("1")),
                ("2", "number", lambda: self._on_digit("2")),
                ("3", "number", lambda: self._on_digit("3")),
                ("+", "operator", lambda: self._on_operator("+")),
            ],
            [
                ("±", "action", self._on_toggle_sign),
                ("0", "number", lambda: self._on_digit("0")),
                (".", "number", self._on_decimal_point),
                ("=", "equals", self._on_equals),
            ],
        ]

        for r, row_data in enumerate(button_rows):
            for c, (text, btn_type, handler) in enumerate(row_data):
                btn = QPushButton(text)
                btn.setProperty("btn_type", btn_type)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                btn.clicked.connect(handler)
                grid_layout.addWidget(btn, r, c)

        main_layout.addLayout(grid_layout)

    def _apply_styles(self):
        """Áp dụng stylesheet cho toàn bộ cửa sổ."""
        self.setStyleSheet(CALCULATOR_STYLESHEET)

    # ----------------- Cập nhật hiển thị UI -----------------
    def _update_display(self):
        """Cập nhật nội dung màn hình chính và phụ theo trạng thái Engine."""
        self.history_label.setText(self.engine.expression_history)

        raw_text = self.engine.display_text
        has_error = self.engine.has_error

        # Đổi kiểu dáng nếu bị lỗi
        self.display_label.setProperty("error", "true" if has_error else "false")
        self.display_label.style().unpolish(self.display_label)
        self.display_label.style().polish(self.display_label)

        if has_error:
            self.display_label.setText(raw_text)
            return

        # Định dạng dấu phẩy hàng nghìn nếu là số hợp lệ
        formatted = self._format_display_number(raw_text)
        self.display_label.setText(formatted)

        # Điều chỉnh kích thước font tự động nếu chuỗi quá dài
        self._adjust_font_size(formatted)

    def _format_display_number(self, text: str) -> str:
        """Định dạng số với dấu phân cách hàng nghìn (ví dụ 1000000 -> 1,000,000)."""
        if "E" in text or "e" in text:
            return text

        parts = text.split(".")
        int_part = parts[0]
        # Thêm dấu phân cách cho phần nguyên
        try:
            if int_part.startswith("-"):
                formatted_int = "-" + f"{int(int_part[1:]):,}" if len(int_part) > 1 else "-"
            else:
                formatted_int = f"{int(int_part):,}"
        except ValueError:
            formatted_int = int_part

        if len(parts) > 1:
            return f"{formatted_int}.{parts[1]}"
        elif text.endswith("."):
            return f"{formatted_int}."
        return formatted_int

    def _adjust_font_size(self, text: str):
        """Tự động thu nhỏ cỡ chữ nếu số quá dài tránh tràn màn hình."""
        length = len(text)
        if length > 16:
            font_size = "18px"
        elif length > 12:
            font_size = "22px"
        elif length > 9:
            font_size = "28px"
        else:
            font_size = "34px"

        self.display_label.setStyleSheet(f"font-size: {font_size};")

    # ----------------- Xử lý Sự kiện Nút Bấm -----------------
    def _on_digit(self, digit: str):
        """Nhập chữ số."""
        self.engine.input_digit(digit)
        self._update_display()

    def _on_decimal_point(self):
        """Nhập dấu chấm thập phân."""
        self.engine.input_decimal_point()
        self._update_display()

    def _on_operator(self, op: str):
        """Nhập toán tử hai ngôi (+, -, *, /)."""
        self.engine.set_operator(op)
        self._update_display()

    def _on_unary_op(self, op_type: str):
        """Xử lý các phép toán một ngôi."""
        if op_type == "percent":
            self.engine.calculate_percent()
        elif op_type == "sqrt":
            self.engine.calculate_square_root()
        elif op_type == "square":
            self.engine.calculate_square()
        elif op_type == "reciprocal":
            self.engine.calculate_reciprocal()
        self._update_display()

    def _on_toggle_sign(self):
        """Đổi dấu ±."""
        self.engine.toggle_sign()
        self._update_display()

    def _on_equals(self):
        """Tính kết quả (=)."""
        self.engine.calculate_equals()
        self._update_display()

    def _on_clear(self):
        """Xóa toàn bộ (C)."""
        self.engine.clear()
        self._update_display()

    def _on_clear_entry(self):
        """Xóa mục hiện tại (CE)."""
        self.engine.clear_entry()
        self._update_display()

    def _on_backspace(self):
        """Xóa lùi (⌫)."""
        self.engine.backspace()
        self._update_display()

    # ----------------- Hỗ trợ Bàn phím (Keyboard Shortcuts) -----------------
    def keyPressEvent(self, event: QKeyEvent):
        """Bắt sự kiện gõ phím từ bàn phím vật lý."""
        key = event.key()
        text = event.text()

        # Phím số (0-9)
        if text in "0123456789":
            self._on_digit(text)
            event.accept()
            return

        # Phím chấm thập phân
        if text in (".", ","):
            self._on_decimal_point()
            event.accept()
            return

        # Toán tử
        if text == "+":
            self._on_operator("+")
            event.accept()
            return
        elif text == "-":
            self._on_operator("-")
            event.accept()
            return
        elif text == "*":
            self._on_operator("*")
            event.accept()
            return
        elif text == "/":
            self._on_operator("/")
            event.accept()
            return
        elif text == "%":
            self._on_unary_op("percent")
            event.accept()
            return
        elif text == "=" or key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._on_equals()
            event.accept()
            return
        elif key == Qt.Key.Key_Backspace:
            self._on_backspace()
            event.accept()
            return
        elif key == Qt.Key.Key_Escape:
            self._on_clear()
            event.accept()
            return
        elif key == Qt.Key.Key_Delete:
            self._on_clear_entry()
            event.accept()
            return

        super().keyPressEvent(event)

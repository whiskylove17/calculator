"""
Kiểm thử tự động cho giao diện PyQt6 CalculatorMainWindow.
Đảm bảo tất cả widget, nút bấm và hiển thị hoạt động chính xác.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from PyQt6.QtWidgets import QApplication
from ui.main_window import CalculatorMainWindow

# Khởi tạo QApplication cho môi trường test nếu chưa có
_app = QApplication.instance() or QApplication(sys.argv)


class TestCalculatorUI:
    """Kiểm thử tương tác giao diện người dùng."""

    def setup_method(self):
        self.window = CalculatorMainWindow()

    def teardown_method(self):
        self.window.close()

    def test_initial_display(self):
        """Màn hình ban đầu hiển thị số 0 và không có lỗi."""
        assert self.window.display_label.text() == "0"
        assert self.window.history_label.text() == ""

    def test_ui_digit_and_operator_flow(self):
        """Kiểm thử luồng bấm phím trên UI: 12 + 8 = 20."""
        self.window._on_digit("1")
        self.window._on_digit("2")
        assert self.window.display_label.text() == "12"

        self.window._on_operator("+")
        assert self.window.history_label.text() == "12 +"

        self.window._on_digit("8")
        self.window._on_equals()
        assert self.window.display_label.text() == "20"
        assert "12 + 8 =" in self.window.history_label.text()

    def test_ui_division_by_zero_error_styling(self):
        """Kiểm thử khi chia cho 0 trên UI thì nhãn hiển thị báo lỗi."""
        self.window._on_digit("9")
        self.window._on_operator("/")
        self.window._on_digit("0")
        self.window._on_equals()

        assert "chia cho 0" in self.window.display_label.text().lower()
        assert self.window.display_label.property("error") == "true"

    def test_ui_clear_action(self):
        """Kiểm thử nút Clear (C)."""
        self.window._on_digit("5")
        self.window._on_clear()
        assert self.window.display_label.text() == "0"
        assert self.window.history_label.text() == ""

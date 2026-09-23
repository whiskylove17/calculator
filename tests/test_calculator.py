"""
Unit tests cho CalculatorEngine.
Kiểm thử toàn diện các phép tính số học, logic bắt lỗi input và bắt lỗi tính toán.
"""

import sys
import os
import pytest

# Thêm đường dẫn thư mục src vào sys.path để import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from core.calculator_engine import CalculatorEngine


class TestCalculatorBasicOperations:
    """Kiểm thử các phép tính số học cơ bản (+, -, *, /)."""

    def setup_method(self):
        self.calc = CalculatorEngine()

    def test_addition(self):
        """Kiểm thử phép cộng: 15 + 27 = 42."""
        for d in "15":
            self.calc.input_digit(d)
        self.calc.set_operator("+")
        for d in "27":
            self.calc.input_digit(d)
        self.calc.calculate_equals()
        assert self.calc.display_text == "42"
        assert not self.calc.has_error

    def test_floating_point_precision(self):
        """Kiểm thử độ chính xác dấu phẩy động: 0.1 + 0.2 = 0.3 (không bị lỗi 0.30000000000000004)."""
        self.calc.input_digit("0")
        self.calc.input_decimal_point()
        self.calc.input_digit("1")
        self.calc.set_operator("+")
        self.calc.input_digit("0")
        self.calc.input_decimal_point()
        self.calc.input_digit("2")
        self.calc.calculate_equals()
        assert self.calc.display_text == "0.3"

    def test_subtraction(self):
        """Kiểm thử phép trừ: 100 - 35 = 65, và 10 - 25 = -15."""
        for d in "100":
            self.calc.input_digit(d)
        self.calc.set_operator("-")
        for d in "35":
            self.calc.input_digit(d)
        self.calc.calculate_equals()
        assert self.calc.display_text == "65"

        self.calc.reset()
        for d in "10":
            self.calc.input_digit(d)
        self.calc.set_operator("-")
        for d in "25":
            self.calc.input_digit(d)
        self.calc.calculate_equals()
        assert self.calc.display_text == "-15"

    def test_multiplication(self):
        """Kiểm thử phép nhân: 12 * 8 = 96."""
        for d in "12":
            self.calc.input_digit(d)
        self.calc.set_operator("*")
        for d in "8":
            self.calc.input_digit(d)
        self.calc.calculate_equals()
        assert self.calc.display_text == "96"

    def test_division(self):
        """Kiểm thử phép chia: 25 / 4 = 6.25."""
        for d in "25":
            self.calc.input_digit(d)
        self.calc.set_operator("/")
        for d in "4":
            self.calc.input_digit(d)
        self.calc.calculate_equals()
        assert self.calc.display_text == "6.25"

    def test_chained_operations(self):
        """Kiểm thử chuỗi phép tính liên tục: 10 + 5 * 2 = (15) * 2 = 30."""
        for d in "10":
            self.calc.input_digit(d)
        self.calc.set_operator("+")
        for d in "5":
            self.calc.input_digit(d)
        self.calc.set_operator("*")  # Tính 10 + 5 = 15 trước
        assert self.calc.display_text == "15"
        for d in "2":
            self.calc.input_digit(d)
        self.calc.calculate_equals()
        assert self.calc.display_text == "30"


class TestCalculatorUnaryOperations:
    """Kiểm thử các phép toán một ngôi (căn bậc hai, bình phương, đổi dấu, phần trăm)."""

    def setup_method(self):
        self.calc = CalculatorEngine()

    def test_square_root(self):
        """Kiểm thử căn bậc hai: √81 = 9."""
        for d in "81":
            self.calc.input_digit(d)
        self.calc.calculate_square_root()
        assert self.calc.display_text == "9"

    def test_square(self):
        """Kiểm thử bình phương: 12² = 144."""
        for d in "12":
            self.calc.input_digit(d)
        self.calc.calculate_square()
        assert self.calc.display_text == "144"

    def test_toggle_sign(self):
        """Kiểm thử đổi dấu ±."""
        for d in "45":
            self.calc.input_digit(d)
        self.calc.toggle_sign()
        assert self.calc.display_text == "-45"
        self.calc.toggle_sign()
        assert self.calc.display_text == "45"

    def test_percent(self):
        """Kiểm thử phần trăm: 50% = 0.5."""
        for d in "50":
            self.calc.input_digit(d)
        self.calc.calculate_percent()
        assert self.calc.display_text == "0.5"

    def test_reciprocal(self):
        """Kiểm thử nghịch đảo: 1/4 = 0.25, và 1/0 -> lỗi."""
        for d in "4":
            self.calc.input_digit(d)
        self.calc.calculate_reciprocal()
        assert self.calc.display_text == "0.25"

        self.calc.reset()
        self.calc.input_digit("0")
        self.calc.calculate_reciprocal()
        assert self.calc.has_error is True
        assert "chia cho 0" in self.calc.display_text.lower()



class TestInputValidation:
    """Kiểm thử cơ chế bắt lỗi dữ liệu đầu vào (Input Validation)."""

    def setup_method(self):
        self.calc = CalculatorEngine()

    def test_prevent_multiple_decimal_points(self):
        """Không cho phép nhập nhiều hơn 1 dấu chấm thập phân trong 1 số (vd: 3.14.5)."""
        self.calc.input_digit("3")
        res1 = self.calc.input_decimal_point()
        assert res1 is True
        self.calc.input_digit("1")
        self.calc.input_digit("4")
        res2 = self.calc.input_decimal_point()  # Thử nhập dấu chấm thứ hai
        assert res2 is False
        self.calc.input_digit("5")
        assert self.calc.display_text == "3.145"

    def test_operator_replacement(self):
        """Người dùng bấm nhầm toán tử và đổi toán tử liên tiếp (5 + * 4 = 20)."""
        self.calc.input_digit("5")
        self.calc.set_operator("+")
        self.calc.set_operator("*")  # Thay đổi thành nhân
        self.calc.input_digit("4")
        self.calc.calculate_equals()
        assert self.calc.display_text == "20"

    def test_backspace(self):
        """Kiểm thử nút xóa ký tự lùi (Backspace)."""
        for d in "123":
            self.calc.input_digit(d)
        assert self.calc.display_text == "123"
        self.calc.backspace()
        assert self.calc.display_text == "12"
        self.calc.backspace()
        assert self.calc.display_text == "1"
        self.calc.backspace()
        assert self.calc.display_text == "0"

    def test_max_digits_limit(self):
        """Kiểm tra giới hạn số lượng chữ số nhập vào để tránh tràn UI."""
        for _ in range(self.calc.MAX_DIGITS + 5):
            self.calc.input_digit("9")
        assert len(self.calc.display_text) == self.calc.MAX_DIGITS


class TestCalculationErrorHandling:
    """Kiểm thử cơ chế bắt lỗi tính toán (Division by Zero, căn số âm, v.v.)."""

    def setup_method(self):
        self.calc = CalculatorEngine()

    def test_division_by_zero(self):
        """Kiểm thử chia cho 0: Bắt lỗi ZeroDivisionError và hiển thị thông báo thân thiện."""
        for d in "50":
            self.calc.input_digit(d)
        self.calc.set_operator("/")
        self.calc.input_digit("0")
        self.calc.calculate_equals()
        assert self.calc.has_error is True
        assert "chia cho 0" in self.calc.display_text.lower()

    def test_square_root_negative_number(self):
        """Kiểm thử căn bậc hai số âm: Bắt lỗi toán học không crash ứng dụng."""
        for d in "16":
            self.calc.input_digit(d)
        self.calc.toggle_sign()  # -16
        self.calc.calculate_square_root()
        assert self.calc.has_error is True
        assert "căn số âm" in self.calc.display_text.lower()

    def test_recovery_after_error(self):
        """Sau khi gặp lỗi, người dùng bấm phím số hoặc Clear thì app khôi phục bình thường."""
        # Gây lỗi chia 0
        self.calc.input_digit("8")
        self.calc.set_operator("/")
        self.calc.input_digit("0")
        self.calc.calculate_equals()
        assert self.calc.has_error is True

        # Nhập số mới -> tự động reset trạng thái lỗi
        self.calc.input_digit("9")
        assert self.calc.has_error is False
        assert self.calc.display_text == "9"

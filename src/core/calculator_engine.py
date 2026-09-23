"""
Module chứa bộ xử lý logic tính toán (CalculatorEngine).
Chịu trách nhiệm thực thi các phép tính, xác thực input và xử lý lỗi toán học.
"""

from decimal import Decimal, InvalidOperation, DivisionByZero, Overflow
import math


class CalculatorError(Exception):
    """Lớp ngoại lệ tùy chỉnh cho các lỗi tính toán của máy tính."""
    pass


class CalculatorEngine:
    """
    Engine xử lý logic tính toán mô phỏng máy tính cầm tay tiêu chuẩn.
    Hỗ trợ:
      - Các phép tính cơ bản: +, -, *, /
      - Các phép tính một ngôi: căn bậc hai (√), bình phương (x²), đổi dấu (±), phần trăm (%)
      - Bắt lỗi đầu vào (nhiều dấu chấm, độ dài tối đa)
      - Bắt lỗi tính toán (chia cho 0, căn số âm, tràn số)
    """

    MAX_DIGITS = 16

    def __init__(self):
        self.reset()

    def reset(self):
        """Khởi tạo hoặc đặt lại toàn bộ trạng thái máy tính về ban đầu."""
        self._current_input = "0"
        self._stored_operand = None
        self._pending_operator = None
        self._last_operator = None
        self._last_operand = None
        self._waiting_for_operand = True
        self._has_error = False
        self._error_message = ""
        self._expression_history = ""

    # ----------------- Getters -----------------
    @property
    def display_text(self) -> str:
        """Chuỗi hiển thị trên màn hình chính (kết quả hoặc số đang nhập hoặc thông báo lỗi)."""
        if self._has_error:
            return self._error_message
        return self._current_input

    @property
    def expression_history(self) -> str:
        """Chuỗi hiển thị trên màn hình phụ (biểu thức trước đó)."""
        return self._expression_history

    @property
    def has_error(self) -> bool:
        """Trạng thái có đang gặp lỗi hay không."""
        return self._has_error

    # ----------------- Input Handling & Validation -----------------
    def input_digit(self, digit: str) -> bool:
        """
        Nhập một chữ số (0-9).
        Trả về True nếu input được chấp nhận, False nếu bị chặn do validation.
        """
        if digit not in "0123456789":
            return False

        if self._has_error:
            self.reset()

        if self._waiting_for_operand:
            self._current_input = digit
            self._waiting_for_operand = False
        else:
            # Ngăn nhập quá giới hạn chữ số
            digits_count = len(self._current_input.replace(".", "").replace("-", ""))
            if digits_count >= self.MAX_DIGITS:
                return False

            if self._current_input == "0":
                self._current_input = digit
            else:
                self._current_input += digit

        return True

    def input_decimal_point(self) -> bool:
        """
        Nhập dấu chấm thập phân.
        Bắt lỗi: Không cho phép nhập nhiều dấu chấm trong cùng một toán hạng.
        """
        if self._has_error:
            self.reset()

        if self._waiting_for_operand:
            self._current_input = "0."
            self._waiting_for_operand = False
            return True

        # Validation: Kiểm tra đã có dấu chấm chưa
        if "." in self._current_input:
            return False  # Từ chối nhập thêm dấu chấm

        self._current_input += "."
        return True

    def backspace(self) -> bool:
        """Xóa ký tự cuối cùng vừa nhập."""
        if self._has_error:
            self.reset()
            return True

        if self._waiting_for_operand:
            return False

        if len(self._current_input) > 1:
            self._current_input = self._current_input[:-1]
            if self._current_input == "-" or self._current_input == "":
                self._current_input = "0"
                self._waiting_for_operand = True
        else:
            self._current_input = "0"
            self._waiting_for_operand = True

        return True

    def clear(self):
        """Xóa toàn bộ (Phím C)."""
        self.reset()

    def clear_entry(self):
        """Xóa toán hạng hiện tại (Phím CE)."""
        if self._has_error:
            self.reset()
            return
        self._current_input = "0"
        self._waiting_for_operand = True

    def toggle_sign(self) -> bool:
        """Đổi dấu âm/dương (+/-) của số hiện tại."""
        if self._has_error:
            return False

        if self._current_input == "0" or self._current_input == "0.":
            return True

        if self._current_input.startswith("-"):
            self._current_input = self._current_input[1:]
        else:
            self._current_input = "-" + self._current_input

        return True

    # ----------------- Unary Operations -----------------
    def calculate_percent(self) -> bool:
        """
        Tính phần trăm (%):
        - Nếu đang có phép tính chờ (vd: 200 + 10%): tính 10% của 200 = 20.
        - Nếu đứng một mình: chia số hiện tại cho 100.
        """
        if self._has_error:
            return False

        try:
            curr = Decimal(self._current_input)
            if self._stored_operand is not None and self._pending_operator in ("+", "-"):
                result = (self._stored_operand * curr) / Decimal("100")
            else:
                result = curr / Decimal("100")

            self._current_input = self._format_result(result)
            self._waiting_for_operand = True
            return True
        except (InvalidOperation, DivisionByZero, OverflowError):
            self._set_error("Lỗi tính toán")
            return False

    def calculate_square_root(self) -> bool:
        """Tính căn bậc hai (√). Bắt lỗi căn số âm."""
        if self._has_error:
            return False

        try:
            curr = Decimal(self._current_input)
            if curr < 0:
                self._set_error("Lỗi: Căn số âm")
                return False

            result = curr.sqrt()
            self._expression_history = f"√({self._current_input})"
            self._current_input = self._format_result(result)
            self._waiting_for_operand = True
            return True
        except (InvalidOperation, ValueError):
            self._set_error("Lỗi: Căn số âm")
            return False
        except Overflow:
            self._set_error("Lỗi: Tràn số")
            return False

    def calculate_square(self) -> bool:
        """Tính bình phương (x²)."""
        if self._has_error:
            return False

        try:
            curr = Decimal(self._current_input)
            result = curr ** 2
            self._expression_history = f"sqr({self._current_input})"
            self._current_input = self._format_result(result)
            self._waiting_for_operand = True
            return True
        except (InvalidOperation, Overflow):
            self._set_error("Lỗi: Tràn số")
            return False

    def calculate_reciprocal(self) -> bool:
        """Tính nghịch đảo (1/x). Bắt lỗi chia cho 0."""
        if self._has_error:
            return False

        try:
            curr = Decimal(self._current_input)
            if curr == 0:
                self._set_error("Lỗi: Không thể chia cho 0")
                return False
            result = Decimal(1) / curr
            self._expression_history = f"1/({self._current_input})"
            self._current_input = self._format_result(result)
            self._waiting_for_operand = True
            return True
        except (DivisionByZero, InvalidOperation):
            self._set_error("Lỗi: Không thể chia cho 0")
            return False
        except Overflow:
            self._set_error("Lỗi: Tràn số")
            return False


    # ----------------- Binary Operations -----------------
    def set_operator(self, operator: str) -> bool:
        """
        Thiết lập toán tử (+, -, *, / hoặc ×, ÷).
        Tự động xử lý thay đổi toán tử nếu bấm liên tiếp mà không nhập số.
        """
        op_map = {
            "+": "+",
            "-": "-",
            "*": "×",
            "×": "×",
            "/": "÷",
            "÷": "÷",
        }
        if operator not in op_map:
            return False

        norm_op = op_map[operator]

        if self._has_error:
            self.reset()

        try:
            current_val = Decimal(self._current_input)
        except InvalidOperation:
            self._set_error("Lỗi cú pháp")
            return False

        # Nếu vừa bấm toán tử và lại bấm toán tử khác -> chỉ đổi toán tử đang chờ
        if self._waiting_for_operand and self._pending_operator is not None:
            self._pending_operator = norm_op
            self._expression_history = f"{self._format_result(self._stored_operand)} {norm_op}"
            return True

        if self._stored_operand is None:
            self._stored_operand = current_val
        elif self._pending_operator is not None:
            # Thực hiện phép tính trung gian trước khi gán toán tử mới
            success = self._execute_pending_operation(self._stored_operand, current_val, self._pending_operator)
            if not success:
                return False

        self._pending_operator = norm_op
        self._waiting_for_operand = True
        self._expression_history = f"{self._format_result(self._stored_operand)} {norm_op}"
        return True

    def calculate_equals(self) -> bool:
        """
        Thực hiện phép tính bằng (=).
        Hỗ trợ tính lặp lại phép toán nếu nhấn = nhiều lần liên tiếp.
        """
        if self._has_error:
            return False

        try:
            current_val = Decimal(self._current_input)
        except InvalidOperation:
            self._set_error("Lỗi biểu thức")
            return False

        if self._pending_operator is not None:
            self._last_operator = self._pending_operator
            self._last_operand = current_val
            op = self._pending_operator
            left = self._stored_operand if self._stored_operand is not None else current_val

            self._expression_history = f"{self._format_result(left)} {op} {self._format_result(current_val)} ="
            self._pending_operator = None

            success = self._execute_pending_operation(left, current_val, op)
            if success:
                self._waiting_for_operand = True
            return success
        elif self._last_operator is not None and self._last_operand is not None:
            # Lặp lại phép tính gần nhất
            op = self._last_operator
            right = self._last_operand
            self._expression_history = f"{self._format_result(current_val)} {op} {self._format_result(right)} ="
            success = self._execute_pending_operation(current_val, right, op)
            if success:
                self._waiting_for_operand = True
            return success

        # Nếu không có toán tử nào, giữ nguyên kết quả
        self._expression_history = f"{self._current_input} ="
        self._waiting_for_operand = True
        return True

    # ----------------- Execution & Error Handling -----------------
    def _execute_pending_operation(self, left: Decimal, right: Decimal, operator: str) -> bool:
        """Thực thi phép tính hai ngôi kèm bắt mọi lỗi toán học."""
        try:
            if operator == "+":
                result = left + right
            elif operator == "-":
                result = left - right
            elif operator in ("*", "×"):
                result = left * right
            elif operator in ("/", "÷"):
                if right == 0:
                    self._set_error("Lỗi: Không thể chia cho 0")
                    return False
                result = left / right
            else:
                self._set_error("Lỗi toán tử")
                return False

            self._stored_operand = result
            self._current_input = self._format_result(result)
            return True

        except DivisionByZero:
            self._set_error("Lỗi: Không thể chia cho 0")
            return False
        except (Overflow, OverflowError):
            self._set_error("Lỗi: Tràn số")
            return False
        except InvalidOperation:
            self._set_error("Lỗi tính toán")
            return False
        except Exception as e:
            self._set_error(f"Lỗi: {str(e)}")
            return False

    def _set_error(self, message: str):
        """Đặt trạng thái lỗi an toàn."""
        self._has_error = True
        self._error_message = message
        self._stored_operand = None
        self._pending_operator = None
        self._waiting_for_operand = True

    def _format_result(self, val: Decimal) -> str:
        """Định dạng kết quả số Decimal gọn gàng, tránh sai số và loại bỏ số 0 thừa."""
        if val.is_zero():
            return "0"

        # Kiểm tra nếu số quá lớn hoặc quá nhỏ để chuyển sang scientific notation
        abs_val = abs(val)
        if abs_val >= Decimal("1e15") or (abs_val < Decimal("1e-7")):
            formatted = f"{val:.8E}"
            return formatted

        # Chuẩn hóa (loại bỏ 0 thừa sau dấu phẩy)
        normalized = val.normalize()
        sign, digits, exponent = normalized.as_tuple()
        if exponent >= 0:
            return str(int(normalized))

        s = f"{normalized:f}"
        if "." in s:
            s = s.rstrip("0").rstrip(".")
        return s

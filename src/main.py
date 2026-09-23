"""
File khởi chạy chính của ứng dụng Máy tính cá nhân (PyQt6 Calculator).
"""

import sys
import os

# Đảm bảo đường dẫn thư mục src nằm trong sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from ui.main_window import CalculatorMainWindow


def main():
    """Khởi tạo và chạy ứng dụng PyQt."""
    # Khởi tạo QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("PyQt Personal Calculator")
    app.setOrganizationName("OpenSource")

    # Tạo và hiển thị cửa sổ chính
    window = CalculatorMainWindow()
    window.show()

    # Vòng lặp sự kiện
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

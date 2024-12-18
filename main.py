"""
Entry point for the Task Manager application.
"""

import sys
from PySide6.QtWidgets import QApplication
from application_window import ApplicationWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())

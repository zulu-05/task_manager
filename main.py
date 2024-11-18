import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from calendar_view import CalendarView


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarView()
    window.show()
    sys.exit(app.exec())

import sys
from PySide6.QtWidgets import (
        QMainWindow,
        QCalendarWidget,
        QWidget,
        QVBoxLayout
        )
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()


        self.setWindowTitle("Calendar")
        self.setGeometry(100, 100, 960, 540)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setFirstDayOfWeek(Qt.Monday)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

        layout.addWidget(self.calendar)

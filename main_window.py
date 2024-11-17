from PySide6.QtWidgets import (
        QMainWindow,
        QWidget,
        QVBoxLayout,
        QLabel,
        QPushButton,
        QHBoxLayout
        )
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QIcon
import os


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Calendar")
        self.setGeometry(300, 300, 960, 540)

        self.current_date = QDate.currentDate()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(self.title_label)

        self.day_display = QLabel("No Content")
        self.day_display.setAlignment(Qt.AlignCenter)
        self.day_display.setFont(QFont("Arial", 14))
        main_layout.addWidget(self.day_display)

        nav_layout = QHBoxLayout()

        self.prev_button = QPushButton("<")
        self.prev_button.setFont(QFont("Arial", 14))
        self.prev_button.setFixedSize(50, 50)
        self.prev_button.clicked.connect(self.show_previous_day)
        nav_layout.addWidget(self.prev_button)


        self.next_button = QPushButton(">")
        self.next_button.setFont(QFont("Arial", 14))
        self.next_button.setFixedSize(50, 50)
        self.next_button.clicked.connect(self.show_next_day)
        nav_layout.addWidget(self.next_button)

        main_layout.addLayout(nav_layout)

        self.update_display()


    def update_display(self):

        formatted_date = self.current_date.toString("dddd, MMMM d, yyyy")
        self.title_label.setText(formatted_date)

        self.day_display.setText("No Content")


    def show_previous_day(self):

        self.current_date = self.current_date.addDays(-1)
        self.update_display()


    def show_next_day(self):

        self.current_date = self.current_date.addDays(1)
        self.update_display()


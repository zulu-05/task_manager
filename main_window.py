from PySide6.QtWidgets import (
        QMainWindow,
        QWidget,
        QVBoxLayout,
        QLabel,
        QPushButton,
        QHBoxLayout
        )
from PySide6.QtWidgets import (
        QListWidget,
        QInputDialog,
        QMessageBox,
        QPushButton
        )
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QIcon
import os
import json


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

        self.events_list = QListWidget()
        self.events_list.setFixedHeight(150)
        self.events_list.itemDoubleClicked.connect(self.view_event_details)
        main_layout.addWidget(self.events_list)

        self.add_event_button = QPushButton("Add Event")
        self.add_event_button.clicked.connect(self.add_event)
        main_layout.addWidget(self.add_event_button)

        self.events = {}

        self.load_events()

        self.update_display()


    def update_display(self):

        formatted_date = self.current_date.toString("dddd, MMMM d, yyyy")
        self.title_label.setText(formatted_date)

        self.events_list.clear()
        if self.current_date in self.events:
            for event in self.events[self.current_date]:
                self.events_list.addItem(event)
        else:
            self.events_list.addItem("No Events")

        self.day_display.setText("No Content")


    def show_previous_day(self):

        self.current_date = self.current_date.addDays(-1)
        self.update_display()


    def show_next_day(self):

        self.current_date = self.current_date.addDays(1)
        self.update_display()


    def add_event(self):

        event_text, ok = QInputDialog.getText(self, "Add Event", "Enter event description: ")

        if ok and event_text:
            if self.current_date in self.events:
                self.events[self.current_date].append(event_text)
            else:
                self.events[self.current_date] = [event_text]

            self.update_display()


    def view_event_details(self, item):

        event_text = item.text()
        if event_text != "No Events":
            QMessageBox.information(self, "Event Details", event_text)


    def load_events(self):

        if os.path.exists("events.json"):

            with open("events.json", "r") as f:

                data = json.load(f)

                for date_str, events in data.items():

                    date = QDate.fromString(date_str, "yyyy-MM-dd")
                    
                    if date.isValid():
                        self.events[date] = events


    def save_events(self):

        data = {}

        for date, events in self.events.items():
            
            date_str = date.toString("yyyy-MM-dd")
            data[date_str] = events

        with open("events.json", "w") as f:
            json.dump(data, f, indent=4)


    def closeEvent(self, event):

        self.save_events()
        event.accept()

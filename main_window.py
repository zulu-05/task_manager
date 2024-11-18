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
        QTextEdit,
        QLineEdit,
        QFileDialog
        )
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QIcon, QBrush, QColor
import os
import json
from components.events import Events
from components.todos import Todos
from components.notes import Notes
from components.navigation import Navigation


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

        self.navigation = Navigation(self)
        
        self.prev_button = QPushButton("<")
        self.prev_button.setFont(QFont("Arial", 14))
        self.prev_button.setFixedSize(50, 50)
        self.prev_button.clicked.connect(self.on_prev_button_clicked)
        nav_layout.addWidget(self.prev_button)

        self.today_button = QPushButton("Today")
        self.today_button.setFont(QFont("Arial", 12))
        self.today_button.setFixedSize(100, 50)
        self.today_button.clicked.connect(self.on_today_button_clicked)
        nav_layout.addWidget(self.today_button)

        self.next_button = QPushButton(">")
        self.next_button.setFont(QFont("Arial", 14))
        self.next_button.setFixedSize(50, 50)
        self.next_button.clicked.connect(self.on_next_button_clicked)
        nav_layout.addWidget(self.next_button)

        main_layout.addLayout(nav_layout)

        self.events = Events(self)

        self.events_list = QListWidget()
        self.events_list.setFixedHeight(150)
        self.events_list.itemDoubleClicked.connect(self.on_event_double_clicked)
        main_layout.addWidget(QLabel("Events: "))
        main_layout.addWidget(self.events_list)

        self.add_event_button = QPushButton("Add Event")
        self.add_event_button.clicked.connect(self.on_add_event_clicked)
        main_layout.addWidget(self.add_event_button)

        self.todos = Todos(self)

        self.todo_list = QListWidget()
        self.todo_list.setFixedHeight(100)
        self.todo_list.itemDoubleClicked.connect(self.on_todo_double_clicked)
        main_layout.addWidget(QLabel("To-Do List:"))
        main_layout.addWidget(self.todo_list)

        self.add_todo_button = QPushButton("Add To-Do")
        self.add_todo_button.clicked.connect(self.on_add_todo_clicked)
        main_layout.addWidget(self.add_todo_button)

        self.notes = Notes(self)

        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Add your notes here...")
        self.notes_edit.textChanged.connect(self.on_notes_changed)
        main_layout.addWidget(QLabel("Notes: "))
        main_layout.addWidget(self.notes_edit)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search events...")
        main_layout.addWidget(self.search_bar)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.on_search_button_clicked)
        main_layout.addWidget(self.search_button)

        self.search_results = QListWidget()
        self.search_results.setFixedHeight(100)
        self.search_results.itemClicked.connect(self.on_search_result_clicked)
        main_layout.addWidget(QLabel("Search Results: "))
        main_layout.addWidget(self.search_results)

        self.export_button = QPushButton("Export Events")
        self.export_button.clicked.connect(self.on_export_button_clicked)
        main_layout.addWidget(self.export_button)

        stylesheet_path = os.path.join("styles", "style.qss")
        self.apply_stylesheet(stylesheet_path)

        self.update_display()


    def on_prev_button_clicked(self):

        self.navigation.show_previous_day()


    def on_next_button_clicked(self):

        self.navigation.show_next_day()


    def on_today_button_clicked(self):

        self.navigation.go_to_today()


    def on_add_event_clicked(self):

        self.events.add_event()


    def on_event_double_clicked(self, item):

        self.events.view_event_details(item)


    def on_add_todo_clicked(self):
        
        self.todos.add_todo()


    def on_todo_double_clicked(self, item):

        self.todos.view_todo_details(item)


    def on_notes_changed(self):

        text = self.notes_edit.toPlainText()
        self.notes.set_note(text)


    def on_search_button_clicked(self):

        query = self.search_bar.text().strip().lower()
        self.searh_results.clear()

        if not query:
            self.search_results.addItem("Please Enter a search term.")
            return

        found = False
        for date, events in self.events.events.items():
            for event in events:
                if query in event.lower():
                    formatted_date = self.format_date(date)
                    self.search_results.addItem(f"{formatted_date}: {event}")
                    found = True

        if not found:
            self.search_results.addItem("No matching events found.")


    def on_search_result_clicked(self, item):

        text = item.text()
        if text in ["Please enter a search term.", "No matching events found."]:
            return

        date_str = text.split(":")[0]
        date = self.parse_date_srt(date_str)
        if date and self.min_date <= date <= self.max_date:
            self.current_date = date
            self.update_display()
        else:
            QMessageBox.warning(self, "Invalid Date", "Unable to parse the date from the search result.")


    def on_export_button_clicked(self):

        path, _ = QFileDialog.getSaveFileName(self, "Save Events", "", "CSV Files (*.csv)")
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write("Date, Event\n")
                    for date, events in self.events.events.items():
                        date_str = self.format_date(date)
                        for event in events:
                            f.write(f'"{date_str}","{event}"\n')
                QMessageBox.information(self, "Export Successful", f"Events exported to {path}")
            except Exception as e:
                QMessageBox.warning(self, "Export Failed", f"An error occurred while exporting events:\n{e}")


    def format_date(self, date):

        return date.toString("dddd, MMMM d, yyyy")


    def parse_date_str(self, date_str):

        date = QDate.fromString(date_str, "dddd, MMMM d, yyyy")
        if date.isValid():
            return date
        else:
            return None


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


    def apply_stylesheet(self, stylesheet_path):

        if os.path.exists(stylesheet_path):
            try:
                with open(stylesheet_path, "r") as f:
                    stylesheet = f.read()
                    self.setStyleSheet(stylesheet)
            except Exception as e:
                QMessageBox.warning(self, "Stylesheet Error", f"Failed to apply stylesheet:\n{e}")
        else:
            QMessageBox.warning(self, "Stylesheet Missing", f"Stylesheet not found at {stylesheet_path}")


    def closeEvent(self, event):

        self.events.save_events()
        self.todos.save_todos()
        self.notes.save_notes()
        event.accept()

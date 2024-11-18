from PySide6.QtWidgets import QListWidgetItem, QMessageBox, QInputDialog
from PySide6.QtGui import QBrush, QColor
import json
import os


class Events:

    def __init__(self, main_window):

        self.main_window = main_window
        self.events = {}
        self.load_events()


    def load_events(self):

        if os.path.exists("events.json"):
            try:
                with open("events.json", "r") as f:
                    data = json.load(f)
                    for date_str, events in data.items():
                        date = self.main_window.parse_date_str(date_str)
                        if date:
                            self.events[date] = events
            except json.JSONDecodeError:
                QMessageBox.warning(self.main_window, "Load Error", "Failed to parse events.json. Please check the file format.")


    def save_events(self):

        data = {}
        for date, events in self.events.items():
            date_str = self.main_window.format_date(date)
            data[date_str] = events
        try:
            with open("events.json", "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            QMessage.warning(self.main_window, "Save Error", f"Failed to save events: {e}")


    def add_event(self):

        event_text, ok = QInputDialog.getText(self.main_window, "Add Event", "Enter event description: ")

        if ok and event_text:
            event_type, ok_type = QInputDialog.getItem(
                self.main_window, "Select Event Type", "Event Type: ",
                ["Work", "Personal", "Holiday", "Other"], 0, False
            )
            if ok_type and event_type:
                full_event_text = f"{event_text} ({event_type})"
            else:
                full_event_text = event_text

            date = self.main_window.current_date
            if date in self.events:
                self.events[date].append(full_event_text)
            else:
                self.events[date] = [full_event_text]

            self.main_window.update_display()


    def view_event_details(self, item):

        event_text = item.text()
        if event_text != "No Events":
            QMessageBox.information(self.main_window, "Event Details", event_text)


    def populate_events_list(self):

        self.main_window.events_list.clear()
        date = self.main_window.current_date
        if date in self.events:
            for event in self.events[date]:
                item = QListWidgetItem(event)

                if "(Work)" in event:
                    item.setForeground(QBrush(QColor("#1E90FF")))
                elif "(Personal)" in event:
                    item.setForeground(QBrush(QColor("#32CD32")))
                elif "(Holiday)" in event:
                    item.setForeground(QBrush(QColor("#FFD700")))
                else:
                    item.setForeground(QBrush(QColor("#808080")))
                self.main_window.events_list.addItem(item)
        else:
            self.main_window.events_list.addItem("No Events")

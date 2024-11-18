from PySide6.QtWidgets import QMessageBox
import json
import os


class Notes:
    
    def __init__(self, main_window):

        self.main_window = main_window
        self.notes = {}
        self.load_notes()


    def load_notes(self):

        if os.path.exists("notes.json"):
            try:
                with open("notes.json", "r") as f:
                    data = json.load(f)
                    for date_str, note in data.items():
                        date = self.main_window.parse_date_str(date_str)
                        if date:
                            self.notes[date] = note
            except json.JSONDecodeError:
                QMessageBox.warning(self.main_window, "Load Error", "Failed to parse notes.json. Please check the file format.")


    def save_notes(self):

        data = {}
        for date, note in self.notes.items():
            date_str = self.main_window.format_date(date)
            data[date_str] = note
        try:
            with open("notes.json", "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            QMessageBox.warning(self.main_window, "Save Error", f"Failed to save notes: {e}")


    def set_note(self, text):

        date = self.main_window.current_date
        if text.strip():
            self.notes[date] = text
        elif date in self.notes:
            del self.notes[date]

        self.main_window.update_display()


    def populate_notes_edit(self):

        self.main_window.notes_edit.blockSignals(True)
        date = self.main_window.current_date
        if date in self.notes:
            self.main_window.notes_edit.setPlainText(self.notes[date])
        else:
            self.main_window.notes_edit.setPlainText("")
        self.main_window.notes_edit.blockSignals(False)



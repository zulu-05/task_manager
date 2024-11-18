from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QDate


class Navigation:

    def __init__(self, main_window):
            
        self.main_window = main_window
        self.min_date = QDate(2000, 1, 1)
        self.max_date = QDate(2099, 12, 31)

        today = QDate.currentDate()
        if today < self.min_date:
            self.main_window.current_date = self.min_date
        elif today > self.max_date:
            self.main_window.current_date = self.max_date
        else:
            self.main_window.current_date = today


    def show_previous_day(self):

        new_date = self.main_window.current_date.addDays(-1)
        if new_date < self.min_date:
            QMessageBox.warning(self.main_window, "Date Limit", "Cannot navigate to a date earlier than January 1, 2000.")
        else:
            self.main_window.current_date = new_date
            self.main_window.update_display()


    def show_next_day(self):

        new_date = self.main_window.current_date.addDays(1)
        if new_date > self.max_date:
            QMessageBox.warning(self.main_window, "Date Limit", "Cannot navigate to a date beyond December 31, 2099.")
        else:
            self.main_window.current_date = new_date
            self.main_window.update_display()


    def go_to_today(self):

        today = QDate.currentDate()
        if today < self.min_date:
            self.main_window.current_date = self.min_date
            QMessageBox.information(self.main_window, "Date Adjusted", "Today's date is earlier than the minimum allowed date. Navigated to January 1, 2000.")
        elif today > self.max_date:
            self.main_window.current_date = self.max_date
            QMessageBox.information(self.main_window, "Date Adjusted", "Today's date is beyond the maximum allowed date. Navigated to December 31, 2099.")
        else:
            self.main_window.current_date = today
        self.main_window.update_display()


    def update_button_states(self):

        if self.main_window.current_date <= self.min_date:
            self.main_window.prev_button.setEnabled(False)
        else:
            self.main_window.prev_button.setEnabled(True)

        if self.main_window.current_date >= self.max_date:
            self.main_window.next_button.setEnabled(False)
        else:
            self.main_window.next_button.setEnabled(True)

        if self.main_window.current_date == QDate.currentDate():
            self.main_window.today_button.setEnabled(False)
        else:
            self.main_window.today_button.setEnabled(True)


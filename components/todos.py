from PySide6.QtWidgets import QListWidgetItem, QMessageBox, QInputDialog
import json
import os


class Todos:

    def __init__(self, main_window):

        self.main_window = main_window
        self.todos = {}
        self.load_todos()


    def load_todos(self):

        if os.path.exists("todos.json"):
            try:
                with open("todos.json", "r") as f:
                    data = json.load(f)
                    for date_str, todos in data.items():
                        date = self.main_window.parse_date_str(date_str)
                        if date:
                            self.todos[date] = todos
            except json.JSONDecodeError:
                QMessageBox.warning(self.main_window, "Load Error", "Failed to parse todos.json. Please check the file format.")


    def save_todos(self):

        data = {}
        for date, todos in self.todos.items():
            date_str = self.main_window.format_date(date)
            data[date_str] = todos
        try:
            with open("todos.json", "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            QMessageBox.warning(self.main_window, "Save Error", f"Failed to save to-dos: {e}")


    def add_todo(self):

        todo_text, ok = QInputDialog.getText(self.main_window, "Add To-Do", "Enter to-do item: ")

        if ok and todo_text:
            date = self.main_window.current_date
            if date in self.todos:
                self.todos[date].append(todo_text)
            else:
                self.todos[date] = [todo_text]

            self.main_window.update_display()


    def view_todo_details(self, item):

        todo_text = item.text()
        if todo_text != "No To-do Items":
            QMessageBox.information(self.main_window, "To-Do Details", todo_text)


    def populate_todos_list(self):

        self.main_window.todo_list.clear()
        date = self.main_window.current_date
        if date in self.todos:
            for todo in self.todos[date]:
                self.main_window.todo_list.addItem(todo)
        else:
            self.main_window.todo_list.addItem("No To-Do Items")


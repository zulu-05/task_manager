import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QListWidget
from PyQt5.QtWidgets import QLineEdit, QLabel


class TaskManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 
        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 400, 300)

        # 
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)

        # 
        self.task_list = QListWidget()
        self.layout.addWidget(self.task_list)

        # 
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter new task")
        self.layout.addWidget(self.task_input)

        # 
        self.add_task_button = QPushButton("Add task")
        self.add_task_button.clicked.connect(self.add_task)
        self.layout.addWidget(self.add_task_button)

        self.setCentralWidget(self.central_widget)


    def add_task(self):
        task = self.task_input.text()
        if task:
            self.task_list.addItem(task)
            self.task_input.clear()


import sys
from PyQt5.QtWidgets import QApplication
from main_window import TaskManagerWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManagerWindow()
    window.show()
    sys.exit(app.exec_())



from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout
    )
from calendar_view import CalendarView
from digital_clock import DigitalClock


class ApplicationWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("Task Manager")
        self.resize(800, 600)
        self.init_ui()


    def init_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.calendar_view = CalendarView('day')

        btn_day = QPushButton("Day View")
        btn_week = QPushButton("Week View")
        btn_month = QPushButton("Month View")

        btn_day.clicked.connect(lambda: self.switch_view('day'))
        btn_week.clicked.connect(lambda: self.switch_view('week'))
        btn_month.clicked.connect(lambda: self.switch_view('month'))

        button_layout = QHBoxLayout()
        button_layout.addWidget(btn_day)
        button_layout.addWidget(btn_week)
        button_layout.addWidget(btn_month)

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.calendar_view)

        self.digital_clock = DigitalClock(format='HH:mm:ss.zzz')
        self.digital_clock.setStyleSheet("font-size: 16px; color: blue;")
        main_layout.addWidget(self.digital_clock)

        main_layout.setAlignment(self.digital_clock, Qt.AlignTop | Qt.AlignLeft)

        central_widget.setLayout(main_layout)


    def switch_view(self, view_mode):

        self.calendar_view.view_mode = view_mode
        self.calendar_view.init_grid()

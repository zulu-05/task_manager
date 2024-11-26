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

        self.digital_clock = DigitalClock(format='HH:mm:ss.zzz')
        self.digital_clock.setStyleSheet("font-size: 16px; color: blue;")
        main_layout.setAlignment(self.digital_clock, Qt.AlignTop | Qt.AlignLeft)

        self.date_range_label = QLabel()
        self.date_range_label.setAlignment(Qt.AlignCenter)
        self.date_range_label.setStyleSheet("font-size: 14px; font-weight: bold;")

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.digital_clock)
        top_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.date_range_label)
        main_layout.addWidget(self.calendar_view)

        central_widget.setLayout(main_layout)


    def switch_view(self, view_mode):

        self.animation = QPropertyAnimation(self.calendar_view, b"geometry")
        self.animation.setDuration(500)
        self.animation.setStartValue(self.calendar_view.geometry())

        end_rect = self.calendar_view.geometry()
        end_rect.setWidth(end_rect.width() * 1.05)
        end_rect.setHeight(end_rect.height() * 1.05)

        self.animation.setEndValue(end_rect)
        self.animation.finished.connect(lambda: self.finish_switch_view(view_mode))
        self.animation.start()


    def finish_switch_view(self, view_mode):

        self.calendar_view.view_mode = view_mode
        self.calendar_view.current_date = QDate.currentDate()
        self.calendar_view.init_grid()

        self.animation = QPropertyAnimation(self.calendar_view, b"geometry")
        self.animation.setDuration(500)

        start_rect = self.calendar_view.geometry()
        end_rect = self.calendar_view.geometry()
        start_rect.setWidth(start_rect.width() * 1.05)
        start_rect.setHeight(start_rect.height() * 1.05)

        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()

        if view_mode == 'week':

            start_date = self.calendar_view.current_date
            end_date = start_date.addDays(6)
            date_range = (
                f"{start_date.toString('MMM dd')} - "
                f"{end_date.toString('MMM dd')}"
            )
            self.date_range_label.setText(date_range)
        
        else:

            self.date_range_label.setText('')
